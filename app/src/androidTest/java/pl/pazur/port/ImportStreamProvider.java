package pl.pazur.port;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import android.os.Bundle;
import java.io.*;

/** Test APK only. One read fixture and one gated export, random per-run capability.
 * Never points at the real game directory; host removes the copy afterwards.
 * OpenAI Codex (LLM). No provider is packaged in the distributed game APK. */
public class ImportStreamProvider extends ContentProvider {
    private static volatile java.util.concurrent.CountDownLatch exportGate=new java.util.concurrent.CountDownLatch(1);
    private String currentToken() throws IOException {
        try(BufferedReader in=new BufferedReader(new FileReader(new File(getContext().getExternalFilesDir(null),"import-stream-token")))) {
            String token=in.readLine();if(token==null||token.length()!=32)throw new IOException("No active capability");return token;
        }
    }
    @Override public Bundle call(String method,String arg,Bundle extras) {
        try{if(!currentToken().equals(arg))throw new SecurityException("Inactive capability");}
        catch(IOException error){throw new SecurityException("No active fixture",error);}
        if("reset_export".equals(method))exportGate=new java.util.concurrent.CountDownLatch(1);
        else if("release_export".equals(method))exportGate.countDown();
        else throw new IllegalArgumentException("Unknown test method");
        Bundle result=new Bundle();result.putBoolean("ok",true);return result;
    }
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
            if(token!=null&&token.length()==32&&uri.getPath().equals("/"+token+"/export")) {
                File output=new File(root,"save-stream-output.xml");
                if("r".equals(mode))return ParcelFileDescriptor.open(output,ParcelFileDescriptor.MODE_READ_ONLY);
                if(!"wt".equals(mode))throw new FileNotFoundException("Read or truncate-write only");
                try{if(!exportGate.await(10,java.util.concurrent.TimeUnit.SECONDS))throw new FileNotFoundException("Export gate timed out");}
                catch(InterruptedException error){Thread.currentThread().interrupt();throw new FileNotFoundException("Export interrupted");}
                return ParcelFileDescriptor.open(output,ParcelFileDescriptor.MODE_WRITE_ONLY|ParcelFileDescriptor.MODE_CREATE|ParcelFileDescriptor.MODE_TRUNCATE);
            }
            if(!"r".equals(mode)||token==null||token.length()!=32||
                !uri.getPath().equals("/"+token+"/fixture"))throw new FileNotFoundException("Not an active fixture");
            return ParcelFileDescriptor.open(new File(root,"import-stream-fixture"),ParcelFileDescriptor.MODE_READ_ONLY);
        } catch(IOException error){throw new FileNotFoundException("Fixture unavailable");}
    }
}
