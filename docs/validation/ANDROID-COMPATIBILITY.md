# Android compatibility / Zgodność z Androidem

Status recorded by OpenAI Codex (LLM), 2026-10-22. Build support and device testing are different claims.

| Area | Evidence | Remaining work |
| --- | --- | --- |
| Android 10, Huawei P9 Lite, 2 GB RAM | Current campaign/attack-audio regressions on the physical device; user confirmed ZIP import and controller operation in earlier builds | Finish campaign, lifecycle, update/save and sustained performance checks |
| Android 16, Redmi Note 8 | Historical tests of earlier development builds | Retest the final candidate; do not transfer old results to a new APK |
| Android 5 / API 21 minimum | Official default x86_64 emulator: actual engine/menu/held jump/level-one exit to level two passed | No physical API-21 phone, full campaign or file-picker import proof |
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

## Minimum API runtime

The official `system-images;android-21;default;x86_64` image was installed for a separate task-local AVD. It initially had no writable SD card, so data preparation failed; a new local 512 MB card image was supplied only to that emulator. No game storage permission was bypassed on a phone. The user's local data was copied as a fixture, so this is not a real file-picker/import usability test.

Android 5's shell-v1 does not reliably propagate remote command exit status, its toolbox lacks `pidof`, and its `logcat` lacks `--pid`. The first test falsely reported an existing mailbox despite the path being absent. `CampaignSession` now checks an explicit existence marker, falls back to exact-name `ps` parsing, and uses a recent-line stream on old logcat. These are test-harness fixes, not engine changes. `compat-api21-x86_64-r2-menu` and `compat-api21-x86_64-r2-level` passed actual engine library mapping, menu, declared 600 ms jump and real exit/score/level-two loading. User-fixture config/saves were restored.

The image reports Android 5.0.2 / API 21. `compat-api21-x86_64-short-menu` and `compat-api21-x86_64-short-level` also passed the separately declared 100 ms jump and exit/score/next-map trial. Short jump: one takeoff, 62.9 px rise, 113 ms effective hold, 75 ms input-to-takeoff in emulation. Held jump: 151.3 px, 640 ms effective hold, 69 ms takeoff. These timings are not physical-touch latency. This image has no `getconf` utility; no 16 KB page runtime claim is made. The task's API-21 emulator was then shut down on its own ADB port.

Po polsku: obecnie najmocniejsze dowody dotyczą Huawei z Androidem 10. Obsługa ARMv7, minimum Android 5 i wyrównanie 16 KB wymagają również prób uruchomieniowych, zanim opiszemy je jako sprawdzoną zgodność. Nie obiecujemy działania na wszystkich Androidach na podstawie samej kompilacji.

## 0.4.13 interface follow-up

`language-api21-0.4.13-r4.txt` passed actual PL/EN settings/file screens and language selection followed by a newly resumed settings instance on Android 5.0.2. `compat-api21-0.4.13-r4-menu/level` passed native x86_64 library mapping, main menu, a declared 100 ms jump (59.1 px rise, 111 ms effective hold, 74 ms takeoff in emulation), real exit/score and level-two load. The separate x86_64 test APK SHA-256 was `6b160acdd39f12a8ac9af1a84de8aa117c594d57f8377defe695eff5281b03b7`. This preceded the launcher-only active-import language guard; do not treat it as a fresh full-campaign or physical Android-5 test. The task emulator was closed afterward; physical-phone USB internet was untouched.

The first update attempt used a different debug certificate because the emulator's private `ANDROID_USER_HOME` was also set during Gradle signing. It was rejected, so `compat-api21-0.4.13-menu/level` actually ran 0.4.12. Those reports are explicitly invalidated for 0.4.13 while retaining their original outcome metadata. Builds were then separated from the emulator's private home; no game data had to be deleted. Two language-selector test failures inspected/awaited an old screen through API-21 ActivityMonitor behavior; observing a different Activity through Application lifecycle callbacks passed. Failed reports are retained, not relabeled as success. The ABI runtime tool now refuses an installed version different from the checkout/requested version.

## 0.4.14 viewport follow-up

See [the exact APK hashes, reports and limitations](PORT-0.4.14.md). Physical Huawei ARM64 touch, score and Game Over checks passed, as did all fourteen map starts and explicit ARMv7 native/menu/jump/exit coverage. Same-APK dense-scene ARMv7 FPS was lower than ARM64; ARM64 was restored. Android-5 emulator native/menu/100 ms jump/exit passed. Android-15 emulator menu and separately declared exit-only coverage passed, but its 600 ms jump failed under very long frames. The failed jump remains open; exit-only success is not jump coverage. Neither emulator test establishes physical-device or 16 KB page runtime support.
