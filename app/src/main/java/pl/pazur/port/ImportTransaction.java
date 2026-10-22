package pl.pazur.port;

import java.io.*;
import java.util.*;

/** Process-interruption recovery for the five-file game-data installation.
 * Written by OpenAI Codex. Saves, bindings and engine-support updates are outside
 * this allowlist. This is a rollback journal, not an atomic directory swap:
 * callers must recover before checking readiness or starting the native engine.
 * Synced files protect process-death recovery; sudden power-loss durability also
 * depends on the device filesystem and is not promised by these Java renames.
 */
final class ImportTransaction {
    static final Object LOCK=new Object();
    static final String[] REQUIRED={"CLAW.REZ","ASSETS.ZIP","config.xml","clacon.ttf","console02.tga"};
    private static final String DIRECTORY="import-transaction", MARKER="rollback";
    interface Checkpoint { void reached(String step) throws IOException; }
    private static final Checkpoint NONE=step->{};

    private static void copy(File source,File destination) throws IOException {
        try(InputStream in=new FileInputStream(source);FileOutputStream out=new FileOutputStream(destination)) {
            byte[] bytes=new byte[65536];int count;
            while((count=in.read(bytes))!=-1)out.write(bytes,0,count);
            out.getFD().sync();
        }
    }
    private static void remove(File file) throws IOException {
        if(file.exists()&&!file.delete())throw new IOException("Cannot remove import file: "+file.getName());
    }
    private static void move(File from,File to) throws IOException {
        if(from.renameTo(to))return;
        // Some filesystems refuse replacement by rename. The rollback journal
        // already protects live destinations here; never remove a directory.
        if(!from.isFile()||!to.isFile()||!to.delete()||!from.renameTo(to))
            throw new IOException("Cannot install game data: "+to.getName());
    }
    private static void clear(File directory) throws IOException {
        // Only our fixed journal files are removed. Unknown content fails closed.
        for(String name:REQUIRED) {
            remove(new File(directory,name));remove(new File(directory,name+".restore"));
        }
        remove(new File(directory,MARKER));remove(new File(directory,MARKER+".tmp"));remove(directory);
    }
    static void recover(File root) throws IOException { recover(root,NONE); }
    static void recover(File root,Checkpoint checkpoint) throws IOException {
        synchronized(LOCK) {
            File directory=new File(root,DIRECTORY),marker=new File(directory,MARKER);
            if(!directory.exists())return;
            if(marker.exists()) {
                Set<String> originals=new HashSet<>();
                try(DataInputStream in=new DataInputStream(new FileInputStream(marker))) {
                    if(!in.readUTF().equals("PAZUR-IMPORT-1"))throw new IOException("Invalid import journal");
                    for(String name:REQUIRED)if(in.readBoolean())originals.add(name);
                    if(in.read()!=-1)throw new IOException("Invalid import journal length");
                }
                // Retain every backup until ALL originals are restored. A second
                // interruption during recovery can safely repeat these steps.
                for(String name:REQUIRED) {
                    File target=new File(root,name);
                    if(originals.contains(name)) {
                        File temporary=new File(directory,name+".restore");
                        copy(new File(directory,name),temporary);move(temporary,target);
                    } else remove(target);
                    checkpoint.reached("restored:"+name);
                }
                remove(marker);checkpoint.reached("recovered");
            }
            clear(directory);
        }
    }
    static void commit(File root,File stage) throws IOException { commit(root,stage,NONE); }
    static void commit(File root,File stage,Checkpoint checkpoint) throws IOException {
        synchronized(LOCK) {
            recover(root);
            for(String name:REQUIRED)if(!new File(stage,name).isFile())throw new IOException("Incomplete import: "+name);
            File directory=new File(root,DIRECTORY);
            if(!directory.mkdir())throw new IOException("Cannot prepare import rollback");
            boolean[] originals=new boolean[REQUIRED.length];
            for(int i=0;i<REQUIRED.length;i++) {
                File old=new File(root,REQUIRED[i]);originals[i]=old.exists();
                if(originals[i])copy(old,new File(directory,REQUIRED[i]));
                checkpoint.reached("backup:"+REQUIRED[i]);
            }
            File temporary=new File(directory,MARKER+".tmp");
            try(FileOutputStream file=new FileOutputStream(temporary);DataOutputStream out=new DataOutputStream(file)) {
                out.writeUTF("PAZUR-IMPORT-1");for(boolean exists:originals)out.writeBoolean(exists);
                out.flush();file.getFD().sync();
            }
            move(temporary,new File(directory,MARKER));checkpoint.reached("journal");
            for(String name:REQUIRED) {
                // Sync prepared content before it becomes part of the live set.
                try(RandomAccessFile file=new RandomAccessFile(new File(stage,name),"rw")){file.getFD().sync();}
                move(new File(stage,name),new File(root,name));checkpoint.reached("published:"+name);
            }
            // This is the commit point. After it, recovery keeps the complete new
            // set and only removes stale backups; before it, it restores the old set.
            remove(new File(directory,MARKER));checkpoint.reached("committed");
            clear(directory);
        }
    }
    static File freshStage(File root) throws IOException {
        recover(root);
        File stage=new File(root,"import-staging");
        if(stage.exists())clear(stage);
        if(!stage.mkdir())throw new IOException("Cannot prepare import staging");
        return stage;
    }
}
