# Active normal-enemy audit

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-23. This is isolated technical coverage, not campaign QA.
45 level-specific prototypes were visited with offensive AI enabled, normal damage,
fresh processes, both sides and both height relations. Standing sword input was
100 ms; setup HP100/pistol99, no healing or pistol shots during observation.

There are **180 valid unique side/relation action observations**: 178 on 0.4.26
ARM debug SHA `f32e9e96e64b91dd12ea7eff0303a97ea3c7abf1d9b16fbe08f6fa4023a3cb1f`,
including two PunkRat supplements, and two TigerGuard supplements on 0.4.27
SHA `e5ae5febf62b009578d320b391078e8b47b1d78825df7398e2bfa89e602e68cb`.
Correction to avoid double counting: the 176 already includes the four partial
48 px actions (two per exceptional prototype), and excludes the superseded
partial GabrielPirate retry. The supplements add four, giving 180 overall.
Native debug libraries are byte-identical between these versions.

Most setups used a 48 px solid step. TigerGuard and PunkRat hero-above setups
failed the height guard at 48 px, so those two failed cases were retained and
separate 64 px setups were tried on both sides. They are **not** a complete
uniform 48 px matrix. Step height is not actual hurtbox separation: PunkRat's
64 px setup had only 2 px initial bottom difference; TigerGuard's moving/airborne
body also changes height during the observation. Inspect actual boxes per frame
before attributing a hit or miss to geometry.

| Index | Prototype | Valid 48 px setup actions | Supplemental 64 px setup |
| --- | --- | --- | --- |
| 0 | Level10_CrazyHook | 4 | 0 |
| 1 | Level10_PegLeg | 4 | 0 |
| 2 | Level10_Seagull | 4 | 0 |
| 3 | Level11_Fish | 4 | 0 |
| 4 | Level11_Mercat | 4 | 0 |
| 5 | Level11_Siren | 4 | 0 |
| 6 | Level12_Fish | 4 | 0 |
| 7 | Level12_Mercat | 4 | 0 |
| 8 | Level12_Siren | 4 | 0 |
| 9 | Level13_BearSailor | 4 | 0 |
| 10 | Level13_Chameleon | 4 | 0 |
| 11 | Level13_RedTailPirate | 4 | 0 |
| 12 | Level14_Chameleon | 4 | 0 |
| 13 | Level14_TigerGuard | 2 | 2 |
| 14 | Level1_Officer | 4 | 0 |
| 15 | Level1_Rat | 4 | 0 |
| 16 | Level1_Soldier | 4 | 0 |
| 17 | Level2_Officer | 4 | 0 |
| 18 | Level2_PunkRat | 4 | 0 |
| 19 | Level2_Soldier | 4 | 0 |
| 20 | Level3_CutThroat | 4 | 0 |
| 21 | Level3_Rat | 4 | 0 |
| 22 | Level3_RobberThief | 4 | 0 |
| 23 | Level4_CutThroat | 4 | 0 |
| 24 | Level4_Rat | 4 | 0 |
| 25 | Level4_RobberThief | 4 | 0 |
| 26 | Level5_Seagull | 4 | 0 |
| 27 | Level5_TownGuard1 | 4 | 0 |
| 28 | Level5_TownGuard2 | 4 | 0 |
| 29 | Level6_Rat | 4 | 0 |
| 30 | Level6_Seagull | 4 | 0 |
| 31 | Level6_TownGuard1 | 4 | 0 |
| 32 | Level6_TownGuard2 | 4 | 0 |
| 33 | Level7_BearSailor | 4 | 0 |
| 34 | Level7_HermitCrab | 4 | 0 |
| 35 | Level7_RedTailPirate | 4 | 0 |
| 36 | Level7_Seagull | 4 | 0 |
| 37 | Level8_BearSailor | 4 | 0 |
| 38 | Level8_GabrielPirate | 4 | 0 |
| 39 | Level8_PunkRat | 2 | 2 |
| 40 | Level8_RedTailPirate | 4 | 0 |
| 41 | Level8_Seagull | 4 | 0 |
| 42 | Level9_CrazyHook | 4 | 0 |
| 43 | Level9_PegLeg | 4 | 0 |
| 44 | Level9_Seagull | 4 | 0 |

## Outcomes and limits

Mixed target losses, misses, parries and hero damage were observed. The legacy
`enemy_damage_observed` means any target loss/defeat, not necessarily Claw's sword.
New traces retain actor/source IDs; Rat explosions can damage their own owner.
See [Soldier/Rat, actual-hit escape and attribution](ACTIVE-SOLDIER-RAT-0.4.26.md)
and [Officer/ladder/edge evidence](TERRAIN-HEIGHTS-0.4.25.md). Area-request traces
prove a request, not creation of a Box2D body; the old area-created field remains
legacy. No balance change was justified solely by these observations.

Private source batches: active-normal-audit-redmi-0.4.26-r2 (indices 0–22),
active-normal-audit-huawei-0.4.26 (23–37 completed, 38 interrupted),
active-normal-audit-tail-redmi-0.4.26 (38–44), active-punkrat64-redmi-0.4.26,
active-tigerguard64-redmi-0.4.27. Original config/progress restored throughout.
No phone serial or user save contents are published.

## Retained failures

The initial Redmi start returned to an orphan DocumentsUI task after a test's
intentional force-stop. NEW_TASK|CLEAR_TOP fixed the test launch; r2 ran. This
was not evidence of a native engine crash. On Huawei, one later level-8 start
produced no expected completion marker. System events still showed the PID alive
until our cleanup; no native fatal signal or low-memory kill was proved. The
cause remains unconfirmed. GabrielPirate's separate four-case Huawei retry passed.
Subsequent 0.4.27 ordinary level-8 startup stress passed 10/10 with rendering and
restored files. Keep the original timeout; retries do not erase it.

Log capture now retains stderr, SDL Java window/focus events, reader reconnects
and timeout PIDs. Explicit invalid-height guards can be skipped only after file
restoration and absence of native fatal evidence; the suite never marks them as
successful actions. Natural terrain, every projectile, timing/fairness, physical
controllers and original Windows parity are not certified by this audit.
