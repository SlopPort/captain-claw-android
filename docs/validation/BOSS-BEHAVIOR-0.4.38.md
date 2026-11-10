# Boss behavior follow-up for 0.4.38

OpenAI Codex (LLM) adapted the existing GPL OpenClaw implementation using retained [REA](https://github.com/morluto/rea) observations and bounded instruction inspection. The supplied x86 executable has SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`, rechecked during this pass. It comes from the CrazyHook distribution and is not certified pristine. Decompiler output is not original source code. Original program bytes, assets and raw pseudocode remain private.

## Gabriel

The port now completes its command animation before making another decision. Returning to idle starts a 1000 ms decision gate, and the idle animation must also complete. These conditions run concurrently: idle1 itself lasts 2420 ms, so it normally supplies the longer boundary. Previously a separate 2000-3500 ms timer could select actions regardless of animation state. The legacy ActionMinInterval/ActionMaxInterval XML fields remain parseable for prototype compatibility; the reconstructed idle rule supersedes them.

Bomb and cannon commands wait 500 ms before animation progression, matching their original entry handlers. A further original animation mismatch was found: both commands select the same constructor field, bound to **strike7**, and their updates trigger on image **401**, index **1** at 130 ms. The port previously threw bombs at index 2 and commanded the cannon from strike3 at index 0. Both now use strike7/index 1, with an explicit current-action discriminator so the same image cannot trigger both effects. The nominal command-to-effect offset is 630 ms, excluding update quantization.

The summon command creates its pirate when the animation completes, rather than at entry. Another summon is refused while two summoned pirates remain active. The port tracks weak actor references and removes dead or expired actors from its count. The two-pirate limit is observed in the original; the precise original counter-decrement lifecycle has not been recovered, so health-based slot release is an explicit adaptation. It does not claim an exact original lifecycle reconstruction.

Uniform selection among three commands is preserved. The old unused 40/30/30 probability and reuse metadata remain unused: activating them would contradict the recovered original uniform selector.

| Original observation | Evidence / inspection boundary |
|---|---|
| Idle entry `0x445600` writes 1000 ms; update `0x4456d0` also requires animation completion | Retained bounded entry instructions; update `ev_a23aa5ccec8754ad308a1c1444ea51a3d5ef64a6da1d3b5ac79d414e3ab5d9ad` |
| Uniform command selector `0x445740` | `ev_9ce2ebd9d8dbeae1675a2283d4c1d5ae53c7ea37efacf794c6d21c1ff6d0a5a5` |
| Constructor `0x444f40` binds +0x4b8 to strike7 | `ev_309848868c93d24affb7fa3d532c8d743b51c883819d98c3bad9940bcdef69ba` |
| Bomb entry `0x4458e0`, cannon entry `0x445c50`: strike7 and 500 ms | `ev_2ae2e9e6f73564e3a99183a7ff193ba3c2decefcefd3f9a3357fa84ee1928bde`, `ev_3c6427dd2e0bdd054de8cb03f696a84ecf278fdb2f3a25a5011eca498cbc01e5` |
| Bomb/cannon updates trigger image 401 | Retained bounded instructions for `0x4459e0` and `0x445d60` |
| Summon entry refuses an active count greater than one | `ev_226282c4741559e4a5396679358859c689078f81115321f13cbf68380aa555bb` |
| Summon creates its pirate only on animation completion | Retained bounded update instructions for `0x445b60` |

Remaining Gabriel differences include randomized bomb trajectories, the original choice among idle animations, exact cannon-signal consumption, interruption paths and the original pirate-counter lifecycle. Fixed bomb spread, existing cannon damage and health values were preserved. The new behavior is a supported reconstruction of the listed conditions, not a complete encounter remake.

## Red Tail

Original kick and gun entries start the same next-action timer, selected uniformly from **1000-1500 ms**. That timer runs during the current action. It is not a pause added before the next animation. The port now shares this gate between its melee and ranged components, rather than independently delaying melee by 750 ms and ranged by 250 ms.

The gate is opt-in, configured by the Red Tail boss component. Other enemies retain their animation delays. An active attack completes before the gate prevents re-entry. Expiry reconsiders an ordinary patrol, while parry, hurt and active attacks finish through their existing callbacks. Fight start/end reset the timer. Existing damage frames remain kick index 1/image 402 and gun index 3/image 209. Their nominal effect offsets are 50 and 210 ms, respectively.

Evidence: kick entry `0x4836b0`, `ev_b9b37a49c704f7b9a7028ab3abd0b17449261717c483f8ccb9a8b5b6d53c3127`; gun entry `0x483ae0`, `ev_de4ccfade85e86df0df27251c9d30ff7370df84563eec1f1efd308d35dc7ae79`; retained custom updates described in [the 0.4.37 report](ORIGINAL-CUSTOM-EVENTS-0.4.37.md).

This recovers the shared timing rule within the port's existing sensors and patrol states. Original Home decisions, complete movement and sustained kick-rectangle geometry are not certified equivalent.

## Le Rauxe: original melee block predicate

A further REA pass resolved the field used by the incoming-melee handler. It is a **random integer**, not distance: shared update `0x44e880` stores the result of helper `0x451060(1000)`, and that helper returns `rand() % 1001`. Le Rauxe's incoming handler `0x481810` blocks when that field lies in `[0,100)`, outside its already-hurt branch. This is **100/1001**, approximately 9.99%, rather than the port's configured 50% melee resistance.

The boss component now caches one roll in `[0,1000]` per update, so hits checked during the same update share it. Its melee resistance path uses the exact integer predicate in `OriginalBossPolicies.h`. The XML displays 10 as a rounded fallback and explains that the engine applies the exact denominator. Other enemies and Le Rauxe's configured projectile resistance paths are unchanged. The original vtable's three projectile-related slots all point to `0x456290`, a bounded handler which marks the incoming object for removal and enters the low-block routine without subtracting health; exact mapping of every port damage category remains unverified.

The existing port protection while already in a parry state is preserved. Original block callbacks set a collision flag and clear it on animation completion, but a complete comparison of overlapping hit acceptance, collision dispatch and repeated hits has not been established. The original already-hurt paths and a 350 ms field also require tracing through the collision pipeline. Consequently this correction establishes the ordinary incoming-melee random predicate, not full boss vulnerability equivalence. Health, sword damage, knockback, hurt-immunity duration and the existing 300-600 ms attack-pause approximation were not retuned.

| Original observation | Evidence |
|---|---|
| Shared update stores helper result in the block-decision field | `ev_fc54c2cb1e20de09f00a9de27e1848d2ce71fec6fdc243b8439e52931c20d51c` |
| Helper `0x451060` uses modulo `maximum + 1` | `ev_6578944177ee437633ba6f0558efec96246b7defca84fac3493ba970ef066c81` |
| Incoming handler `0x481810` compares field against 0 and 100 | `ev_b48084fc784601d638cbbe99bf126af286fd456e64ebb896cfa53628d0ab9b04` |
| Low block entry sets its collision flag; completion clears it | Entry `ev_d4ba9c7b6be1a3acdd52826d4087b22d6e403256a64021c1ef5c4480f6d7f24f`; completion checked through bounded instructions |

The supplied executable was not executed. REA refused pseudocode for some labels; these are explicitly checked through bounded Capstone disassembly rather than presented as provider pseudocode. The new private session and instruction files remain excluded from publication.

## Validation boundary

Final Android ARM64 syntax checks passed against the existing native compile configuration for Gabriel, Red Tail, EnemyAIComponent and the shared attack source. They are compile checks, not physical gameplay evidence. The initial integrated shared-source check exposed an unrelated new ranged-state `max` macro conflict; it was reported and corrected before the next check.

`tools/redtail_cadence_smoke.py` now checks both attack types in the real level-13 arena. It checks the selected decision range, zero animation prelude, minimum start-to-start spacing, exact damage/projectile frames and duplicate emission prevention. `tools/gabriel_timing_smoke.py` checks all three commands in the real level-8 arena, their effect offsets, completed idle boundaries and the observed pirate count. Both use protected positional fixtures and restore user files. Their assertions do not establish a natural campaign clear, original Windows runtime parity or boss fairness.

The standalone host test `tools/original_boss_policy_test.cpp` includes the actual production policy header. It passed boundaries 0 and 99 (block), 100 and 1000 (do not block), invalid outside-domain inputs, and the full integer-domain count of exactly 100 blocked values out of 1001. This is a predicate test, not a statistical measurement of physical gameplay.

Cannon event diagnostics record a call to the cannon controller; a busy cannon may consume that command without firing. The original selector always enters the cannon-command state, so the previous readiness rejection was removed instead of rerolling another action every frame. Exact original pending-signal retention is still unknown. Callback identity and once-per-command guards prevent stale animation events from dispatching another command.

Final APK/device results belong to the enclosing 0.4.38 validation report; source preparation alone must not be described as a passing phone test.

The first integrated Gabriel device attempt observed no commands after the introduction. Best-state selection retained the already-active brain and its dialogue animation, so the new idle-completion condition could never become true. Fight start now explicitly re-enters that brain, resetting the idle animation and its gate. The failed test restored user files; final results are recorded separately in the update report.

The final arena-local fixture passed all three command types and observed two active pirates, with recorded counts never above two. This validates the supported count boundary within the port; it does not certify the unrecovered original decrement lifecycle or every cannon queue state. Exact artifact and metrics are in [the update report](UPDATE-0.4.38.md).
