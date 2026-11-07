# Ambient audio and TODO follow-up: debug 0.4.39

2026-11-07. OpenAI Codex (LLM) performed implementation, documentation and automated technical testing, guided by anonymous human requirements. Upstream work remains separately credited. This is not release 1.0, a natural campaign clear, a physical controller matrix or original-runtime parity evidence.

## Artifact and actual change

Candidate **0.4.39-dev / versionCode 51**, both ARM64/ARMv7 built. Installed in place over the debug app on the allocated Huawei P9 Lite / LineageOS Android 10 / ARM64; no uninstall or Redmi operation.

- APK SHA-256: `aa8fa8d8d34d919631dd4249826ce381db68f6c9a218e0a636e7b7c5b797689c`.
- Support archive SHA-256: `853334b5119d5f199bd1f7bc88fead46068b7f6e360c4c54aa77325cb0d8bb44` (unchanged from debug38).
- Public signed distribution remains 0.4.32-test. Do not imply this candidate is already its replacement.

The targeted source-comment audit found that LocalAmbientSoundComponent still applied master volume to its cached chunk as well as its channel. The ordinary-effects path had already been fixed in debug33, but this separate path had not. Android local ambient chunks now contain intrinsic gain only. Live master changes act through channel gain. Entering a new ambient source while master sound is off now zeros the reserved channel before playback and pauses it, preventing newly created loops bypassing mute. Unmuting uses the existing central audio path. Non-Android behavior is preserved.

Per-300-loop performance logs now include p99 in addition to p95/max. Active intervals above 1000 ms, which the existing loop skips, are logged separately instead of silently disappearing from reports. This changes evidence collection, not simulation timing, jump physics or AI rate. Quantiles remain batch quantiles, not complete display-presentation telemetry.

## Verified mixer and touch results

The ambient fixture creates a temporary real sensor and production local-ambient component using a stock sound from user-owned data. It does not directly invoke audio gain logic or attach a microphone.

| Check | Exact-candidate result |
| --- | --- |
| Ambient master 10% then 100%, same running loop | Peaks 1823 and 19455; ratio 0.0937034, consistent with channel gain 12/128. Chunk gain remained 128, not master-scaled. |
| Mute an existing source and resume | Zero nonzero samples while muted; resumed peak 19455. |
| Enter a new source already muted | Zero nonzero samples; channel zero and paused. Unmuting resumed peak 1823. |
| Short/held touch jumps | Six cases passed; takeoff 20-23 ms after native receipt. Ten-millisecond tap rose 70.7 px, long holds reached 155 px; each recorded one jump. Queue delay was separately 6-19 ms. |
| Touch combinations and cancellation | Existing local-window fixture asserted simultaneous movement/jump, separate action inputs, drift rejection and released final controls. This is instrumentation delivery, not a human screen-sensor latency measurement. |
| Game Over and score | Existing local-window tests passed their real death/menu and score/next-level transitions. |

Private evidence: `todo-regression-0.4.39-a*`; additional results are recorded only after their owners finish and restoration is checked. Do not treat a running batch as a completed pass.

## Baseline regressions and retained failures

Before updating, the installed debug38 APK was identified by its exact [existing hash](UPDATE-0.4.38.md). Sixteen partial-edge/crouch cases passed. Floor joins in both directions at 1/2 px, normal/Catnip wall jumps, level 3 cap fixtures, after-hit Soldier melee recovery and attack sound mixer checks at 10%/100% passed on that debug38 artifact. These results are not relabelled as debug39 measurements.

The first batch failed to publish a nested floor-seam report even though its four physics assertions completed. The runner now supplies flat unique child report prefixes compatible with existing helpers. A fresh run passed; failed evidence is retained.

The old rope test rejected a late remote status that showed Claw attached again. Its replacement captures game-thread jump states around release and requires actual takeoff, while retaining final reattachment separately. It passed on unchanged debug38, establishing a measurement problem rather than justifying a speculative physics change. Visual smoothness is still not certified by this trace.

The new sequential runner records installed APK identity, checks byte-identical config/SAVES restoration and unchanged APK after each child, and stops on failure. It never silently repairs user saves. Its success means the selected fixture assertions passed, not that all TODO tasks are complete.

## Host evidence and boundaries

- Clean-source ARM64/ARMv7 build of committed baseline `040e258` passed from a Git archive, pinned local dependency objects and cached Gradle/installed SDK. No upstream working edits were copied. This is not a clean-machine bootstrap or byte-identical APK reproduction claim.
- Both current patches clean-apply and match 64 OpenClaw files plus one SDL file after CRLF normalization.
- Production import transaction checks: 64 interruption/commit/journal cases passed. TinyXML atomic save: 18 failure/child-death cases passed. Host packer: eight publication/input groups passed. These are host/bounded checks, not every Android picker or real-phone disk exhaustion.
- Candidate attack inventory: 55 concrete prototypes, 75 configured actions, zero missing ANI files. Support archive contains 211 XML/generated-PNG entries; four PNGs are the generated help/credits. No REZ/WWD/PID/FEC archive member was found in the APK. This is a content/provenance check, not a legal opinion on every dependency.
- Source history scan reported no private-pattern findings before this batch's commit. Publication checks must be repeated for the new commits.

The [known limitations](../KNOWN-LIMITATIONS.md), [behavior ledger](../ORIGINAL-BEHAVIOR-LEDGER.md) and [source-comment audit](SOURCE-COMMENTS-2026-11-07.md) distinguish completed work from remaining investigation. Level 2 blockage and natural diagonal-combat fairness remain open; broad controller testing remains deferred. English voice data is not supplied. All natural campaign testing remains with the human.
