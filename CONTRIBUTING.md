# Praca nad projektem

[English](CONTRIBUTING.en.md) · [Przekazanie projektu](docs/HANDOFF.md) · [Publikacja](docs/PUBLISHING.md)

Kod Androida znajduje się w `native/` i `app/src/`. Zależności są pobierane do ignorowanego katalogu `upstream/` według `sources.lock.json`.

Zmiany silnika edytuje się w `upstream/OpenClaw/`, a następnie zapisuje poleceniem `python tools/export_patch.py`. Do repozytorium trafia `patches/openclaw-android.patch`, a nie zagnieżdżone repozytorium silnika. Nie zmieniaj przypiętego commita bez osobnej aktualizacji patcha i testów.

Przy zmianach produkcyjnego kodu natywnego zbuduj obie architektury ARM i sprawdź APK przez `tools/verify_apk.py`. Dla samej dokumentacji lub narzędzi bez zmian APK uruchom odpowiednie kontrole źródeł i narzędzia; nie przebudowuj niezmienionej gry. Przy zmianach wejścia uruchom testy dotyku; przy zmianach fizyki lub walki dobierz odpowiednie scenariusze urządzenia. Pomyślne ładowanie mapy nie oznacza jej przejścia.

Testy ADB korzystają z `adb` dostępnego w PATH. Przy wielu urządzeniach ustaw `ANDROID_SERIAL`. Skrypty z diagnostyką zmieniają konfigurację i zapis tymczasowo i przywracają je w bloku `finally`. Testy dotyku są kierowane do okna aplikacji i przerywane po utracie fokusu. Starsze scenariusze w narzędziach mają charakter historyczny; do aktualnego interfejsu używaj `jump_touch_smoke.py`.

Surowe logi, zrzuty, konfiguracje testowe, komercyjne dane gry i wygenerowane APK pozostają lokalnie. Przed publikacją użyj `git status` i przejrzyj listę śledzonych plików. Nowe poprawki dokumentuj jako adaptację OpenClaw; zachowaj autorów i licencje zależności.

Przy kilku wykonawcach używaj osobnych repozytoriów dla innych projektów i gałęzi
roboczych dla zmian w tym projekcie. Nie zmieniaj globalnego konta Git ani cudzych
poświadczeń. `adb kill-server` wpływa na wszystkie urządzenia. Nie restartuj ADB,
USB ani telefonu udostępniającego internet jako sposobu naprawy jednego testu.
Nie zapisuj prywatnych numerów urządzeń w repozytorium.

`campaignposition`, `pegtrial`, `combatstage` i `campaignfinish` zmieniają scenę;
nie wolno używać ich do dowodzenia naturalnego przejścia. Starszy
`checkpoint_smoke.py` używa globalnego wejścia Androida i nie jest zatwierdzonym
bieżącym scenariuszem. Po niepowodzeniu sprawdź przywrócenie danych użytkownika.
