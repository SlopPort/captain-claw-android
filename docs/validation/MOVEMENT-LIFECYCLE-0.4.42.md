# Movement and lifecycle follow-up: debug42

OpenAI Codex (LLM), 2026-11-08. Huawei P9 Lite, LineageOS Android 10, ARM64; exact debug APK SHA-256 `2af60b03c18d393bb632080507c90f7d3ac8ccd90c0f3bb91f61367ab66f29ad`. [Build and diagnostic scope](UPDATE-0.4.42.md). These are controlled fixtures, not human campaign acceptance or physical controller testing.

## Movement observations

The sequential runner passed the following cases and checked fresh configuration/progress restoration and installed APK identity after each:

| Case | Observed scope | Still not established |
| --- | --- | --- |
| Forest | Both actual level-3 leafy cap types: short Up/release stands at the cap, Down re-enters, middle remains attached without false floor | Every transfer, interruption and natural route |
| Ladder pause | Three neutral-input pause/resume cycles retain position and attachment; fresh Up climbs | Hurt/death and physical input |
| Rope | Attached position/handle alignment and release/re-attachment assertions | Human visual smoothness, low-FPS presentation and original swing parity |
| Checkpoint respawn | Actual checkpoint save, process/menu reload, ordinary death from an active Soldier, respawn, then right/left/right walking without jumping | Every checkpoint, held-input respawn and the unreproduced natural platform snags |
| Cyclic platforms | Both selected level-1 upward transfers landed with ordinary jump, no Catnip; measured rise 155 px each | Disappearance underfoot/return, every phase and the complete human route |

The cyclic-platform case also completed its short continuous foreground observation with no explicit skipped gap. This is neither a 20-minute stability result nor an all-level FPS claim. It establishes that those two selected transfers do not require Catnip in this port, not that the human's difficult jump was necessarily an input mistake.

Private evidence: `todo-movement-lifecycle-0.4.42/results.json` and corresponding child report directories. MOVE-01 through MOVE-09 retain their broader acceptance conditions in [TODO](../../TODO.md).

## Lifecycle and data safety

The same eight-case batch also passed:

- Own-app focus transition with held virtual axis: after resume the observed horizontal drift was **0.0 px**; a fresh press moved **191.36 px**. This is an app-local virtual input test, not Bluetooth reconnection, screen-lock or arbitrary OS process recreation coverage.
- Import publication/recovery process deaths for empty, partial and full isolated fixture sets. Each set rolled back, retained its save sentinel and reclaimed abandoned staging. These deliberately killed processes are expected test events, not accidental native crashes. Real game assets were not replaced. Low-storage/power-loss and real DocumentsUI providers remain separate.
- Delayed save export after its Activity lifetime changed: the exact expected export completed without the previously targeted `BadTokenException`; game config/progress were unchanged and temporary provider files were removed. The real picker was not exercised.

All eight children exited successfully, restored or preserved fresh configuration/progress and retained the same installed APK hash. This narrows INSTALL-03/05 and LIFE-01; it does not close their broader final acceptance criteria.

## Held climbing input released during pause

`tools/ladder_held_pause_smoke.py` extends the earlier neutral-input case with app-local virtual D-pad Up and Down. Each direction gets a fresh process/isolated production ladder. After climbing begins, Escape pauses, the held direction is released in the pause menu, and Escape resumes. Five position samples must remain attached, non-grounded, motionless and stable; a fresh Up press must then climb again. The driver also verifies that the original held input actually moved in its requested direction, preventing an unmapped button from passing as a release fix.

Both directions passed: Up moved from Y868.8 to Y788.9 before the resumed baseline; Down from Y868.4 to Y1028.1. Subsequent sampled drift was **0.0 px** in each direction. Fresh presses climbed, no target/unattributed fatal crash was recorded, and fresh configuration/progress were restored. The additional direction criterion was independently checked against these saved measurements after the runtime trial. Evidence: `todo-held-pause-audio-0.4.42-r2-ladder-held-pause/results.json`.

The final helper, including that direction assertion, also passed a fresh two-direction runtime repeat in `todo-held-pause-stability-0.4.42-ladder-held-pause`. The runner verified user-file restoration and unchanged APK before proceeding to its separate long observation; this ladder result alone makes no long-observation claim.

The initial attempt stopped because `ladderstatus` is deliberately rejected by the diagnostic mailbox while paused. This was a harness limitation, not an engine crash or blocked climbing bug; its runner verified restoration. The corrected helper respects that guard, releases through allowed virtual input and takes its baseline only after resume. Thus it does not measure exact paused coordinates or prove physical Bluetooth/touch delivery. Earlier failure retained in `todo-held-pause-audio-0.4.42`. Hurt/death on the ladder and other MOVE-05 branches remain open.

## Selected audio and pause/bonus checks

The follow-up runner `todo-held-pause-audio-0.4.42-r2` also passed selected audio at effects volume **10% and 100%**: idle output was zero; hero crouched sword, pistol, level-1 Officer and level-13/14 Chameleon cases requested their expected resources and produced nonzero SDL post-mix output. Music was muted during these fixtures; selected enemies were staged and protected hero setup was used. This is a signal/resource check, not a human listening judgment, isolated attribution of every mixed sample, or a complete hurt/death sound inventory. Different runs are not a calibrated loudness comparison.

Three app-local raw-Start pause/resume cycles passed. Console-applied Catnip acquisition, expiry and reacquisition switched prepared music in **1, 1 and 2 ms**, with PCM observed and no MIDI preparation during the measured sequence. This does not measure full real-pickup cold-frame latency or prove Bluetooth transport. Both audio runs and the bonus run restored fresh user configuration/progress and retained the installed APK hash. AUDIO-01/02 and physical INPUT-04 acceptance therefore remain broader than these results.
