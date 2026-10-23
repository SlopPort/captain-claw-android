package pl.pazur.port;

import android.app.*;
import android.content.*;
import android.net.Uri;
import android.os.Bundle;
import java.io.*;

/** Codex (LLM): deterministic save export completion after Activity destruction.
 * A test provider gates openOutputStream until onActivityDestroyed; no user
 * file is overwritten and no real picker UI or controller input is claimed. */
public class LateSaveActivityTest extends Instrumentation {
    private Bundle args;
    @Override public void onCreate(Bundle value){super.onCreate(value);args=value;start();}
    @Override public void onStart() {
        Bundle result=new Bundle();final Activity[] screen={null};
        java.util.concurrent.CountDownLatch destroyed=new java.util.concurrent.CountDownLatch(1);
        Application app=(Application)getTargetContext().getApplicationContext();
        Uri uri=Uri.parse(args.getString("uri"));String token=args.getString("token");
        Application.ActivityLifecycleCallbacks observer=new Application.ActivityLifecycleCallbacks() {
            public void onActivityDestroyed(Activity a){if(a==screen[0])destroyed.countDown();}
            public void onActivityCreated(Activity a,Bundle b){}
            public void onActivityStarted(Activity a){}
            public void onActivityResumed(Activity a){}
            public void onActivityPaused(Activity a){}
            public void onActivityStopped(Activity a){}
            public void onActivitySaveInstanceState(Activity a,Bundle b){}
        };
        app.registerActivityLifecycleCallbacks(observer);
        try {
            byte[] canonical;try(InputStream in=new FileInputStream(new File(getTargetContext().getExternalFilesDir(null),"SAVES.XML"))){canonical=SaveFiles.validate(in);}
            byte[] digest=java.security.MessageDigest.getInstance("SHA-256").digest(canonical);StringBuilder hex=new StringBuilder();
            for(byte b:digest)hex.append(String.format("%02x",b&255));
            Bundle status=new Bundle();status.putString("expected_export_sha256",hex.toString());sendStatus(0,status);
            getTargetContext().getContentResolver().call(uri,"reset_export",token,null);
            screen[0]=startActivitySync(new Intent(getTargetContext(),FileToolsActivity.class).setAction(Intent.ACTION_MAIN)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK|Intent.FLAG_ACTIVITY_CLEAR_TOP));
            runOnMainSync(()-> {
                try {
                    java.lang.reflect.Method callback=FileToolsActivity.class.getDeclaredMethod("onActivityResult",int.class,int.class,Intent.class);
                    callback.setAccessible(true);callback.invoke(screen[0],1,Activity.RESULT_OK,new Intent().setData(uri));
                    screen[0].finish();
                } catch(Exception error){throw new RuntimeException(error);}
            });
            if(!destroyed.await(6,java.util.concurrent.TimeUnit.SECONDS))throw new Exception("Save tools did not reach onActivityDestroyed");
            waitForIdleSync();
            getTargetContext().getContentResolver().call(uri,"release_export",token,null);
            Thread.sleep(1200);waitForIdleSync();
            byte[] expected;try(InputStream in=new FileInputStream(new File(getTargetContext().getExternalFilesDir(null),"SAVES.XML"))){expected=SaveFiles.validate(in);}
            byte[] actual;try(InputStream in=getTargetContext().getContentResolver().openInputStream(uri);ByteArrayOutputStream out=new ByteArrayOutputStream()) {
                byte[] block=new byte[4096];int n;while((n=in.read(block))!=-1)out.write(block,0,n);actual=out.toByteArray();
            }
            if(!java.util.Arrays.equals(expected,actual))throw new Exception("Export bytes differ");
            result.putString("late_save","PASS: export completed after actual Activity destruction; no late dialog crash");
        } catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));}
        finally {
            app.unregisterActivityLifecycleCallbacks(observer);
            try{getTargetContext().getContentResolver().call(uri,"release_export",token,null);}catch(Exception ignored){}
            if(screen[0]!=null)runOnMainSync(screen[0]::finish);
        }
        finish(result.containsKey("error")?1:0,result);
    }
}
