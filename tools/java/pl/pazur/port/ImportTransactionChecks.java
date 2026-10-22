package pl.pazur.port;

import java.io.*;
import java.nio.file.*;
import java.util.*;

/** Same production class, deterministic process-interruption boundaries on JVM.
 * Error intentionally bypasses ordinary IOException cleanup, like process death.
 */
public class ImportTransactionChecks {
    static class Interrupted extends Error {}
    static File base;
    static int cases;
    static void write(File file,String value) throws IOException {Files.write(file.toPath(),value.getBytes("UTF-8"));}
    static void equal(File file,String value) throws IOException {
        if(!new String(Files.readAllBytes(file.toPath()),"UTF-8").equals(value))throw new AssertionError(file);
    }
    static File fixture(String mode) throws IOException {
        File root=Files.createTempDirectory(base.toPath(),"case-").toFile();
        File stage=ImportTransaction.freshStage(root);
        for(int i=0;i<ImportTransaction.REQUIRED.length;i++) {
            String name=ImportTransaction.REQUIRED[i];
            if(mode.equals("full")||(mode.equals("partial")&&i%2==0))write(new File(root,name),"old "+name);
            write(new File(stage,name),"new "+name);
        }
        write(new File(root,"SAVES.XML"),"keep saves");return root;
    }
    static void check(File root,String mode,boolean committed) throws IOException {
        ImportTransaction.prepareStartup(root);ImportTransaction.prepareStartup(root);
        if(new File(root,"import-staging").exists())throw new AssertionError("Staging bytes retained");
        for(int i=0;i<ImportTransaction.REQUIRED.length;i++) {
            String name=ImportTransaction.REQUIRED[i];File file=new File(root,name);
            if(committed)equal(file,"new "+name);
            else if(mode.equals("full")||(mode.equals("partial")&&i%2==0))equal(file,"old "+name);
            else if(file.exists())throw new AssertionError("Unexpected new file: "+file);
        }
        equal(new File(root,"SAVES.XML"),"keep saves");cases++;
    }
    public static void main(String[] args) throws Exception {
        base=Files.createTempDirectory("pazur-import-jvm-").toFile();
        try {
            List<String> boundaries=new ArrayList<>();
            for(String name:ImportTransaction.REQUIRED)boundaries.add("backup:"+name);
            boundaries.add("journal");for(String name:ImportTransaction.REQUIRED)boundaries.add("published:"+name);
            boundaries.add("committed");
            for(String mode:Arrays.asList("empty","partial","full")) {
                for(String boundary:boundaries) {
                    File root=fixture(mode);
                    try {ImportTransaction.commit(root,new File(root,"import-staging"),step->{if(step.equals(boundary))throw new Interrupted();});throw new AssertionError("No interruption");}
                    catch(Interrupted expected){}
                    check(root,mode,boundary.equals("committed"));
                }
                for(String name:ImportTransaction.REQUIRED) {
                    File root=fixture(mode);
                    try {ImportTransaction.commit(root,new File(root,"import-staging"),step->{if(step.equals("published:config.xml"))throw new Interrupted();});}
                    catch(Interrupted expected){}
                    try {ImportTransaction.recover(root,step->{if(step.equals("restored:"+name))throw new Interrupted();});throw new AssertionError("No recovery interruption");}
                    catch(Interrupted expected){}
                    check(root,mode,false);
                }
                File root=fixture(mode);ImportTransaction.commit(root,new File(root,"import-staging"));check(root,mode,true);
                for(String failure:Arrays.asList("backup:ASSETS.ZIP","published:ASSETS.ZIP")) {
                    File failed=fixture(mode);
                    try {ImportTransaction.commit(failed,new File(failed,"import-staging"),step->{if(step.equals(failure))throw new IOException("Injected I/O failure");});throw new AssertionError("No I/O failure");}
                    catch(IOException expected){}
                    check(failed,mode,false);
                }
            }
            // No valid journal means no rollback is guessed. Keep backups and
            // block startup instead of silently accepting mixed live data.
            File root=fixture("full");
            try {ImportTransaction.commit(root,new File(root,"import-staging"),step->{if(step.equals("journal"))throw new Interrupted();});}catch(Interrupted expected){}
            File marker=new File(root,"import-transaction/rollback");write(marker,"truncated");
            try {ImportTransaction.recover(root);throw new AssertionError("Bad journal accepted");}catch(IOException expected){}
            if(!new File(root,"import-transaction/CLAW.REZ").isFile())throw new AssertionError("Backup removed");cases++;
            // Unknown journal must prevent staging cleanup: preserve evidence.
            try {ImportTransaction.prepareStartup(root);throw new AssertionError("Bad journal accepted at startup");}catch(IOException expected){}
            equal(new File(root,"import-staging/CLAW.REZ"),"new CLAW.REZ");cases++;
            // Rejected extraction before publication: startup frees only staging.
            root=fixture("full");check(root,"full",false);
            root=fixture("full");write(new File(root,"import-staging/unknown.bin"),"preserve unknown");
            try {ImportTransaction.prepareStartup(root);throw new AssertionError("Unknown staging content accepted");}catch(IOException expected){}
            equal(new File(root,"import-staging/unknown.bin"),"preserve unknown");
            equal(new File(root,"CLAW.REZ"),"old CLAW.REZ");equal(new File(root,"SAVES.XML"),"keep saves");cases++;
            System.out.println("PASS: "+cases+" interruption/commit/journal cases; save sentinels preserved");
        } finally {
            try(java.util.stream.Stream<Path> paths=Files.walk(base.toPath())) {
                for(Path path:(Iterable<Path>)paths.sorted(Comparator.reverseOrder())::iterator)Files.delete(path);
            }
        }
    }
}
