# Campaign validation toward 1.0 / Kampania przed 1.0

Work and testing by OpenAI Codex (LLM), 2026-10-21. Human reports and hardware are acknowledged without personal identifying information. This is a work log, not a declaration that version 1.0 is ready.

## Reproduced blockers / Odtworzone blokady

- Collecting the real level-one end pickup reached the score screen, then a missing regional voice file (`/states/booty/sounds/claw/1110004.wav`) caused an assertion in HumanView. Optional missing WAV playback now logs and returns instead of aborting the game. This does not add copyrighted recordings to the project.
- The score screen handled keyboard confirmation only. Android left mouse presses, including SDL-translated screen taps, now call the existing score-state progression. Desktop controls are unchanged.

## Controlled transition tests / Kontrolowane przejścia

`tools/campaign_score_smoke.py` uses `CampaignSession` to back up and restore the phone's configuration and saves. It starts an isolated save, teleports to an **existing** end pickup, lets normal collision collect it, confirms the score screen using app-local SDL mouse events, checks that the next map loads and inspects its saved checkpoint. No global Android input or USB/network configuration changes are used.

The initial level 1 → 2 test passed on Huawei P9 Lite / Android 10. APK SHA-256: `71d8bc83eed5c81858419f7dd3a8f8dd63fddb71bf3922497b69c04e250906ad`. Evidence: ignored local report `reports/campaign-score-touch-fixed`. This first test skipped the intro quickly; it does not alone prove the missing voice branch was exercised after the fix.

These are technical transition tests, **not natural playthroughs**. Teleporting does not establish that platforms, routes or bosses can be passed. App-local SDL events also do not establish Android window touch delivery; that requires a separate instrumentation test.

Further tests of 3 → 4, 5 → 6, 7 → 8 9 → 10 and 11 → 12 passed with next-level saves. Each has its own `reports/campaign-score-fixed-levelN` evidence folder and JSON result. The level-seven and level-nine intros explicitly logged `Skipping unavailable sound` and continued successfully, exercising the missing-WAV fix.

## Encounter audit finding / Wynik przeglądu bossów

The current converter explicitly skips `AquatisCrack`, `AquatisDynamite` and `Tentacle` on level 12. `AquatisEncounter.cpp` has empty active update/animation behavior and a commented-out state activation. The prototype describes stalactite damage, but this encounter cannot be accepted as complete based on map loading. This is a concrete implementation gap requiring an encounter-level test and repair before 1.0; no claim of a completed normal Aquatis fight is made.

## Remaining release gates / Warunki wydania

- Record technical transitions for all normal exits and boss-generated exits; verify final completion returns correctly without creating level 15.
- Verify every boss with actual damage and encounter mechanics; record any assistance or fixtures explicitly.
- Complete natural traversal of all fourteen levels, including ladders, edges, disappearing platforms, checkpoint recovery, death and resource carry-over.
- Recheck physical controller bindings and Android window touch, including score and final screens.
- Recheck installation/import, update, save backup and restore, lifecycle and audio on the weak phone.
- Document remaining performance limits: the dense level-nine scene previously measured approximately 57–59 FPS; 60 FPS throughout the campaign is not demonstrated.
- Finish Polish/English installation and known-issues documentation, source/notice audit, reproducible packaging and final APK verification. Keep proprietary game data outside the open-source distribution.

Po polsku: przejście końca mapy przez teleport jest próbą techniczną. Nie oznacza ukończenia kampanii zwykłą rozgrywką. Dopóki powyższe próby nie zostaną zakończone, nie oznaczamy wydania jako gotowej wersji 1.0.
