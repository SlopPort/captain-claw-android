package pl.pazur.port;

import org.libsdl.app.SDLActivity;
import android.os.Bundle;
import android.view.KeyEvent;
import java.io.*;

public class GameActivity extends SDLActivity {
    private android.widget.Button settingsButton;
    private boolean menuOverlayMode=true;
    /** Called only when the SDL presentation context changes. Main-menu Quit
     * occupies the bottom center, so keep settings above the menu there. During
     * play retain the bottom position that leaves the health HUD unobstructed. */
    public void setMenuOverlay(boolean menu) {
        runOnUiThread(()-> {
            menuOverlayMode=menu;
            if(settingsButton==null)return;
            float density=getResources().getDisplayMetrics().density;
            android.widget.RelativeLayout.LayoutParams position=new android.widget.RelativeLayout.LayoutParams((int)(64*density),(int)(44*density));
            position.addRule(android.widget.RelativeLayout.CENTER_HORIZONTAL);
            position.addRule(menu?android.widget.RelativeLayout.ALIGN_PARENT_TOP:android.widget.RelativeLayout.ALIGN_PARENT_BOTTOM);
            if(menu)position.topMargin=(int)(8*density);else position.bottomMargin=(int)(8*density);
            settingsButton.setLayoutParams(position);
        });
    }
    @Override protected void attachBaseContext(android.content.Context context) {
        super.attachBaseContext(AppLanguage.wrap(context));
    }
    public static native void nativePadButton(int device, int key, boolean down);
    public int getTouchLayout() {
        return getSharedPreferences("controls",MODE_PRIVATE).getInt("touch_layout",0);
    }
    public int[] getControlOptions() {
        android.content.SharedPreferences prefs=getSharedPreferences("controls",MODE_PRIVATE);
        int[] options=new int[18];
        options[0]=prefs.getInt("movement",0);
        options[1]=prefs.getInt("deadzone",14);
        options[2]=prefs.getInt("difficulty",1);
        for(int i=0;i<5;i++) {
            options[3+i*3]=prefs.getInt("button_size_"+i,100);
            options[4+i*3]=prefs.getInt("button_x_"+i,0);
            options[5+i*3]=prefs.getInt("button_y_"+i,0);
        }
        return options;
    }
    public void openDifficultySettings() {
        runOnUiThread(()->startActivity(new android.content.Intent(this,ControllerSettingsActivity.class).putExtra("difficulty_only",true)));
    }
    public void openControlSettings() {
        runOnUiThread(()->startActivity(new android.content.Intent(this,ControllerSettingsActivity.class)));
    }
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
        super.onCreate(state);
        android.widget.Button pad = new android.widget.Button(this);
        settingsButton=pad;
        pad.setText("PAD");
        pad.setTextSize(12);
        pad.setFocusable(false);
        pad.setContentDescription(getString(R.string.pad_accessibility));
        pad.setOnClickListener(v -> startActivity(new android.content.Intent(this,ControllerSettingsActivity.class)));
        android.widget.RelativeLayout.LayoutParams position = new android.widget.RelativeLayout.LayoutParams(
            (int)(64*getResources().getDisplayMetrics().density), (int)(44*getResources().getDisplayMetrics().density));
        position.addRule(android.widget.RelativeLayout.ALIGN_PARENT_BOTTOM);
        position.addRule(android.widget.RelativeLayout.CENTER_HORIZONTAL);
        position.bottomMargin=(int)(8*getResources().getDisplayMetrics().density);
        mLayout.addView(pad,position);
        setMenuOverlay(menuOverlayMode);
    }
    @Override protected String[] getLibraries() {
        return new String[] { "SDL2", "openclaw" };
    }
    /** Called on the SDL thread; Vibrator is thread-safe. Disabled by default. */
    public void pulseHaptic(int duration) {
        if(!new File(getExternalFilesDir(null),"haptics-enabled").isFile())return;
        android.os.Vibrator vibrator=(android.os.Vibrator)getSystemService(VIBRATOR_SERVICE);
        if(vibrator==null||!vibrator.hasVibrator())return;
        if(android.os.Build.VERSION.SDK_INT>=26)vibrator.vibrate(android.os.VibrationEffect.createOneShot(duration,80));
        else vibrator.vibrate(duration);
    }
    @Override protected String[] getArguments() {
        try {GameFiles.prepare(this);}
        catch(Exception error) {
            android.util.Log.e("Pazur","Native startup preparation failed",error);
            runOnUiThread(()->startActivity(new android.content.Intent(this,LauncherActivity.class)
                .putExtra("startup_error",error.toString())));
            return new String[] { "--startup-aborted" };
        }
        return new String[] { getExternalFilesDir(null).getAbsolutePath() };
    }
}
