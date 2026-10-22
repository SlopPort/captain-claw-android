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
    private static final String[] REQUIRED = {"CLAW.REZ", "ASSETS.ZIP", "config.xml", "clacon.ttf", "console02.tga"};
    private TextView status;
    private Button importButton;
    private boolean launching;

    private boolean ready() {
        File root = getExternalFilesDir(null);
        if (root == null) return false;
        for (String name : REQUIRED) if (!new File(root, name).isFile()) return false;
        return new File(root, "CLAW.REZ").length() > 168;
    }
    private void play() {
        if(launching)return;
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
        if (ready()) { play(); return; }
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
        Button language=new Button(this);language.setText(R.string.language);
        language.setOnClickListener(v->AppLanguage.choose(this));layout.addView(language);
        setContentView(layout);
    }

    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request != 1 || result != RESULT_OK || data == null) return;
        importButton.setEnabled(false);
        status.setText(R.string.import_busy);
        new Thread(() -> {
            try {
                File root = getExternalFilesDir(null);
                if (root == null) throw new IOException(getString(R.string.storage_unavailable));
                Set<String> allowed = new HashSet<>(Arrays.asList(REQUIRED));
                Set<String> seen = new HashSet<>();
                File stage = new File(root, "import-staging");
                if (!stage.isDirectory() && !stage.mkdirs()) throw new IOException(getString(R.string.import_stage_error));
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
                for (String name : REQUIRED) {
                    if (!new File(stage, name).renameTo(new File(root, name))) throw new IOException(getString(R.string.import_save_error) + name);
                }
                runOnUiThread(this::play);
            } catch (Exception error) {
                runOnUiThread(() -> {
                    status.setText(R.string.import_failed);
                    importButton.setEnabled(true);
                    new AlertDialog.Builder(this).setMessage(error.getMessage()).setPositiveButton("OK", null).show();
                });
            }
        }, "asset-import").start();
    }
}
