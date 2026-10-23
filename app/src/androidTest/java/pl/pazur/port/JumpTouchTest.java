package pl.pazur.port;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.InputDevice;
import android.view.MotionEvent;
import java.io.File;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

/** Events go directly to this game's window, never to another foreground app. */
public class JumpTouchTest extends Instrumentation {
    private Activity game;
    private boolean baseline;
    private boolean gameOver;
    private boolean deathWithPowerup;
    private int gameOverTaps=1;
    private boolean score;
    private boolean directActivity;
    private long down;
    private int width, height, ticket;
    private float logicalWidth;
    private File folder;

    @Override public void onCreate(Bundle args) {
        super.onCreate(args);
        baseline="baseline".equals(args.getString("layout"));
        gameOver="game-over".equals(args.getString("scenario"));
        deathWithPowerup="true".equals(args.getString("death_powerup"));
        gameOverTaps=Math.max(1,Math.min(8,Integer.parseInt(args.getString("death_taps","1"))));
        score="score".equals(args.getString("scenario"));
        directActivity="true".equals(args.getString("direct_activity"));
        start();
    }
    private void focus() {
        if (game==null || game.isFinishing() || !game.hasWindowFocus())
            throw new IllegalStateException("Game lost focus; no input sent");
    }
    private void command(String command) throws Exception {
        focus();
        String key="jump"+(++ticket);
        File temporary=new File(folder,"combat-command.tmp");
        try (FileOutputStream out=new FileOutputStream(temporary)) {
            out.write((key+"|"+command+"\n").getBytes(StandardCharsets.US_ASCII));
        }
        if (!temporary.renameTo(new File(folder,"combat-command.txt")))
            throw new IllegalStateException("Cannot publish test command");
        File response=new File(folder,"combat-response.txt");
        long deadline=SystemClock.uptimeMillis()+45000;
        long retryAt=0;
        while (SystemClock.uptimeMillis()<deadline) {
            focus();
            if (response.exists()) {
                try (java.io.BufferedReader reader=new java.io.BufferedReader(new java.io.FileReader(response))) {
                    String reply=reader.readLine();
                    if ((key+"|done").equals(reply)) return;
                    if (reply!=null && reply.startsWith(key+"|rejected:") && SystemClock.uptimeMillis()>=retryAt) {
                        // Slow devices may still be loading when the first fixture is requested.
                        retryAt=SystemClock.uptimeMillis()+1000;
                        try(FileOutputStream out=new FileOutputStream(temporary)) {
                            out.write((key+"|"+command+"\n").getBytes(StandardCharsets.US_ASCII));
                        }
                        if(!temporary.renameTo(new File(folder,"combat-command.txt")))
                            throw new IllegalStateException("Cannot retry test command");
                    }
                }
            }
            SystemClock.sleep(20);
        }
        throw new IllegalStateException("No acknowledgement: "+command);
    }
    private void touch(int action,int[] ids,float[][] points) {
        focus();
        MotionEvent.PointerProperties[] properties=new MotionEvent.PointerProperties[ids.length];
        MotionEvent.PointerCoords[] coords=new MotionEvent.PointerCoords[ids.length];
        for (int i=0;i<ids.length;i++) {
            properties[i]=new MotionEvent.PointerProperties();
            properties[i].id=ids[i]; properties[i].toolType=MotionEvent.TOOL_TYPE_FINGER;
            coords[i]=new MotionEvent.PointerCoords();
            coords[i].x=points[i][0]*width/logicalWidth;
            coords[i].y=points[i][1]*height/480f;
            coords[i].pressure=1;coords[i].size=.1f;
        }
        MotionEvent event=MotionEvent.obtain(down,SystemClock.uptimeMillis(),action,ids.length,
            properties,coords,0,0,1,1,0,0,InputDevice.SOURCE_TOUCHSCREEN,0);
        runOnMainSync(()-> { focus();game.getWindow().getDecorView().dispatchTouchEvent(event); });
        event.recycle();
    }
    private void single(int action,float x,float y) {
        touch(action,new int[]{11},new float[][]{{x,y}});
    }
    private void screenshot(String name) throws Exception {
        Bitmap shot=getUiAutomation().takeScreenshot();
        if (shot==null) throw new IllegalStateException("No screenshot");
        try (FileOutputStream out=new FileOutputStream(new File(folder,name))) {
            shot.compress(Bitmap.CompressFormat.PNG,100,out);
        }
        shot.recycle();
    }
    @Override public void onStart() {
        Bundle result=new Bundle();
        try {
            ActivityMonitor monitor=addMonitor("pl.pazur.port.GameActivity",null,false);
            Intent launch=new Intent().setClassName(getTargetContext(),directActivity?"pl.pazur.port.GameActivity":"pl.pazur.port.LauncherActivity")
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getTargetContext().startActivity(launch);
            game=waitForMonitorWithTimeout(monitor,30000);
            long deadline=SystemClock.uptimeMillis()+10000;
            while (game!=null && !game.hasWindowFocus() && SystemClock.uptimeMillis()<deadline) SystemClock.sleep(50);
            focus();
            SystemClock.sleep(7000);
            Bitmap shot=getUiAutomation().takeScreenshot();
            width=shot.getWidth();height=shot.getHeight();shot.recycle();
            if (width<=height) throw new IllegalStateException("Expected landscape game");
            logicalWidth=Math.max(640,Math.round(480f*width/height));
            folder=getTargetContext().getExternalFilesDir(null);
            if(score) {
                command("campaignfinish");
                SystemClock.sleep(8000);
                screenshot("score-window-before.png");
                for(int tap=0;tap<3;tap++) {
                    down=SystemClock.uptimeMillis();
                    single(MotionEvent.ACTION_DOWN,logicalWidth/2,240);
                    SystemClock.sleep(80);
                    single(MotionEvent.ACTION_UP,logicalWidth/2,240);
                    SystemClock.sleep(700);
                }
                SystemClock.sleep(10000);
                screenshot("score-window-after.png");
                result.putString("stream","Real end pickup and Android window taps completed.\n");
                finish(0,result);return;
            }
            if(gameOver) {
                if(deathWithPowerup){command("catnip");SystemClock.sleep(500);}
                command("combatlastlife");
                SystemClock.sleep(4500);
                screenshot("game-over-before.png");
                for(int tap=0;tap<gameOverTaps;tap++) {
                    down=SystemClock.uptimeMillis();
                    single(MotionEvent.ACTION_DOWN,logicalWidth/2,240);
                    SystemClock.sleep(30);
                    single(MotionEvent.ACTION_UP,logicalWidth/2,240);
                    SystemClock.sleep(30);
                }
                // Returning to Main initializes its pages/textures. This is a
                // functional exit check, not a 1.5-second load-time assertion.
                SystemClock.sleep(8000);
                screenshot("game-over-after.png");
                result.putString("stream","Last-life death and app-local touch completed.\n");
                finish(0,result);return;
            }
            float x=logicalWidth-(baseline?56:74),y=baseline?438:406;
            int[] durations={10,100,250,700,1800,100};
            for (int i=0;i<durations.length;i++) {
                command("combatstage -1 80 0");
                SystemClock.sleep(400);
                command("combatjumpmeasure "+(i==5?"drift100":"hold"+durations[i]));
                down=SystemClock.uptimeMillis();
                single(MotionEvent.ACTION_DOWN,x,y);
                if (i==5) {
                    SystemClock.sleep(40);
                    single(MotionEvent.ACTION_MOVE,x-110,y-5);
                    SystemClock.sleep(60);
                    single(MotionEvent.ACTION_UP,x-110,y-5);
                } else {
                    SystemClock.sleep(durations[i]);
                    single(MotionEvent.ACTION_UP,x,y);
                }
                SystemClock.sleep(Math.max(500,2500-durations[i]));
            }
            if (!baseline) {
                command("combatstage -1 80 0");SystemClock.sleep(400);
                down=SystemClock.uptimeMillis();
                touch(MotionEvent.ACTION_DOWN,new int[]{11},new float[][]{{147,394}});
                SystemClock.sleep(120);
                touch(MotionEvent.ACTION_POINTER_DOWN|(1<<MotionEvent.ACTION_POINTER_INDEX_SHIFT),
                    new int[]{11,29},new float[][]{{147,394},{x,y}});
                SystemClock.sleep(300);
                screenshot("jump-multitouch.png");
                touch(MotionEvent.ACTION_POINTER_UP,new int[]{11,29},new float[][]{{147,394},{x,y}});
                SystemClock.sleep(120);
                touch(MotionEvent.ACTION_UP,new int[]{29},new float[][]{{x,y}});
                SystemClock.sleep(300);
                for (float[] point:new float[][]{{logicalWidth-210,410},{logicalWidth-145,276}}) {
                    down=SystemClock.uptimeMillis();single(MotionEvent.ACTION_DOWN,point[0],point[1]);
                    SystemClock.sleep(120);single(MotionEvent.ACTION_UP,point[0],point[1]);
                }
                down=SystemClock.uptimeMillis();single(MotionEvent.ACTION_DOWN,x,y);
                SystemClock.sleep(30);single(MotionEvent.ACTION_CANCEL,x,y);
                SystemClock.sleep(300);
                screenshot("jump-layout.png");
                // Pause from the game surface and resume through the centered menu.
                down=SystemClock.uptimeMillis();single(MotionEvent.ACTION_DOWN,45,96);
                single(MotionEvent.ACTION_UP,45,96);SystemClock.sleep(350);
                screenshot("jump-pause.png");
                down=SystemClock.uptimeMillis();single(MotionEvent.ACTION_DOWN,logicalWidth/2,160);
                single(MotionEvent.ACTION_UP,logicalWidth/2,160);SystemClock.sleep(350);
                command("combatstatus");
                down=SystemClock.uptimeMillis();single(MotionEvent.ACTION_DOWN,147,394);
                SystemClock.sleep(120);
                runOnMainSync(()->game.moveTaskToBack(true));
                SystemClock.sleep(500);
                getTargetContext().startActivity(launch);
                SystemClock.sleep(1200);
                focus();
                screenshot("jump-focus.png");
            }
            result.putString("stream","App-local touch and jump measurements completed.\n");finish(0,result);
        } catch (Exception failure) {
            result.putString("stream",failure.toString());finish(1,result);
        }
    }
}
