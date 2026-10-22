# Droga do 1.0 / Road to 1.0

Stan: 2026-10-22. Dokument opracował OpenAI Codex (LLM). Wymagania i uwagi pochodzą od człowieka; OpenClaw i biblioteki zachowują autorstwo swoich twórców. Wyniki zawsze dotyczą konkretnego APK, urządzenia i scenariusza. To lista warunków wydania, nie deklaracja ukończenia prac.

## Polski

Zakres zlecenia od 2026-10-22: realizujemy pozostałe punkty, ale testy padów zostały odłożone na prośbę użytkownika. Dotyk pozostaje w zakresie. Odzyskiwanie przerwanego importu ma już [implementację i testy](validation/IMPORT-RECOVERY.md); pozostałe próby instalacji nadal są otwarte.

### Co mamy

- Lokalny projekt z historią Git, odtwarzalnymi łatkami OpenClaw/SDL, instrukcjami instalacji PL/EN, przypisaniem autorstwa i archiwum otwartych źródeł. Komercyjne dane gry pozostają oddzielnie.
- APK dla ARM64 i ARMv7; rzeczywiste próby na Huawei z Androidem 10 i Redmi z Androidem 16 oraz wybrane próby emulatorów Androida 5 i 15. Każdy nowszy kandydat wymaga własnego potwierdzenia; nie obiecujemy działania na wszystkich telefonach.
- Import własnego REZ lub ZIP, narzędzia zapisów, gałka i przyciski dotykowe, regulowana wysokość skoku, mapowanie pada oraz zapamiętywany wybór PL/EN dla naszych ekranów i napisów.
- Kontrolowane dowody przejść technicznych wszystkich 14 map i walk z bossami. Nie jest to naturalne przejście kampanii. [Szczegóły](validation/CAMPAIGN-1.0.md).
- Dodatkowe pomiary trafień powyżej/poniżej przeciwnika, przyjęcia ataku, animacji i ucieczki. Część prób używa izolowanego terenu i wyłączonej ofensywnej AI; ich ograniczenia są jawne. [Wyniki](validation/VERTICAL-COMBAT.md).

Przeprowadzono [180 prób dla 45 typów przeciwników](validation/VERTICAL-45-0.4.18.md), przy kroku 48 px i wyłączonych stanach ofensywnej AI. Nie zamyka to audytu aktywnej walki ani naturalnych schodów. Redmi jest już podłączony: aktualizacja, skok i dotykowe wyjścia przeszły na Androidzie 16 w 0.4.21. [Dokładny zakres](validation/REDMI-0.4.21.md); pełna kampania i końcowe pokrycie pozostają otwarte.

### Co trzeba zrobić, w kolejności

| Priorytet | Zadanie | Warunek zamknięcia |
| --- | --- | --- |
| P0 | Przejść całą kampanię normalną rozgrywką | Wszystkie 14 poziomów od początku do finału, bez teleportów, ochrony, edycji HP i nieskończonej amunicji. Zachować zasoby, sprawdzić checkpointy, śmierć, ponowne wczytanie i wyjścia z każdego ekranu. Zapisać wersję danych, trudność, APK i wyniki. |
| P0 | Dokończyć audyt walki i terenu | Rozszerzyć próby na pozostałe typy przeciwników, rzeczywiste schody, drabiny i krawędzie. Obie strony, różnice 16/32/48/64 px, stanie, kucanie, wznoszenie/opadanie, szabla i pociski. Oddzielić brak zasięgu od przerwanego wejścia i parowania; potwierdzić możliwość reakcji na ataki. |
| P0 | Domknąć mechaniki bossów | Zweryfikować fazy, niedozwolone trafienia, reset po śmierci i ponowne wejście, zapas amunicji oraz finał bez ułatwień. Dotychczasowe kontrolowane zwycięstwa nie dowodzą balansu ani dostępności zasobów w normalnej kampanii. |
| P0 | Sprawdzić sterowanie gracza | Rzeczywisty dotyk. Testy padów pozostają odłożone zgodnie z zakresem użytkownika. Menu, pauza, Game Over, podsumowanie, rozłączenie/wznowienie, zmiana przypisań, mieszanie pada i dotyku, krótkie tapnięcia i wielodotyk. Bez zasłaniania HUD. |
| P0 | Dopiąć instalację, aktualizacje i postęp | Początkująca osoba instaluje APK i importuje własne dane według obu instrukcji. Aktualizacja zachowuje dane/zapisy/przypisania. Sprawdzić mało miejsca, anulowanie, uszkodzoną paczkę, przerwany import, kopię i przywracanie. Odzyskiwanie importu ma 61 prób granic operacji i testy rzeczywistego zabicia procesu na Huawei; nadal sprawdzić selektor plików, duże paczki i rzeczywisty brak miejsca. |
| P0 | Dokończyć wydajność i stabilność | Celem optymalizacji pozostaje 60 FPS. Użytkownik zaakceptował próg 55 FPS w ciężkiej scenie Huawei; nie oznacza to potwierdzenia takiego minimum we wszystkich scenach. Mierzyć także gęste sceny i 20–30 minut obciążenia, pamięć oraz zachowanie po nagrzaniu. Dotychczasowe średnie około 58–60 FPS nie potwierdzają minimum 55 FPS: dłuższa próba zawierała niższe próbki. Porównywać ten sam widok i scenę; nie ograniczać fizyki, AI ani jakości dla pozornego wyniku. W próbie tej samej sceny ARMv7 osiągnął około 51–52 FPS, a ARM64 58–59; na Huawei pozostajemy przy ARM64. Zbadać opóźniony i zbyt niski skok przy bardzo długich klatkach emulatora Androida 15. |
| P0 | Potwierdzić zakres Androidów | Końcowy APK na Huawei i Redmi, 32/64 bity, minimalny Android, nowsze systemy, utrata fokusu, proces ubity przez system i powrót. Emulator Androida 15 z rzeczywistymi stronami 16 KB przeszedł menu PL/EN, skok i wyjście poziomu w osobnym buildzie x86_64 0.4.16; pozostaje końcowy build ARM na fizycznym urządzeniu 16 KB. Jawnie opisać urządzenia/emulatory i nieprzetestowane konfiguracje. |
| P1 | Ukończyć polski i angielski interfejs | Przetłumaczyć pozostałe nasze komunikaty, pomoc i menu; sprawdzić długie napisy, małe ekrany i obsługę padem. Menu i pomoc mają już własne napisy PL/EN oraz testy 109 nazwanych elementów w 0.4.16. Głosy, tła i oryginalne grafiki podsumowań nadal zależą od danych użytkownika. Wybór English nie oznacza przetłumaczonego dubbingu. |
| P1 | Porównać zachowanie z oryginałem | Kontrolowane porównania skoku, drabin, krawędzi, obrażeń i bossów przy tej samej wersji/danych/trudności i FPS. Oznaczać zgodność, różnicę zamierzoną, błąd i niewiadomą. Nie mamy potwierdzonego oryginalnego kodu Monolith; porównanie z OpenClaw nie jest porównaniem z tym kodem. [Pochodzenie źródeł](validation/ORIGINAL-COMPARISON.md). |
| P1 | Przygotować wydanie | Zamknąć błędy blokujące, opublikować uczciwe znane ograniczenia, sprawdzić czyste budowanie, licencje/NOTICE, brak danych komercyjnych i prywatnych. Przygotować podpisane APK, odpowiadające źródła i sumy SHA-256; klucz podpisu pozostaje prywatny. Utrzymać informację o pracy LLM i autorach projektów bazowych. Dopiero po spełnieniu warunków oznaczyć 1.0. Publikacja w sieci wymaga osobnego polecenia. |

Jeżeli uzgodniony próg wydajności lub inny wymagany warunek nie zostanie potwierdzony, pozostaje otwartym warunkiem. Nie przenosimy automatycznie wyniku starej wersji na nową ani nie zastępujemy przejścia gry teleportami. Ostateczny raport powinien wyraźnie rozdzielać: ukończone, blokujące wydanie oraz opcjonalne po 1.0.

## English

Scope from 2026-10-22: proceed with the remaining work, but defer controller testing at the user's request. Touch remains in scope. Interrupted-import recovery now has an [implementation and tests](validation/IMPORT-RECOVERY.md); the other installation checks remain open.

### What we have

- A local Git project, reproducible OpenClaw/SDL patches, Polish/English installation guides, attribution and an open-source archive. Commercial game data remains separate.
- ARM64/ARMv7 APKs, physical Huawei Android 10 and Redmi Android 16 testing, plus selected Android 5/15 emulator trials. Each newer candidate needs its own evidence; this does not establish support for every phone.
- Import of the player's own REZ/ZIP, save tools, touch stick/buttons, variable jump height, configurable controller actions and persisted PL/EN selection for our screens and added captions.
- Controlled evidence for technical transitions across all 14 maps and boss encounters. This is not a natural campaign playthrough. [Evidence](validation/CAMPAIGN-1.0.md).
- Additional measurements of attacks with the hero above/below enemies, accepted inputs, animations and escape. Some trials use isolated geometry or disabled offensive AI; their limits are explicit. [Results](validation/VERTICAL-COMBAT.md).

[180 fixtures across 45 enemy prototypes](validation/VERTICAL-45-0.4.18.md) completed with a 48 px step and offensive AI states disabled. Active combat and natural stairs remain open. Redmi is now connected: upgrade, jumping and touch exits passed on Android 16 in 0.4.21. [Exact scope](validation/REDMI-0.4.21.md); natural campaign and final coverage remain open.

### Work required, in order

| Priority | Task | Completion condition |
| --- | --- | --- |
| P0 | Complete a natural campaign playthrough | All 14 levels from the beginning to the finale, without teleports, protection, HP edits or infinite ammo. Preserve resources; exercise checkpoints, death/reload and every exit screen. Record data version, difficulty, APK and outcomes. |
| P0 | Finish combat and terrain coverage | Remaining enemy types on actual stairs, ladders and ledges. Both sides, 16/32/48/64 px offsets, standing/crouching, ascent/descent, sword and projectiles. Separate reach limits from interrupted input and parry; establish available reactions to attacks. |
| P0 | Close boss mechanics | Verify phase gates, rejected damage, death/re-entry resets, ammo availability and the finale without assistance. Existing controlled victories do not establish balance or normal-campaign resource availability. |
| P0 | Validate player controls | Real touch. Controller testing remains deferred at the user’s request. Menus, pause, Game Over, score, disconnect/resume, remapping, mixed controller/touch, short taps and multitouch. Keep controls clear of the HUD. |
| P0 | Finish installation, updates and progress safety | A novice installs/imports their own data using either guide. Updates preserve data, saves and bindings. Test low storage, cancellation, corrupt archives, interrupted import, backup and restore. Import recovery has 61 boundary checks and actual process-death tests on Huawei; still validate the picker, large archives and real full-disk behavior. |
| P0 | Finish performance and stability | 60 FPS remains the optimization target. The user accepts 55 FPS in the heavy Huawei scene; this does not establish a universal measured minimum. Include dense scenes, 20–30 minute runs, memory and warm-device behavior. The roughly 58–60 FPS averages do not establish a 55 FPS minimum: the longer observation included lower samples. Compare the same viewport/scene; do not reduce physics, AI or visual quality for a misleading gain. In the same-scene trial ARMv7 reached about 51–52 FPS versus ARM64 at 58–59; retain ARM64 on this Huawei. Investigate the delayed, low jump during very long frames on the Android-15 emulator. |
| P0 | Establish Android coverage | Final APK on Huawei/Redmi, 32/64 bit, minimum Android, newer systems, focus loss, system process death and recovery. The actual 16 KB Android-15 emulator passed menus, jump and a level exit on the separate 0.4.16 x86_64 build; final ARM build coverage on physical 16 KB hardware remains open. State exact devices/emulators and untested configurations. |
| P1 | Complete Polish and English UI | Translate remaining app-owned messages, help and menus; check long labels, small screens and controller navigation. Menus/help now have our own PL/EN labels and 109-item coverage in 0.4.16. Voices, backgrounds and original score-screen pictures remain data-dependent. Selecting English does not translate recorded dialogue. |
| P1 | Compare with the original game | Controlled jump, ladder, ledge, damage and boss comparisons using matching version/data/difficulty/FPS. Classify matches, intentional differences, bugs and unknowns. Original Monolith source has not been established as available; comparing with OpenClaw is not comparing with that source. [Source provenance](validation/ORIGINAL-COMPARISON.md). |
| P1 | Prepare the release | Close blockers, publish honest known limitations, verify clean builds, licenses/NOTICE and absence of commercial/private data. Prepare signed APKs, matching sources and SHA-256 checksums; keep the signing key private. Retain LLM-work disclosure and upstream attribution. Label 1.0 only after its gates pass. Online publication requires a separate instruction. |

If the agreed performance threshold or another required gate is not verified, it remains open. Do not transfer an older build's results to a newer APK or replace natural traversal with teleports. The final report should clearly separate completed work, release blockers and optional post-1.0 improvements.

Aktualizacja 0.4.21 / Update 0.4.21: [Redmi — 14 startów map, PL/EN, ARM64/ARMv7 i pomiary FPS](validation/REDMI-0.4.21.md), [sprzątanie importu i czysta kompilacja](validation/IMPORT-CLEANUP-0.4.21.md), [ograniczone próby aktywnego Tiger Guarda](validation/ACTIVE-TIGER-0.4.21.md). These results do not close the natural-campaign, agreed-performance or full-disk gates.

0.4.22: [kontrola konfiguracji przed importem / pre-publication config checks](validation/CONFIG-IMPORT-0.4.22.md) przeszła 11 przypadków na Androidzie 5/10/16. [20-minute Redmi 0.4.21 observation](validation/SUSTAINED-REDMI-0.4.21.md) averaged 59.998 FPS with occasional stalls; natural campaign, the accepted Huawei performance threshold, real full-disk and physical ARM 16 KB checks remain open.

## Zmiana kryterium wydajności / Performance acceptance update

2026-10-22: użytkownik zaakceptował dolny próg 55 FPS w ciężkiej scenie Huawei. 60 FPS pozostaje celem optymalizacji, ale nie jest już bezwzględnym warunkiem wydania w tej scenie. Nadal ujawniamy przycięcia i wyniki dłuższych prób. Priorytetem jest teraz naturalne przejście kampanii.

The user now accepts 55 FPS as the lower threshold in the heavy Huawei scene. 60 FPS remains an optimization target rather than an absolute release requirement there. Report frame-time stalls and sustained observations separately; natural campaign traversal is the current priority.

0.4.23: [awaria beczki znaleziona podczas naturalnej próby kampanii / powder-keg crash found during natural campaign attempt](validation/POWDER-KEG-0.4.23.md). Reproduced on 0.4.22, fixed and regression-tested on Redmi Android 16 and Huawei Android 10. The campaign itself remains incomplete.
