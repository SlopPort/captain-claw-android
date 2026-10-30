# Original attack-handler verification for 0.4.37

OpenAI Codex (LLM) used [REA](https://github.com/morluto/rea) and Ghidra 12.1.4 to check whether the attack-frame differences in the [0.4.36 audit](ENEMY-ATTACK-AUDIT-2026-10-30.md) were actually consumed by original enemy handlers. This closes the handler gap for the 26 mismatching configured actions; it does **not** establish complete original AI or elapsed-time parity.

The supplied CrazyHook-distributed x86 `CLAW.EXE` has SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. It is not certified as an untouched 1997 release. The evidence is static executable analysis, not original source code or an original-Windows gameplay measurement. Proprietary pseudocode, assets and raw evidence are not redistributed.

## Why the frame corrections are supported

The [previous comparison](ORIGINAL-ENEMY-CADENCE-2026-10-30.md) traced ANI word 6 through the original decoder and animation interpreter into result code 1. Shared STRIKE consumes that result to expose its damage rectangle. Soldier's firing update consumes it to emit its projectile. Le Rauxe retains shared STRIKE. This pass checks the remaining families rather than assuming every ANI marker means the same action.

| Family | Additional original evidence | Supported correction |
|---|---|---|
| Crazy Hook | Class registration `0x436490` calls HumanEnemy registration and overrides Idle, Home, Block and HoldHook, but not STRIKE. Constructor vtable `0x50e180` binds strike entry to `0x43ffd0`. | Standing strike1 frame 3 to 2; crouched strike2 frame 2 to 1, in levels 9 and 10. |
| Bear Sailor | Registration `0x40a8b0` inherits HumanEnemy and adds its hug states; it does not replace STRIKE. Constructor vtable `0x50cae8` binds shared strike. | Standing strike1 frame 3 to 2 in levels 7, 8 and 13. Low strike4 frame 0 already matches its marker; initial frame dispatch is a separate port issue. |
| Chameleon | Registration `0x4225a0` inherits HumanEnemy and overrides Home/phase states, but not STRIKE. Constructor vtable `0x50d410` binds shared strike. | strike1 frame 2 to 1 in levels 13 and 14. |
| Town Guard 1 | Constructor `0x499b80` assigns vtable `0x511660`, whose strike slot is `0x43ffd0`. Town Guard registration `0x49ab70` inherits HumanEnemy and overrides Home/Idle/Block, but not STRIKE. | Standing strike2 frame 5 to 4 in levels 5 and 6. Crouched strike1 already matches. |
| Cut Throat | Registration `0x4399d0` binds FIRING to `0x43a220`. Setup `0x43a080` selects strike2 or crouched strike3. Update consumes animation result 1 and emits one knife, guarded by a once-per-state flag. | Standing and crouched ranged frame 0 to 6 in levels 3 and 4. The former frame-zero callback waited for wrap; it was not an immediate first shot. |
| Robber Thief | Registration `0x488bf0` binds FIRING to `0x4891f0`. Setup `0x489050` selects strike1 or crouched strike2. Update consumes result 1 and emits one arrow, guarded by a once-per-state flag. | Standing and crouched ranged frame 6 to 5 in levels 3 and 4. |

Together with previously traced Soldier and Le Rauxe handlers, these cover all 26 mismatching per-level action entries. An attack-frame correction changes the point inside an animation at which damage or a projectile is emitted; it does not independently correct the actor's complete decision cadence, hit acceptance or recovery.

## Evidence ledger

| Procedure | REA evidence ID |
|---|---|
| Crazy Hook registration `0x436490` | `ev_1a73dd4419c1f7560b65c4b75e0dd2d8102a6f06560d65b5b9221b6af5b0c88f` |
| Bear Sailor registration `0x40a8b0` | `ev_575faef71c8f3544cbe3f69a6713f0b7fdbbd5524f01273852caa85bd2acfe23` |
| Chameleon registration `0x4225a0` | `ev_69a06dbe38f5540f3570f772cb9ad06b42799ae51d003dd1c12c40b6dc6bb00a` |
| Town Guard constructor `0x499b80` | `ev_47bd02a3d84c2883791aea4ca12ec4bbc9185c55b9ad7626cf0065e80a53331f` |
| Town Guard registration `0x49ab70` | `ev_fdea12e3d94333f5a5aee09ca929d6404821a1e58a7744f757d1159d9d58c1d8` |
| HumanEnemy registration `0x44e1f0` | `ev_ebed0fa3a95da30142038158a3b1d130c4b6fc3b665dc57ee0cc1836837416f4` |
| Cut Throat firing update `0x43a220` | `ev_773f9e532306a9491400536d5104ac233d7e04f5b31da40d6f1c3325effdc7f0` |
| Robber Thief firing update `0x4891f0` | `ev_c7a279606c5ee7716d984c58d2ce2e8da6c80ef9624ce37612e5571e5ca61a10` |

Constructor evidence for the other families, ANI decoding and shared STRIKE are indexed in the previous comparison. Virtual-table bindings were also checked directly against mapped original PE bytes. Several exploratory addresses were rejected as functions or resolved to containing procedures; those are not counted as additional timing proofs.

## Gabriel: unused port weights are not original balance evidence

The original Gabriel action selector `0x445740` uses `rand() % 3` to choose the multi-bomb, thug or cannon entry. This is a uniform initial choice, not a 40/30/30 weighted selection. Implementing the port's unused 40/30/30 fields would therefore introduce a policy unsupported by this recovered original path. Successful action frequencies can still differ because action eligibility and encounter state intervene.

The original Idle update `0x4456d0` requires an idle animation termination condition, an elapsed timer, and encounter flags before calling that selector. Its idle-entry vtable target is `0x445600`. Ghidra rejected this label as a procedure; bounded instruction inspection of mapped PE bytes shows it sets duration at actor +0x508 to **1000 ms** and start time at +0x504 to the current game clock. This is a minimum idle timer combined with an animation-completion gate, **not a complete 1000 ms attack interval**.

Multi-bomb entry `0x4458e0` and cannon entry `0x445c50` set a **500 ms prelude** timer. Their bounded update instructions at `0x4459e0` and `0x445d60` gate animation advancement until that timer expires, then eventually return through idle-entry slot +0x64. Thug entry `0x445af0` refuses another summon when its active-thug counter is greater than one; bounded update `0x445b60` increments that counter when creating a thug. Counter decrements and all interruption paths have not been fully traced.

These paths do not establish the port's unused 2500/4000/3000 ms per-action reuse fields. The current port also differs by using a 2000-3500 ms timer without the same complete original idle/prelude/counter machinery. Reconstruct that state machine as a separate change with encounter tests; do not call either the existing port cadence or a quick timer substitution original parity.

| Gabriel procedure | REA evidence ID / method |
|---|---|
| Constructor `0x444f40` | `ev_309848868c93d24affb7fa3d532c8d743b51c883819d98c3bad9940bcdef69ba` |
| Registration `0x444960` | `ev_275929a80822fb56cc42d54986b6481329f519c236cd4c0f9c4b70e228e95436` |
| Idle update `0x4456d0` | `ev_a23aa5ccec8754ad308a1c1444ea51a3d5ef64a6da1d3b5ac79d414e3ab5d9ad` |
| Selector `0x445740` | `ev_9ce2ebd9d8dbeae1675a2283d4c1d5ae53c7ea37efacf794c6d21c1ff6d0a5a5` |
| Multi-bomb entry `0x4458e0` | `ev_2ae2e9e6f73564e3a99183a7ff193ba3c2decefcefd3f9a3357fa84ee1928bde` |
| Thug entry `0x445af0` | `ev_226282c4741559e4a5396679358859c689078f81115321f13cbf68380aa555bb` |
| Cannon entry `0x445c50` | `ev_3c6427dd2e0bdd054de8cb03f696a84ecf278fdb2f3a25a5011eca498cbc01e5` |
| Idle entry `0x445600`, special updates | Bounded Capstone disassembly of original mapped PE bytes; provider rejected these procedure labels. No invented pseudocode or complete-function claim. |

## Remaining boundaries

- Exact repeat rates still require full Home/attack/hurt/parry transitions and original-Windows measurements with matched distance, stance and terrain.
- The ten actions without an event-1 marker require their own custom logic. They are not candidates for a blanket event-marker rewrite.
- The port's Le Rauxe pause before every attack remains an approximation of the original conditional Home pause.
- Red Tail's misplaced XML delay is a confirmed port parser mismatch; fixing it is not proof that its resulting rate equals the original.
