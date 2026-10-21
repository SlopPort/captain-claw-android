# 0.4.8 — integracja funkcji, wydajność i audyt

Praca i testy wykonane przez LLM OpenAI Codex, 2026-10-20/21, z wymaganiami i sprzętem człowieka. To wersja testowa. Nie potwierdzono naturalnego przejścia całej gry ani 60 FPS we wszystkich sytuacjach.

## Pochodzenie funkcji

Punkt odniesienia: Claw Web, Arthur Boss i współtwórcy, commit `e723d3d48b5ba2cc723751209954cfc46c82d202`, GPLv3. [Porównanie źródeł](CLAW-WEB-COMPARISON.md) opisuje stan przed integracją.

- Bezpośredni import REZ i eksport/import postępu: przejęty pomysł przepływu użytkownika; nowe implementacje Androida wykorzystują systemowy wybór dokumentu i nasz format SAVES.XML. Nie skopiowano warstwy IndexedDB/localStorage ani nie zadeklarowano zgodności z ich JSON.
- Wibracje: adaptacja pomysłu warstwy zdarzeń/presetów HapticFeedback. Nowe wyjście przez SDL rumble i Android Vibrator. Skok, lądowanie, atak/strzał i otrzymanie obrażeń; opcja domyślnie wyłączona. Nie przeniesiono wszystkich ich wzorców kroków, eksplozji czy interfejsu.
- Węższy preload menu/fontów: adaptacja podejścia ich BaseGameApp. Zasoby rozgrywki nadal obsługuje odziedziczony cache OpenClaw. Nie przenoszono ich całego renderera WebGL lub dźwięku przeglądarkowego.

Autorstwo i rewizja są zapisane w NOTICE.md, komentarzach źródeł, ekranie narzędzi zapisów i licencjach APK. Oryginalne grafiki/dźwięki gry nie są dołączane przez te funkcje.

## Instalacja i zapisy

APK zawiera wsparcie XML i własne neutralne obrazy pomocnicze. Font konsoli jest kopiowany z fontów telefonu do lokalnego katalogu; nie rozprowadzamy nieustalonej licencji fontu z upstreamu. Użytkownik wskazuje pełny CLAW.REZ lub dotychczasowy game-data.zip. Lokalny CrazyHook ma REZ wielkości 168 bajtów oraz luźne Assets — dla takiego układu nadal potrzebny jest przygotowany ZIP.

Eksport/import zapisów jest dostępny pod PAD → Kopie zapisów i wibracje. Parser ogranicza rozmiar, numery poziomów/checkpointów, pola i wartości oraz odrzuca deklaracje DOCTYPE. Import jest przygotowywany do następnego uruchomienia silnika, z zachowaniem poprzedniego SAVES.XML jako SAVES.before-import.xml. Zapis przez plik tymczasowy i podmianę. Nie importujemy zapisów Windows ani JSON Claw Web.

`PortFeaturesTest` na Androidzie zaliczył: odczyt/ponowny zapis, zastosowanie oczekującego importu, zachowanie kopii i poprzedniego postępu przy błędnym imporcie, odrzucenie nieprawidłowego REZ, zawartość pakietu wsparcia i dostępność systemowego fontu. Testuje rzeczywiste klasy Java i izolowany katalog, nie ręczną interakcję z systemowym selektorem dokumentów.

`tools/direct_rez_runtime_smoke.py`: pełny REZ użytkownika wraz ze wsparciem wyjętym z APK uruchomił mapy 1 i 14 z dźwiękiem. Próba użycia 168-bajtowej atrapy zatrzymała się przed uruchomieniem silnika; następnie poprawiono dane testowe i komunikat błędu. Wszystkie dane telefonu przywrócono. To próba formatu runtime, nie dowód kompletności każdego wydania CLAW.REZ.

## Optymalizacje bez obniżania obrazu

- ThinLTO i `-O3` domyślnie dla kodu natywnego. Asercje i symbole pozostają; bez fast-math, zmiany solvera, rozdzielczości lub częstotliwości animacji/AI. `-PnativeLto=OFF` umożliwia porównanie.
- Statyczne hasze nazw komponentów i usunięcie zbędnych kopii shared_ptr przy zwracaniu surowego wskaźnika.
- Lista aktualizowanych komponentów zachowuje kolejność ID z mapy. Pomija wyłącznie dokładne typy z odziedziczoną pustą VUpdate (pozycja, render, trigger i zdrowie). Sprawdzenie typu i typu wskaźnika do metody chroni aktualizujące podklasy i przyszłe nadpisania. Fizyka, zdarzenia triggerów, AI i animacje nadal działają normalnie.
- Nie powtarzamy Mix_SetDistance, jeśli jego skwantowana wartość się nie zmieniła. Nie wykazano istotnego osobnego zysku tej poprawki na poziomie 13.
- Zegar symulacji jest resetowany po przejściu z ładowania/pauzy do rozgrywki. Czas blokującego ładowania nie powinien stawać się pojedynczym wielkim krokiem fizyki ani aktualizacji timerów.
- Licznik FPS bierze tylko aktywną symulację; pauza i przestoje odradzania nie są dowodem 60 FPS rozgrywki. Dodano rozdzielenie czasu fizyki/aktorów/widoków oraz opcjonalny profiler komponentów (sam profiler zwiększa koszt, więc nie jest benchmarkiem).

Huawei P9 Lite / VNS-L21, LineageOS Android 10, około 2 GB RAM, 1920×1080, dotyk widoczny, muzyka i efekty 22050 Hz. `reports/all-levels-final-0.4.8/`: po 35 sekund na początkową scenę każdej mapy, nieruchomy bohater, bez ochrony. Zakresy poniżej pomijają pierwszą partię 300 klatek. To nie najgorsze miejsce każdej mapy, nie trasa gracza i nie gwarancja stabilności cieplnej.

| Poziom | FPS w kolejnych partiach aktywnych klatek |
|---|---|
| 1 | około 60 |
| 2 | około 60 |
| 3 | około 60 |
| 4 | 58–60 |
| 5 | około 60 |
| 6 | około 41 w tym przebiegu; w innych próbach 40–60, wynik niestabilny |
| 7 | około 60 |
| 8 | 56–58 |
| 9 | 53–56 |
| 10 | około 60 |
| 11 | około 60 |
| 12 | około 60 |
| 13 | 57–59 |
| 14 | około 60 |

Wcześniejsza scena poziomu 13 w 0.4.7 miała około 43 FPS. Po zmianie listy komponentów czas aktualizacji aktorów w tej scenie spadł z około 9,6 do 4,9 ms. Zmiany kompilacji, ładowania i zegara testowano etapami, ale tabela opisuje ich łączny wynik, nie indywidualny udział każdej poprawki.

Migawki PSS procesu w przebiegu wszystkich map: około 134–187 MiB. To migawki, nie maksimum użycia RAM; sterownik GPU i pamięć systemowa mają osobne koszty. Skrypt odczytuje dokładny PID także ze zbiorczego zestawienia tej wersji LineageOS.

Ponowna próba poziomu 6 na końcowym APK (`box2d-monotonic-0.4.8`, 40 sekund): pierwsza partia 55,6 FPS, kolejne 60,0–60,4 FPS, p95 18 ms, maksima 21–27 ms po pierwszej partii. PSS 194198 KiB. Poprawiony profiler Box2D raportuje prawidłowe wartości, np. collide 0,75 / solve 2,59 / TOI 0,93 ms. Ten korzystny przebieg nie usuwa wcześniejszej zmienności ani nie potwierdza całego poziomu w 60 FPS.

## Znalezione błędy i ograniczenia

- Dół drabiny: odtworzono dalsze schodzenie/animację i wciskanie w podłogę mimo kontaktu stóp z podłożem. Sam warunek zatrzymania nie wystarczył: stary wskaźnik kontaktu ze szczytem nie był czyszczony po EndContact. Kontakt Box2D może potem zostać zwolniony lub użyty ponownie. Pierwsze czyszczenie przed rozliczeniem podestu wywołało regresję: pozostał nadmiarowy kontakt stóp i zejście zamieniało się w spadanie. Ostateczna kolejność najpierw usuwa podest z listy kontaktów, a potem zeruje wskaźnik. `ladder-balanced-0.4.8` zaliczył szczyt, zejście, skoki, zatrzymanie na dole, ponowne wejście i obie krawędzie. Przy trzymaniu dołu stopy pozostają na y=1098 przy podłodze y=1100, bez dalszego wciskania w podłoże.
- Zegar diagnostyczny starego Box2D odejmował unsigned mikrosekundy; przy przejściu przez sekundę raportował ogromne wartości. Android używa teraz signed czasu monotonicznego. To poprawka pomiaru, nie reguł symulacji.
- Odbiornik USB przypiętego SDL nie określał wymaganej polityki eksportu w nowych Androidach. Dodano flagę dla API33+ i zachowano ścieżkę starszych wersji. Jest w osobnym odtwarzalnym patchu SDL; fizyczne USB nie zostało jeszcze sprawdzone.
- Lint: poprawiono dwie uwagi naszego UI i rzeczywisty problem odbiornika USB. Wąskie wyjątki dotyczą wyłącznie odziedziczonych plików SDL: uprawnienia nieużywanej ścieżki BLE Steam Controller/mikrofonu oraz podklasy wybierane przez warunki API26. Nie przyznano aplikacji dostępu do mikrofonu lub nowych uprawnień Bluetooth. Pozostałe ostrzeżenia obejmują m.in. teksty interfejsu i stare API; brak błędów lint nie jest dowodem pełnej zgodności urządzeń.
- Voice/Ambient w starym menu nadal nie ma kompletnej niezależnej obsługi; audyt 0.4.7 pozostaje aktualny.

## Rozgrywka: co rzeczywiście sprawdzono

- Wszystkie 14 map: ładowanie, dźwięk i brak wykrytej awarii procesu w krótkich próbach.
- 13 kontrolowanych kombinacji trafień i ponownego kontaktu: zaliczone po zmianach aktualizacji/clock. Nie zastępuje walki z każdym bossem.
- Drabina: szczyt rzeczywistej pierwszej drabiny poziomu 1, ponowna góra, zejście, skok z drabiny, wyjście bokiem i góra+skok. Dodatkowo izolowany dół drabiny i podłoga.
- Krawędzie: kontrolowany podest, wyjście z obu stron, opadanie, lądowanie na niższym podłożu i brak dodatkowego skoku w powietrzu. Teleporty/izolacja sceny są częścią testu; to nie naturalne przejście mapy. Nie zbadano wszystkich drabin, ruchomych platform, połączeń i geometrii każdego poziomu.
- Omar: rzeczywiste kontakty miecza/strzałów zmieniły HP 200→0, obie fazy, inscenizacja finału, podsumowanie i powrót do menu. Test używał teleportów, mocy, nieskończonej amunicji i ochrony gracza; nie edytował HP bossa. Nie jest dowodem normalnego pokonania finału z zasobami zebranymi po drodze.

**Pełne naturalne przejście 1→14 pozostaje niepotwierdzone.** Nie zastępujemy go teleportami, odblokowaniem poziomów ani samym załadowaniem map. Do zamknięcia pozostają trasy, wszystkie walki z bossami, śmierć/odrodzenie i checkpointy podczas normalnej gry oraz wszystkie warianty drabin/krawędzi. Podczas takiej próby trzeba zapisywać poziom, checkpoint i czynności prowadzące do blokady; każdy blokujący błąd wymaga osobnego odtworzenia i ponownego sprawdzenia trasy.

## Końcowy kandydat APK

`dist/kapitan-pazur-0.4.8-debug-universal.apk`, wersja 0.4.8-dev (20), ARM64 + ARMv7. SHA-256: `455b2ef12e2831ad74d87a571a1eb837eb06cffe8dd1af12b55a3e4b3d6cc526`. Jest to lokalna kompilacja deweloperska, bez oryginalnych danych gry.

- `ladder-balanced-0.4.8` i `ladder-real-balanced-0.4.8`: zaliczone próby izolowane oraz pierwsza drabina rzeczywistego poziomu 1.
- `combat-balanced-0.4.8`: 13/13 przypadków, w tym ponowny callback tego samego pocisku bez drugich obrażeń.
- `jump-touch-balanced-0.4.8`: sześć pomiarów zaliczonych, wznios krótkiego tapnięcia 72,9–74,1 px, długiego 155 px, opóźnienie zdarzenie→wybicie 29–31 ms. Pomiar wejścia lokalnego aplikacji, nie pełnego opóźnienia fizycznego ekranu. Próby ruchu z dotykiem, przesunięcia palca, pauzy i powrotu z tła zakończone.
- `omar-balanced-0.4.8`: po ostatecznej zmianie kontaktów ponownie zaliczono obie fazy (HP 200→0), finał, podsumowanie i menu. Nadal jest to jawnie kontrolowana próba z pomocą dla gracza.
- `features-balanced-0.4.8.txt`: ponowiony test na końcowym APK zaliczył import, kopię poprzedniego zapisu, ochronę przed błędnym importem, odrzucenie błędnego REZ i pakiet wsparcia.
- Kontrole ELF obu ABI, wyrównania 16 KiB ARM64, zipalign i podpisów v1/v2: zaliczone. Weryfikator podpisu zgłasza standardową uwagę o metadanych Gradle w META-INF.
- Oba patche nałożone na czyste kopie źródeł: zgodne z 42 zmienionymi plikami OpenClaw i jednym SDL, z normalizacją CRLF. Lint: 0 błędów, 33 ostrzeżenia; nie wszystkie ostrzeżenia usunięto.

## English summary

Claw Web inspired direct REZ import, save export/import, optional event haptics and narrower preloading, with explicit credits and GPLv3 provenance. Android uses its own file picker/storage and SAVES.XML validation/backup path, not Web JSON compatibility. Native optimization retains image resolution and physics solver settings. Most stationary map starts approach 60 FPS; levels 8/9/13 remain lower and level 6 varies substantially. No universal 60 FPS claim is made. Controlled collision, ladder/ledge and Omar/finale tests are separate from a natural full playthrough, which remains unverified. Original game content remains outside public sources/APK support assets.
