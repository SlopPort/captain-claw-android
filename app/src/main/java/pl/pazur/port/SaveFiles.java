package pl.pazur.port;

import java.io.*;
import java.util.*;
import org.xmlpull.v1.XmlPullParser;
import android.util.Xml;

/** Save export/import UX inspired by Claw Web. Native SAVES.XML stays compatible.
 * Parse to a bounded, canonical document before replacing any user file. */
final class SaveFiles {
    static final String[] FIELDS={"CheckpointNumber","Score","Health","Lives","BulletCount","MagicCount","DynamiteCount"};
    private static byte[] readBounded(InputStream in) throws IOException {
        ByteArrayOutputStream bytes=new ByteArrayOutputStream();byte[] buffer=new byte[4096];int n;
        while((n=in.read(buffer))!=-1) {if(bytes.size()+n>262144)throw new IOException("Save exceeds 256 KiB");bytes.write(buffer,0,n);}
        return bytes.toByteArray();
    }
    static byte[] validate(InputStream in) throws Exception {
        byte[] bytes=readBounded(in);
        XmlPullParser parser=Xml.newPullParser();
        parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES,false);
        parser.setInput(new ByteArrayInputStream(bytes),"UTF-8");
        StringBuilder out=new StringBuilder("<GameSaves>");
        Set<Integer> levels=new HashSet<>(),checks=new HashSet<>();Set<String> fields=new HashSet<>();
        int level=0,checkpoint=-1;boolean first=false;String levelName="";
        while(parser.nextToken()!=XmlPullParser.END_DOCUMENT) {
            int type=parser.getEventType();String name=parser.getName();
            if(type==XmlPullParser.DOCDECL)throw new IOException("DOCTYPE is not supported");
            if(type==XmlPullParser.START_TAG) {
                int depth=parser.getDepth();
                if(depth==1 && name.equals("GameSaves"))continue;
                if(depth==2 && name.equals("Level")) {level=0;levelName="";checks.clear();out.append("<Level>");continue;}
                if(depth==3 && name.equals("LevelNumber")) {
                    level=Integer.parseInt(parser.nextText().trim());
                    if(level<1||level>14||!levels.add(level))throw new IOException("Invalid/duplicate level");
                    out.append("<LevelNumber>").append(level).append("</LevelNumber>");continue;
                }
                if(depth==3 && name.equals("LevelName")) {
                    levelName=parser.nextText();if(levelName.length()>128)throw new IOException("Level name too long");
                    out.append("<LevelName>").append(levelName.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")).append("</LevelName>");continue;
                }
                if(depth==3 && name.equals("Checkpoint")) {checkpoint=-1;fields.clear();out.append("<Checkpoint>");continue;}
                if(depth==4 && Arrays.asList(FIELDS).contains(name)) {
                    long value=Long.parseLong(parser.nextText().trim());
                    if(!fields.add(name)||value<0||value>1000000000L)throw new IOException("Invalid save value");
                    if(name.equals("CheckpointNumber")) {checkpoint=(int)value;if(value>2||!checks.add(checkpoint))throw new IOException("Invalid checkpoint");}
                    if(name.equals("Health") && value>100)throw new IOException("Invalid health");
                    out.append('<').append(name).append('>').append(value).append("</").append(name).append('>');continue;
                }
                throw new IOException("Unexpected save element: "+name);
            } else if(type==XmlPullParser.END_TAG) {
                if(name.equals("Checkpoint")) {if(fields.size()!=FIELDS.length||checkpoint<0)throw new IOException("Incomplete checkpoint");out.append("</Checkpoint>");}
                if(name.equals("Level")) {if(level==0||levelName.isEmpty()||!checks.contains(0))throw new IOException("Incomplete level");if(level==1)first=true;out.append("</Level>");}
            }
        }
        if(!first)throw new IOException("Level 1 is required");
        out.append("</GameSaves>");return out.toString().getBytes("UTF-8");
    }
    static void writeAtomic(File root,String name,byte[] bytes) throws IOException {
        File temporary=new File(root,name+".tmp");
        try(FileOutputStream out=new FileOutputStream(temporary)) {out.write(bytes);out.getFD().sync();}
        if(!temporary.renameTo(new File(root,name)))throw new IOException("Cannot save "+name);
    }
    static void applyPending(File root) throws Exception {
        File pending=new File(root,"SAVES.pending.xml");if(!pending.isFile())return;
        byte[] imported;try(InputStream in=new FileInputStream(pending)){imported=validate(in);}
        File saves=new File(root,"SAVES.XML");
        if(saves.isFile())try(InputStream in=new FileInputStream(saves)) {
            writeAtomic(root,"SAVES.before-import.xml",readBounded(in));
        }
        writeAtomic(root,"SAVES.XML",imported);
        if(!pending.delete())throw new IOException("Save applied, but pending file could not be removed");
    }
}
