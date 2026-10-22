package pl.pazur.port;

import android.app.Activity;
import android.app.Application;
import android.app.Instrumentation;
import android.content.Intent;
import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.InputDevice;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import java.io.*;

/** Navigate only the focused game window. No global events or controller input.
 * CampaignSession supplies isolated progress/configuration outside this class. */
public class MenuTouchTest extends Instrumentation {
    private String language;
    private boolean dismissIntro;
    private int cycles;
    private volatile Activity game;
    private int width,height;
    private float logicalWidth;
    private File root;
    private final Application.ActivityLifecycleCallbacks lifecycle=new Application.ActivityLifecycleCallbacks() {
        public void onActivityResumed(Activity activity) {
            if(activity instanceof GameActivity) {game=activity;android.util.Log.i("SDL/APP","Pazur menu test resumed: "+System.identityHashCode(activity));}
        }
        public void onActivityPaused(Activity activity) {if(activity instanceof GameActivity)android.util.Log.i("SDL/APP","Pazur menu test paused: "+System.identityHashCode(activity));}
        public void onActivityCreated(Activity activity,Bundle state){}
        public void onActivityStarted(Activity activity){}
        public void onActivityStopped(Activity activity){}
        public void onActivitySaveInstanceState(Activity activity,Bundle state){}
        public void onActivityDestroyed(Activity activity){}
    };
    @Override public void onCreate(Bundle args){super.onCreate(args);language=args.getString("language","en");dismissIntro="true".equals(args.getString("dismiss_intro"));cycles=Integer.parseInt(args.getString("cycles","0"));start();}
    private void dismissEmulatorIntro() {
        if(!dismissIntro||game.hasWindowFocus())return;
        if(!android.os.Build.HARDWARE.equals("ranchu")&&!android.os.Build.HARDWARE.equals("goldfish"))
            throw new IllegalStateException("Intro dismissal is limited to the task emulator");
        AccessibilityNodeInfo window=getUiAutomation().getRootInActiveWindow();
        android.util.Log.i("SDL/APP","Pazur emulator intro window: "+(window==null?"null":window.getPackageName()+" intro="+window.findAccessibilityNodeInfosByText("Viewing full screen").size()+" button="+window.findAccessibilityNodeInfosByText("Got it").size()));
        if(window==null||window.getPackageName()==null||
            !("android".contentEquals(window.getPackageName())||"com.android.systemui".contentEquals(window.getPackageName())))return;
        if(window.findAccessibilityNodeInfosByText("Viewing full screen").isEmpty())return;
        java.util.List<AccessibilityNodeInfo> buttons=window.findAccessibilityNodeInfosByText("Got it");
        if(buttons.size()!=1||!buttons.get(0).isClickable()||!buttons.get(0).performAction(AccessibilityNodeInfo.ACTION_CLICK))
            throw new IllegalStateException("Cannot dismiss known emulator fullscreen introduction");
        android.util.Log.i("SDL/APP","Pazur menu test dismissed emulator fullscreen intro using its accessibility node");
        SystemClock.sleep(1200);
    }
    private void focus() {
        if(game==null||game.isFinishing()||!game.hasWindowFocus())throw new IllegalStateException("Game not focused; input refused (instance="+(game==null?"null":System.identityHashCode(game)+", finishing="+game.isFinishing()+", destroyed="+game.isDestroyed())+")");
    }
    private void tap(float x,float y) {
        focus();long now=SystemClock.uptimeMillis();
        float px=(logicalWidth/2-320+x)*width/logicalWidth,py=y*height/480f;
        for(int action:new int[]{MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP}) {
            MotionEvent event=MotionEvent.obtain(now,SystemClock.uptimeMillis(),action,px,py,0);
            event.setSource(InputDevice.SOURCE_TOUCHSCREEN);
            runOnMainSync(()->{focus();game.getWindow().getDecorView().dispatchTouchEvent(event);});event.recycle();
            SystemClock.sleep(60);
        }
        SystemClock.sleep(900);
    }
    private void escape() {
        focus();for(int action:new int[]{KeyEvent.ACTION_DOWN,KeyEvent.ACTION_UP}) {
            KeyEvent event=new KeyEvent(action,KeyEvent.KEYCODE_ESCAPE);
            runOnMainSync(()->{focus();game.getWindow().getDecorView().dispatchKeyEvent(event);});
        }
        SystemClock.sleep(900);
    }
    private void capture(String name) throws IOException {
        focus();Bitmap shot=getUiAutomation().takeScreenshot();
        if(shot==null)throw new IOException("No image");
        try(FileOutputStream out=new FileOutputStream(new File(root,"menu-"+language+"-"+name+".png"))){shot.compress(Bitmap.CompressFormat.PNG,100,out);}
        shot.recycle();
    }
    @Override public void onStart() {
        Bundle result=new Bundle();int code=1;
        SharedPreferences prefs=getTargetContext().getSharedPreferences("interface",Context.MODE_PRIVATE);
        String previous=prefs.getString("language",null);byte[] nativeBefore=null;boolean backedUp=false;
        Application application=(Application)getTargetContext().getApplicationContext();
        try {
            application.registerActivityLifecycleCallbacks(lifecycle);
            if(!language.equals("en")&&!language.equals("pl"))throw new IllegalArgumentException("language");
            root=getTargetContext().getExternalFilesDir(null);File nativeFile=new File(root,"ui-language.txt");
            if(nativeFile.exists())try(InputStream in=new FileInputStream(nativeFile);ByteArrayOutputStream out=new ByteArrayOutputStream()) {
                byte[] b=new byte[1024];int n;while((n=in.read(b))!=-1)out.write(b,0,n);nativeBefore=out.toByteArray();
            }
            backedUp=true;if(!prefs.edit().putString("language",language).commit())throw new IOException("Preference");
            getUiAutomation();ActivityMonitor monitor=addMonitor("pl.pazur.port.GameActivity",null,false);
            getTargetContext().startActivity(new Intent(getTargetContext(),LauncherActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            Activity observed=waitForMonitorWithTimeout(monitor,30000);
            if(game==null)game=observed;
            long deadline=SystemClock.uptimeMillis()+15000;
            while(game!=null&&!game.hasWindowFocus()&&SystemClock.uptimeMillis()<deadline) {dismissEmulatorIntro();SystemClock.sleep(50);}
            focus();SystemClock.sleep(8000);
            dismissEmulatorIntro();focus();
            Bitmap screen=getUiAutomation().takeScreenshot();width=screen.getWidth();height=screen.getHeight();screen.recycle();
            if(width<=height)throw new IOException("Expected landscape");
            logicalWidth=Math.max(640,Math.round(480f*width/height));
            capture("main");
            if(cycles>0) {
                if(cycles>100)throw new IllegalArgumentException("Too many cycles");
                for(int i=0;i<cycles;i++) {
                    tap(185,217);
                    if(i%5==0)capture("stress-single");
                    tap(228,217);tap(290,427);tap(290,392);
                }
            } else {
            tap(200,252);tap(275,392);capture("help-index");tap(335,462);capture("help");
            tap(275,427);
            tap(185,217);capture("single");tap(228,217);capture("levels");
            tap(288,427);tap(276,392);
            tap(248,322);capture("options");tap(270,337);capture("audio");tap(220,268);tap(220,302);
            tap(276,372);tap(276,407);
            tap(248,357);capture("credits");tap(276,427);
            tap(282,427);capture("quit");tap(302,342);capture("returned");
            escape();escape();capture("keyboard-return");
            }
            result.putString("menu","PASS: focused-window navigation completed in "+language+"; page logs and screenshots require verification");code=0;
        }catch(Throwable error){
            result.putString("error",android.util.Log.getStackTraceString(error));
            if(root!=null)try {
                Bitmap evidence=getUiAutomation().takeScreenshot();
                if(evidence!=null)try(FileOutputStream out=new FileOutputStream(new File(root,"menu-"+language+"-focus-failure.png"))){evidence.compress(Bitmap.CompressFormat.PNG,100,out);evidence.recycle();}
            }catch(Throwable ignored){}
        }
        finally {
            application.unregisterActivityLifecycleCallbacks(lifecycle);
            if(previous==null)prefs.edit().remove("language").commit();else prefs.edit().putString("language",previous).commit();
            if(backedUp)try {
                File nativeFile=new File(root,"ui-language.txt");
                if(nativeBefore==null){if(nativeFile.exists()&&!nativeFile.delete())throw new IOException("Native preference cleanup");}
                else try(FileOutputStream out=new FileOutputStream(nativeFile)){out.write(nativeBefore);out.getFD().sync();}
            }catch(IOException error){code=1;result.putString("restore_error",error.toString());}
        }
        finish(code,result);
    }
}
