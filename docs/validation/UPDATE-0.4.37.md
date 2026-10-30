# Debug 0.4.37: confirmed enemy attack corrections

Date: 2026-10-30. Implementation, investigation, documentation and automated fixtures by OpenAI Codex (LLM), guided by anonymous human reports. OpenClaw and dependency authorship remain separate. This is a local tested debug build; the public signed test release remains 0.4.32-test.

## Changes

- Corrected **28 effective attack-frame configurations** across nine families: 26 shared-event differences plus Siren first-projectile phase in levels 11/12. There are 23 explicit XML frame values and five inherited per-level entries. The [updated inventory](ENEMY-ATTACK-INVENTORY-0.4.37.md) covers all 55 packaged enemy/encounter prototypes and 76 actions. All **66 actions with an original event-1 marker** now select that marker.
- Fixed Red Tail melee `AttackDelay=750` placement. It is read by the component and gives a nominal 1050 ms port sequence. This repairs an ignored setting; the original custom next-action policy still differs.
- Added deferred frame-zero emission in generic attack states. It runs once after the selected delay, outside Box2D contact-entry callbacks. Leaving the state clears pending work; later actions retain sequence-delay semantics. This addresses first attacks that formerly waited for a whole animation wrap.
- Added bounded opt-in attack-cycle/emission timing logs and a synthetic frame-zero fixture. These are active only under existing combat diagnostics. Normal actor health, configured damage, sensors, parry probabilities, player hitboxes and difficulty multipliers were preserved. A semantic XML comparison verified those fields were unchanged.
- Documented Gabriel uniform choice as deliberate: original selector uses rand()%3. Its old unused 40/30/30 metadata is not a reason to implement weighted selection. Original idle/prelude/eligibility behavior needs a separate encounter change.

The [shared-handler evidence](ORIGINAL-HANDLERS-0.4.37.md) verifies the 26 corrections against original handler dispatch, rather than only matching data. The [custom-handler evidence](ORIGINAL-CUSTOM-EVENTS-0.4.37.md) covers all ten actions without event-1 markers, including the Siren correction. Proprietary executable code and game resources are not included.

## Exact artifact

- Version: **0.4.37-dev**, versionCode **49**.
- APK SHA-256: `bf8c68ebaf6b1e39e0bb8fee26ccaeb9d620288a5aa3f23fb49eac6dd91fe7a1`.
- APK size: **36529826 bytes**.
- Packaged support SHA-256: `7a6dfe000543e2608a37b1279545de4ed0c83c50c2fd7105cb607f9155ce0f37`.
- ARM64 and ARMv7 build passed. APK checks verified both architectures and 16 KB load alignment for ARM64 native libraries. Physical runtime in this batch used **Huawei ARM64 / Android 10** only. ARMv7 and other Android releases have build/static coverage here, not new physical runtime certification.

## Final physical evidence

All following checks used the exact APK above. Arenas were temporary, the player was protected and boss HP was never edited. These are technical fixtures; campaign progression remains human-tested.

| Ordinary actor / animation | Expected emission frame | Emissions | Median repeat interval (ms) |
|---|---:|---:|---:|
| Officer / strike | 3 | 6 | 770 |
| Soldier / strike1 | 2 | 6 | 626 |
| Soldier / strike | 3 | 4 | 1248 |
| Level3_CutThroat / strike2 | 6 | 5 | 868.5 |
| Level3_RobberThief / strike1 | 5 | 4 | 1108 |
| Level10_CrazyHook / strike1 | 2 | 9 | 525.0 |
| Level7_BearSailor / strike1 | 2 | 8 | 589 |
| Level13_Chameleon / strike1 | 1 | 12 | 401 |
| Level5_TownGuard1 / strike2 | 4 | 9 | 576.5 |
| Level11_Siren / strike1 | 1 | 3 | 1779.5 |

Ten ordinary cases passed exact-frame, one-emission-per-cycle, timing and repeat checks. The Officer is an unchanged control case. Metadata references were also checked across every inherited variant; this does not claim physical execution of every stance on every level.

| Synthetic first-frame delay | Observed event latency from cycle entry (ms) | Median repeat interval (ms) |
|---|---:|---:|
| 0 | 0-2 | 589.5 |
| 150 | 149-175 | 747.5 |
| 750 | 749-765 | 1342 |

The synthetic actor modifies its emission frame in memory only. It tests the real engine delay/dispatch path and absence of duplicate emissions, rather than claiming a natural Bear Sailor low-attack encounter.

- **Le Rauxe:** 11 measured emissions used frame 4 after the selected 300-600 ms port pause. Consecutive intervals ranged from 686 to 897 ms, median 791 ms. Ten ordinary sword taps reduced boss HP from 100 to 80. The test retains player protection and does not certify natural boss fairness.
- **Red Tail:** 6 melee emissions used frame 1 after the effective 750 ms delay. Intervals ranged from 1048 to 1063 ms, median 1050 ms. Boss started with 150 HP and no attacks were made by the player.

Original configuration and saves were restored byte for byte after every fixture. Backups from all eight runs in this batch agreed, including failed harness attempts and final reruns. The normal app was reopened afterward. Its canonical `.engine-support/ASSETS.ZIP` was checked against the final APK digest; the legacy imported root ASSETS.ZIP is a separate preserved file. The diagnostic mailbox was absent, and installed version 0.4.37-dev / 49 was confirmed. Redmi, USB tethering settings and the shared ADB server were not operated.

## Reproducibility and caught test limitations

Tools: [ordinary/frame-zero regression](../../tools/enemy_timing_regression.py), [Le Rauxe](../../tools/leraux_cadence_smoke.py), [Red Tail](../../tools/redtail_cadence_smoke.py), [metadata inventory](../../tools/audit_enemy_cadence.py). Set ANDROID_SERIAL only to a newly allocated device; regenerate `reports/combat-audit` before using fixture indices. Reports, user backups and proprietary assets remain private.

Initial harness runs rejected the first cold-spawn timing sample: actor/resource creation can consume part of an already-started frame budget. The final fixture warms the actor resources before timing a fresh instance, trims the staging boundary, asserts the exact emission frame independently, and allows 85 ms around nominal in-animation latency. Repeat-period tolerance is 75 ms. This is not exact millisecond original parity; cold dynamic-spawn timing and interruption behavior remain separate boundaries. The frame-zero checks specifically require first emission after the configured delay and only once per cycle.

Both source patches applied to clean reconstructed files and matched the working tree (60 OpenClaw files and one SDL file, CRLF normalized). Semantic XML review found only intended frame and delay changes in 15 files. All animation paths, frame bounds, event-marker comparisons and the absence of ignored action-level delays passed against the final APK. Python tools compiled successfully.

## Original behavior still to reconstruct

- Siren: original up-to-four-projectile burst, 300 ms spacing, 4000 ms entry gate and singing/recovery rules. The first-projectile frame is now aligned; the port still has its existing single-shot policy.
- Gabriel: original idle animation plus 1000 ms gate, 500 ms bomb/cannon preludes and active-thug eligibility/counter lifecycle. Uniform action selection already agrees with the recovered selector.
- Tiger Guard: original timer-gated three-move set; the standing port strike2 was not established as an original selected move.
- Fish: movement/apex-driven damage; image 202 is a sound cue rather than a shared damage marker. Hermit Crab: sustained active window across images 203/204, rather than only one transient attack.
- Red Tail and Le Rauxe: complete original decision/reuse policies and defensive/hurt transitions. The repaired port delays remain documented approximations. Original custom onset frames already matching for Red Tail, Aquatis body and Tiger Guard knife were preserved.

All ten markerless actions now have a concrete handler comparison or a specified reconstruction boundary. Original-Windows runtime comparison, complete campaign validation and universal FPS/Android compatibility remain outside the evidence established by this batch.

Source-only cleanup after the final APK test removed trailing whitespace from three XML lines. Parsed XML values are unchanged; the tested APK hashes above refer to the pre-cleanup formatting.
