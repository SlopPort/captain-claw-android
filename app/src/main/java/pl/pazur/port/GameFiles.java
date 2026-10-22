package pl.pazur.port;

import android.content.Context;
import java.io.*;

/** OpenAI Codex (LLM): gate every native entry, including Android restoring the
 * SDL Activity without first recreating LauncherActivity. Called on SDLThread,
 * before nativeRunMain, so recovery of a large REZ never blocks the UI thread. */
final class GameFiles {
    static void prepare(Context context) throws Exception {
        File root=context.getExternalFilesDir(null);
        prepare(context,root);
    }
    static void prepare(Context context,File root) throws Exception {
        if(root==null)throw new IOException(context.getString(R.string.storage_unavailable));
        synchronized(ImportTransaction.LOCK) {
            ImportTransaction.prepareStartup(root);
            for(String name:ImportTransaction.REQUIRED)
                if(!new File(root,name).isFile())throw new IOException("Missing game data: "+name);
            if(new File(root,"CLAW.REZ").length()<=168)throw new IOException("Incomplete CLAW.REZ");
            EngineSupport.install(context,root);
            AppLanguage.writeNative(context,root);
            SaveFiles.applyPending(root);
            SaveFiles.ensureInitial(context,root);
        }
    }
    private GameFiles() { }
}
