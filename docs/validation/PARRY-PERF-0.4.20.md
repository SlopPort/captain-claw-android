# Parry observations and diagnostic overhead / Parowanie i koszt diagnostyki

OpenAI Codex (LLM), 2026-10-22. Scoped observations, not a release declaration.

## Build and method

Huawei Android 10, ARM64. APK SHA-256 `58ac36886b396639b24432cdbc550c5fb1dba8eed5c1ae0e3acaec9efa199067`, version 0.4.20-dev. Both ARM libraries were checked for absence of the rejected tile-atlas implementation. The only native changes after 0.4.19 add diagnostic observations and an opt-in way to silence verbose preview diagnostics. Parry uses the existing random draw and predicate; it does not draw another random number or change damage rules.

## Twelve controlled sword fixtures

Reports: `parry-redtail-0.4.20`, `parry-tiger-0.4.20`, `parry-hermit-0.4.20`, four fresh-process cases each: enemy/hero above, left/right, 48 px fixture step, standing sword attack. Source-map actor definitions and health are used. Attack/roll AI states are disabled; parry remains enabled. Setup initializes hero HP to 100 and pistol ammunition to 99; no HP edits during the observed action, no shots, no protection. Configuration and saves restored after each prototype. This is not natural terrain or active-combat validation.

| Prototype | Enemy above: left/right | Hero above: left/right | Actual melee parry chance |
| --- | --- | --- | --- |
| Level13_RedTailPirate | damage / damage | parry / parry | 33% |
| Level14_TigerGuard | damage / damage | parry / parry | 33% |
| Level7_HermitCrab | parry / parry | no contact / no contact | 100% |

All six contacted attacks without HP loss logged a successful actual parry decision followed by the health resistance event. The four damaging contacts logged failed parries. The two noncontacts logged neither. These observations explain the new cases; they do not retrospectively prove the cause of every old non-damaging contact in the 180-case baseline. No hitbox expansion or damage rebalance was applied. Crab behavior matches its inherited 100% melee-parry definition; equivalence to original Monolith behavior is unconfirmed.

## Same-scene performance comparison

Three sequential 90-second observations on the same installed APK, level 9 at setup position (11027,5500), settled logical viewport 853x480. Protected stationary hero, no attacks. Discard the first 300-frame batch consistently; harmonic mean of the remaining 17 batches per run:

| Mode | FPS | Battery temperature before/after |
| --- | --- | --- |
| Verbose A | 58.229 | 33 / 33 C |
| Quiet | 58.859 | 34 / 34 C |
| Verbose B | 58.484 | 35 / 34 C |

`--quiet-diagnostics` warms up for ten seconds and disables verbose actor tracing, the preview badge and further command polling for that process. Periodic frame/phase/physics diagnostics remain; it does not alter game AI, physics or image rendering. The final position cannot be queried after polling stops and is explicitly marked unqueried. Before-position evidence and final screenshot remain. Battery temperature is not CPU temperature. These short sequential runs do not establish statistical significance, sustained 60 FPS or coverage of all maps. Quiet mode is a measurement option, not a claimed optimization. Reports are `quiet-perf-0.4.20-verbose-a`, `quiet-perf-0.4.20-quiet`, `quiet-perf-0.4.20-verbose-b`.

## Polski

Dwanaście nowych prób rozdzieliło kontakt szabli, utratę HP i blok przeciwnika. Wszystkie sześć trafień bez obrażeń w tych próbach miało potwierdzone parowanie, a dwa zamachy na kraba z wyższego stopnia nie miały kontaktu. Nie powiększono hitboxów ani nie zmieniono obrażeń. Próby mają wyłączone stany ofensywnej AI i przygotowany teren, więc nie zamykają audytu normalnej walki.

Wyłączenie części diagnostyki dało w krótkiej próbie około 58,86 FPS wobec 58,23 i 58,48 FPS w próbach przed i po. To nadal nie jest stałe 60 FPS. Odrzucony atlas kafelków pozostaje wyłącznie w archiwum eksperymentów: jego różnice obrazu nie spełniały wymaganego warunku jakości. Redmi będzie sprawdzony później; testów padów nie wykonywano.

## Touch regression

On this exact ARM APK, `touch-0.4.20-jump` passed all six focused-window gestures, including direct activity restoration and multitouch: short rises 73.1–73.5 px, held rise 155 px, takeoff 19–24 ms. `touch-0.4.20-score` and `touch-0.4.20-game-over` passed actual single-touch returns. Each fixture restores original configuration/progress. These are app-window injected gestures, not a claim of physical touchscreen latency.

## Starts without preview diagnostics

`production-start-0.4.20-level1..14` passed all fourteen actual map starts on this exact Huawei ARM APK with `PreviewIncompleteLevel14=false`, no mailbox commands, logical viewport 853x480 and three seconds after each load. A separate post-run check verified all saved configs and every log for `NOT LOADED:`, `LEVEL14 PREVIEW:`, unexpected commands and fatal markers. No matches. Checkpoint-zero test saves use HP 100, lives 3, bullets 10, magic 5, dynamite 3; original files were restored after each map. This confirms startup without preview bypasses, not traversal, boss balance or all-map FPS.
