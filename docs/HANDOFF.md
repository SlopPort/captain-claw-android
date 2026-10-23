# Handoff / Przekazanie projektu

Updated / Aktualizacja: 2026-10-23. Adaptation work: OpenAI Codex (LLM), guided
by human requirements and device feedback. Upstream OpenClaw authorship is separate.

**Scope update, 2026-10-23:** the human takes over natural campaign playtesting.
Redmi was authorized for this task on 2026-10-23. Its initially offline ADB
connection recovered; final 0.4.25 tests now run on Android 16.
See [current Redmi evidence](validation/REDMI-0.4.25.md). Respect current device allocation.
Latest candidate: [0.4.26 import checks](validation/IMPORT-FLOW-0.4.26.md) and
[signed candidate evidence](validation/RELEASE-0.4.26.md). Both phones retain the debug signature.
Preserve private-signing/ locally; never publish it. Earlier [0.4.25 checks and retained failures](validation/READINESS-0.4.25.md),
[twenty-minute Huawei measurement](validation/SUSTAINED-HUAWEI-0.4.25.md), and
[bounded ENOSPC](validation/IMPORT-FULL-DISK.md).
Do not resume autonomous campaign traversal. Continue technical checks and fixes;
use human campaign reports as evidence, recording APK, level and reproduction.

**Zmiana zakresu, 2026-10-23:** użytkownik przejmuje przechodzenie kampanii.
Użytkownik udostępnił Redmi do tego zadania. Początkowy stan offline ustąpił;
[bieżące próby 0.4.25](validation/REDMI-0.4.25.md) dotyczą Androida 16.
Nie wznawiaj samodzielnego przechodzenia. Kontynuuj kontrole techniczne i poprawki;
zgłoszenia użytkownika zapisuj z wersją APK, poziomem i sposobem odtworzenia.

## English

**0.4.26-dev is not release 1.0. No complete natural campaign clear exists.**
Six further retries did not extend the natural route; see
[retained failures and driver limitations](validation/CAMPAIGN-RETRIES-0.4.24.md).
Do not replay the old route blindly after knockback or a missed landing.
The experimental first-carrier helper has no device pass yet. All owners ended;
the final Huawei configuration/save comparison passed. [Game-data language
research and current limits](GAME-LANGUAGE.md) distinguish English UI from voices.
Start with [contributing](../CONTRIBUTING.en.md), [build](BUILDING.en.md),
[installation](INSTALL-EN.md), [release gates](ROADMAP-1.0.md), and
[upstream differences](UPSTREAM-DIFF.md). The last document is currently Polish.

The latest natural continuation used Huawei P9 Lite / Android 10 / 2 GB RAM.
It loaded an unchanged checkpoint actually written by the earlier Redmi run:
level 1, checkpoint 1, HP100, zero spare lives, pistol6, magic2, dynamite3.
It passed carriers, ladder transfers, the upper shaft, the Soldier encounter,
the next flag ledge and the first two cyclic pegs. A later group remains uncleared;
missed jumps reach the lower floor, where normal combat/pickups left HP85.
This is partial route coverage. The next persistent checkpoint and level exit
have not been reached naturally. [Exact evidence and failures](validation/HUAWEI-CAMPAIGN-0.4.24.md).

The human owns further route/campaign testing. Do not resume this autonomous
route. Continue technical installation, lifecycle, terrain/combat and compatibility
checks, and use human bug reports to reproduce failures. Technical teleports must
remain explicitly labelled; they are never natural progression evidence.
The former live phone session has ended and original user files were restored
byte for byte. Runtime position on the lower floor is not a new game save.
Ignored local evidence is not available to a fresh clone; reproduce a route or
use your own legitimate save and state its origin. Do not assume private reports exist.

`campaign_play.py` owns test backups and an app-local command mailbox.
`campaign_session.py` now reconnects its dead logcat reader from the last recorded
timestamp. The recovery was tested on Huawei without restarting the game or ADB
server. `campaign_log_reader.py` can supervise logs for an older live owner; its
stop marker terminates only that reader. Raw timestamp overlap can repeat a line;
consume each observation tick once. A reader timeout is not automatically a game bug.

55 FPS in a heavy Huawei scene is the human's accepted target, not an established
minimum on every map. Preserve image quality. Do not call the adaptation complete
because controlled map starts/boss fixtures passed. Physical controller tests are
currently excluded at the user's request. Redmi is authorized and online;
current work may also use Huawei and must preserve its
USB internet tether. No phone serial belongs in this document.

Remaining compatibility and release gates are maintained in the roadmap. New
contributors must distinguish documented historical notes from current proof.
Never describe this code as original Monolith source or assume game copyrights expired.

## Polski

**0.4.24-dev nie jest wersją 1.0. Całej kampanii nie ukończono naturalnie.**
Instrukcje: [współpraca](../CONTRIBUTING.md), [budowanie](BUILDING.md),
[instalacja](INSTALL-PL.md), [droga do 1.0](ROADMAP-1.0.md).

Ostatnia kontynuacja na Huawei przeszła ruchome platformy, przesiadki na drabiny,
górny szyb, żołnierza, dalszą półkę z flagą i pierwszą parę cyklicznych podestów.
Następna grupa nadal nie jest zaliczona. Po upadkach można wrócić windą; zwykła
walka i przedmioty pozostawiły zdrowie 85. Próba korzystała z niezmienionej kopii
prawdziwego zapisu: poziom 1, checkpoint 1, zdrowie 100, zero zapasowych żyć,
pistolet 6, magia 2, dynamit 3. [Wyniki i niepowodzenia](validation/HUAWEI-CAMPAIGN-0.4.24.md).

Następny krok to przejście podestów ze świadomym doborem fazy, trwały checkpoint 2,
koniec poziomu 1 i dalsza kampania. Pozycja z zakończonej próby nie jest nowym
zapisem gry. Własne pliki użytkownika zostały przywrócone i porównane bajt w bajt.
Nowa osoba nie ma prywatnego katalogu raportów: musi odtworzyć trasę lub jawnie
opisać pochodzenie własnego zapisu. Teleport, odporność i kontrolowana scena nie
zastępują naturalnego przejścia.

Odzyskiwanie przerwanego czytnika logów jest poprawką narzędzia, nie APK ani FPS.
Sprawdzono je na Huawei bez restartu gry i serwera ADB. Powtórzony graniczny wpis
należy odczytywać tylko raz. Brak próbek nie dowodzi błędu rozgrywki.

55 FPS w ciężkiej scenie jest zaakceptowanym celem, nie potwierdzonym minimum.
Testy fizycznych padów są wyłączone na życzenie użytkownika. Redmi jest obecnie
udostępniony do tych prób; Huawei może być używany bez zmian połączenia USB z internetem.
Nie publikuj numerów urządzeń, danych gry ani prywatnych raportów. Zachowaj autorów
OpenClaw i bibliotek oraz informację o pracy LLM. Pozostałe bramki wydania są w planie 1.0.
