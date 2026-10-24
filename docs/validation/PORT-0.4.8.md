# 0.4.8 — feature integration, performance and audit

OpenAI Codex (LLM) performed the work and tests on 2026-10-20/21, using requirements and hardware supplied by a human. This is a development checkpoint. Neither a natural full-game completion nor 60 FPS in every situation was established.

## Feature provenance

Reference: Claw Web, Arthur Boss and contributors, commit `e723d3d48b5ba2cc723751209954cfc46c82d202`, GPLv3. The [source comparison](CLAW-WEB-COMPARISON.md) describes the state before integration.

- Direct REZ import and progress export/import adopt the user-flow idea. The new Android implementation uses the system document picker and this port's SAVES.XML format. It does not copy IndexedDB/localStorage or claim compatibility with Claw Web JSON.
- Haptics adapt the idea of the HapticFeedback event/preset layer, with new output through SDL rumble and Android Vibrator. Jump, landing, attack/fire and hurt events are supported; haptics are off by default. Not every upstream footstep, explosion or interface pattern was ported.
- Narrower menu/font preloading adapts their BaseGameApp approach. Gameplay resources still use the inherited OpenClaw cache. The WebGL renderer and browser audio system were not ported.

Credits and revision references appear in NOTICE.md, source comments, the save-tools screen and APK licences. These features do not include original game graphics or audio.

## Installation and saves

The APK includes supporting XML and original neutral helper images. The console font is copied from the phone into local storage; an upstream font with an unconfirmed licence is not redistributed. The user selects a full CLAW.REZ or the existing game-data.zip. The local CrazyHook layout has a 168-byte REZ and loose Assets, so that layout still requires a prepared ZIP.

Save export/import is under PAD → Save backups and haptics. The parser limits size, level/checkpoint numbers, fields and values, and rejects DOCTYPE declarations. Import is staged for the next engine start, retaining the previous SAVES.XML as SAVES.before-import.xml. Writes use a temporary file followed by replacement. Windows saves and Claw Web JSON are not imported.

Android `PortFeaturesTest` passed read/write round trips, applying pending imports, retaining backups and previous progress after invalid import, rejecting invalid REZ, checking support-package contents, and finding the system font. It exercises actual Java classes in an isolated directory, not manual interaction with the system document picker.

`tools/direct_rez_runtime_smoke.py`: the user's full REZ plus support files extracted from the APK started maps 1 and 14 with audio. The 168-byte placeholder was rejected before engine startup; test data and the error message were then corrected. All phone data was restored. This checks the runtime format, not the completeness of every CLAW.REZ edition.

## Optimization without reducing image quality

- ThinLTO and `-O3` are the native defaults. Assertions and symbols remain. No fast-math, solver, resolution, animation-frequency or AI-frequency changes were made. `-PnativeLto=OFF` enables comparison.
- Component-name hashes are static; unnecessary shared_ptr copies were removed when returning raw pointers.
- The update list preserves component-ID order from the map. It skips only exact types inheriting an empty VUpdate: position, render, trigger and health. Type and member-function-pointer checks protect updating subclasses and future overrides. Physics, trigger events, AI and animation still update normally.
- Mix_SetDistance is not repeated when its quantized value is unchanged. No significant separate benefit was demonstrated on level 13.
- The simulation clock resets when loading/pause ends. Blocking load time should not become one large physics or timer step.
- FPS counts active simulation only. Pause and respawn stalls are not evidence of 60 FPS gameplay. Physics/actor/view timing and an optional component profiler were added. The profiler adds overhead and is not itself a benchmark.

Huawei P9 Lite / VNS-L21, LineageOS Android 10, approximately 2 GB RAM, 1920×1080, touch controls visible, music and effects at 22050 Hz. `reports/all-levels-final-0.4.8/` contains 35 seconds at each map's opening scene with a stationary, unprotected hero. Ranges below exclude the first 300-frame batch. These are not the worst scenes, player routes or sustained thermal tests.

| Level | FPS in successive active-frame batches |
| --- | --- |
| 1 | approximately 60 |
| 2 | approximately 60 |
| 3 | approximately 60 |
| 4 | 58–60 |
| 5 | approximately 60 |
| 6 | approximately 41 in this run; 40–60 in other runs, unstable |
| 7 | approximately 60 |
| 8 | 56–58 |
| 9 | 53–56 |
| 10 | approximately 60 |
| 11 | approximately 60 |
| 12 | approximately 60 |
| 13 | 57–59 |
| 14 | approximately 60 |

The earlier level-13 scene in 0.4.7 ran at about 43 FPS. Changing the component update list reduced actor-update time there from about 9.6 to 4.9 ms. Compilation, loading and clock changes were tested in stages, but the table reports their combined result, not each change's individual contribution.

Process PSS snapshots across the maps were approximately 134–187 MiB. These are snapshots, not peak RAM measurements; GPU driver and system memory have separate costs. The script reads the exact PID even from this LineageOS version's aggregate output.

A level-6 repeat on the final APK (`box2d-monotonic-0.4.8`, 40 seconds) measured 55.6 FPS in its first batch, then 60.0–60.4 FPS, p95 18 ms and maxima of 21–27 ms after the first batch. PSS was 194198 KiB. The corrected Box2D profiler reported plausible values, for example collide 0.75 / solve 2.59 / TOI 0.93 ms. This better run does not erase earlier variability or prove 60 FPS throughout the level.

## Bugs and limits

- Ladder bottom: holding Down continued the animation and pushed the hero into the floor despite foot contact. A stop condition alone was insufficient: EndContact did not clear the old ladder-top contact pointer, which Box2D could later free or reuse. The first attempt cleared it before removing platform support and caused a regression: a stale foot contact remained and descent became falling. The final order removes the platform contact first, then clears the pointer. `ladder-balanced-0.4.8` passed the cap, descent, jumps, bottom stop, re-entry and both edges. With Down held, feet stayed at y=1098 above floor y=1100 without further sinking.
- The old Box2D diagnostic clock subtracted unsigned microseconds and produced enormous values across a second boundary. Android now uses signed monotonic time. This fixes measurement, not simulation rules.
- Pinned SDL's USB receiver lacked an export policy required by newer Android versions. An API33+ flag was added while retaining older behavior, in a separate reproducible SDL patch. Physical USB had not yet been tested at this checkpoint.
- Lint: two port-UI findings and the actual USB receiver issue were fixed. Narrow exceptions cover only inherited SDL files: permissions for unused BLE Steam Controller/microphone paths and subclasses selected by API26 conditions. The app gained no microphone access or new Bluetooth permission. Remaining warnings include UI text and old APIs; zero lint errors does not establish full device compatibility.
- Voice/Ambient in the old menu still lacked complete independent control; the 0.4.7 audit remained applicable.

## Gameplay coverage

- All 14 maps loaded with audio, with no detected process crash during short trials.
- All 13 controlled damage/repeated-contact cases passed after update-list and clock changes. These do not replace every boss fight.
- Ladder tests covered the real first ladder of level 1: cap, repeated Up, descent, jump, side exit, and Up+jump. An isolated ladder-bottom/floor fixture was also tested.
- Edge tests covered an isolated ledge, leaving both sides, falling, lower-floor landing and no extra mid-air jump. Teleports and scene isolation are part of the test; this is not natural map traversal. Not every ladder, moving platform, join or level geometry was tested.
- Omar: actual sword/projectile contacts reduced HP 200→0 through both phases, finale staging, score and return to menu. The test used teleports, powerups, infinite ammunition and player protection, without editing boss HP. It does not prove an ordinary final-boss victory with resources collected during a campaign.

**Natural completion of levels 1→14 remained unverified.** Teleports, level unlocks and map loading do not replace it. Routes, every boss fight, ordinary death/respawn/checkpoints and all ladder/edge variants remained open. A blocked run needs its level, checkpoint and preceding actions recorded, a separate reproduction, and a route retest after fixing the cause.

## Final APK candidate

`dist/kapitan-pazur-0.4.8-debug-universal.apk`, version 0.4.8-dev (20), ARM64 + ARMv7. SHA-256: `455b2ef12e2831ad74d87a571a1eb837eb06cffe8dd1af12b55a3e4b3d6cc526`. This is a local development build without original game data.

- `ladder-balanced-0.4.8` and `ladder-real-balanced-0.4.8`: isolated and real first-level ladder trials passed.
- `combat-balanced-0.4.8`: 13/13 cases passed, including repeated callbacks for the same projectile without duplicate damage.
- `jump-touch-balanced-0.4.8`: six measurements passed; short tap rise 72.9–74.1 px, long hold 155 px, event-to-takeoff latency 29–31 ms. This is app-local input timing, not full physical-screen latency. Touch movement, pointer drift, pause and background/resume tests passed.
- `omar-balanced-0.4.8`: both phases (HP 200→0), finale, score and menu passed again after the final contact change. This remains an explicitly assisted fixture.
- `features-balanced-0.4.8.txt`: the final APK passed import, previous-save backup, invalid-import protection, invalid-REZ rejection and support-package checks again.
- ELF checks for both ABIs, ARM64 16 KiB alignment, zipalign and v1/v2 signatures passed. The signature verifier reported its standard Gradle metadata warning for META-INF.
- Both patches applied to clean source copies and matched 42 changed OpenClaw files and one SDL file with CRLF normalization. Lint: 0 errors, 33 warnings; not every warning was fixed.
