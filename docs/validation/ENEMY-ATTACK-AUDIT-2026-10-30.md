# Enemy attack-speed audit - 2026-10-30

Follow-up: [debug 0.4.37 fixes and final tests](UPDATE-0.4.37.md) address the confirmed frame/dispatch/delay issues below. Original analysis also confirms Gabriel uniform selection; unused weights are not a balancing defect. This report retains its original debug36 scope.

**Result: 26 of 76 configured attack actions use a different frame from the original ANI event-1 marker; 40 match it and 10 require custom-handler analysis. The port timing inventory is complete for its packaged enemy prototypes, but exact original-game cadence parity is not established.** Confirmed port issues and reconstruction gaps are listed separately. This audit changes no combat balance or APK. Analysis, documentation and fixtures were produced by OpenAI Codex (LLM), following anonymous human feedback.

## What was checked

- **55 concrete EnemyAI/encounter prototypes, representing 30 names/families, and 76 configured attack actions:** inherited XML, ANI duration, damage frame, component delay and multi-action sequence. All 76 referenced ANI files were present and frame indices valid. Laser is an unused/skipped prototype, not a functioning encounter certified by the count.
- **Ten separate environmental/spawner prototypes**, plus dynamic Aquatis tentacles and native Omar logic. These do not use one universal melee-cooldown formula.
- **15 ordinary-enemy physical cases on Huawei**, plus a separate crouched ranged Cut Throat case. Another attempted Bear Sailor low-attack case stayed in standing strike; it does not validate that low attack.
- **Original executable comparison with REA:** original ANI event decoder, shared strike/event/Home/pause paths and selected family decisions; 13 additional constructor/vtable bindings. Complete per-family original timing and original-Windows runtime measurements remain open.

Artifacts: local debug **0.4.36-dev**, APK SHA-256 `63478ba59d551d37ef9c1fffe3cf473287de09a4dc8c763eb213adc4eeb1c013`; packaged support SHA-256 `380d6e1a83fe5d09f61951e4555e03dccbb443f8885bce26668cbd0802d9c4a6`. Audit source baseline is commit `18c3bc2`. Original binary identity and evidence are in the [original comparison](ORIGINAL-ENEMY-CADENCE-2026-10-30.md). The Windows executable is a supplied CrazyHook distribution, not a certified pristine release.

## Findings and priorities

| Priority | Finding | Interpretation / next step |
|---|---|---|
| High | Original event marker / port hit frame differs in 26 actions (including repeated level variants). | Decoder, interpreter and shared strike / Soldier firing paths are traced. Soldier melee is 100 ms later in animation-relative metadata; its standing shot is 50 ms earlier. Le Rauxe selects 150 ms versus the original marker at 250 ms. See the original evidence for exact scope. Do not change all markers blindly: ten actions have no event-1 marker. |
| High | Red Tail melee delay 750 is nested inside AttackAction and ignored. Effective delay is zero; nominal cycle 300 ms. | Confirmed parser/config mismatch. Correcting placement would yield a nominal 1050 ms cycle, but original equivalence still needs a dedicated comparison. No unverified global slowdown. |
| High | Generic attack callbacks do not fire for reset frame zero. Bear Sailor low attack and Cut Throat ranged attacks use frame zero. | The first event waits for the first wrap instead of occurring at nominal offset zero. Repeat period and first-hit latency must be tested separately before changing dispatch. |
| Medium | Gabriel stores action weights and reuse times but selects uniformly without using those fields. | Confirmed unused policy metadata. Establish intended/original policy before implementing guessed weights. |
| Medium | Port generic AI repeats the selected sequence while its sensor/LOS permits it. Original Officer, Robber Thief and Peg Leg have different decision paths. | Shared ANI data does not prove shared attack frequency. Peg Leg timer/stance selection is particularly unlike the fixed two-action port sequence. |
| Medium | Original STRIKE dispatch uses an animation result/event; port hardcodes frame indices. | Original raw word-6 event loading is now traced and all 76 selections compared. Full custom-handler behavior and Windows runtime checks remain open. |
| Existing limitation | Le Rauxe range delay applies before every port strike; original has a conditional Home pause branch. | Keep the current approximation labelled. The protected debug36 encounter previously measured 707-932 ms between strikes; this is port evidence, not original parity. |
| Existing limitation | Laser map logic is explicitly skipped. | Existing missing behavior, not a correctly matched zero attack speed. |

## Measured port intervals

Each number is the median elapsed wall-clock interval between logged **damage/projectile emission frames of the same animation**, not accepted damage on Claw. Initial separation was 70 px on an isolated flat arena. The player was protected, other enemies were removed between cases, no player attacks were sent and enemy HP was not edited. This is a technical fixture, not natural campaign progression. State switches can lengthen mixed samples. The full private log retains every interval.

| Prototype | Animation | Events | Median interval (ms) |
|---|---|---:|---:|
| Level1_Officer | strike | 9 | 766.0 |
| Level1_Soldier | strike1 | 11 | 628.0 |
| Level3_CutThroat | strike2 | 1 | - |
| Level3_CutThroat | strike1 | 12 | 532.0 |
| Level3_RobberThief | strike1 | 7 | 1100.0 |
| Level5_TownGuard1 | strike2 | 12 | 571.0 |
| Level5_TownGuard2 | strike2 | 18 | 411.0 |
| Level7_BearSailor | strike1 | 12 | 588.0 |
| Level7_RedTailPirate | strike1 | 16 | 427.0 |
| Level10_CrazyHook | strike1 | 13 | 528.5 |
| Level10_PegLeg | strike1 | 5 | 1280.0 |
| Level10_PegLeg | strike2 | 5 | 1266.5 |
| Level11_Mercat | strike1 | 11 | 599.0 |
| Level11_Siren | strike1 | 4 | 1774.0 |
| Level13_BearSailor | strike1 | 12 | 590.0 |
| Level13_Chameleon | strike1 | 18 | 399.0 |
| Level14_TigerGuard | strike2 | 8 | 598.0 |
| Level14_TigerGuard | strike1 | 2 | 2827.0 |

Peg Leg values compare the same animation in successive two-action sequences, not each individual shot. Tiger Guard strike1 appeared only twice with state changes between; its 2827 ms interval must **not** be treated as the low-attack base cooldown. Cut Throat strike2 appeared once during the initial transition, so no repeat estimate was assigned.

A separate 250 px crouched Cut Throat fixture produced five strike3 events: intervals 891, 899, 869 and 911 ms, median **895 ms**, against nominal 890 ms. The attempted crouched Bear Sailor fixture produced strike1 only, median 590 ms; it did not reach strike4.

Configuration and saves were restored byte for byte after fixtures. Huawei alone was used; Redmi was not queried. USB/tethering settings and the shared ADB server were not changed. No original-Windows runtime was measured.

## Family coverage and original comparison status

Nominal cycles below are milliseconds, not measured original rates. Exact per-level/action details are in the [76-action inventory](ENEMY-ATTACK-INVENTORY-2026-10-30.md). "Entry traced" means original constructor/virtual entry evidence only; it does not certify the full cadence.

| Family / name | Port nominal configured sequence cycles | Original comparison status |
|---|---|---|
| Aquatis | 590 | Original full timing policy unresolved; port source/data audited. |
| BearSailor | 180, 590 | Original constructor / virtual entry traced; full timing policy unresolved. |
| Chameleon | 400 | Original constructor / virtual entry traced; full timing policy unresolved. |
| CrazyHook | 525, 580 | Original constructor / virtual entry traced; full timing policy unresolved. |
| CutThroat | 530, 870, 890 | Original constructor / virtual entry traced; full timing policy unresolved. |
| Fish | 800 | Original full timing policy unresolved; port source/data audited. |
| Gabriel | Special / contact / encounter; see companion report | Original full timing policy unresolved; port source/data audited. |
| GabrielPirate | 430, 470 | Original full timing policy unresolved; port source/data audited. |
| HermitCrab | 330 | Original full timing policy unresolved; port source/data audited. |
| Katherine | 460 | Original full timing policy unresolved; port source/data audited. |
| LaRaux | 650-950 | Conditional original pause branch traced; per-strike port delay is an approximation. |
| Laser | Special / contact / encounter; see companion report | Port map conversion skips it; original full behavior unresolved. |
| Marrow | 410, 630 | Original full timing policy unresolved; port source/data audited. |
| MarrowParrot | Special / contact / encounter; see companion report | Original full timing policy unresolved; port source/data audited. |
| Mercat | 600, 800 | Original constructor / virtual entry traced; full timing policy unresolved. |
| Officer | 530, 770 | Home directly chooses shared strike in close classes; full elapsed timing not measured. |
| Omar | Special / contact / encounter; see companion report | Original full timing policy unresolved; port source/data audited. |
| PegLeg | 1250 | Timer-gated and stance/level-based attack selection differs from fixed port pair; exact original periods unresolved. |
| PunkRat | Special / contact / encounter; see companion report | Original constructor / virtual entry traced; full timing policy unresolved. |
| Rat | 1750 | Original full timing policy unresolved; port source/data audited. |
| RedTail | 300, 830 | Original constructor / virtual entry traced; full timing policy unresolved. |
| RedTailPirate | 430, 470 | Strike wrapper reaches shared strike; no full original cadence certification. |
| RobberThief | 1100 | LOS / vertical / random firing gate traced; full timer and repeat policy unresolved. |
| Seagull | Special / contact / encounter; see companion report | Original full timing policy unresolved; port source/data audited. |
| Siren | 1780 | Original constructor / virtual entry traced; full timing policy unresolved. |
| Soldier | 630, 680, 1250 | Shared strike, firing setup/update and bounded Home instructions traced; exact rates unresolved. |
| TigerGuard | 520, 590 | Original constructor / virtual entry traced; full timing policy unresolved. |
| TownGuard1 | 570, 580 | Original full timing policy unresolved; port source/data audited. |
| TownGuard2 | 410, 480 | Original full timing policy unresolved; port source/data audited. |
| Wolvington | 520, 640 | Original full timing policy unresolved; port source/data audited. |

## Reproduce and extend

1. Build or supply the exact APK and your own original Assets directory. Run `python tools/audit_enemy_cadence.py --markdown docs/validation/ENEMY-ATTACK-INVENTORY-2026-10-30.md`. Proprietary assets are never copied to the repository.
2. For a newly authorized physical-device fixture, set process-local ANDROID_SERIAL, then run `python tools/audit_combat.py` and `python tools/enemy_cadence_smoke.py --report <new-private-report-name>`. The tool requires the installed APK to match the local APK and checks native index ordering before changing user files. Do not use another worker's phone.
3. Compare first entry, uninterrupted repeat, hurt/parry recovery and above/below terrain separately. Match distance, player posture and map object overrides. Never infer original cadence by adding the same pause to all actors.

Engine review: Animation updates at most one frame per game update and carries residual time; animation switches can discard residual time. Zero-duration frames still consume an update in the port, so low FPS can add timing error and ordinary ANI sums are nominal. Current difficulty presets change damage/healing, not animation duration or attack delay. Attack attempts, hitbox overlap, immunity and hurt animation are separate questions; this audit alone does not resolve the reported staircase counterattack fairness.

## Completion ledger

| Question | Status |
|---|---|
| Every concrete packaged enemy/encounter prototype and configured attack action inventoried | Answered for the recorded APK |
| Special/native attack and environmental timers reviewed | Answered at source level; map/runtime parity remains partial |
| Physical intervals checked against port configuration | Answered for 15 ordinary cases + separate ranged case; not all stances / levels |
| Original animation-event decoder and all 76 port marker selections compared | Answered: 40 marker matches / 26 mismatches / 10 no-marker custom cases |
| Original shared attack/decision mechanism compared | Partially answered with retained evidence |
| Exact original attack speed and damage-frame parity for every family | **Unresolved; not certified by this audit** |

Companion reports: [complete inventory](ENEMY-ATTACK-INVENTORY-2026-10-30.md), [special mechanisms](SPECIAL-ENEMY-CADENCE-2026-10-30.md), [original evidence](ORIGINAL-ENEMY-CADENCE-2026-10-30.md).

Validation: inventory counts/frame bounds/marker classification, Markdown column widths and local links passed. The event aggregator was rechecked against saved physical logs. Repository validation reported 355 source files and no errors; the pre-commit public-history scan reported no private-data findings. No production/gameplay code changed, so no new APK build or balance regression pass is claimed.
