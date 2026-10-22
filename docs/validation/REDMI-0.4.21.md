# Redmi Note 8 / Android 16

OpenAI Codex (LLM), 2026-10-22. Controller testing excluded.

## Device and exact build

Physical Redmi Note 8, Android 16/API 36, security-patch property 2026-06-01, page size 4096. Reported ABIs ARM64 + ARMv7. Native run uses ARM64. Surface 2340x1080, logical viewport 1040x480, preserving uniform scale. This is a wider view than Huawei 853x480; performance numbers must not be presented as a controlled same-viewport phone comparison.

ARM APK SHA-256 `cfc586439527bb6e4f063d4d6b7b526aa8fa64e2c9f44d6fccc7e7889c7672cf`, version 0.4.21-dev. It is a debug-signed development package. No phone serials or commercial data are published.

## Update and touch

`redmi-update-0.4.21`: update from installed 0.4.3-dev using replacement installation preserved the exact save/config bytes before first launch. Source hashes and before/after copies remain in local reports. This is one actual upgrade path, not all old-version migration coverage.

`redmi-0.4.21-jump-r2`: six focused-window gestures passed, including direct native activity restoration, multitouch, finger drift/cancel and focus transitions. Short rise 73.5–74.1 px; held rise 154.8–155 px; takeoff 17–20 ms. These are window-event timings, not physical digitizer latency. Screenshot layout was visually inspected: uniform image scale, joystick/action buttons clear of health HUD.

The first `redmi-0.4.21-jump` attempt used the tool's default Huawei viewport expectation 853x480 and failed that assertion after execution. Actual Redmi output was 1040x480. Failure is retained; the second run explicitly selected the observed device viewport, without changing rendering or jump thresholds.

`redmi-0.4.21-score` and `redmi-0.4.21-game-over`: actual single-touch return from both end screens passed. These fixtures control the exit/death trigger; they are not natural campaign traversal. Configuration and progress restored after each trial. Huawei USB tethering/network settings were not changed.

## Polski

Fizyczny Redmi Note 8 z Androidem 16 uruchamia wersję ARM64. Aktualizacja z 0.4.3 zachowała zapisy i konfigurację. Próby skoku, wielodotyku, bezpośredniego wznowienia oraz wyjścia z podsumowania i końca gry przeszły. Szerszy ekran pokazuje więcej planszy przy zachowaniu proporcji. To potwierdzenie wymienionych scenariuszy na tym urządzeniu, nie wszystkich Androidów, pełnej kampanii ani stałych 60 FPS.

## Bilingual menus

`redmi-menu-0.4.21-en/pl` passed 17 navigation transitions each, all six volume gestures, mute/unmute and disabled shared-sound controls. Exact-APK translation checks passed 109/109 names in both languages. English maximum-volume screenshot was visually inspected. These are app-window events; no controller was tested.

## Dense level-nine observation

`redmi-dense-9-0.4.21`: 90.24 seconds at controlled position (11027,5500), stationary protected hero, no shots or HP edits, quiet preview diagnostics, viewport 1040x480. After consistently excluding the first 300-frame batch: 17 batches, harmonic mean **59.953 FPS**, batch range 59.6–60.0, worst logged frame **69 ms**, maximum batch p95 18 ms. Battery 28.6→28.7 C, not CPU temperature. Final position unqueried because quiet mode disables mailbox polling; setup position and final screenshot remain. Original files restored. This is short one-scene evidence with occasional stalls, not a sustained/all-level 60 FPS pass. Huawei used a different viewport, so no controlled phone-to-phone speedup is claimed.

## All fourteen map starts

`redmi-production-0.4.21-level1..14` passed with preview diagnostics off, no diagnostic commands, viewport 1040x480 and twelve seconds after each load. Test checkpoint-zero saves use HP 100, lives 3, bullets 10, magic 5, dynamite 3. Original config/progress restored. The table contains only startup-scene frame batches; it does not establish FPS throughout each level or a natural campaign.

| Level | Logged FPS range | Worst logged frame | Maximum batch p95 |
| --- | --- | --- | --- |
| 1 | 60.0–60.3 | 19 ms | 18 ms |
| 2 | 60.0–60.4 | 19 ms | 18 ms |
| 3 | 60.0–60.4 | 40 ms | 18 ms |
| 4 | 60.0–60.3 | 19 ms | 18 ms |
| 5 | 60.0–60.4 | 21 ms | 18 ms |
| 6 | 59.5–60.0 | 89 ms | 18 ms |
| 7 | 60.0–60.4 | 22 ms | 17 ms |
| 8 | 60.0–60.3 | 23 ms | 18 ms |
| 9 | 60.0–60.3 | 18 ms | 18 ms |
| 10 | 60.0–60.2 | 22 ms | 18 ms |
| 11 | 60.0–60.4 | 19 ms | 18 ms |
| 12 | 60.0–60.3 | 20 ms | 18 ms |
| 13 | 60.0–60.4 | 19 ms | 18 ms |
| 14 | 60.0–60.2 | 19 ms | 17 ms |

Startup FPS estimates slightly above 60 reflect finite measurement windows, not a higher refresh-rate claim. Isolated long frames remain visible in the table.

## ARMv7 and final restoration

`compat-redmi-armv7-0.4.21-menu/level` passed actual 32-bit library mapping, native menu, ordinary 100 ms jump, exit pickup, score and level two on this same ARM APK. ARM64 was reinstalled afterwards and confirmed through package metadata. After all menu, performance, map and ABI fixtures, the real save/config bytes were pulled again and compared with their pre-update 0.4.3 copies: both remained identical. This does not claim preservation of every possible preference or verification of untested upgrade paths.

Na Redmi przeszły starty wszystkich 14 map bez diagnostyki oraz rzeczywista próba biblioteki 32-bitowej. Następnie przywrócono ARM64. Pomiary początków map były bliskie 60 FPS, ale wystąpiła pojedyncza klatka 89 ms. Ciężka scena poziomu 9 dała średnio 59,953 FPS przez 90 sekund z przycięciami do 69 ms; nie jest to zaliczenie stałych 60 FPS całej kampanii.
