package pl.pazur.port;

import java.io.*;
import java.util.Arrays;

/** OpenAI Codex (LLM): run only in the dedicated 8 MiB emulator tmpfs.
 * Uses real ENOSPC, not a phone-wide filler or a mocked write exception.
 * The runner must verify the mount before invoking this root-shell fixture. */
public final class ImportFullDiskChecks {
    private static final String ROOT="/data/local/tmp/pazur-import-space";
    private static final int LARGE=1024*1024;
    private static void write(File file,int size,int value) throws IOException {
        byte[] bytes=new byte[4096];Arrays.fill(bytes,(byte)value);
        try(FileOutputStream out=new FileOutputStream(file)) {
            for(int left=size;left>0;left-=Math.min(left,bytes.length))out.write(bytes,0,Math.min(left,bytes.length));
            out.getFD().sync();
        }
    }
    private static void verify(File file,int size,int value) throws IOException {
        if(file.length()!=size)throw new AssertionError("length: "+file.getName());
        try(InputStream in=new BufferedInputStream(new FileInputStream(file))) {
            int count=0,b;while((b=in.read())!=-1){if(b!=value)throw new AssertionError("content: "+file.getName());count++;}
            if(count!=size)throw new AssertionError("read length");
        }
    }
    private static void fill(File file) throws IOException {
        try(FileOutputStream out=new FileOutputStream(file)) {
            byte[] bytes=new byte[4096];
            // A hard bound prevents filling a general-purpose filesystem if
            // the required tmpfs mount was accidentally omitted by a caller.
            for(int i=0;i<4096;i++)out.write(bytes);
        } catch(IOException error) {
            if(!error.toString().contains("ENOSPC")&&!error.toString().contains("No space left"))throw error;
            System.out.println("Observed actual ENOSPC while filling dedicated tmpfs");return;
        }
        throw new AssertionError("Expected bounded 8 MiB mount, no ENOSPC by 16 MiB");
    }
    private static void originals(File root) throws IOException {
        for(String name:ImportTransaction.REQUIRED)verify(new File(root,name),name.equals("CLAW.REZ")?LARGE:4096,17);
        verify(new File(root,"SAVES.XML"),4096,71);
    }
    public static void main(String[] args) throws Exception {
        if(args.length!=1||!Arrays.asList("backup","rollback").contains(args[0]))throw new IllegalArgumentException("backup|rollback");
        boolean boundedMount=false;
        try(BufferedReader in=new BufferedReader(new FileReader("/proc/mounts"))) {
            String line;
            while((line=in.readLine())!=null)
                if(line.startsWith("tmpfs "+ROOT+" tmpfs ")&&line.contains("size=8192k"))boundedMount=true;
        }
        if(!boundedMount)throw new IOException("Refusing test outside exact dedicated 8 MiB tmpfs");
        File root=new File(ROOT),filler=new File(root,"bounded-filler");
        if(!root.isDirectory()||root.list().length!=0)throw new IOException("Fixture mount must start empty");
        File stage=ImportTransaction.freshStage(root);
        for(String name:ImportTransaction.REQUIRED) {
            int size=name.equals("CLAW.REZ")?LARGE:4096;
            write(new File(root,name),size,17);write(new File(stage,name),size,39);
        }
        write(new File(root,"SAVES.XML"),4096,71);
        boolean failed=false;
        if(args[0].equals("backup")) {
            fill(filler);
            try {ImportTransaction.commit(root,stage);}catch(IOException expected){failed=true;System.out.println("Commit refused full filesystem: "+expected);}
            if(!failed)throw new AssertionError("Commit unexpectedly passed");
            originals(root);
        } else {
            try {
                ImportTransaction.commit(root,stage,step->{if(step.equals("published:CLAW.REZ")){fill(filler);throw new IOException("Deliberate interruption after publication");}});
            }catch(IOException expected){failed=true;}
            if(!failed)throw new AssertionError("Interruption not reached");
            failed=false;
            try {ImportTransaction.recover(root);}catch(IOException expected){failed=true;System.out.println("Recovery blocked while full: "+expected);}
            if(!failed)throw new AssertionError("Expected no room for restore copy");
            verify(new File(root,"import-transaction/CLAW.REZ"),LARGE,17);
            verify(new File(root,"SAVES.XML"),4096,71);
        }
        if(!filler.delete())throw new IOException("Cannot release fixture filler");
        ImportTransaction.prepareStartup(root);ImportTransaction.prepareStartup(root);originals(root);
        if(new File(root,"import-staging").exists()||new File(root,"import-transaction").exists())throw new AssertionError("Cleanup incomplete");
        for(File file:root.listFiles())if(!file.delete())throw new IOException("Fixture cleanup");
        System.out.println("PASS: "+args[0]+", originals and save preserved after actual ENOSPC and retry");
    }
}
