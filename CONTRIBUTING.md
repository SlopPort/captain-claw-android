# Praca nad projektem

Kod Androida znajduje się w `native/` i `app/src/`. Zależności są pobierane do ignorowanego katalogu `upstream/` według `sources.lock.json`.

Zmiany silnika edytuje się w `upstream/OpenClaw/`, a następnie zapisuje poleceniem `python tools/export_patch.py`. Do repozytorium trafia `patches/openclaw-android.patch`, a nie zagnieżdżone repozytorium silnika. Nie zmieniaj przypiętego commita bez osobnej aktualizacji patcha i testów.

Przed commitem zbuduj obie architektury ARM i sprawdź APK przez `tools/verify_apk.py`. Przy zmianach wejścia uruchom testy dotyku; przy zmianach fizyki lub walki dobierz odpowiednie scenariusze urządzenia. Pomyślne ładowanie mapy nie oznacza jej przejścia.

Testy ADB korzystają z `adb` dostępnego w PATH. Przy wielu urządzeniach ustaw `ANDROID_SERIAL`. Skrypty z diagnostyką zmieniają konfigurację i zapis tymczasowo i przywracają je w bloku `finally`. Testy dotyku są kierowane do okna aplikacji i przerywane po utracie fokusu. Starsze scenariusze w narzędziach mają charakter historyczny; do aktualnego interfejsu używaj `jump_touch_smoke.py`.

Surowe logi, zrzuty, konfiguracje testowe, komercyjne dane gry i wygenerowane APK pozostają lokalnie. Przed publikacją użyj `git status` i przejrzyj listę śledzonych plików. Nowe poprawki dokumentuj jako adaptację OpenClaw; zachowaj autorów i licencje zależności.
