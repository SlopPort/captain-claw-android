# 0.4.41 verification and remaining release work

2026-11-08. Work and automated checks by OpenAI Codex (LLM), guided by an anonymous human. This is a development build, not a finished 1.0 release. Natural campaign playtesting remains with the human.

## Exact build identities

All hashes are SHA-256. Build inputs were archived at source commit `cf93e5c4d2a4c1b6ee82da4e3e0d1467a357d7e3`; subsequent test/tool/document changes are not automatically covered by these results.

| Artifact | Hash | Evidence scope |
| --- | --- | --- |
| Huawei debug, code 53 | `4bcf15bade79c4047cd6b387b02ae5b0c35b7596f19528f167041a5416d8f187` | Installed in place; ARM64 runtime checks |
| Signed production, both ARM ABIs | `11c32c781ff183a4bc8846cfbfb6321f0e9700c7ae92752631144136449724cd` | Static checks only; not published or installed under production identity |
| Signed isolated releasecheck, both ARM ABIs | `374ba9e26831b89670466fce66b22aa5668a4c54c89d48251288ae27dcaf4afa` | Both ABI selections tested on Huawei |
| Archived-source ARM debug | `ae22d6db5ba54aaa9da1fe6d25fab668e52a196fc9e43ec692517e50ec3f7f9f` | Fresh sources/native objects; installed toolchain/cached Gradle |
| Archived-source x86_64 debug | `b12a35d443e9336b3ec417acc0d6bb82873be7520c81947bb82e4bdb54242e75` | Emulator results below |

All five passed the known-pattern APK privacy scan. Production passed signature, native ABI/alignment and 16 KB ZIP alignment checks. All six native libraries are byte-identical between universal production and releasecheck APKs. This is payload evidence, not a runtime test of the exact production identity. See [privacy investigation](BUILD-PRIVACY-2026-11-08.md) for withdrawn downloads and scan limitations.

## Completed bounded checks

- Huawei debug40 to debug41 installation preserved seven existing external game/configuration/progress files immediately after installation. No uninstall or stale backup restore occurred. **The report contains no private preference XML files; preservation of existing private preference values is not established.** The helper now reports preference coverage explicitly; the revised helper has not been rerun.
- Exact Huawei debug41 passed menu, short-touch jump, game-over, save-error and ambient-audio regression cases. Each child restored configuration/progress and verified the installed APK stayed unchanged. This does not prove every game-over choice, combat sound or campaign route.
- Signed isolated releasecheck passed menu, level 1/14 startup, positive gameplay music PCM, a 100 ms jump and a staged level-exit/progress-write fixture with each ARM ABI selected. ARMv7 on a 64-bit phone is not a physical 32-bit-only phone test. The disposable package was removed; the main game's checked files stayed unchanged.
- An older signed releasecheck code 44 upgraded to code 53 with six seeded external files unchanged before new-version launch. Subsequent runtime cases passed. This used a separate identity and did not test private preferences or replace the user's main installation.
- API 21 x86_64 passed menu, touch-jump, save-error and lifecycle cases with the exact archived-source APK above.
- Archived-source builds used locked upstream revisions and committed patches without copying upstream worktree modifications. Existing JDK/SDK and cached Gradle were required; this is neither a clean-machine bootstrap nor a byte-identical-build claim.

## Unresolved Android 15 test

On the API 35 emulator with 16 KB pages, the first debug41 menu run failed after returning from settings because the game lacked focus. Adding a bounded focus wait did **not** establish a passing run: the next run failed earlier at editor slider persistence. Configuration/progress restoration and unchanged APK checks passed in both failed runs. Later cases were not run after the menu failure.

Additional test diagnostics check slider layout and include actual size/X/Y values in assertion errors. The test APK built successfully. A subsequent English run passed all menu assertions, including editor persistence, audio sliders and disabled independent voice/ambient controls (318 localized image states; no target/unattributed crash). Configuration/progress were restored. This bounded passing repeat does **not** explain the two earlier failures or prove the intermittent problem fixed. Polish and remaining short cases are still pending. Retain the failed reports and inspect fresh diagnostics if the failure recurs.

## Remaining work and performance scope

The signed production APK has not been published. Old 0.4.31/0.4.32 downloads remain withdrawn to private drafts for diagnostic filename privacy. Resolve or clearly scope the Android 15 failure, finish documentation/checks, then publish only the scanned new signed artifact with matching checksums and accurate limitations.

The 20-minute stationary level-9 heavy-scene test belongs to **debug40**, not debug41: 47.0–60.2 FPS, batch median 53.2, longest reported loop 35 ms. Continuous foreground/batch coverage passed. The user made 55/60 FPS optional; preserve image quality, physics and AI rather than pursuing the target indefinitely. This is not an all-level performance guarantee.

Natural campaign completion, reported geometry/combat issues and wider original-engine parity tasks retain their own TODO requirements. Broad physical controller tests remain deferred. Only Huawei is allocated; Redmi needs a new allocation. A post-runtime phone preference/hash check and launcher reopening were not executed because automatic approval review could not complete at the usage limit; do not claim those actions succeeded.

Raw device identifiers, saves, commercial data and logs remain private under ignored reports.
