# Instalacja krok po kroku

[English instructions](INSTALL-EN.md)

To wersja testowa. Potrzebujesz telefonu z Androidem, pliku APK tego portu oraz paczki `game-data.zip` przygotowanej z własnej kopii gry. APK to instalator aplikacji; ZIP to dane gry. Nie rozpakowuj ZIP na telefonie.

## Mam już APK i przygotowaną paczkę danych

1. Skopiuj oba pliki do folderu **Pobrane / Download** w telefonie. Możesz użyć kabla USB: odblokuj telefon, wybierz **Przesyłanie plików**, otwórz pamięć telefonu na komputerze i skopiuj pliki do Download.
2. Otwórz aplikację **Pliki** na telefonie, potem **Pobrane**. Dotknij pliku kończącego się na `.apk`.
3. Jeśli Android blokuje instalację, w pokazanym oknie otwórz ustawienia i zezwól tej aplikacji Pliki na instalowanie aplikacji. Wróć do instalatora i wybierz **Zainstaluj**. Nazwy opcji zależą od Androida. Zezwolenie możesz później wyłączyć.
4. Otwórz **Kapitan Pazur**. Dotknij **Wybierz dane gry**.
5. W systemowym oknie wyboru plików otwórz **Pobrane** i wybierz `game-data.zip`. Poczekaj na zakończenie importowania; gra uruchomi się sama.
6. Przy kolejnych uruchomieniach nie trzeba ponownie wybierać danych.

Nie potrzebujesz debugowania USB, ADB, Android Studio ani konta GitHub. Nie odinstalowuj aplikacji, żeby ją zaktualizować: zainstaluj nowszy APK na istniejący. Aktualizacja musi mieć zgodny podpis; komunikat o konflikcie podpisów nie oznacza uszkodzenia telefonu. Odinstalowanie usuwa dane i zapis gry — najpierw zabezpiecz zapis.

## Mam oryginalną grę na komputerze, ale nie mam ZIP

Samo przemianowanie `CLAW.REZ` na ZIP nie zadziała. Paczka zawiera też pliki potrzebne silnikowi portu. Obecnie przygotowanie paczki wymaga komputera; automatyczny import samego REZ nie jest jeszcze dostępny.

**Prostsza opcja w Windows:** po zainstalowaniu Pythona 3.11+ (z Tcl/Tk) i Git rozpakuj źródła, uruchom dwuklikiem `Prepare-game-data.cmd`, wybierz PL i wskaż `CLAW.REZ`. Okno poda lokalizację gotowego ZIP. Pierwsze przygotowanie wymaga internetu. Ten nowy kreator wymaga jeszcze sprawdzenia na czystym komputerze; jeśli nie otwiera się, użyj kroków terminalowych poniżej.

1. Pobierz i rozpakuj źródła portu. Zainstaluj Python 3.11 lub nowszy oraz Git. Przy instalacji Pythona zaznacz dodanie do PATH.
2. Otwórz terminal w rozpakowanym katalogu projektu — tym, w którym jest README.md. W Windows możesz otworzyć ten folder w Eksploratorze, wpisać `powershell` w pasku adresu i nacisnąć Enter.
3. Wpisz `python tools/bootstrap.py` i poczekaj. Potrzebny jest internet; skrypt pobiera otwarte zależności, nie komercyjną grę.
4. Wpisz `python tools/pack_assets.py --game-root "C:\Gry\Claw"`, zastępując przykładową ścieżkę folderem swojej gry zawierającym `CLAW.REZ`. Zachowaj cudzysłowy, zwłaszcza jeśli ścieżka zawiera spacje.
5. Gotowy plik znajdziesz w `build/game-data.zip` wewnątrz katalogu projektu. Skopiuj go na telefon i wykonaj instrukcję powyżej. Oryginalna instalacja pozostaje bez zmian.

Nie musisz kompilować APK, jeśli masz już gotowy instalator. [Budowanie APK ze źródeł](BUILDING.md) to osobna instrukcja dla osób, które chcą zmieniać program.

## Gdy coś nie działa

- **Nie widzę ZIP:** otwórz folder Download/Pobrane w systemowym selektorze, a nie plik wewnątrz archiwum.
- **Nieprawidłowa lub niekompletna paczka:** przygotuj ją narzędziem portu. Zwykły ZIP całego katalogu gry nie ma wymaganego układu.
- **Aplikacja nie została zainstalowana:** zapisz dokładną treść komunikatu, wersję Androida i nazwę APK. Nie usuwaj zapisów w ciemno.
- **Gra zamyka się lub działa wolno:** podaj model telefonu, Androida, poziom i czynność poprzedzającą problem. Android 5+ jest minimum kompilacji, a nie obietnicą działania na każdym telefonie.

Kod portu jest otwarty. Oryginalne dane Claw mają osobne prawa autorskie i nie są częścią publicznych źródeł. Posiadanie plików nie daje automatycznie prawa do ich publikowania. [Pochodzenie i licencje](../NOTICE.md).
