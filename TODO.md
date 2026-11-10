# Project TODO and release backlog

Updated **2026-11-10** by OpenAI Codex (LLM), guided by anonymous human requirements and feedback. Adaptation authorship is separate from OpenClaw and dependency authorship.

This is the detailed, actionable backlog. The [roadmap](docs/ROADMAP-1.0.md) summarizes release gates; the [handoff](docs/HANDOFF.md) records current state and operating constraints. An unchecked item means work or evidence is still required, not necessarily that a defect has been proved.

## Current execution plan for 1.0

Follow the [remaining-work checklist](docs/RELEASE-1.0-CHECKLIST.md), reviewed against commits, local changes and saved reports on November 10. It groups this backlog into eight ordered gates: pending audio; reported movement/combat blockers; encounters/original-policy decisions; touch/menus/language; installation/save safety; declared Android coverage/stability; human campaign acceptance; and the exact signed release. Stable task IDs below remain authoritative. Do not restart completed fixtures without a relevant change or missing acceptance condition.

The [debug43 audio correction](docs/validation/UPDATE-0.4.43.md) now has baseline/fixed ARM64 evidence for Soldier hurt/death, Officer impact and hero hurt; wider listening and boss coverage remain open. The saved debug42 20-minute heavy-scene run **has completed successfully**, including runner checks of restored user configuration/progress and unchanged APK; its scope is protected stationary observation, not debug43 or full-campaign acceptance. See the checklist for exact versions, evidence and remaining limits.

## Completed in the current follow-up

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

## Recommended next engineering work

Debug42 adds [input triggered after actual enemy damage](docs/validation/UPDATE-0.4.42.md). Four synchronized active-Soldier observations distinguish short input ending during hurt from held input surviving recovery; both sword trials defeated the target. This narrows COMBAT-01/02 without closing natural stairs, original policy or broader geometry. No gameplay priority or balance was changed.

1. Capture the next live level 2 blockage before jumping, restarting or moving away (MOVE-01).
2. Reproduce lower-hero diagonal combat with active enemy AI and trace damage/recovery windows (COMBAT-01).
3. Recheck touch, Game Over, audio and reported pause regressions on the exact candidate (INPUT, UI, AUDIO).
4. Resolve or explicitly scope the remaining original-behavior questions (ORIGINAL and BOSS).
5. Measure the final candidate on Huawei, then obtain device allocation for missing compatibility checks (PERF and ANDROID).
6. Close installation/documentation/release gates while the human independently reports campaign results. Do not autonomously take over that playthrough.

## Movement, contacts and platforms

- [ ] **MOVE-01 / P0 / OPEN:** Diagnose level 2 leftward small-platform blockage near the crate at approximately (2460, 4956). Seventeen earlier attempts did not reproduce it. Use the [existing capture instructions](docs/validation/LEVEL2-PLATFORM-0.4.34.md) and [background recorder](docs/BACKGROUND-DEBUGGING.md). Capture requested input, velocity, foot/support state, contact normals and nearby geometry before escape. Done: reproducible cause, bounded fix, regression at that geometry and human recheck; otherwise retain OPEN.
- [ ] **MOVE-02 / P0 / VERIFY:** Revisit both recorded level 1 snag locations. Test traversal in both directions, standing, crouching and after jumping back. Confirm the floor-join fix does not create a wall foothold or allow a held jump to trigger an unintended second jump halfway up a wall.
- [ ] **MOVE-03 / P0 / VERIFY:** Exercise flat-foot ledges and tile joins at small offsets, including stopping on the last supported pixel, walking off and reversing. Done: stable legitimate support, clean loss of support, no snag, false grounding or rounding-dependent slide.
- [ ] **MOVE-04 / P0 / VERIFY:** Recheck first level 1 ladder and leafy level 3 ladder tops with early input release, held up, jump-away, sideways transfer and down re-entry. Confirm neither a false falling animation nor a fall through the cap remains.
- [ ] **MOVE-05 / P1 / VERIFY:** Test ladder bottoms, mid-ladder jump/hurt, death, pause and restoration. Check animation agrees with actual movement and a ladder cannot retain control after leaving it.
- [ ] **MOVE-06 / P1 / VERIFY:** Observe level 3 swinging vines across attachment, reversal, release, reattachment and low FPS. Check hero/rope visual alignment and smooth motion without changing swing reach to hide interpolation defects.
- [ ] **MOVE-07 / P0 / VERIFY:** Test cyclic disappearing platforms in level 1 through boarding, disappearance underfoot and return. Separate timing difficulty from collision failure. Compare ordinary and Catnip jumps; do not assume the bonus is required without route evidence.
- [ ] **MOVE-08 / P1 / VERIFY:** Check elevators, moving carriers and crumbling platforms: passenger entry/exit, jump, crouch, underside contact and overlapping supports. Investigate the old carrier-removal comment only after reproducing a concrete failure.
- [ ] **MOVE-09 / P0 / VERIFY:** Check checkpoint respawn next to terrain, ladders and platforms. No persistent blocked movement, stale contacts or invalid spawn support may survive death/reload.

Movement follow-up: [debug41 first/leafy ladders, flat edges, attached rope and pause checks](docs/validation/LADDER-EDGES-0.4.41.md) passed their stated assertions. Remaining natural snag, ladder interruption/transfer combinations and rope visual/slow-frame cases above stay open; this is not a blanket movement pass.

[Debug42 movement/lifecycle follow-up](docs/validation/MOVEMENT-LIFECYCLE-0.4.42.md) repeats leafy caps, neutral ladder pause, attached rope and ordinary-death checkpoint movement on the current installed artifact. Both selected cyclic-platform transfers landed without Catnip. Focus/held-axis release, isolated interrupted-import recovery and late save export also passed. Broader geometry, physical input, provider UI and interruption requirements remain open.

Checkpoint follow-up: [debug41 reload and ordinary-death respawn movement](docs/validation/CHECKPOINT-RESPAWN-0.4.41.md) passed right/left/right traversal at level-1 checkpoint 1 without jumping. A failed premature fade read is retained separately. This does not close every MOVE-09 geometry/input combination.

## Ordinary enemies, hitboxes and recovery

- [ ] **COMBAT-01 / P0 / OPEN:** Reproduce the level 1 sword enemy attacking a lower-standing hero on stairs. Keep offensive AI active. Record attack acceptance, hurt entry/exit, overlap and available escape/counter timing. Separate a reach mismatch from hurt-state input suppression and repeated stagger. Done: original-supported behavior or a clearly documented accommodation, plus a playable human recheck.
- [ ] **COMBAT-02 / P0 / VERIFY:** Extend active vertical combat coverage to both facing directions and 16/32/48/64 px height offsets, standing/crouching and ascent/descent. Include sword and relevant projectiles. Earlier disabled-AI fixtures do not establish a fair active encounter.
- [ ] **COMBAT-03 / P1 / VERIFY:** Check one damage event per intended window, multi-target contacts, leaving/re-entering reach, simultaneous hits, invulnerability and interrupted attacks. Ensure a late animation callback cannot damage after death or actor removal.
- [x] **COMBAT-04 / P1 / DONE:** Reconcile the current packaged attack inventory with runtime handlers after each change. Check every referenced ANI exists and its event frames are valid; distinguish metadata that executes from unused configuration.
- [ ] **COMBAT-05 / P1 / RESEARCH:** Crab: compare original sprite/PID-derived strike rectangles, continuous contact and re-hit rules with the port's configured sensor. The reconstructed 203/204 window is not complete collision parity.
- [ ] **COMBAT-06 / P1 / RESEARCH:** Fish: recover swimming-home eligibility and the separate JumpStrike path. Verify attack rectangles and re-hit rules. Captured-X horizontal lunges do not implement every original Fish branch.
- [ ] **COMBAT-07 / P1 / RESEARCH:** Tiger Guard: recover home/obstacle decisions, per-state hit-reaction flags, knife-chain contact persistence/refacing and edge behavior. Existing three-move timing evidence does not certify full hurt/parry behavior.
- [ ] **COMBAT-08 / P1 / VERIFY:** Siren: test interruption, death, visibility changes and slow frames during bursts; document missing/undecodable sound duration behavior. Do not generalize stock-data sound-duration findings to custom assets.
- [ ] **COMBAT-09 / P1 / VERIFY:** Regression-test generic attacks, deferred frame-zero emissions and the line-of-sight degenerate-ray guard after shared animation/physics changes. Include an actual zero-length ray, not only a near-zero approximation.
- [ ] **COMBAT-10 / P1 / RESEARCH:** Review remaining ordinary families against versioned original evidence, including projectile origin, direction, damage, health and attack eligibility. Prioritize player-visible discrepancies instead of globally changing health or attack speed.

Family evidence: [attack inventory](docs/validation/ENEMY-ATTACK-INVENTORY-0.4.38.md), [custom melee](docs/validation/CUSTOM-MELEE-0.4.38.md), [Siren](docs/validation/SIREN-BEHAVIOR-0.4.38.md).

Debug41 follow-up: [eight active Soldier reactions on a 32 px step](docs/validation/ACTIVE-SOLDIER-0.4.41.md). Standing counters and jump-away escapes occurred on both sides, but one requested short jump never took off. This does not close COMBAT-01/02 or establish original balance.

The same report now includes corrected-facing 48 px trials and a **64 px reach asymmetry**: sampled standing attacks missed the higher enemy while its attack still contacted Claw; jump-away escape remained possible. Cached original attack-construction evidence confirms different per-attack bounds, but the origin/collision mapping is not joined. Do not close this as a passing balance test or enlarge every hitbox indiscriminately.

Later coverage adds 16 px enemy-above reactions and 24 hero-above observations across 16/32/48/64 px. Some requested postures were not sampled, so completion of the fixture is not completion of every requested action. Existing per-update jump measurement additionally recorded one 264 ms held-jump trial with **0 px rise** and a standing buffered attack. Investigate recovery/input ordering; do not dismiss all absent jumps as sampling artifacts or claim touchscreen latency from diagnostic keys.

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

- [ ] **INPUT-01 / P0 / VERIFY:** Measure short jump taps and press-to-action latency under ordinary and slow frames. Check minimum jump, held jump, release and rapid repeated taps with/without Catnip. Avoid attributing a reproducible input bug to the phone screen without evidence.
- [ ] **INPUT-02 / P0 / VERIFY:** Test movement stick plus jump/attack/fire simultaneously; release outside buttons, pointer cancellation and finger crossing. No stuck action or lost release after pause/resume.
- [ ] **INPUT-03 / P1 / VERIFY:** Check enlarged buttons/custom layouts on small and wide displays, safe areas and both UI languages. Keep PAD/configuration controls clear of health and other HUD information; confirm saved layouts survive updates.
- [ ] **INPUT-04 / P0 / VERIFY:** Recheck specifically reported controller pause behavior if a controller is available within authorized scope. Distinguish Start mapping, game pause dispatch and Android system navigation. Do not silently expand this into the deferred broad controller matrix.
- [ ] **INPUT-05 / P2 / DEFERRED:** Broad Bluetooth/USB controller coverage, reconnection and model matrix. Resume only when requested. Huawei custom-ROM Bluetooth pairing is separate from game input support; red Pro Controller mode worked historically, yellow mode discovery did not.
- [ ] **UI-01 / P0 / VERIFY:** Check every visible menu action in PL/EN, including return/cancel paths, pause, score and Game Over. Unsupported multiplayer entries were removed; do not restore placeholders.
- [x] **UI-02 / P1 / DONE:** Confirm the three working difficulty presets and controls settings remain functional and clearly described as port features where appropriate. Do not remove difficulty on the assumption it is a dead option.
- [ ] **UI-03 / P0 / VERIFY:** On loss of the last life, distinguish the Game Over title from actionable choices. Instructions must describe the actual touch target. Test tapping each choice and background areas; no crash, ambiguous global-tap wording or inescapable screen.
- [x] **UI-04 / P1 / DONE:** Re-audited Voice/Ambient options from the [historical comment audit](docs/validation/TODO-AUDIT.md). Independent switches are unsupported and disabled; the shared sound control remains functional. Exact debug40 PL/EN menu tests verified they stay disabled after mute/unmute, and the production ambient mixer passed gain/mute/resume checks. [Dated evidence and limitations](docs/validation/UPDATE-0.4.40.md).

## Audio, bonus effects and language

Debug43 [fatal-hero and actual Red Tail follow-up](docs/validation/UPDATE-0.4.43.md#fatal-hero-and-actual-red-tail-hurt-follow-up) confirms one current death cue after real fatal enemy damage/normal respawn, and one corrected boss voice after an accepted arena melee hit. These are combined-output/request observations, not subjective listening or full encounter acceptance. Ordinary fatal melee currently uses the death-tile cue; original policy remains unverified. AUDIO-01 stays open for its wider requirements.

- [ ] **AUDIO-01 / P0 / VERIFY:** On the final candidate, audibly verify hero sword/gun/hurt and enemy attack/hurt/death effects at low and high master/effects settings. Check simultaneous sounds and distance attenuation. The double-gain fix is not evidence that every cue plays correctly.
- [ ] **AUDIO-02 / P0 / VERIFY (regression acceptance, not a newly confirmed defect):** The earlier Catnip instrument-loading stall was fixed by preparing music before gameplay; prepared switches subsequently measured 1/1/2 ms. No new recurrence has been established. Confirm the complete actual pickup path on the frozen candidate, including first/subsequent collection frame time, timer sound, expiry and music restoration. Do not reopen optimization without a reproduced regression; retain meaningful frame-time evidence rather than only average FPS.
- [ ] **AUDIO-03 / P1 / VERIFY:** Check mute, volume persistence, background/focus loss and audio device changes without duplicate playback or lost channels. Preserve a user's existing settings.
- [ ] **LANG-01 / P1 / VERIFY:** Audit all app-owned PL/EN messages, import errors, help, settings, score additions and long labels. Persist language across normal updates; do not confuse UI translation with recorded dialogue translation.
- [ ] **LANG-02 / P1 / RESEARCH:** If a player supplies a lawful English copy, document data selection and edition compatibility, then test English voices using that copy. No rights-cleared redistributable English voice pack has been established. Do not bundle or link an unlicensed asset download as an installation solution.

See [game language boundaries](docs/GAME-LANGUAGE.md).

## Installation, saves and lifecycle

- [ ] **INSTALL-01 / P0 / VERIFY:** A novice follows the English guide on a clean setup using their own data, without developer assistance. Repeat the applicable Polish instructions. Record confusing screens and revise the guide from observed difficulties.
- [ ] **INSTALL-02 / P0 / VERIFY:** Finish large-file DocumentsUI selection, external document-provider behavior and save backup/restore through the real picker. Existing REZ/ZIP, cancellation and import-transaction checks do not cover every provider.
- [ ] **INSTALL-03 / P0 / VERIFY:** Recheck cancellation, corrupt input, insufficient space and interrupted import on the final candidate using existing bounded tests. Confirm the prior valid installation remains usable and temporary files are cleaned safely.
- [ ] **INSTALL-04 / P0 / VERIFY:** Verify upgrade paths with the correct signing identity, preserving game data, saves, language, bindings and layout. Never solve a signature mismatch by silently uninstalling a user's installation.
- [ ] **INSTALL-05 / P0 / VERIFY:** Validate save export/import, partial failure and restored progress on the final candidate. Use backups; do not overwrite the user's only copy for testing.
- [ ] **LIFE-01 / P0 / VERIFY:** Check background/resume, screen lock, focus changes and system process death from menus and gameplay. Distinguish orderly saved settings from changes lost before an abrupt kill.
- [ ] **LIFE-02 / P1 / VERIFY:** Check renderer/audio resource recreation, no duplicate actors or callbacks, correct pause state and stable repeated level reloads. Inspect memory retention rather than treating every allocation as a leak.

## Performance and Android coverage

- [ ] **PERF-01 / P1 / VERIFY:** Measure the exact final APK in the agreed heavy Huawei scene. On 2026-11-08 the human allowed accepting lower FPS if measurement-led optimizations do not offer a sensible improvement. **55 FPS is an optimization target, no longer a mandatory release floor**; 60 FPS remains desirable. Preserve an honest limitation if the target is missed. Record batch sizes, frame-time distribution, stalls, duration, viewport and thermal state; do not claim an all-frame/all-level minimum.
- [ ] **PERF-02 / P0 / VERIFY:** Run a 20-30 minute warm-device observation, including dense combat and repeated transitions. Record memory, frame-time p95/p99 and worst stalls. Historical 0.4.25 measurements do not certify 0.4.38 or a later candidate.
- [ ] **PERF-03 / P1 / VERIFY:** Profile CPU update, rendering, GPU/vsync waiting, audio decoding and loading separately before optimizing. Compare identical scene/data/settings; preserve visual quality, AI cadence and physics. Retain rejected experiments and explain why they were rejected.
- [ ] **PERF-04 / P1 / VERIFY:** Investigate delayed/low jumping during very long frames observed on the Android 15 emulator. Determine whether this is input sampling, time integration or emulator behavior; do not infer physical-phone failure from it alone.
- [x] **ANDROID-01 / P0 / DONE:** Publish an exact-build compatibility matrix: device/ROM, Android, ABI, RAM, GPU, installation, gameplay/lifecycle scope and failures. Distinguish compiled, emulator-tested and physical-device-tested.
- [ ] **ANDROID-02 / P0 / VERIFY:** Recheck Huawei ARM64 first. Obtain explicit allocation before Redmi checks. Test supported ARMv7 runtime on appropriate hardware when available; ARMv7 compilation does not prove runtime performance or compatibility.
- [ ] **ANDROID-03 / P1 / VERIFY:** Establish final-candidate minimum/newer Android coverage, storage/picker behavior, focus recovery and relevant screen shapes. State missing configurations honestly rather than promising all Android versions.
- [ ] **ANDROID-04 / P1 / VERIFY:** Recheck native library/package alignment and final ARM behavior on actual 16 KB-page hardware when available. Historical x86_64 Android 15 emulator and static alignment checks do not certify final ARM hardware.

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

- [x] **ORIGINAL-01 / P1 / DONE:** Keep a behavior comparison ledger: observation, supplied-binary finding, inference, intentional port difference or unknown. Include exact binary/data version and evidence limits for each conclusion.
- [ ] **ORIGINAL-02 / P1 / RESEARCH:** Where feasible, capture controlled original Windows behavior for jump height, ledges, ladders, hurt recovery and boss timing using a matching edition. No original-runtime timing has been established by static analysis alone.
- [x] **ORIGINAL-03 / P1 / DONE:** Preserve provenance: the supplied CrazyHook-distributed CLAW.EXE used for current research is not certified pristine 1997 and is not original source code. Keep raw executable/disassembly/assets private; publish concise independent findings and adaptation patches.
- [x] **SOURCE-01 / P1 / DONE:** Review relevant source TODOs/comments against executable paths and current behavior. Mark obsolete comments or document genuine gaps; incomplete export helpers alone do not prove gameplay defects.
- [x] **SOURCE-02 / P0 / DONE:** Reproduced debug41 from archived build-input commit `cf93e5c4d2a4c1b6ee82da4e3e0d1467a357d7e3` and locked upstream Git revisions, applying committed patches into fresh sources/native objects. ARM64/ARMv7 and a separate x86_64 build passed without copying upstream working-tree changes or commercial data. [Exact identities and limits](docs/validation/UPDATE-0.4.41.md): installed SDK/JDK and cached Gradle dependencies were used; this is not a clean-machine bootstrap or byte-identical APK claim. Repeat if required build inputs change before release.
- [x] **SOURCE-03 / P1 / DONE:** Update upstream-difference documentation and attribution for imported ideas/code. Distinguish this Android adaptation from OpenClaw work and from findings in other repositories.
- [x] **SOURCE-04 / P1 / DONE:** Keep regression tests focused on observed failures and real contracts. Validate fixtures actually exercise the intended state; retain meaningful failed attempts instead of counting setup failures as passes.

## Public documentation, privacy and release

- [ ] **DOC-01 / P1 / VERIFY:** Keep GitHub guides in clear English with a short novice installation path. Preserve Polish instructions/UI support where intended. Check links, filenames, screenshots, current versions and terminology after candidate changes.
- [ ] **DOC-02 / P1 / VERIFY:** Keep this backlog, roadmap, handoff and known limitations consistent. Archive historical results with exact versions; never silently upgrade old evidence to the newest APK.
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

Current completion evidence for COMBAT-04 and UI-02: [debug40 inventory and gameplay-options results](docs/validation/UPDATE-0.4.40.md). Other combat/UI gates retain their own wider completion requirements.

ANDROID-01 publication evidence: [current exact-candidate matrix](docs/validation/ANDROID-COMPATIBILITY.md#current-candidate-matrix-0440-dev-2026-11-08). Publishing the matrix does not close its explicitly untested runtime configurations (ANDROID-02/03/04).
