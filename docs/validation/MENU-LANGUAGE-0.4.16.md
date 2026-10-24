# Menu PL/EN checkpoint 0.4.16-dev

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-22. Development checkpoint, not a completed 1.0 campaign certification.

## Implementation

Android menu action/title text is now rendered locally in Polish or English, with the phone's installed font. No commercial English lettering or third-party font file is added to the APK/source archive. Menu backgrounds/branding and recorded dialogue still come from the player's data. Original score-screen artwork is not relabeled by this menu renderer.

The renderer covers main/pause/Game Over labels, level and checkpoint names, touch help, audio descriptions and the port's original attribution cards. Polish diacritics are supported. Textures are created during menu initialization, not on every frame. Font size is fitted with reflow to keep longer translations readable. Action rectangles are centered consistently; the level grid and volume rows retain their layout. Owned labels use the same position/rectangle as touch testing, without inherited bitmap offsets.

Inherited buttons targeting nonexistent pages are disabled instead of accepting a click that goes nowhere. This includes unsupported multiplayer/custom-level/movie and some options pages; it does not implement those features. Voice and ambient sounds share the master Sound option in the existing audio backend. Their inherited independent no-op toggles are now disabled and labeled accordingly. At this 0.4.16 checkpoint, touch dragging of legacy volume knobs still needed separate implementation; [the later 0.4.19 audio work](MENU-AUDIO-0.4.19.md) addresses it and a mute/unmute state bug. Navigation coverage alone is not a test of every audio control.

The Android settings overlay moves above menus and remains at the bottom during gameplay. Its previous bottom-center placement covered part of Quit. Controller bindings/transport are unchanged and were not tested in this work.

## Exact ARM candidate and runtime evidence

`reports/kapitan-pazur-0.4.16-menu-diagnostic-arm.apk`, versionCode 28, ARM64 + ARMv7. SHA-256 `453942fa75eec387746563681af29c0d5aedcd3fa764d2455252e43225038123`.

- `menu-language-huawei-0.4.16-r4-en/pl`: both passed 17 actual page transitions using focused game-window touch and Escape. This includes help, level selection, audio, credits, Quit/cancel, keyboard cancel and attempts to click disabled controls. No global Android input or controller events were injected.
- `check_menu_translation.py` reads menu definitions from that actual APK's support archive and checks runtime labels. **109 named text/action items, zero missing in either language**. This includes initialization of checkpoint subpages; it does not mean every checkpoint subpage was visited. Support SHA-256 `3a1b9ef10ab1ccf69d46e3ca528a2406760935f8870d3c5fc8f4f3ff55cee829`.
- Earlier aligned candidate `78b1fcc3a2abb6c8db04d4a8669b6533c120b8c1f93cdb4f71f5b466a5ecfa65` also passed full PL/EN navigation; its main/level/audio/help/credits captures were inspected. Later changes clarify shared audio settings, improve credit text fitting and add opt-in tap diagnostics.
- `menu-stress-huawei-0.4.16-en`: **30 repeated entry/exit cycles, 120 expected transitions**, no retrying missed taps. Original configuration, progress and language preference/native file were restored by the harness/instrumentation.

## Failed attempts retained

The first route expected Help's Back button to return to its index, but the inherited XML returns directly to Main. The test's extra Escape opened Quit; correcting the expected route was a harness fix. No engine change is claimed for that failure.

`menu-language-huawei-0.4.16-r3-en` observed one missing New Game transition with a 60 ms injected tap. It remains a failed report. The next candidate added opt-in coordinate/item-rectangle diagnostics, without changing tap duration or retrying input. Full PL/EN navigation and the 30-cycle stress run then passed. The isolated miss was not reproduced or conclusively attributed; logging is not claimed to fix it.

On the older API-35 4 KB emulator, initial tests stopped rather than sending input after focus loss. A captured image identified Android's first-use fullscreen education panel. Its accessibility package was `android`; the test now allows clicking only its exact introduction/button on the task emulator, guarded by emulator hardware and an explicit flag. No physical phone system dialogs/settings were changed. An earlier boot also had empty emulator fixture config/save files of undetermined cause; preserved valid fixture backups were restored only on that emulator. Neither issue is relabeled as a successful game trial.

The old x86_64 APK `4e2e28fc4e3b8b42cd246120f759819e40b8ceecbc6cf7dd33da1c7eb27da605` passed PL/EN navigation in `menu-language-api35-0.4.16-r7`. It predates the final ARM layout/audio/diagnostic changes and is not evidence for the final candidate on every Android version.

## Final ARM checkpoint

Final local ARM APK: `ea216541214684b0a2ea50dca60dd78dd4d1fa87f9102a54831b8f9c8cfa901b`, version 0.4.16-dev (28). `menu-font-batch-0.4.16-en/pl` passed all 17 transitions and the actual-APK translation check: 109/109 named elements in each language. Final English credits were visually inspected; attribution, licensing and LLM disclosure fit.

Menu initialization now reuses system font faces by point size within one SDL-thread initialization and closes them afterward. It does not keep font objects alive across SDL teardown or rebuild text each frame. This reduces repeated font opening; no gameplay FPS improvement is claimed.

On this exact ARM APK, `menu-font-batch-score-0.4.16` passed score-to-level-two transition, `menu-font-batch-jump-0.4.16` passed six focused-window jump/multitouch/focus cases (15–21 ms measured takeoff, short rise 70.1–73.5 px, held rise 155 px), and `reports/menu-font-batch-game-over-0.4.16` passed one-touch Game Over return. The latter report is nested under the local reports directory. Config/saves were restored. The earlier 1.5-second Game Over test ended during main-menu creation; its failed report remains failed. The final test waits eight seconds after one tap; it does not certify a 1.5-second response-time target.

Separate x86_64 candidate `891da6d0348f447c00f8cb2e9f98d6fdb9285c3c9eb20cad21ef267c1bf73951` passed PL/EN menu navigation in `menu-api35-16k-0.4.16-r3-en/pl` on the official API-35 Google APIs 16 KB emulator. Runtime `getconf PAGE_SIZE` returned 16384. It predates the final font-batch change and is not the ARM distribution. The preceding r2 harness rejected an unrelated Google search-process crash; original raw failure is retained. Crash attribution now requires our process markers or an explicit process name, and fails closed for unidentified fatal lines.

The test harness also refuses pending save restores/import recovery before replacing fixture files, so it cannot consume a player's queued restore and then overwrite it during cleanup. Controller testing remains excluded.
