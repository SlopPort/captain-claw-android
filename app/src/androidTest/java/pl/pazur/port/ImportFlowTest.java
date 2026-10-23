package pl.pazur.port;

import android.app.*;
import android.content.*;
import android.net.Uri;
import android.os.Bundle;
import android.view.*;
import android.widget.*;

/** Runs the production importer with an ordinary content-resolver descriptor.
 * The picker result is injected: this does NOT claim system picker UI QA.
 * Host owns backups, missing-font setup, stream fixtures and final restoration.
 * OpenAI Codex (LLM). No broad-storage grants or shell identity in app code. */
public class ImportFlowTest extends Instrumentation {
    private Bundle args;
    @Override public void onCreate(Bundle value){super.onCreate(value);args=value;start();}
    private View text(View view,String value) {
        if(view instanceof TextView&&((TextView)view).getText().toString().equals(value))return view;
        if(view instanceof ViewGroup)for(int i=0;i<((ViewGroup)view).getChildCount();i++) {
            View found=text(((ViewGroup)view).getChildAt(i),value);if(found!=null)return found;
        }
        return null;
    }
    @Override public void onStart() {
        Bundle result=new Bundle();Activity screen=null;ActivityMonitor game=null;
        try {
            String mode=args.getString("mode");
            if("recover".equals(mode)) {
                synchronized(ImportTransaction.LOCK){ImportTransaction.prepareStartup(getTargetContext().getExternalFilesDir(null));}
                result.putString("import_flow","PASS: recover");finish(0,result);return;
            }
            if(!java.util.Arrays.asList("cancel","invalid","rez","picker-cancel","zip","traversal","bad-config","duplicate","missing","crc").contains(mode))throw new Exception("Unknown mode");
            Intent selected=("cancel".equals(mode)||"picker-cancel".equals(mode))?null:new Intent().setData(Uri.parse(args.getString("uri")));

            // Observe launch intent, blocking native startup so no live engine
            // can write to settings while the host restores the test installation.
            game=addMonitor(GameActivity.class.getName(),new ActivityResult(Activity.RESULT_CANCELED,null),true);
            screen=startActivitySync(new Intent(getTargetContext(),LauncherActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            final Activity activity=screen;View[] choose={null};
            for(int i=0;i<200;i++) {
                runOnMainSync(()->choose[0]=text(activity.getWindow().getDecorView(),activity.getString(R.string.import_choose)));
                if(choose[0]!=null)break;Thread.sleep(50);
            }
            if(choose[0]==null)throw new Exception("Importer screen not ready; host must isolate a missing required file");
            runOnMainSync(()-> {
                choose[0].requestRectangleOnScreen(new android.graphics.Rect(0,0,choose[0].getWidth(),choose[0].getHeight()),true);
                if("picker-cancel".equals(mode)){choose[0].performClick();return;}
                // Inject only the picker result into the production callback.
                // A broad IntentFilter monitor also matches actionless starts
                // on some Androids and can block the launcher itself.
                try {
                    java.lang.reflect.Method callback=LauncherActivity.class.getDeclaredMethod("onActivityResult",int.class,int.class,Intent.class);
                    callback.setAccessible(true);
                    callback.invoke(activity,1,"cancel".equals(mode)?Activity.RESULT_CANCELED:Activity.RESULT_OK,selected);
                } catch(Exception error){throw new RuntimeException(error);}
            });
            if("picker-cancel".equals(mode)) {
                // The only global accessibility operation is Back, guarded by
                // the resolved system picker owning the active window. Never
                // send input to settings, a launcher or another foreground app.
                Intent pick=new Intent(Intent.ACTION_OPEN_DOCUMENT).setType("*/*").addCategory(Intent.CATEGORY_OPENABLE);
                android.content.pm.ResolveInfo info=getTargetContext().getPackageManager().resolveActivity(pick,0);
                if(info==null)throw new Exception("No system document picker");
                String expected=info.activityInfo.packageName;boolean seen=false;
                for(int i=0;i<100;i++) {
                    android.view.accessibility.AccessibilityNodeInfo window=getUiAutomation().getRootInActiveWindow();
                    if(window!=null&&expected.contentEquals(window.getPackageName())){seen=true;break;}
                    Thread.sleep(50);
                }
                if(!seen)throw new Exception("System picker did not own active window");
                if(!getUiAutomation().performGlobalAction(android.accessibilityservice.AccessibilityService.GLOBAL_ACTION_BACK))
                    throw new Exception("Picker Back action rejected");
            }
            long until=android.os.SystemClock.uptimeMillis()+120000;boolean complete=false;
            while(android.os.SystemClock.uptimeMillis()<until) {
                boolean[] state={false};
                runOnMainSync(()-> {
                    View button=text(activity.getWindow().getDecorView(),activity.getString(R.string.import_choose));
                    if("cancel".equals(mode))state[0]=button!=null&&button.isEnabled();
                    else if("picker-cancel".equals(mode)) {
                        android.view.accessibility.AccessibilityNodeInfo window=getUiAutomation().getRootInActiveWindow();
                        state[0]=window!=null&&getTargetContext().getPackageName().contentEquals(window.getPackageName())&&button!=null&&button.isEnabled();
                    }
                    else if(!"rez".equals(mode)&&!"zip".equals(mode))state[0]=button!=null&&button.isEnabled()&&
                        text(activity.getWindow().getDecorView(),activity.getString(R.string.import_failed))!=null;
                });
                if(("rez".equals(mode)||"zip".equals(mode))?game.getHits()>0:state[0]){complete=true;break;}
                Thread.sleep(50);
            }
            if(!complete)throw new Exception("Expected picker callback/import outcome missing");
            result.putString("import_flow","PASS: "+mode+("picker-cancel".equals(mode)?"; real system picker opened and cancelled":"; production Activity and content resolver; picker result injected"));
        } catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));}
        finally {
            if(game!=null)removeMonitor(game);
            if(screen!=null){final Activity activity=screen;runOnMainSync(activity::finish);}
        }
        finish(result.containsKey("error")?1:0,result);
    }
}
