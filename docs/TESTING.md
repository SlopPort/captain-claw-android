# Weryfikacja

Walidacja 0.4.8 i ograniczenia pomiarów: [raport](validation/PORT-0.4.8.md). Nowe scenariusze:

- `python tools/ladder_smoke.py --expect-fixed --bottom --edges` sprawdza szczyt i dół izolowanej drabiny, ponowne wejście oraz obie strony podestu. Osobno uruchom `--first-map-ladder` dla rzeczywistej pierwszej drabiny poziomu 1.
- `python tools/omar_app_smoke.py` wykonuje kontrolowaną walkę i finał przez wejście lokalne aplikacji. Używa ochrony, mocy i teleportów; nie jest normalnym przejściem gry. Historyczne opcje bossów w `level_boot_smoke.py` nie są aktualną metodą testowania.
- `python tools/direct_rez_runtime_smoke.py` sprawdza runtime pełnego REZ wraz ze wsparciem z APK, zachowując i przywracając dane telefonu. Nie używaj 168-bajtowej atrapy REZ z instalacji CrazyHook.
- `PortFeaturesTest` sprawdza rzeczywiste klasy importu danych i zapisów w izolowanym katalogu. Zbuduj test APK z `-PtestRunner=pl.pazur.port.PortFeaturesTest`, zainstaluj go i uruchom `adb shell am instrument -w pl.pazur.port.test/pl.pazur.port.PortFeaturesTest`. Przed testami dotyku odbuduj test APK z domyślnym runnerem.
- `python tools/check_patches.py` nakłada oba patche na czyste kopie zmienionych plików przypiętych zależności i porównuje wynik ze źródłami roboczymi. Nie resetuje upstreamu.

Scenariusze urządzenia uruchamiaj kolejno. Wymagają wolnej aplikacji i nie mogą działać równocześnie z ręczną grą; konfiguracja i postęp są przywracane w bloku końcowym. FPS mierzy tylko aktywną symulację. Profiler komponentów zwiększa koszt klatki i nie służy do porównywania FPS.

Sprzęt używany do prób: Redmi Note 8, Android 16, ARM64 oraz Huawei P9 Lite, Android 10 / LineageOS, około 2 GB RAM. Biblioteki budowane również dla ARMv7, minimum API 21. Nie ma potwierdzenia na wszystkich wersjach Androida ani na telefonach z 1 GB RAM. Wyniki krótkich prób FPS Huawei i ograniczenia: [audyt](validation/TODO-AUDIT.md).

Aktualny test wejścia: zbuduj `:app:assembleDebugAndroidTest`, zainstaluj oba APK i uruchom `python tools/jump_touch_smoke.py`. Scenariusz mierzy wysokość i opóźnienie skoku przy dotknięciach 10/100/250/700/1800 ms oraz przesunięciu palca; sprawdza ruch ze skokiem, przyciski akcji, pauzę i utratę fokusu. Zmienna `ANDROID_SERIAL` wybiera urządzenie. Opcja `--size` pozwala wykonać tę samą próbę przy innych proporcjach i przywraca poprzedni rozmiar ekranu.

`tools/combat_device_smoke.py --mode regression` sprawdza 12 kombinacji pozycji/kierunku/wysokości pocisku i jeden powtórzony kontakt. `tools/combat_matrix.py` uruchamia zwykłych przeciwników na ich mapach źródłowych. `tools/combat_projectile_regression.py` wymaga kontaktu rzeczywistego pocisku z obu stron bohatera.

`tools/level_boot_smoke.py --levels 1 13 --frequency 22050 --effects-on` sprawdza ładowanie, dźwięk i pozostanie procesu przy życiu. Opcja `--combat-audit` odczytuje początkowe HP i ciała przeciwników i wymaga wcześniej wygenerowanej inwentaryzacji. Nie jest to przejście całej mapy. Historyczne opcje walk z bossami i starszy ControlSmokeTest nie są aktualnym testem interfejsu.

Surowe wyniki zapisują się w ignorowanym `reports/` i nie są częścią repozytorium źródeł. Zawierają lokalne konfiguracje, ścieżki, logi i zrzuty z gry. Czytelne podsumowania publikowane są w `docs/validation/`. Dane testowe i pliki gry pozostają własnością użytkownika.

Testy kontrolowane izolują geometrię i czas ataków. Ochrona bohatera oraz wyłączenie ataków celu są jawnie oznaczone w wynikach. Wynik pozytywny nie potwierdza pełnej zgodności balansu lub wszystkich scenariuszy z wydaniem Windows.

`tools/audio_options_smoke.py` sprawdza zapis po przejściu w tło, odczyt po ponownym uruchomieniu i zachowanie innych wartości/atrybutów XML. Przywraca konfigurację i zapis gry. `tools/ladder_smoke.py --expect-fixed --first-map-ladder` sprawdza rzeczywistą pierwszą drabinę poziomu 1. Test walki akceptuje format informacji o aktywności z Androida 10, zachowując kontrolę, czy gra jest na pierwszym planie.
