package pl.pazur.port;

import android.app.Instrumentation;
import android.os.Bundle;
import java.io.*;
import java.util.*;

/** Kills only this app's instrumented process, with tiny isolated fixture files.
 * The real game data/progress are never imported or renamed by this test. */
public class ImportRecoveryTest extends Instrumentation {
    private Bundle args;
    @Override public void onCreate(Bundle value){super.onCreate(value);args=value;start();}
    private void write(File file,String text) throws IOException {
        try(FileOutputStream out=new FileOutputStream(file)){out.write(text.getBytes("UTF-8"));out.getFD().sync();}
    }
    private void verify(File file,String text) throws IOException {
        byte[] expected=text.getBytes("UTF-8"),actual=new byte[expected.length];
        try(InputStream in=new FileInputStream(file)) {
            int offset=0,count;while(offset<actual.length&&(count=in.read(actual,offset,actual.length-offset))>0)offset+=count;
            if(offset!=actual.length||in.read()!=-1||!Arrays.equals(expected,actual))throw new AssertionError("Changed: "+file.getName());
        }
    }
    @Override public void onStart() {
        Bundle result=new Bundle();
        try {
            String phase=args.getString("phase","verify"),mode=args.getString("mode","partial");
            if(!Arrays.asList("empty","partial","full").contains(mode))throw new AssertionError("mode");
            File root=new File(getTargetContext().getExternalFilesDir(null),"import-transaction-test");
            if(phase.equals("kill-publish")) {
                if(!root.mkdir())throw new IOException("Refusing existing fixture");
                write(new File(root,"fixture-owner"),"Codex import test "+mode);
                write(new File(root,"SAVES.XML"),"untouched progress");
                File stage=ImportTransaction.freshStage(root);
                for(int i=0;i<ImportTransaction.REQUIRED.length;i++) {
                    String name=ImportTransaction.REQUIRED[i];
                    if(mode.equals("full")||(mode.equals("partial")&&i%2==0))write(new File(root,name),"old "+name);
                    write(new File(stage,name),"new "+name);
                }
                ImportTransaction.commit(root,stage,step->{if(step.equals("published:config.xml"))android.os.Process.killProcess(android.os.Process.myPid());});
                throw new AssertionError("Expected process termination");
            }
            verify(new File(root,"fixture-owner"),"Codex import test "+mode);
            if(phase.equals("kill-recover")) {
                ImportTransaction.recover(root,step->{if(step.equals("restored:ASSETS.ZIP"))android.os.Process.killProcess(android.os.Process.myPid());});
                throw new AssertionError("Expected recovery termination");
            }
            if(!phase.equals("verify"))throw new AssertionError("phase");
            ImportTransaction.recover(root);ImportTransaction.recover(root);
            for(int i=0;i<ImportTransaction.REQUIRED.length;i++) {
                String name=ImportTransaction.REQUIRED[i];File file=new File(root,name);
                if(mode.equals("full")||(mode.equals("partial")&&i%2==0))verify(file,"old "+name);
                else if(file.exists())throw new AssertionError("New data survived rollback: "+name);
            }
            verify(new File(root,"SAVES.XML"),"untouched progress");
            // freshStage removes only known staged names and refuses unknown files.
            File stage=ImportTransaction.freshStage(root);
            if(!stage.delete())throw new IOException("stage cleanup");
            for(File file:root.listFiles())if(!file.delete())throw new IOException("fixture cleanup");
            if(!root.delete())throw new IOException("root cleanup");
            result.putString("recovery","PASS: "+mode+", actual process death during publish and recovery; original set and save preserved");
            finish(0,result);
        }catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));finish(1,result);}
    }
}
