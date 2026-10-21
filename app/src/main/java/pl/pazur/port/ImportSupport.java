package pl.pazur.port;

import android.content.Context;
import java.io.*;
import java.util.zip.*;

/** Direct-REZ workflow inspired by arthurboss/claw-web, GPLv3.
 * New Android implementation; support assets contain XML and generated artwork only.
 */
final class ImportSupport {
    static void copy(InputStream in, File file, long limit) throws IOException {
        try (OutputStream out=new FileOutputStream(file)) {
            byte[] bytes=new byte[65536];long total=0;int n;
            while((n=in.read(bytes))!=-1) {total+=n;if(total>limit)throw new IOException("File too large");out.write(bytes,0,n);}
        }
    }
    static void validateRez(File file) throws IOException {
        try(RandomAccessFile input=new RandomAccessFile(file,"r")) {
            if(input.length()<=168)throw new IOException("Niepełny REZ: przygotuj game-data.zip z folderu Assets. / Incomplete REZ: prepare game-data.zip from the Assets folder.");
            input.seek(127);long version=((long)Integer.reverseBytes(input.readInt()))&0xffffffffL;
            long offset=((long)Integer.reverseBytes(input.readInt()))&0xffffffffL;
            long size=((long)Integer.reverseBytes(input.readInt()))&0xffffffffL;
            if(version!=1 || offset<168 || size<16 || offset+size>input.length())
                throw new IOException("Invalid REZ directory");
        }
    }
    static void prepare(Context context,File stage) throws IOException {
        for(String name:new String[]{"ASSETS.ZIP","config.xml","console02.tga"}) {
            try(InputStream in=context.getAssets().open("import-support/"+name)) {copy(in,new File(stage,name),32L*1024*1024);}
        }
        // Copy the phone's own installed font locally; never redistribute an
        // unlicensed upstream font in APK/source archives.
        File font=null;
        for(String path:new String[]{"/system/fonts/Roboto-Regular.ttf","/system/fonts/DroidSans.ttf","/system/fonts/NotoSans-Regular.ttf"})
            if(new File(path).isFile()) {font=new File(path);break;}
        if(font==null)throw new IOException("System font unavailable; use game-data.zip");
        try(InputStream in=new FileInputStream(font)) {copy(in,new File(stage,"clacon.ttf"),32L*1024*1024);}
    }
    static boolean isZip(InputStream input) throws IOException {
        input.mark(4);int a=input.read(),b=input.read();input.reset();return a=='P' && b=='K';
    }
}
