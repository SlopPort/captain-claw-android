# Historia adaptacji

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
