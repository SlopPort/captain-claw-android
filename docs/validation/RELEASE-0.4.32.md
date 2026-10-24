# Public development test APK 0.4.32

2026-10-24. Automated work by OpenAI Codex (LLM), guided by anonymous human reports.

## Artifact and source

- [Public release v0.4.32-test](https://github.com/SlopPort/captain-claw-android/releases/tag/v0.4.32-test).
- `captain-claw-android-0.4.32-test.apk`: 34,224,915 bytes.
- SHA-256: `ba47b306408048e2523840e86872411ac6afc8eea75e7780549abbc99811553e`.
- Source: `88214a4f43a29deb83255a9b2783315df3d60563`.
- ID `pl.pazur.port`, versionCode 44, versionName 0.4.32-dev.
- Certificate SHA-256: `a8200c77d99383a71432c62f2e970d5fdfac0b0c80c317142e983d0f3ce9460a`.

Both ARM64/ARMv7 builds, signature, ELF LOAD alignment and ZIP 16 KB alignment
checks passed. Anonymous GitHub download exactly matched the local published
file's hash. Source, pinned dependency instructions and licenses are available;
commercial game data and signing secrets remain excluded. The signer emitted
its standard warnings about individual META-INF metadata JAR entries; verification
succeeded. This is not an exhaustive binary/security audit.

This uses the same signing identity as public31, so that APK can be updated
normally. Main local Huawei debug32 was retained; a debug signature cannot be
updated with this public signature. Do not uninstall to bypass the mismatch;
follow [backup/migration guidance](../RELEASE-SIGNING.md).

## Runtime limits

Exact main Huawei ARM64 debug32 artifact:
`3b2a0e995e6882f762d653a9e02a422d1e914009016164033464dda104eb1d17`.
[Floor/wall/ladder/checkpoint/platform/Catnip results](EDGE-SUPPORT-0.4.32.md)
record the detailed fixtures. Melee recovery against a higher Soldier passed on
both sides, and Game Over corner taps returned to menu. Existing settings,
controller bindings and the latest human progress were preserved. Historical
save archives that predate human play were not restored over newer progress.

A separately signed ARM64 release-check package,
`41de0be19bb8d04e8c052cdb95e9ea4edd4d82b033e77279243cc15d09b25188`,
passed menu/levels 1 and 14 startup, gameplay PCM, a 100 ms jump (73.5 px rise),
level-exit fixture and level-2 progress write. It was then uninstalled. This is
release-configuration evidence, not a runtime test of the exact public
production-ID APK. No existing main app was uninstalled or migrated.

ARMv7 runtime was not retested for32. Full natural campaign completion, every
Android/controller variant and all-level FPS minima remain unverified. English
UI does not translate Polish recordings. A clean-computer/new-user installation
still requires an external test. Human retesting at both recorded snag locations
is needed; synthetic regression coverage is not a universal real-map guarantee.
