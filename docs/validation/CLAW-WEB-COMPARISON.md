# Porównanie z Claw Web

Data: 2026-10-20. Audyt źródeł wykonany przez LLM (Codex). Nasz stan: `f376b10` / 0.4.7-dev. Claw Web: [`e723d3d48b5ba2cc723751209954cfc46c82d202`](https://github.com/arthurboss/claw-web/tree/e723d3d48b5ba2cc723751209954cfc46c82d202). Wspólny punkt odniesienia: OpenClaw `5ee5740ca98377c76b13b50c84f610b0066a4717`, obecny w historii obu drzew.

## Wniosek

Nie znaleziono w tej rewizji gotowej implementacji finałowego poziomu, która zastępowałaby nasze uzupełnienia. Deklaracja README „Full Game: All 14 levels” nie ma pokrycia w sprawdzonych źródłach. Claw Web ma natomiast wartościową, rozbudowaną integrację przeglądarkową, wygodniejszy import oryginalnego REZ i funkcje zapisu oraz wibracji, których u nas nie ma. Część funkcji powstała równolegle: szeroki ekran, gałka dotykowa, pad. To wspólne cele, nie dowód identycznej implementacji lub zbędności całej pracy Androidowej.

Przegląd obejmuje kod i różnice względem wspólnej bazy. Nie uruchomiono ich buildu, nie zmierzono go na Huawei i nie przeprowadzono pełnego przejścia. Nie twierdzimy, że nasza wersja jest już w pełni ukończona ani że jest szybsza od Claw Web.

## Sprawdzone różnice

| Obszar | Claw Web w sprawdzonej rewizji | Nasz port 0.4.7 |
|---|---|---|
| Platforma | WebAssembly, HTML/JS, instalowalna PWA, service worker i obsługa offline | Natywny APK, Gradle/NDK, ARM64 + ARMv7, importer systemowy Androida |
| Poziom 14 | Brak `LEVEL_METADATA/LEVEL14.XML`; jedyny śledzony zasób ścieżki LEVEL14 to ekran ładowania. Brak komponentu Omara i naszych nowych prototypów | Metadane, platformy i pułapki, gejzery, LavaHand/LavaMouth, TigerGuard i Chameleon, własny Omar oraz inscenizacja finału. Zgodność z oryginałem i pełne przejście nadal niepotwierdzone |
| Poziom 13 | `Chameleon` mapowany na `ActorPrototype_Null` | Przywrócone 54 rozmieszczenia kameleonów, obsługa zanikania |
| Trafienia i zdrowie | Zmiany względem bazy w HealthComponent i ProjectileAIComponent dodają głównie wibracje. ClawPhysics ma implementację SetVelocity; brak naszych poprawek kontaktów i aktywnego ciała kucania | Poprawki HP/śmierci, jednokrotnego kontaktu pocisku, czujnika stóp i granic kucania; 13 prób regresji na Huawei zaliczonych |
| Drabiny | PhysicsComponent różni się od bazy tylko progiem lądowania `>2` → `>0`; brak naszej blokady ponownego wspinania na szczycie | Zakończenie wspinania, blokada ponownego zaczepienia; test pierwszej drabiny poziomu 1 zaliczony |
| Gałka i przyciski | HTML/CSS, Pointer Events, przechwytywanie palca, gałka lub krzyżak, wibracje, dopasowanie do ekranu; JS wysyła KeyboardEvents | SDL, gałka 8 kierunków, wielodotyk, niezależna własność klawiszy z padem, minimalny impuls skoku 110 ms, cache tekstur |
| Krótki skok | `setupHoldButton` puszcza klawisz po pointerup/cancel; w tej ścieżce nie znaleziono minimalnego podtrzymania jak u nas | Przystosowanie krótkiego tapnięcia; na Huawei około 74 px i jeden skok na przytrzymanie, pomiar silnika 28–30 ms |
| Pad | Browser Gamepad API, obsługa połączeń, stałe przypisania w C++/JS, wibracje zdarzeń rozgrywki | SDL_GameControllerDB, natywne kody Androida, własne przypisania i ekran ich przechwytywania, focus/hotplug; fizyczny GameSir sprawdzany z użytkownikiem |
| Wibracje | Osobna warstwa HapticFeedback, zdarzenia obrażeń, eksplozji, kroków i lądowania | Brak własnej implementacji wibracji — przewaga funkcjonalna Claw Web |
| Szeroki ekran | Obsługa widescreen, ustawienia wyświetlania i układ przeglądarki | Więcej świata bez deformacji sprite'ów, kotwiczenie HUD i menu; rozwiązywane równolegle |
| Dane gry | Użytkownik wskazuje bezpośrednio `CLAW.REZ`, przechowywany w IndexedDB | Użytkownik wskazuje przygotowany `game-data.zip`; wygoda przygotowania danych słabsza niż bezpośredni REZ |
| Zapisy | Postęp w localStorage, import/eksport JSON i reset z menu | Plik SAVES.XML w katalogu aplikacji; brak równie wygodnego interfejsu eksportu/importu postępu |
| Zapis ustawień dźwięku | C++ SaveGameOptions nadal zawiera stub; nie jest to dowód, że każda konfiguracja przeglądarki jest tracona | Android zapisuje aktywność i głośności w tle/przy zamykaniu; test ponownego uruchomienia i zachowania innych pól zaliczony |
| Ładowanie | Węższy preload menu/fontów, metadane ładowane na żądanie, infrastruktura cache/offline przeglądarki | Nadal szerszy preload CLAW/GAME/STATES i wcześniejsze ładowanie metadanych; kandydat do dalszej optymalizacji startu |
| FPS | Nie mierzono na tym samym telefonie; liczba zmian renderera nie stanowi dowodu przewagi wydajności | Krótkie stacjonarne próby Huawei: poziom 1 około 60 FPS, poziom 13 około 43 FPS; brak pełnego benchmarku gry |

## Dlaczego „14 poziomów” nie wystarcza

1. [README](https://github.com/arthurboss/claw-web/blob/e723d3d48b5ba2cc723751209954cfc46c82d202/README.md) deklaruje wszystkie 14 poziomów.
2. [Katalog metadanych](https://github.com/arthurboss/claw-web/tree/e723d3d48b5ba2cc723751209954cfc46c82d202/Build_Release/ASSETS/LEVEL_METADATA) zawiera poziomy 1–13, bez 14.
3. [BaseGameApp.cpp](https://github.com/arthurboss/claw-web/blob/e723d3d48b5ba2cc723751209954cfc46c82d202/OpenClaw/Engine/GameApp/BaseGameApp.cpp#L1423) buduje ścieżkę `/LEVEL_METADATA/LEVEL<n>.XML`; brak pliku kończy się `false`, a GetLevelMetadata zwraca NULL. Nie znaleziono zastępczej ścieżki generującej dane poziomu 14.
4. [build_wasm.sh](https://github.com/arthurboss/claw-web/blob/e723d3d48b5ba2cc723751209954cfc46c82d202/build_wasm.sh#L31) odbudowuje ASSETS.ZIP z tego katalogu źródłowego. Nie znaleziono śledzonego alternatywnego ZIP z pełnym poziomem.
5. [LEVEL13.XML](https://github.com/arthurboss/claw-web/blob/e723d3d48b5ba2cc723751209954cfc46c82d202/Build_Release/ASSETS/LEVEL_METADATA/LEVEL13.XML#L34) wyłącza kameleona przez ActorPrototype_Null.

Menu wyboru poziomu i grafika jego ładowania nie są implementacją jego przeciwników, pułapek i finału. Nie wykluczamy innego, nieopublikowanego stanu lub różnicy między wdrożoną stroną i tą rewizją źródeł.

## Co warto wykorzystać dalej

1. **Import samego CLAW.REZ.** Największe uproszczenie dla użytkownika. U nas wymagałoby zbudowania redystrybuowalnego pakietu wsparcia z pewnymi licencjami oraz zachowania polskich wariantów danych. Nie wolno po prostu dołączyć cudzego ASSETS.ZIP lub grafik gry bez sprawdzenia pochodzenia.
2. **Eksport/import postępu przez systemowy wybór pliku.** Dobry wzorzec funkcjonalny, ale kod EM_ASM/localStorage trzeba zastąpić mechanizmem Androida. Nie wymaga porzucania istniejących SAVES.XML.
3. **Węższy preload.** Porównać czasy zimnego startu, pamięć i przycięcia przy pierwszym użyciu zasobu. Ich BaseGameApp jest sensownym punktem odniesienia; opis „lazy loading” częściowo wykorzystuje już istniejący cache OpenClaw.
4. **Opcjonalne wibracje pada/telefonu.** Można wykorzystać organizację zdarzeń/presetów, a wyjście podłączyć przez SDL/Android. Domyślne ustawienie i koszt na słabym telefonie wymagają prób.
5. **Drobne poprawki rozgrywki do osobnego odtworzenia:** pozostawienie bohatera w pozycji śmierci po utracie ostatniego życia, SetVelocity zamiast assert oraz walidacja pustych akcji ataku. Nasza walidacja AI już istnieje i korzysta z pierwszego sensora, więc nie zastępujemy jej mechanicznie ich kontrolą indeksu.

Nie przeniesiono jeszcze żadnego z tych rozwiązań do produkcyjnego kodu w ramach tego porównania. Najpierw zidentyfikowano różnice; nie ma uzasadnienia dla automatycznej podmiany całego silnika.

## Co było wspólne, a co dodatkowe

- Oba projekty dziedziczą zdecydowaną większość silnika i rozgrywki z OpenClaw. Nie zaliczamy tego jako własnego dorobku.
- Widescreen, dotyk i pad mają odpowiedniki w obu projektach. Wcześniejsze porównanie mogło ograniczyć część równoległego projektowania i testów pomysłów; nie da się uczciwie wyliczyć zaoszczędzonego czasu bez wcześniejszej integracji.
- Nasz APK, obsługa cyklu życia Androida, import danych, przypisania GameSira, poprawki drabiny i walki, uzupełnienia poziomu 14 oraz testy na Huawei pozostają konkretną dodatkową pracą. Nie znaleziono ich odpowiedników w tej rewizji Claw Web.
- Ich PWA/offline, warstwa dźwięku przeglądarkowego, eksport zapisów, wibracje i wygoda bezpośredniego REZ są konkretną dodatkową pracą po ich stronie.

GPLv3 umożliwia współpracę kodu przy zachowaniu warunków licencji, informacji o autorach i zmianach. Nie daje automatycznie praw do oryginalnych zasobów gry. Ta notatka nie jest kompletnym audytem prawnym lub audytem wszystkich plików Claw Web.

## English summary

Static comparison against Claw Web commit e723d3d and our f376b10 found complementary work, not a finished Android replacement. Its README claims all 14 levels, but the checked source lacks level 14 metadata/Omar implementation and still disables level 13 chameleons. Our Android lifecycle, remapping, collision/ladder fixes and level 14 additions remain distinct; exact original-game equivalence and a complete playthrough remain unverified. Claw Web offers useful browser/PWA infrastructure, direct REZ import, save export/import, haptics and narrower startup preloading. Shared feature goals include touch controls, widescreen and gamepads. No same-device performance comparison or upstream code integration was performed during this audit.
