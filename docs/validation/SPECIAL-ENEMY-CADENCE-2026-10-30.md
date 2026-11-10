# Special enemy and boss timing - 2026-10-30

Follow-up: [debug 0.4.37 fixes and final tests](UPDATE-0.4.37.md) address the confirmed frame/dispatch/delay issues below. Original analysis also confirms Gabriel uniform selection; unused weights are not a balancing defect. This report retains its original debug36 scope.

OpenAI Codex (LLM) reviewed the debug 0.4.36 source and packaged XML. This is a source audit, not original-Windows runtime verification. The [full inventory](ENEMY-ATTACK-INVENTORY-2026-10-30.md) contains every concrete EnemyAI/encounter prototype; the [comparison](ENEMY-ATTACK-AUDIT-2026-10-30.md) records evidence and remaining gaps. All times below are milliseconds.

| Actor / mechanism | Effective port behavior | Important qualification |
|---|---|---|
| Punk Rat, levels 2/8 | Fire ANI 1750 + recoil ANI 750 + random wait 300-1000: nominal 2800-3500 between equivalent shots | Rat starts cannon animation at its configured frame; cannon emits at its own frame. Camera visibility gates projectile creation. This is not a generic AttackDelay state. |
| Seagull, levels 5-10 | Dive to a sampled destination, return to initial height; vertical speed 4.5 | Travel distance and collision determine duration. On return the aggro list is cleared; reacquiring the sensor is required. A universal fixed cooldown would misdescribe this AI. |
| Peg Leg, levels 9/10 | Two 500 ms animations with a 250 ms sequence delay: nominal 1250 for the pair | The gap between the two shots differs from the gap between successive pairs. The original has additional timer/stance decisions; parity is not established. |
| Bear Sailor, levels 7/8/13 | Standing 590; low attack 180, no configured delay | Low attack targets frame zero. Fresh animation selection does not notify the generic frame-changed observer, so the first damage event waits for wraparound. Both first-hit and repeat behavior require distinguishing. |
| Cut Throat, levels 3/4 | Melee 530; standing ranged 870; duck ranged 890 | Ranged actions also target frame zero. Nominal ANI offset zero is not an immediate projectile upon entering the state. |
| Le Rauxe, level 2 | Strike ANI 350 + randomized 300-600 before each cycle: nominal 650-950 | Intentional port approximation. Original evidence establishes a conditional Home pause branch, not that every original strike has this mandatory delay. |
| Katherine, level 4 | Generic melee ANI 460, no extra delay | Movement, parry and hurt states interrupt the sequence. No exact original cadence certification. |
| Wolvington, level 6 | Melee 520; ranged 540 + delay 100 = 640 | Roll/dodge AI has its own reuse gate; it is not an extra fixed delay on every sword attack. |
| Gabriel, level 8 | Chooses an action after a sampled 2000-3500 interval (`>` comparison) | Timer runs independently of animation completion. Cannon-not-ready returns before resetting the timer and retries. Bomb/cannon damage occurs at animation frames; pirate summon is immediate at action selection. |
| Gabriel action metadata | Probabilities 40/30/30 and reuse values 2500/4000/3000 are stored in the action vector | Current update selects a uniform random vector item and does not filter these probability/reuse fields. The apparent per-action cooldowns do not control selection. Original probabilities remain unverified. |
| Marrow, level 10 | Generic melee 410; ranged 530 + delay 100 = 630 | Encounter alternates with parrot/arena movement. These numbers do not describe the complete encounter cycle. |
| Marrow's parrot | Wait 700, charge 1000, return 900: about 2600 per uninterrupted flight cycle | Parrot phase, 250 stun and 700 hit cooldown alter behavior. Flight timing is custom port logic. |
| Aquatis body, level 12 | Configured melee 390 + delay 200 = 590 | Arena puzzle and dynamically created tentacles are separate mechanisms. |
| Aquatis tentacles | Initial wait 700; after starting a strike, cooldown 1300; strike ANI 320; damage at frame 2 or later (nominal offset 170) | Cooldown counts concurrently with animation, not 1300 + 320. Requires Claw within 115 horizontal / 90 vertical units. Damage interrupts swinging. |
| Red Tail, level 13 | Melee ANI 300, effective extra delay **0**; ranged 580 + 250 = 830 | **Confirmed configuration/parser defect:** melee `AttackDelay=750` is nested inside AttackAction. Parser reads the component-level field only. Moving it would produce a nominal 1050 cycle, but that would not prove original parity. No balance edit was made in this audit. |
| Tiger Guard, level 14 | Melee 590; low melee 520; flip reuse 2400 | Flip has jump speed 5 and horizontal speed 2.6. Flips, target position and state changes make mixed event intervals unsuitable as a single sword cooldown. |
| Omar, level 14 | Initial attack timer 1700; shot starts reset to 2100 in phase one / 1200 in phase two; recovery 650 | Recovery and defense-opening gates can postpone a shot. Timer continues decreasing during those gates, so 650 must not simply be added to each period. Projectiles are emitted by Shoot at attack start, not by the sword ANI damage-frame listener. |
| Omar contact/projectile hits | Shared player-hit cooldown 900 | This limits accepted damage, not attack-animation frequency. Boss-hit cooldown and opening timers are separate. |

## Additional environmental threats

The inventory separately lists ten concrete spawner/environment prototypes. They are not counted as ordinary enemies. Lava Hand has a 1060 ms fire ANI and 1500 ms pre-fire delay, giving a nominal 2560 ms continuous loop; projectile emission targets frame 11. Its first shot also depends on the initial delay and frame offset. Lava Mouth and geyser apply a 1000 ms damage pulse while active, and add 1000 ms rest at animation wrap. Their full animation/map cycle is distinct from the contact-damage pulse.

Puff darts, fireball launchers, tower cannons and skull cannons use ProjectileSpawnerComponent. MinSpawnDelay/MaxSpawnDelay are added before the fire animation; map conversion may override them. Camera visibility suppresses offscreen projectile creation. A per-prototype delay alone cannot certify all placed objects.

The level-11 Laser prototype exists, but the map converter explicitly skips `logic == "Laser"` as missing logic. It is **not a functioning enemy certified by this audit**. Treat this as an existing coverage gap, not a zero attack rate matching the original.

## Source trail

Generic attacks, dive and roll: OpenClaw `Engine/Actor/Components/EnemyAI/EnemyAIStateComponent.cpp`; animation timing: `Animation.cpp` and `AnimationComponent.cpp`. Special inherited handlers: `EnemyAI/PunkRatAIStateComponent.cpp`, `EnemyAI/Gabriel/GabrielEncounter.cpp`, `EnemyAI/Marrow/MarrowEncounter.cpp`. These refer to the local patched OpenClaw tree reconstructed from the pinned source and repository patches, not recovered Monolith source.

Port-specific mechanisms: [Aquatis](../../native/AquatisArena.cpp), [Omar](../../native/OmarEncounterComponent.cpp), [lava hazards](../../native/LavaGeyserComponent.cpp), [difficulty](../../native/GameplayBalance.h). Difficulty changes damage/healing only. Assets remain supplied by the player and are not redistributed.

No APK, enemy balance or player saves were changed by this source audit. Exact original timers for these custom mechanisms remain a separate reconstruction task.
