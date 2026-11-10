# Debug 0.4.36 validation — 2026-10-30

Implementation, investigation and automated validation by OpenAI Codex (LLM), guided by anonymous human reports. Latest inherited project change reviewed: commit425cdb1, which introduced touch customization and working three-preset difficulty. Those features were retained.

## Artifact and scope

Huawei ARM64 debug app was updated in place, without uninstalling. Version code48, version0.4.36-dev; combined ARM64/ARMv7 APK SHA256 `63478ba59d551d37ef9c1fffe3cf473287de09a4dc8c763eb213adc4eeb1c013`, 36,508,741 bytes at the time of this build. Use the actual local artifact metadata if a future build differs. ARM64 was physically run; ARMv7 was built only. Both ABI/library packaging and 16 KB ARM64 ELF LOAD alignment passed. Public signed distribution remains 0.4.32-test; no public signed debug36 release is claimed.

## Changes and evidence

- [Menu audit](MENU-AUDIT-2026-10-30.md): six unsupported rows omitted and three action lists compacted. Physical Polish and English focused-window touch navigation passed; all103 expected text/item names and all6 intentional omissions matched runtime evidence. Working Controls/Difficulty and checkpoint-saving explanation remain.
- [Forest motion](FOREST-MOTION-2026-10-30.md): actual leafy-ladder cap geometry replaces the sensor-top assumption; small final ascent completion excludes descent and jump requests. Rope-only clock catch-up and interpolation move the hero/grab trigger each update, retaining map-specific authored frame timing. Real trigger attachment, carrying and jump-detachment passed.
- [Le Rauxe](LERAUX-ORIGINAL-2026-10-30.md): original executable analysis establishes a random pause branch, not a mandatory exact per-strike delay. The port now uses a boss-only300–600ms delay range, with actual uninterrupted strike intervals0.707–0.932s in the fixture. Existing parry percentages remain unchanged and original exact blocking remains unresolved.

## Retained failures and limits

The initial local map-reader launch used an incompatible DLL search path and displayed a Windows application-error dialog. The matching MSYS UCRT directory was subsequently selected only in that helper's environment; no global PATH/Windows settings were changed. Later map reads succeeded. This helper is separate from the phone game.

Physical fixtures caught two intermediate native defects before final validation: an inherited unimplemented physical-position getter, and an immediate transform inside the rope contact callback while Box2D was locked. Both were corrected and the failed attempts remain in the forest report. The first forest harness also carried climbing state between teleports; a fresh-process-per-cap revision was used afterward. The first final build command lacked its process-local Android SDK path and failed configuration; the corrected build passed. None of these failures is omitted from the evidence.

Human playtesting still owns the campaign. Teleports, removed enemies and protected-player boss/rope fixtures are explicitly technical evidence. No full natural campaign, broad controller sweep, physical ARMv7 runtime, all-level FPS minimum or pristine-original parity is claimed. User configuration/saves are restored and byte-checked after each fixture; menu tests restore their preference changes. The previously reported level2 platform blockage remains open. Human rechecks of boss feel, natural leafy-ladder approaches and vine visual smoothness are still needed.

The final forest cap matrix was repeated on the exact final APK and passed. A final source-only comment correction removes an unsupported RNG-correlation inference; it changes no executable behavior or test result. Clean engine patch reconstruction passed for59 changed files and SDL for1 file.

Level1 ladder summit/release/descent/jump and solid-floor bottom regressions passed on the final APK. Raw user video, screenshots containing proprietary game backgrounds, original executable and REA decompilation remain ignored/private.
