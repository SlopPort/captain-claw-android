package pl.pazur.port;

import android.app.*;
import android.content.*;
import android.net.Uri;
import android.os.Bundle;
import android.view.accessibility.AccessibilityNodeInfo;

/** Real asynchronous provider failures and visible localized dialogs, by Codex.
 * No global input, provider fixture, save import or game-data replacement. */
public class SaveErrorMessagesTest extends Instrumentation {
    @Override public void onCreate(Bundle args){super.onCreate(args);start();}
    private AccessibilityNodeInfo findText(AccessibilityNodeInfo node,String text) {
        if(node==null)return null;
        if(node.getText()!=null&&text.contentEquals(node.getText()))return node;
        for(int i=0;i<node.getChildCount();i++) {
            AccessibilityNodeInfo found=findText(node.getChild(i),text);
            if(found!=null)return found;
        }
        return null;
    }
    @Override public void onStart() {
        Bundle result=new Bundle();Activity current=null;
        Context context=getTargetContext();
        SharedPreferences prefs=context.getSharedPreferences("interface",Context.MODE_PRIVATE);
        String original=prefs.getString("language",null);
        try {
            // Connect before launching; inspect/click only this app's own window.
            getUiAutomation();
            int checked=0;
            for(String code:new String[]{"en","pl"}) {
                if(!prefs.edit().putString("language",code).commit())throw new Exception("Cannot select fixture locale");
                for(int request:new int[]{1,2}) {
                    current=startActivitySync(new Intent(context,FileToolsActivity.class)
                        .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK|Intent.FLAG_ACTIVITY_CLEAR_TOP));
                    final FileToolsActivity screen=(FileToolsActivity)current;
                    String expected=screen.getString(request==1?R.string.backup_export_failed:R.string.progress_import_failed);
                    // Unsupported path fails in the test provider before any file opens.
                    Uri invalid=Uri.parse("content://pl.pazur.port.test.importstream/not-an-authorized-fixture");
                    runOnMainSync(()->screen.onActivityResult(request,Activity.RESULT_OK,new Intent().setData(invalid)));
                    boolean found=false;
                    for(int attempt=0;attempt<100;attempt++) {
                        AccessibilityNodeInfo root=getUiAutomation().getRootInActiveWindow();
                        if(root!=null&&root.getPackageName()!=null&&context.getPackageName().contentEquals(root.getPackageName())&&findText(root,expected)!=null) {
                            AccessibilityNodeInfo ok=findText(root,"OK");
                            if(ok==null||!ok.performAction(AccessibilityNodeInfo.ACTION_CLICK))throw new Exception("Own error dialog cannot be dismissed");
                            found=true;break;
                        }
                        Thread.sleep(50);
                    }
                    if(!found)throw new Exception("Localized visible error missing: "+code+" request="+request);
                    checked++;runOnMainSync(screen::finish);waitForIdleSync();current=null;
                }
            }
            result.putString("save_errors","PASS: four actual provider failures produced dismissible localized dialogs");
            result.putInt("checked",checked);
        } catch(Throwable error) {result.putString("error",android.util.Log.getStackTraceString(error));}
        finally {
            if(current!=null){final Activity old=current;runOnMainSync(old::finish);waitForIdleSync();}
            SharedPreferences.Editor edit=prefs.edit();
            if(original==null)edit.remove("language");else edit.putString("language",original);
            if(!edit.commit())result.putString("error","Could not restore original language preference");
        }
        finish(result.containsKey("error")?1:0,result);
    }
}
