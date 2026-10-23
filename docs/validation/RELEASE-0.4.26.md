# Signed development candidate / Podpisany kandydat rozwojowy

OpenAI Codex (LLM), 2026-10-23. This is **not 1.0**; the human owns campaign QA.

## Artifact identity

- Production package: `pl.pazur.port`, 0.4.26-dev, code 38, min21 / target35.
- Local file: `dist/kapitan-pazur-0.4.26-candidate-release.apk`.
- SHA-256: `249e96d6a9980d96c189a8a5eed3318f6a4c871f840b40dc6a135ca29e8aaeb4`.
- Certificate subject `CN=SlopPort`; certificate SHA-256:
  `a8200c77d99383a71432c62f2e970d5fdfac0b0c80c317142e983d0f3ce9460a`.
- RSA3072, APK v1/v2 verification passed. No application-debuggable flag in badging.
- Both ARM ABIs present; all ARM64 ELF LOAD alignments 16384. SDK zipalign 16 KB
  verification passed. Test-provider/test-runner classes absent from release DEX.
- Gradle release build passed; missing-key task rejected absent configuration with
  the intended error. Debug lint: zero errors, thirty retained warnings.

The new identity is kept privately, not in Git or source archives.
[Key backup and debug-to-release migration](../RELEASE-SIGNING.md) are essential.
Neither existing phone app was uninstalled or replaced by the release certificate.
Do not tell a tester to uninstall merely because signatures differ.

## Physical runtime scope

A separate `pl.pazur.port.releasecheck` build was installed temporarily. Its hash:
`5338e60c935dd01fa7bb180d1d45324976cb08ee54a13377f7756d7b4322b11b`.
All six native libraries and all DEX entries match production release bytes.
Differences: AndroidManifest.xml, resources.arsc and APK signature metadata.
Thus this validates release code/library startup with a separate installed identity;
it does not prove in-place migration or exact production-identity runtime behavior.

On Huawei / Android 10 and Redmi / Android 16:

- ARM64 default installation: menu, level 1 and normal level 14 with nonzero music
  PCM passed. Preview mode disabled; no inputs, teleports or natural traversal.
- Explicit `--abi armeabi-v7a`: same three starts/music passed. Package primary ABI
  checked; process maps were not read from the non-debuggable release process.
- Isolated level-14 save unlock was a fixture, not campaign progress.
- Task-owned isolated app was removed after each run. Original config/save/REZ
  hashes remained unchanged. Both main apps retain ARM64 debug 0.4.26-dev.

Private prefixes: `release-runtime-huawei-0.4.26`, `release-runtime-redmi-0.4.26`,
`release-runtime-huawei-armv7-0.4.26`, `release-runtime-redmi-armv7-0.4.26`.
No physical controller, complete combat suite, sustained release benchmark,
production migration, physical ARM16KB or original-game parity certification.
The release native variant uses RelWithDebInfo / NDEBUG and differs from debug;
do not assign debug's long FPS measurement to this artifact.

## Polski

Powstał podpisany kandydat 0.4.26 z prywatnym kluczem, bez imienia człowieka.
Podpis, dwie architektury i statyczne wyrównanie 16 KB przeszły kontrolę.
W osobnej instalacji na obu telefonach działały menu i poziomy 1/14 z dźwiękiem,
także po wymuszeniu ARMv7. Biblioteki i kod DEX tej instalacji są identyczne z
kandydatem, ale identyfikator i zasoby pakietu różnią się. Dotychczasowej gry
nie usuwano. Nie jest to pełny audyt wydania, dowód przejścia kampanii ani 1.0.
Przed dystrybucją zachowaj prywatną kopię klucza i hasła. Przed migracją ze starego
podpisu trzeba osobno sprawdzić eksport i przywracanie zapisów.
