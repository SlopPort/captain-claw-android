# Kapitan Pazur na Androida

Natywna adaptacja [OpenClaw](https://github.com/pjasicek/OpenClaw) na Androida, z polskimi zasobami dostarczanymi przez użytkownika. Silnik C++/SDL budowany dla ARM64 i ARMv7. Aktualna podstawa: 0.4.3-dev, minimum API 21.

Gałka dotykowa, większe przyciski i regulowana wysokość skoku, szeroki widok planszy z zachowaniem proporcji, muzyka MIDI w APK, uzupełnienia poziomu 14 oraz walka z Omarem i inscenizacja zakończenia. Port korzysta z istniejącego silnika i rozgrywki OpenClaw.

**Zakres własnej pracy:** [różnice względem OpenClaw](docs/UPSTREAM-DIFF.md). Zmiany silnika są zapisane jako odtwarzalny patch do konkretnego commita; kod Androida i nowe komponenty są osobno w tym repozytorium.

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

Gałka po lewej służy do ruchu, wspinania i kucania. Skok jest na dole po prawej; atak obok niego, strzał wyżej. Szybki tap daje użyteczny niski skok, dłuższe trzymanie zwiększa wysokość. BRON zmienia broń; PAUZA lub systemowy Wstecz otwiera menu.

## Stan i ograniczenia

Sprawdzono 45 wariantów zwykłych przeciwników, 1415 początkowych obiektów na 14 mapach, 16 typów atakujących pociskami z obu stron i 13 przypadków hitboxów. To kontrolowane scenariusze, nie pełne naturalne przejście gry. Balans i zakończenie nie mają pełnego porównania z wydaniem Windows.

Próby sprzętowe wykonano na Redmi Note 8 z Androidem 16. API 21 i dwie architektury są ustawieniami kompilacji; nie potwierdzają działania na każdym starszym Androidzie. Poziom 13 nadal ma spadek do około 54 FPS na tym telefonie, mimo około 60 FPS na poziomie 1 po rozgrzaniu. Obsługa padów jest kolejną, osobno weryfikowaną zmianą.

- [Dotyk i skok](docs/validation/JUMP-TOUCH.md)
- [Audyt walki](docs/validation/COMBAT-AUDIT.md)
- [Szeroki ekran](docs/validation/JOYSTICK-WIDESCREEN.md)
- [Finał](docs/validation/LEVEL14-FINALE.md)
- [Testowanie](docs/TESTING.md)
- [Zasady zmian](CONTRIBUTING.md)
- [Autorzy i licencje](NOTICE.md)

Kod adaptacji i OpenClaw: GPL-3.0, patrz [LICENSE.txt](LICENSE.txt). Biblioteki i bank instrumentów zachowują swoje licencje. Prawa do komercyjnych danych Claw pozostają przy ich właścicielach.

Przy rozpoznaniu instalacji użyto pomocniczo [REA](https://github.com/morluto/rea) oraz zestawień [awesome-game-decompilations](https://github.com/CharlotteCross1998/awesome-game-decompilations), [open-source-games](https://github.com/bobeff/open-source-games), [awesome-reverse-engineering](https://github.com/morluto/awesome-reverse-engineering) i tematów android-ports/android-reverse. REA nie jest zależnością gry.
