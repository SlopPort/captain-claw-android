package pl.pazur.port;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import java.io.*;

/** Test APK only. Read-only, single fixture, unguessable per-run capability.
 * Never points at the real game directory; host removes the copy afterwards.
 * OpenAI Codex (LLM). No provider is packaged in the distributed game APK. */
public class ImportStreamProvider extends ContentProvider {
    public boolean onCreate(){return true;}
    public String getType(Uri uri){return "application/octet-stream";}
    public Cursor query(Uri uri,String[] p,String s,String[] a,String sort){return null;}
    public Uri insert(Uri uri,ContentValues values){throw new UnsupportedOperationException();}
    public int delete(Uri uri,String s,String[] a){throw new UnsupportedOperationException();}
    public int update(Uri uri,ContentValues v,String s,String[] a){throw new UnsupportedOperationException();}
    public ParcelFileDescriptor openFile(Uri uri,String mode) throws FileNotFoundException {
        File root=getContext().getExternalFilesDir(null);
        try(BufferedReader in=new BufferedReader(new FileReader(new File(root,"import-stream-token")))) {
            String token=in.readLine();
            if(!"r".equals(mode)||token==null||token.length()!=32||
                !uri.getPath().equals("/"+token+"/fixture"))throw new FileNotFoundException("Not an active fixture");
            return ParcelFileDescriptor.open(new File(root,"import-stream-fixture"),ParcelFileDescriptor.MODE_READ_ONLY);
        } catch(IOException error){throw new FileNotFoundException("Fixture unavailable");}
    }
}
