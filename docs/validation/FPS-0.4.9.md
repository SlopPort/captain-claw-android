# Optymalizacja FPS — 0.4.9

Prace i pomiary wykonał Codex (LLM), 2026-10-21. Sprzęt: Huawei P9 Lite VNS-L21, LineageOS Android 10, około 2 GB RAM, ekran 1920×1080. Zachowano rozdzielczość, proporcje, filtrowanie nearest, widoczność dotyku, muzykę i efekty 22050 Hz oraz reguły aktualizacji i fizyki z 0.4.8.

## Punkt wyjścia

Ponowiony pomiar 0.4.8 (`reports/fps-baseline-0.4.9`, po 35 sekund na początek mapy, bez ochrony gracza), z pominięciem pierwszej partii 300 aktywnych klatek:

| Poziom | FPS |
|---|---|
| 8 | 56,4–57,9 |
| 9 | 52,6–56,1 |
| 13 | 56,1–59,5 |

Na poziomie 9 aktualizacja zajmowała około 10 ms, a faza renderowania wraz z prezentacją około 8 ms. Profil komponentów wskazał animacje jako największy koszt aktualizacji, ale sam profiler zwiększa narzut; jego wyników nie traktujemy jako benchmarku FPS. Box2D zachowuje 10/8 iteracji solvera.

## Przyczyna i zmiana

Androidowy punkt wejścia wybiera `opengles2` przez `SDL_HINT_RENDER_DRIVER`. W przypiętym SDL taki jawny wybór ustawia domyślnie `batching = SDL_FALSE`. To oznacza wykonywanie kolejki po poszczególnych poleceniach zamiast wspólnego przekazania poleceń do sterownika. Ustawienie `SDL_HINT_RENDER_BATCHING=1` jawnie włącza kolejkę. Źródło: [SDL_render.c, przypięta rewizja](https://github.com/libsdl-org/SDL/blob/5d249570393f7a37e037abf22cd6012a4cc56a71/src/render/SDL_render.c#L1008), w szczególności wybór sterownika i nadpisanie polityki batching około linii 1069.

To użycie istniejącej funkcji SDL, nie nasz nowy renderer. Integracja Androida zachowuje kolejność rysowania i stany tekstur; kod gry nie przeplata SDL z bezpośrednimi wywołaniami OpenGL. Nie zmniejszamy obrazu, liczby przeciwników, tempa animacji ani częstotliwości logiki.

Diagnostyczny plik `render-batching-off` w katalogu danych aplikacji wyłącza tę zmianę przy następnym starcie. Pozwala porównać identyczny APK i stanowi lokalną drogę powrotu przy problemie sterownika. Nie usuwa danych gry ani zapisów.

## Metoda porównania

`python tools/render_batch_smoke.py --levels 8 9 13 --hold-seconds 35 --report fps-batching-ab` uruchamia kolejno grupowanie wyłączone, włączone i ponownie wyłączone. Każdy przebieg korzysta z tego samego APK i identycznych ustawień oraz tymczasowego odblokowania map. Skrypt wymaga właściwego komunikatu o trybie w logu i zachowuje poprzedni plik opt-out; podskrypt przywraca konfigurację oraz postęp. Zapisujemy również stan baterii przed każdym przebiegiem. Nie wymuszamy częstotliwości CPU/GPU, temperatury ani trybu wydajności telefonu.

Zakres testu to nieruchomy początek mapy. Wynik nie obejmuje całej trasy, wszystkich walk, temperatury po długiej grze ani innych sterowników GPU. FPS liczymy tylko podczas aktywnej symulacji, a faza renderowania zawiera oczekiwanie na prezentację; nie jest to czysty pomiar czasu GPU.

Wykryto też istniejącą zmienność startu trybu pełnoekranowego: czasem silnik odczytuje powierzchnię 1800×1020 przed schowaniem pasków systemowych i wybiera 847×480, a czasem 1920×1080 → 853×480. Fizyczny ekran i zrzuty pozostają 1920×1080; pierwszy wariant ma niewielki margines. W pierwszej parze poziomu 8 i 9 warianty te się różniły, więc te porównania mają dodatkowe ograniczenie. Poziom 9 z batching miał szersze 853×480 wobec 847×480 bez batching; poziom 13 miał identyczne 847×480. To osobny błąd ustalania wymiarów przy starcie, nie celowe obniżenie jakości na potrzeby benchmarku. Narzędzie zapisuje teraz również faktycznie wybrane wymiary logiczne.

## Wynik off/on/off

Ten sam APK w `reports/fps-batching-ab`, średnia kolejnych sześciu partii po 300 aktywnych klatek, po pominięciu pierwszej partii:

| Poziom | Wyłączone | Włączone | Ponownie wyłączone |
|---|---:|---:|---:|
| 8 | 56,90 | 60,20 | 56,42 |
| 9 | 54,22 | 60,20 | 54,98 |
| 13 | 57,93 | 60,17 | 57,05 |

Przy włączonej kolejce p95 wynosiło 17–18 ms; bez niej 19–22 ms. Raportowane 60,2 oznacza około 60 FPS (rozdzielczość i sposób pomiaru zegara), nie podwyższenie częstotliwości ekranu. Temperatura baterii przed kolejnymi seriami: 31 / 32 / 32°C; to nie temperatura CPU/GPU ani gwarancja braku throttlingu. Spadek po powrotnym wyłączeniu przy zbliżonej temperaturze wspiera przypisanie zysku batchingowi. Zastrzeżenie dotyczące wymiarów startowych opisano powyżej.

Zrzuty poziomu 8 obejrzano dla obu trybów: plansza, sprite'y, przezroczystości, HUD i kontrolki są renderowane. Animacje zostały uchwycone w różnych fazach, a margines wynika z różnego wymiaru startowego; nie twierdzimy, że klatki są identyczne piksel w piksel.

## Końcowy APK: wszystkie mapy i dotyk

`reports/all-levels-0.4.9`: po 25 sekund po potwierdzeniu ładowania i dźwięku na każdej mapie; bohater stoi, bez ochrony, zwykli przeciwnicy pozostają aktywni. Pierwszą partię 300 klatek pominięto. Wszystkie 14 map załadowało się z dźwiękiem, bez wykrytej awarii procesu. Poniżej zakresy średnich FPS kolejnych partii oraz najgorsze p95 czasu klatki w tych partiach. To pomiar pętli silnika, nie pomiar fizycznej prezentacji każdej klatki na ekranie.

| Poziom | FPS | p95 maks. (ms) | Partie po rozgrzaniu | Widok logiczny |
|---|---|---:|---:|---|
| 1 | 60,2 | 18 | 4 | 847×480 |
| 2 | 60,2 | 18 | 4 | 853×480 |
| 3 | 60,2–60,4 | 18 | 3 | 853×480 |
| 4 | 60,2 | 18 | 4 | 853×480 |
| 5 | 60,1–60,2 | 20 | 4 | 847×480 |
| 6 | 60,2–60,4 | 18 | 3 | 847×480 |
| 7 | 60,2 | 18 | 4 | 847×480 |
| 8 | 60,2 | 18 | 4 | 847×480 |
| 9 | 60,2 | 18 | 4 | 847×480 |
| 10 | 60,2 | 18 | 4 | 847×480 |
| 11 | 60,2 | 18 | 4 | 847×480 |
| 12 | 60,2–60,3 | 18 | 4 | 847×480 |
| 13 | 60,2 | 18 | 4 | 847×480 |
| 14 | 60,1–60,2 | 21 | 4 | 853×480 |

Na poziomach 5 i 14 czas klatki jest mniej równy mimo średniej około 60 FPS. Pierwsze partie zawierały pojedyncze większe przestoje, np. 113 ms na poziomie 6 i 129 ms na poziomie 10; rozgrzanie nie oznacza usunięcia wszystkich przycięć. Migawki PSS procesu wynosiły około 132–187 MiB, nie są pomiarem szczytowej pamięci ani całego kosztu GPU.

`reports/jump-touch-0.4.9`: sześć pomiarów zaliczonych, wysokość krótkiego skoku około 74 px, długiego 155 px. Zdarzenie w aplikacji → wybicie: 18–22 ms (wcześniejsza próba 0.4.8: 29–31 ms). To nie pełne opóźnienie ekranu dotykowego. Przesuwanie palca nie uruchamia obcej akcji; scenariusze ruchu ze skokiem, pauzy i powrotu z tła zakończone.

`reports/gameplay-perf-9-0.4.9`: 45 sekund powtarzanej sekwencji ruchu w obie strony, szabli, skoku, strzału i kucania na prawdziwym początku poziomu 9. Wykonano 54 komendy wejścia; odczytane położenie zmieniło się z x=1594 do x=1733 i z powrotem, więc nie polegamy wyłącznie na potwierdzeniach komend. Bez teleportów, ochrony lub dodanej amunicji; HP przed i po wynosiło 100. Pierwsza partia: 58,3 FPS, p95 20 ms, maksimum 67 ms; następne osiem: 60,0–60,3 FPS, p95 18 ms, maksima 18–23 ms. Test zaliczony, a oryginalny zapis i konfigurację przywrócono. To krótki fragment z ruchem i działaniami, nie pomiar całej mapy ani walki ze wszystkimi przeciwnikami.

APK: `dist/kapitan-pazur-0.4.9-debug-universal.apk`, wersja 0.4.9-dev (21), ARM64 i ARMv7. SHA-256: `60283884da15886c70844b20e35c9dd894166d79d83b4133be48173dedbb7812`. Kontrole obu ABI, segmentów 16 KiB ARM64, zipalign i podpisów v1/v2 zaliczone. Standardowa uwaga apksigner o metadanych Gradle w META-INF pozostaje. Brak danych komercyjnej gry w APK i paczce źródeł.

## English summary

The Android entry point explicitly selects GLES2, which disables batching by default in the pinned SDL version. Off/on/off runs on one APK measured map starts 8/9/13 at about 57/54/58 FPS without batching and about 60 FPS with batching; disabling it again reduced performance. The final APK reached about 60 FPS in warmed starts of all 14 maps, with sound and no detected crash. A 45-second level 9 movement/jump/attack sequence also reached 60.0–60.3 FPS after its first batch, without protection, teleporting or extra ammunition. Map 5/14 loop frame times remain less even and initial hitches remain. Touch tests passed. Image resolution, filtering, draw order, audio, simulation cadence and physics solver iterations are unchanged. This integrates SDL's existing queue, not a new renderer. Startup immersive-mode timing sometimes chooses a slightly different logical width, documented above; level 13 used matching dimensions. Short map-start measurements are separate from sustained whole-level performance.
