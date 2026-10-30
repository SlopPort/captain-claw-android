# Original enemy cadence evidence - 2026-10-30

OpenAI Codex (LLM) used [REA](https://github.com/morluto/rea), its task-local reverse-engineering skill and Ghidra 12.1.4. The supplied x86 `CLAW.EXE` has SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. It is a CrazyHook-distributed executable, not a certified untouched 1997 release. This is static machine-code interpretation, not recovered original source or a Windows gameplay measurement. Proprietary code, assets and raw evidence remain private.

## What is established

| Evidence | Supported comparison | Boundary |
|---|---|---|
| Shared strike entry `0x43ffd0` and strike update `0x440020`, registered by `0x43e660` | Original enters a named STRIKE state, selects an animation, reacts to animation result code 1 and returns through virtual slot +0x60 when animation termination conditions are met. Port uses configured frame indices and animation-loop callbacks. | This proves different event-dispatch implementation, not a numeric speed error for every actor. ANI metadata totals alone do not recover the complete original decision loop. |
| Shared Home continuation `0x44f210`, pause setter `0x440590` | A conditional branch can attack or select a randomized 300-600 ms pause. | This is not a mandatory cooldown after every original hit. Port fixed delays cannot all be certified by this one branch. |
| Officer Home `0x465510`, constructor/vtable `0x510440` | In proximity classes 0-4 it calls its strike virtual directly; that slot resolves to the shared strike entry. | A mandatory long pause on every Officer strike would contradict this path. Exact elapsed intervals depend on animation, transitions and scene. |
| Soldier Home callback `0x48e740`, registration `0x48e490`, constructor `0x48dd90` | Bounded raw instruction analysis shows direct strike choices, a firing branch and shared Home fallback. | REA did not admit the Home label as a decompilable function. Its bounded Capstone instruction inspection is retained privately; it is not invented pseudocode. |
| Soldier firing setup `0x48eae0`, firing update `0x48ec70` | Firing loads STRIKE / level-2 crouched STRIKE2; animation result code 1 creates a musket ball once per firing state. | The 500 constant in firing setup also appears as horizontal projectile speed. Do not label it a universal 500 ms firing cooldown. Idle timer code is a separate path. |
| Robber Thief Home `0x488ef0`, firing setup `0x489050` | LOS, vertical proximity and a random threshold gate firing; it is not simply a permanently running attack animation. | Full first-shot/repeat timing and all idle transitions remain unresolved. |
| Peg Leg attack entry `0x46ba90` | Checks elapsed time against a timer before firing, and another timer / level / stance before choosing and alternating attack animations. | Port always sequences its configured two actions. This is an AI policy difference; original timer initialization, reset paths and runtime intervals still need full tracing. |
| Red Tail Pirate strike wrapper `0x486a00` | Adds a randomized speech choice, then calls shared strike entry. | Speech randomization is not evidence of an extra combat cooldown. |
| Le Rauxe prior pass | Original Home decision/pause behavior differs from unconditional melee repetition; see [boss evidence](LERAUX-ORIGINAL-2026-10-30.md). | Debug36 adds 300-600 before every strike as an explicit approximation. Original per-strike parity and exact parry probabilities are unresolved. |

The original animation interpreter `0x4c8550` includes delay/event handling and a playback multiplier. The port directly consumes ANI durations but does not reconstruct every original animation command or actor decision. The ANI decoder at `0x4d99d0` was subsequently recovered: raw signed word 6 becomes decoded frame +0x1c, while word 5 becomes duration +0x18. The interpreter carries frame +0x1c into its returned event value. Shared STRIKE and Soldier firing consume result 1 for attack behavior. This establishes an actual original event-marker crosswalk, not a guess from artwork or sound markers. It still does not turn ANI duration into an exact complete Windows attack interval.

## Constructor and dispatch coverage

These constructors were recovered and checked against virtual-table bytes in the admitted executable. Strike/pause bindings describe entry points only; they do **not** certify every family update, cooldown or attack-frame choice. Raw table reads used pefile against the recorded SHA-256.

| Family | Constructor evidence ID | Strike entry | Pause entry |
|---|---|---|---|
| Officer | `ev_2b8fa81c31338d10359bad2c78082833da68cbfc757596ba5e98bc509956170e` | `0x43ffd0` | `0x440590` |
| PunkRat | `ev_06c61032ba684fc12c5ebf0c2d05844457f437510f7639a1557946acbd2370ac` | `0x43ffd0` | `0x440590` |
| CutThroat | `ev_e0f41c2de96839866be3047cdce0d04b762dd17e1dca166a183980be80534a64` | `0x43ffd0` | `0x440590` |
| RobberThief | `ev_d3d66fcc3e3e546e7b869997021cf0c79f4a0209450ddeedbfe11078b312d101` | `0x43ffd0` | `0x440590` |
| BearSailor | `ev_f6be3bd227883124089648562d45fa8835d22c1c61b97ba4807e250658c975c8` | `0x43ffd0` | `0x440590` |
| RedTailPirate | `ev_5cf090c4c7d03b278d2bd6337ea023159f64fbc139ea9c5971126de0f1376c43` | `0x486a00` | `0x440590` |
| RedTail | `ev_b491b2bd71e3203afcdd0774a09d8558f9f062a29d5b160bae1e38e7e98b710f` | `0x43ffd0` | `0x440590` |
| CrazyHook | `ev_f3ad926a5af3ebb37a5d91e4b2cd7582d57238b626ef1b6006665cc1831d2f04` | `0x43ffd0` | `0x440590` |
| PegLeg | `ev_54b0764a32d177d1ba0542c53a6a867ca1ce67966eadcf7a853046481d3a320b` | `0x46ba90` | `0x440590` |
| Siren | `ev_3305ca0111110c7171a6cfe142c4ec3e61a4f65981aa59c68cbe61926c28bd53` | `0x48d640` | `0x440590` |
| Chameleon | `ev_49c66e606077ddaf1973b2e277a51274c43d417bb9870d70e0e770604c78e55b` | `0x43ffd0` | `0x440590` |
| TigerGuard | `ev_21e57ef4b770d4ccf98c4718925a20c3cf669d9ea05ff610fced3bf18eb891c5` | `0x4988e0` | `0x440590` |
| Mercat | `ev_2ee0b080482a43807aece64d7260a1cc887f1277212f7a93cc008a5e3a48a070` | `0x43ffd0` | `0x440590` |

Soldier and Le Rauxe are covered by additional evidence above and the linked prior report. Rat, fish, seagull, town guards, Hermit Crab, Gabriel Pirate, the other bosses and spawned encounter actors have complete port inventory entries, but this pass has **not** recovered all of their original timing policies. An inherited shared slot is not a substitute for that work.

## Evidence index

| Procedure / purpose | REA evidence ID |
|---|---|
| Shared strike entry | `ev_869a80a377039e3ea37833098e8a6deac96dc7bbff9e67af6b2b81e5fe2ff88b` |
| Shared Home | `ev_2696cc29a7e5431f28fd413f49a6f8458ed0bc3c5219f15bd0fd44e5b08f1a73` |
| Pause setter | `ev_69a5c8f8e4a7fc6fd654570b7683477ac2b0134498501821831afb48b5786986` |
| Officer Home | `ev_80074a1b748342fe7cbf5e7058c43d449923568cf3c365373f4de988d1f9676f` |
| Robber Home (provider resolved containing procedure 0x488ef0) | `ev_e60914e90a68932229b10c637e2858b3e35d80de50c6b6b50b52a58553f6b013` |
| Soldier firing setup | `ev_679e2e7d09123cc43a0a7e379cc758fc3c9d98176e8a121cda561b596088fde5` |
| Soldier firing update | `ev_7d70cd24c31381582c25deeada1520e74df626c62e1a97df898bfabf94e033c3` |
| Robber firing setup | `ev_f340260f09f20e1fff44126c0e9253417127cd34b03795b4ee3421eaa4b539db` |
| Pirate strike wrapper | `ev_9ec2feb63eafc76dd3d2ab5c262dacef16172bb435d26d6fc28b8f5c0e3b070f` |
| Peg Leg attack entry | `ev_f90a4cc01e08ebc529cb5063d2cbae90afc119eaf56c0656ede206604d17431f` |
| Human state registration | `ev_ebed0fa3a95da30142038158a3b1d130c4b6fc3b665dc57ee0cc1836837416f4` |
| Base state registration | `ev_18f5750e8d8398bd228658a1d1e81465f5e0bb739a36584b75755a3c43ab16c0` |
| Shared strike update | `ev_02813fb5bccc969aca427667f1ec87e77f323a474ef7b0096b3cbdcbd762e867` |
| Original animation update | `ev_a6424d71c15507f82fcc2b0e54bd731f04eb55906eb1e6afbaa7beb9f92b4ff2` |

## Attack-event comparison

The full generated table lists original event-1 indices beside each port index. For Soldier melee the marker is frame 2 (nominal ANI offset 60 ms), whereas the port selects frame 4 (160 ms). Soldier standing firing selects frame 2 (700 ms) versus original event marker 3 (750 ms); level-2 crouched firing selects frame 3 (275 ms) versus marker 4 (350 ms). These are supported marker/emission differences, not invented cooldowns.

Le Rauxe selects frame 3 (150 ms) versus marker 4 (250 ms). Its registration at `0x481320` overrides Home, Idle, hurt and JumpOver, but not STRIKE; it retains the shared strike update. Registration evidence: `ev_7bd1c6741e4beb73e08324609b5de3d76aad8ec10155bb22286db582b48ced18`. For Cut Throat, port frame zero waits for wrap: its effective animation-relative first event is about 620/640 ms, versus original markers at 520/540 ms. Do not call that an immediate 0 ms attack or subtract the nominal zero offset to claim it fires 520 ms early. Original per-family state handling still matters.

Decoder evidence: `ev_9f1442665fab594fc0f0b3dfd925a0348292551f4246f834a95888b4bdffcee8`; interpreter and shared strike/firing evidence are indexed above. The word-0 sound-event field is separate. The 26 mismatches include repeated per-level variants, not 26 distinct enemy species.

## Outstanding comparison work

- Recover full family-specific Home/strike/firing transitions, including pause probabilities and timer reset sites, before assigning exact original rates.
- ANI word-6 / interpreter result-1 mapping is now traced and all 76 port actions compared: 40 select an event-1 marker, 26 select a different frame, and 10 have no event-1 marker. Trace the per-family custom handlers for the latter and verify which non-shared firing states consume event 1. Matching markers do not certify full timing policy.
- Capture original-Windows first-hit and repeated-hit intervals at the same distances, stance and height. No such capture was performed in this batch.
- Verify damage acceptance / hurt recovery separately from attack frequency; one attack log does not equal one accepted hit on Claw.

Several callback labels were rejected for pseudocode; those rejections are retained and not counted as successful reconstruction. An interrupted earlier worker had no surviving process; the owned task-local session was resumed with existing results preserved, then closed after this pass. Original executable bytes were not edited.

See [the audit summary and per-family coverage](ENEMY-ATTACK-AUDIT-2026-10-30.md), [packaged timing](ENEMY-ATTACK-INVENTORY-2026-10-30.md) and [special mechanisms](SPECIAL-ENEMY-CADENCE-2026-10-30.md).
