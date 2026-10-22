package pl.pazur.port;

import android.content.Context;
import java.io.*;
import java.util.zip.*;
import org.xmlpull.v1.XmlPullParser;
import android.util.Xml;

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
    /** Validate imported config before publishing the five-file installation.
     * A valid outer ZIP CRC does not imply that config.xml is valid XML. This
     * checks framing/root and rejects DTDs; it is not a full engine schema or
     * proof that arbitrary numeric settings are meaningful. Existing user
     * configurations are never silently rewritten by this check. */
    static void validateConfig(Context context,File file) throws IOException {
        try {
            if(file.length()>1024L*1024)throw new IOException("config.xml exceeds 1 MiB");
            XmlPullParser parser=Xml.newPullParser();
            parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES,false);
            boolean root=false;java.util.ArrayDeque<String> elements=new java.util.ArrayDeque<>();
            try(InputStream input=new FileInputStream(file)) {
                parser.setInput(input,"UTF-8");
                while(parser.nextToken()!=XmlPullParser.END_DOCUMENT) {
                    if(parser.getEventType()==XmlPullParser.DOCDECL)throw new IOException("DOCTYPE is not supported");
                    // nextToken exposes unresolved entities without necessarily
                    // throwing; a missing replacement text is invalid XML.
                    if(parser.getEventType()==XmlPullParser.ENTITY_REF && parser.getText()==null)throw new IOException("Unresolved XML entity");
                    if(parser.getEventType()==XmlPullParser.START_TAG)elements.push(parser.getName());
                    if(parser.getEventType()==XmlPullParser.END_TAG &&
                            (elements.isEmpty()||!elements.pop().equals(parser.getName())))throw new IOException("Mismatched closing tag");
                    if(parser.getEventType()==XmlPullParser.START_TAG && parser.getDepth()==1) {
                        if(root||!"Configuration".equals(parser.getName()))throw new IOException("Expected Configuration root");
                        root=true;
                    }
                }
            }
            // Android's pull parser can report END_DOCUMENT for an unclosed
            // root; explicitly reject it instead of trusting EOF as validation.
            if(!root||!elements.isEmpty())throw new IOException("Incomplete Configuration document");
        } catch(Exception error) {
            throw new IOException(context.getString(R.string.import_config_error)+" config.xml: "+error.getMessage(),error);
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
