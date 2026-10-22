# Budowanie

[English](BUILDING.en.md)

Sprawdzone narzędzia: pełny JDK 17 lub nowszy (np. z Android Studio), Gradle 8.10.2, Android SDK 35 / Build Tools 35.0.0, NDK 27.2.12479018, CMake 3.22.1, Python 3.11 lub nowszy i Git. Pierwsza konfiguracja wymaga internetu do pobrania zależności, SDK i pluginu Gradle.

1. Zainstaluj wskazane pakiety przez SDK Manager. Ustaw `JAVA_HOME` na JDK i `ANDROID_HOME` na SDK; lokalna konfiguracja SDK może też być w ignorowanym `local.properties`.
2. W katalogu projektu wykonaj `python tools/bootstrap.py`. Pobierze rewizje z `sources.lock.json`, podmoduł FreeType i zastosuje lokalny patch. Skrypt nie resetuje istniejących zmian przy niezgodnej rewizji.
3. Windows: `tools/build.ps1 -Abis 'arm64-v8a,armeabi-v7a'`. Linux/macOS: `./gradlew '-Pabis=arm64-v8a,armeabi-v7a' :app:assembleDebug`. Na Unix można użyć `python3` w kroku 2.
4. APK: `app/build/outputs/apk/debug/app-debug.apk`. To pakiet debug podpisany lokalnym kluczem SDK, nie wydanie podpisane kluczem produkcyjnym.

Wrapper weryfikuje SHA-256 dystrybucji Gradle. `preBuild` przygotowuje bank muzyki FreePats z przypiętego repozytorium. Narzędzie nie pobiera komercyjnych danych gry. Zmienną `PYTHON` można wskazać inny interpreter.

0.4.8: preBuild przygotowuje również XML i własne neutralne obrazy dla importu REZ. Nie kopiuje do APK oryginalnych grafik gry. ThinLTO/O3 są domyślnie włączone; `-PnativeLto=OFF` wyłącza ten eksperyment porównawczy. Asercje pozostają aktywne. Bootstrap stosuje teraz osobne patche OpenClaw i SDL; oba eksportuje i sprawdza `tools/export_patch.py`.

## Własne dane gry

`python tools/pack_assets.py --game-root '/sciezka/do/wlasnej/instalacji'` tworzy `build/game-data.zip`. Przy luźnym katalogu `Assets/` pakuje go do REZ; w pozostałych przypadkach kopiuje dostarczone CLAW.REZ. Dodaje wsparcie XML z OpenClaw i `asset-overrides/`, profil i pliki pomocnicze. Oryginalna instalacja nie jest modyfikowana. Utworzoną paczkę importuje się w aplikacji systemowym selektorem plików.

## Sprawdzenie pakietu

`python tools/clean_source_build.py --revision HEAD --report clean-source-new` tworzy nowy katalog raportu, eksportuje wskazany commit i buduje oba ARM od nowa z przypiętymi zależnościami. Wykorzystuje lokalne repozytoria zależności, zainstalowane SDK/JDK i cache Gradle; nie jest próbą pobierania wszystkiego na nowym komputerze. Nie kopiuje niezatwierdzonych zmian ani starych obiektów natywnych. Nazwa raportu musi być nowa. Przykład faktycznej próby: [0.4.17](validation/ATOMIC-PROGRESS-0.4.18.md).

`python tools/verify_apk.py app/build/outputs/apk/debug/app-debug.apk` sprawdza obie architektury ARM i wyrównanie segmentów ELF dla stron 16 KB. Dodatkowo użyj `zipalign -c -P 16 4` i `apksigner verify` z Build Tools.

## Telefon

Włącz debugowanie USB, zainstaluj platform-tools i dodaj `adb` do PATH. Przy kilku urządzeniach ustaw `ANDROID_SERIAL`. Testy urządzenia mają opisy w `docs/TESTING.md`. Minimalne API 21 jest ustawieniem pakietu; działanie na każdym Androidzie 5+ nie zostało potwierdzone.
