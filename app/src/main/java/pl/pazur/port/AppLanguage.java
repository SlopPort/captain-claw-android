package pl.pazur.port;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.res.Configuration;
import android.util.AtomicFile;
import java.io.*;
import java.util.Locale;

/** Explicit app locale on API 21+, independent of game data and bindings.
 * OpenAI Codex (LLM). Native labels read an atomic copy on the next game start.
 */
final class AppLanguage {
    static String code(Context context) {
        String saved=context.getSharedPreferences("interface",Context.MODE_PRIVATE).getString("language","");
        if(saved.equals("pl") || saved.equals("en"))return saved;
        return Locale.getDefault().getLanguage().equals("pl")?"pl":"en";
    }
    static Context wrap(Context context) {
        Configuration config=new Configuration(context.getResources().getConfiguration());
        config.setLocale(new Locale(code(context)));
        return context.createConfigurationContext(config);
    }
    static AlertDialog choose(Activity activity) {
        return new AlertDialog.Builder(activity).setTitle(R.string.language)
            .setSingleChoiceItems(new String[]{"Polski","English"},code(activity).equals("pl")?0:1,(dialog,index)-> {
                activity.getSharedPreferences("interface",Context.MODE_PRIVATE).edit()
                    .putString("language",index==0?"pl":"en").apply();
                dialog.dismiss();activity.recreate();
            }).setNegativeButton(android.R.string.cancel,null).show();
    }
    static void writeNative(Context context) throws IOException {
        File root=context.getExternalFilesDir(null);
        writeNative(context,root);
    }
    static void writeNative(Context context,File root) throws IOException {
        if(root==null)throw new IOException(context.getString(R.string.storage_unavailable));
        AtomicFile file=new AtomicFile(new File(root,"ui-language.txt"));
        FileOutputStream output=null;
        try {
            output=file.startWrite();output.write(code(context).getBytes("US-ASCII"));
            file.finishWrite(output);output=null;
        } catch(IOException error) {
            if(output!=null)file.failWrite(output);throw error;
        }
    }
    private AppLanguage() { }
}
