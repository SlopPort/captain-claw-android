package pl.pazur.port;

import android.app.Instrumentation;
import android.os.Bundle;
import java.io.*;
import java.util.zip.*;

/** Real Android parser, filesystem and packaged support assets; no global input. */
public class PortFeaturesTest extends Instrumentation {
    @Override public void onCreate(Bundle args){super.onCreate(args);start();}
    private void reject(String value) throws Exception {
        boolean rejected=false;try{SaveFiles.validate(new ByteArrayInputStream(value.getBytes("UTF-8")));}catch(Exception expected){rejected=true;}
        if(!rejected)throw new AssertionError("Accepted invalid save");
    }
    @Override public void onStart() {
        Bundle result=new Bundle();
        try {
            File root=getTargetContext().getExternalFilesDir(null);
            byte[] valid;try(InputStream in=new FileInputStream(new File(root,"SAVES.XML"))){valid=SaveFiles.validate(in);}
            byte[] again=SaveFiles.validate(new ByteArrayInputStream(valid));
            if(!java.util.Arrays.equals(valid,again))throw new AssertionError("Non-idempotent save validation");
            reject("<GameSaves/>");reject("<!DOCTYPE x [<!ENTITY y SYSTEM 'file:///x'>]><GameSaves>&y;</GameSaves>");
            reject(new String(valid,"UTF-8").replace("<Health>","<Health>-"));
            reject(new String(valid,"UTF-8").replace("<LevelNumber>1</LevelNumber>","<LevelNumber>99</LevelNumber>"));
            File stage=new File(root,"features-test");if(!stage.isDirectory()&&!stage.mkdirs())throw new IOException("stage");
            ImportSupport.prepare(getTargetContext(),stage);
            boolean level14=false;
            java.util.Set<String> generatedPngs=new java.util.HashSet<>(java.util.Arrays.asList(
                "CONTROLS/touchscreen_title.png","CONTROLS/touchscreen_img.png",
                "CREDITS/credits_ja.png","CREDITS/credits_pavel.png"));
            try(ZipFile zip=new ZipFile(new File(stage,"ASSETS.ZIP"))) {
                java.util.Enumeration<? extends ZipEntry> entries=zip.entries();
                while(entries.hasMoreElements()) {
                    String name=entries.nextElement().getName();
                    if(name.equals("LEVEL_METADATA/LEVEL14.XML"))level14=true;
                    if(!name.endsWith(".XML")&&!generatedPngs.remove(name))throw new AssertionError("Unexpected support content: "+name);
                }
            }
            if(!level14)throw new AssertionError("Missing level 14");
            if(!generatedPngs.isEmpty())throw new AssertionError("Missing generated help/credits: "+generatedPngs);
            ImportSupport.validateRez(new File(root,"CLAW.REZ"));
            File bad=new File(stage,"bad.rez");try(FileOutputStream out=new FileOutputStream(bad)){out.write(new byte[168]);}
            boolean rejected=false;try{ImportSupport.validateRez(bad);}catch(IOException expected){rejected=true;}
            if(!rejected)throw new AssertionError("Accepted invalid REZ");
            SaveFiles.writeAtomic(stage,"SAVES.XML",valid);
            // Exercise the exact startup application path in an isolated folder.
            byte[] imported=new String(valid,"UTF-8").replaceFirst("<Score>\\d+</Score>","<Score>321</Score>").getBytes("UTF-8");
            SaveFiles.writeAtomic(stage,"SAVES.pending.xml",imported);SaveFiles.applyPending(stage);
            try(InputStream in=new FileInputStream(new File(stage,"SAVES.XML"))) {
                if(!java.util.Arrays.equals(SaveFiles.validate(in),imported))throw new AssertionError("Pending save not applied");
            }
            try(InputStream in=new FileInputStream(new File(stage,"SAVES.before-import.xml"))) {
                if(!java.util.Arrays.equals(SaveFiles.validate(in),valid))throw new AssertionError("Original save not backed up");
            }
            if(new File(stage,"SAVES.pending.xml").exists())throw new AssertionError("Import would repeat on next start");
            SaveFiles.writeAtomic(stage,"SAVES.pending.xml","<GameSaves/>".getBytes("UTF-8"));
            boolean invalidRejected=false;try{SaveFiles.applyPending(stage);}catch(Exception expected){invalidRejected=true;}
            if(!invalidRejected)throw new AssertionError("Invalid pending save applied");
            try(InputStream in=new FileInputStream(new File(stage,"SAVES.XML"))) {
                if(!java.util.Arrays.equals(SaveFiles.validate(in),imported))throw new AssertionError("Invalid import damaged progress");
            }
            for(File file:stage.listFiles())if(!file.delete())throw new IOException("cleanup");
            if(!stage.delete())throw new IOException("cleanup stage");
            result.putString("features","PASS: save roundtrip, pending import/backup, invalid import preserves progress, invalid REZ rejected, XML plus exact generated help/credits and system font");
            finish(0,result);
        }catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));finish(1,result);}
    }
}
