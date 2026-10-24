# Signed candidate 0.4.27

OpenAI Codex (LLM), 2026-10-23. **Not 1.0.**
Production package pl.pazur.port, code39, min21/target35, local artifact
`dist/kapitan-pazur-0.4.27-candidate-release.apk`, SHA-256:
`010a6b710c088c3f3dc55379a49fafe2d060c3e471ccebcf9d0b26efc2dd9fb4`.

APK v1/v2 verification, both ARM ABIs, ARM64 ELF LOAD alignment 16384 and SDK
zipalign 16 KB verification passed. CN=SlopPort, RSA3072, certificate SHA-256:
`a8200c77d99383a71432c62f2e970d5fdfac0b0c80c317142e983d0f3ce9460a`.
Verifier warns that two Gradle META-INF metadata entries are not JAR-signature
protected; APK v2 verification succeeds. No debuggable flag. Test-only provider
and instrumentation classes are not part of the production source set.

The isolated pl.pazur.port.releasecheck APK SHA-256 is
`ba5d00cba4450e47fc3642f7338799a02fb4788cda0169dd188134c1af9fd00e`.
All six native libraries and classes.dex match production bytes. Only manifest,
resources.arsc and META-INF signature entries differ. Runtime evidence therefore
uses the release code under a separate installed identity; this is not an exact
production-identity or in-place migration test.

## Physical checks

Each fresh isolated app loaded the menu, normal levels 1 and 14, nonzero music
PCM, a 100 ms diagnostic jump, technical level-1 exit, virtual SDL score tap and
actual level-2 save. Level 14 unlock and exit placement are explicit fixtures,
never a natural playthrough. Primary installed ABI was verified; maps were not
read from this non-debuggable process.

| Device | ABI | Jump rise px | Exit placements | Next level/save |
| --- | --- | --- | --- | --- |
| Redmi | arm64-v8a | 64.3 | 1 | pass |
| Redmi | armeabi-v7a | 72.9 | 1 | pass |
| Huawei | arm64-v8a | 64.3 | 1 | pass |
| Huawei | armeabi-v7a | 72.9 | 1 | pass |

The task-owned app was removed after every run. Main app config/save/REZ/support
bytes stayed unchanged. Both phones retain ARM64 debug 0.4.27 for the human's
campaign. No uninstall or signature migration was performed on the main app.

Release uses RelWithDebInfo/NDEBUG. All six native libraries match 0.4.26 release,
but differ from debug; do not assign debug's long FPS measurement to release.
No sustained release benchmark, physical ARM16KB, natural campaign or physical
controller pass is claimed. Source is public; no binary GitHub release/tag 1.0
was published. [Safety tests](READINESS-0.4.27.md) and
[private key backup/migration](../RELEASE-SIGNING.md).

Before distribution, keep a private backup of the signing key and password file
outside the project. Debug-to-release migration requires a separately verified
progress backup; do not uninstall the game merely because its signature differs.
