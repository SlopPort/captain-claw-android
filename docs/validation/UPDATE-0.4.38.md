# Enemy behavior update: debug 0.4.38

Date: 2026-11-07. Implementation, reverse engineering, review, documentation and automated testing by OpenAI Codex (LLM), guided by anonymous human feedback. OpenClaw and dependency authorship remain separate.

## Scope

This batch addresses the requested enemy-behavior follow-up only. It does not claim a natural campaign clear, release 1.0, universal Android runtime support or a new minimum FPS.

- [Siren](SIREN-BEHAVIOR-0.4.38.md): original four-note pattern, singing duration, entry recovery and projectile origin/speed, inherited by both level variants.
- [Custom melee](CUSTOM-MELEE-0.4.38.md): moving Crab damage window, Fish captured-target lunge and Tiger Guard three-move policy/entry timing.
- [Bosses](BOSS-BEHAVIOR-0.4.38.md): Gabriel command phases and summon limit, shared Red Tail decision timing and the separately documented Le Rauxe findings.

Original behavior is inferred from the supplied CrazyHook-distributed executable, not recovered original source. Raw proprietary evidence and game resources remain private. Each detailed report distinguishes implemented rules from unresolved original state-machine and collision differences.

## Review and caught failures

The independent review caught a missing Siren cooldown wakeup and a Fish/Tiger completion guard which would have blocked subsequent entries. Both were corrected; the physical fixture requires repeated entries. Active damage resolves live actors by committed identifiers and checks body/health availability, rather than retaining raw pointers across synchronous health callbacks.

An initial compile check caught a legacy `max` macro conflict in new code. The first Siren device attempt exposed a fixture assertion: zero patrol speed requires the idle-only flag. Its files were restored after the failed attempt. A later preliminary Siren run passed three cases but rejected a 279 ms first spacing in the fourth case; the new timer had charged the animation callback's already-elapsed frame a second time. This was corrected in code, rather than widening the accepted range. Private failed-run evidence is retained.

The first integrated custom-melee run passed both Crab directions but failed before the Fish moved: the fixture's 65-pixel separation lay outside its sensor. Re-entering at the stationary Fish's exact X then exposed a real zero-length line-of-sight ray assertion in Box2D. The production raycast now handles exact and float-collapsed zero-length segments without calling Box2D; a device command exercises both cases. Fish fixtures use a 50-pixel initial separation inside the actual sensor. Both the failed run and the restored user files are retained privately.

A safety check initially called a private physics-body lookup and failed compilation. A narrow read-only public existence check was added; gameplay does not receive a raw body pointer.

The expanded Tiger inspection observed all three moves but only knife contacts. Its lunge was incorrectly moving during image 800, the original 500 ms wind-up; it could cross the target before activating its damage window. This was corrected and the physical test now requires actual contacts from both knife and lunge.

## Verified artifact and results

Final candidate: **0.4.38-dev / versionCode 50**, build r9, installed on the allocated Huawei P9 Lite (VNS-L21), ARM64 / Android 10. Both ARM64 and ARMv7 compiled; physical runtime evidence here is Huawei ARM64 only. Static package/ARM64 16 KB ELF checks do not certify all Android systems. Public signed distribution remains 0.4.32-test.

- APK SHA-256: `4340b88012e8c7bb76258b9aeed4ef687fc71aeee6572acbce9fff1cee668407`; 36,543,612 bytes.
- Support archive SHA-256: `853334b5119d5f199bd1f7bc88fead46068b7f6e360c4c54aa77325cb0d8bb44`.
- All six main physical result files below record this exact APK hash and `passed=true`. Reports, user backups and proprietary data remain private.

| Test | Result and boundary |
|---|---|
| Siren | Four cases (two levels, both directions), twelve complete bursts and 48 notes. Within-burst intervals 298-323 ms; first-note intervals 4190-4211 ms. Origin and velocity checked. |
| Crab | Both directions; ordered open/close windows measured 102-132 ms around nominal 120 ms; contacts restricted to images 203/204 and at most one target hit/window. |
| Fish | Both levels/directions; first captured-target crossings 281-300 ms. A real sensor exit/re-entry confirmed another attack on the same actor. |
| Tiger Guard | All three moves and 34 decisions; original 1250-2000 ms gate and 2-4 knife chains checked. 36 knife and 4 lunge contacts exercised both damage paths. |
| Red Tail | Real-arena melee/ranged phases passed: selected shared 1000-1500 ms gate, no animation prelude, exact frames and at most one emission/cycle. |
| Gabriel | All three commands, 17 observed actions; nominal 630 ms bomb/cannon effect and 590 ms summon timing passed. Main run did not saturate the two-pirate limit; an arena-local follow-up is recorded separately below. |
| Le Rauxe | Exact cached integer predicate checked on real hits; ordinary sword inputs reduced HP 100 to 55. Boss HP was never edited. Existing cadence approximation remains explicitly separate from original full AI. |
| Shared attacks | Nine ordinary cases plus three synthetic frame-zero delays (0, 150, 750 ms) passed exact-frame, delay and duplicate-emission checks. |
| Coincident visibility | Production raycast passed exact and float-collapsed zero-length queries in the device fixture. |

These are protected positional fixtures, not natural campaign completion, original-Windows runtime measurements or fairness certification. Completed test owners restored config/SAVES byte for byte and removed the command mailbox. The temporary ADB-offline interruption was resolved by the human; no phone reboot, USB/network change or shared ADB-server restart was used.

Private main evidence directories: `siren-0.4.38-r5`, `custom-melee-0.4.38-r5`, `redtail-0.4.38-r4`, `gabriel-0.4.38-r3`, `leraux-0.4.38-r3`, `enemy-timing-0.4.38-r3`.

## Host checks and source correspondence

Production-header boundary checks passed for all 101 Tiger selector inputs, Crab image boundaries, movement direction, speed conversion and exactly 100 blocked Le Rauxe integer values out of 1001. Six changed XML prototypes preserve health, physics and root attributes. The clean reconstructed patch matches 64 OpenClaw files and one SDL file. All 55 packaged concrete enemy/encounter prototypes and 75 configured actions have available ANI files and valid configured frame bounds; custom policies are distinguished from the generic cycle formula in the [metadata inventory](ENEMY-ATTACK-INVENTORY-0.4.38.md).

After compilation, two physics files had their original CRLF endings restored to avoid a whole-file patch. Normalized source bytes were asserted identical; no functional engine-source change was made after the tested build. No original executable or game assets are published.

## Remaining original fidelity boundaries

The detailed reports retain unresolved original swimming/jump-strike eligibility, complete boss Home/obstacle decisions, overlapping hurt/block collision handling, cannon signal retention, exact sprite-derived rectangles and original pirate-counter lifecycle. Preserved port accommodations and inherited rules are not presented as proven original behavior. Natural campaign testing belongs to the human.

## Additional Gabriel arena follow-up

The arena-local follow-up also passed on the same APK, with 23 observed actions and all three command types. Claw was positioned near the real cannon button after the introduction; two active pirates were observed and recorded counts did not exceed two. This exercises the limit boundary more directly than the initial remote-trigger fixture. It does not recover the original counter-decrement mechanism: the implementation still uses its documented live-actor/health adaptation. Private evidence: `gabriel-0.4.38-r4`.

Final post-test inspection verified the installed APK hash, canonical support archive, byte-identical restored config/SAVES and absence of command files. The game was reopened normally. No Redmi operations were performed.
