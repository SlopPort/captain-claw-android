# Co wykonano ponad OpenClaw

Aktualizacja 0.4.8: import pełnego REZ, walidowane kopie zapisów i opcjonalne wibracje mają inspirację w Claw Web (Arthur Boss i współautorzy), z odrębną implementacją integracji Androida. Dodano też ThinLTO, ograniczenie pustych aktualizacji komponentów, węższe ładowanie zasobów, reset zegara po ładowaniu oraz diagnostykę kosztów klatki. Autorstwo, wyniki i niepotwierdzone obszary opisuje [raport 0.4.8](validation/PORT-0.4.8.md). Implementację i narzędzia adaptacji wykonywał Codex (LLM), pod kierunkiem użytkownika.

Punkt odniesienia: [pjasicek/OpenClaw](https://github.com/pjasicek/OpenClaw), commit `5ee5740ca98377c76b13b50c84f610b0066a4717`. Nie jest to gra napisana od zera. Istniejąca implementacja zapewnia silnik SDL/C++, libwap, fizykę Box2D, odczyt zasobów, bohatera, większość zwykłej AI, menu i znaczną część rozgrywki.

| Obszar | Praca tej adaptacji | Gdzie sprawdzić |
|---|---|---|
| Android | Aktualny projekt Gradle/CMake/NDK, ARM64 i ARMv7, API 21, wyrównanie 16 KB, SDLActivity, dane w katalogu aplikacji i import ZIP przez systemowy selektor | `app/`, `CMakeLists.txt`, `native/android_main.cpp` |
| Grafika i polskie zasoby | Obsługa indeksu przezroczystości PCX, poprawki przenośności formatów i ścieżek | `patches/openclaw-android.patch` |
| Muzyka i mała pamięć | TiMidity/FreePats w APK, zamienniki brakujących instrumentów, profil 22050 Hz/1024, mniejsza pamięć podręczna, poprawki własności bufora i obsługi audio | `tools/prepare_music_bank.py`, `profiles/`, patch |
| Dotyk | Własna gałka 8 kierunków, niezależne palce, większe przyciski, przechwycenie palca do puszczenia, natychmiastowa obsługa klawisza, minimalny impuls tapnięcia i cache rysowania | `native/TouchControls.cpp` |
| Ustawienia i FPS | Zapis zmian dźwięku przy przejściu Androida w tło; optymalizacja kompilacji bibliotek i cache gałki; pomiary faz klatki | patch, `CMakeLists.txt`, `docs/validation/TODO-AUDIT.md` |
| Drabiny i menu | Zakończenie wspinania na szczycie, blokada ponownego zaczepienia przy trzymaniu góry oraz przyjmowanie powtarzanych kierunków menu Androida | patch, `docs/validation/LADDERS.md` |
| Pad — w walidacji | Obsługa zdarzeń SDL, martwa strefa, mapowanie działań/menu, podłączanie i odłączanie, wspólne posiadanie klawiszy z dotykiem; Androidowe mapowania z SDL_GameControllerDB | `native/GamepadControls.cpp`, `native/PlatformInput.cpp`, `docs/validation/GAMEPAD.md` |
| Szeroki ekran | Więcej świata przy stałej wysokości 480, bez deformowania grafiki; kotwiczenie HUD, obsługa współrzędnych menu i podsumowania | patch oraz `native/TouchControls.cpp` |
| Poziom 14 | Prototypy/metadane oraz brakujące elementy finału: platformy, kolce, wyrzutnie, gejzery, LavaHand, LavaMouth, kameleony i strażnicy | `asset-overrides/`, `native/LavaGeyserComponent.cpp`, patch |
| Omar i zakończenie | Własna dwufazowa walka, dialogi, reset podejścia, kapitulacja i inscenizacja zakończenia z istniejących grafik gry | `native/OmarEncounterComponent.cpp` |
| Aquatis i Marrow | Nowa arena macek, dynamitu i stalaktytów; uzupełnienie pustych metod papugi, mostów i przenoszenia Marrowa. Nowe parametry wymagają porównania z oryginałem | `native/AquatisArena.cpp`, patch, `docs/validation/AQUATIS-ARENA.md`, `docs/validation/MARROW-ENCOUNTER.md` |
| Aktualizacja i menu | Atomowa aktualizacja własnego pakietu XML; obsługa dotyku na wynikach, pomijanie brakującego opcjonalnego WAV, własne plansze autorów i kontrola kompletności PNG | `app/.../EngineSupport.java`, `tools/prepare_import_support.py`, `tools/credits_png.py`, patch |
| Dźwięki ataków | Pięć brakujących przypisań do istniejących nagrań oraz pomiar rzeczywistego sygnału miksera bez nagrywania dźwięku | `asset-overrides/`, `native/AudioProbe.cpp`, `docs/validation/ATTACK-AUDIO.md` |
| Zwykli przeciwnicy | Przywrócenie 54 kameleonów poziomu 13, kierunek patrolowania, zdrowie/śmierć, jednokrotne obrażenia od pocisku, wyłączenie obrażeń czujnika stóp i poprawne aktywne granice kucania | `asset-overrides/`, patch |
| Narzędzia i dowody | Przypięte źródła, bootstrap, pakowanie własnych danych, kontrola ABI/ELF, inwentaryzacja 45 wariantów/1415 rozmieszczeń i testy na telefonie | `sources.lock.json`, `tools/`, `tests/`, `app/src/androidTest/` |

Własne komponenty są podłączane przez patch do fabryki aktorów i pętli zdarzeń OpenClaw. Patch jest pełnym zapisem zmian względem powyższego commita; można go odtworzyć `tools/export_patch.py` i sprawdzić `git apply --reverse --check` w drzewie silnika. Biblioteki SDL i Box2D nie są naszymi nowymi implementacjami.

Stan uporządkowanej podstawy 0.4.3: patch zmienia 34 pliki silnika (572 dodane i 45 usuniętych linii), a poza nim jest 11 nowych plików natywnych oraz 17 plików XML z lokalnymi uzupełnieniami. Dodatkowo są źródła aplikacji Android, testy, narzędzia i konfiguracja budowania. Szczegóły zapisano w `docs/upstream-diff-statistics.json`. Liczby pokazują zakres źródeł, nie są miarą kompletności ani zgodności gry.

## Granice wykonanej pracy

Zakończenie jest inscenizacją w silniku, nie odtworzeniem oryginalnego filmu. Parametry nowych elementów finału i balans nie mają pełnego porównania z Windows. CrazyHook DLL/FFI i adresy x86 nie są wykonywane przez port. Testy kontrolowane i odczyt wszystkich obiektów nie zastępują naturalnego przejścia wszystkich map. Jednorazowa awaria kontaktu pocisku poziomu 7 jest zachowana w raporcie audytu; po dodaniu kontroli rejestracji nie powtórzyła się w końcowych próbach, ale jej źródła nie ustalono jednoznacznie.

Obsługa padów jest osobną zmianą po uporządkowaniu podstawy 0.4.3. Aktualny zakres i niewykonane jeszcze sprawdzenia zapisano w `docs/validation/GAMEPAD.md`.
