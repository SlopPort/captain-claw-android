# Dotyk i skok — 0.4.3

20 października 2026. Redmi Note 8, Android 16. Zmiany dotyczą sterowania dotykowego; fizyka klawiatury pozostaje regulowana czasem przytrzymania.

Potwierdzono dwa źródła złego odczucia: dodatkowe kolejkowanie klawisza po dotyku i zmiana przycisku podczas przesuwania palca. W próbie starego układu przesunięcie palca ze skoku w lewo puszczało skok i uruchamiało atak. Impuls 10 ms dawał zaledwie 11,8 piksela wysokości.

Dotyk przekazuje teraz zdarzenie w bieżącym obiegu gry. Przycisk zachowuje przypisany palec do puszczenia; samo przesunięcie nad sąsiada nie uruchamia go. Tapnięcie podtrzymuje skok przez minimum 110 ms, bez opóźnienia jego rozpoczęcia. Dłuższe przytrzymanie pozwala skoczyć wyżej. Utrata fokusu i reset sterowania zwalniają klawisze oraz anulują podtrzymanie.

Przyciski są ułożone w łuk: skok 120×120, atak 104×104, strzał 96×96 jednostek logicznych. Skok jest na dole po prawej, atak po lewej, strzał wyżej. Są większe symbole i margines trafienia. Inspiracją do grupowania akcji pod kciukiem była [relacja twórców mobilnego Dead Cells](https://www.gamedeveloper.com/design/porting-i-dead-cells-i-to-mobile-an-in-depth-breakdown), nie kopiowanie jego zasobów.

| Przytrzymanie / próba | Wysokość przed | Wysokość po | Start ruchu przed / po |
|---|---:|---:|---|
| hold10 | 11.8 px | 73.5 px | 41 / 25 ms |
| hold100 | 63.6 px | 73.5 px | 43 / 26 ms |
| hold250 | 154.1 px | 155.0 px | 43 / 26 ms |
| hold700 | 155.0 px | 155.0 px | 43 / 26 ms |
| hold1800 | 155.0 px | 155.0 px | 40 / 26 ms |
| drift100 | 33.7 px | 74.0 px | 42 / 27 ms |

Czas jest mierzony od odebrania zdarzenia dotykowego przez silnik do pierwszej zmiany pozycji o ponad 2 piksele. Nie obejmuje całej drogi od fizycznego kontaktu z ekranem do wyświetlenia obrazu; do takiego pomiaru potrzebna jest kamera lub odpowiedni sprzęt. Rozdzielnie zapisano wiek zdarzenia w kolejce SDL. Sześć prób nie jest pomiarem pełnego rozkładu opóźnień.

Większe okrągłe przyciski początkowo spowolniły rysowanie. Ich dwa stany są teraz przygotowywane raz w małych teksturach i kopiowane w kolejnych klatkach. Rezerwa tekstur to około 0,3 MiB. Przy resecie urządzenia renderującego cache jest odtwarzany. Na poziomie 1 z muzyką i efektami po rozgrzaniu: około 60 FPS. Na poziomie 13: około 54 FPS; poprzednia APK na tych samych danych miała około 53 FPS. To pozostałe ograniczenie wydajności poziomu, nie deklaracja 60 FPS na wszystkich mapach.

Zaliczone: 18 pomiarów skoku przy trzech proporcjach ekranu (fizyczny 2340×1080, 16:9 i 4:3), ruch ze skokiem i niezależne puszczenie palców, atak/strzał, pauza i powrót z tła, 13 regresji hitboxów oraz krótkie uruchomienia map 1 i 13 z dźwiękiem. Surowe wyniki są w `reports/jump-*`; podsumowanie tworzy `tools/verify_jump_release.py`.

[Relacja gracza oryginału z 2009 r.](https://forum.winehq.org/viewtopic.php?p=28959) również opisuje niższy skok po tapnięciu i wyższy po trzymaniu spacji. Nie wykonano pomiaru oryginalnego EXE klatka po klatce. Minimalne podtrzymanie 110 ms jest wygodniejszą adaptacją dotyku, nie twierdzeniem o dokładnym parametrze wersji Windows.
