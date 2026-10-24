# Public development test APK 0.4.31

Date: 2026-10-24. Work and automated checks by OpenAI Codex (LLM), guided by
anonymous human requirements and feedback. No natural campaign clear is claimed.

## Published artifact

- [Release v0.4.31-test](https://github.com/SlopPort/captain-claw-android/releases/tag/v0.4.31-test).
- Installer: `captain-claw-android-0.4.31-test.apk`, 34,222,098 bytes.
- SHA-256: `ee385cb56418d4a2bcdc25adc9678ed10c07a4bb06af51e421a01d86959a0a51`.
- Source commit: `559c12daf1977722f4e4e17c4eb4daa993faade8`.
- Public certificate SHA-256: `a8200c77d99383a71432c62f2e970d5fdfac0b0c80c317142e983d0f3ce9460a`.
- Application ID: `pl.pazur.port`, versionCode 43, versionName 0.4.31-dev.

Anonymous download from GitHub was streamed and hashed; it exactly matched the
local APK. Both ARM64/ARMv7 libraries are included. Signature, ELF alignment and
`zipalign -c -P 16 4` checks passed. Packaged license notices are present; no
CLAW.REZ, game map, PID or PCX game resource is included. The public source and
pinned dependency/build instructions remain available. Signing secrets stay local.

The signer reported its normal warnings about metadata entries under META-INF
not being covered as individual JAR entries. Signature verification succeeded;
this is not a claim of an exhaustive binary security audit.

## Runtime evidence and boundaries

Huawei / Android 10 retained the main ARM64 debug31 installation. Its exact
artifact `c31507c5541f3c94675b7563337dc151ac3b5cafde6b9e131b69401349d1c8cc`
passed last-life Game Over return, corner taps and melee recovery fixtures.
Flat-foot/ladder checks were performed on debug30, as identified in their reports.

A separately signed release-check package passed menu and levels 1/14 startup,
nonzero gameplay PCM, a 100 ms jump (74.6 px rise), a level-exit fixture and a
level-2 progress write. Its APK was
`12af42985657af9817247dcceeaa8bc9c274766a49a2378fc8a4aba41374fc69`.
Its ID was `pl.pazur.port.releasecheck`, then it was uninstalled. This checks the
release configuration, not this exact production-identity public APK. No existing
main app was uninstalled or signature-migrated. Original files were unchanged.
ARMv7 runtime was not retested for this version. No Redmi access was used.

## Player implications

Use the [installation guide](../INSTALL-EN.md). A debug-signed local build and
this release-signed APK cannot directly update each other. Keep the existing
installation and export progress before considering migration; do not uninstall
merely to bypass a signature error. Future public updates must use the same key.

API21 is the minimum package setting, not a universal compatibility guarantee.
Full natural campaign completion, every controller mode and 60 FPS throughout
all levels remain unverified. English interface selection does not translate
voices in Polish game data. A clean-computer/new-user installation remains an
external test gate; the developer machine's installed tools do not prove it.
