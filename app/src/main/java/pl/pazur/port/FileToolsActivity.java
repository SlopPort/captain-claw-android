package pl.pazur.port;

import android.app.*;
import android.content.Intent;
import android.os.Bundle;
import android.widget.*;
import java.io.*;

/** Android adaptation of Claw Web's save-management workflow, GPLv3.
 * Import is staged until the next engine creation so live checkpoint writes
 * cannot silently undo the imported progress. Existing saves get a backup. */
public class FileToolsActivity extends Activity {
    private boolean english;
    private String tr(String pl,String en){return english?en:pl;}
    private File root(){return getExternalFilesDir(null);}
    private void message(String text){new AlertDialog.Builder(this).setMessage(text).setPositiveButton("OK",null).show();}
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);english=!getResources().getConfiguration().locale.getLanguage().equals("pl");
        LinearLayout layout=new LinearLayout(this);layout.setOrientation(LinearLayout.VERTICAL);layout.setPadding(24,24,24,24);
        TextView title=new TextView(this);title.setText(tr("Zapisy i wibracje","Saves and vibration"));title.setTextSize(22);layout.addView(title);
        TextView credit=new TextView(this);credit.setText("Inspired by Claw Web — Arthur Boss and contributors (GPLv3). Android adaptation: OpenAI Codex / LLM.");layout.addView(credit);
        Button export=new Button(this);export.setText(tr("Zapisz kopię postępu do pliku","Export progress to file"));
        export.setOnClickListener(v->{Intent pick=new Intent(Intent.ACTION_CREATE_DOCUMENT).setType("text/xml").addCategory(Intent.CATEGORY_OPENABLE).putExtra(Intent.EXTRA_TITLE,"pazur-saves.xml");startActivityForResult(pick,1);});layout.addView(export);
        Button load=new Button(this);load.setText(tr("Wczytaj kopię postępu","Import progress"));
        load.setOnClickListener(v->new AlertDialog.Builder(this).setMessage(tr("Import zastąpi postęp przy następnym uruchomieniu gry. Dotychczasowy zapis pozostanie jako kopia. To format XML naszego portu, nie zapis Windows ani JSON Claw Web.","Import replaces progress on the next game start. The previous save is backed up. Use this port's XML, not Windows saves or Claw Web JSON."))
            .setNegativeButton(tr("Anuluj","Cancel"),null).setPositiveButton(tr("Wybierz plik","Choose file"),(d,w)->startActivityForResult(new Intent(Intent.ACTION_OPEN_DOCUMENT).setType("*/*").addCategory(Intent.CATEGORY_OPENABLE),2)).show());layout.addView(load);
        CheckBox haptics=new CheckBox(this);haptics.setText(tr("Wibracje (opcjonalne)","Vibration (optional)"));haptics.setChecked(new File(root(),"haptics-enabled").isFile());
        haptics.setOnCheckedChangeListener((button,on)->{try {File file=new File(root(),"haptics-enabled");if(on){try(FileOutputStream out=new FileOutputStream(file)){out.write(1);}}else if(file.exists()&&!file.delete())throw new IOException("Cannot change setting");}catch(IOException e){message(e.getMessage());}});layout.addView(haptics);
        Button done=new Button(this);done.setText(tr("Wróć","Back"));done.setOnClickListener(v->finish());layout.addView(done);setContentView(layout);
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
                runOnUiThread(()->message(request==1?tr("Kopia zapisana.","Backup exported."):tr("Import przygotowany. Zakończ grę z jej menu i uruchom ponownie, aby go zastosować.","Import prepared. Quit from the game menu and launch again to apply it.")));
            }catch(Exception e){runOnUiThread(()->message(tr("Nie zmieniono postępu: ","Progress unchanged: ")+e.getMessage()));}
        },"save-files").start();
    }
}
