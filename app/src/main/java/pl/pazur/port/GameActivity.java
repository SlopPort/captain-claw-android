package pl.pazur.port;

import org.libsdl.app.SDLActivity;
import android.os.Bundle;
import android.view.KeyEvent;
import java.io.*;

public class GameActivity extends SDLActivity {
    @Override public void onBackPressed() {
        // Let the game open its pause menu or return to the previous menu page.
        SDLActivity.onNativeKeyDown(KeyEvent.KEYCODE_ESCAPE);
        SDLActivity.onNativeKeyUp(KeyEvent.KEYCODE_ESCAPE);
    }
    @Override public boolean dispatchKeyEvent(KeyEvent event) {
        if (event.getKeyCode() == KeyEvent.KEYCODE_BACK) {
            if (event.getAction() == KeyEvent.ACTION_UP) onBackPressed();
            return true;
        }
        return super.dispatchKeyEvent(event);
    }
    @Override public void onCreate(Bundle state) {
        File saves = new File(getExternalFilesDir(null), "SAVES.XML");
        if (!saves.exists()) {
            try (InputStream input = getAssets().open("default-saves.xml");
                 OutputStream output = new FileOutputStream(saves)) {
                byte[] bytes = new byte[4096];
                int count;
                while ((count = input.read(bytes)) != -1) output.write(bytes, 0, count);
            } catch (IOException error) {
                android.util.Log.e("Pazur", "Cannot create initial save", error);
            }
        }
        super.onCreate(state);
    }
    @Override protected String[] getLibraries() {
        return new String[] { "SDL2", "openclaw" };
    }
    @Override protected String[] getArguments() {
        return new String[] { getExternalFilesDir(null).getAbsolutePath() };
    }
}
