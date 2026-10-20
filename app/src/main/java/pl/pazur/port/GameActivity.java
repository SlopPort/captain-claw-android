package pl.pazur.port;

import org.libsdl.app.SDLActivity;
import android.os.Bundle;
import android.view.KeyEvent;
import java.io.*;

public class GameActivity extends SDLActivity {
    public static native void nativePadButton(int device, int key, boolean down);
    @Override public void onBackPressed() {
        // Let the game open its pause menu or return to the previous menu page.
        SDLActivity.onNativeKeyDown(KeyEvent.KEYCODE_ESCAPE);
        SDLActivity.onNativeKeyUp(KeyEvent.KEYCODE_ESCAPE);
    }
    @Override public boolean dispatchKeyEvent(KeyEvent event) {
        if ((event.getSource() & android.view.InputDevice.SOURCE_GAMEPAD) != 0 &&
            (KeyEvent.isGamepadButton(event.getKeyCode()) || event.getKeyCode()==KeyEvent.KEYCODE_BACK)) {
            if (event.getAction()==KeyEvent.ACTION_DOWN && event.getRepeatCount()==0)
                nativePadButton(event.getDeviceId(),event.getKeyCode(),true);
            else if (event.getAction()==KeyEvent.ACTION_UP)
                nativePadButton(event.getDeviceId(),event.getKeyCode(),false);
            return true; // Avoid a second action through SDL's device-specific button mapping.
        }
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
        android.widget.Button pad = new android.widget.Button(this);
        pad.setText("PAD");
        pad.setTextSize(12);
        pad.setFocusable(false);
        pad.setContentDescription("Ustawienia pada / Controller settings");
        pad.setOnClickListener(v -> startActivity(new android.content.Intent(this,ControllerSettingsActivity.class)));
        android.widget.RelativeLayout.LayoutParams position = new android.widget.RelativeLayout.LayoutParams(
            (int)(64*getResources().getDisplayMetrics().density), (int)(44*getResources().getDisplayMetrics().density));
        position.addRule(android.widget.RelativeLayout.ALIGN_PARENT_TOP);
        position.addRule(android.widget.RelativeLayout.ALIGN_PARENT_RIGHT);
        mLayout.addView(pad,position);
    }
    @Override protected String[] getLibraries() {
        return new String[] { "SDL2", "openclaw" };
    }
    @Override protected String[] getArguments() {
        return new String[] { getExternalFilesDir(null).getAbsolutePath() };
    }
}
