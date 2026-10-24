package pl.pazur.port;

import android.app.*;
import android.content.*;
import android.graphics.*;
import android.os.Bundle;
import android.view.View;
import java.io.*;

/** Capture only the app's own importer views for the public installation guide.
 * OpenAI Codex (LLM). Host isolates one missing required file and restores it.
 * No game assets, system notifications, picker contents or user files are imaged.
 * The original language preference is restored even after a failed capture. */
public class InstallGuideTest extends Instrumentation {
    private void capture(View view, String name) throws Exception {
        final Exception[] error={null};
        runOnMainSync(()-> {
            try {
                if(view.getWidth()<1 || view.getHeight()<1)throw new IOException("View not laid out");
                Bitmap image=Bitmap.createBitmap(view.getWidth(),view.getHeight(),Bitmap.Config.ARGB_8888);
                view.draw(new Canvas(image));
                try(OutputStream out=new FileOutputStream(new File(getTargetContext().getExternalFilesDir(null),name))) {
                    if(!image.compress(Bitmap.CompressFormat.PNG,100,out))throw new IOException("PNG failed");
                } finally {image.recycle();}
            } catch(Exception e){error[0]=e;}
        });
        if(error[0]!=null)throw error[0];
    }
    @Override public void onCreate(Bundle args){super.onCreate(args);start();}
    @Override public void onStart() {
        Context context=getTargetContext();
        android.content.SharedPreferences prefs=context.getSharedPreferences("interface",Context.MODE_PRIVATE);
        String old=prefs.getString("language",null);
        Activity activity=null;AlertDialog[] dialog={null};
        ActivityMonitor nativeGame=addMonitor(GameActivity.class.getName(),new ActivityResult(Activity.RESULT_CANCELED,null),true);
        Bundle result=new Bundle();int code=0;
        try {
            if(!prefs.edit().putString("language","en").commit())throw new IOException("Cannot select English");
            activity=startActivitySync(new Intent(context,LauncherActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            final Activity screen=activity;
            for(int i=0;i<100;i++) {
                boolean[] ready={false};
                runOnMainSync(()->ready[0]=screen.findViewById(android.R.id.content).getHeight()>0);
                if(ready[0])break;Thread.sleep(50);
            }
            Thread.sleep(1000);waitForIdleSync();
            if(nativeGame.getHits()>0)throw new IOException("Host did not isolate importer");
            capture(screen.getWindow().getDecorView(),"guide-importer-en.png");
            runOnMainSync(()->dialog[0]=AppLanguage.choose(screen));waitForIdleSync();Thread.sleep(300);
            capture(dialog[0].getWindow().getDecorView(),"guide-language-en.png");
            result.putString("guide","PASS: English importer and language dialog captured; visual review required");
        } catch(Exception e){code=1;result.putString("error",e.toString());}
        finally {
            final Activity screen=activity;
            runOnMainSync(()->{if(dialog[0]!=null)dialog[0].dismiss();if(screen!=null)screen.finish();});
            android.content.SharedPreferences.Editor edit=prefs.edit();
            if(old==null)edit.remove("language");else edit.putString("language",old);
            if(!edit.commit()){code=1;result.putString("restore","Language restoration failed");}
            removeMonitor(nativeGame);
        }
        finish(code,result);
    }
}
