# First ladder, cap jumps and flat edge regression

2026-11-08. Automated testing and analysis by OpenAI Codex (LLM), guided by anonymous human reports.

Huawei P9 Lite / LineageOS Android 10, main ARM64 debug41 APK SHA-256:
`4bcf15bade79c4047cd6b387b02ae5b0c35b7596f19528f167041a5416d8f187`.

## Scope and results

The full existing ladder fixture completed with `fixed_checks_passed: true` and 990 trace samples. Raw evidence remains private in `reports/todo-ladder-edges-0.4.41-full`. No target or unattributed fatal error was found. After completion, a separate device-side SHA-256 comparison confirmed that both configuration and progress matched this test's **fresh** backups. This is not private preference preservation evidence.

| Area | Executed scope | Result |
| --- | --- | --- |
| First real level-1 ladder cap | Held Up, release, Up again, descent and ladder jump | Top held a standing animation without climbing; descent and jump detached appropriately |
| Short cap inputs | Up/Down at horizontal offsets -28/-16/0/16/28 px | Recorded endpoint and time-series observations; not a separate original-policy equivalence assertion |
| Lateral input after descent | 60/100/180 ms Down then left/right | Claw stayed attached below the summit; record as a policy question rather than declaring a terrain snag |
| Cap and just-below-cap jumps | 100/250 ms jump holds, no lateral input / delayed left / delayed right; 12 cases | Every trace contained actual `jumping=1`; all endpoints returned to grounded standing on the cap |
| Stationary falling animation | Full captured jump traces | No detected grounded, stationary falling-animation streak lasting at least 300 ms; shorter transitions are not ruled out |
| Walk off cap / Up plus jump | Actual cap | Walk-off lost support; Up plus jump rose without remaining in climbing state |
| Ladder bottom | Isolated ladder ending at a solid floor | Held Down ended climbing on the floor; release stood; Up re-entered climbing. Feet did not penetrate below the asserted floor tolerance |
| Platform edge loss | Isolated left and right edges | Ground support cleared on walking off, downward velocity appeared and landing occurred on the lower floor |
| Air-jump rejection | Jump request after each edge departure | Recorded jump rise remained below 2 px and jump count stayed zero |
| Idle edge support | Both sides; center 20/5/1 px inside and 1/5/15 px outside the nominal edge | All observed endpoints remained supported with unchanged horizontal position; mandatory inside-edge stability assertions passed |

Fixtures use teleports, an isolated ladder/platform and protection to avoid unrelated enemy deaths. They are not natural traversal, death/hurt tests or a 55/60 FPS measurement. Lateral inputs are app-local diagnostic keys, not a physical-controller test. The outside-center observations do not establish pixel-perfect original support geometry or how far beyond these offsets support must end.

## Reproduce and remaining work

Select only an allocated device:

```text
python tools/ladder_smoke.py --report unique-report-name --expect-fixed --first-map-ladder --bottom --edges --idle-edges --seam-audit --seam-exits --seam-jumps
```

MOVE-02/03 remain broader than this fixture: both user-recorded natural snag locations, crouching/reversal, real tile joins and false wall footholds retain their own checks. MOVE-04 still includes leafy level-3 ladders. MOVE-05 still needs interruption by hurt/death and pause/restoration while attached. MOVE-01's unreproduced level-2 blockage remains open. Do not generalize this pass to all geometry or original-game parity.

## Additional leafy-ladder, rope and pause checks

The same exact Huawei debug41 subsequently passed:

- **Leafy ladder caps:** production level-3 tile types 668 and 667. A 20 ms Up pulse near each calibrated summit followed by release ended grounded and not climbing (feet at 6339/6014, within the asserted surface tolerance). Down re-entry remained attached and moved below the cap. Pausing input mid-ladder left Claw attached without a phantom ground contact. Teleport setup and removed enemies are explicit fixtures. These cases do not cover every jump/side-transfer/interruption combination.
- **First level-3 rope:** attachment occurred through its real trigger after diagnostic placements; 18 subsequent samples stayed attached. Maximum interpolated handle-position error was about **0.0066 px** against the configured offsets/phase. A game-thread trace confirmed a transient jump after release input; a later re-grab is permitted. This verifies sampled position alignment and release, **not visual smoothness or low-FPS animation**. Setup removed enemies and protected Claw.
- **Pause while attached:** new `ladder_pause_smoke.py` performed three app-local Escape pause/resume cycles on an isolated ladder. Each cycle confirmed menu/game context transitions, unchanged position, continued ladder attachment, no floor contact and zero vertical velocity. A subsequent Up pulse moved from Y=923.9 to Y=866.1. No target/unattributed crash was recorded. The test pauses while input is already neutral; held-input cancellation, hurt, death and process recreation are separate cases.

The forest/rope batch independently checked restored config/progress hashes and unchanged APK after each child. The pause helper used the shared session's byte-for-byte restoration check. No physical controller was attached by these helpers; no Bluetooth/USB transport claim is made.

Private raw evidence: `todo-forest-rope-0.4.41*` and `todo-ladder-pause-0.4.41`. Reproduce the additional cases on an allocated device with:

```text
python tools/run_regression_batch.py --report unique-report-name --cases forest rope ladder-pause
```

This reduces the missing scope above, but MOVE-04/05/06 remain open for the other combinations, interruption rules and visual/slow-frame assessment. Neither an attached rope clock nor a sampled handle match proves a smooth rendered animation.
