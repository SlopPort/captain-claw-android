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
