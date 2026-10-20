package pl.pazur.port;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.InputDevice;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Properties;

/** Calls only this app's activities; never injects global Android input. */
public class ControllerBindingsTest extends Instrumentation {
    private File folder;
    private int ticket;
    private Activity game;
    @Override public void onCreate(Bundle args) {super.onCreate(args);start();}
    private Button find(View view,String text) {
        if(view instanceof Button && ((Button)view).getText().toString().contains(text))return (Button)view;
        if(view instanceof ViewGroup) {
            ViewGroup group=(ViewGroup)view;
            for(int i=0;i<group.getChildCount();i++) {Button result=find(group.getChildAt(i),text);if(result!=null)return result;}
        }
        return null;
    }
    private void key(Activity activity,int code,boolean down) {
        runOnMainSync(()-> {
            if(activity==game && !activity.hasWindowFocus())throw new IllegalStateException("Game lost focus");
            long now=SystemClock.uptimeMillis();
            KeyEvent event=new KeyEvent(now,now,down?KeyEvent.ACTION_DOWN:KeyEvent.ACTION_UP,code,0);
            event.setSource(InputDevice.SOURCE_GAMEPAD);
            activity.dispatchKeyEvent(event);
        });
    }
    private void command(String value) throws Exception {
        String tag="bind-test-"+(++ticket);
        File temporary=new File(folder,"combat-command.tmp");
        try(FileOutputStream out=new FileOutputStream(temporary)) {out.write((tag+"|"+value+"\n").getBytes(StandardCharsets.US_ASCII));}
        if(!temporary.renameTo(new File(folder,"combat-command.txt")))throw new IOException("Mailbox rename failed");
        long deadline=SystemClock.uptimeMillis()+45000;
        long retryAt=0;
        while(SystemClock.uptimeMillis()<deadline) {
            File response=new File(folder,"combat-response.txt");
            if(response.exists())try(BufferedReader reader=new BufferedReader(new FileReader(response))) {
                String reply=reader.readLine();
                if((tag+"|done").equals(reply))return;
                if(reply!=null && reply.startsWith(tag+"|rejected:") && SystemClock.uptimeMillis()>=retryAt) {
                    // Menus render before level loading finishes; wait for live physics.
                    retryAt=SystemClock.uptimeMillis()+1000;
                    try(FileOutputStream out=new FileOutputStream(temporary)) {out.write((tag+"|"+value+"\n").getBytes(StandardCharsets.US_ASCII));}
                    if(!temporary.renameTo(new File(folder,"combat-command.txt")))throw new IOException("Mailbox retry failed");
                }
            }
            SystemClock.sleep(50);
        }
        throw new IOException("No response: "+value);
    }
    @Override public void onStart() {
        Bundle result=new Bundle();
        try {
            ActivityMonitor gameMonitor=addMonitor("pl.pazur.port.GameActivity",null,false);
            Intent launch=new Intent(Intent.ACTION_MAIN).setClassName("pl.pazur.port","pl.pazur.port.LauncherActivity").addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getTargetContext().startActivity(launch);
            game=waitForMonitorWithTimeout(gameMonitor,15000);
            if(game==null)throw new IllegalStateException("No game activity");
            folder=getTargetContext().getExternalFilesDir(null);
            long focusDeadline=SystemClock.uptimeMillis()+10000;
            while(!game.hasWindowFocus() && SystemClock.uptimeMillis()<focusDeadline)SystemClock.sleep(50);
            SystemClock.sleep(7000);
            command("padvirtual attach");
            command("combatstage -1 80 0");
            ActivityMonitor settingsMonitor=addMonitor("pl.pazur.port.ControllerSettingsActivity",null,false);
            runOnMainSync(()->find(game.getWindow().getDecorView(),"PAD").performClick());
            Activity settings=waitForMonitorWithTimeout(settingsMonitor,8000);
            if(settings==null)throw new IllegalStateException("No settings activity");
            SystemClock.sleep(500);
            runOnMainSync(()-> {
                Button attack=find(settings.getWindow().getDecorView(),"szablą");
                if(attack==null)attack=find(settings.getWindow().getDecorView(),"Sword attack");
                if(attack==null)throw new IllegalStateException("No attack row");
                attack.performClick();
            });
            SystemClock.sleep(200);
            key(settings,KeyEvent.KEYCODE_BUTTON_L1,true);
            key(settings,KeyEvent.KEYCODE_BUTTON_L1,false);
            Properties values=new Properties();
            try(InputStream in=new FileInputStream(new File(folder,"controller-bindings.txt"))) {values.load(in);}
            if(!"102".equals(values.getProperty("attack")))throw new IllegalStateException("Binding was not saved");
            runOnMainSync(settings::finish);
            SystemClock.sleep(1700);
            command("combatdummy 16 55 0");
            command("combatkey right 20");
            // Capture UI, saved file, Java dispatch, JNI and SDL must all agree.
            key(game,KeyEvent.KEYCODE_BUTTON_L1,true);
            SystemClock.sleep(150);
            key(game,KeyEvent.KEYCODE_BUTTON_L1,false);
            SystemClock.sleep(500);
            command("combatstatus");
            command("padvirtual detach");
            result.putString("result","PASS: captured L1, persisted attack=102, returned to game and dispatched input");
            finish(0,result);
        } catch(Throwable error) {
            result.putString("error",error.toString());finish(1,result);
        }
    }
}
