package pl.pazur.port;

import android.app.Activity;
import android.app.AlertDialog;
import android.os.Bundle;
import android.view.InputDevice;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.widget.*;
import java.io.*;
import java.util.Properties;

/** Physical key capture avoids assumptions about Xbox/Switch printed labels.
 * Saves atomically; the SDL thread reloads only a complete binding file.
 * LLM-authored adaptation: see docs/DEVELOPMENT-NOTES.md.
 */
public class ControllerSettingsActivity extends Activity {
    private static final String[] ACTIONS={"jump","attack","fire","weapon","pause","confirm","back"};
    private static final int[] DEFAULTS={96,99,97,100,108,96,97};
    private final int[] bindings=DEFAULTS.clone();
    private final Button[] rows=new Button[7];
    private boolean english;
    private int capturing=-1;
    private AlertDialog capture;
    private boolean triggerReady;

    private String tr(String pl,String en) { return english?en:pl; }
    private String action(int i) {
        return (english ? new String[]{"Jump","Sword attack","Shoot","Change weapon","Pause","Menu: confirm","Menu: back"}
            : new String[]{"Skok","Atak szablą","Strzał","Zmiana broni","Pauza","Menu: zatwierdź","Menu: wstecz"})[i];
    }
    private File file() { return new File(getExternalFilesDir(null),"controller-bindings.txt"); }
    private String name(int code) {
        if (code==1000) return "LT / L2";
        if (code==1001) return "RT / R2";
        return KeyEvent.keyCodeToString(code).replace("KEYCODE_","");
    }
    private void refresh() { for (int i=0;i<7;i++) rows[i].setText(action(i)+": "+name(bindings[i])); }
    private void save() throws IOException {
        File temporary=new File(getExternalFilesDir(null),"controller-bindings.tmp");
        try (Writer out=new OutputStreamWriter(new FileOutputStream(temporary),"US-ASCII")) {
            for(int i=0;i<7;i++) out.write(ACTIONS[i]+"="+bindings[i]+"\n");
        }
        if (!temporary.renameTo(file())) throw new IOException("Cannot save controller bindings");
    }
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        english=!getResources().getConfiguration().locale.getLanguage().equals("pl");
        try (InputStream input=new FileInputStream(file())) {
            Properties values=new Properties();values.load(input);
            for(int i=0;i<7;i++) {
                int code=Integer.parseInt(values.getProperty(ACTIONS[i],""+DEFAULTS[i]));
                if(code>=0 && code<=1001) bindings[i]=code;
            }
        } catch(Exception ignored) { /* Missing/invalid file falls back to usable defaults. */ }
        ScrollView scroll=new ScrollView(this);
        LinearLayout layout=new LinearLayout(this);layout.setOrientation(LinearLayout.VERTICAL);
        int padding=(int)(16*getResources().getDisplayMetrics().density);
        layout.setPadding(padding,padding,padding,padding);
        TextView intro=new TextView(this);
        intro.setText(tr("Ustawienia pada\nWybierz czynność, a potem naciśnij przycisk lub spust. Ustawienia zapisują się automatycznie. Zajęty przycisk zamienia przypisania w tej samej grupie. Nazwy przycisków pochodzą z Androida. Ruch: gałka / krzyżak.",
            "Controller settings\nChoose an action, then press a button or trigger. Changes save automatically. Occupied buttons swap assignments within the same group. Button names come from Android. Movement: left stick / D-pad."));
        intro.setTextSize(18);layout.addView(intro);
        for(int i=0;i<7;i++) {
            final int index=i;rows[i]=new Button(this);
            rows[i].setOnClickListener(v -> beginCapture(index));layout.addView(rows[i]);
        }
        Button reset=new Button(this);reset.setText(tr("Przywróć domyślne","Restore defaults"));
        reset.setOnClickListener(v -> {
            int[] previous=bindings.clone();System.arraycopy(DEFAULTS,0,bindings,0,7);
            try {save();refresh();} catch(IOException error) {System.arraycopy(previous,0,bindings,0,7);showError(error);}
        });layout.addView(reset);
        Button files=new Button(this);files.setText(tr("Kopie zapisów i wibracje","Save backups and vibration"));files.setOnClickListener(v->startActivity(new android.content.Intent(this,FileToolsActivity.class)));layout.addView(files);
        Button done=new Button(this);done.setText(tr("Wróć do gry","Return to game"));done.setOnClickListener(v -> finish());layout.addView(done);
        scroll.addView(layout);setContentView(scroll);refresh();
    }
    private void showError(Exception error) {
        new AlertDialog.Builder(this).setMessage(tr("Nie zapisano ustawień: ","Settings were not saved: ")+error.getMessage()).setPositiveButton("OK",null).show();
    }
    private void beginCapture(int index) {
        capturing=index;triggerReady=false;
        capture=new AlertDialog.Builder(this).setTitle(action(index))
            .setMessage(tr("Puść przyciski i spusty, potem naciśnij wybrany. Ruch gałką nie zmienia przypisania.",
                "Release buttons and triggers, then press the desired one. Stick movement does not bind an action."))
            .setNegativeButton(tr("Anuluj","Cancel"),(d,w)->capturing=-1).create();
        capture.setOnDismissListener(d -> capturing=-1);
        capture.setOnKeyListener((d,key,event)->captureKey(event));
        capture.show();
        // Triggers must pass through a released sample before a press is captured.
        capture.getWindow().getDecorView().setOnGenericMotionListener((v,event)->captureMotion(event));
    }
    private void bind(int code) {
        if(capturing<0)return;
        final int index=capturing;int[] previous=bindings.clone();
        int first=index<5?0:5,last=index<5?5:7;
        for(int i=first;i<last;i++) if(i!=index && bindings[i]==code) bindings[i]=previous[index];
        bindings[index]=code;
        try {save();refresh();capture.dismiss();}
        catch(IOException error) {System.arraycopy(previous,0,bindings,0,7);capture.dismiss();showError(error);}
    }
    private boolean captureKey(KeyEvent event) {
        if(capturing<0 || (event.getSource()&InputDevice.SOURCE_GAMEPAD)==0)return false;
        if(!KeyEvent.isGamepadButton(event.getKeyCode()) && event.getKeyCode()!=KeyEvent.KEYCODE_BACK)return false;
        if(event.getAction()==KeyEvent.ACTION_DOWN && event.getRepeatCount()==0)bind(event.getKeyCode());
        return true;
    }
    private boolean captureMotion(MotionEvent event) {
        if(capturing<0 || (event.getSource()&InputDevice.SOURCE_JOYSTICK)==0)return false;
        float left=event.getAxisValue(MotionEvent.AXIS_LTRIGGER),right=event.getAxisValue(MotionEvent.AXIS_RTRIGGER);
        if(left<.2f && right<.2f)triggerReady=true;
        if(triggerReady && left>.6f)bind(1000);
        else if(triggerReady && right>.6f)bind(1001);
        return true;
    }
    @Override public boolean dispatchKeyEvent(KeyEvent event) {
        return captureKey(event)||super.dispatchKeyEvent(event);
    }
    @Override public boolean dispatchGenericMotionEvent(MotionEvent event) {
        return captureMotion(event)||super.dispatchGenericMotionEvent(event);
    }
}
