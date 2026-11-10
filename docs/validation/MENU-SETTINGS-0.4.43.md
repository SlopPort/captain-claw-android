# Menus, settings and resume: debug43

OpenAI Codex (LLM), 2026-11-10. Huawei P9 Lite, LineageOS Android 10, ARM64. Exact installed debug43 APK SHA-256 `dfedd91134113cacf5f43dbdbe17e6575b0848a43710922eeaea86d777e35b8a`. No native/gameplay change or new APK was needed for these checks. Public download remains 0.4.41-test.

## Completed menu/settings batch

`todo-menu-settings-0.4.43-20261110/results.json` records successful `menus`, `gameplay-options` and `lifecycle` cases. After each child, the runner checked fresh configuration/progress restoration and the unchanged installed APK hash. These are technical fixtures, not campaign or physical-controller acceptance.

Both English and Polish focused-window menu navigation passed the expected page sequence, including help, single-player/new-game pages, options, audio, credits, quit/cancel and Escape return. Android settings/editor pages were exercised by the same instrumentation. The native log contained **276 English and 271 Polish localized texture states**; these are emitted states, not counts of unique translated messages. Recorded labels matched the requested locale and fit their item bounds. No target or unattributed fatal crash was found.

Audio slider tests covered zero/maximum, changed committed values, cancel paths and toggles. The six recorded volume commits had the expected channel sequence and ended at effects 50/music 20 in the temporary fixture. Independent voice/ambient controls remained disabled through the tested transitions because they share the sound setting. Multiplayer was absent; no disabled destination accepted input or font fallback was logged.

The Java instrumentation restores the previous language, native language file and control preferences. The runner independently verifies the game's configuration/progress files; this is not a signed-version upgrade test or whole-device preference audit.

Visual review covered English Options/Audio and Polish Audio/Difficulty screenshots: the inspected labels were readable without visible clipping, disabled shared-sound labels were distinct, and the difficulty page explained the actual damage/healing behavior. This subset does not certify every screen size or every captured screen. Screenshots containing player-supplied game art remain private.

## Gameplay options and own-app focus transition

The gameplay-options fixture passed its native assertions for four control layouts times three movement modes, direction drag-out/re-entry, release, custom button bounds, three damage scales and three healing scales. This is controlled input/health setup, not physical multitouch, natural combat or original difficulty behavior.

The lifecycle fixture used app-local virtual controller input. After own-app focus return, held-axis drift was **0.0 px**; a fresh press moved **179.55 px**. This does not test Bluetooth transport/reconnection, screen lock or arbitrary OS process death. Existing historical emulator results are not transferred to this ARM APK.

## Catnip backlog clarification

The earlier instrument-loading stall was fixed by preparing Catnip music before gameplay; prepared acquisition/expiry/reacquisition switches subsequently measured 1/1/2 ms on debug42. No new recurrence has been established. AUDIO-02 is explicitly a frozen-candidate **regression acceptance** check of the actual pickup/timer/expiry path, not a newly confirmed bug or authorization to repeat optimization without evidence. This batch did not collect a new physical-pickup frame trace.

## Score and whole-screen Game Over

The score fixture teleported to the existing level-1 exit pickup, opened the score screen and used focused Android window taps to advance into level 2. This is a technical transition, not natural campaign traversal or separate proof of saved-progress continuity. The runner verified fresh configuration/progress restoration and unchanged APK. Evidence: `todo-score-0.4.43-20261110/results.json`.

Two fresh Game Over fixtures tapped **(10,10)** and **(843,470)** in the actual **853x480** logical viewport. Both returned to the main menu with the process alive, no target/unattributed fatal crash and restored fresh configuration/progress. These corner taps were app-local SDL diagnostic events, not physical-screen touches; the earlier debug43 center case separately used focused Android window MotionEvents. Evidence: `todo-game-over-corners-0.4.43-20261110-top-left/results.json` and `...-bottom-right/results.json`.

Visual review of the Polish Game Over capture confirmed the larger heading, divider and separate readable whole-screen instruction: the instruction describes tapping anywhere to return to the main menu. This is one title plus one instruction, not two selectable options. English Game Over presentation and other display shapes were not visually certified by these Polish captures.

UI-01/03, INPUT-01/02/03 and LIFE-01 retain their broader acceptance conditions, including remaining physical input, display variants, process-death and final signed-artifact coverage.
