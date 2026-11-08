# Development test APK 0.4.41

2026-11-08. Code, investigation, packaging and automated tests by OpenAI Codex (LLM), guided by anonymous human requirements and feedback. Upstream authors retain their credits and licenses.

This is a **development prerelease, not 1.0**. Natural campaign completion and several geometry/combat issues remain unverified. See [TODO](../../TODO.md) and [exact verification](UPDATE-0.4.41.md).

## Artifact and provenance

- Intended release tag: `v0.4.41-test`, targeting build-input commit `cf93e5c4d2a4c1b6ee82da4e3e0d1467a357d7e3`.
- APK: `captain-claw-android-0.4.41-test.apk`, 34,284,030 bytes.
- SHA-256: `11c32c781ff183a4bc8846cfbfb6321f0e9700c7ae92752631144136449724cd`.
- Package `pl.pazur.port`; versionCode 53; versionName `0.4.41-dev`; ARM64 and ARMv7.
- Signing certificate SHA-256: `a8200c77d99383a71432c62f2e970d5fdfac0b0c80c317142e983d0f3ce9460a`.
- Later test/tool/document commits do not change these APK build inputs. Archived-source builds passed with the installed toolchain/cached Gradle; no byte-identical-build guarantee is made.

This replaces withdrawn 0.4.31/0.4.32 downloads, whose SDL diagnostics contained a build-account directory path. Filename-prefix mapping removes the known path without disabling assertions. The exact new artifact passed the known-pattern privacy scan, signature check, both-ABI checks, ELF alignment and 16 KB ZIP alignment checks. The scan is not an exhaustive security or copyright audit. [Privacy investigation](BUILD-PRIVACY-2026-11-08.md).

## Runtime evidence and limitations

Exact Huawei main debug41 passed bounded menu, jump, Game Over, save-error and ambient-audio checks. Signed isolated releasecheck passed menu, level 1/14 startup, gameplay music PCM, short jump and staged exit/progress-write fixtures with each ARM ABI selected. Its six native libraries match production byte-for-byte. An older signed isolated package upgraded without changing its six seeded external files.

**The exact production package identity was not runtime-installed over the user's differently signed debug application.** No uninstall was performed to work around that mismatch. Isolated signed tests do not certify production-package-specific storage behavior, private preference preservation or natural campaign completion. ARMv7 was selected on a 64-bit Huawei, not tested on a physical 32-bit-only phone.

Archived-source x86_64 builds passed bounded API 21 checks. On the API 35 / 16 KB emulator, two menu runs failed before later PL/EN repeats and short jump/save-error/lifecycle cases passed. The intermittent menu-test cause remains unexplained. This is not physical ARM 16 KB runtime certification.

No 55/60 FPS guarantee is offered. A debug40 heavy stationary scene measured 47.0–60.2 FPS with batch median 53.2 during a 20-minute covered run; it is not an exact production41 performance result or an all-level minimum.

Changes since the previous public test include documented combat/animation, movement, audio, save-error, menu and diagnostic work. Remaining reported stair combat, occasional geometry snag and hurt/jump input questions are listed openly; controlled victories do not establish original balance.

## Installation and updates

Use your own lawful PC game files; this APK does not contain the commercial game. UI supports Polish/English. English UI does not translate Polish recorded voices; no redistributable English voice pack is supplied.

Existing public 0.4.31/0.4.32 users have the same signing identity. Back up progress before updating. Debug-channel users must follow [signing/migration guidance](../RELEASE-SIGNING.md); do not uninstall blindly to bypass a signature mismatch. Signing keys/passwords, private logs and human account details are excluded from source and release assets.
