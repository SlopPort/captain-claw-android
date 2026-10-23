package pl.pazur.port;

import android.app.*;
import android.content.Intent;
import android.os.Bundle;
import android.widget.*;
import java.io.*;

/** Android adaptation of Claw Web's save-management workflow, GPLv3.
 * Import is staged until the next engine creation so live checkpoint writes
 * cannot silently undo the imported progress. Existing saves get a backup. */
public class FileToolsActivity extends LocalizedActivity {
    private File root(){return getExternalFilesDir(null);}
    private void message(String text){new AlertDialog.Builder(this).setMessage(text).setPositiveButton("OK",null).show();}
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout layout=new LinearLayout(this);layout.setOrientation(LinearLayout.VERTICAL);layout.setPadding(24,24,24,24);
        TextView title=new TextView(this);title.setText(getString(R.string.saves_vibration));title.setTextSize(22);layout.addView(title);
        TextView credit=new TextView(this);credit.setText(R.string.save_tools_credit);layout.addView(credit);
        Button export=new Button(this);export.setText(getString(R.string.export_progress));
        export.setOnClickListener(v->{Intent pick=new Intent(Intent.ACTION_CREATE_DOCUMENT).setType("text/xml").addCategory(Intent.CATEGORY_OPENABLE).putExtra(Intent.EXTRA_TITLE,"pazur-saves.xml");startActivityForResult(pick,1);});layout.addView(export);
        Button load=new Button(this);load.setText(getString(R.string.import_progress));
        load.setOnClickListener(v->new AlertDialog.Builder(this).setMessage(getString(R.string.import_progress_hint))
            .setNegativeButton(getString(R.string.import_cancel),null).setPositiveButton(getString(R.string.choose_file),(d,w)->startActivityForResult(new Intent(Intent.ACTION_OPEN_DOCUMENT).setType("*/*").addCategory(Intent.CATEGORY_OPENABLE),2)).show());layout.addView(load);
        CheckBox haptics=new CheckBox(this);haptics.setText(getString(R.string.vibration_optional));haptics.setChecked(new File(root(),"haptics-enabled").isFile());
        haptics.setOnCheckedChangeListener((button,on)->{try {File file=new File(root(),"haptics-enabled");if(on){try(FileOutputStream out=new FileOutputStream(file)){out.write(1);}}else if(file.exists()&&!file.delete())throw new IOException("Cannot change setting");}catch(IOException e){message(e.getMessage());}});layout.addView(haptics);
        Button done=new Button(this);done.setText(getString(R.string.back));done.setOnClickListener(v->finish());layout.addView(done);
        // Large system fonts can put the footer below a small display. Keep
        // save actions and Back reachable without changing the system font.
        ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);
        scroll.addView(layout);setContentView(scroll);
    }
    @Override protected void onActivityResult(int request,int result,Intent data) {
        super.onActivityResult(request,result,data);if(result!=RESULT_OK||data==null)return;
        new Thread(()->{
            try {
                if(request==1) {
                    byte[] bytes;try(InputStream in=new FileInputStream(new File(root(),"SAVES.XML"))){bytes=SaveFiles.validate(in);}
                    try(OutputStream out=getContentResolver().openOutputStream(data.getData(),"wt")){out.write(bytes);}
                } else if(request==2) {
                    byte[] bytes;try(InputStream in=getContentResolver().openInputStream(data.getData())){bytes=SaveFiles.validate(in);}
                    SaveFiles.writeAtomic(root(),"SAVES.pending.xml",bytes);
                } else return;
                runOnUiThread(()->message(request==1?getString(R.string.backup_exported):getString(R.string.progress_import_prepared)));
            }catch(Exception e){runOnUiThread(()->message(getString(R.string.progress_error)+e.getMessage()));}
        },"save-files").start();
    }
}
