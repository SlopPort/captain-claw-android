# Audyt komentarzy i wydajności — 0.4.7

Przegląd wykonany przez LLM (Codex), 2026-10-20. To przegląd wybranych ścieżek silnika, nie dowód braku wszystkich błędów ani pełne przejście gry. Ścieżki poniżej odnoszą się do `upstream/OpenClaw/OpenClaw/Engine/`.

| Znalezisko | Ocena i działanie |
|---|---|
| `GameApp/BaseGameApp.cpp`, `SaveGameOptions`: pusta implementacja | Rzeczywisty brak zapisu zmian dźwięku. Android zapisuje teraz aktywność i głośności muzyki/efektów przy przejściu w tło i poprawnym zamknięciu. Zapis przez plik tymczasowy i podmianę; pozostała konfiguracja zachowana. Wymuszone zabicie bez wcześniejszego przejścia w tło nadal nie gwarantuje zapisu. |
| `UserInterface/UserInterface.cpp`, dwa warunki `VoiceOn`, brak `VoiceOff` | Potwierdzony defekt kodu. Menu Voice/Ambient generuje głównie zmiany widoczności przycisków; brak pełnej obsługi tych niezależnych kanałów. Pozostaje otwarte: sama zmiana literówki nie naprawiłaby przełączania dźwięku. |
| `Actor/Components/PhysicsComponent.cpp`, stary TODO drabiny | Poprawka zakończenia wspinania już w 0.4.6; test prawdziwej pierwszej drabiny poziomu 1. Nie porównano dokładnie z oryginalnym Windows. |
| `VGenerateXml` w komponentach pickup/aura/ambient zwraca null | Nieukończony eksport/serializacja. Nie stanowi sam w sobie dowodu błędu zwykłej rozgrywki. |
| `KinematicComponent::RemoveCarriedBody` | TODO zachowania windy po zejściu pasażera. Wymaga odtworzenia na konkretnej windzie; bez spekulacyjnej zmiany fizyki. |
| `CrumblingPeg`, komentarz o końcu animacji | Aktualna obsługa zmiany klatki już zatrzymuje i ukrywa obiekt. Komentarz może być nieaktualny; wymaga próby mapy. |
| TODO oryginalnego efektu śmierci i efektu aury | Różnice wizualne; nie potwierdzają wad obliczania obrażeń. |

## Optymalizacja

W pakiecie debug silnik miał `-O2`, ale biblioteki zależne, w tym Box2D, nie. Opcja CMake `PAZUR_OPTIMIZE_DEPENDENCIES` domyślnie dodaje `-O2` również do nich. Symbole diagnostyczne i asercje pozostają, bez `fast-math` i bez zmiany kroku fizyki.

Gałka dotykowa wcześniej rysowała koła i krawędzie od nowa co klatkę. Teraz ma trzy niewielkie tekstury (około 115 KiB), z tymi samymi wymiarami i kolorami. Po utracie zasobów renderera cache jest odtwarzany; nieobsługiwany renderer korzysta ze starego rysowania.

Huawei P9 Lite, Android 10 / LineageOS, około 2 GB RAM, 1920×1080, dotyk widoczny, muzyka i efekty włączone, 22050 Hz. Po 40 sekund na poziom, nieruchomy bohater w początkowej scenie, bez nietykalności. Wartości po pierwszej partii 300 klatek:

| Scena | Przed: FPS / p95 klatki | Po: FPS / p95 klatki |
|---|---|---|
| Poziom 1 | 22,9–23,0 / 49 ms | 60,0–60,2 / 18 ms |
| Poziom 13 | 18,3 / 62 ms | 42,5–43,9 / 25–26 ms |

Przed: logi lokalne `reports/fps-phases-baseline-0.4.7/`; po: `reports/fps-phases-optimized-0.4.7/`. Obie sceny uruchomiły się z dźwiękiem i bez wykrytej awarii procesu. W poziomie 1 aktualizacja świata spadła z około 11,6 do 7,1 ms, a renderowanie wraz z oczekiwaniem na GPU/vsync z około 31,8 do 9,4 ms. Zmieniono jednocześnie kompilację i cache: pomiar nie rozdziela ich indywidualnego wpływu.

To krótkie pomiary tych scen, nie gwarancja 60 FPS wszędzie, odporności na przegrzanie ani pełnej zgodności fizyki. Nie zmniejszono rozdzielczości ani jakości zasobów. Odczyt pamięci w tym przebiegu zwrócił zestawienie systemowe zamiast wiarygodnego PSS aplikacji; nie wyciągamy z niego wniosków o zużyciu RAM.

## English summary

An LLM (Codex) reviewed selected TODO paths. Android audio settings persistence was missing and is now implemented, preserving unrelated XML values. Voice/Ambient menu controls remain incomplete; serialization TODOs are not automatically gameplay defects. Native dependencies now use `-O2` while retaining debug symbols/assertions; joystick graphics are cached without lowering resolution. Short stationary Huawei P9 Lite tests improved level 1 from about 23 to 60 FPS and level 13 from about 18 to 43 FPS. These results are not a full playthrough or a sustained thermal benchmark. Raw logs remain local and are excluded from public source archives.

## Końcowe sprawdzenia

APK 0.4.7-dev, SHA256 `cec99ab20a247bae106303a932e0e55abc4bc6417e7c30a0b56f9ecf6db22465`: ARM64 i ARMv7 zbudowane, sprawdzone biblioteki ELF, wyrównanie ZIP/16 KiB i podpis APK. Próby fizycznego telefonu dotyczą ARM64, nie osobnego urządzenia ARMv7.

- `reports/audio-options-0.4.7/`: zapis w tle i odczyt po restarcie zaliczone; inne wartości, atrybuty i znacząca spacja w prompt zachowane. Pierwsza próba ujawniła usuwanie spacji przez TinyXML, poprawione przed końcowym testem.
- `reports/ladder-optimized-0.4.7/`: pierwsza drabina poziomu 1, zakończenie wspinania, ponowna góra, schodzenie, skok i zejście bokiem — zaliczone.
- `reports/combat-optimized-verified-0.4.7/`: wszystkie 13 kontrolowanych prób trafienia i ponownego kontaktu zaliczone. Poprzednia próba zatrzymała się na kontroli fokusu, ponieważ Android 10 inaczej nazywa pole w dumpsys; poprawiono parser, bez wyłączania zabezpieczenia.
- `reports/jump-touch-optimized-0.4.7/`: sześć prób skoku zaliczonych. Od odebrania zdarzenia przez silnik do ruchu: 28–30 ms; krótki tap 73,5–74,1 px, długi skok około 155 px. Każde przytrzymanie uruchomiło jeden skok. Zaliczono multitouch, brak przypadkowego ataku po przesunięciu palca, pauzę i powrót z tła. To pomiar programowy, nie fizyczne opóźnienie ekran–palec.

Konfigurację, zapis gry i ustawienia ekranu przywrócono po próbach. Obejrzano obraz bezczynnej i trzymanej gałki. Logi profilowania FPS powstały przed drobną korektą zachowania spacji XML i dodaniem komendy testowej dźwięku; końcowe testy regresji dotyczą powyższego SHA256. Nie przeprowadzono pełnego przejścia gry.
