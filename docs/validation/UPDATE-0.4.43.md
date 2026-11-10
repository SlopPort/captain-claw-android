# Debug 0.4.43: configured enemy hurt voices

OpenAI Codex (LLM), 2026-11-10. Huawei P9 Lite, LineageOS Android 10, ARM64 runtime, supplied Polish game data. This is development evidence, not release 1.0, a campaign clear or original-runtime parity.

## Exact artifact and correction

Debug APK versionCode **55**, versionName **0.4.43-dev**, SHA-256 `dfedd91134113cacf5f43dbdbe17e6575b0848a43710922eeaea86d777e35b8a`. ARM64 and ARMv7 were built; this runtime batch exercised ARM64 only. Public signed downloads remain [0.4.41-test](RELEASE-0.4.41.md).

The ordinary hurt state now plays its existing configured voice once on entry. Empty lists stay silent. The common impact sound is still emitted by the normal health-change path, so the added path filters the generic impact names and the old missing `LEVEL1/SOUNDS/HIT1.WAV` placeholder. It does not alter damage, recovery, attack cadence, invulnerability or the fatal-hit branch. Red Tail's configured hurt reference now includes its existing `REDTAIL` subdirectory; no new game recording is bundled.

[Static investigation](HURT-AUDIO-FOLLOWUP.md) distinguishes actual voices, generic placeholders and animation events. The initial unrestricted voice-list build was superseded before installation after the missing-placeholder issue was found. The revised build completed successfully. Private build logs: `todo-debug43-build.log`, `todo-debug43-build-r2.log`.

## Baseline and corrected runtime

The preserved debug42 runtime was tested before upgrading. Its SHA-256 was `2af60b03c18d393bb632080507c90f7d3ac8ccd90c0f3bb91f61367ab66f29ad`. Actual crouched sword contact reduced a passive Soldier from 10 to 5 HP, but only the sword and generic impact requests appeared: the configured hurt voice was absent. A second 5-to-0 contact produced its configured death sound. An active Soldier produced real hero damage and the hero hurt voice. This baseline explicitly expected the missing enemy voice; it is evidence of the old defect, not fixed-game acceptance.

After the in-place update, the corrected exact APK passed:

| Case | Real contact/health evidence | Audio result |
| --- | --- | --- |
| Soldier hurt | Crouched sword, 10 to 5 HP | Configured `00320005.WAV` accepted once; nonzero mixed output |
| Soldier death | Second crouched sword, 5 to 0 HP | Configured `00320006.WAV` accepted once; nonzero mixed output |
| Officer generic impact | Crouched sword, 10 to 5 HP | One generic impact accepted; no missing legacy placeholder request |
| Hero hurt | Active Soldier, first observed 100 to 95 HP | Expected hero hurt voice accepted; nonzero mixed output |

Each fixture restored fresh configuration/progress and found no target or unattributed fatal crash. The passive targets isolate outgoing sound behavior, not active combat fairness. The mixer observes the combined output, not an isolated recording of each voice; human listening and hero-death audio remain untested by this helper. The baseline preceded the additional Officer assertion; the fixed runtime executed all four cases.

Private evidence: `todo-hurt-audio-baseline-0.4.42-20261110/results.json`, `todo-hurt-audio-fixed-0.4.43-20261110/results.json`.

## Upgrade and static verification

The debug42-to-debug43 upgrade passed without uninstalling and preserved the seven checked external game/configuration/progress files. No private preference XML existed in the snapshot, so existing private preference preservation is not established. Report: `todo-upgrade-0.4.43-20261110/results.json`.

Known-pattern APK privacy checks passed for 375 members. Both-ABI packaging/ELF checks passed; ARM64 load alignment is 16 KB. Exported patches match the prepared upstream worktrees. These are not physical 16 KB ARM, clean-machine build, all-Android or production-signature runtime certification.

The exact packaged audio inventory reports no missing referenced attack sound among its 75 action rows. Red Tail's revised hurt/death references exist in the supplied data and its hurt animation contains no duplicate sound event. This verifies the reference, **not** playback during the actual boss's accepted hurt branch. Two attack definitions have no configured sound; the audit does not invent replacements. Private report: `todo-audio-inventory-0.4.43-20261110/results.json`.

## Remaining acceptance

The exact installed APK additionally passed the sequential `touch-jump`, `game-over`, `ambient` and `save-errors` regressions. Each child restored configuration/progress and retained the installed hash. Private batch: `todo-audio-regression-0.4.43-20261110/results.json`. These scoped cases do not certify every menu, input method or Android version.

Complete subjective low/high-volume listening, other configured enemy families and custom boss paths, hero death, full cold/warm Catnip pickup stalls and the final signed-candidate matrix. The earlier debug42 20-minute protected observation remains debug42 evidence; it is not automatically transferred to this newer APK. AUDIO-01/02/03 and the wider release checklist remain open.
