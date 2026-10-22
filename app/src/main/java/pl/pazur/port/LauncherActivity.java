package pl.pazur.port;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.io.*;
import java.util.*;
import java.util.zip.*;

/** Imports the user's prepared data without broad storage permissions. */
public class LauncherActivity extends LocalizedActivity {
    private static final String[] REQUIRED = ImportTransaction.REQUIRED;
    private TextView status;
    private Button importButton;
    private Button languageButton;
    private boolean launching;
    private boolean storageChecked;
    private Intent pendingImport;

    private boolean ready() {
        File root = getExternalFilesDir(null);
        if (root == null) return false;
        for (String name : REQUIRED) if (!new File(root, name).isFile()) return false;
        return new File(root, "CLAW.REZ").length() > 168;
    }
    private void play() {
        if(launching || isFinishing() || isDestroyed())return;
        launching=true;
        // Run the small, atomic engine update off the UI thread. Imported REZ,
        // settings and saves remain owned by the user across APK upgrades.
        new Thread(() -> {
            try {
                AppLanguage.writeNative(this);
                EngineSupport.install(this,getExternalFilesDir(null));
                runOnUiThread(() -> {
                    if(isFinishing() || isDestroyed())return;
                    startActivity(new Intent(this, GameActivity.class));finish();
                });
            } catch(IOException error) {
                runOnUiThread(() -> {
                    launching=false;
                    if(isFinishing() || isDestroyed())return;
                    new AlertDialog.Builder(this)
                    .setMessage(getString(R.string.prepare_error) + error.getMessage())
                    .setPositiveButton(R.string.retry,(dialog,which)->play())
                    .setNegativeButton(R.string.close,(dialog,which)->finish()).show();
                });
            }
        },"engine-support").start();
    }

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        if(getIntent().hasExtra("startup_error")) {
            // Do not auto-launch into the same failing native initialization.
            new AlertDialog.Builder(this).setMessage(getString(R.string.prepare_error)+getIntent().getStringExtra("startup_error"))
                .setPositiveButton(R.string.retry,(dialog,which)->{getIntent().removeExtra("startup_error");recreate();})
                .setNeutralButton(R.string.save_tools,(dialog,which)->{startActivity(new Intent(this,FileToolsActivity.class));finish();})
                .setNegativeButton(R.string.close,(dialog,which)->finish()).show();
            return;
        }
        if (getIntent().getBooleanExtra("pin_shortcut", false)) {
            // Let the launcher ask the user where to place it; never edit its database.
            if (android.os.Build.VERSION.SDK_INT >= 26) {
                android.content.pm.ShortcutManager manager = getSystemService(android.content.pm.ShortcutManager.class);
                if (manager != null && manager.isRequestPinShortcutSupported()) {
                    Intent open = new Intent(this, LauncherActivity.class).setAction(Intent.ACTION_MAIN);
                    android.content.pm.ShortcutInfo shortcut = new android.content.pm.ShortcutInfo.Builder(this, "open-claw")
                        .setShortLabel("Kapitan Pazur")
                        .setIcon(android.graphics.drawable.Icon.createWithResource(this, android.R.drawable.ic_media_play))
                        .setIntent(open).build();
                    new Thread(()-> {
                        try {manager.requestPinShortcut(shortcut,null);}
                        finally {runOnUiThread(this::finish);}
                    },"pin-shortcut").start();
                    return;
                } else {
                    android.widget.Toast.makeText(this, R.string.pin_help, android.widget.Toast.LENGTH_LONG).show();
                }
            } else {
                android.widget.Toast.makeText(this, R.string.pin_help, android.widget.Toast.LENGTH_LONG).show();
            }
            finish();
            return;
        }
        // Recovery can copy a large REZ. Keep it off the UI thread and serialize
        // it with imports, including a second launcher instance after recreation.
        TextView preparing=new TextView(this);preparing.setText(R.string.import_recovering);
        setContentView(preparing);
        new Thread(()-> {
            try {
                File root=getExternalFilesDir(null);
                if(root==null)throw new IOException(getString(R.string.storage_unavailable));
                synchronized(ImportTransaction.LOCK) { ImportTransaction.prepareStartup(root); }
                runOnUiThread(()-> {
                    if(isFinishing()||isDestroyed())return;
                    storageChecked=true;
                    // A document-picker result may arrive before this worker
                    // finishes after Activity recreation. Do not lose it or
                    // access buttons that have not been constructed yet.
                    if(pendingImport!=null) {
                        Intent selected=pendingImport;pendingImport=null;
                        showImporter();startImport(selected);
                    } else if(ready())play();else showImporter();
                });
            } catch(IOException error) {
                runOnUiThread(()-> {
                    if(isFinishing()||isDestroyed())return;
                    new AlertDialog.Builder(this).setMessage(getString(R.string.import_recovery_error)+error.getMessage())
                        .setPositiveButton(R.string.retry,(dialog,which)->recreate())
                        .setNegativeButton(R.string.close,(dialog,which)->finish()).show();
                });
            }
        },"import-recovery").start();
    }

    private void showImporter() {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        int pad = (int)(24 * getResources().getDisplayMetrics().density);
        layout.setPadding(pad, pad, pad, pad);
        status = new TextView(this);
        status.setText(R.string.import_intro);
        status.setTextSize(20);
        layout.addView(status);
        importButton = new Button(this);
        importButton.setText(R.string.import_choose);
        importButton.setOnClickListener(v -> {
            Intent pick = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            pick.setType("*/*");
            pick.addCategory(Intent.CATEGORY_OPENABLE);
            startActivityForResult(pick, 1);
        });
        layout.addView(importButton);
        languageButton=new Button(this);languageButton.setText(R.string.language);
        languageButton.setOnClickListener(v->AppLanguage.choose(this));layout.addView(languageButton);
        setContentView(layout);
    }

    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request != 1 || result != RESULT_OK || data == null) return;
        if(!storageChecked) {pendingImport=data;return;}
        startImport(data);
    }

    private void startImport(Intent data) {
        importButton.setEnabled(false);
        // Recreating the launcher during an active import would leave its
        // worker attached to the old screen and allow a second import worker.
        languageButton.setEnabled(false);
        status.setText(R.string.import_busy);
        new Thread(() -> {
            synchronized(ImportTransaction.LOCK) {
            try {
                File root = getExternalFilesDir(null);
                if (root == null) throw new IOException(getString(R.string.storage_unavailable));
                Set<String> allowed = new HashSet<>(Arrays.asList(REQUIRED));
                Set<String> seen = new HashSet<>();
                File stage = ImportTransaction.freshStage(root);
                long total = 0;
                try (BufferedInputStream input = new BufferedInputStream(getContentResolver().openInputStream(data.getData()))) {
                    if (!ImportSupport.isZip(input)) {
                        ImportSupport.copy(input,new File(stage,"CLAW.REZ"),1024L*1024*1024);
                        ImportSupport.validateRez(new File(stage,"CLAW.REZ"));
                        ImportSupport.prepare(this,stage);
                        seen.addAll(allowed);
                    } else try (ZipInputStream zip = new ZipInputStream(input)) {
                    ZipEntry entry;
                    byte[] buffer = new byte[65536];
                    while ((entry = zip.getNextEntry()) != null) {
                        String name = entry.getName();
                        // Exact allowlist also excludes traversal, directories and save replacement.
                        if (!allowed.contains(name) || !seen.add(name)) throw new IOException(getString(R.string.import_content_error) + name);
                        try (OutputStream out = new FileOutputStream(new File(stage, name))) {
                            int count;
                            while ((count = zip.read(buffer)) != -1) {
                                total += count;
                                if (total > 1024L * 1024 * 1024) throw new IOException(getString(R.string.import_size_error));
                                out.write(buffer, 0, count);
                            }
                        }
                    }
                    }
                }
                if (!seen.equals(allowed) || new File(stage, "CLAW.REZ").length() <= 168)
                    throw new IOException(getString(R.string.import_missing_error));
                ImportSupport.validateRez(new File(stage,"CLAW.REZ"));
                ImportTransaction.commit(root,stage);
                runOnUiThread(this::play);
            } catch (Exception error) {
                // Normal I/O failures roll back immediately. Process death takes
                // the same path during the next launcher startup, before ready().
                File root=getExternalFilesDir(null);
                if(root!=null)try {ImportTransaction.prepareStartup(root);}catch(IOException recovery){error.addSuppressed(recovery);}
                runOnUiThread(() -> {
                    if(isFinishing()||isDestroyed())return;
                    status.setText(R.string.import_failed);
                    importButton.setEnabled(true);
                    languageButton.setEnabled(true);
                    new AlertDialog.Builder(this).setMessage(error.getMessage()).setPositiveButton("OK", null).show();
                });
            }
            }
        }, "asset-import").start();
    }
}
