# 0.4.12-dev validation / Walidacja

Work by OpenAI Codex (LLM), 2026-10-21/22. This is a development checkpoint, not a final 1.0 release.

## Campaign and audio

Controlled technical transitions now cover the fourteen campaign levels, including real boss gems and finale/menu return. This does not replace natural traversal of the maps. Aquatis ordinary-input/resupply/real-death-reset and Marrow three-phase bridge/parrot/carry fights passed with explicit setup/protection fixtures. Gabriel's ordinary sword-button/cannon fight passed; its inherited missing vertical cannonball visual remains documented. See [campaign release gates](CAMPAIGN-1.0.md).

The new engine-support update initially omitted two credit PNGs: menu initialization after Omar asserted. Original generated credit cards now supply these resources, preserve upstream attribution and state LLM involvement. `omar-campaign-credits-fixed` passed combat, finale, score, menu and no level-15 save. Packaging checks all referenced support PNGs, uses stable ZIP metadata and copies no commercial art/fonts.

Five attack-effect references were added to existing user-owned recordings. Claw sword/gun, officer and both chameleon effects passed actual nonzero mixed-output checks. This is not a physical speaker/listening test. See [audio evidence](ATTACK-AUDIO.md).

## Hardware and compatibility

Huawei Android 10/2 GB RAM: ARM64 campaign tests and real ARMv7 process/menu/jump/level-transition checks passed. The original ARM64 installation was restored. API 35/Android 15 x86_64 emulator: native process, menu, held jump and level transition passed, but a short tap failed under severe stalls. The emulator uses 4 KB pages; 16 KB runtime support remains unverified. See [compatibility limits](ANDROID-COMPATIBILITY.md).

An official Android 5.0.2/API-21 x86_64 emulator subsequently passed menu, both separately tested short/held jumps and real level-one exit/score/level-two loading. Data was staged locally; file-picker import and physical old phones remain unverified. Old toolbox/ADB/logcat differences required test-harness adaptations, documented in the compatibility report. Both task-created emulators were closed after testing.

`perf-0.4.12-level9`: sixty-second action loop near the actual map start, without teleports, protection or ammo edits, passed. Twelve frame samples: 57.8 and 59.3 FPS initially, then 59.7–60.2 FPS; later p95 was 18 ms. This route is not the previously documented dense level-nine scene and does not establish 60 FPS throughout the level or campaign. Startup surface reported 1800×1020, logical view 847×480. Original config/saves restored.

The performance script originally hashed the workstation build output, which had become the separate x86_64 APK. The report now records the actual installed phone package, pulled immediately after testing: `992446a223d42eff8c363c3f1b0f0be1c0bf7a7dc5e9c14814447121eff3b333`. The incorrect hash and reason for correction are retained in its report metadata. The script now hashes the installed package.

## Distribution checkpoint

`campaign-start-0.4.12-level1` through `level14` passed: each map loaded from an isolated save, remained alive for eight seconds after loading, and produced a screenshot/process-memory record. No teleports, protection or health edits were used. This is a startup sweep, not traversal. Original config/saves were restored after every map.

`features-0.4.12.txt` passed real Android instrumentation: save validation roundtrip, pending import and backup, invalid import preserving progress, invalid REZ rejection, and exact XML/generated-help/credits support content. The test operates in an isolated staging directory and does not replace user progress.

`marrow-death-reset-0.4.12` passed actual life loss in the arena pit, boss health/position reset, full rematch and next-level transition. See [the encounter evidence](MARROW-ENCOUNTER.md). User files were restored afterward.

`checkpoint-process-reload-0.4.12-r3` passed actual checkpoint-one collision/save on level one, process shutdown/restart, virtual-pad menu selection and reload near the saved point (6882, 4991.6). Only setup teleport/isolated saves were used; no synthetic save/checkpoint/load events. The first trial repeated the held menu direction because USB release arrived late and selected level start; the second was rejected because combat-key commands are intentionally unavailable in menu context. A test-only virtual-pad pulse now schedules its own button release; normal physical-controller behavior is unchanged. Original files were restored after every attempt. This later diagnostic build is distinct from the distributed APK hash below.

`lifecycle-focus-0.4.12` passed own-app transitions from GameActivity to controller settings and back. A virtual left-stick direction held across focus loss produced zero post-resume drift; after neutral and a fresh press, measured movement was 173.57 pixels. Instrumentation starts/finishes only the game's activities and sends no system-wide input. This is not a physical Bluetooth or full background/process-death lifecycle test. User files were restored.

Startup-sweep process PSS samples ranged from 132175 to 182391 KiB (largest sampled value on level 13, approximately 178 MiB). These are point samples after loading, not peak campaign memory, total phone use or a leak/thermal test.

Local ARM APK: `dist/kapitan-pazur-0.4.12-dev.apk`, SHA-256 `992446a223d42eff8c363c3f1b0f0be1c0bf7a7dc5e9c14814447121eff3b333`. ELF alignment, both ARM ABIs, ZIP alignment with 16 KB checks and APK signature verification passed. The source archive created at commit `27694c6` has SHA-256 `a956e3eeb9fb12b1b27964ae0890786e993bc319809f9e9ccbeebfe47450a55d`; later compatibility evidence is committed separately. Proprietary data remains outside source/APK distribution.

Po polsku: to sprawdzony etap rozwojowy z nowymi walkami i poprawkami, nie certyfikat ukończenia całej kampanii ani zgodności ze wszystkimi Androidami. Naturalne przejście, część resetów bossów, dalsze próby urządzeń i spadki przy długich klatkach pozostają otwarte.
