# Testing

Run device scenarios one at a time, on a phone explicitly allocated to the task. They need an idle game and must not run alongside manual play. Set a process-local `ANDROID_SERIAL`; do not restart the shared ADB server or change a phone's USB internet connection. See [current allocation](HANDOFF.md).

Most owned scenarios temporarily change configuration/progress and restore them in a final cleanup block. Check restoration after failure. Read each script's scope before running it; do not assume every historical helper follows the latest input method. FPS samples cover active simulation only. Component profiling adds frame cost and is not an FPS benchmark.

## Input and lifecycle

Build `:app:assembleDebugAndroidTest`, install the game and its test APK, then run `python tools/jump_touch_smoke.py`. This measures jump height and delay for 10/100/250/700/1800 ms touches and finger movement; it also checks movement plus jump, action buttons, pause and focus loss. `ANDROID_SERIAL` selects the device. `--size` tests another aspect ratio and restores the prior screen size.

`tools/audio_options_smoke.py` checks saving on backgrounding, loading after restart and preservation of unrelated XML values/attributes. It restores configuration and progress.

## Terrain and combat

- `python tools/ladder_smoke.py --expect-fixed --bottom --edges` checks an isolated ladder's top/bottom, re-entry and both platform sides. Run `--first-map-ladder` separately for the actual first ladder of level 1. Additional edge/seam modes are described in the script's help and versioned reports.
- `tools/combat_device_smoke.py --mode regression` checks twelve projectile position/direction/height combinations and one repeated contact. Its foreground checks accept Android 10's activity format while still requiring the game to be in front.
- `tools/combat_matrix.py` places ordinary enemies on their source maps. `tools/combat_projectile_regression.py` requires actual projectile contact from both sides of the hero.
- `python tools/omar_app_smoke.py` performs a controlled encounter/finale through app-local input. It uses protection, powers and teleports; this is not a natural playthrough. Historical boss options in `level_boot_smoke.py` are not the current test method.

Controlled scenarios isolate geometry and attack timing. Protection or disabled target attacks must be explicit in results. Passing does not establish exact Windows balance or every natural encounter. Natural campaign testing belongs to the human; technical fixture commands are never progression evidence.

## Import and progress

`python tools/direct_rez_runtime_smoke.py` checks a complete REZ with APK support files, preserving and restoring phone data. Do not use a CrazyHook installation's 168-byte placeholder REZ.

`PortFeaturesTest` exercises the actual import/save classes in an isolated directory. Build the test APK with `-PtestRunner=pl.pazur.port.PortFeaturesTest`, install it, then run the following with the authorized device selected:

```sh
adb shell am instrument -w pl.pazur.port.test/pl.pazur.port.PortFeaturesTest
```

Before touch tests, rebuild the test APK with the default runner. Class tests and direct runtime import do not prove that a novice can complete every Android file-picker/provider workflow.

## Builds and map starts

`python tools/check_patches.py` applies both patches to clean copies of changed files from the pinned dependencies and compares them with working sources. It does not reset upstream checkouts.

`tools/level_boot_smoke.py --levels 1 13 --frequency 22050 --effects-on` checks loading, audio and process survival. `--combat-audit` reads initial enemy HP/bodies and requires a generated inventory. A map start is not a completed level. Historical boss options and the older `ControlSmokeTest` are not the current UI test.

## Performance measurements

`tools/render_batch_smoke.py --levels 8 9 13 --hold-seconds 35` compares the same APK with SDL batching off/on/off. It requires the 0.4.9 feature, retains the previous opt-out file and uses the map test's configuration/save restoration. [Method and limits](validation/FPS-0.4.9.md).

`component_profile_smoke.py --level 9 --report example-name` selects a map for component profiling. Its instrumentation overhead rules out using it as an FPS benchmark.

`tools/gameplay_perf_smoke.py --level 9 --seconds 45` measures a short sequence of movement both ways, jumping, melee, shooting and crouching on an actual map. It does not protect or teleport the hero or add ammo. It checks observed movement and active FPS samples; a command acknowledgement alone is insufficient. This is a performance scene, not level completion. Configuration and saves are restored afterwards.

Compare the same APK, viewport and scene. Report duration, warm-up, stalls and measurement overhead. [0.4.8 validation](validation/PORT-0.4.8.md) and [early Huawei measurement limits](validation/TODO-AUDIT.md) explain why short averages are insufficient.

## Evidence and compatibility

Historical hardware includes Redmi Note 8 / Android 16 / ARM64 and Huawei P9 Lite / LineageOS Android 10 / approximately 2 GB RAM. ARMv7 libraries are also built; minimum API is 21. These facts do not prove support for every Android version or 1 GB phone. See the [compatibility matrix](validation/ANDROID-COMPATIBILITY.md) and current allocation before using hardware.

Raw results go to ignored `reports/`, not public source commits. They may contain local configurations, paths, logs and game screenshots. Reviewed summaries belong in `docs/validation/`. Test data and commercial game files remain supplied by the user and must not be published.
