# Project TODO and release backlog

Updated **2026-11-12** by OpenAI Codex (LLM), guided by anonymous human requirements and feedback. Adaptation authorship is separate from OpenClaw and dependency authorship.

This is the detailed, actionable backlog. The [roadmap](docs/ROADMAP-1.0.md) summarizes release gates; the [handoff](docs/HANDOFF.md) records current state and operating constraints. An unchecked item means work or evidence is still required, not necessarily that a defect has been proved.

## Current execution plan for 1.0

**Start with the [completed-work reconciliation](docs/validation/BACKLOG-RECONCILIATION-2026-11-10.md).** This is the shared backlog, not a fresh implementation list for each assistant. Completed fixes stay completed after unrelated version/documentation/diagnostic changes. An unchecked `VERIFY` item below names remaining coverage or a final release gate; it must not be read as proof that the underlying feature is missing.

Follow the [remaining-work checklist](docs/RELEASE-1.0-CHECKLIST.md), reviewed against commits, local changes and saved reports on November 10. It groups this backlog into eight ordered gates: pending audio; reported movement/combat blockers; encounters/original-policy decisions; touch/menus/language; installation/save safety; declared Android coverage/stability; human campaign acceptance; and the exact signed release. Stable task IDs below remain authoritative. Do not restart completed fixtures without a relevant change or missing acceptance condition.

The [debug43 audio correction](docs/validation/UPDATE-0.4.43.md) now has baseline/fixed ARM64 evidence for Soldier hurt/death, Officer impact and hero hurt; wider listening and boss coverage remain open. The saved debug42 20-minute heavy-scene run **has completed successfully**, including runner checks of restored user configuration/progress and unchanged APK; its scope is protected stationary observation, not debug43 or full-campaign acceptance. See the checklist for exact versions, evidence and remaining limits.

## Historical follow-up records

[0.4.40 evidence](docs/validation/UPDATE-0.4.40.md) adds verified Tiger continuation, Siren interruption/death, localized save-error and gameplay-options checks. The old sustained FPS pass was invalidated; performance remains open. The full custom-AI research tasks are not closed by a narrow fix.


[0.4.39 evidence](docs/validation/UPDATE-0.4.39.md) records actual results, including failed fixture attempts. Original comparison ledger, explicit known limitations, targeted source-comment review and a sequential restoration-verifying test runner are now present. Other items retain their individual open conditions.

## Baseline: do not repeat completed work without a reason

- Latest verified Huawei runtime: **0.4.43-dev, ARM64** ([exact evidence](docs/validation/UPDATE-0.4.43.md)), upgraded in place and fixture-tested on November 10. Earlier debug42 movement/stability and debug41 emulator results remain version-specific. [Signed41 test download](https://github.com/SlopPort/captain-claw-android/releases/tag/v0.4.41-test) and its [production identity/runtime limits](docs/validation/RELEASE-0.4.41.md) remain unchanged. This is not a finished 1.0 release.
- [0.4.38 results](docs/validation/UPDATE-0.4.38.md) cover reconstructed Siren, Crab, Fish, Tiger Guard, Gabriel and Red Tail behavior, the Le Rauxe ordinary melee block predicate, and the zero-length line-of-sight guard. These are bounded technical results, not complete original-game parity.
- [0.4.37](docs/validation/UPDATE-0.4.37.md) corrected effective attack emission frames and deferred frame-zero handling. Do not replace these with arbitrary global attack-speed changes.
- Prior builds addressed double audio attenuation, Game Over instructions, floor joins, wall-only grounding, leafy-ladder caps, rope interpolation and unsupported menu entries. Their exact-build reports remain evidence; final-build regression checks below remain necessary.
- Technical transitions through all 14 maps and controlled boss encounters do not establish natural campaign completion. The human owns natural campaign testing.
- Only Huawei is allocated now. Ask for a new allocation before using Redmi. Preserve Huawei USB tethering; do not restart shared ADB, reboot the phone or change its network/USB settings to repair a test.
- Broad physical controller testing remains deferred. Specific reported pause/input regressions can be investigated within the allocated-device scope.

## How to maintain this list

Priorities: **P0** blocks a credible 1.0 release; **P1** requires investigation, verification or an explicit documented scope decision; **P2** is optional follow-up. Statuses: **DONE** means the documented completion scope has dated evidence; **OPEN** means a reported unresolved issue; **VERIFY** means evidence is incomplete or historical; **RESEARCH** means original behavior is not established; **DEFERRED** means do not start without scope reactivation.

Keep the stable IDs in reports and commits. When closing an item, add a dated evidence link, exact APK/version/hash, device/ABI/data edition, steps and result. Record failed trials and fixture limitations. A successful compilation, absent log message or unreproduced report does not close a runtime bug. If a research item is accepted as an intentional difference, record the decision and player impact instead of claiming original parity.

Before repeating a test, record one concrete trigger: a relevant changed production path, a new reproduction, a previously uncovered scenario, or the single frozen-candidate acceptance run. A newer version number or an unrelated edit is not enough. Historical results keep their exact APK identity, but remain useful for deciding what **not** to implement/test again. Do not expand a task's completion conditions after its stated scope has passed; put genuinely separate coverage under its existing owning task. Final import/menu/audio/compatibility checks are one coordinated RELEASE-02 gate, not separate full reruns after every development step.

## Recommended next engineering work

Debug42 adds [input triggered after actual enemy damage](docs/validation/UPDATE-0.4.42.md). Four synchronized active-Soldier observations distinguish short input ending during hurt from held input surviving recovery; both sword trials defeated the target. This narrows COMBAT-01/02 without closing natural stairs, original policy or broader geometry. No gameplay priority or balance was changed.

1. Capture the next live level 2 blockage before jumping, restarting or moving away (MOVE-01).
2. Reproduce lower-hero diagonal combat with active enemy AI and trace damage/recovery windows (COMBAT-01).
3. Select only uncovered INPUT/UI/AUDIO scenarios from the reconciliation; completed checks wait for a relevant production change or the frozen release candidate.
4. Resolve or explicitly scope the remaining original-behavior questions (ORIGINAL and BOSS).
5. Measure the final candidate on Huawei, then obtain device allocation for missing compatibility checks (PERF and ANDROID).
6. Close installation/documentation/release gates while the human independently reports campaign results. Do not autonomously take over that playthrough.

## Movement, contacts and platforms

- [ ] **MOVE-01 / P0 / OPEN:** Diagnose level 2 leftward small-platform blockage near the crate at approximately (2460, 4956). Seventeen earlier attempts did not reproduce it. Use the [existing capture instructions](docs/validation/LEVEL2-PLATFORM-0.4.34.md) and [background recorder](docs/BACKGROUND-DEBUGGING.md). Capture requested input, velocity, foot/support state, contact normals and nearby geometry before escape. Done: reproducible cause, bounded fix, regression at that geometry and human recheck; otherwise retain OPEN.
- [ ] **MOVE-02 / P0 / VERIFY:** Remaining: the two exact recorded natural level-1 snag locations, including traversal/reversal, crouched traversal and return after jumping. The synthetic 1/2 px join, partial-edge crouch and tall-wall anti-boost checks already passed in debug32/40. Do not repeat those as a new fix; their success does not identify both natural recording locations.
- [ ] **MOVE-03 / P0 / VERIFY:** Remaining: unverified crouched traversal/reversal across raised joins and exact natural support-boundary combinations. Flat-foot bearing, both-sided 1/2 px joins, partial-edge standing/crouching, fully-outside falling, walk-off and air-jump rejection already passed. Do not reimplement or routinely repeat them. See the completed-work audit.
- [ ] **MOVE-04 / P0 / VERIFY:** Remaining: unverified lateral-transfer/early-release combinations on natural ladder geometry and the recorded natural top/jump location. First level-1 and both leafy level-3 caps already passed held Up, release, down re-entry and stated jump checks. Keep those fixes; distinguish an original-policy question from a new fall-through.
- [x] **MOVE-05 / P1 / DONE:** The named bounded technical cases are covered: bottoms/cap jumps (debug41), neutral and held-release pause (debug41/42), actual mid-ladder hurt recovery/jump-away and death/respawn without stale attachment (debug43). [Combined scope and retained failed setup](docs/validation/LADDER-DAMAGE-0.4.43.md). Natural cap/transfer work remains MOVE-04; original policy, physical input and wider lifecycle remain separate tasks.
- [ ] **MOVE-06 / P1 / VERIFY:** Remaining: human visual/low-FPS review at swing reversal and any unverified natural attachment geometry. Attached handle alignment, ordinary release/jump and regrab already passed. Do not change swing reach or repeat those same fixtures solely for a version-number change.
- [ ] **MOVE-07 / P0 / VERIFY:** Remaining: disappearance underfoot, return/reboarding and unverified timing phases on the natural route. Two selected upward transfers already passed without Catnip; they do not require another boarding implementation. Compare bonus behavior only for a genuinely uncovered route/timing case.
- [ ] **MOVE-08 / P1 / VERIFY:** Check elevators, moving carriers and crumbling platforms: passenger entry/exit, jump, crouch, underside contact and overlapping supports. Investigate the old carrier-removal comment only after reproducing a concrete failure.
- [ ] **MOVE-09 / P0 / VERIFY:** Remaining: held-input death/reload and other checkpoint/terrain/ladder/platform combinations. Level-1 checkpoint-1 real save/menu reload, actual ordinary death and right/left/right walking already passed. Do not rerun that same checkpoint by default or generalize it to every spawn.

Movement follow-up: [debug41 first/leafy ladders, flat edges, attached rope and pause checks](docs/validation/LADDER-EDGES-0.4.41.md) passed their stated assertions. Remaining natural snag, ladder interruption/transfer combinations and rope visual/slow-frame cases above stay open; this is not a blanket movement pass.

[Debug42 movement/lifecycle follow-up](docs/validation/MOVEMENT-LIFECYCLE-0.4.42.md) repeats leafy caps, neutral ladder pause, attached rope and ordinary-death checkpoint movement on the current installed artifact. Both selected cyclic-platform transfers landed without Catnip. Focus/held-axis release, isolated interrupted-import recovery and late save export also passed. Broader geometry, physical input, provider UI and interruption requirements remain open.

Checkpoint follow-up: [debug41 reload and ordinary-death respawn movement](docs/validation/CHECKPOINT-RESPAWN-0.4.41.md) passed right/left/right traversal at level-1 checkpoint 1 without jumping. A failed premature fade read is retained separately. This does not close every MOVE-09 geometry/input combination.

## Ordinary enemies, hitboxes and recovery

- [ ] **COMBAT-01 / P0 / OPEN:** Reproduce the level 1 sword enemy attacking a lower-standing hero on stairs. Keep offensive AI active. Record attack acceptance, hurt entry/exit, overlap and available escape/counter timing. Separate a reach mismatch from hurt-state input suppression and repeated stagger. Done: original-supported behavior or a clearly documented accommodation, plus a playable human recheck.
- [ ] **COMBAT-02 / P0 / VERIFY:** Remaining: requested postures/phases not actually observed, ascent/descent, relevant projectiles and other enemy archetypes, plus the reported natural stairs. Active Soldier observations already cover both sides and 16/32/48/64 px offsets; keep their recorded misses and limits. Do not restart the whole offset matrix without a relevant combat change.
- [ ] **COMBAT-03 / P1 / VERIFY:** Check one damage event per intended window, multi-target contacts, leaving/re-entering reach, simultaneous hits, invulnerability and interrupted attacks. Ensure a late animation callback cannot damage after death or actor removal.
- [x] **COMBAT-04 / P1 / DONE:** Reconcile the current packaged attack inventory with runtime handlers after each change. Check every referenced ANI exists and its event frames are valid; distinguish metadata that executes from unused configuration.
- [ ] **COMBAT-05 / P1 / RESEARCH:** Crab: compare original sprite/PID-derived strike rectangles, continuous contact and re-hit rules with the port's configured sensor. The reconstructed 203/204 window is not complete collision parity.
- [ ] **COMBAT-06 / P1 / RESEARCH:** Fish: recover swimming-home eligibility and the separate JumpStrike path. Verify attack rectangles and re-hit rules. Captured-X horizontal lunges do not implement every original Fish branch.
- [ ] **COMBAT-07 / P1 / RESEARCH:** Tiger Guard: recover home/obstacle decisions, per-state hit-reaction flags, knife-chain contact persistence/refacing and edge behavior. Existing three-move timing evidence does not certify full hurt/parry behavior.
- [ ] **COMBAT-08 / P1 / VERIFY:** Remaining: Siren visibility/slow-frame burst behavior and missing/undecodable custom-sound duration cases. Actual interruption, death and no stale burst emission already passed in debug40. Do not reimplement those paths or generalize supplied-data duration findings to custom assets.
- [x] **COMBAT-09 / P1 / DONE:** Generic attack cases, deferred frame-zero delays and the production exact/float-collapsed zero-ray guard passed the [debug38 device fixtures](docs/validation/UPDATE-0.4.38.md). The exact zero-length query was already executed. Repeat only after affected animation/physics/raycast changes or in the final candidate suite; broader interruption/multi-target requirements remain COMBAT-03.
- [ ] **COMBAT-10 / P1 / RESEARCH:** Review remaining ordinary families against versioned original evidence, including projectile origin, direction, damage, health and attack eligibility. Prioritize player-visible discrepancies instead of globally changing health or attack speed.

Family evidence: [attack inventory](docs/validation/ENEMY-ATTACK-INVENTORY-0.4.38.md), [custom melee](docs/validation/CUSTOM-MELEE-0.4.38.md), [Siren](docs/validation/SIREN-BEHAVIOR-0.4.38.md).

Debug41 follow-up: [eight active Soldier reactions on a 32 px step](docs/validation/ACTIVE-SOLDIER-0.4.41.md). Standing counters and jump-away escapes occurred on both sides, but one requested short jump never took off. This does not close COMBAT-01/02 or establish original balance.

The same report now includes corrected-facing 48 px trials and a **64 px reach asymmetry**: sampled standing attacks missed the higher enemy while its attack still contacted Claw; jump-away escape remained possible. Cached original attack-construction evidence confirms different per-attack bounds, but the origin/collision mapping is not joined. Do not close this as a passing balance test or enlarge every hitbox indiscriminately.

Later coverage adds 16 px enemy-above reactions and 24 hero-above observations across 16/32/48/64 px. Some requested postures were not sampled, so completion of the fixture is not completion of every requested action. Existing per-update jump measurement additionally recorded one 264 ms held-jump trial with **0 px rise** and a standing buffered attack. The later synchronized debug42 observations establish that the short hold ended during hurt and longer holds jumped after recovery/attack; no new buffer defect is proved by that zero-rise case. Keep natural stair/original-policy questions separate, and do not claim physical touchscreen latency from diagnostic keys.

## Bosses and finale

- [ ] **BOSS-01 / P0 / VERIFY:** For each boss, check normal entry, phase transitions, accepted/rejected hits, death, restart and re-entry. Check resources available through the human's actual route; controlled victories do not establish normal ammo availability or balance.
- [ ] **BOSS-02 / P1 / RESEARCH:** Le Rauxe: recover the full Home/proximity/movement and jump-over branches, when the 300-600 ms pause applies, the hurt/collision immunity pipeline and projectile-handler categories. The recovered 100/1001 cached ordinary melee predicate is not a blanket block rate for every incoming hit.
- [ ] **BOSS-03 / P1 / VERIFY:** Le Rauxe: test sustained ordinary melee and already-parrying overlaps with natural resources. Preserve separate conclusions for the recovered predicate and the port's remaining cadence approximation.
- [ ] **BOSS-04 / P1 / RESEARCH:** Gabriel: compare original pirate-count decrement lifecycle, idle choice, pending cannon commands while busy and interruption/reset rules. Also replace the immediate vertical HP shortcut only after joining the original firing-animation signal, actual cannonball collision and boss acceptance; a pending boolean alone is insufficient. The current weak-reference/health lifecycle and observed two-pirate cap are not proof of all original paths. [Additional static boundaries](docs/validation/ORIGINAL-FOLLOWUP-2026-11-08.md#additional-cannon-boundary-2026-11-08).
- [ ] **BOSS-05 / P1 / RESEARCH:** Red Tail: recover Home/movement eligibility, sustained kick geometry/window lifetime, hurt/parry acceptance and reset policy. Preserve the recovered shared timing gate while investigating these separately.
- [ ] **BOSS-06 / P0 / VERIFY:** Recheck the other encounters, including Aquatis and Omar, for required objects/projectiles, phase progression, recovery after death and a reachable victory without fixture assistance. Record any original-fidelity question separately from an actual softlock.
- [ ] **BOSS-07 / P0 / VERIFY:** Verify final victory, score, transition out, skip/replay input and persistence. Explain that the staged engine finale is not proof of original movie playback or an identical original presentation.

Starting evidence: [boss behavior](docs/validation/BOSS-BEHAVIOR-0.4.38.md). Natural encounter acceptance belongs to the human campaign checklist below.

## Touch, pause and menus

[Debug43 menu/settings acceptance](docs/validation/MENU-SETTINGS-0.4.43.md) adds PL/EN page navigation and sliders, gameplay-options assertions, focused score progression, both actual Game Over corners and limited visual review. Own-app virtual-input focus recovery passed with zero resumed drift. This narrows the items below; physical multitouch/controllers, other display configurations and wider lifecycle cases remain distinct.

- [ ] **INPUT-01 / P0 / VERIFY:** Remaining: rapid repeated taps, Catnip/slow-frame combinations and any required physical finger-to-action measurement. Normal short/held/release software-input cases already passed, including debug43; their queue timings are not physical touchscreen latency. Do not reopen the minimum-jump fix without new evidence.
- [ ] **INPUT-02 / P0 / VERIFY:** Test movement stick plus jump/attack/fire simultaneously; release outside buttons, pointer cancellation and finger crossing. No stuck action or lost release after pause/resume.
- [ ] **INPUT-03 / P1 / VERIFY:** Remaining: other small/wide/safe-area configurations and actual upgrade preservation of populated layout preferences. Enlarged controls, editable layouts and the PAD relocation already exist; current selected PL/EN settings were checked. Do not treat display coverage as an unimplemented layout feature.
- [ ] **INPUT-04 / P0 / VERIFY:** Remaining: physical reported GameSir pause behavior when the controller is available within scope. Raw-Start pause/resume dispatch already passed virtually; repeating that helper is not the missing Bluetooth/device evidence. Broad controller coverage remains deferred under INPUT-05.
- [ ] **INPUT-05 / P2 / DEFERRED:** Broad Bluetooth/USB controller coverage, reconnection and model matrix. Resume only when requested. Huawei custom-ROM Bluetooth pairing is separate from game input support; red Pro Controller mode worked historically, yellow mode discovery did not.
- [ ] **UI-01 / P0 / VERIFY:** Remaining: unreviewed Android subpages/message paths, English Game Over/score visual review and untested display variants. Current PL/EN native navigation, sliders, return/cancel, unsupported-entry removal, focused score progression and Polish Game Over exit already passed. Recheck completed routes only for a relevant UI change or the frozen final candidate.
- [x] **UI-02 / P1 / DONE:** Confirm the three working difficulty presets and controls settings remain functional and clearly described as port features where appropriate. Do not remove difficulty on the assumption it is a dead option.
- [x] **UI-03 / P0 / DONE:** The reported Huawei Game Over ambiguity/crash path is fixed and technically verified: distinct title/divider, one whole-screen instruction, focused-window center tap and both actual 853x480 corners return to the main menu without a crash. [Debug43 evidence and Polish visual review](docs/validation/MENU-SETTINGS-0.4.43.md). Other language/display review remains UI-01/LANG-01; final-artifact acceptance remains RELEASE-02.
- [x] **UI-04 / P1 / DONE:** Re-audited Voice/Ambient options from the [historical comment audit](docs/validation/TODO-AUDIT.md). Independent switches are unsupported and disabled; the shared sound control remains functional. Exact debug40 PL/EN menu tests verified they stay disabled after mute/unmute, and the production ambient mixer passed gain/mute/resume checks. [Dated evidence and limitations](docs/validation/UPDATE-0.4.40.md).

## Audio, bonus effects and language

Debug43 [fatal-hero and actual Red Tail follow-up](docs/validation/UPDATE-0.4.43.md#fatal-hero-and-actual-red-tail-hurt-follow-up) confirms one current death cue after real fatal enemy damage/normal respawn, and one corrected boss voice after an accepted arena melee hit. These are combined-output/request observations, not subjective listening or full encounter acceptance. Ordinary fatal melee currently uses the death-tile cue; original policy remains unverified. AUDIO-01 stays open for its wider requirements.

- [ ] **AUDIO-01 / P0 / VERIFY:** Remaining: human listening, untested families/custom paths, distance/concurrency and original death-cue policy. Gain/ambient fixes, selected 10%/100% attack output, Soldier/Officer/hero hurt/death and actual Red Tail hurt already have bounded evidence. Do not reimplement or repeatedly retest the same missing-voice fix. Perform one final candidate regression.
- [ ] **AUDIO-02 / P0 / VERIFY (regression acceptance, not a newly confirmed defect):** The earlier Catnip instrument-loading stall was fixed by preparing music before gameplay; prepared switches subsequently measured 1/1/2 ms. No new recurrence has been established. Confirm the complete actual pickup path on the frozen candidate, including first/subsequent collection frame time, timer sound, expiry and music restoration. Do not reopen optimization without a reproduced regression; retain meaningful frame-time evidence rather than only average FPS.
- [ ] **AUDIO-03 / P1 / VERIFY:** Remaining: untested audio-output-device/focus changes and lost/duplicate-channel cases. Mute/unmute, slider commits, historical orderly volume persistence and current selected mixer paths already passed. Preserve user settings; this is not a request to rebuild the working volume system.
- [ ] **LANG-01 / P1 / VERIFY:** Remaining: unreviewed import/error/help/long-label paths and populated-language preference preservation across the final update. PL/EN selection and app-owned/native translations already exist; current menu paths passed in both languages. Original Polish recordings are not missing English UI code (LANG-02).
- [ ] **LANG-02 / P1 / RESEARCH:** If a player supplies a lawful English copy, document data selection and edition compatibility, then test English voices using that copy. No rights-cleared redistributable English voice pack has been established. Do not bundle or link an unlicensed asset download as an installation solution.

See [game language boundaries](docs/GAME-LANGUAGE.md).

## Installation, saves and lifecycle

- [ ] **INSTALL-01 / P0 / VERIFY:** A novice follows the English guide on a clean setup using their own data, without developer assistance. Repeat the applicable Polish instructions. Record confusing screens and revise the guide from observed difficulties.
- [ ] **INSTALL-02 / P0 / VERIFY:** Finish large-file DocumentsUI selection, external document-provider behavior and save backup/restore through the real picker. Existing REZ/ZIP, cancellation and import-transaction checks do not cover every provider.
- [ ] **INSTALL-03 / P0 / VERIFY:** Final gate only unless import code changes or a new failure appears: recheck cancellation, corruption, insufficient space and interruption on the frozen candidate using existing tests. Transaction recovery, bounded real process deaths and earlier full-disk cases are already implemented/tested. Real picker/provider UX is INSTALL-02, not a reason to reimplement the importer.
- [ ] **INSTALL-04 / P0 / VERIFY:** Remaining: exact final signing/update path with populated language, binding and layout preferences. Existing debug upgrades preserved checked external files; their absent private preference XML does not prove populated preference preservation. Never uninstall user data to bypass a signature mismatch.
- [ ] **INSTALL-05 / P0 / VERIFY:** Remaining: actual picker save export/import round trip, partial-provider failures and restored progress on the final candidate. Save validation and late-Activity export completion already passed. Reuse those fixes; protect the only user copy and avoid duplicating INSTALL-02 picker work.
- [ ] **LIFE-01 / P0 / VERIFY:** Remaining: screen lock and relevant system-process-death cases from menus/gameplay. Own-app focus return, held virtual-input release and fresh movement already passed, including debug43. Reuse that evidence; do not present every background/resume task as untested.
- [ ] **LIFE-02 / P1 / VERIFY:** Check renderer/audio resource recreation, no duplicate actors or callbacks, correct pause state and stable repeated level reloads. Inspect memory retention rather than treating every allocation as a leak.

## Performance and Android coverage

- [ ] **PERF-01 / P1 / VERIFY:** Final measurement gate: report the frozen APK in the agreed heavy Huawei scene, frame distributions/stalls, viewport and thermal state. Existing measurements remain versioned evidence. Under the November 8 decision, 55/60 FPS are desired targets, not mandatory release floors; do not start another optimization cycle without a measured regression or a sensible proposed improvement.
- [ ] **PERF-02 / P0 / VERIFY:** Remaining: dense combat, repeated transitions and memory-retention evidence, plus one final warm-candidate observation. The debug42 protected stationary 1200-second run already passed continuous foreground checks and restoration. Do not repeat that same scene on every development version or call it a full combat/transition/memory pass.
- [ ] **PERF-03 / P1 / VERIFY:** Only if further optimization is justified: isolate the remaining CPU/render/GPU-wait/audio bottleneck with identical scene/settings. Prior dependency/render/input-cache, physics and music-preparation work already has measurements. Record rejected experiments; preserve image quality, AI cadence and physics. This is not a mandatory new FPS investigation when the accepted limitation has not regressed.
- [ ] **PERF-04 / P1 / VERIFY:** Investigate delayed/low jumping during very long frames observed on the Android 15 emulator. Determine whether this is input sampling, time integration or emulator behavior; do not infer physical-phone failure from it alone.
- [x] **ANDROID-01 / P0 / DONE:** Publish an exact-build compatibility matrix: device/ROM, Android, ABI, RAM, GPU, installation, gameplay/lifecycle scope and failures. Distinguish compiled, emulator-tested and physical-device-tested.
- [ ] **ANDROID-02 / P0 / VERIFY:** Remaining: allocated additional hardware/runtime coverage and the final declared candidate matrix. Huawei ARM64 debug43 is already fixture-tested. Obtain a new allocation before Redmi use; separately qualify ARMv7 runtime on suitable hardware. Compilation and ARMv7 selection on a 64-bit phone do not prove 32-bit-only device performance.
- [ ] **ANDROID-03 / P1 / VERIFY:** Establish final-candidate minimum/newer Android coverage, storage/picker behavior, focus recovery and relevant screen shapes. State missing configurations honestly rather than promising all Android versions.
- [ ] **ANDROID-04 / P1 / VERIFY:** Remaining: physical 16 KB ARM runtime when hardware is available, and one final artifact alignment check. Both-ABI packaging and static native alignment already passed for debug43; historical 16 KB x86_64 emulator evidence remains separate. Do not rework alignment merely because hardware validation is unavailable.

## Natural campaign acceptance: human tester

All rows remain unchecked until linked natural-play evidence exists. Technical map starts, teleports, invulnerability, altered health/ammo and controlled boss fixtures do not qualify. Engineering may reproduce a reported bug without taking over the campaign.

For each level record: APK/data edition and difficulty, entry resources, checkpoints, significant enemies/platforms, deaths/reloads, exit/resources and remaining issues. Maintain a continuous route; document any replay caused by an update. Exact pixel-perfect original parity is a separate research claim.

| Done | ID | Level | Required evidence |
| --- | --- | --- | --- |
| [ ] | CAMP-01 | 1 | Natural entry through exit; checkpoints, cyclic platforms, ladder/edge regressions |
| [ ] | CAMP-02 | 2 | Natural route and boss; reported leftward platform blockage recheck |
| [ ] | CAMP-03 | 3 | Natural route; leafy ladder tops and swinging vines |
| [ ] | CAMP-04 | 4 | Natural route, encounter progression and exit |
| [ ] | CAMP-05 | 5 | Natural route, checkpoints and exit |
| [ ] | CAMP-06 | 6 | Natural route, encounter progression and exit |
| [ ] | CAMP-07 | 7 | Natural route, checkpoints and exit |
| [ ] | CAMP-08 | 8 | Natural route, encounter progression and exit |
| [ ] | CAMP-09 | 9 | Natural route, checkpoints and exit |
| [ ] | CAMP-10 | 10 | Natural route, encounter progression and exit |
| [ ] | CAMP-11 | 11 | Natural route, aquatic enemies and exit |
| [ ] | CAMP-12 | 12 | Natural route, encounter progression and exit |
| [ ] | CAMP-13 | 13 | Natural route, dense combat and exit |
| [ ] | CAMP-14 | 14 | Natural route, final encounter and complete ending flow |

- [ ] **CAMP-15 / P0 / VERIFY:** Human confirms all 14 rows, normal resource continuity and no progression-blocking issue. Link reports rather than asserting completion from the table itself.

## Original-game investigation and upstream maintenance

- [ ] **ORIGINAL-04 / P1 / RESEARCH (active explicit goal, 2026-11-12):** Audit the entire supplied executable through REA, with a complete function and executable-range coverage ledger, semantic review, port comparisons and explicit unresolved dependencies. [Scope, initial inventory and completion contract](docs/validation/REA-FULL-AUDIT.md). Enumeration/decompilation is not semantic completion; earlier focused findings must be migrated with evidence rather than restarted blindly.

- [x] **ORIGINAL-01 / P1 / DONE:** Keep a behavior comparison ledger: observation, supplied-binary finding, inference, intentional port difference or unknown. Include exact binary/data version and evidence limits for each conclusion.
- [ ] **ORIGINAL-02 / P1 / RESEARCH:** Where feasible, capture controlled original Windows behavior for jump height, ledges, ladders, hurt recovery and boss timing using a matching edition. No original-runtime timing has been established by static analysis alone.
- [x] **ORIGINAL-03 / P1 / DONE:** Preserve provenance: the supplied CrazyHook-distributed CLAW.EXE used for current research is not certified pristine 1997 and is not original source code. Keep raw executable/disassembly/assets private; publish concise independent findings and adaptation patches.
- [x] **SOURCE-01 / P1 / DONE:** Review relevant source TODOs/comments against executable paths and current behavior. Mark obsolete comments or document genuine gaps; incomplete export helpers alone do not prove gameplay defects.
- [x] **SOURCE-02 / P0 / DONE:** Reproduced debug41 from archived build-input commit `cf93e5c4d2a4c1b6ee82da4e3e0d1467a357d7e3` and locked upstream Git revisions, applying committed patches into fresh sources/native objects. ARM64/ARMv7 and a separate x86_64 build passed without copying upstream working-tree changes or commercial data. [Exact identities and limits](docs/validation/UPDATE-0.4.41.md): installed SDK/JDK and cached Gradle dependencies were used; this is not a clean-machine bootstrap or byte-identical APK claim. Repeat if required build inputs change before release.
- [x] **SOURCE-03 / P1 / DONE:** Update upstream-difference documentation and attribution for imported ideas/code. Distinguish this Android adaptation from OpenClaw work and from findings in other repositories.
- [x] **SOURCE-04 / P1 / DONE:** Keep regression tests focused on observed failures and real contracts. Validate fixtures actually exercise the intended state; retain meaningful failed attempts instead of counting setup failures as passes.

## Public documentation, privacy and release

- [ ] **DOC-01 / P1 / VERIFY:** Final documentation gate: update versions, tested matrix, links and novice PL/EN guidance for the frozen release. English GitHub guides and the short owned-data installation path already exist; improve observed confusing steps instead of rewriting them from scratch.
- [ ] **DOC-02 / P1 / VERIFY:** Final consistency gate: keep TODO, checklist, roadmap and limitations aligned with actual remaining work. The November 10 reconciliation separates completed fixes, missing coverage and final checks. Do not revive historical plan items or relabel old results as new APK evidence.
- [x] **DOC-03 / P1 / DONE:** Explain remaining original differences, Android coverage, English-voice limitations, controller scope and engine-staged finale. Mark supported port-specific features clearly.
- [ ] **LEGAL-01 / P0 / VERIFY:** Check the distributable source/APK/archive contains no commercial game assets, supplied executable, raw proprietary dumps, user saves, identifiers or private reports. Preserve GPL and third-party notices; do not assume the game's copyright expired.
- [ ] **LEGAL-02 / P0 / VERIFY:** Preserve anonymous human participation, explicit OpenAI Codex (LLM) adaptation disclosure and separate upstream authorship in public docs and metadata. Review public history using the private-pattern check without committing its private input.
- [ ] **RELEASE-01 / P0 / VERIFY:** Prepare the exact signed candidate, matching source commit/tag and SHA-256 checksums. Verify signing/update identity; keep keystore/password material private and backed up outside public distribution.
- [ ] **RELEASE-02 / P0 / VERIFY:** Run candidate-specific installation, runtime, regression and compatibility checks. Link failures and remaining untested coverage. A debug APK pass does not automatically certify a separately packaged signed artifact.
- [ ] **RELEASE-03 / P0 / VERIFY:** Write release notes separating fixes, intentional differences, open limitations and exact tested configurations. Do not call a public source push or test APK release 1.0.
- [ ] **RELEASE-04 / P0 / VERIFY:** Before 1.0, close crashes, progression softlocks, save-loss defects and required acceptance gates; obtain the human's campaign results. Resolve P1 research scope explicitly where original parity remains unknown. Publish only claims supported by evidence.

Release procedure: [publishing](docs/PUBLISHING.md), [signing/migration](docs/RELEASE-SIGNING.md), [building](docs/BUILDING.en.md), [testing](docs/TESTING.md), [contributing](CONTRIBUTING.en.md).

## Bug report and task closure template

Copy the fields into a report; exclude device serials, personal paths, commercial assets and signing material from public attachments.

```text
Task ID / short title:
Date and tester type (human natural play / technical fixture):
App version, source commit and APK SHA-256:
Device model, Android/ROM, ABI and relevant settings:
Game-data edition/version (no copyrighted files attached):
Level, approximate position/checkpoint and entry resources:
Input method and exact reproduction steps:
Expected behavior and its evidence (original / port contract / unknown):
Observed behavior, frequency and recovery method:
Fixture changes (teleport, protection, AI disabled, edited resources), if any:
Relevant sanitized recorder/log excerpt and screenshot/video reference:
Fix or explicit scope decision:
Verification on the fixed exact candidate, including negative cases:
Remaining limitations and human recheck needed:
```

A task is closed only when its stated completion condition has evidence or an explicit recorded scope decision. Keep unresolved user reports visible even when a neighboring issue has been fixed.

Earlier completion evidence for COMBAT-04 and UI-02: [debug40 inventory and gameplay-options results](docs/validation/UPDATE-0.4.40.md). Other combat/UI gates retain their own wider completion requirements.

ANDROID-01 publication evidence: [current exact-candidate matrix](docs/validation/ANDROID-COMPATIBILITY.md). Publishing the matrix does not close its explicitly untested runtime configurations (ANDROID-02/03/04).
