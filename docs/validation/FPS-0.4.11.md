# 0.4.11 — początkowy koszt fizyki i animacja po skoku

Pracę, kod i próby wykonał OpenAI Codex (LLM), 2026-10-21. Człowiek zgłasza zachowanie gry i udostępnia Huawei P9 Lite VNS-L21, 2 GB RAM, LineageOS / Android 10. Oryginalna fizyka pochodzi z OpenClaw i dołączonego Box2D autorstwa Erin Catto i współtwórców; modyfikacje są oznaczone w źródłach i zachowują ich licencje.

## Co wykazała diagnostyka

Na poziomie 9 pierwszy krok fizyki zajmował około 60–68 ms. Z tego około 46–57 ms przypadało poza właściwymi fazami Collide/Solve/TOI. Z analizy kodu Step wynika, że główną przyczyną jest przygotowanie początkowej partii możliwych kontaktów. Nie zastosowano rozgrzewania przez Step(0), nie przesuwano kontaktów do fazy ładowania i nie zmieniono solvera ani czasu symulacji.

Pierwszy eksperyment, odrzucanie niemożliwych par dopiero po przeszukaniu drzewa, nie wykazał przekonującej poprawy i został usunięty. Zachowane raporty `pair-filter-9-off-a`, `pair-filter-9-on`, `pair-filter-9-off-b` pokazują pierwsze kroki 59,66 / 57,96 / 65,16 ms. Pierwsze partie klatek miały maksima 73 / 78 / 82 ms. Gęsta scena także nie wykazała zysku. Część startów miała różne okna 847×480 i 853×480; nie traktujemy różnic w tych pomiarach jako przyspieszenia.

## Ostateczna zmiana

Podczas ładowania nowej mapy wszystkie aktywne proxy kolizji trafiają do pierwszej partii wyszukiwania. Każdy kontakt dopuszczany przez Box2D musi mieć przynajmniej jedno ciało dynamiczne — jest to istniejąca, bezwarunkowa reguła b2Body::ShouldCollide, poprzedzająca filtr użytkownika.

Jeśli partia zawiera **wszystkie odrębne aktywne proxy**, wystarczy przeszukać drzewo od końców dynamicznych: każda dopuszczalna para nadal zostanie znaleziona. Pozostałe pary i tak byłyby odrzucone. Oryginalne sortowanie par, tworzenie kontaktów, wywołania filtrów użytkownika i solver pozostają bez zmian. Zwykłe niepełne partie używają dotychczasowego wyszukiwania.

Warunek pełnej partii sprawdza posortowane, unikalne identyfikatory, z pominięciem wpisów po usuniętych proxy. Sama liczba wpisów nie wystarcza: wielokrotne dotknięcie jednego proxy nie oznacza, że wszystkie pozostałe zostały zgłoszone. Ogólna klasa broad-phase korzysta z opcjonalnej funkcji kwalifikującej początek zapytania; nie zależy od klas aktorów gry.

Plik diagnostyczny `physics-pairs-unfiltered` w katalogu danych gry przywraca dotychczasowy algorytm przy następnym uruchomieniu. `tools/gameplay_perf_smoke.py --pair-filter off|on` zarządza nim wyłącznie na czas próby i usuwa własny znacznik w sekcji przywracania; odmawia nadpisania istniejącego znacznika. Oba tryby można porównać w jednym APK.

## Test zgodności

`tests/box2d_pair_filter_test.cpp`, uruchamiany przez `tools/test_box2d_pair_filter.ps1` z hostowym g++ MSYS2 UCRT64 15.1: dwa światy, włączony/wyłączony wariant, 600 kroków z różnym dt i solverem 10/8. Wynik: identyczne pozycje, kąty, prędkości, uśpienie, liczba kontaktów, liczba wywołań filtra i kolejność 7003 wywołań Begin/End/PreSolve/PostSolve.

Scena zawiera połączone kafle statyczne, sensory, platformę kinematyczną, pocisk, połączenie blokujące kolizję, zmiany typu ciał, dodawanie/usuwanie fixture i ciała, aktywowanie/wyłączanie oraz zmianę masek. Tysiąc powtórzonych zgłoszeń jednego proxy sprawdza, że optymalizacja nie uznaje niepełnej partii za kompletną. To test przypiętej biblioteki Box2D na komputerze; próby urządzenia opisujemy oddzielnie. Nie dowodzi zgodności całej gry z oryginałem Windows.

## Pomiar urządzenia: ten sam APK, wyłączone/włączone/wyłączone

Raporty `query-subset-9-off-a`, `query-subset-9-on`, `query-subset-9-off-b`. Każdy to świeży proces, start rzeczywistego poziomu 9, 20 sekund obserwacji bez teleportacji, ochrony gracza i modyfikacji amunicji. Obraz w każdej próbie: początkowa powierzchnia 1800×1020, logicznie 847×480, po ukryciu pasków ekran 1920×1080. Nie zmieniano rozdzielczości ani filtrowania; muzyka i efekty pozostawały włączone.

| Pomiar | Wyłączone A | Włączone | Wyłączone B |
|---|---:|---:|---:|
| Pierwszy krok Box2D | 57,52 ms | 21,92 ms | 66,13 ms |
| Czas poza Collide/Solve/TOI | 46,41 ms | 10,22 ms | 55,24 ms |
| Najdłuższa klatka pierwszej partii | 72 ms | 38 ms | 83 ms |
| FPS kolejnych pełnych partii | 59,9–60,2 | 60,0–60,2 | 60,2 |
| Ciała / kontakty po pierwszym kroku | 3197 / 268 | 3197 / 268 | 3197 / 268 |

To wyraźna poprawa początkowego przycięcia, **bez wykazanego wzrostu stałego FPS**. 38 ms nadal przekracza budżet pojedynczej klatki 60 FPS. Kolejność A/B/A ogranicza pomylenie z rozgrzaniem zasobów; nie jest pełną kontrolą temperatury CPU ani obciążenia systemu. Nie obiecuje 60 FPS w całej grze.

## Starty wszystkich poziomów

`tools/level_boot_smoke.py --levels 1 2 3 4 5 6 7 8 9 10 11 12 13 14 --frequency 22050 --effects-on --preview-level14 --hold-seconds 18 --report all-levels-0.4.11`: 14/14 uruchomień bez awarii, działająca muzyka i efekty, poprawne liczniki fizyki. Poziom 14 uruchamiany w trybie diagnostycznym, pozostałe normalnie. Bez teleportacji, ochrony gracza i wymuszania ataków. Przez telefon był udostępniany internet USB; nie zmieniano tetheringu, USB ani sieci.

FPS poniżej pomija pierwszą partię 300 klatek; zależnie od startu pozostało 1–3 pełnych partii, więc to krótka obserwacja. Maksimum obejmuje także start, żeby nie ukrywać przycięć. PSS jest pojedynczą próbką pamięci procesu, nie szczytem zużycia.

| Poziom | FPS po pierwszej partii | Największe p95 po starcie | Najdłuższa klatka całej próby | PSS MiB |
|---|---:|---:|---:|---:|
| 1 | 60,2 | 18 ms | 38 ms | 130,4 |
| 2 | 60,2 | 18 ms | 33 ms | 140,7 |
| 3 | 60,2 | 18 ms | 32 ms | 177,0 |
| 4 | 60,0–60,2 | 18 ms | 26 ms | 130,7 |
| 5 | 60,2 | 20 ms | 41 ms | 148,7 |
| 6 | 60,1 | 18 ms | 74 ms | 186,7 |
| 7 | 60,2 | 18 ms | 40 ms | 141,6 |
| 8 | 60,1–60,2 | 18 ms | 30 ms | 163,2 |
| 9 | 60,2 | 18 ms | 32 ms | 161,9 |
| 10 | 60,0–60,2 | 18 ms | 55 ms | 160,0 |
| 11 | 60,0–60,2 | 18 ms | 32 ms | 144,4 |
| 12 | 60,2 | 18 ms | 30 ms | 140,5 |
| 13 | 60,2 | 18 ms | 26 ms | 180,3 |
| 14 | 60,2 | 20 ms | 30 ms | 160,0 |

To nie test pełnych map ani naturalne przejście gry. Pozostają przycięcia, szczególnie 74 ms na początku poziomu 6 oraz 55 ms na poziomie 10. Nie przypisujemy ich bez dalszego profilowania konkretnej części silnika.

## Pierwsza drabina

Dziesięć krótkich prób góra/dół przy środku i bokach rzeczywistej pierwszej drabiny poziomu 1: 247 próbek, wszystkie zmiany stanu rejestrowane co klatkę, zero próbek animacji spadania. Sześć prób krótkiego zejścia i ruchu w bok: 200 próbek, również zero animacji spadania. Nie oznacza to, że zgłoszenie użytkownika zostało rozwiązane.

Druga seria miała porażkę dalszej próby chodzenia po szczycie: test przestawiał postać, zachowując stan wspinania z poprzedniej próby. Naprawiono przygotowanie testu — postać kończy wspinanie przed niezależnym sprawdzeniem chodzenia i skoku. Nie zmieniono produkcyjnego zachowania drabiny. Raporty `first-ladder-seam-trace` i `first-ladder-sideways-exits` zachowują pierwotne obserwacje i tę porażkę.

Po doprecyzowaniu użytkownika („góra i skok”) dodano macierz 12 krótkich/pełnych skoków ze szczytu i tuż pod nim, bez ruchu oraz z późniejszym ruchem w lewo/prawo. Odtworzono błąd: między innymi przy x≈1392, y≈4304 i x≈1492, y≈4312 postać stała na podłożu, lecz animacja `fall` trwała przez kolejne sekundy. Końcowe odczyty części tej pierwszej długiej próby nie przeszły przez przepełnienie pierścieniowego logu Androida; narzędzie zostało poprawione i zapisuje pełny strumień lokalnie zamiast traktować długość logu jako kursor. To nie awaria gry.

Osobna próba `first-ladder-precise-baseline` potwierdziła przyczynę: `ground=1`, `falling=0`, `jumping=0`, zerowa prędkość pozioma, ale resztkowa prędkość pionowa od około 2,45×10⁻⁷ do −1,37×10⁻⁷ m/s. PhysicsComponent sprawdzał prędkość float z Box2D względem DBL_EPSILON, czyli tolerancji double. Nie wywoływał więc VOnStopMoving mimo faktycznego ustania postaci.

Pierwsza poprawka z tolerancją `1e-5 m/s` nie przeszła pełnej macierzy: przy prawym narożniku wystąpiły powolne korekty pozycji z prędkością około −0,00048 m/s, a animacja nadal pozostawała błędna. Zachowano porażkę w `first-ladder-top-jump-fixed`; nie rozluźniano warunku zaliczenia testu.

Ostateczna poprawka zmienia wyłącznie tolerancję prędkości pionowej przy wywołaniu animacji zatrzymania na `0,01 m/s` (0,75 piksela/s przy przeliczniku silnika 75 px/m). Nadal wymaga kontaktu z podłożem i stanu zatrzymania. Nie zmienia prędkości fizycznej, sił, kształtu postaci, skoku ani filtrów kolizji. Nie ponawia zdarzenia lądowania, więc nie dodaje kolejnych dźwięków i wibracji. Wspinanie, obrażenia i śmierć zachowują istniejące warunki obsługi.

`first-ladder-top-jump-fixed2`: 12/12 scenariuszy, 555 próbek, zaliczone sprawdzenia szczytu, zejścia, skoku z drabiny i chodzenia. Zero przypadków animacji spadania trwającej co najmniej 300 ms przy podłożu, prędkości poniżej tolerancji i zmianie pozycji do 0,25 px. Cztery pojedyncze próbki zatrzymania wystąpiły przy normalnych przejściach; nie zaliczamy ich automatycznie jako błędu. Próby korzystają z teleportacji przygotowawczej i ochrony gracza, ale ze zwykłych wejść SDL i rzeczywistych kolizji mapy, nie z zastępczej drabiny.

Regresja końcowego APK: `combat-0.4.11-final`, 13/13 prób — pociski z obu stron, trzy wysokości, stanie/kucanie i powtórzone wywołanie trafienia tego samego pocisku. To kontrolowane próby kontaktów, nie audyt zachowania każdego przeciwnika na wszystkich schodach. Balans i geometria hitboxów pozostały bez zmian.

Pełna seria startów 14 map i porównanie A/B/A używały tego samego końcowego algorytmu Box2D, przed ostatnią poprawką wyboru animacji. Końcowy APK osobno przeszedł powyższą macierz drabiny i regresję kontaktów. Nie przedstawiamy wcześniejszego APK pomiarowego jako identycznego pliku binarnego z późniejszą poprawką animacji.

## Końcowy APK i ograniczenia

`dist/kapitan-pazur-0.4.11-debug-universal.apk`, versionCode 23, SHA-256 `530237efc559b76f99b1f5ac0bcd60cdf0317d9aeabcfb2e6bac5e1f6cc34c13`.

- ARM64 i ARMv7 zbudowane poprawnie; sprawdzone ABI, ARM64 ELF 16 KiB, zipalign oraz podpis v1/v2. Oba patche stosują się na czystych kopiach przypiętych źródeł i odpowiadają drzewom roboczym po normalizacji CRLF.
- `jump-touch-0.4.11-final`: 6/6 prób, pojedynczy skok po naciśnięciu, krótki skok 70,6–73,5 px, pełny 154,3–155 px, zdarzenie aplikacji → wybicie 16–20 ms. Wielodotyk, puszczanie przycisków, zmiana fokusu i brak przypadkowego ataku/strzału po przesunięciu palca: zaliczone. To nie pomiar fizycznego opóźnienia ekranu.
- `game-over-touch-0.4.11-final`: rzeczywista ostatnia śmierć → ekran końca gry → dotyk → menu: zaliczone.
- `dense-9-0.4.11-final`: kontrolowana teleportacja do (11027,5500), ochrona gracza, obserwacja bez ataków i zmiany amunicji przez 25 s. Pierwsza partia 55,4 FPS / max 47 ms; kolejne 56,9–58,8 FPS, p95 19–20 ms, maksima 21–23 ms. **Ta gęsta scena nadal nie osiąga stałych 60 FPS.** Nie deklarujemy poprawy jej stałego FPS.
- Wszystkie próby przywróciły konfigurację i postęp; testowe znaczniki oraz skrzynki poleceń zostały usunięte. Nie przełączano USB, tetheringu, Bluetooth ani sieci. Zasoby gry i prywatne raporty pozostały poza repozytorium i archiwum źródeł.

Następne otwarte prace: koszt gęstszych scen, pozostałe przycięcia, zachowania walki na schodach i dalszy audyt drabin/krawędzi. Nie potwierdzono naturalnego przejścia kampanii ani zgodności każdej sytuacji z oryginałem Windows.

## English

This work and its tests were performed by OpenAI Codex, an LLM. The first experimental per-pair rejection did not demonstrate a useful gain and was removed. The final algorithm optimizes complete broad-phase update batches: if every active proxy is present, querying from dynamic endpoints still finds every permitted contact. Partial batches retain the original algorithm. Unique proxy IDs, including duplicate/removal handling, determine whether a batch is complete. Solver settings, simulation cadence and image quality are unchanged.

The host comparison passed 600 steps with identical trajectories, contact counts, filter calls and 7003 ordered contact callbacks, including sensors, joints, type/fixture/filter changes and duplicate touches. This is separate from device performance measurements. Initial ladder checks did not reproduce the animation issue; after the user specified a jump near the top, the jump matrix did reproduce it. Tiny residual float velocities prevented a double-epsilon stop check from restoring the standing animation. The correction uses a subpixel tolerance only for that animation callback; physical velocity and collisions are unchanged. Natural completion of the entire game and 60 FPS in every situation remain unverified.

On Huawei, the same-APK off/on/off comparison measured the first level-nine physics step at 57.52 / 21.92 / 66.13 ms, with identical body/contact counts and viewport sizes. The first batch's longest frame was 72 / 38 / 83 ms. This improves the initial hitch, not sustained FPS. All fourteen map starts loaded with working audio and no crashes; subsequent short batches were around 60 FPS. Startup hitches of up to 74 ms remain. These are spawn observations, not whole-map benchmarks or a full playthrough.

The final APK passed twelve ladder-top jump scenarios (555 samples, no grounded stationary fall animation lasting 300 ms), thirteen projectile/contact checks, six touch/jump cases and Game Over touch confirmation. An earlier animation tolerance failed one corner case; that failed report is retained. The final tolerance is 0.01 m/s, below one pixel per second, and only selects the stop animation without changing physical motion. The denser level-nine scene still measured 56.9–58.8 FPS after its initial batch. Config and saves were restored; USB tethering and network settings were untouched. The final animation fix followed the full map-start run, so that earlier performance APK is explicitly distinguished from the final binary.
