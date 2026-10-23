# Twenty-minute Huawei observation / 20 minut na Huawei

OpenAI Codex (LLM), 2026-10-23. Huawei P9 Lite, LineageOS Android 10, 2 GB RAM,
ARM64. Exact installed APK SHA-256:
`6ab3b9c47b648278eb80cbfb9192437839441ea9886b4d8f96222ad7512b6286`.
This precedes the final save-screen scrolling change; all six shared native
libraries match the later `6175b1…` ARM package byte for byte. Attribute this
observation to the exact tested package, not every later APK.

## English

Controlled existing level-nine scene: setup teleport (11027,5500), settled hero
(11027,5554.6), explicit protection, no shots/movement/ammo edits. Verbose traces
and preview overlay were disabled, then allowed ten seconds to settle. Viewport
remained physical1920x1080/logical853x480. USB tethering/charging was unchanged.
This is a passive live-enemy performance fixture, not a natural playthrough.

| Measurement | Observed value |
| --- | --- |
| Requested / measured time | 1200 / 1200.112 seconds |
| Complete 300-interval batches | 236 |
| Approximate equal-batch harmonic FPS | 58.988 |
| Batch FPS range | 57.0–60.3 |
| Largest batch p95 / single interval | 20 / 31 ms |
| First / last 30-batch arithmetic means | 58.987 / 59.010 FPS |
| Reported battery temperature | 31.0 → 35.0 C |
| End-of-run app PSS | 196810 KiB |

The process remained alive, with no observed fatal marker. Full configuration
and saves restored byte for byte afterward. Ignored evidence:
`reports/sustained-huawei-0.4.25/`, including results, continuous native log,
battery reports, memory listing and final screenshot; restoration comparison is
`reports/readiness-huawei-0.4.25/sustained-restoration.json`.

Every recorded batch exceeded the user's accepted 55 FPS threshold in this one
scene/run. This does **not** establish an instantaneous minimum of 55 FPS: the
31 ms interval is a shorter slowdown within an otherwise faster batch. Rounded
300-loop batches are not frame presentation telemetry. No sustained decay is
established in this run; battery temperature is not CPU temperature and one PSS
sample does not establish a peak or memory-leak trend. All-map performance remains
unverified. No native optimization was made in this release-preparation batch;
do not attribute the difference from older observations to a new optimization.

## Polski

Pełna próba trwała 1200,112 s. W tej ciężkiej scenie zapisano 236 paczek po
300 odstępów: średnio około **58,99 FPS**, najniższa paczka **57 FPS**. Każda
przekroczyła zaakceptowane 55 FPS. Pojedynczy najdłuższy odstęp miał jednak
31 ms, więc nie deklarujemy minimum 55 FPS dla każdej klatki ani wszystkich map.

Nie wystąpiła obserwowana awaria ani trwały spadek średniej pod koniec próby.
Temperatura baterii wzrosła z 31 do 35 C; nie jest to pomiar temperatury CPU.
Końcowy PSS gry wyniósł 196810 KiB, co nie dowodzi braku wycieku pamięci.
Przywrócenie konfiguracji i zapisu potwierdzono sumami plików.

To obserwacja istniejącej sceny z ochroną postaci i wyłączoną diagnostyką,
bez zmian amunicji, rozgrywki lub jakości obrazu. Nie jest przejściem kampanii.
APK wskazane powyżej było testowane przed poprawką przewijania ekranu zapisów;
biblioteki silnika w obu paczkach są identyczne. Nie przypisujemy tego wyniku
nowej optymalizacji ani nie przenosimy go automatycznie na dowolną wersję.
