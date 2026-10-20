> Surowe dowody i konfiguracje przywołane niżej są lokalnie w ignorowanym `reports/`; nie są dołączone do repozytorium.

# Audyt zwykłych przeciwników — 0.4.2

Zakończono kontrolowane próby 20 października 2026. Wyniki nie oznaczają pełnego przejścia wszystkich map. Podsumowanie maszynowe: `combat-audit/final-validation.json`.

## Zakres i dane

Inwentaryzacja obejmuje 45 wariantów zwykłych przeciwników i 1415 obiektów WWD na 14 mapach. Nie obejmuje bossów ani dodatkowych przeciwników tworzonych dopiero w trakcie gry. Zbadano efektywne prototypy po dziedziczeniu XML z dokładnie tego archiwum ASSETS.ZIP, które trafiło na telefon.

Sprawdzono istnienie 73 animacji i 71 indeksów klatek wywołujących ataki, w tym armaty szczurów. Wszystkie indeksy mieszczą się w oryginalnych animacjach. Początkowe HP i rozmiary ciał wszystkich 45 prototypów są dodatnie i poprawne strukturalnie. Wyniki: `combat-audit/asset-validation.json`, `inventory.json`, `map-coverage.json`. Powtarzalna weryfikacja: `tools/audit_combat.py`, ekstrakcja przez `tests/combat_assets_probe.cpp`, następnie `tools/verify_combat_assets.py`.

## Zmiany w grze

- Przywrócono 54 kameleony poziomu 13. Wcześniej logika Chameleon była przypisana do pustego prototypu. Nowy prototyp korzysta z grafik i animacji poziomu 13 oraz wspólnego zachowania kameleona.
- Czujnik podparcia stóp nie przyjmuje już trafień od pocisków i obszarów obrażeń. Ten czujnik sięga poniżej rzeczywistego ciała i służy do wykrywania podłoża; wcześniej strzał poniżej stóp zabierał zdrowie.
- Jeden pocisk zadaje danemu aktorowi obrażenia najwyżej raz, także przy kilku zgłoszeniach kontaktu i pociskach przebijających. Oddzielne pociski nadal mogą trafiać niezależnie.
- Granice aktywnego ciała kucającego bohatera pomijają wyłączone części głowy i tułowia. Kucanie miało już wyłączone kolizje tych części, ale zapytanie o granice zwracało rozmiar postaci stojącej.
- Patrol zwykłego przeciwnika respektuje początkowy kierunek grafiki. Wcześniej zmienna kierunku zawsze startowała w prawo.
- Uporządkowano obsługę zdrowia: poprawny identyfikator źródła inicjalizacji, brak powtórnego wejścia w śmierć, brak reakcji na otrzymanie obrażeń podczas leczenia oraz odrzucanie dalszych obrażeń po śmierci.
- Punkt trafienia pocisku jest wyznaczany symetrycznie na lewej lub prawej krawędzi aktywnego ciała.
- Obsługa kontaktu pocisku sprawdza zgodność obu rejestrów ciała fizycznego i identyfikatora jego aktora. Kontakt niezarejestrowanego lub zastąpionego ciała jest pomijany przed zapytaniem o jego granice i przed naliczeniem obrażeń.

## Metoda prób na telefonie

Urządzenie: Redmi Note 8, Android 16, ARM64. Polecenia sterujące są odczytywane wyłącznie przez działającą grę, a klawisze trafiają bezpośrednio do SDL. Skrypt kontroluje proces i aktywne okno; przerywa po ich utracie. Nie wysyła globalnych naciśnięć klawiszy Androida. Konfiguracja i zapis są przywracane po każdej serii.

Próby przyjmowania ataków używają rzeczywistej AI, bez ochrony bohatera, z przeciwnikiem po obu stronach. Próby szabli i pistoletu mają nieruchomy cel z wyłączonymi atakami i chronionego bohatera; służą do sprawdzania trafień, HP i śmierci, a nie trudności naturalnej walki. Wyjątkiem jest krab: jego osłona w spoczynku ma 100% parowania, dlatego do próby trafień pozostawiono jego ataki i trafiano podczas otwarcia osłony. Wcześniejszy nieruchomy krab słusznie nie otrzymywał obrażeń. Niskie cele są ostrzeliwane z kucania. Syrena jest oceniana także po efekcie zamrożenia, ponieważ jej pocisk nie musi odejmować zdrowia. Mewy i armaty używają innych mechanizmów niż wspólna klatka ataku wręcz.

Każda grupa jest ładowana na własnej mapie źródłowej. Wczesna próba wstawienia Mercata do poziomu 1 zakończyła się asercją podczas tworzenia efektu trójzębu: zestaw LEVEL_* poziomu 1 nie zawiera takiego efektu. To ograniczenie niewłaściwej konfiguracji próby, nie potwierdzona awaria naturalnej walki poziomu 11. Inne wczesne błędy pomocnika testowego dotyczyły usuwania obiektów bez powiadomienia sceny i próby wznowienia umierającej postaci; poprawiono pomocnik, a nie zaliczono tych prób jako udanych.

## Wyniki i ograniczenia

Przed poprawką potwierdzono trafienie 10 HP poniżej stóp oraz dwukrotne odebranie 1 HP przez ten sam pocisk. Wstępna regresja po poprawce przeszła 12 kombinacji wysokości/kierunku/kucania oraz próbę powtórzonego kontaktu: 13/13. Końcowe powtórzenie przez wejście lokalne aplikacji także przeszło 13/13: `combat-final-regression-0.4.2/results.json`.

Pełna macierz 45 wariantów przeszła po dopasowaniu próby kraba do jego rzeczywistej podatności. Przy pierwszej próbie BearSailora na poziomie 7 wystąpiła jednorazowa asercja podczas odczytu granic pocisku bez zarejestrowanego ciała: `combat-level7-failed-0.4.2/crash.log`. Ponowienie w świeżym procesie przeszło. Nie ustalono jednoznacznie źródła rozbieżności; dodano kontrolę rejestracji kontaktu, ale nie przedstawiamy jej jako dowodu usunięcia przyczyny. Końcowy pakiet przeszedł dodatkowe regresje po tej zmianie: 16 wariantów atakujących pociskami z odległości 250 pikseli, ponowienie czterech typów poziomu 7 i 13 prób hitboxów. Każdy z 16 wariantów potwierdził kontakt pocisku z bohaterem po obu stronach. Log `Pazur ignored unregistered projectile contact` obejmuje także zwykłe kontakty już usuniętych pocisków z wyczyszczonym wskaźnikiem aktora; sam nie dowodzi odtworzenia wcześniejszej rozbieżności rejestrów.

Nie potwierdzono zgodności balansu z wydaniem Windows. Oryginalne WWD zawierają 84 obiekty z niezerowym polem zdrowia lub obrażeń; nie zmieniono globalnie ich interpretacji bez potwierdzenia semantyki oryginalnej gry. Są zapisane w `map-coverage.json`. Kontrola plików, odczyt obiektów przy ładowaniu i kontrolowane walki nie zastępują przejścia wszystkich map, obserwacji każdego ataku w naturalnym terenie ani porównania klatka po klatce z Windows. Obsługa innych Androidów i telefonów z 1–2 GB RAM nadal wymaga osobnych urządzeń.


Końcowa próba pirata poziomu 7 początkowo odbiła trzy kolejne kule (HP 25→25); prototyp ma 50% parowania kul i 33% parowania szabli. Powtórzenie potwierdziło obrażenia (25→5). Zachowano wcześniejszy wynik w `combat-level7-final-0.4.2/results-before-parry-retry.json`, a ponowienie w `combat-pirate-final-0.4.2/`. Nie zmieniono szans parowania.

Pełną macierz 45 wariantów wykonano przed ostatnim zabezpieczeniem rejestracji ciał. Po tej zmianie końcowa APK przeszła powyższe regresje kontaktów, cztery warianty poziomu 7 oraz kontrolę wszystkich map. Dowody: `combat-matrix-0.4.2-level*/`, `combat-ranged-final-0.4.2-level*/`, `combat-level7-final-0.4.2/`, `combat-all-maps-0.4.2/`. Tabela wartości HP i ciał: [enemy-health.csv](enemy-health.csv).

Kontrola uruchomionych map potwierdziła 1415/1415 oczekiwanych obiektów, dodatnie początkowe HP, poprawne rozmiary ciał i 54 kameleony poziomu 13. Wszystkie 14 procesów pozostało aktywnych w krótkiej próbie z muzyką i efektami. PSS po ładowaniu: 191,0–345,4 MiB; nie jest to pomiar długiej rozgrywki ani potwierdzenie płynności na urządzeniu z małą pamięcią.

| Poziom | Liczba zwyklych przeciwnikow | Poprawne HP i ciala |
|---|---:|---|
| 1 | 54 | tak |
| 2 | 72 | tak |
| 3 | 90 | tak |
| 4 | 88 | tak |
| 5 | 132 | tak |
| 6 | 140 | tak |
| 7 | 124 | tak |
| 8 | 174 | tak |
| 9 | 118 | tak |
| 10 | 90 | tak |
| 11 | 75 | tak |
| 12 | 102 | tak |
| 13 | 113 | tak |
| 14 | 43 | tak |
