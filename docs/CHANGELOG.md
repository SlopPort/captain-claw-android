# Historia adaptacji

## 0.4.26 — import i podpis wydania / Import and signing

Przewijany ekran instalacji. Próby rzeczywistego anulowania selektora i pełnego
REZ na Androidzie 10/16, z przywracaniem danych. [Zakres](validation/IMPORT-FLOW-0.4.26.md).
Oddzielny, lokalny klucz wydania i blokowanie release bez konfiguracji podpisu;
klucz i hasło nigdy nie są częścią źródeł. [Podpis](RELEASE-SIGNING.md).
Audyt [drabin, krawędzi i wysokości](validation/TERRAIN-HEIGHTS-0.4.25.md) dotyczy
0.4.25. Sześć bibliotek debug pozostaje identycznych; nie zmieniano fizyki/balansu.

Scrollable installer; actual picker cancellation plus full-REZ stream tests on
Android 10/16. Separate local signing identity; release builds require explicit
signing files. This remains development work, not 1.0 or a complete campaign clear.

## 0.4.25 — dostępność ekranów i przygotowanie wydania

Własna ikona bez grafik oryginalnej gry, informacja o autorach narzędzi zapisów
w PL/EN oraz przewijanie tego ekranu. Brak dostępu do dolnego przycisku odtworzono
na małym emulatorze z czcionką 200%; po poprawce próba obu języków przeszła.
Jawne wyłączenie automatycznych kopii i transferu danych również dla nowszych
Androidów; ręczny eksport zapisów pozostaje dostępny. Diagnostyka dotyku odczytuje
sumę APK z urządzenia. Bounded retries of explicit exit teleports remain technical
fixtures, with the count recorded; they are not campaign evidence. Bez zmian
fizyki i balansu. Dokładne paczki, próby i ograniczenia: [raport](validation/READINESS-0.4.25.md).

Original icon, localized save-tool credits and scrollable save tools. The clipped
Back button was reproduced with large fonts on a small emulator and checked in
PL/EN after the fix. Explicit modern Android backup/transfer exclusions retain
the existing automatic-backup opt-out; manual save export remains. No gameplay
or native-engine changes. Runtime coverage and retained failures are in the report.

## 0.4.24 — pomiary platform i naturalny checkpoint

Opcjonalny odczyt ruchu platform i jednoczesny zwykły skok bez dodatkowego ciosu. Próby wejścia i przenoszenia na Redmi/Huawei. Naturalne dotarcie do pierwszego trwałego checkpointu i jego wczytanie przez menu z zachowaniem wyniku, żyć oraz amunicji. Cała kampania nadal nieukończona. [Pomiary](validation/PLATFORM-0.4.24.md), [naturalny zapis i wczytanie](validation/NATURAL-CHECKPOINT-0.4.24.md).

Opt-in platform observations and ordinary input scheduling; no physics changes. Real platform boarding passed on Redmi/Huawei. The first persistent checkpoint was reached naturally and reloaded through the normal menu with matching resources. The campaign remains incomplete.

## 0.4.23 — awaria wybuchu beczki

Naprawiono przedwczesny odczyt obszaru kolizji nowego wybuchu w diagnostyce. Awaria znaleziona w naturalnej próbie kampanii, odtworzona na starej wersji i sprawdzona po poprawce na obu telefonach. Obrażenia i rozmiar wybuchu bez zmian. [Raport](validation/POWDER-KEG-0.4.23.md).

Fixed a premature explosion-body bounds query in adaptation diagnostics, found during natural gameplay. Old-version reproduction and fixed-version checks are documented; damage and blast size are unchanged.

## 0.4.22 — kontrola konfiguracji przed importem

Przed podmianą danych sprawdzany jest XML konfiguracji: korzeń, zamknięcia znaczników, encje i limit rozmiaru. Komunikat PL/EN i zachowanie istniejących danych po odrzuceniu. Jedenaście błędnych przypadków odrzuconych na Huawei, Redmi z Androidem 16 i emulatorze Androida 5; dwie nieudane iteracje parsera zachowane w raportach. Czysta kompilacja obu ARM, próba jej parsera oraz skok i wyjścia na telefonach. [Wyniki](validation/CONFIG-IMPORT-0.4.22.md). Osobny długi pomiar 0.4.21 na Redmi dał 59,998 FPS w jednej ciężkiej scenie przez 20 minut; [ograniczenia i przycięcia](validation/SUSTAINED-REDMI-0.4.21.md).

## 0.4.21 — sprzątanie importu i Android 16

Porzucone pliki robocze importu są usuwane po poprawnym odzyskaniu danych przy starcie i po błędzie importu. Zachowanie kopii przy uszkodzonym dzienniku, 64 próby granic operacji oraz testy Huawei/Android 5. Aktualizacja Redmi z 0.4.3 zachowała zapisy i konfigurację; skok, wielodotyk i wyjścia dotykowe przeszły na Androidzie 16. [Import](validation/IMPORT-CLEANUP-0.4.21.md), [Redmi](validation/REDMI-0.4.21.md).

## 0.4.20 — rozdzielenie parowania od błędu trafienia

Diagnostyka zapisuje istniejący wynik losowania parowania i opór zdrowia, bez zmiany obrażeń ani dodatkowego losowania. Opcjonalne cichsze pomiary nie są reklamowane jako optymalizacja. Wszystkie 14 map wystartowało na Huawei bez flagi podglądu. [Wyniki i ograniczenia](validation/PARRY-PERF-0.4.20.md).

## 0.4.19 — dotykowe ustawienia dźwięku

Suwaki głośności obsługują przeciąganie i anulowanie dotyku, zapisują ustawienia atomowo i zachowują wybrany kanał po przesunięciu palca między wierszami. Wyciszenie nie włącza ponownie nieobsługiwanych osobnych kontrolek głosów i otoczenia. Próby PL/EN na Huawei Android 10 i emulatorze Androida 5, po 109 etykiet w każdym języku. [Zakres i sumy APK](validation/MENU-AUDIO-0.4.19.md).

## 0.4.18 — atomowy zapis postępu

Zapis punktu kontrolnego i ukończenia poziomu nie obcina starego pliku przed ukończeniem nowego. Wspólny pomocnik sprawdza zapis, synchronizację i podmianę; błąd pokazuje komunikat PL/EN. Serializacja importu zapisu między wątkami. Przeszły rzeczywisty punkt kontrolny/restart/wczytanie, przejście podsumowania oraz starty wszystkich 14 map. Mały eksperyment FPS odrzucono; nie jest reklamowany jako optymalizacja. [Dokładne APK, wyniki i ograniczenia](validation/ATOMIC-PROGRESS-0.4.18.md).

## 0.4.17 — przygotowanie każdego startu

Również bezpośrednio wznowiony ekran gry przygotowuje wsparcie silnika, język, odzyskiwanie importu i postęp poza wątkiem interfejsu. Atomowy pierwszy zapis i zachowanie kopii poprzedniego postępu przy powtórzeniu przerwanego importu. Czysta kompilacja obu architektur i próba jej APK na Huawei. [Wyniki](validation/STARTUP-0.4.17.md).

## 0.4.16 — menu PL/EN i zgodność 16 KB

Własne napisy menu, pomoc i autorstwo PL/EN, bez dołączania komercyjnych angielskich grafik. Wyłączenie odziedziczonych przycisków bez działającej funkcji, czytelne pola dotyku i przenoszenie ustawień ponad menu. Czcionki współdzielone podczas jednego wczytywania. Huawei: nawigacja PL/EN, skok, podsumowanie i powrót z końca gry. Osobny emulator Androida 15 ze stronami 16 KB: menu PL/EN, natywna biblioteka, skok i przejście poziomu. To nie pełna kampania ani potwierdzenie 60 FPS. [Dokładne APK i ograniczenia](validation/MENU-LANGUAGE-0.4.16.md).

## 0.4.9 — grupowanie rysowania SDL

Jawne włączenie kolejki rysowania, domyślnie wyłączanej przez SDL po wybraniu sterownika GLES2. W porównaniu wyłączone/włączone/wyłączone na jednym APK początki poziomów 8/9/13 osiągnęły około 60 FPS zamiast około 57/54/58 FPS. Bez zmian rozdzielczości, filtrowania, fizyki i tempa logiki. Lokalny opt-out pozwala wrócić do poprzedniej ścieżki przy problemie sterownika. [Metoda, wyniki i ograniczenia](validation/FPS-0.4.9.md).

## 0.4.8 — funkcje Claw Web, optymalizacja i audyt

Bezpośredni REZ, eksport/import zapisów z kopią poprzedniego postępu, opcjonalne wibracje oraz węższy preload, z przypisaniem inspiracji/adaptacji Claw Web (Arthur Boss i współtwórcy). ThinLTO/O3, cache wyszukiwania komponentów i pominięcie odziedziczonych pustych aktualizacji; bez obniżenia obrazu i solvera. Reset zegara po ładowaniu, pomiary tylko aktywnej gry. Audyt dołu drabiny i czasu życia kontaktu, poprawka diagnostycznego zegara Box2D oraz zgodności odbiornika USB nowszych Androidów. [Raport i pozostałe ograniczenia](validation/PORT-0.4.8.md); pełne naturalne przejście nadal niepotwierdzone.

## 0.4.7 — zapis dźwięku i FPS

Naprawa pustego zapisu ustawień dźwięku na Androidzie, z zachowaniem pozostałej konfiguracji. Optymalizacja bibliotek natywnych w debug i cache grafiki gałki. Na Huawei P9 Lite w krótkiej stacjonarnej próbie poziom 1: około 23 → 60 FPS, poziom 13: około 18 → 43 FPS. Bez obniżania rozdzielczości. Zakres audytu komentarzy, nierozwiązane problemy i ograniczenia pomiaru: `validation/TODO-AUDIT.md`.

## 0.4.6 — drabiny i dostęp do ustawień pada

Zakończenie wspinania, gdy drabina nie sięga już ponad stopy; blokada ponownego zaczepiania przy trzymaniu góry na szczycie. PAD przeniesiony z licznika życia na dół ekranu. Menu Androida przyjmuje powtarzane kierunki góra/dół z pada, nadal bez powtarzania zatwierdzania. Szczegóły i granice porównania z oryginałem: `validation/LADDERS.md`.

## 0.4.5 — własne przypisania pada

Ekran przechwytywania fizycznych przycisków/spustów, zapis i przywracanie przypisań, osobne czynności w menu. Kolejka Java/JNI/SDL omija niejednoznaczne tłumaczenie przycisków urządzenia. Test potwierdził obrażenia szabli po przypisaniu L1; użytkownik następnie potwierdził dobre działanie.

## 0.4.4 — obsługa padów i uporządkowanie źródeł

SDL_GameControllerDB, obsługa podłączania i odłączania, martwa strefa, poprawki wejścia w pauzie i zamykania Androida, instrukcje instalacji PL/EN oraz lokalny projekt Git bez komercyjnych danych gry.

## 0.4.3 — dotyk i skok

Większe przyciski w łuku pod kciukiem, symbole akcji, utrzymanie palca na przypisanym przycisku, bezpośrednia obsługa zdarzeń, minimalne podtrzymanie krótkiego tapnięcia 110 ms oraz cache rysowania przycisków. Porównanie pomiarów jest w `validation/JUMP-TOUCH.md`.

## 0.4.2 — walka

Audyt 45 wariantów i 1415 rozmieszczeń. Przywrócenie 54 kameleonów poziomu 13; poprawki zdrowia, śmierci, kierunku patrolu, kontaktów pocisków i aktywnego ciała kucania. Zachowano informację o jednorazowej awarii kontaktu, której źródła nie ustalono.

## 0.4.1 — gałka i szeroki ekran

Gałka ośmiu kierunków z niezależnymi palcami; rozszerzanie widoku świata bez deformowania grafiki; kotwiczenie HUD i obsługa wyśrodkowanych menu.

## 0.4.0 — Omar i zakończenie

Dwufazowa walka, dialogi, kapitulacja, reset podejścia i własna inscenizacja końca gry; akrobatyka strażników i zanikanie kameleonów. To interpretacja w silniku, nie odtworzenie oryginalnego filmu.

## 0.3.x — uzupełnianie finału

Kolejne elementy poziomu 14: platformy, pułapki, wyrzutnie, gejzery, LavaHand i LavaMouth. Testy były kontrolowane i nie potwierdziły pełnego przejścia lub zgodności parametrów z Windows.

## 0.1–0.3 — podstawa Androida

Gradle/CMake/NDK, SDLActivity, ARM64/ARMv7, import danych, polskie PCX, sterowanie dotykowe, poprawki przenośności i audio, muzyka TiMidity/FreePats oraz profil dla skromniejszych urządzeń.
