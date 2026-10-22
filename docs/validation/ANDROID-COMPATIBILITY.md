# Android compatibility / Zgodność z Androidem

Status recorded by OpenAI Codex (LLM), 2026-10-22. Build support and device testing are different claims.

| Area | Evidence | Remaining work |
| --- | --- | --- |
| Android 10, Huawei P9 Lite, 2 GB RAM | Current campaign/attack-audio regressions on the physical device; user confirmed ZIP import and controller operation in earlier builds | Finish campaign, lifecycle, update/save and sustained performance checks |
| Android 16, Redmi Note 8 | Historical tests of earlier development builds | Retest the final candidate; do not transfer old results to a new APK |
| Android 5.0 / API 21 minimum | Project minSdk 21; lint/build checks | No current physical/runtime proof for the minimum API |
| ARM64 and ARMv7 | Both packaged; 0.4.12-dev actually ran as ARMv7 on Huawei Android 10, with process library mappings checked | Broader 32-bit gameplay/device coverage remains open |
| 16 KB memory pages | `tools/verify_apk.py` confirms 16 KB ELF load alignment for all packaged ARM64 libraries | Check ZIP alignment/signature and run on a 16 KB runtime; static ELF checks alone are insufficient |
| Android 15 / API 35 emulator, x86_64 | Separate test APK built; actual native process, menu, held jump and level-one exit to level two passed | Short-tap test failed under severe emulator stalls; lifecycle/import UI and wider gameplay remain open |
| Other vendors/controllers | Android/SDL input paths and configurable mappings | More physical devices and controller modes remain untested |

Release compatibility must be tied to the tested APK, device/API, ABI and scenario. A successful level load is not a completed playthrough, and minSdk is not evidence that every Android version works. The API 36.1 image directory observed during preparation was empty; no Android 16 emulator result is claimed.

Use a workspace-local emulator configuration and explicit device selection before running an emulator alongside the phone. The physical phone supplies USB internet: do not alter its USB mode, tethering, network or Bluetooth during this work.

`compat-armv7-0.4.12-r2-menu` and `compat-armv7-0.4.12-r2-level` passed: primary ABI `armeabi-v7a`, actual engine mapped from `/lib/arm/`, main-menu initialization, ordinary level-one jump and real exit/score/level-two loading. Original files were restored and the same APK was reinstalled with ARM64 afterward. The earlier `compat-armv7-0.4.12-level` fixture waited two seconds for a measurement emitted after 2.2 seconds, so it failed with an empty trace; the script now waits for the measurement marker. This was not an engine crash or evidence of broken jumping.

API 35 tests use the installed Google Play x86_64 image, headless software rendering and a separate emulator-only APK. Data files were supplied locally as a fixture; this does not validate the system file-picker import workflow. `compat-api35-x86_64-menu` passed. The first level trial failed its 100 ms jump check (zero rise/jumps) during frames of hundreds of milliseconds and occasional stalls exceeding one second. No crash was observed, but an engine contact warning was logged. Do not relabel this as a passing short-tap test or assume all problems are solely the emulator.

`compat-api35-x86_64-held-jump-menu` and `compat-api35-x86_64-held-jump-level` passed using a separately declared 600 ms held jump: native x86_64 mapping, menu, jump, actual exit pickup, score confirmation and level two. The original emulator config/saves were restored after both trials. No phone USB, tethering or Bluetooth settings were changed. Emulator timing is not a physical-device FPS measurement. The inherited handling of large update intervals remains an audit item; simulation timing was not changed to force this trial to pass.

The emulator reports Android 15, SDK 35 and 4096-byte memory pages. The held jump measured 151.3 pixels, one jump, 618 ms effective hold and 222 ms input-to-takeoff under emulation. This is expressly not a 16 KB runtime test. After the tests the task's emulator was shut down using its own ADB emulator port; the phone remained connected. The x86_64 test APK remains in ignored reports, separate from the ARM distribution.

Po polsku: obecnie najmocniejsze dowody dotyczą Huawei z Androidem 10. Obsługa ARMv7, minimum Android 5 i wyrównanie 16 KB wymagają również prób uruchomieniowych, zanim opiszemy je jako sprawdzoną zgodność. Nie obiecujemy działania na wszystkich Androidach na podstawie samej kompilacji.
