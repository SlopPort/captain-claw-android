# Natural checkpoint and menu reload — 0.4.24

## English

OpenAI Codex (LLM) performed and documented this work. Status: **first persistent
checkpoint reached naturally; level 1 and the full campaign remain incomplete**.
APK SHA-256: `583ec1d605527ba812e7da3da510a52dc4e08a2cc94f84c4733592051f2cc0a2`.

The owned Redmi / Android 16 run starts from an isolated standard level-one save
(HP100, lives3, pistol10, magic5, dynamite3). Subsequent traversal uses ordinary
app-local SDL input and read-only observations: no teleport, invulnerability,
health/ammo edits, generated projectiles or added terrain. Ordinary deaths,
respawns, pickups and one End Life menu action are retained, not rolled back.

The run passed the early ladders, both routes around the first moving platform,
the vertical elevator, the second respawn flag, four static stone steps, the
next ladder, enemies and the real start elevator / lower ladder transfer.
An early lower-ladder attempt overshot and died; that failure remains recorded.
The corrected sequence first passed an explicitly controlled Huawei fixture,
then passed during the natural Redmi run. A controlled fixture is not counted
as natural traversal.

At the first persistent checkpoint the game emitted
`Pazur progress atomically saved` and wrote these values itself:

| Field | Saved and reloaded value |
| --- | --- |
| Level / checkpoint | 1 / 1 |
| Score | 43900 |
| Health | 100 |
| Spare lives | 0 |
| Pistol / magic / dynamite | 6 / 2 / 3 |

The natural collision position was approximately (6867.6,4991.6). The exact save
snapshot SHA-256 is
`6931269371ecc6bc82754bea9f4dd61953bfe5df41952f26b72313247ee38159`.
It is byte-identical to the file copied when the owned run ended. Original user
configuration and save files were then re-read and matched their backups byte
for byte. The ongoing continuation owns separate backups and restores them on exit.

The first resume-driver attempt used the debug new-level shortcut and therefore
started checkpoint zero; it was stopped without traversal and is not a reload
pass. The corrected driver starts the ordinary menu, chooses Load game, La Roca,
and checkpoint 1 using keyboard events. The supplied game-written XML is copied
unchanged. The engine places the hero near (6873,4991.6). Runtime observations
confirm HP100, lives0, pistol6, magic2 and dynamite3; the screenshot shows score43900.
Weapons are cycled normally and returned to the pistol. No position/resource
restoration command is used to obtain these results.

Local evidence (ignored, no game data or private device ids added to Git):
`reports/natural-campaign-0.4.24-run1`,
`reports/natural-campaign-0.4.24-resume1` (rejected driver attempt),
`reports/natural-campaign-0.4.24-resume2/normal-resume-proof.json`,
`reports/cavity-huawei-0.4.24-r1` (controlled transfer fixture).

Open observations: getting hit on the first moving platform was followed by
losing support and falling. This needs a controlled reproduction and comparison
before changing gameplay. A missed fourth stone step led into a lower pocket;
this was a route error, not established as a physics bug. The checkpoint write
also produced a logged 61.9 ms frame, so these diagnostics do not establish a
55/60 FPS minimum. Remaining maps, bosses and final ending are still release gates.

## Polski

Pracę wykonał i udokumentował OpenAI Codex (LLM). Stan: **naturalnie osiągnięto
pierwszy trwały zapis; pierwszy poziom i cała kampania nadal nie są ukończone**.
Test dotyczy wskazanego wyżej APK na Redmi z Androidem 16.

Początek korzysta z oddzielnego standardowego zapisu poziomu 1. Dalsze przejście
używa zwykłych przycisków i odczytu stanu; bez teleportowania, odporności, zmian
zdrowia/amunicji, tworzenia pocisków lub terenu. Zachowano śmierci, odrodzenia,
przedmioty z mapy i jedno użycie zwykłej opcji „Zakończ życie”. Nie cofano ich.

Pazur przeszedł drabiny, ruchomą platformę i pionową windę, dotarł do kolejnej
flagi, przeszedł cztery kamienne podesty i dalszy dolny przejazd. Pierwsza próba
przesiadki na dolną drabinę zakończyła się śmiercią po zbyt dalekim ruchu w prawo.
Poprawiona sekwencja przeszła najpierw osobny kontrolowany test na Huawei, potem
naturalną próbę na Redmi. Testu kontrolowanego nie zalicza się jako przejścia.

Gra sama zapisała checkpoint 1 poziomu 1: 43 900 punktów, zdrowie 100, zero
zapasowych żyć, pistolet 6, magia 2, dynamit 3. Log potwierdza zapis atomowy.
Zachowana kopia jest identyczna z plikiem przy zakończeniu sesji; jej suma jest
podana wyżej. Po zakończeniu pierwszej sesji ponownie pobrano pliki użytkownika
— konfiguracja i zapis były identyczne bajt w bajt z kopiami sprzed testu.
Bieżąca kontynuacja posiada oddzielne kopie i przywraca je przy zakończeniu.

Pierwsza próba wznowienia narzędzia błędnie użyła skrótu rozpoczynania poziomu;
zatrzymano ją bez grania dalej i nie zaliczono jako poprawnego wczytania.
Poprawione narzędzie przechodzi zwykłe menu „Wczytaj grę”, La Roca, checkpoint 1.
Kopiuje niezmieniony plik zapisany przez grę. Silnik sam ustawia pozycję startową
checkpointu. Odczyty potwierdzają zdrowie, życia i całą amunicję zgodnie z tabelą,
a zrzut ekranu pokazuje 43 900 punktów. Nie używa się poleceń ustawiających
pozycję lub zasoby do uzyskania tych wyników.

Do dalszego audytu: utrata oparcia na ruchomej platformie po trafieniu wymaga
osobnego odtworzenia i porównania. Ominięty kamienny stopień był błędem trasy,
nie potwierdzonym błędem fizyki. Przy zapisie wystąpiła klatka 61,9 ms, więc te
próby nie dowodzą minimum 55/60 FPS. Pozostałe poziomy, bossowie i zakończenie
nadal wymagają przejścia przed wydaniem 1.0.

## Further continuation / Dalsza kontynuacja

English: The ordinary continuation crossed the crumbling pegs at x7502,7631,
7758 and reached the static catwalk near x7900 with HP100. The observer initially
re-read older support samples and falsely reported a bad landing; consuming each
sample only once fixed this test-tool error. A subsequent natural repetition
also crossed all four landings with HP100. No platform timing or collision was
changed. The continuation defeated the catwalk Officer with a normal pistol shot
and climbed the x8224 ladder. It later lost its last life under enemy fire; this
failure is retained in `natural-campaign-0.4.24-resume3`, not counted as a pass.

The suspected ladder-jump failure was separately observed without enemies
(`ladder-jump-redmi-0.4.24-r1`): ordinary ascent ended at (8224,4104.6), climb=0,
ground=1. A normal 600 ms jump with 650 ms right movement took off after 31 ms,
rose 155 pixels and landed at (8448.8,4114.6), ground=1. The earlier natural
1700 ms right input ran past the short upper catwalk and fell onto the lower one.
This evidence does not justify a physics change. The isolated fixture removes
enemies and sets HP100/ammo99 before initial placement; it is not a campaign pass.

Polski: Zwykłe skoki pozwoliły przejść kruche podesty x7502,7631,7758 i dotrzeć
na stały pomost około x7900 ze zdrowiem 100. Narzędzie początkowo odczytywało
ponownie stare próbki kontaktu i fałszywie odrzucało lądowanie. Poprawiono wyłącznie
obserwator; powtórzenie również przeszło cały odcinek ze zdrowiem 100. Nie zmieniano
czasu znikania ani kolizji podestów. Następnie zwykły strzał pokonał Oficera,
a Pazur wszedł na drabinę x8224. Później zginął pod ostrzałem, tracąc ostatnie życie.
Nie zaliczono tej próby jako ukończenia poziomu.

Osobna próba bez przeciwników potwierdziła poprawny skok z tej drabiny: początek
(8224,4104.6), brak wspinania, kontakt z podłożem; start skoku po 31 ms, wznios
155 pikseli i lądowanie na górnym pomoście (8448.8,4114.6). W naturalnej próbie
zbyt długi ruch w prawo (1700 ms) przeprowadził bohatera za koniec pomostu.
Nie ma podstaw do zmiany fizyki. Próba kontrolowana usuwa przeciwników i ustawia
zdrowie/amunicję przed początkowym ustawieniem bohatera; nie jest przejściem gry.

The fourth continuation repeated the real peg crossing, boarded the y4182 moving
platform and reached the next ledge near (9063,4114), HP60. It then died to repeated
Officer hits near (9094,4114). Input acceptance under hurt recovery remains an
open combat-fairness check; the loss is not hidden and level 1 remains incomplete.
No invulnerability, recovery, reach or enemy timing parameters were changed.
Local evidence: `natural-campaign-0.4.24-resume4`.

Czwarta kontynuacja ponownie przeszła podesty, przejechała platformą y4182 i dotarła
na następną półkę około (9063,4114), zdrowie 60. Następnie Pazur zginął od kolejnych
trafień Oficera około (9094,4114). Przyjmowanie sterowania w trakcie reakcji na
obrażenia nadal wymaga audytu uczciwości walki. Nie zmieniano odporności, czasu
reakcji na obrażenia, zasięgu ani tempa ataków. Poziom 1 nadal nieukończony.

## Later route attempts / Kolejne próby trasy

The fifth ordinary continuation defeated the next Officer by firing from the
moving platform, reached x9236 with HP70 and boarded the second carrier. A late
jump began at x9606.8, outside the ladder column x9568; it fell and reached Game
Over. This is retained as a failed route, not a ladder-collision fix.
The sixth continuation instead held Up early and attached to that ladder:
HP60, x9568, y3548. The helper stopped its test 19.4 pixels below the cap because
it did not allow enough held-input time for both the carrier return and ascent.
It restored the user files; this is a test-duration failure, not a death or a
completed ascent. The seventh attempt died to a Soldier before this transfer:
a requested pistol action during hurt recovery had not defeated it. Blindly
continuing after a requested attack is therefore not a reliable route controller.
The game APK was unchanged throughout these attempts.

`second-carrier-ladder-redmi-0.4.24-r1` separately confirms the ordinary early-Up
sequence reaches x9568,y3528.6, HP100 in an explicit controlled fixture. The
reusable observer now allows three two-second Up holds, accounting for variation
in the platform's return timing. This fixture removes enemies and initializes
HP100/ammo99 before initial placement. It is not natural campaign completion.

Piąta naturalna kontynuacja pokonała Oficera strzałem z ruchomej platformy,
dotarła do x9236 ze zdrowiem 70 i weszła na kolejną platformę. Za późny skok
rozpoczął się przy x9606,8, poza kolumną drabiny x9568, i zakończył się śmiercią.
Szósta próba wcześniej przytrzymała „góra” i poprawnie zaczepiła się o drabinę:
zdrowie 60, x9568, y3548. Narzędzie zakończyło test 19,4 piksela przed szczytem,
ponieważ nie uwzględniło całego czasu powrotu platformy i wspinania. Przywróciło
pliki użytkownika; to za krótki czas próby, nie śmierć ani pełne wejście.
Siódma próba zginęła wcześniej od żołnierza: strzał zlecony podczas reakcji na
obrażenia nie pokonał przeciwnika. Dalsza automatyzacja wymaga potwierdzania
wyniku walki, zamiast zakładać skuteczność naciśnięcia przycisku. APK nie zmieniano.

Osobna jawnie kontrolowana próba potwierdziła wejście po wcześniejszym
przytrzymaniu „góra”: x9568,y3528,6, zdrowie 100. Obserwator pozwala teraz na trzy
przytrzymania po dwie sekundy, aby uwzględnić fazę powrotu platformy. Scena
kontrolowana usuwa przeciwników i ustawia zdrowie/amunicję przed początkowym
umieszczeniem bohatera. Nie zaliczamy jej jako naturalnego przejścia.

The eighth natural attempt confirmed a Soldier defeat before departure but again
missed the second ladder after boarding. The controlled landing offset was not
representative of every natural state: a real catnip pickup changes movement
speed. The helper's status-query round trips also allowed the carrier to move
past the sensor before Up began. The observer now presses Up during the boarding
jump, rather than waiting for post-landing queries. Controlled candidate r3
(`second-carrier-ladder-redmi-0.4.24-r3`) reaches the cap at (9568,3528.6), HP100.
This is still not a complete natural-route or campaign pass. Earlier r1/r2
controlled passes remain evidence only for their own fixture and input timing.

Ósma naturalna próba potwierdziła pokonanie żołnierza przed dalszym ruchem, lecz
ponownie minęła drabinę po wejściu na platformę. Naturalnie zdobyta kocimiętka
zmienia prędkość i miejsce lądowania; odczyty po lądowaniu pozwalały też platformie
wyjechać poza kolumnę drabiny przed naciśnięciem „góra”. Obserwator przytrzymuje
teraz wspinanie już podczas skoku. Próba kontrolowana r3 przeszła do szczytu
(9568,3528,6), zdrowie 100. Nie jest to ukończenie naturalnej trasy ani kampanii.
Poprzednie próby kontrolowane potwierdzają wyłącznie własne ustawienie i sterowanie.

## Natural ninth continuation / Dziewiąta naturalna kontynuacja

The corrected ordinary sequence now passes in the natural run too:
`natural-campaign-0.4.24-resume9/second-carrier-natural-ladder.json` records HP60,
x9568,y3528.6 at the ladder cap. The following ordinary left jump boarded the
real x9442 vertical elevator. Riding it and a short jump with held Up reached
the next ladder cap x9568,y2440.6, HP30 (`tower-transfer.json`). The next Soldier
subsequently killed the hero; the attempted longer jump/shot did not survive.
Level 1 remains incomplete. This is incremental natural route coverage, not a
single uninterrupted clear, all-level pass, FPS guarantee or 1.0 release.
After ending this owned run the real device configuration and save were pulled
again and matched both original backups byte for byte (`restoration.json`).

Poprawiona sekwencja zwykłych przycisków przeszła również w naturalnej próbie:
zdrowie 60, x9568,y3528,6 na szczycie drabiny. Kolejny skok w lewo wszedł na
prawdziwą pionową windę x9442. Przejazd i krótki skok z przytrzymaną wspinaczką
pozwoliły dotrzeć na następną drabinę x9568,y2440,6, zdrowie 30. Następny żołnierz
zabił jednak bohatera; próba dłuższego skoku ze strzałem nie zapewniła przeżycia.
Pierwszy poziom nadal nieukończony. Są to kolejne sprawdzone fragmenty naturalnej
trasy, nie nieprzerwane przejście całej gry ani gwarancja FPS czy wersja 1.0.
Po zakończeniu ponownie pobrano konfigurację i zapis z telefonu — oba pliki były
identyczne bajt w bajt z kopiami użytkownika sprzed próby.

[Huawei continuation and log-reader recovery / Kontynuacja na Huawei i odzyskiwanie logów](HUAWEI-CAMPAIGN-0.4.24.md).
