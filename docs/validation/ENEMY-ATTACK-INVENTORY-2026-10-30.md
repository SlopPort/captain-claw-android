# Packaged enemy attack timing inventory - 2026-10-30

Generated with `python tools/audit_enemy_cadence.py --markdown docs/validation/ENEMY-ATTACK-INVENTORY-2026-10-30.md`.

APK SHA-256: `63478ba59d551d37ef9c1fffe3cf473287de09a4dc8c763eb213adc4eeb1c013`.

Coverage: **55 concrete enemy/encounter prototypes**, **76 configured attack actions**, **0 missing ANI files**. Bosses are included; special state machines are listed below. **26 actions select a different frame from the original ANI event-1 marker; 10 have no event-1 marker and need their custom original handler traced.**

All numbers are milliseconds. Frame indices start at zero. The original event-1 column is decoded ANI metadata: REA traced raw word 6 into the original interpreter result, used by shared strike and Soldier firing. A matching marker alone does not certify a custom handler or full timing parity. ANI totals are metadata from user-owned original assets; delays and damage-frame selection come from inherited packaged port XML. No original resources are included.

**Cycle is the nominal uninterrupted full attack sequence**, with delay once per sequence. Multiple actions share the total; do not add their repeated cycle cells. Event offsets are within each animation. Delay precedes the first animation only. Contact damage, hurt/parry interruptions, movement and visibility alter observed intervals.

The engine advances at most one animation frame per game update and carries residual time. Setting the same animation does not reset it. Frame-zero callbacks and state transitions require runtime checking: these nominal offsets are not a promise of exact first-hit timing or measured DPS. Difficulty affects damage/healing, not cadence.

| Prototype | State / animation | Frames / ANI duration | Damage frame / animation offset | Added delay | Nominal sequence cycle | Original ANI event-1 frames |
|---|---|---:|---:|---:|---:|---|
| ActorPrototype_Level10_CrazyHook | MeleeAttack / strike1 | 5 / 275 | 3 / 170 | 250 | 525 | 2 |
| ActorPrototype_Level10_CrazyHook | DuckMeleeAttack / strike2 | 3 / 330 | 2 / 260 | 250 | 580 | 1 |
| ActorPrototype_Level10_Marrow | MeleeAttack / strike2 | 5 / 410 | 3 / 250 | 0 | 410 | 3 |
| ActorPrototype_Level10_Marrow | RangedAttack / strike1 | 8 / 530 | 4 / 280 | 100 | 630 | 4 |
| ActorPrototype_Level10_MarrowParrot | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level10_PegLeg | RangedAttack / strike1 | 4 / 500 | 2 / 300 | 250 | 1250 | 2 |
| ActorPrototype_Level10_PegLeg | RangedAttack / strike2 | 4 / 500 | 2 / 300 | 250 | 1250 | 2 |
| ActorPrototype_Level10_Seagull | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level11_Fish | MeleeAttack / strike1 | 6 / 800 | 2 / 330 | 0 | 800 | none / custom |
| ActorPrototype_Level11_Laser | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level11_Mercat | MeleeAttack / strike1 | 4 / 300 | 2 / 150 | 300 | 600 | 2 |
| ActorPrototype_Level11_Mercat | RangedAttack / strike1 | 4 / 300 | 2 / 150 | 500 | 800 | 2 |
| ActorPrototype_Level11_Siren | RangedAttack / strike1 | 3 / 1280 | 2 / 280 | 500 | 1780 | none / custom |
| ActorPrototype_Level12_Aquatis | MeleeAttack / strike1 | 4 / 390 | 3 / 190 | 200 | 590 | none / custom |
| ActorPrototype_Level12_Fish | MeleeAttack / strike1 | 6 / 800 | 2 / 330 | 0 | 800 | none / custom |
| ActorPrototype_Level12_Mercat | MeleeAttack / strike1 | 4 / 300 | 2 / 150 | 300 | 600 | 2 |
| ActorPrototype_Level12_Mercat | RangedAttack / strike1 | 4 / 300 | 2 / 150 | 500 | 800 | 2 |
| ActorPrototype_Level12_Siren | RangedAttack / strike1 | 3 / 1280 | 2 / 280 | 500 | 1780 | none / custom |
| ActorPrototype_Level13_BearSailor | MeleeAttack / strike1 | 5 / 590 | 3 / 370 | 0 | 590 | 2 |
| ActorPrototype_Level13_BearSailor | DuckMeleeAttack / strike4 | 3 / 180 | 0 / 0 | 0 | 180 | 0 |
| ActorPrototype_Level13_Chameleon | MeleeAttack / strike1 | 5 / 250 | 2 / 150 | 150 | 400 | 1 |
| ActorPrototype_Level13_RedTail | MeleeAttack / strike8 | 4 / 300 | 1 / 50 | 0 | 300 | none / custom |
| ActorPrototype_Level13_RedTail | RangedAttack / strike4 | 6 / 580 | 3 / 210 | 250 | 830 | none / custom |
| ActorPrototype_Level13_RedTailPirate | MeleeAttack / strike1 | 6 / 280 | 3 / 150 | 150 | 430 | 2, 3 |
| ActorPrototype_Level13_RedTailPirate | DuckMeleeAttack / strike2 | 5 / 220 | 2 / 100 | 250 | 470 | 2 |
| ActorPrototype_Level14_Chameleon | MeleeAttack / strike1 | 5 / 250 | 2 / 150 | 150 | 400 | 1 |
| ActorPrototype_Level14_Omar | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level14_TigerGuard | MeleeAttack / strike2 | 6 / 440 | 2 / 140 | 150 | 590 | none / custom |
| ActorPrototype_Level14_TigerGuard | DuckMeleeAttack / strike1 | 3 / 270 | 1 / 70 | 250 | 520 | none / custom |
| ActorPrototype_Level1_Officer | MeleeAttack / strike | 6 / 770 | 3 / 480 | 0 | 770 | 3 |
| ActorPrototype_Level1_Officer | DuckMeleeAttack / strike1 | 5 / 530 | 2 / 190 | 0 | 530 | 2 |
| ActorPrototype_Level1_Rat | RangedAttack / throweastwest | 3 / 1750 | 2 / 1500 | 0 | 1750 | 2 |
| ActorPrototype_Level1_Soldier | MeleeAttack / strike1 | 9 / 630 | 4 / 160 | 0 | 630 | 2 |
| ActorPrototype_Level1_Soldier | RangedAttack / strike | 6 / 1250 | 2 / 700 | 0 | 1250 | 3 |
| ActorPrototype_Level1_Soldier | DuckRangedAttack / strike | 6 / 1250 | 2 / 700 | 0 | 1250 | 3 |
| ActorPrototype_Level2_LaRaux | MeleeAttack / strike | 5 / 350 | 3 / 150 | 300-600 | 650-950 | 4 |
| ActorPrototype_Level2_Officer | MeleeAttack / strike | 6 / 770 | 3 / 480 | 0 | 770 | 3 |
| ActorPrototype_Level2_Officer | DuckMeleeAttack / strike1 | 5 / 530 | 2 / 190 | 0 | 530 | 2 |
| ActorPrototype_Level2_PunkRat | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level2_Soldier | MeleeAttack / strike1 | 9 / 630 | 4 / 160 | 0 | 630 | 2 |
| ActorPrototype_Level2_Soldier | RangedAttack / strike | 6 / 1250 | 2 / 700 | 0 | 1250 | 3 |
| ActorPrototype_Level2_Soldier | DuckRangedAttack / strike2 | 8 / 680 | 3 / 275 | 0 | 680 | 4 |
| ActorPrototype_Level3_CutThroat | MeleeAttack / strike1 | 5 / 380 | 2 / 150 | 150 | 530 | 2 |
| ActorPrototype_Level3_CutThroat | RangedAttack / strike2 | 8 / 620 | 0 / 0 | 250 | 870 | 6 |
| ActorPrototype_Level3_CutThroat | DuckRangedAttack / strike3 | 8 / 640 | 0 / 0 | 250 | 890 | 6 |
| ActorPrototype_Level3_Rat | RangedAttack / throweastwest | 3 / 1750 | 2 / 1500 | 0 | 1750 | 2 |
| ActorPrototype_Level3_RobberThief | RangedAttack / strike1 | 11 / 1000 | 6 / 740 | 100 | 1100 | 5 |
| ActorPrototype_Level3_RobberThief | DuckRangedAttack / strike2 | 11 / 1000 | 6 / 740 | 100 | 1100 | 5 |
| ActorPrototype_Level4_CutThroat | MeleeAttack / strike1 | 5 / 380 | 2 / 150 | 150 | 530 | 2 |
| ActorPrototype_Level4_CutThroat | RangedAttack / strike2 | 8 / 620 | 0 / 0 | 250 | 870 | 6 |
| ActorPrototype_Level4_CutThroat | DuckRangedAttack / strike3 | 8 / 640 | 0 / 0 | 250 | 890 | 6 |
| ActorPrototype_Level4_Katherine | MeleeAttack / strike1 | 10 / 460 | 6 / 180 | 0 | 460 | 6 |
| ActorPrototype_Level4_Rat | RangedAttack / throweastwest | 3 / 1750 | 2 / 1500 | 0 | 1750 | 2 |
| ActorPrototype_Level4_RobberThief | RangedAttack / strike1 | 11 / 1000 | 6 / 740 | 100 | 1100 | 5 |
| ActorPrototype_Level4_RobberThief | DuckRangedAttack / strike2 | 11 / 1000 | 6 / 740 | 100 | 1100 | 5 |
| ActorPrototype_Level5_Seagull | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level5_TownGuard1 | MeleeAttack / strike2 | 9 / 570 | 5 / 410 | 0 | 570 | 4 |
| ActorPrototype_Level5_TownGuard1 | DuckMeleeAttack / strike1 | 11 / 580 | 5 / 350 | 0 | 580 | 5 |
| ActorPrototype_Level5_TownGuard2 | MeleeAttack / strike2 | 7 / 410 | 4 / 240 | 0 | 410 | 4 |
| ActorPrototype_Level5_TownGuard2 | DuckMeleeAttack / strike1 | 7 / 480 | 4 / 250 | 0 | 480 | 4 |
| ActorPrototype_Level6_Rat | RangedAttack / throweastwest | 3 / 1750 | 2 / 1500 | 0 | 1750 | 2 |
| ActorPrototype_Level6_Seagull | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level6_TownGuard1 | MeleeAttack / strike2 | 9 / 570 | 5 / 410 | 0 | 570 | 4 |
| ActorPrototype_Level6_TownGuard1 | DuckMeleeAttack / strike1 | 11 / 580 | 5 / 350 | 0 | 580 | 5 |
| ActorPrototype_Level6_TownGuard2 | MeleeAttack / strike2 | 7 / 410 | 4 / 240 | 0 | 410 | 4 |
| ActorPrototype_Level6_TownGuard2 | DuckMeleeAttack / strike1 | 7 / 480 | 4 / 250 | 0 | 480 | 4 |
| ActorPrototype_Level6_Wolvington | MeleeAttack / strike2 | 9 / 520 | 5 / 200 | 0 | 520 | 5 |
| ActorPrototype_Level6_Wolvington | RangedAttack / strike3 | 7 / 540 | 4 / 240 | 100 | 640 | 4 |
| ActorPrototype_Level7_BearSailor | MeleeAttack / strike1 | 5 / 590 | 3 / 370 | 0 | 590 | 2 |
| ActorPrototype_Level7_BearSailor | DuckMeleeAttack / strike4 | 3 / 180 | 0 / 0 | 0 | 180 | 0 |
| ActorPrototype_Level7_HermitCrab | MeleeAttack / strike1 | 5 / 180 | 4 / 80 | 150 | 330 | none / custom |
| ActorPrototype_Level7_RedTailPirate | MeleeAttack / strike1 | 6 / 280 | 3 / 150 | 150 | 430 | 2, 3 |
| ActorPrototype_Level7_RedTailPirate | DuckMeleeAttack / strike2 | 5 / 220 | 2 / 100 | 250 | 470 | 2 |
| ActorPrototype_Level7_Seagull | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level8_BearSailor | MeleeAttack / strike1 | 5 / 590 | 3 / 370 | 0 | 590 | 2 |
| ActorPrototype_Level8_BearSailor | DuckMeleeAttack / strike4 | 3 / 180 | 0 / 0 | 0 | 180 | 0 |
| ActorPrototype_Level8_Gabriel | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level8_GabrielPirate | MeleeAttack / strike1 | 6 / 280 | 3 / 150 | 150 | 430 | 2, 3 |
| ActorPrototype_Level8_GabrielPirate | DuckMeleeAttack / strike2 | 5 / 220 | 2 / 100 | 250 | 470 | 2 |
| ActorPrototype_Level8_PunkRat | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level8_RedTailPirate | MeleeAttack / strike1 | 6 / 280 | 3 / 150 | 150 | 430 | 2, 3 |
| ActorPrototype_Level8_RedTailPirate | DuckMeleeAttack / strike2 | 5 / 220 | 2 / 100 | 250 | 470 | 2 |
| ActorPrototype_Level8_Seagull | Special / contact AI; see below | - | - | - | - | - |
| ActorPrototype_Level9_CrazyHook | MeleeAttack / strike1 | 5 / 275 | 3 / 170 | 250 | 525 | 2 |
| ActorPrototype_Level9_CrazyHook | DuckMeleeAttack / strike2 | 3 / 330 | 2 / 260 | 250 | 580 | 1 |
| ActorPrototype_Level9_PegLeg | RangedAttack / strike1 | 4 / 500 | 2 / 300 | 250 | 1250 | 2 |
| ActorPrototype_Level9_PegLeg | RangedAttack / strike2 | 4 / 500 | 2 / 300 | 250 | 1250 | 2 |
| ActorPrototype_Level9_Seagull | Special / contact AI; see below | - | - | - | - | - |

## States outside the generic sequence formula

These scalar XML fields are inventory clues, not complete cadence calculations. Native encounter timers need separate source review.

- **ActorPrototype_Level10_Marrow / MarrowAIStateComponent**: StatePriority=100; BossDialogAnimation=home.
- **ActorPrototype_Level10_MarrowParrot / MarrowParrotAIStateComponent**: StatePriority=100; IdleAnim=idle.
- **ActorPrototype_Level10_Seagull / DiveAttackAIStateComponent**: StatePriority=20; DiveSound=/LEVEL5/SOUNDS/SEAGULL/SEAGULLDIVE.WAV; DiveInAnimation=dive3; DiveOutAnimation=flying; DiveSpeed=4.5.
- **ActorPrototype_Level12_Aquatis / AquatisAIStateComponent**: StatePriority=100; BossDialogAnimation=home.
- **ActorPrototype_Level12_Aquatis / AquatisArenaComponent**: no scalar XML timing fields.
- **ActorPrototype_Level14_Omar / OmarEncounterComponent**: no scalar XML timing fields.
- **ActorPrototype_Level2_PunkRat / PunkRatAIStateComponent**: StatePriority=10; CannonActorPrototype=ActorPrototype_Level2_PunkRatCannon; RatFireAnim=strike; RatRecoilAnim=recoil; CannonFireAnim=firing; CannonIdleAnim=home; RatFireAnimFrameIdx=2; CannonFireAnimFrameIdx=2; ProjectileActorPrototype=ActorPrototype_Level2_CannonBall.
- **ActorPrototype_Level5_Seagull / DiveAttackAIStateComponent**: StatePriority=20; DiveSound=/LEVEL5/SOUNDS/SEAGULL/SEAGULLDIVE.WAV; DiveInAnimation=dive3; DiveOutAnimation=flying; DiveSpeed=4.5.
- **ActorPrototype_Level6_Seagull / DiveAttackAIStateComponent**: StatePriority=20; DiveSound=/LEVEL5/SOUNDS/SEAGULL/SEAGULLDIVE.WAV; DiveInAnimation=dive3; DiveOutAnimation=flying; DiveSpeed=4.5.
- **ActorPrototype_Level7_Seagull / DiveAttackAIStateComponent**: StatePriority=20; DiveSound=/LEVEL5/SOUNDS/SEAGULL/SEAGULLDIVE.WAV; DiveInAnimation=dive3; DiveOutAnimation=flying; DiveSpeed=4.5.
- **ActorPrototype_Level8_Gabriel / GabrielAIStateComponent**: StatePriority=50; BossDialogAnimation=idle2; IdleAnim=idle1; ThrowBombAnim=strike7; FireCannonAnim=strike3; SpawnPirateAnim=strike2; ThrowBombAnimFrameIdx=2; FireCannonAnimFrameIdx=0; NumThrownBombs=3; NumSpawnedPirates=1; BombDamage=0; ActionMinInterval=2000; ActionMaxInterval=3500; ThrowBombSound=/LEVEL8/SOUNDS/GABRIEL/00400029.WAV; SummonPirateSound=/LEVEL8/SOUNDS/GABRIEL/00400011.WAV; FireCannonSound=/LEVEL8/SOUNDS/GABRIEL/00400015.WAV.
- **ActorPrototype_Level8_PunkRat / PunkRatAIStateComponent**: StatePriority=10; CannonActorPrototype=ActorPrototype_Level8_PunkRatCannon; RatFireAnim=strike; RatRecoilAnim=recoil; CannonFireAnim=firing; CannonIdleAnim=home; RatFireAnimFrameIdx=2; CannonFireAnimFrameIdx=2; ProjectileActorPrototype=ActorPrototype_Level8_CannonBall.
- **ActorPrototype_Level8_Seagull / DiveAttackAIStateComponent**: StatePriority=20; DiveSound=/LEVEL5/SOUNDS/SEAGULL/SEAGULLDIVE.WAV; DiveInAnimation=dive3; DiveOutAnimation=flying; DiveSpeed=4.5.
- **ActorPrototype_Level9_Seagull / DiveAttackAIStateComponent**: StatePriority=20; DiveSound=/LEVEL5/SOUNDS/SEAGULL/SEAGULLDIVE.WAV; DiveInAnimation=dive3; DiveOutAnimation=flying; DiveSpeed=4.5.

### Special animation metadata

| Prototype | Field / animation | Frames | ANI duration |
|---|---|---:|---:|
| ActorPrototype_Level10_MarrowParrot | IdleAnim / idle | 11 | 940 |
| ActorPrototype_Level10_Seagull | DiveInAnimation / dive3 | 1 | 0 |
| ActorPrototype_Level10_Seagull | DiveOutAnimation / flying | 6 | 720 |
| ActorPrototype_Level2_PunkRat | RatFireAnim / strike | 3 | 1750 |
| ActorPrototype_Level2_PunkRat | RatRecoilAnim / recoil | 3 | 750 |
| ActorPrototype_Level2_PunkRat | CannonFireAnim / firing | 6 | 500 |
| ActorPrototype_Level2_PunkRat | CannonIdleAnim / home | 1 | 0 |
| ActorPrototype_Level5_Seagull | DiveInAnimation / dive3 | 1 | 0 |
| ActorPrototype_Level5_Seagull | DiveOutAnimation / flying | 6 | 720 |
| ActorPrototype_Level6_Seagull | DiveInAnimation / dive3 | 1 | 0 |
| ActorPrototype_Level6_Seagull | DiveOutAnimation / flying | 6 | 720 |
| ActorPrototype_Level7_Seagull | DiveInAnimation / dive3 | 1 | 0 |
| ActorPrototype_Level7_Seagull | DiveOutAnimation / flying | 6 | 720 |
| ActorPrototype_Level8_Gabriel | IdleAnim / idle1 | 12 | 2420 |
| ActorPrototype_Level8_Gabriel | ThrowBombAnim / strike7 | 6 | 650 |
| ActorPrototype_Level8_Gabriel | FireCannonAnim / strike3 | 3 | 200 |
| ActorPrototype_Level8_Gabriel | SpawnPirateAnim / strike2 | 6 | 590 |
| ActorPrototype_Level8_PunkRat | RatFireAnim / strike | 3 | 1750 |
| ActorPrototype_Level8_PunkRat | RatRecoilAnim / recoil | 3 | 750 |
| ActorPrototype_Level8_PunkRat | CannonFireAnim / firing | 6 | 500 |
| ActorPrototype_Level8_PunkRat | CannonIdleAnim / home | 1 | 0 |
| ActorPrototype_Level8_Seagull | DiveInAnimation / dive3 | 1 | 0 |
| ActorPrototype_Level8_Seagull | DiveOutAnimation / flying | 6 | 720 |
| ActorPrototype_Level9_Seagull | DiveInAnimation / dive3 | 1 | 0 |
| ActorPrototype_Level9_Seagull | DiveOutAnimation / flying | 6 | 720 |

## Ignored timing fields

These are parser/configuration defects; no balance change is made by this audit.

- **ActorPrototype_Level13_RedTail / MeleeAttackAIStateComponent**: action-level `AttackDelay=750` is ignored; component-level effective value is `0`.

## Separate spawner and environmental-threat coverage

These are not additional ordinary enemy variants. Min/max spawn delay is added before the fire animation; it is not the whole shot interval. Map conversion can override fields.

- **ActorPrototype_Level10_PuffDartSpawner / ProjectileSpawnerComponent**: IdleAnim=INVISIBLE; FireAnim=OVERRIDEN_IN_CODE; IsAlwaysOn=false; StartSpawnDelay=0; MinSpawnDelay=650; MaxSpawnDelay=650; TriggerCollisionMask=2; ProjectileSpawnAnimFrameIdx=0; ProjectilePrototype=OVERRIDEN_IN_CODE; ProjectileDirection=Direction_Right; ANI duration unresolved/generated.
- **ActorPrototype_Level13_PuffDartSpawner / ProjectileSpawnerComponent**: IdleAnim=INVISIBLE; FireAnim=OVERRIDEN_IN_CODE; IsAlwaysOn=false; StartSpawnDelay=0; MinSpawnDelay=650; MaxSpawnDelay=650; TriggerCollisionMask=2; ProjectileSpawnAnimFrameIdx=0; ProjectilePrototype=OVERRIDEN_IN_CODE; ProjectileDirection=Direction_Right; ANI duration unresolved/generated.
- **ActorPrototype_Level14_FireballSpawner / ProjectileSpawnerComponent**: IdleAnim=INVISIBLE; FireAnim=OVERRIDDEN_IN_CODE; IsAlwaysOn=false; StartSpawnDelay=0; MinSpawnDelay=1500; MaxSpawnDelay=1500; TriggerCollisionMask=2; ProjectileSpawnAnimFrameIdx=7; ProjectilePrototype=ActorPrototype_Level14_Fireball; ProjectileDirection=Direction_Right; ANI duration unresolved/generated.
- **ActorPrototype_Level14_LavaGeyser / LavaGeyserComponent**: StartDelay=0; RestMs=1000; Damage=10; FirstActiveFrame=4; LastActiveFrame=18; PulseMs=1000; ANI duration unresolved/generated.
- **ActorPrototype_Level14_LavaHand / ProjectileSpawnerComponent**: IdleAnim=INVISIBLE; FireAnim=lavahand; IsAlwaysOn=true; StartSpawnDelay=0; MinSpawnDelay=1500; MaxSpawnDelay=1500; TriggerCollisionMask=0; ProjectileSpawnAnimFrameIdx=11; ProjectilePrototype=ActorPrototype_Level14_LavaHandProjectile; ProjectileDirection=Direction_Left; fire ANI=1060 ms.
- **ActorPrototype_Level14_LavaMouth / LavaMouthComponent**: StartDelay=0; RestMs=1000; Damage=10; FirstActiveFrame=1; LastActiveFrame=18; PulseMs=1000; ANI duration unresolved/generated.
- **ActorPrototype_Level2_TowerCannonLeft / ProjectileSpawnerComponent**: IdleAnim=home; FireAnim=firing; IsAlwaysOn=true; StartSpawnDelay=0; MinSpawnDelay=500; MaxSpawnDelay=1500; TriggerCollisionMask=2; ProjectileSpawnAnimFrameIdx=1; ProjectilePrototype=ActorPrototype_Level2_CannonBall; ProjectileDirection=Direction_Left; fire ANI=525 ms.
- **ActorPrototype_Level2_TowerCannonRight / ProjectileSpawnerComponent**: IdleAnim=home; FireAnim=firing; IsAlwaysOn=true; StartSpawnDelay=0; MinSpawnDelay=500; MaxSpawnDelay=1500; TriggerCollisionMask=2; ProjectileSpawnAnimFrameIdx=1; ProjectilePrototype=ActorPrototype_Level2_CannonBall; ProjectileDirection=Direction_Right; fire ANI=525 ms.
- **ActorPrototype_Level9_PuffDartSpawner / ProjectileSpawnerComponent**: IdleAnim=INVISIBLE; FireAnim=OVERRIDEN_IN_CODE; IsAlwaysOn=false; StartSpawnDelay=0; MinSpawnDelay=650; MaxSpawnDelay=650; TriggerCollisionMask=2; ProjectileSpawnAnimFrameIdx=0; ProjectilePrototype=OVERRIDEN_IN_CODE; ProjectileDirection=Direction_Right; ANI duration unresolved/generated.
- **ActorPrototype_Level9_SkullCannon / ProjectileSpawnerComponent**: IdleAnim=home; FireAnim=firing; IsAlwaysOn=true; StartSpawnDelay=0; MinSpawnDelay=500; MaxSpawnDelay=1500; TriggerCollisionMask=2; ProjectileSpawnAnimFrameIdx=1; ProjectilePrototype=ActorPrototype_Level9_CannonBall; ProjectileDirection=Direction_Right; fire ANI=700 ms.

Native/map-generated Aquatis tentacles are additional actors, not packaged EnemyAI prototypes. Their timers and the Laser contact actor need source/terrain analysis; they are not assigned a fabricated generic attack cycle.

## Reproducibility and limitations

The script uses `audit_combat.merge`, matching engine first-element-by-path inheritance. ANI frames use `<9H2B` after `<8I` and the image path; duration is the sixth 16-bit field. NUL-terminated event names are skipped. Trailing bytes fail validation. Private JSON records per-frame durations and hashes; the public table contains derived metadata.

Frame-zero findings: Bear Sailor crouched melee and Cut Throat ranged actions target frame zero. `AnimationComponent::SetAnimation` calls `OnAnimationFrameStarted` but does not notify frame-changed observers on reset; the generic attack observer listens to frame-changed. A fresh state therefore waits until the first wrap to frame zero, rather than delivering the event at nominal offset zero. This warrants a dedicated runtime test before changing timing.

This inventory does not establish original executable parity. OpenAI Codex (LLM) produced the tooling and report. Human original-Windows captures are still needed for runtime parity. See the [comparison and measured results](ENEMY-ATTACK-AUDIT-2026-10-30.md) and [special encounter timing](SPECIAL-ENEMY-CADENCE-2026-10-30.md).
