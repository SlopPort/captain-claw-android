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
            ImportSupport.validateConfig(getTargetContext(),new File(stage,"config.xml"));
            File invalidConfig=new File(stage,"invalid-config.xml");
            for(String invalid:new String[]{"", "<Configuration>", "<Wrong/>",
                    "<!DOCTYPE Configuration [<!ENTITY a 'text'>]><Configuration/>",
                    "<Configuration/><Configuration/>", "<Configuration></Wrong>", "<Configuration><A></Configuration>", "junk<Configuration/>", "<Configuration/>junk", "<Configuration>&unknown;</Configuration>"}) {
                try(FileOutputStream out=new FileOutputStream(invalidConfig)){out.write(invalid.getBytes("UTF-8"));}
                boolean configRejected=false;
                try{ImportSupport.validateConfig(getTargetContext(),invalidConfig);}catch(IOException expected){configRejected=true;}
                if(!configRejected)throw new AssertionError("Accepted malformed config: "+invalid);
            }
            try(RandomAccessFile out=new RandomAccessFile(invalidConfig,"rw")){out.setLength(1024*1024+1);}
            boolean largeRejected=false;
            try{ImportSupport.validateConfig(getTargetContext(),invalidConfig);}catch(IOException expected){largeRejected=true;}
            if(!largeRejected)throw new AssertionError("Accepted oversized config");
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
            // Simulate death after the atomic publication and before pending
            // removal: replay must not replace the old backup with new progress.
            SaveFiles.writeAtomic(stage,"SAVES.pending.xml",imported);SaveFiles.applyPending(stage);
            try(InputStream in=new FileInputStream(new File(stage,"SAVES.before-import.xml"))) {
                if(!java.util.Arrays.equals(SaveFiles.validate(in),valid))throw new AssertionError("Replay destroyed pre-import backup");
            }
            SaveFiles.writeAtomic(stage,"SAVES.pending.xml","<GameSaves/>".getBytes("UTF-8"));
            boolean invalidRejected=false;try{SaveFiles.applyPending(stage);}catch(Exception expected){invalidRejected=true;}
            if(!invalidRejected)throw new AssertionError("Invalid pending save applied");
            try(InputStream in=new FileInputStream(new File(stage,"SAVES.XML"))) {
                if(!java.util.Arrays.equals(SaveFiles.validate(in),imported))throw new AssertionError("Invalid import damaged progress");
            }
            for(File file:stage.listFiles())if(!file.delete())throw new IOException("cleanup");
            if(!stage.delete())throw new IOException("cleanup stage");
            checkStartup(root);
            result.putString("features","PASS: save roundtrip, pending import/backup, invalid import preserves progress, invalid REZ and eleven malformed/oversized configs rejected, XML plus exact generated help/credits and system font");
            finish(0,result);
        }catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));finish(1,result);}
    }
    private void checkStartup(File root) throws Exception {
        File fixture=new File(root,"startup-fixture-test");
        if(!fixture.mkdir())throw new IOException("Existing startup fixture; preserve evidence");
        try {
            boolean rejected=false;try{GameFiles.prepare(getTargetContext(),fixture);}catch(IOException expected){rejected=true;}
            if(!rejected)throw new AssertionError("Missing data entered native startup");
            // Filename/size fixtures only: GameFiles must not attempt to parse
            // commercial REZ data; native validation remains a separate test.
            for(String name:ImportTransaction.REQUIRED)
                SaveFiles.writeAtomic(fixture,name,new byte[name.equals("CLAW.REZ")?169:1]);
            File abandoned=ImportTransaction.freshStage(fixture);
            SaveFiles.writeAtomic(abandoned,"CLAW.REZ",new byte[1024*1024]);
            GameFiles.prepare(getTargetContext(),fixture);
            if(abandoned.exists())throw new AssertionError("Startup retained abandoned import bytes");
            byte[] initial;try(InputStream in=new FileInputStream(new File(fixture,"SAVES.XML"))){initial=SaveFiles.validate(in);}
            SaveFiles.writeAtomic(fixture,"SAVES.XML",new byte[0]);
            GameFiles.prepare(getTargetContext(),fixture);
            if(new File(fixture,"SAVES.XML").length()!=0)throw new AssertionError("Existing damaged save was silently reset");
            SaveFiles.writeAtomic(fixture,"SAVES.XML",initial);
            SaveFiles.writeAtomic(fixture,"SAVES.XML.tmp",new byte[0]);
            if(!new File(fixture,"SAVES.XML").delete())throw new IOException("fixture delete");
            GameFiles.prepare(getTargetContext(),fixture);
            try(InputStream in=new FileInputStream(new File(fixture,"SAVES.XML"))){
                if(!java.util.Arrays.equals(initial,SaveFiles.validate(in)))throw new AssertionError("Interrupted initial save did not recover");
            }
            if(!new File(fixture,".engine-support/ASSETS.ZIP").isFile()||!new File(fixture,"ui-language.txt").isFile())
                throw new AssertionError("Restored activity preparation incomplete");
        } finally {removeFixture(fixture);}
    }
    private void removeFixture(File file) throws IOException {
        if(file.isDirectory())for(File child:file.listFiles())removeFixture(child);
        if(!file.delete())throw new IOException("Cannot remove own startup fixture");
    }
}
