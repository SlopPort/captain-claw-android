# Kapitan Pazur na Androida

[English README](README.en.md)

Natywna adaptacja [OpenClaw](https://github.com/pjasicek/OpenClaw) na Androida, z danymi dostarczanymi przez użytkownika. Silnik C++/SDL dla ARM64 i ARMv7, minimum API 21. Aktualna wersja rozwojowa: **0.4.21-dev**. Pełne wydanie 1.0 pozostaje w przygotowaniu.

**[Droga do 1.0 — po polsku i angielsku](docs/ROADMAP-1.0.md)** rozdziela wykonane prace, warunki wydania i potrzebne testy. Ostatnie poprawki zabezpieczają zapisy punktów kontrolnych i ukończenia poziomu oraz bezpośrednie wznowienie gry przez Androida. [Wyniki 0.4.18 i czyste budowanie](docs/validation/ATOMIC-PROGRESS-0.4.18.md), [start 0.4.17](docs/validation/STARTUP-0.4.17.md), [20 minut ciężkiej sceny](docs/validation/SUSTAINED-0.4.15.md).

**Język:** przed importem danych lub w **PAD → Język / Language** wybierz Polski albo English. Ustawienia, menu i nasza pomoc obsługują oba języki; napisy w grze zmienią się po jej ponownym uruchomieniu. Głosy, tła i oryginalne grafiki podsumowań zależą od danych użytkownika. [Menu PL/EN i testy 0.4.16](docs/validation/MENU-LANGUAGE-0.4.16.md).

Bieżące prace obejmują walki z Aquatisem i Marrowem, przechodzenie między mapami, dźwięki ataków i poprawki menu. [Wyniki i pozostałe warunki wydania](docs/validation/CAMPAIGN-1.0.md). Wcześniejsze [pomiary fizyki i drabin](docs/validation/FPS-0.4.11.md), [audyt zgłoszeń](docs/validation/BUG-AUDIT-2026-10-21.md) i [optymalizacja rysowania](docs/validation/FPS-0.4.9.md) opisują dokładny zakres sprawdzonych zmian.

Od 0.4.8 można wskazać sam pełny **CLAW.REZ** zamiast przygotowanego ZIP. Pod **PAD → Kopie zapisów i wibracje** są eksport/import postępu i opcjonalne wibracje. Funkcje inspirowane Claw Web (Arthur Boss i współtwórcy), z przypisaniem pochodzenia w [NOTICE](NOTICE.md). Instalacja z 168-bajtową atrapą REZ i luźnym folderem Assets nadal wymaga ZIP.

Gałka dotykowa, większe przyciski i regulowana wysokość skoku, szeroki widok planszy z zachowaniem proporcji, muzyka MIDI w APK, uzupełnienia poziomu 14 oraz walka z Omarem i inscenizacja zakończenia. Port korzysta z istniejącego silnika i rozgrywki OpenClaw.

**Zakres własnej pracy:** [różnice względem OpenClaw](docs/UPSTREAM-DIFF.md). Zmiany silnika są zapisane jako odtwarzalny patch do konkretnego commita; kod Androida i nowe komponenty są osobno w tym repozytorium.

## Instalacja dla gracza

**[Polski: instalacja krok po kroku](docs/INSTALL-PL.md)** · **[English: step-by-step installation](docs/INSTALL-EN.md)**

Gotowy APK instaluje aplikację. Dane z własnej kopii gry importuje się osobno jako pełny `CLAW.REZ` albo `game-data.zip`. Instrukcja wyjaśnia kopiowanie plików, instalowanie i najczęstsze problemy. Nie trzeba kompilować programu, jeśli ma się gotowy APK.

## Transparentność

Całą pracę nad adaptacją w tej sesji — kod, dokumentację, analizę i wykonanie testów automatycznych — wykonał agent LLM (OpenAI Codex), według wymagań i uwag człowieka. OpenClaw i biblioteki pozostają pracą ich autorów. [Ustalenia, ograniczenia i plan słabszego telefonu](docs/DEVELOPMENT-NOTES.md).

All adaptation work in this session was performed by an LLM coding agent (OpenAI Codex), guided by human requirements and feedback. Upstream work retains its original attribution. Controlled tests are not a completed natural playthrough.

## Budowanie

Zainstaluj JDK, SDK 35, Build Tools 35.0.0, NDK 27.2.12479018, CMake 3.22.1, Python 3.11+ i Git. Ustaw lokalizację SDK/JDK.

```sh
python tools/bootstrap.py
./gradlew '-Pabis=arm64-v8a,armeabi-v7a' :app:assembleDebug
```

Na Windows użyj `tools/build.ps1 -Abis 'arm64-v8a,armeabi-v7a'`. APK powstaje w `app/build/outputs/apk/debug/`. Szczegóły: [budowanie i własne dane](docs/BUILDING.md).

Repozytorium nie zawiera komercyjnych danych Claw. Własną instalację można spakować poleceniem:

```sh
python tools/pack_assets.py --game-root '/sciezka/do/wlasnej/instalacji'
```

Zainstaluj APK i wybierz przygotowany `build/game-data.zip` w aplikacji. Dane i zapis są przechowywane w katalogu aplikacji. Odinstalowanie usuwa dane aplikacji.

## Sterowanie dotykowe

**Pad:** dotknij przycisku **PAD** na dole, pośrodku ekranu, aby przypisać fizyczne przyciski do czynności. [Instrukcja PL/EN](docs/CONTROLLER.md). Domyślne nazwy Androida mogą różnić się od nadruków na padzie.

Gałka po lewej służy do ruchu, wspinania i kucania. Skok jest na dole po prawej; atak obok niego, strzał wyżej. Szybki tap daje użyteczny niski skok, dłuższe trzymanie zwiększa wysokość. BRON zmienia broń; PAUZA lub systemowy Wstecz otwiera menu.

## Stan i ograniczenia

Sprawdzono 45 wariantów zwykłych przeciwników, 1415 początkowych obiektów na 14 mapach, 16 typów atakujących pociskami z obu stron i 13 przypadków hitboxów. To kontrolowane scenariusze, nie pełne naturalne przejście gry. Balans i zakończenie nie mają pełnego porównania z wydaniem Windows.

Najnowsze próby kampanii wykonujemy na Huawei P9 Lite z Androidem 10 i 2 GB RAM; wersja 0.4.21 przeszła także próby dotyku, menu i startów wszystkich map na Redmi Note 8 z Androidem 16. Po optymalizacjach wiele scen osiąga około 60 FPS, ale gęsta scena poziomu 9 mierzyła około 57–59 FPS. Nie ma jeszcze dowodu stałych 60 FPS przez całą kampanię. Minimum API 21 i dwie architektury są ustawieniami kompilacji, a nie potwierdzeniem działania na wszystkich telefonach. [Zakres sprawdzonej zgodności](docs/validation/ANDROID-COMPATIBILITY.md).

Trwają końcowe prace nad kampanią. Pełne kontrolowane walki z Aquatisem i Marrowem oraz przejścia do następnych map przeszły testy; używają jawnych teleportów i ochrony bohatera. Nie oznacza to naturalnego przejścia wszystkich poziomów ani gotowej wersji 1.0. [Warunki wydania i wyniki](docs/validation/CAMPAIGN-1.0.md), [dźwięki ataków](docs/validation/ATTACK-AUDIO.md).

- [Dotyk i skok](docs/validation/JUMP-TOUCH.md)
- [Audyt walki](docs/validation/COMBAT-AUDIT.md)
- [Szeroki ekran](docs/validation/JOYSTICK-WIDESCREEN.md)
- [Finał](docs/validation/LEVEL14-FINALE.md)
- [Testowanie](docs/TESTING.md)
- [Zasady zmian](CONTRIBUTING.md)
- [Autorzy i licencje](NOTICE.md)

Kod adaptacji i OpenClaw: GPL-3.0, patrz [LICENSE.txt](LICENSE.txt). Biblioteki i bank instrumentów zachowują swoje licencje. Prawa do komercyjnych danych Claw pozostają przy ich właścicielach.

Przy rozpoznaniu instalacji użyto pomocniczo [REA](https://github.com/morluto/rea) oraz zestawień [awesome-game-decompilations](https://github.com/CharlotteCross1998/awesome-game-decompilations), [open-source-games](https://github.com/bobeff/open-source-games), [awesome-reverse-engineering](https://github.com/morluto/awesome-reverse-engineering) i tematów android-ports/android-reverse. REA nie jest zależnością gry.

Nowe: [dotykowe suwaki dźwięku i próby PL/EN na Huawei](docs/validation/MENU-AUDIO-0.4.19.md), [180 kontrolowanych prób walki](docs/validation/VERTICAL-45-0.4.18.md), [jawne archiwum odrzuconych eksperymentów](experiments/README.md).

[0.4.21: odzyskiwanie miejsca po przerwanym imporcie](docs/validation/IMPORT-CLEANUP-0.4.21.md) i [rzeczywiste próby Redmi z Androidem 16](docs/validation/REDMI-0.4.21.md).
