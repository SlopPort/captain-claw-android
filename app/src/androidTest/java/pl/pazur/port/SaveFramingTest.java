package pl.pazur.port;

import android.app.Instrumentation;
import android.os.Bundle;
import java.io.*;
import java.util.*;

/** Codex (LLM): actual Android parser, memory-only malformed save framing.
 * Never publishes pending progress or edits the user's current save. */
public class SaveFramingTest extends Instrumentation {
    private boolean expectOldAcceptance;
    @Override public void onCreate(Bundle args){super.onCreate(args);expectOldAcceptance=args!=null&&"true".equals(args.getString("expect_old_acceptance"));start();}
    @Override public void onStart() {
        Bundle result=new Bundle();
        try {
            String valid;try(InputStream input=new FileInputStream(new File(getTargetContext().getExternalFilesDir(null),"SAVES.XML"))){valid=new String(SaveFiles.validate(input),"UTF-8");}
            Map<String,String> cases=new LinkedHashMap<>();
            cases.put("missing_root_close",valid.replace("</GameSaves>",""));
            cases.put("second_root",valid+"<GameSaves/>");
            cases.put("duplicate_level_name",valid.replaceFirst("</LevelName>","</LevelName><LevelName>duplicate</LevelName>"));
            cases.put("prefix_text","junk"+valid);
            cases.put("suffix_text",valid+"junk");
            java.util.regex.Matcher first=java.util.regex.Pattern.compile("<Level><LevelNumber>1</LevelNumber>.*?</Level>",java.util.regex.Pattern.DOTALL).matcher(valid);
            if(!first.find())throw new Exception("No canonical level-one fixture");
            String levelOne=first.group();
            String duplicateNumbers=levelOne.replace("<LevelNumber>1</LevelNumber>","<LevelNumber>2</LevelNumber><LevelNumber>3</LevelNumber>");
            cases.put("duplicate_level_number","<GameSaves>"+levelOne+duplicateNumbers+"</GameSaves>");
            boolean anyAccepted=false;
            for(Map.Entry<String,String> entry:cases.entrySet()) {
                boolean accepted=true;
                try{SaveFiles.validate(new ByteArrayInputStream(entry.getValue().getBytes("UTF-8")));}catch(Exception expected){accepted=false;}
                result.putString(entry.getKey(),accepted?"ACCEPTED":"REJECTED");anyAccepted|=accepted;
            }
            if(expectOldAcceptance?!anyAccepted:anyAccepted)throw new Exception("Unexpected save framing acceptance; inspect individual results");
            result.putString("save_framing",expectOldAcceptance?"PASS: old malformed acceptance reproduced":"PASS: all malformed framing rejected");
        } catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));}
        finish(result.containsKey("error")?1:0,result);
    }
}
