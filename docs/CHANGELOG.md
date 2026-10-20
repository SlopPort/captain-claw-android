# Historia adaptacji

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
