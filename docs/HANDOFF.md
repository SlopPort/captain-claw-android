# Project handoff

Current state: **2026-11-08**. Adaptation code, documentation, investigation and automated tests were performed by OpenAI Codex (LLM), guided by anonymous human requirements and feedback. OpenClaw and dependency authorship remain separate.

The [detailed TODO](../TODO.md) tracks remaining work with stable task IDs and completion criteria. Read the [known limitations](KNOWN-LIMITATIONS.md) and [original-behavior ledger](ORIGINAL-BEHAVIOR-LEDGER.md) before changing balance or claiming parity.

## Current state and boundaries

- Main Huawei installation: **ARM64 debug 0.4.42-dev**. [Current diagnostic evidence and unresolved checks](validation/UPDATE-0.4.42.md). Public signed downloads remain 0.4.41-test; earlier results retain their exact version. Only Huawei is allocated to this task now. **Do not query, install on or otherwise operate Redmi without a new allocation.** Earlier Redmi results below are historical, not permission to use it now.
- Huawei supplies internet over USB. Do not reboot it, change USB/tethering/network settings, disconnect it or restart the shared ADB server to repair a test. Select the authorized device with a process-local `ANDROID_SERIAL`; never publish device serials.
- The human owns natural campaign playtesting. Do not resume autonomous traversal. Technical reproductions of reported bugs are allowed, but teleports, invulnerability and resource edits must be labelled as fixtures, never natural campaign evidence.
- This is not release 1.0. Full campaign completion, original-game parity and a universal FPS minimum are not established. Broad physical controller testing was deferred; later specific pause/input bug reports remain in scope.
- Public explanatory documentation is English. Keep Polish game UI supported, and preserve actual Polish UI text when quoted in instructions or evidence. Keep the human anonymous, disclose the LLM contribution and preserve upstream notices.

Start with [contributing](../CONTRIBUTING.en.md), [building](BUILDING.en.md), [installation](INSTALL-EN.md), [release gates](ROADMAP-1.0.md) and [upstream differences](UPSTREAM-DIFF.en.md).

Public development APK distribution resumed with [v0.4.41-test](https://github.com/SlopPort/captain-claw-android/releases/tag/v0.4.41-test). [Exact artifact, source, signer and limitations](validation/RELEASE-0.4.41.md). Older 0.4.31/0.4.32 releases remain private drafts after diagnostic filename disclosure; do not republish those binaries. Their files/metadata are retained privately and source/tags remain public. The [0.4.32 record](validation/RELEASE-0.4.32.md) is historical.
The phone's existing debug installation was not migrated or uninstalled.

## Latest verified behavior

The debug40 follow-up also passed clean-source ARM64/ARMv7 building from `f11b80f`, PL/EN menu/shared-sound regressions, short touch jumps, ambient mixing, focused Game Over/score paths, 10%/100% selected attack audio and virtual Start/Catnip-music transitions. Exact scope is in the report below. Its valid 120-second heavy level-9 observation ranged from **48.0 to 59.6 FPS** across 300-loop batches and **failed the 55 FPS floor**. Do not describe the performance target as achieved. Broader TODO items remain open where these fixtures cover only part of acceptance.

[Debug 0.4.40](validation/UPDATE-0.4.40.md) verifies Tiger front-flip continuation, actual Siren interruption/death, localized save-failure messages and working gameplay options. Recorder identity follows the APK version. The debug39 sustained result was invalidated after backgrounding/missing coverage; do not quote it as a performance pass. Remaining original-policy details are in the [follow-up](validation/ORIGINAL-FOLLOWUP-2026-11-08.md).


[Debug 0.4.39](validation/UPDATE-0.4.39.md) fixes local ambient double attenuation and muted entry, adds p99/skipped-gap evidence and a sequential restoration-verifying regression runner. Exact candidate checks are versioned; do not treat an in-progress batch as complete. Public signed distribution remains 0.4.32-test.


[Debug 0.4.38](validation/UPDATE-0.4.38.md) reconstructs Siren bursts, Crab active windows, Fish target-crossing lunges, Tiger Guard moves, Gabriel command phases and Red Tail shared timing. Le Rauxe now uses the recovered cached 100/1001 ordinary melee block predicate. The exact installed r9 APK passed the six main Huawei fixture groups. The report records intermediate failures, source-only newline cleanup and remaining original-AI/collision boundaries. Public signed distribution remains 0.4.32-test; this is not 1.0 or a natural campaign clear.

[Debug 0.4.37](validation/UPDATE-0.4.37.md) corrects 28 effective emission-frame configurations, makes Red Tail's configured delay effective, and fixes deferred first-frame attacks. Final Huawei tests passed ten ordinary cases, three synthetic first-frame delays and two real boss arenas. [Original custom-handler findings](validation/ORIGINAL-CUSTOM-EVENTS-0.4.37.md) identify the remaining full-AI/window work. Public signed distribution remains 0.4.32-test.

[Enemy attack-speed audit](validation/ENEMY-ATTACK-AUDIT-2026-10-30.md): 55 packaged enemy/encounter prototypes and 76 attacks inventoried, 15 ordinary Huawei cadence cases plus one ranged case measured. Original ANI event mapping is traced: 26 configured actions differ from event-1 markers, 40 match and ten need custom handlers. Red Tail has an ignored nested delay; frame-zero first-hit behavior and unused Gabriel action metadata need follow-up. Exact original timing for every family remains unresolved. This source/documentation batch changes no APK or balance.

Current build/test summary: [debug and signed isolated 0.4.41 checks](validation/UPDATE-0.4.41.md). The signed production APK is a public development prerelease, with its exact identity runtime limitation disclosed. API 35 menu instrumentation passed English and Polish repeats after two failures; its intermittent failure remains unexplained. [Debug40](validation/UPDATE-0.4.40.md) and [debug36](validation/UPDATE-0.4.36.md) remain historical evidence.


After reviewing commit 425cdb1 (touch customization and working three-preset difficulty), debug36 removes six unsupported menu actions and compacts the main/single-player/options lists. Controls and Difficulty remain functional port features. [Menu audit](validation/MENU-AUDIT-2026-10-30.md) records physical PL/EN navigation and translation coverage.

The forest update addresses leafy-ladder cap geometry and interpolates rope carrying with a rope-specific clock; [forest evidence](validation/FOREST-MOTION-2026-10-30.md) preserves caught intermediate failures and validation scope. [Le Rauxe investigation](validation/LERAUX-ORIGINAL-2026-10-30.md) distinguishes original pause-branch evidence from debug36's boss-only 300–600 ms cadence approximation. The ordinary melee block predicate was subsequently recovered in debug38; full encounter parity remains unresolved. Public signed distribution remains 0.4.32-test; debug36 is not a public signed release.


Debug35 adds an automatic, bounded local [background gameplay recorder](BACKGROUND-DEBUGGING.md). It retains movement/action/contact history and candidate wall-push reports without enabling combat fixtures. [Physical evidence and limits](validation/FLIGHT-RECORDER-0.4.35.md) distinguish candidate detection from a proved bug. The level 2 blockage remains open. Public signed distribution remains 0.4.32-test.


The level 2 small-platform leftward blockage remains OPEN. The private recording was matched to the crate near (2460,4956), but 17 walking/entry/depth fixture attempts on debug33 did not reproduce the frozen movement. Debug34 adds read-only live collision capture without enabling combat diagnostics, so the next occurrence can be inspected before restart. See [attempts and capture instructions](validation/LEVEL2-PLATFORM-0.4.34.md). Do not label this as fixed.


Android33 fixes double attenuation of sound effects: the master slider was applied both to each chunk and its mixer channel. At the user's 10% setting this reduced ordinary effects to roughly 1% amplitude. The Android path now applies master gain only to channels. [Audio evidence](validation/AUDIO-GAIN-0.4.33.md) records the measured fixtures. Public signed distribution remains 0.4.32-test until a separately verified release artifact is published.


Host packaging now publishes a CRC-checked ZIP through a same-filesystem temporary file and atomic replacement. Eight failure/input check groups and a real local repack passed; the original installation remained byte-identical. Full REZ plus loose Assets is rejected because this tool does not merge partial overrides. See [host packaging evidence](validation/HOST-PACKAGING-2026-10-24.md). This batch changed no APK and used no phone. The clean-computer GUI trial remains open.


Android32 corrects floor-join snagging, rejects wall-only grounding and restores
Catnip's double-damage bonus. See [exact reproduction/fixtures](validation/EDGE-SUPPORT-0.4.32.md)
and [REA follow-up](ORIGINAL-BEHAVIOR-REA-2.md). Human rechecks of both recorded
locations remain necessary; no complete natural campaign clear is claimed.


The 0.4.31 changes separate the Game Over title from its touch instruction. The Huawei last-life/touch return test passed. Native builds for ARM64 and ARMv7 passed; this is build coverage, not physical runtime coverage for every architecture. See [Game Over UI evidence](GAME-OVER-UI.md).

The flat player foot in 0.4.30 passed the controlled ledge/crouch cases and full ladder matrix on Huawei. Melee recovery checks passed on 0.4.31. Static REA findings distinguish hurt-state attack suppression from attacks after recovery; the port's 400 ms melee buffer remains an intentional accommodation, not verified original behavior. Read [original-behavior evidence and limitations](ORIGINAL-BEHAVIOR-REA.md) before making collision or balance changes. Do not treat decompiled executable output as original source or publish proprietary code dumps.

Versioned reports keep their exact-build scope. Prior compatibility results do not automatically certify 0.4.32. Game audio language still depends on the player's own data; see [language research](GAME-LANGUAGE.md).

## Historical evidence, not current allocation

- **0.4.29:** [Huawei regressions](validation/USER-REGRESSIONS-0.4.29.md) and [Redmi follow-up/cleanup](validation/REDMI-0.4.29.md) passed. Redmi was explicitly allocated for that batch, then its test companion was removed. Reinstall it only if a future authorized test needs it. The main apps retained debug signing.
- **0.4.27:** [lifecycle/import/compatibility checks](validation/READINESS-0.4.27.md), [isolated signed ARM64/ARMv7 checks](validation/RELEASE-0.4.27.md) and the [45-variant active audit](validation/ACTIVE-NORMAL-0.4.26.md). Isolated releasecheck apps were removed; production-key candidates did not replace the main debug installations.
- **0.4.26:** [import/picker checks](validation/IMPORT-FLOW-0.4.26.md) and [signed candidate evidence](validation/RELEASE-0.4.26.md).
- **0.4.25:** [readiness and retained failures](validation/READINESS-0.4.25.md), [Redmi Android 16 results](validation/REDMI-0.4.25.md), [twenty-minute Huawei observation](validation/SUSTAINED-HUAWEI-0.4.25.md) and [bounded full-disk tests](validation/IMPORT-FULL-DISK.md).

The desired performance target is 55 FPS in the measured heavy Huawei scene, with 60 FPS desirable. On 2026-11-08 the human allowed accepting lower FPS if sensible measurement-led optimizations do not help; 55 FPS is no longer a mandatory release floor. Neither target is a proved minimum for every frame or level. Preserve image quality and report stalls separately.

## Historical natural route and test ownership

The last autonomous continuation, before the human took over, used Huawei P9 Lite / Android 10 / 2 GB RAM and an unchanged checkpoint written by the earlier Redmi run: level 1, checkpoint 1, HP100, zero spare lives, pistol6, magic2, dynamite3. It passed carriers, ladder transfers, the upper shaft, the Soldier encounter, the next flag ledge and the first two cyclic pegs. A later group remained uncleared; missed jumps reached the lower floor, where normal combat/pickups left HP85. This was partial route coverage, not a level exit or a new persistent checkpoint. [Evidence and failures](validation/HUAWEI-CAMPAIGN-0.4.24.md).

[Six subsequent retries](validation/CAMPAIGN-RETRIES-0.4.24.md) did not extend the natural route. Do not blindly replay those commands after knockback or a missed landing. The experimental first-carrier helper has no device pass. Those test owners ended, and user configuration/save files were restored byte for byte. The lower-floor runtime position was not a new save. Further natural route work belongs to the human.

A fresh clone has no ignored private reports or user saves. Reproduce a technical scenario or use your own legitimately obtained save and document its origin. Never assume local reports are available to other contributors.

`campaign_play.py` owns test backups and an app-local command mailbox. `campaign_session.py` reconnects a dead logcat reader from its last recorded timestamp; that recovery was tested on Huawei without restarting the game or ADB. `campaign_log_reader.py` can supervise an older live owner; its stop marker ends only that reader. Timestamp overlap can duplicate a line, so consume each observation tick once. Missing samples or a reader timeout do not by themselves prove a gameplay bug.

## Publication and signing

Use this project's repository and task-local Git identity. Do not change another project's credentials, global identity or remote. Review [publication checks](PUBLISHING.md). Keep commercial data, raw reports, user saves, device identifiers, signing keys and passwords private. Preserve `private-signing/` locally; never upload it. Debug and release identities differ, so follow the [signing/migration guide](RELEASE-SIGNING.md) instead of uninstalling a user's game to bypass an update failure.

Remaining release gates are in the roadmap. Clearly distinguish current verified facts, historical results, intentional differences and unknowns. Do not call this original Monolith source or assume game copyrights have expired.
