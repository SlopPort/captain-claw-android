# Original-behavior comparison ledger

Updated 2026-11-07 by OpenAI Codex (LLM), guided by anonymous human requirements. This is an evidence index and scope ledger, not a claim of recovered original source or complete original-game parity.

## Reference and interpretation

Current static research used the supplied **CrazyHook-distributed CLAW.EXE**, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. It is not certified pristine 1997. Resource-event findings depend on the player's supplied data edition. No matched original Windows runtime timing series has been recorded. Do not infer runtime equivalence from static constants alone.

Classification:

- **Binary finding:** a bounded rule recovered from this supplied executable, independently implemented or documented; surrounding paths may remain unknown.
- **Port observation:** measured on a named Android artifact/fixture; not an original-game measurement.
- **Port choice:** deliberate or inherited adaptation with no original-parity claim.
- **Unknown:** missing original evidence or incomplete state/collision reconstruction.

Raw executable, disassembly, game assets, saves and recordings remain private. Public findings describe rules and boundaries without publishing proprietary dumps. Future comparisons must record the exact executable/data hashes privately and publish suitable nonpersonal provenance. A different edition needs its own comparison.

## Current ledger

| Behavior | Classification / established scope | Difference or unresolved boundary | Evidence / task |
| --- | --- | --- | --- |
| Hurt-state attack suppression | Binary finding; ordinary input rejection during hurt is distinct from post-recovery attacks | Complete overlap/immunity pipeline and natural stair fairness remain unknown | [REA investigation](ORIGINAL-BEHAVIOR-REA.md); COMBAT-01/02 |
| 400 ms melee tap buffer | Port choice; bounded recovery fixtures observe a queued tap execute | Not an original input-buffer constant or general immunity extension | [regressions](validation/USER-REGRESSIONS-0.4.29.md); COMBAT-01 |
| Flat foot and floor joins | Port choice with Android reproduction/regressions | Bevel dimensions/support tolerance are solver choices, not recovered Monolith geometry; level 2 snag remains open | [edge/support report](validation/EDGE-SUPPORT-0.4.32.md); MOVE-01/03 |
| Wall-only grounding rejection | Port choice fixing an Android support classification error | No claim that original engine used the same rays/tolerance | [REA follow-up](ORIGINAL-BEHAVIOR-REA-2.md); MOVE-02 |
| Ordinary/Catnip jump and short tap | Port observation and touch accommodation | Exact matched original jump traces, especially long-frame behavior, remain unknown | INPUT-01; PERF-04; ORIGINAL-02 |
| Catnip doubles ordinary melee damage | Binary finding; Android contact checks distinguish normal/bonus standing and crouching damage | Does not establish all powerup/weapon interactions | [REA follow-up](ORIGINAL-BEHAVIOR-REA-2.md); COMBAT-03 |
| Generic ANI effect frames | Resource/binary findings; 0.4.37 fixes effective configured frames and deferred frame zero | Generic frame metadata does not replace custom handlers or certify attack eligibility | [custom events](validation/ORIGINAL-CUSTOM-EVENTS-0.4.37.md); COMBAT-04/09 |
| Siren burst and gate | Binary findings implemented and measured on 0.4.38: up to four notes, 300 ms spacing, 4000 ms entry gate, sound-duration singing | Missing audio, interruptions/visibility and complete original custom-asset behavior remain unknown | [Siren](validation/SIREN-BEHAVIOR-0.4.38.md); COMBAT-08 |
| Crab active images | Binary finding: moving strike active at images 203/204; Android bounded window/contact evidence | Exact PID-derived rectangles and continuous re-hit behavior unresolved | [custom melee](validation/CUSTOM-MELEE-0.4.38.md); COMBAT-05 |
| Fish horizontal lunge | Binary findings: captured target X, 180 px/s, immediate window and image-202 cue; port re-entry measured | Swimming-home eligibility, JumpStrike and exact rectangles remain unknown | [custom melee](validation/CUSTOM-MELEE-0.4.38.md); COMBAT-06 |
| Tiger Guard moves | Binary findings: three move selection, 1250-2000 ms gate, knife chains, delayed lunge and front flip; all three observed | Home/obstacle graph, reaction flags, contact persistence and full parry/hurt behavior unknown | [custom melee](validation/CUSTOM-MELEE-0.4.38.md); COMBAT-07 |
| Le Rauxe ordinary block predicate | Binary finding: cached integer roll 0..1000, blocked values 0..99; Android ordinary-hit checks | Not a blanket rate for projectiles/already-parrying overlaps; full collision pipeline unknown | [boss report](validation/BOSS-BEHAVIOR-0.4.38.md); BOSS-02/03 |
| Le Rauxe 300-600 ms cadence | Port approximation informed by a bounded original pause branch | Applying this pause to every strike is not full recovered original control flow | [original investigation](validation/LERAUX-ORIGINAL-2026-10-30.md); BOSS-02 |
| Gabriel command phases | Binary findings: concurrent gate, bomb/cannon prelude/effect and summon completion; actual arena actions observed | Pirate weak-reference/health lifecycle is a port adaptation; original counters, signal retention and interruptions remain unknown | [boss report](validation/BOSS-BEHAVIOR-0.4.38.md); BOSS-04 |
| Red Tail shared decision gate | Binary finding: 1000-1500 ms shared gate and no old port pre-animation pauses; both arena phases observed | Complete eligibility graph, kick geometry/lifetime and hit acceptance unknown | [boss report](validation/BOSS-BEHAVIOR-0.4.38.md); BOSS-05 |
| Aquatis/Marrow/Omar encounter additions | Port implementation and controlled encounter observations | Full original phase/resource fairness and natural wins not established | [upstream differences](UPSTREAM-DIFF.en.md); BOSS-01/06 |
| Finale | Port choice: staged engine sequence | Not original movie playback or an identical presentation | [limitations](KNOWN-LIMITATIONS.md); BOSS-07 |

## How to extend or resolve an entry

Record the question, exact reference version, eligible initial state, inputs and trace. Separate selection delay, animation wind-up, active window, emission, recovery and next eligibility. Measure original and port under comparable conditions; explicitly report slow frames, protection, teleports or disabled AI. Add positive and negative cases for changed rules. Keep the old finding when a later result narrows it.

An intentional difference may be accepted with stated player impact; an unknown must remain unknown until evidence resolves it. Original parity research does not excuse crashes, save loss or progression softlocks. Natural route acceptance remains the human's task.
