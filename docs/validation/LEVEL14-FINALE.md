> Surowe dowody i konfiguracje przywołane niżej są lokalnie w ignorowanym `reports/`; nie są dołączone do repozytorium.

Aktualizacja 22.10.2026, 0.4.12-dev: `omar-campaign-current1` wykrył regresję naszego nowego pakietu pomocniczego — brak dwóch PNG autorów powodował awarię przy inicjalizacji menu po finale. Dodano własne plansze tekstowe, bez portretów i grafik gry, oraz kontrolę kompletności PNG podczas pakowania. `omar-campaign-credits-fixed` przeszedł obie fazy Omara, inscenizację, wyniki, powrót do menu i kontrolę braku poziomu 15 w zapisie. Próba używa teleportów, żywiołów, nieskończonej amunicji i ochrony; nie zmienia HP bossa. To nie jest naturalne przejście mapy.

# Finał i przeciwnicy, 0.4.0 — 20.10.2026

Dodano Omara i BossStager do zwykłego ładowania poziomu 14. Limit wyboru
poziomów oraz profil podniesiono do 14; konfiguracja poprzedniej wersji z
limitem 13 jest aktualizowana podczas odczytu. Koniec poziomu 13 może teraz
zapisać dostęp do 14. Podsumowanie finału wraca do menu, bez tworzenia
zapisu lub próby wczytania poziomu 15.

## Walka i inscenizacja

Omar ma 200 zdrowia. Pierwsza połowa walki wymaga przeciwnego żywiołu,
przepuszczonego przez lukę w obracającej się osłonie. Poprawny żywioł
odbiera 25 zdrowia i zmienia osłonę, zgodny z osłoną przywraca 25.
Zwykłe obrażenia są blokowane. Druga połowa wymaga trzech trafień kulą
z pistoletu i ataku mieczem w kucki; trafienie odbiera 25 i przenosi bossa
na drugą stronę górnej platformy. Nie wystarcza samo wysłanie klawisza:
obrażenia przechodzą przez rzeczywiste kontakty pocisków i obszaru miecza.

Walka korzysta z oryginalnych grafik osłon, energii i animacji Omara.
Pociski energii zadają 20 obrażeń. Osiem elementów osłony i maksymalnie
12 pocisków ograniczają liczbę obiektów; pociski mają czas życia.
Zmiany pozycji bossa są odkładane poza zablokowany krok fizyki.
Po śmierci gracza zerowane są faza, osłona, liczniki, pociski i pozycja.
Wejście na arenę ustawia tymczasowy punkt odrodzenia na jej górnej
platformie; nie nadpisuje zapisu checkpointu w pliku.

Oryginalne miecze przy arenie odnawiają się sześć sekund po zebraniu,
po jednym egzemplarzu każdego rodzaju. Na początku drugiej fazy port
uzupełnia pistolet do co najmniej 24 kul. To jawne ustawienia portu.
Okno po trzeciej kuli trwa 3,5 s, przerwa po poprawnym trafieniu 900 ms,
a prędkość pocisków wynosi 230 pikseli/s. Wartości nie były odtwarzane
z kodu maszynowego ani porównane klatka po klatce z Windows.

Wprowadzenie używa oryginalnych dialogów STAGING, panoramy kamery w obu osiach,
nazwy bossa i zapowiedzi. Kapitulacja odtwarza killfall, killfall2 oraz
killfall3, zatrzymując ostatnią klatkę. Następnie pokazuje oryginalne grafiki
klejnotu, Adory i amuletu z krótkim polskim tekstem, a potem podsumowanie.
Jest to zakończenie odtworzone w silniku, nie oryginalny film końcowy.
Kamera podczas zapowiedzi śledzi wysokość Omara, a zamrożona postać nie
próbuje równocześnie zerować jej przesunięcia pionowego.

Poprawiono odczyt dekoracji WALL, GONG, SIAMESE i AMULET, których pojedyncze
pliki PID nie mają numeru klatki. Podsumowanie korzysta z dostępnego
AMMAKE.WAV zamiast nieobecnego angielskiego nagrania Clawa. Brak pliku WAV
nie powoduje już dereferencji pustego uchwytu przy odczycie jego długości.

## Przeciwnicy

TigerGuard korzysta z frontflip/backflip, prędkości poziomej 2,6 i skoku
5 m/s. Zachowuje granice patrolowania; przerwa między unikami wynosi 2,4 s.
Nie rozpoczyna kolejnego uniku w powietrzu. Pozostałe poziomy zachowują
poprzednie parametry istniejącego komponentu RollEnemyAIStateComponent.
Ataki wysokie, niskie, blokowanie, łup i śmierć pozostają aktywne.

Kameleon przechodzi od pełnej widoczności do alfa 32 i z powrotem w cyklu
6 s. Atak językiem i reakcja na trafienie odsłaniają go, a śmierć przywraca
pełną widoczność. Alfa jest ustawieniem pojedynczego obiektu. Nie dodawano
wspinania kameleonów ani rekonstrukcji wszystkich ruchów strażnika.

Próba tiger-polish-0.4.0 ujawniła odczyt akcji ataku poza wektorem,
gdy przerwa między unikami kończyła się przed zakończeniem animacji ataku.
Sprawdzanie widoczności korzysta teraz ze stałego sensora pierwszej akcji,
a martwy przeciwnik nie może ponownie wejść w stan walki. Wynik tej
nieudanej próby zachowano wraz ze stosem awarii.

Próba ponowienia walki ujawniła też przerywanie animacji śmierci Clawa
przez zwykłe callbacki zatrzymania ruchu i lądowania. Przez to gracz
pozostawał z zerowym zdrowiem. Stan śmierci jest teraz zachowywany do
końca animacji; dopiero wtedy uruchamia się istniejący mechanizm odrodzenia.

## Zakres dowodów

Test reguł tests/omar_battle_test.cpp uruchomiono jako program ARM64 na
telefonie: PASS dla przeciwnych żywiołów, leczenia, obu faz, bramki trzech
kul, śmierci i resetu. To uzupełnienie prób gry, nie ich zastępstwo.

Scenariusz --omar-fight używa zwykłych zdarzeń klawiszy Androida,
tymczasowej ochrony wyłącznie gracza, deweloperskich teleportacji,
mieczy żywiołów oraz nieskończonej amunicji. Nie zmienia bezpośrednio
zdrowia Omara ani nie usuwa go poleceniem. Nie dowodzi naturalnego
przejścia mapy, balansu walki ani dotarcia do areny ze startu.

Wcześniejsza próba omar-input-0.4.0-final pokonała bossa, ale wykazała
awarię brakującego nagrania przy otwieraniu podsumowania. Jej wynik
crash_free=false zachowano; nie jest raportowana jako PASS.

Redmi Note 8, Android 16, ARM64; muzyka i efekty włączone:

| Próba | Wynik | PSS KiB | Znaczenie |
|---|---|---:|---|
| tiger-polish-0.4.0-final | PASS | 202455 | uniki, ataki i obrażenia gracza bez ochrony, 14 s |
| chameleon-polish-0.4.0 | PASS | 202765 | alfa 32 i 255 bez ochrony, 12 s |
| tiger-defeat-0.4.0 | PASS | 201383 | zwykłe ataki i śmierć strażnika z ochroną gracza |
| sword-resupply-0.4.0 | PASS | 202916 | zebranie lodowego miecza i odnowienie, bez ochrony |
| omar-reset-0.4.0-final | PASS | 200735 | trafienie 200→175, śmierć w lawie, odrodzenie i nowa walka |
| finale-release-0.4.0 | PASS | 219801 | osiem trafień, kapitulacja, amulet, podsumowanie i menu |
| normal-release-0.4.0: poziom 1 | PASS | 196070 | zwykły start, 6 s, bez ochrony |
| normal-release-0.4.0: poziom 13 | PASS | 360435 | zwykły start, 6 s, bez ochrony |
| normal-release-0.4.0: poziom 14 | PASS | 249820 | zwykły start bez trybu podglądu, 6 s, bez ochrony |
| chameleon-defeat-0.4.0 | PASS | 200237 | zwykłe ataki i śmierć kameleona z ochroną gracza |

W próbie resetu ochrona gracza została wyłączona przed rzeczywistą śmiercią
w lawie. Odrodzona postać ma mniej żyć, pojawia się na arenie, a boss
rozpoczyna nową walkę z pełnym zdrowiem. Nie użyto ręcznej zmiany jego HP.

finale-release-0.4.0 bada dokładnie APK z dist/ o SHA-256 zaczynającym się
181402071ce6d346. Zrzuty finału, podsumowania i polskiego menu obejrzano.
Próba potwierdza brak awarii i brak nieznalezionych zasobów podczas całego
scenariusza. PSS 219801 zmierzono po powrocie do menu; osobny pomiar
memory-during-battle.txt wyniósł 201882 KiB podczas walki. Stabilne próbki
procesu miały około 60 FPS i p95 17–18 ms; rozgrzewanie, teleportacje
i zrzuty dawały większe skoki. Nie jest to test długotrwałego obciążenia.

Kontrola APK potwierdza ARM64 i ARM32, wyrównanie segmentów ARM64 i ZIP do
16 KiB oraz poprawny podpis v1/v2. Łatka silnika przechodzi kontrolę
odwrotnego zastosowania. Suma APK zainstalowanego na telefonie jest zgodna
z dist/, podobnie jak suma ASSETS.ZIP w sparowanej paczce danych.
Pełne sumy: distribution-0.4.0.json; pozostałe kontrole: apk-0.4.0.json,
zipalign-0.4.0.txt i signature-0.4.0.txt. Konfiguracje i zapisy po testach
zostały przywrócone.

Raport omar-finale-0.4.0 potwierdził wszystkie osiem trafień, kapitulację,
ekran amuletu, podsumowanie i przejście do menu, bez awarii i brakujących
odwołań do zasobów. Skrypt wysłał wtedy kolejne potwierdzenia już w menu,
uruchamiając poziom 1; jego końcowy pomiar PSS 260678 nie jest pamięcią
samej walki. Scenariusz poprawiono, aby zatrzymywał wejście po powrocie do menu.

## Źródła mechanik

- [Claw Design Bible](https://ics.uci.edu/~frost/GameDesign/ClawDesignDoc.pdf):
  opisy przeciwników i ceremonii amuletu. Dokument projektu nie jest
  identyczny z końcową grą.
- [Relacja z przejścia Richiego Kleinhenza](https://captainclaw.net/en/walkthroughs.html):
  naprzemienne żywioły oraz sekwencja trzech kul i ataku w kucki.
- Oryginalny WORLD.WWD, PID, ANI, tekst ANIMATION.TXT i WAV lokalnej gry;
  odczyt geometrii: asset-probe-14-omar.txt.

Pełne przejście wszystkich map, wierny balans, starszy Android,
telefon 1–2 GB RAM oraz fizyczne strony pamięci 16 KiB pozostają
niezweryfikowane. Kompilacja ARM32 nie jest testem jego działania.
