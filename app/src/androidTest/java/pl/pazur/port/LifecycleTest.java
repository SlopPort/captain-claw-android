package pl.pazur.port;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import java.io.File;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

/** Codex: app-owned activity transitions only; no system-wide input or settings. */
public class LifecycleTest extends Instrumentation {
    private File folder;
    private int ticket;
    private void command(String value) throws Exception {
        String tag="lifecycle-"+(++ticket);
        File temporary=new File(folder,"combat-command.tmp");
        try(FileOutputStream out=new FileOutputStream(temporary)) {
            out.write((tag+"|"+value+"\n").getBytes(StandardCharsets.US_ASCII));
        }
        if(!temporary.renameTo(new File(folder,"combat-command.txt")))throw new Exception("Cannot publish command");
        long until=SystemClock.uptimeMillis()+10000;
        while(SystemClock.uptimeMillis()<until) {
            File response=new File(folder,"combat-response.txt");
            if(response.isFile()) {
                String text;
                try(java.io.FileInputStream in=new java.io.FileInputStream(response)) {
                    byte[] bytes=new byte[1024];int count=in.read(bytes);
                    text=count>0?new String(bytes,0,count,StandardCharsets.US_ASCII).trim():"";
                }
                if(text.equals(tag+"|done"))return;
                if(text.startsWith(tag+"|rejected"))throw new Exception(text);
            }
            SystemClock.sleep(30);
        }
        throw new Exception("No response: "+value);
    }
    @Override public void onCreate(Bundle args){super.onCreate(args);start();}
    @Override public void onStart() {
        Bundle result=new Bundle();
        try {
            ActivityMonitor gameMonitor=addMonitor("pl.pazur.port.GameActivity",null,false);
            getTargetContext().startActivity(new Intent().setClassName(getTargetContext(),"pl.pazur.port.LauncherActivity")
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            Activity game=waitForMonitorWithTimeout(gameMonitor,30000);
            if(game==null)throw new Exception("Game not opened");
            SystemClock.sleep(7000);
            if(!game.hasWindowFocus())throw new Exception("Game not focused");
            folder=getTargetContext().getExternalFilesDir(null);
            command("padvirtual attach");SystemClock.sleep(300);
            command("padvirtual axis leftx 32767");SystemClock.sleep(250);
            ActivityMonitor settingsMonitor=addMonitor("pl.pazur.port.ControllerSettingsActivity",null,false);
            runOnMainSync(()->game.startActivity(new Intent(game,ControllerSettingsActivity.class)));
            Activity settings=waitForMonitorWithTimeout(settingsMonitor,10000);
            if(settings==null)throw new Exception("Settings not opened");
            SystemClock.sleep(800);
            if(game.hasWindowFocus())throw new Exception("Game retained focus under settings");
            runOnMainSync(settings::finish);
            long until=SystemClock.uptimeMillis()+10000;
            while(!game.hasWindowFocus()&&SystemClock.uptimeMillis()<until)SystemClock.sleep(50);
            if(!game.hasWindowFocus())throw new Exception("Game focus not restored");
            // Axis remains held: the game's neutral gate should prevent drift.
            SystemClock.sleep(400);command("laddertrace lifecycle-held-resume 1600");SystemClock.sleep(1900);
            command("padvirtual axis leftx 0");SystemClock.sleep(150);
            command("laddertrace lifecycle-repress 900");command("padvirtual axis leftx 32767");SystemClock.sleep(500);
            command("padvirtual axis leftx 0");SystemClock.sleep(600);
            command("padvirtual detach");
            result.putString("lifecycle","PASS: game/settings/focus restored; native trace checks required");
            finish(0,result);
        }catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));finish(1,result);}
    }
}
