# Campaign validation toward 1.0

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Work and testing by OpenAI Codex (LLM), 2026-10-21/22. Human reports and hardware are acknowledged without personal identifying information. This is a work log, not a declaration that version 1.0 is ready.

## Reproduced blockers

- Collecting the real level-one end pickup reached the score screen, then a missing regional voice file (`/states/booty/sounds/claw/1110004.wav`) caused an assertion in HumanView. Optional missing WAV playback now logs and returns instead of aborting the game. This does not add copyrighted recordings to the project.
- The score screen handled keyboard confirmation only. Android left mouse presses, including SDL-translated screen taps, now call the existing score-state progression. Desktop controls are unchanged.
- `omar-campaign-current1` defeated Omar and completed the finale/score, then returning to the menu exposed missing credit PNGs in our new XML support bundle. Menu initialization loads every page, so this was a packaging regression, not merely an unavailable optional credit screen. Generated original credit cards now supply both paths; packaging checks all support-PNG references and uses stable metadata. `omar-campaign-credits-fixed` passed on 0.4.12-dev: both combat phases, finale, score, return to menu and no level-15 save. Fixtures include teleports, elemental powerups, infinite ammo and protection; no boss-health edits.

## Controlled transition tests

`tools/campaign_score_smoke.py` uses `CampaignSession` to back up and restore the phone's configuration and saves. It starts an isolated save, teleports to an **existing** end pickup, lets normal collision collect it, confirms the score screen using app-local SDL mouse events, checks that the next map loads and inspects its saved checkpoint. No global Android input or USB/network configuration changes are used.

The initial level 1 → 2 test passed on Huawei P9 Lite / Android 10. APK SHA-256: `71d8bc83eed5c81858419f7dd3a8f8dd63fddb71bf3922497b69c04e250906ad`. Evidence: ignored local report `reports/campaign-score-touch-fixed`. This first test skipped the intro quickly; it does not alone prove the missing voice branch was exercised after the fix.

These are technical transition tests, **not natural playthroughs**. Teleporting does not establish that platforms, routes or bosses can be passed. App-local SDL events also do not establish Android window touch delivery; that requires a separate instrumentation test.

Further tests of 3 → 4, 5 → 6, 7 → 8, 9 → 10 and 11 → 12 passed with next-level saves. Each has its own `reports/campaign-score-fixed-levelN` evidence folder and JSON result. The level-seven and level-nine intros explicitly logged `Skipping unavailable sound` and continued successfully, exercising the missing-WAV fix.

Android window touch confirmation also passed: `reports/score-android-window1`. Instrumentation dispatches finger MotionEvents only to this game's focused window, after collecting the real level-one end pickup. Three taps advance the score screen and level 2 loads. This closes the input-delivery gap in the earlier SDL-only tests.

## Encounter audit finding

The inherited converter skipped `AquatisCrack`, `AquatisDynamite` and `Tentacle` on level 12. `AquatisEncounter.cpp` contains empty active update/animation behavior and a commented-out state activation. The added Android arena component now connects original WWD tentacles, crack, dynamite resupply and five stalactites to the existing boss health/death/gem flow. Normal generic boss melee remains in OpenClaw.

`reports/aquatis-arena-rules2` passed all five rock strikes, tentacle respawns, boss defeat and level 13 loading. The test uses actual pistol projectile collisions and real dynamite fuses, with teleports, player protection and spawned projectiles explicitly recorded. Direct bullets, a crack explosion with uncleared tentacles and explosions outside the crack did not damage the boss. Boss HP is never edited by the fixture.

The normal charged player throw subsequently passed in `aquatis-player-throw5-bounds`, after implementing the missing dynamite receptacle and using its actual imported image bounds. `aquatis-player-fight-reset1` then passed the full controlled ordinary-input fight, actual ammo consumption/resupply and recovery after a real water death. It uses teleports and combat protection, but no spawned projectiles or health/ammo edits. Original-game timing, hitbox and balance parity remain unverified. See [Aquatis arena notes](AQUATIS-ARENA.md).

Controlled real sword attacks, existing gem collection, score confirmation and next-level saves passed for LaRaux (2 → 3), Katherine (4 → 5), Wolvington (6 → 7) and Red Tail (13 → 14). Evidence: `boss-campaign-level2-pilot`, `boss-campaign-level4-audio`, `boss-campaign-level6-audio`, `boss-campaign-level13-audio`. These use teleports and player protection, not boss HP edits. They do not certify full arena behavior or natural map traversal. Attack-audio findings and tests are recorded in [the audio audit](ATTACK-AUDIO.md).

Further source review found empty Marrow parrot/floor behavior. The new implementation adds three parrot hits, extending/retracting bridges, five successful sword hits per phase and carrying between sides. `marrow-contact-fight8-transition` passed the full controlled encounter, real gem, score and level 11 load. `marrow-death-reset-0.4.12` additionally passed a real arena-pit death (lives 3 to 2), boss reset from 100 to 150 HP on the initial side, complete rematch, gem and level 11. Original timing/balance parity and dedicated negative phase gates remain open. See [Marrow encounter notes](MARROW-ENCOUNTER.md).

`gabriel-button-fight6-atomic-input` passed the inherited real button/raised-cannon mechanic, four 25 HP hits, boss defeat, real gem, score and level 9. The fixture uses teleports/protection and ordinary sword events. Its development failures and the inherited missing vertical projectile visual are documented in [Gabriel encounter notes](GABRIEL-ENCOUNTER.md).

## Remaining release gates

- Technical exits for all fourteen levels now have controlled evidence across the reports above, including the finale/menu/no-level-15 regression. Preserve those results while completing the remaining natural-playthrough and reset gates.
- Verify every boss with actual damage and encounter mechanics; record any assistance or fixtures explicitly.
- Complete natural traversal of all fourteen levels, including ladders, edges, disappearing platforms, checkpoint recovery, death and resource carry-over.
- Recheck physical controller bindings and Android window touch, including score and final screens.
- Recheck installation/import, update, save backup and restore, lifecycle and audio on the weak phone.
- Document remaining performance limits: the dense level-nine scene previously measured approximately 57–59 FPS; 60 FPS throughout the campaign is not demonstrated.
- Finish Polish/English installation and known-issues documentation, source/notice audit, reproducible packaging and final APK verification. Keep proprietary game data outside the open-source distribution.
- User-requested follow-up, 2026-10-22: expand vertical-offset combat tests in both directions (hero above/below enemy), including stairs, ledges, airborne and crouching attacks; distinguish attack areas from hurt bodies and verify possible counterattacks/escape.
- Compare behavior with the original game and available source evidence. Do not call OpenClaw original Monolith source, and do not claim access to original game source without finding and establishing its provenance. Identify observations, design-document descriptions and reconstruction choices separately.
- Add English application/control UI in addition to the existing English documentation. Inventory native touch/menu labels, Android screens, errors and help; document any game-data language dependency instead of claiming all original recordings/text are translated.
