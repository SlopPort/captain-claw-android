package pl.pazur.port;

import android.app.*;
import android.content.*;
import android.net.Uri;
import android.os.Bundle;
import android.view.*;
import android.widget.*;

/** Runs the production importer with an ordinary content-resolver descriptor.
 * Default stream cases inject the picker result. picker-cancel and picker-rez
 * exercise real system UI; picker-rez uses a test-only initial Downloads URI.
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
    private boolean clickExact(android.view.accessibility.AccessibilityNodeInfo window,String name) {
        for(android.view.accessibility.AccessibilityNodeInfo node:window.findAccessibilityNodeInfosByText(name)) {
            if(!name.equals(String.valueOf(node.getText()))&&!name.equals(String.valueOf(node.getContentDescription())))continue;
            android.view.accessibility.AccessibilityNodeInfo exact=node;
            // Older DocumentsUI wraps the title in multiple card/nameplate
            // containers; the actual clickable item can be six parents away.
            for(int depth=0;node!=null&&depth<12;depth++,node=node.getParent()) {
                if(node.isClickable()&&node.performAction(android.view.accessibility.AccessibilityNodeInfo.ACTION_CLICK))return true;
            }
            // Some Android10 document rows handle touch through the RecyclerView
            // and expose no working accessibility click. Tap only the verified,
            // visible exact title in this already-verified picker window.
            android.graphics.Rect bounds=new android.graphics.Rect();exact.getBoundsInScreen(bounds);
            if(exact.isVisibleToUser()&&!bounds.isEmpty()) {
                long now=android.os.SystemClock.uptimeMillis();
                android.view.MotionEvent down=android.view.MotionEvent.obtain(now,now,android.view.MotionEvent.ACTION_DOWN,bounds.exactCenterX(),bounds.exactCenterY(),0);
                android.view.MotionEvent up=android.view.MotionEvent.obtain(now,now+30,android.view.MotionEvent.ACTION_UP,bounds.exactCenterX(),bounds.exactCenterY(),0);
                down.setSource(android.view.InputDevice.SOURCE_TOUCHSCREEN);up.setSource(android.view.InputDevice.SOURCE_TOUCHSCREEN);
                try{if(getUiAutomation().injectInputEvent(down,true)&&getUiAutomation().injectInputEvent(up,true))return true;}
                finally{down.recycle();up.recycle();}
            }
        }
        return false;
    }
    private boolean scrollForward(android.view.accessibility.AccessibilityNodeInfo node,int depth) {
        if(node==null||depth>30)return false;
        // Target the vertical document list, not the horizontal filter chips
        // or nested toolbar ScrollViews. A true action return alone is not
        // evidence that the requested file has become visible.
        if(node.isScrollable()&&String.valueOf(node.getViewIdResourceName()).endsWith(":id/dir_list")) {
            if(android.os.Build.VERSION.SDK_INT>=23&&node.performAction(android.view.accessibility.AccessibilityNodeInfo.AccessibilityAction.ACTION_SCROLL_DOWN.getId()))return true;
            if(node.performAction(android.view.accessibility.AccessibilityNodeInfo.ACTION_SCROLL_FORWARD))return true;
        }
        for(int i=0;i<Math.min(node.getChildCount(),60);i++)if(scrollForward(node.getChild(i),depth+1))return true;
        return false;
    }
    private String describe(android.view.accessibility.AccessibilityNodeInfo node,int depth) {
        if(node==null||depth>30)return "";
        StringBuilder out=new StringBuilder();
        out.append(node.getClassName()).append(" text=").append(node.getText()).append(" desc=").append(node.getContentDescription()).append(" id=").append(node.getViewIdResourceName()).append("\n");
        for(int i=0;i<Math.min(node.getChildCount(),80);i++)out.append(describe(node.getChild(i),depth+1));
        return out.toString();
    }
    @Override public void onStart() {
        Bundle result=new Bundle();Activity screen=null;ActivityMonitor game=null;String[] pickerPackage={null};
        try {
            String mode=args.getString("mode");
            if("recover".equals(mode)) {
                synchronized(ImportTransaction.LOCK){ImportTransaction.prepareStartup(getTargetContext().getExternalFilesDir(null));}
                result.putString("import_flow","PASS: recover");finish(0,result);return;
            }
            if(!java.util.Arrays.asList("cancel","invalid","rez","picker-cancel","zip","traversal","bad-config","duplicate","missing","crc","picker-rez").contains(mode))throw new Exception("Unknown mode");
            Intent selected=("cancel".equals(mode)||"picker-cancel".equals(mode)||"picker-rez".equals(mode))?null:new Intent().setData(Uri.parse(args.getString("uri")));

            // Observe launch intent, blocking native startup so no live engine
            // can write to settings while the host restores the test installation.
            game=addMonitor(GameActivity.class.getName(),new ActivityResult(Activity.RESULT_CANCELED,null),true);
            screen=startActivitySync(new Intent(getTargetContext(),LauncherActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK|Intent.FLAG_ACTIVITY_CLEAR_TOP));
            final Activity activity=screen;View[] choose={null};
            for(int i=0;i<200;i++) {
                runOnMainSync(()->choose[0]=text(activity.getWindow().getDecorView(),activity.getString(R.string.import_choose)));
                if(choose[0]!=null)break;Thread.sleep(50);
            }
            if(choose[0]==null)throw new Exception("Importer screen not ready; host must isolate a missing required file");
            runOnMainSync(()-> {
                choose[0].requestRectangleOnScreen(new android.graphics.Rect(0,0,choose[0].getWidth(),choose[0].getHeight()),true);
                if("picker-cancel".equals(mode)){choose[0].performClick();return;}
                if("picker-rez".equals(mode)) {
                    if(android.os.Build.VERSION.SDK_INT<26)throw new IllegalStateException("Picker fixture requires API26+");
                    Intent pick=new Intent(Intent.ACTION_OPEN_DOCUMENT).setType("*/*").addCategory(Intent.CATEGORY_OPENABLE);
                    // Test-only initial folder. Production choose-button launch
                    // is covered separately; callback/URI grant are real here.
                    pick.putExtra(android.provider.DocumentsContract.EXTRA_INITIAL_URI,
                        android.provider.DocumentsContract.buildDocumentUri("com.android.externalstorage.documents",args.getString("pick_dir")));
                    activity.startActivityForResult(pick,1);return;
                }
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
                String expected=info.activityInfo.packageName;pickerPackage[0]=expected;boolean seen=false;
                for(int i=0;i<100;i++) {
                    android.view.accessibility.AccessibilityNodeInfo window=getUiAutomation().getRootInActiveWindow();
                    if(window!=null&&expected.contentEquals(window.getPackageName())){seen=true;break;}
                    Thread.sleep(50);
                }
                if(!seen)throw new Exception("System picker did not own active window");
                if(!getUiAutomation().performGlobalAction(android.accessibilityservice.AccessibilityService.GLOBAL_ACTION_BACK))
                    throw new Exception("Picker Back action rejected");
            }
            if("picker-rez".equals(mode)) {
                Intent pick=new Intent(Intent.ACTION_OPEN_DOCUMENT).setType("*/*").addCategory(Intent.CATEGORY_OPENABLE);
                android.content.pm.ResolveInfo info=getTargetContext().getPackageManager().resolveActivity(pick,0);
                if(info==null)throw new Exception("No document picker");
                String expected=info.activityInfo.packageName;pickerPackage[0]=expected;boolean clicked=false;
                boolean entered=false;long searchUntil=android.os.SystemClock.uptimeMillis()+30000;
                while(!clicked&&android.os.SystemClock.uptimeMillis()<searchUntil) {
                    android.view.accessibility.AccessibilityNodeInfo window=getUiAutomation().getRootInActiveWindow();
                    if(window!=null&&expected.contentEquals(window.getPackageName())) {
                        clicked=clickExact(window,args.getString("pick_name"));
                        if(!clicked) {
                            // Breadcrumbs also say Download; clicking them opens
                            // a location popup rather than entering a directory.
                            for(android.view.accessibility.AccessibilityNodeInfo list:window.findAccessibilityNodeInfosByViewId(expected+":id/dir_list")) {
                                if(!entered&&(clickExact(list,"Download")||clickExact(list,"Downloads")||clickExact(list,"Pobrane")))entered=true;
                                else scrollForward(list,0);
                            }
                        }
                    }
                    if(!clicked)Thread.sleep(200);
                }
                if(!clicked){result.putString("picker_tree",describe(getUiAutomation().getRootInActiveWindow(),0));throw new Exception("Owned REZ fixture not found in real picker");}
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
                    else if(!"rez".equals(mode)&&!"zip".equals(mode)&&!"picker-rez".equals(mode))state[0]=button!=null&&button.isEnabled()&&
                        text(activity.getWindow().getDecorView(),activity.getString(R.string.import_failed))!=null;
                });
                if(("rez".equals(mode)||"zip".equals(mode)||"picker-rez".equals(mode))?game.getHits()>0:state[0]){complete=true;break;}
                Thread.sleep(50);
            }
            if(!complete){result.putString("picker_tree",describe(getUiAutomation().getRootInActiveWindow(),0));throw new Exception("Expected picker callback/import outcome missing");}
            result.putString("import_flow","PASS: "+mode+("picker-cancel".equals(mode)?"; real system picker opened and cancelled":("picker-rez".equals(mode)?"; full REZ selected in real system picker":"; production Activity and content resolver; picker result injected")));
        } catch(Throwable error){result.putString("error",android.util.Log.getStackTraceString(error));}
        finally {
            if(pickerPackage[0]!=null) {
                for(int attempt=0;attempt<8;attempt++) {
                    android.view.accessibility.AccessibilityNodeInfo window=getUiAutomation().getRootInActiveWindow();
                    if(window==null||!pickerPackage[0].contentEquals(window.getPackageName()))break;
                    getUiAutomation().performGlobalAction(android.accessibilityservice.AccessibilityService.GLOBAL_ACTION_BACK);
                    try{Thread.sleep(100);}catch(InterruptedException ignored){break;}
                }
            }
            if(game!=null)removeMonitor(game);
            if(screen!=null){final Activity activity=screen;runOnMainSync(activity::finish);}
        }
        finish(result.containsKey("error")?1:0,result);
    }
}
