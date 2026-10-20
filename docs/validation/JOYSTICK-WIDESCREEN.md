> Surowe dowody i konfiguracje przywołane niżej są lokalnie w ignorowanym `reports/`; nie są dołączone do repozytorium.

# Gałka i szeroki ekran — 0.4.1

20 października 2026, Redmi Note 8, Android 16, ARM64. Wersja 0.4.1-dev (13).

## Zmiana

Zamiast czterech strzałek jest gałka z ośmioma kierunkami, martwą strefą 14 jednostek i ograniczeniem wychylenia do 48. Pierwszy palec zachowuje gałkę również poza jej okręgiem; drugi jej nie przejmuje. Przyciski skoku, ataku, strzału i zmiany broni działają niezależnie. Anulowanie dotyku, utrata fokusu i przejście do menu zwalniają sterowanie. Góra/dół zachowują funkcje wspinania, kucania i rozglądania; skok pozostaje osobnym przyciskiem. Ruch nadal ma prędkość oryginalnej gry, wychylenie wybiera kierunek.

Wysokość logiczna pozostaje 480, szerokość wynika z proporcji okna i wynosi co najmniej 640. Na ekranie 2340×1080 otrzymujemy 1040×480: o 62,5% więcej planszy w poziomie. Kamera i HUD korzystają z rozmiaru okna, przyciski akcji są zakotwiczone po prawej. Skalowanie jest jednakowe w obu osiach, z filtrem nearest; grafika nie jest deformowana ani rozmywana. Przy skali niecałkowitej poszczególne piksele mogą mieć nierówną szerokość o jeden piksel ekranu — nie dodajemy sztucznych szczegółów do oryginalnych sprite'ów. Menu i podsumowanie zachowują format 4:3, wyśrodkowany w szerokim oknie; pauza nakłada się na pełny widok planszy. Współrzędne dotyku menu uwzględniają przesunięcie. Finał i podpowiedź Omara są wyśrodkowane, a jego przyciemnienie pokrywa cały ekran.

## Potwierdzone testy

- Rzeczywiste wielopunktowe zdarzenia Android: gałka + skok, niezależne puszczanie, skosy, góra/dół/lewo, powrót do martwej strefy, brak przejęcia gałki przez drugi palec, wspólny przycisk akcji i anulowanie dotyku. Dodatkowo dotykowy atak, strzał, pauza i wznowienie oraz powrót z ekranu głównego bez zablokowanego kierunku. Log: joystick-0.4.1/native.log, weryfikacja tools/verify_controls.py.
- Te same testy przy tymczasowym rozmiarze urządzenia 1920×1080 (853×480 logicznie) i 1440×1080 (640×480 logicznie). To symulacja proporcji na tym samym telefonie, nie dodatkowe urządzenia. Wyniki i zrzuty: aspect-controls-0.4.1/. Rozmiar ekranu, konfigurację i zapis przywrócono.
- Zwykły start poziomów 1, 13 i 14, odtwarzanie muzyki i efektów, brak awarii. PSS odpowiednio 186526, 352177 i 251627 KiB. Krótkie próbki po rozgrzaniu poziomu 14: 59,9 FPS, p95 18 ms, maks. 25 ms; pierwsze próbki obejmują ładowanie i mają przycięcia. Wyniki: widescreen-0.4.1/.
- Dłuższy pomiar po rozgrzaniu: poziom 1 — 60 FPS, p95 18 ms, maks. 18–19 ms; poziom 13 — 59,6–60 FPS, p95 18 ms, maks. 19–24 ms. PSS 182198 i 361291 KiB. Logi i pamięć w widescreen-steady-0.4.1/. Próbki początkowe obejmują ładowanie; te należy oddzielać od ustabilizowanej pracy.
- Kontrolowana pełna walka z Omarem i zakończenie: zwycięstwo, pełne przyciemnienie, amulet, podsumowanie 4:3 i powrót do menu. Zrzuty obejrzano. Próba wykorzystuje teleport, ochronę gracza i przyznane zasoby; nie potwierdza balansu. Dowody: finale-widescreen-0.4.1-final/. Wcześniejsza próba finale-widescreen-0.4.1/ użyła niewłaściwego punktu startu 42050,1900 i nie uruchomiła inscenizacji; poprawny punkt to 41820,1940.
- Kompilacja obu ABI (ARM64/ARM32), podpis v1/v2, wyrównanie ZIP i bibliotek ARM64 do stron 16 KiB, kontrola eksportowanej poprawki. Suma APK zainstalowanego na telefonie jest identyczna z plikiem dystrybucyjnym.

APK: dist/kapitan-pazur-0.4.1-debug-universal.apk. Sumy i rozmiary: distribution-0.4.1.json. Paczka game-data.zip z 0.4.0 pozostaje bez zmian; ponowny import danych nie jest potrzebny.

Nie potwierdzono wykonania na starszym Androidzie, procesorze ARM32, telefonie z 1–2 GB RAM ani z fizycznymi stronami pamięci 16 KiB. Krótkie próby nie zastępują pełnego przejścia gry i długiego testu temperatury. Szeroki widok ujawnia więcej obiektów jednocześnie; obciążenie zależy od planszy.
