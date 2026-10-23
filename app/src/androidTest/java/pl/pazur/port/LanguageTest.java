package pl.pazur.port;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import java.io.*;
import java.util.Arrays;

/** Real activity/resource checks, restoring the user's language and files.
 * Codex (LLM): does not press global keys, import data, or change bindings.
 */
public class LanguageTest extends Instrumentation {
    private boolean previewNative;
    private boolean checkFileFooter;
    private View exactText(View view,String text) {
        if(view instanceof TextView && ((TextView)view).getText().toString().equals(text))return view;
        if(view instanceof ViewGroup) {
            ViewGroup group=(ViewGroup)view;
            for(int i=0;i<group.getChildCount();i++) {
                View found=exactText(group.getChildAt(i),text);if(found!=null)return found;
            }
        }
        return null;
    }
    private void requireFileFooter(Activity screen) throws Exception {
        boolean[] visible={false};
        for(int attempt=0;attempt<40;attempt++) {
            runOnMainSync(()-> {
                View button=exactText(screen.getWindow().getDecorView(),screen.getString(R.string.back));
                if(button==null||button.getWidth()==0||button.getHeight()==0)return;
                // Request the real parent hierarchy to reveal this control;
                // presence in the view tree alone does not prove reachability.
                button.requestRectangleOnScreen(new android.graphics.Rect(0,0,button.getWidth(),button.getHeight()),true);
                android.graphics.Rect bounds=new android.graphics.Rect();
                visible[0]=button.getGlobalVisibleRect(bounds)&&bounds.height()>=button.getHeight()&&bounds.width()>=button.getWidth();
            });
            if(visible[0])return;
            Thread.sleep(50);
        }
        throw new Exception("File-tools Back button cannot be fully revealed: "+AppLanguage.code(screen));
    }
    private byte[] bytes(File file) throws IOException {
        if(!file.exists())return null;
        try(InputStream in=new FileInputStream(file);ByteArrayOutputStream out=new ByteArrayOutputStream()) {
            byte[] buffer=new byte[4096];int n;while((n=in.read(buffer))!=-1)out.write(buffer,0,n);
            return out.toByteArray();
        }
    }
    private boolean contains(View view,String text) {
        if(view instanceof TextView && ((TextView)view).getText().toString().contains(text))return true;
        if(view instanceof ViewGroup) {
            ViewGroup group=(ViewGroup)view;
            for(int i=0;i<group.getChildCount();i++)if(contains(group.getChildAt(i),text))return true;
        }
        return false;
    }
    @Override public void onCreate(Bundle args){super.onCreate(args);previewNative=args!=null&&"true".equals(args.getString("preview_native"));checkFileFooter=args!=null&&"true".equals(args.getString("check_file_footer"));start();}
    @Override public void onStart() {
        Bundle result=new Bundle();Context context=getTargetContext();
        SharedPreferences prefs=context.getSharedPreferences("interface",Context.MODE_PRIVATE);
        String original=prefs.getString("language",null);
        File root=context.getExternalFilesDir(null),nativeFile=new File(root,"ui-language.txt");
        byte[] previous=null,bindings=null,saves=null;boolean backedUp=false;Activity current=null;
        try {
            if(previewNative)getUiAutomation(); // Connect before opening SDL, not during the captured frame.
            previous=bytes(nativeFile);bindings=bytes(new File(root,"controller-bindings.txt"));
            saves=bytes(new File(root,"SAVES.XML"));backedUp=true;
            for(String code:new String[]{"en","pl"}) {
                if(!prefs.edit().putString("language",code).commit())throw new Exception("Preference not saved");
                Context localized=AppLanguage.wrap(context);
                String jump=localized.getString(R.string.action_jump);
                if(!jump.equals(code.equals("en")?"Jump":"Skok"))throw new Exception("Wrong resources: "+jump);
                AppLanguage.writeNative(localized);
                if(!new String(bytes(nativeFile),"US-ASCII").equals(code))throw new Exception("Wrong native locale");
                current=startActivitySync(new Intent(context,ControllerSettingsActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                final Activity screen=current;final boolean[] visible={false};
                runOnMainSync(()->visible[0]=contains(screen.getWindow().getDecorView(),code.equals("en")?"Sword attack":"Atak szablą"));
                if(!visible[0])throw new Exception("Settings translation not visible: "+code);
                runOnMainSync(screen::finish);current=null;waitForIdleSync();
                current=startActivitySync(new Intent(context,FileToolsActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                final Activity files=current;
                runOnMainSync(()->visible[0]=contains(files.getWindow().getDecorView(),code.equals("en")?"Export progress to file":"Zapisz kopię postępu do pliku"));
                if(!visible[0])throw new Exception("File tools translation not visible: "+code);
                if(checkFileFooter)requireFileFooter(files);
                runOnMainSync(files::finish);current=null;waitForIdleSync();
            }
            if(!Arrays.equals(bindings,bytes(new File(root,"controller-bindings.txt"))) ||
               !Arrays.equals(saves,bytes(new File(root,"SAVES.XML"))))throw new Exception("User progress or bindings changed");
            current=startActivitySync(new Intent(context,ControllerSettingsActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            final Activity chooser=current;
            final android.app.AlertDialog[] dialog={null};
            runOnMainSync(()->dialog[0]=AppLanguage.choose(chooser));waitForIdleSync();
            final Activity[] replacement={null};
            java.util.concurrent.CountDownLatch resumed=new java.util.concurrent.CountDownLatch(1);
            android.app.Application application=(android.app.Application)context.getApplicationContext();
            // ActivityMonitor is unreliable for recreate() on API 21. Observe
            // the application's real lifecycle and require a different instance.
            android.app.Application.ActivityLifecycleCallbacks lifecycle=new android.app.Application.ActivityLifecycleCallbacks() {
                public void onActivityResumed(Activity a){if(a instanceof ControllerSettingsActivity && a!=chooser){replacement[0]=a;resumed.countDown();}}
                public void onActivityCreated(Activity a,Bundle b){}
                public void onActivityStarted(Activity a){}
                public void onActivityPaused(Activity a){}
                public void onActivityStopped(Activity a){}
                public void onActivitySaveInstanceState(Activity a,Bundle b){}
                public void onActivityDestroyed(Activity a){}
            };
            application.registerActivityLifecycleCallbacks(lifecycle);
            try {
                runOnMainSync(()->dialog[0].getListView().performItemClick(null,1,1));
                if(!resumed.await(10,java.util.concurrent.TimeUnit.SECONDS))throw new Exception("Recreated settings did not resume");
            } finally {application.unregisterActivityLifecycleCallbacks(lifecycle);}
            current=replacement[0];
            if(!AppLanguage.code(current).equals("en"))throw new Exception("Language choice not persisted");
            waitForIdleSync();
            final Activity selected=current;final boolean[] translated={false};
            runOnMainSync(()->translated[0]=contains(selected.getWindow().getDecorView(),"Sword attack"));
            if(!translated[0])throw new Exception("Selection did not refresh visible text: "+selected.getString(R.string.action_attack));
            runOnMainSync(selected::finish);current=null;waitForIdleSync();
            if(previewNative) {
                // Caller must isolate config/saves. Capture before restoring the
                // preference; no global input or changes to original game data.
                File preview=new File(root,"language-english-native.png");
                if(preview.exists())throw new IOException("Preview already exists");
                prefs.edit().putString("language","en").commit();
                ActivityMonitor monitor=addMonitor("pl.pazur.port.GameActivity",null,false);
                context.startActivity(new Intent(context,LauncherActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                Activity game=waitForMonitorWithTimeout(monitor,30000);
                if(game==null)throw new IOException("Game did not open");
                android.os.SystemClock.sleep(7000);
                waitForIdleSync();
                final boolean[] overlay={false};
                runOnMainSync(()->overlay[0]=game.hasWindowFocus()&&contains(game.getWindow().getDecorView(),"PAD"));
                if(!overlay[0])throw new IOException("Game window/Android overlay not ready for preview");
                android.graphics.Bitmap image=getUiAutomation().takeScreenshot();
                if(image==null)throw new IOException("Screenshot unavailable");
                try(OutputStream out=new FileOutputStream(preview)){image.compress(android.graphics.Bitmap.CompressFormat.PNG,100,out);}
                finally{image.recycle();}
                result.putString("preview","English native screenshot captured; visual review required");
            }
            result.putString("language","PASS: PL/EN resources, actual settings/file screens, native preference; saves and bindings unchanged");
        } catch(Throwable error) {result.putString("error",android.util.Log.getStackTraceString(error));}
        finally {
            try {
                if(current!=null){final Activity screen=current;runOnMainSync(screen::finish);}
                SharedPreferences.Editor edit=prefs.edit();if(original==null)edit.remove("language");else edit.putString("language",original);
                if(!edit.commit())throw new IOException("Cannot restore language preference");
                if(backedUp) {
                    if(previous==null){if(nativeFile.exists()&&!nativeFile.delete())throw new IOException("Cannot restore native preference");}
                    else try(FileOutputStream out=new FileOutputStream(nativeFile)){out.write(previous);}
                }
            } catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));}
        }
        finish(result.containsKey("error")?1:0,result);
    }
}
