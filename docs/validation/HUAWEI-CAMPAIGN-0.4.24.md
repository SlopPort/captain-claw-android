# Huawei campaign continuation and log recovery / Kampania na Huawei i odzyskiwanie logów

## English

OpenAI Codex (LLM), 2026-10-23. Device: Huawei P9 Lite, Android 10,
2 GB RAM. Redmi was reserved for another task and was not operated in this run.
The USB tether and shared ADB server were not intentionally restarted.
APK: 0.4.24-dev, SHA-256
`583ec1d605527ba812e7da3da510a52dc4e08a2cc94f84c4733592051f2cc0a2`.
No game physics, collision, combat parameters or game assets changed in this work.

The continuation loads the exact game-written level-one checkpoint from the
[earlier natural run](NATURAL-CHECKPOINT-0.4.24.md) through the normal menu.
Its recorded resources are preserved: HP100, zero spare lives, pistol6, magic2,
dynamite3. The Huawei user's own files are backed up separately. Subsequent play
uses ordinary app-local keys and read-only observations, with no teleport,
resource replenishment, protection or added world geometry.

Observed natural progress:

- Crumbling pegs and both horizontal carrier/ladder transfers passed on Huawei.
- The real vertical elevator and upper ladder passed after a longer held jump.
  An earlier short-jump attempt missed and safely returned to the lower cap.
- Leaving the upper cap promptly, jumping onto the ledge and crouching allowed
  an ordinary pistol shot to defeat the Soldier; the hero retained HP30.
- The next flag ledge and ladder were reached. The two cyclic pegs at x10608
  and x10740 passed without catnip. Their pickups raised HP30 to HP60.
- The next group was not cleared. One peg was reached, then a later off-phase
  landing fell to the lower floor. The Officer there was defeated normally.
  Subsequent ordinary pickups raised health to HP85. Recovery attempts from
  the real trigger elevator are retained, including missed landings.

This is partial route coverage, not a level-one clear, full campaign pass,
minimum-FPS result or release 1.0. Local evidence is in the ignored report
`natural-campaign-huawei-0.4.24-resume1`; no map dumps or commercial data are
included in Git.

The logcat client stopped while the game kept running. The cause of the stream
interruption was not established. Several observer timeouts therefore had no
fresh samples; they are not evidence of failed jumps or a game crash. The stale
results and later fresh-log failures remain separate in the local evidence.

The test owner now detects a terminated **own logcat client**, reconnects from
its last recorded timestamp and appends evidence. It does not restart the ADB
server, game, USB connection or another device. A separate owned-reader helper
supports already running older owners and has an explicit stop marker.
An actual interrupted-client trial on Huawei recovered fresh native status
with the same game process. This improves test reliability; it is not an APK
performance or gameplay fix. Timestamp overlap can repeat the last log line;
observers must continue to consume sample ticks only once.

## Polski

Pracę wykonał OpenAI Codex (LLM), 23 października 2026. Próba dotyczy Huawei
P9 Lite z Androidem 10 i 2 GB RAM. Redmi pozostawiono drugiemu zadaniu.
Nie zlecano restartu współdzielonego serwera ADB ani połączenia USB z internetem.
APK i parametry rozgrywki nie zmieniły się; suma pliku jest podana wyżej.

Przez zwykłe menu wczytano dokładną kopię zapisu zdobytego wcześniej w naturalnej
próbie: poziom 1, checkpoint 1, zdrowie 100, zero zapasowych żyć, pistolet 6,
magia 2, dynamit 3. Własne pliki użytkownika Huawei zabezpieczono oddzielnie.
Dalej używano zwykłych przycisków i odczytów stanu. Nie teleportowano bohatera,
nie odnawiano zasobów poleceniami ani nie dodawano odporności lub terenu.

Przeszły kruche podesty, ruchome platformy i przesiadki na drabiny. Pionowa
winda i górna drabina również przeszły; wcześniejszy zbyt krótki skok zakończył
się bezpiecznym powrotem. Szybkie wyjście z drabiny, skok na pomost i kucnięcie
pozwoliły pokonać żołnierza normalnym strzałem, ze zdrowiem 30. Osiągnięto dalszą
półkę z flagą i drabinę. Pierwsza para cyklicznych podestów przeszła bez
kocimiętki; mikstury zwiększyły zdrowie do 60.

Następna grupa nadal nie jest zaliczona. Po wejściu na jeden podest kolejny
skok zakończył się upadkiem na dolną podłogę. Oficer został normalnie pokonany,
a dalszy przedmiot zwiększył zdrowie do 85. Zachowano nieudane powroty windą.
Nie jest to ukończenie pierwszego poziomu, całej kampanii, pomiar minimum FPS
ani potwierdzenie gotowości 1.0. Dowody lokalne są w wymienionym wyżej raporcie;
mapy i komercyjne dane pozostają poza Gitem.

Przerwał się klient odczytujący logi, chociaż gra nadal działała. Nie ustalono
przyczyny przerwania. Kilka komunikatów o braku fazy windy wynikało z braku
świeżych próbek, a nie z potwierdzonej awarii gry lub nieudanego skoku.
Nowe narzędzie odzyskuje wyłącznie własny czytnik, wznawia od ostatniego czasu
logu i dopisuje dowody. Nie restartuje ADB, gry, USB ani drugiego telefonu.
Rzeczywista próba zatrzymania własnego czytnika na Huawei potwierdziła odzyskanie
świeżego stanu bez zmiany procesu gry. To poprawka wiarygodności testów,
nie poprawka APK ani optymalizacja FPS. Graniczny wpis logu może się powtórzyć;
obserwatory nadal muszą odczytywać każdy znacznik próbki tylko raz.

## Final tool verification / Końcowe sprawdzenie narzędzia

The owner-idle integration test (`log-recovery-huawei-0.4.24-owner`) also passed:
its own logcat client was terminated, the idle loop reconnected, and an ordinary
status-query step completed with the same game process. No ADB-server restart
was requested. After cleanup, configuration and save pulled from Huawei were
byte-identical both to the integration-test backups and to the natural-run
original backups (`restoration.json`). The natural campaign remains incomplete.

Test głównej pętli również przeszedł: zatrzymano jej własny czytnik, pętla
odtworzyła odczyt i wykonała kolejny zwykły krok, bez zmiany procesu gry i bez
zlecania restartu ADB. Po zakończeniu ponownie pobrano konfigurację i zapis z
Huawei. Oba pliki były identyczne bajt w bajt z kopiami sprzed testu narzędzia
oraz sprzed naturalnej próby. Kampania nadal nie jest ukończona.
