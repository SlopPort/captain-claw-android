# Remaining work before 1.0

Reviewed **2026-11-10** by OpenAI Codex (LLM). Human participation is anonymous; upstream authorship remains separate. This is the execution plan for the existing [detailed TODO](../TODO.md), not a replacement for its task IDs or an assertion of completion.

## Verified starting point

- Latest committed work reviewed: `4c24060` and `af143ee`. Debug42 adds synchronized jump/attack-after-damage diagnostics and bounded movement, pause, audio and data-safety evidence. See [debug42](validation/UPDATE-0.4.42.md) and [movement/lifecycle results](validation/MOVEMENT-LIFECYCLE-0.4.42.md).
- Latest verified Huawei runtime artifact: debug **0.4.43-dev**, versionCode 55, SHA-256 `dfedd91134113cacf5f43dbdbe17e6575b0848a43710922eeaea86d777e35b8a`. The November 10 follow-up reconnected only to the allocated Huawei, verified the debug42 baseline, upgraded in place and tested the correction. See [exact scope](validation/UPDATE-0.4.43.md).
- The saved debug42 heavy-scene run completed 1200.415 seconds, with 212 observation batches, continuous foreground evidence and no explicit skipped interval. The runner passed and verified configuration/progress restoration and unchanged APK. Private evidence: `todo-held-pause-stability-0.4.42/results.json`. This protected, stationary level-9 fixture does not certify campaign combat, repeated transitions, memory-leak freedom or a later build.
- Debug **0.4.43-dev** adds configured enemy hurt voices, skips generic impact placeholders and corrects Red Tail's hurt-sound path. Both ARM builds completed; ARM64 baseline/fixed fixtures confirm the bounded correction. Subsequent actual hero death/respawn and actual Red Tail hurt also passed. Other enemy/boss playback, original death-cue policy and human listening remain open. See [audio investigation](validation/HURT-AUDIO-FOLLOWUP.md).
- Public download remains **0.4.41-test**. A successful debug build or previous test release is not 1.0 acceptance.

## 1. Finish and verify pending audio work

- [x] Reproduced the missing voice on preserved debug42 before upgrading; no downgrade or uninstall was used. [Evidence](validation/UPDATE-0.4.43.md).
- [x] Debug43 passed real Soldier nonfatal/fatal contacts, configured voice once, Officer generic impact without duplication and actual incoming hero damage. These bounded checks do not close the wider listening/family matrix.
- [x] Verified Red Tail's actual accepted hurt path in the real arena: ordinary melee contact changed 150 to 140 HP and the corrected voice was accepted once. Protected setup is not full boss acceptance. [Evidence](validation/UPDATE-0.4.43.md#fatal-hero-and-actual-red-tail-hurt-follow-up).
- [x] Observed one current hero fatal cue after real enemy damage and a normal respawn. Original correctness of the cue and subjective listening remain open.
- [ ] Audibly check hero/enemy attack, gun, hurt and death effects, low/high volume and overlapping sounds. Include missing/empty sound definitions without inventing replacement recordings.
- [ ] Confirm the earlier Catnip loading-stall fix on the frozen candidate's actual pickup path, including first/subsequent collection frame time, timer, expiry and music restoration. Prepared switches already measured 1/1/2 ms; no recurrence is currently established. This is regression acceptance, not a new open stall report or a reason to repeat optimization without evidence.
- [ ] Check mute, focus/audio-device changes and persisted volume. Run suitable normal-play regressions after the native change.

Task IDs: AUDIO-01/02/03, COMBAT-03, RELEASE-02. Exit: runtime evidence for the exact corrected APK, restored user data, no unexplained missing/duplicate cue or crash; subjective listening and mixer measurements are labelled separately.

## 2. Resolve reported movement and combat blockers

- [ ] Capture the level-2 leftward platform blockage near (2460, 4956) while blocked, before jumping away; reproduce, fix and retest both directions. Earlier failed reproductions do not close the report.
- [ ] Recheck both reported level-1 snag locations, stopping/reversing/crouching at joins and edges. Reject wall footholds, false support and unintended second jumps.
- [ ] Reproduce the lower-standing hero's active stair encounter. Distinguish reach mismatch, recovery/input suppression and repeated stagger. Verify an actual counter or escape on the reported terrain, not only an isolated step.
- [ ] Finish ladder transfers and jump/hurt/death/pause combinations, leafy tops, vine visual/slow-frame behavior, disappearing-platform phases and moving/crumbling supports.
- [ ] Check checkpoint death/reload with held inputs and different nearby terrain. The existing checkpoint-1 walking result remains a bounded pass.
- [ ] Cover active attacks with both facings, above/below offsets, standing/crouching/ascent/descent, projectiles, simultaneous contacts and interrupted/dead attackers.

Task IDs: MOVE-01–09, COMBAT-01/02/03/09. Exit: no reproducible blocking collision, false jump support or unhandled combat defect; each reported regression has a scoped fix/result and human recheck where specified.

## 3. Complete encounters and original-behavior decisions

- [ ] Recheck normal boss entry, phases, damage acceptance, death/restart/re-entry and required objects/projectiles, including Le Rauxe, Gabriel, Red Tail, Aquatis and Omar.
- [ ] Verify final victory, score, replay/skip/exit and persistence. Describe the staged ending accurately; original movie playback is not established.
- [ ] Resolve or explicitly document the remaining Crab, Fish, Tiger Guard and other enemy/boss policy differences using versioned evidence. Do not replace unknown timing with arbitrary global speed/health changes.
- [ ] Where feasible, record matching original runtime behavior for recovery, ladders, ledges and boss timing. The supplied modified executable is not original source code or certified pristine media.
- [ ] For every remaining P1 research item, record its player impact and a justified fix, accepted documented difference or explicit deferral. Do not silently turn an unknown into a parity claim.

Task IDs: COMBAT-05–10, BOSS-01–07, ORIGINAL-02. Exit: no encounter softlock or unreachable required victory, and no unresolved research item hidden by a blanket compatibility claim.

## 4. Finish touch, menus and languages

- [ ] Verify short/held/repeated jump input, Catnip and slow frames; simultaneous stick/jump/attack/fire; release outside controls, cancellation and finger crossing.
- [ ] Check layouts and HUD on small/wide displays, both languages, safe areas and persisted bindings/layout.
- [ ] Check every visible PL/EN menu route, pause, score and Game Over, including foreground/background touch targets and return/cancel. Keep unsupported entries removed.
- [ ] Audit all app-owned messages, import errors, help and long labels. Explain that English UI does not translate Polish recordings.
- [ ] Recheck the specific reported physical-controller pause issue if a controller is available within scope. Broad model/transport testing stays deferred.

Task IDs: INPUT-01–04, UI-01/03, LANG-01. English recorded voices require a lawful supplied English edition; do not bundle an unlicensed language pack (LANG-02).

## 5. Prove installation and save safety

- [ ] Have a novice follow the English guide, and check applicable Polish instructions, on a clean setup using owned game data.
- [ ] Exercise actual large-file DocumentsUI selection and relevant providers, plus real save export/import and restoration of progress.
- [ ] Recheck corrupt/cancelled/interrupted/low-space imports on the release candidate. A previous valid installation must remain usable; clean temporary staging safely.
- [ ] Verify a correctly signed in-place upgrade retaining game data, saves, language, bindings and layout. Seed or observe real existing preferences; an empty preference directory is not coverage.
- [ ] Check background/resume, screen lock, process death, resource recreation and repeated level reloads without stale input, duplicate callbacks or retained actors.

Task IDs: INSTALL-01–05, LIFE-01/02. Exit: clear installation instructions and tested recovery/update paths without user-data loss; isolated transaction tests are not the whole picker workflow.

## 6. Validate the declared Android support and stability

- [ ] Freeze one candidate before final measurements. On Huawei, observe warm-device stability, dense combat, repeated transitions, memory and p95/p99/worst stalls on that exact APK.
- [ ] Recheck minimum/newer Android and relevant storage/focus/display behavior. Obtain fresh allocation before any Redmi use; keep Huawei tethering unchanged.
- [ ] Verify ARMv7 runtime when suitable hardware is available and distinguish it from compilation or ARMv7 selection on a 64-bit phone.
- [ ] Check final native/ZIP alignment; physical 16 KB ARM behavior remains unverified until appropriate hardware is tested. Publish the exact matrix and missing coverage.
- [ ] Investigate long-frame jump behavior where reproducible; do not infer a phone defect from emulator behavior alone.

Task IDs: PERF-01–04, ANDROID-02–04. **55/60 FPS are desired targets, not mandatory release floors** under the user's November 8 decision. Retain image quality, physics and AI; report measured limits honestly. Missing hardware coverage must be explicitly scoped, not advertised as universal Android support.

## 7. Human campaign acceptance

- [ ] The human tester completes the fourteen CAMP rows in [TODO](../TODO.md), using a continuous normal-resource route and recording APK/data edition, checkpoints, deaths/reloads, exits and defects.
- [ ] Engineering reproduces and repairs reported blockers, then requests only the affected replay/recheck rather than claiming campaign completion from teleports or protected fixtures.
- [ ] Confirm normal boss resources, level-14 completion and complete ending flow (CAMP-15).

The agent must not take over autonomous campaign traversal. Broad physical controller testing is also outside the current scope.

## 8. Produce the release only after acceptance

- [ ] Match documentation, known limitations, TODO, tested matrix and novice instructions to the frozen candidate. Keep GitHub-facing material in English, anonymous human participation and explicit LLM adaptation disclosure.
- [ ] Build from the recorded source/upstream revisions and verify patches, dependency notices, licenses and public history. Exclude commercial assets, proprietary executable/dumps, saves, device identifiers, private reports and signing secrets.
- [ ] Prepare the signed production APK with matching source commit/tag and SHA-256. Verify signing identity and upgrade behavior; runtime-test the actual production identity or explicitly resolve the outstanding identity gap.
- [ ] Run candidate-specific regressions and record failures as well as passes. Repeat affected checks after fixes; do not transfer debug42 or isolated-package results to a different artifact automatically.
- [ ] Publish 1.0 notes only when crashes, progression softlocks, save-loss defects, required acceptance checks and human campaign results are resolved. List intentional differences and declared compatibility limits.

Task IDs: DOC-01/02, LEGAL-01/02, RELEASE-01–04. Until then, label downloads development/test releases.
