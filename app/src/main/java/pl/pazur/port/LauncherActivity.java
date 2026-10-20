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
public class LauncherActivity extends Activity {
    private static final String[] REQUIRED = {"CLAW.REZ", "ASSETS.ZIP", "config.xml", "clacon.ttf", "console02.tga"};
    private TextView status;
    private Button importButton;

    private boolean ready() {
        File root = getExternalFilesDir(null);
        if (root == null) return false;
        for (String name : REQUIRED) if (!new File(root, name).isFile()) return false;
        return new File(root, "CLAW.REZ").length() > 168;
    }
    private void play() { startActivity(new Intent(this, GameActivity.class)); finish(); }

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        if (ready()) { play(); return; }
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        int pad = (int)(24 * getResources().getDisplayMetrics().density);
        layout.setPadding(pad, pad, pad, pad);
        status = new TextView(this);
        status.setText("Kapitan Pazur — wersja testowa\n\nWybierz paczkę danych game-data.zip przygotowaną z własnej instalacji gry. APK zawiera silnik, a dane gry importujesz osobno.");
        status.setTextSize(20);
        layout.addView(status);
        importButton = new Button(this);
        importButton.setText("Wybierz dane gry");
        importButton.setOnClickListener(v -> {
            Intent pick = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            pick.setType("*/*");
            pick.addCategory(Intent.CATEGORY_OPENABLE);
            startActivityForResult(pick, 1);
        });
        layout.addView(importButton);
        setContentView(layout);
    }

    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request != 1 || result != RESULT_OK || data == null) return;
        importButton.setEnabled(false);
        status.setText("Importowanie danych…");
        new Thread(() -> {
            try {
                File root = getExternalFilesDir(null);
                if (root == null) throw new IOException("Pamięć aplikacji jest niedostępna.");
                Set<String> allowed = new HashSet<>(Arrays.asList(REQUIRED));
                Set<String> seen = new HashSet<>();
                File stage = new File(root, "import-staging");
                if (!stage.isDirectory() && !stage.mkdirs()) throw new IOException("Nie można przygotować importu.");
                long total = 0;
                try (InputStream input = getContentResolver().openInputStream(data.getData());
                     ZipInputStream zip = new ZipInputStream(input)) {
                    ZipEntry entry;
                    byte[] buffer = new byte[65536];
                    while ((entry = zip.getNextEntry()) != null) {
                        String name = entry.getName();
                        // Exact allowlist also excludes traversal, directories and save replacement.
                        if (!allowed.contains(name) || !seen.add(name)) throw new IOException("Nieprawidłowa zawartość paczki: " + name);
                        try (OutputStream out = new FileOutputStream(new File(stage, name))) {
                            int count;
                            while ((count = zip.read(buffer)) != -1) {
                                total += count;
                                if (total > 1024L * 1024 * 1024) throw new IOException("Paczka przekracza 1 GB.");
                                out.write(buffer, 0, count);
                            }
                        }
                    }
                }
                if (!seen.equals(allowed) || new File(stage, "CLAW.REZ").length() <= 168)
                    throw new IOException("Paczka nie zawiera kompletu danych gry.");
                for (String name : REQUIRED) {
                    if (!new File(stage, name).renameTo(new File(root, name))) throw new IOException("Nie można zapisać: " + name);
                }
                runOnUiThread(this::play);
            } catch (Exception error) {
                runOnUiThread(() -> {
                    status.setText("Nie udało się zaimportować danych.");
                    importButton.setEnabled(true);
                    new AlertDialog.Builder(this).setMessage(error.getMessage()).setPositiveButton("OK", null).show();
                });
            }
        }, "asset-import").start();
    }
}
