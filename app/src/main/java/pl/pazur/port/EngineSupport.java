package pl.pazur.port;

import android.content.Context;
import android.util.AtomicFile;
import java.io.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;

/** Keep engine XML paired with its APK without replacing imported game data,
 * configuration or saves. AtomicFile is available before our minimum API 21.
 * Written by OpenAI Codex. No original game artwork is stored in this bundle.
 */
final class EngineSupport {
    private static byte[] digest(InputStream stream) throws IOException {
        try (InputStream in=stream) {
            MessageDigest hash=MessageDigest.getInstance("SHA-256");
            byte[] buffer=new byte[8192];int n;
            while((n=in.read(buffer))!=-1)hash.update(buffer,0,n);
            return hash.digest();
        } catch(NoSuchAlgorithmException error) {throw new IOException(error);}
    }
    static synchronized void install(Context context,File root) throws IOException {
        if(root==null)throw new IOException("Brak pamięci aplikacji / App storage unavailable");
        File folder=new File(root,".engine-support");
        if(!folder.isDirectory() && !folder.mkdirs())throw new IOException("Cannot prepare engine support");
        AtomicFile destination=new AtomicFile(new File(folder,"ASSETS.ZIP"));
        byte[] expected=digest(context.getAssets().open("import-support/ASSETS.ZIP"));
        byte[] actual=null;
        try {actual=digest(destination.openRead());} catch(FileNotFoundException ignored) { }
        if(Arrays.equals(expected,actual))return;
        FileOutputStream output=null;
        try(InputStream in=context.getAssets().open("import-support/ASSETS.ZIP")) {
            output=destination.startWrite();
            byte[] buffer=new byte[8192];int n;long total=0;
            while((n=in.read(buffer))!=-1) {
                total+=n;if(total>32L*1024*1024)throw new IOException("Engine support exceeds limit");
                output.write(buffer,0,n);
            }
            destination.finishWrite(output);output=null;
        } catch(IOException error) {
            if(output!=null)destination.failWrite(output);
            throw error;
        }
    }
}
