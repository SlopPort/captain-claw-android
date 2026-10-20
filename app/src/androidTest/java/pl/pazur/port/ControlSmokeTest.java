package pl.pazur.port;

import android.app.Instrumentation;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.InputDevice;
import java.io.File;
import java.io.FileOutputStream;

/** Device smoke test: real multi-pointer events delivered to the game surface. */
public class ControlSmokeTest extends Instrumentation {
    private long down;
    private int width, height;
    private float logicalWidth;

    @Override public void onCreate(Bundle arguments) { super.onCreate(arguments); start(); }

    private void touch(int action, int[] ids, float[][] points) {
        MotionEvent.PointerProperties[] properties = new MotionEvent.PointerProperties[ids.length];
        MotionEvent.PointerCoords[] coords = new MotionEvent.PointerCoords[ids.length];
        float scale = Math.min(width / logicalWidth, height / 480f);
        float offsetX = (width - logicalWidth * scale) / 2;
        float offsetY = (height - 480 * scale) / 2;
        for (int i = 0; i < ids.length; i++) {
            properties[i] = new MotionEvent.PointerProperties();
            properties[i].id = ids[i];
            properties[i].toolType = MotionEvent.TOOL_TYPE_FINGER;
            coords[i] = new MotionEvent.PointerCoords();
            coords[i].x = offsetX + points[i][0] * scale;
            coords[i].y = offsetY + points[i][1] * scale;
            coords[i].pressure = 1;
            coords[i].size = 0.1f;
        }
        MotionEvent event = MotionEvent.obtain(down, SystemClock.uptimeMillis(), action,
            ids.length, properties, coords, 0, 0, 1, 1, 0, 0, InputDevice.SOURCE_TOUCHSCREEN, 0);
        sendPointerSync(event);
        event.recycle();
    }

    private void screenshot(String name) throws Exception {
        Bitmap shot = getUiAutomation().takeScreenshot();
        if (shot == null) throw new IllegalStateException("No screenshot available");
        try (FileOutputStream out = new FileOutputStream(new File(getTargetContext().getExternalFilesDir(null), name))) {
            shot.compress(Bitmap.CompressFormat.PNG, 100, out);
        }
        shot.recycle();
    }

    @Override public void onStart() {
        Bundle result = new Bundle();
        try {
            Intent start = new Intent().setClassName(getTargetContext(), "pl.pazur.port.LauncherActivity")
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getTargetContext().startActivity(start);
            SystemClock.sleep(2500);
            for (int i = 0; i < 4; i++) {
                sendKeyDownUpSync(KeyEvent.KEYCODE_ENTER);
                SystemClock.sleep(400);
            }
            SystemClock.sleep(7000);
            Bitmap shot = getUiAutomation().takeScreenshot();
            width = shot.getWidth(); height = shot.getHeight(); shot.recycle();
            if (width <= height) throw new IllegalStateException("Game did not enter landscape");
            logicalWidth = Math.max(640, Math.round(480f * width / height));
            float jumpX = logicalWidth - 56;
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{147,394}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_POINTER_DOWN | (1 << MotionEvent.ACTION_POINTER_INDEX_SHIFT),
                new int[]{11,29}, new float[][]{{147,394},{jumpX,438}});
            SystemClock.sleep(250);
            screenshot("control-multitouch.png");
            touch(MotionEvent.ACTION_POINTER_UP, new int[]{11,29}, new float[][]{{147,394},{jumpX,438}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_UP, new int[]{29}, new float[][]{{jumpX,438}});
            SystemClock.sleep(700);
            screenshot("control-release.png");
            // The stick owns its finger even outside its base; returning to center stops motion.
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{100,394}});
            touch(MotionEvent.ACTION_MOVE, new int[]{11}, new float[][]{{140,354}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_MOVE, new int[]{11}, new float[][]{{100,320}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_MOVE, new int[]{11}, new float[][]{{100,468}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_MOVE, new int[]{11}, new float[][]{{8,394}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_MOVE, new int[]{11}, new float[][]{{105,395}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_UP, new int[]{11}, new float[][]{{105,395}});
            // A second thumb in the base must not steal ownership or keep movement stuck.
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{147,394}});
            touch(MotionEvent.ACTION_POINTER_DOWN | (1 << MotionEvent.ACTION_POINTER_INDEX_SHIFT),
                new int[]{11,29}, new float[][]{{147,394},{53,394}});
            touch(MotionEvent.ACTION_POINTER_UP, new int[]{11,29}, new float[][]{{147,394},{53,394}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_UP, new int[]{29}, new float[][]{{53,394}});
            // Shared action buttons retain their key until the last finger leaves, including cancel.
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{jumpX,438}});
            touch(MotionEvent.ACTION_POINTER_DOWN | (1 << MotionEvent.ACTION_POINTER_INDEX_SHIFT),
                new int[]{11,29}, new float[][]{{jumpX,438},{jumpX,438}});
            touch(MotionEvent.ACTION_POINTER_UP, new int[]{11,29}, new float[][]{{jumpX,438},{jumpX,438}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_CANCEL, new int[]{29}, new float[][]{{jumpX,438}});
            SystemClock.sleep(150);
            screenshot("control-joystick.png");
            // Pause/resume must preserve centered menu hit targets and release all movement.
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{45,96}});
            touch(MotionEvent.ACTION_UP, new int[]{11}, new float[][]{{45,96}});
            SystemClock.sleep(400);
            screenshot("control-pause.png");
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{logicalWidth/2,160}});
            touch(MotionEvent.ACTION_UP, new int[]{11}, new float[][]{{logicalWidth/2,160}});
            SystemClock.sleep(400);
            screenshot("control-resume.png");
            // Verify that the right-side action buttons use the expanded viewport too.
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{logicalWidth-148,438}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_UP, new int[]{11}, new float[][]{{logicalWidth-148,438}});
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{logicalWidth-56,360}});
            SystemClock.sleep(120);
            touch(MotionEvent.ACTION_UP, new int[]{11}, new float[][]{{logicalWidth-56,360}});
            SystemClock.sleep(120);
            // Backgrounding the activity must release the stick, even without a finger-up.
            down = SystemClock.uptimeMillis();
            touch(MotionEvent.ACTION_DOWN, new int[]{11}, new float[][]{{147,394}});
            SystemClock.sleep(120);
            sendKeyDownUpSync(KeyEvent.KEYCODE_HOME);
            SystemClock.sleep(500);
            getTargetContext().startActivity(start);
            SystemClock.sleep(1500);
            screenshot("control-focus-resume.png");
            result.putString("stream", "Multi-pointer input sequence completed; inspect native control log and screenshots.\n");
            finish(0, result);
        } catch (Exception failure) {
            result.putString("stream", failure.toString());
            finish(1, result);
        }
    }
}
