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
public class ControllerSettingsActivity extends LocalizedActivity {
    private static final String[] ACTIONS={"jump","attack","fire","weapon","pause","confirm","back"};
    private static final int[] DEFAULTS={96,99,97,100,108,96,97};
    private final int[] bindings=DEFAULTS.clone();
    private final Button[] rows=new Button[7];
    private int capturing=-1;
    private AlertDialog capture;
    private boolean triggerReady;

    private String action(int i) {
        return getString(new int[]{R.string.action_jump,R.string.action_attack,R.string.action_fire,
            R.string.action_weapon,R.string.action_pause,R.string.action_confirm,R.string.action_back}[i]);
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
        if(getIntent().getBooleanExtra("difficulty_only",false)) {
            LinearLayout difficulty=new LinearLayout(this);difficulty.setOrientation(LinearLayout.VERTICAL);difficulty.setPadding(24,24,24,24);
            GameplaySettingsUi.difficulty(this,difficulty);
            Button done=new Button(this);done.setText(R.string.return_game);done.setOnClickListener(v->finish());difficulty.addView(done);
            setContentView(difficulty);return;
        }
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
        intro.setText(getString(R.string.controller_intro));
        intro.setTextSize(18);layout.addView(intro);
        TextView touchTitle=new TextView(this);touchTitle.setText(R.string.touch_layout_title);
        touchTitle.setTextSize(20);layout.addView(touchTitle);
        RadioGroup layouts=new RadioGroup(this);
        String[] titles=getResources().getStringArray(R.array.touch_layout_names);
        String[] descriptions=getResources().getStringArray(R.array.touch_layout_descriptions);
        int selected=getSharedPreferences("controls",MODE_PRIVATE).getInt("touch_layout",0);
        for(int i=0;i<titles.length;i++) {
            RadioButton choice=new RadioButton(this);choice.setId(2000+i);
            choice.setText(titles[i]+"\n"+descriptions[i]);layouts.addView(choice);
        }
        layouts.check(2000+(selected>=0&&selected<titles.length?selected:0));
        layouts.setOnCheckedChangeListener((group,id)-> {
            if(!getSharedPreferences("controls",MODE_PRIVATE).edit().putInt("touch_layout",id-2000).commit())
                showError(new IOException(getString(R.string.settings_save_error)));
        });layout.addView(layouts);
        GameplaySettingsUi.controls(this,layout);
        for(int i=0;i<7;i++) {
            final int index=i;rows[i]=new Button(this);
            rows[i].setOnClickListener(v -> beginCapture(index));layout.addView(rows[i]);
        }
        Button reset=new Button(this);reset.setText(getString(R.string.restore_defaults));
        reset.setOnClickListener(v -> {
            int[] previous=bindings.clone();System.arraycopy(DEFAULTS,0,bindings,0,7);
            try {save();refresh();} catch(IOException error) {System.arraycopy(previous,0,bindings,0,7);showError(error);}
        });layout.addView(reset);
        Button files=new Button(this);files.setText(getString(R.string.save_tools));files.setOnClickListener(v->startActivity(new android.content.Intent(this,FileToolsActivity.class)));layout.addView(files);
        Button language=new Button(this);language.setText(R.string.language);
        language.setOnClickListener(v->AppLanguage.choose(this));layout.addView(language);
        TextView languageHelp=new TextView(this);languageHelp.setText(R.string.language_restart);layout.addView(languageHelp);
        Button done=new Button(this);done.setText(getString(R.string.return_game));done.setOnClickListener(v -> finish());layout.addView(done);
        scroll.addView(layout);setContentView(scroll);refresh();
    }
    private void showError(Exception error) {
        new AlertDialog.Builder(this).setMessage(getString(R.string.settings_save_error)+error.getMessage()).setPositiveButton("OK",null).show();
    }
    private void beginCapture(int index) {
        capturing=index;triggerReady=false;
        capture=new AlertDialog.Builder(this).setTitle(action(index))
            .setMessage(getString(R.string.capture_hint))
            .setNegativeButton(getString(R.string.cancel),(d,w)->capturing=-1).create();
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
