# Development checkpoint 0.4.13

OpenAI Codex (LLM), 2026-10-22. This remains a development version, not the final 1.0.

## Interface language

Explicit PL/EN selection, Android string resources, translated native touch labels and added Omar/finale captions. Selection is stored separately from game data, progress and controller bindings. See [scope, evidence and untranslated original assets](ENGLISH-UI-PLAN.md).

`language-selection-0.4.13` passed on physical Huawei Android 10: actual controller/file screens in both languages, dialog selection/recreation, native preference serialization and an isolated English level preview. Previous preferences, saves and configuration were restored. No global Android keys, network, USB or Bluetooth settings were changed.

## Combat audit

Body and attack-area diagnostics now distinguish overlapping damage from hurt-interrupted input. Officer trials cover both sides and higher/lower arrangements; [measurements and limitations](VERTICAL-COMBAT.md) remain separate from original-game fidelity. Diagnostic input can now hold direction longer than the previous 250 ms pulse. No production health, reach, damage or invulnerability parameters were changed for these trials.

Static audit tools now read canonical XML from the actual APK's support bundle instead of an older imported `build/game-data/ASSETS.ZIP`. They record APK/support hashes and reject a mismatched follow-up APK. On this checkpoint: 45 regular enemy prototypes, 73 requested animations, 71 attack-frame checks and 1415 map placements; no structural/frame/missing-animation errors in the local extracted-asset comparison. There are 84 nondefault WWD combat-field placements, retained for behavioral review. This is not proof of fair combat or a natural playthrough.

## Local package

`dist/kapitan-pazur-0.4.13-dev.apk`, versionCode 25, SHA-256 `f0df9125bb970fc735a39c306ae52366a8240d8ff20736af78790820e5e432e2`. ARM64 and ARMv7 built; ARM64 ELF 16 KB alignment, ZIP alignment and APK signature checks passed. Actual 16 KB runtime remains untested. Huawei PL/EN checks passed after the final launcher-only import guard. Initial language iteration `994a2f1b94c256aebd642e23f761103619d6737b9d45f86bd495d130d0532eaa` is preserved as `reports/kapitan-pazur-0.4.13-before-import-guard.apk`.

Earlier iteration `5ccf38b86262bcc53369792021d446377a876c0ef942d7bb9ca03410d67b3ed7` is preserved as `reports/kapitan-pazur-0.4.13-vertical-diagnostic.apk`; the initial 16/32/64-height and held-escape batch used that iteration. It differs in Java chooser/test code; do not silently attribute its installed APK hash to the later package. Soldier trials and the new [dense-scene measurement](FPS-0.4.13.md) used the final `f0df...` APK.

The final package still needs broader Android/runtime, full-campaign traversal and sustained dense-scene performance checks. Earlier compatibility results remain associated with their tested builds. Original Monolith source has not been established as available; see [source provenance and comparison boundaries](ORIGINAL-COMPARISON.md). Commercial game data is excluded from APK/source distribution.
