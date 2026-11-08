# Known limitations and tested scope

Updated 2026-11-08 by OpenAI Codex (LLM), guided by anonymous human feedback. This page describes the development state, not a 1.0 release guarantee.

## Which version does this describe?

The allocated Huawei runs ARM64 **0.4.40-dev / versionCode 52**, APK SHA-256 `2383a7d6d789a77c9504b9f459e575e394aca48817e4e704528c3f3b41134f9b`. The [0.4.40 report](validation/UPDATE-0.4.40.md) gives its exact tested scope. The downloadable signed public test remains **0.4.32-test**; fixes in a development report are not automatically included in that older download.

## Issues still requiring investigation

- **Level 2 platform blockage:** leftward movement can reportedly stop on the small platform near the crate around (2460, 4956). The earlier reproduction attempts did not trigger it. The report remains open; jumping away can destroy the contact state needed to diagnose it. See [capture instructions](validation/LEVEL2-PLATFORM-0.4.34.md), TODO MOVE-01.
- **Combat with Claw lower than an enemy:** the human reported repeated stagger and inability to strike a level 1 sword enemy. A buffered tap can execute after hurt in controlled tests, but that does not establish natural stair fairness or all original damage rules. See TODO COMBAT-01/02.
- **Natural campaign completion:** all fourteen levels have not been certified through a continuous ordinary playthrough. Technical map transitions and protected boss fixtures do not establish this. The human is the campaign tester.
- **Original-game fidelity:** several custom enemy and boss decisions, collision rectangles and damage acceptance paths remain incomplete comparisons. The [behavior ledger](ORIGINAL-BEHAVIOR-LEDGER.md) distinguishes recovered findings, port choices and unknowns.

Historical fixes for sound gain, short touches, Game Over, floor joins, ladder caps and vines have versioned evidence. They are not advertised as universal fixes for every location, input method or future build. See the [detailed TODO](../TODO.md) for exact-candidate rechecks and remaining gates.

## Deliberate differences and unsupported features

- This is an OpenClaw-based Android adaptation, not the original Monolith source or a Windows executable running on Android.
- The finale is a staged engine sequence, not reproduction of the original ending movie. Original cutscene playback is not established.
- A single melee tap may be buffered for up to 400 ms during hurt. This is an intentional port accommodation, not proven original behavior.
- Touch controls, wider view, user bindings and three difficulty presets are port features. Difficulty changes damage behavior; it is not a nonfunctional placeholder. Unsupported multiplayer and missing-page actions are removed.
- Voices and ambient sounds share the master sound setting. Inherited independent Voice/Ambient controls are disabled rather than pretending to offer separate channel switches.
- One game-data set is active. Selecting English changes supported interface text; it does not translate Polish recordings or switch between installed dubbing sets. English voice playback needs a player's own lawful English data and is not verified here. No commercial voice pack is bundled.

## Android, controllers and speed

The [compatibility matrix](validation/ANDROID-COMPATIBILITY.md) separates historical emulator/phone results from current evidence. Minimum API 21, a compiled ABI and static 16 KB alignment each establish different facts; none guarantees every Android phone. Exact final-candidate ARMv7, newer Android and physical 16 KB-page coverage remain incomplete.

The performance goal is 60 FPS; the accepted lower target is 55 FPS in the specified heavy Huawei scene. This is not an all-level or per-frame guarantee. Report long stalls, warm-device behavior and memory separately from average FPS.

Controller transport/mode, Android pairing and SDL button mapping are separate issues. GameSir red Pro Controller mode worked historically on Huawei; this does not prove every Bluetooth/USB mode works. Broad physical controller testing is deferred. Specific reported pause/input regressions remain actionable within authorized device scope.

## Data and installation boundaries

Players provide their own game data. An APK/source download does not supply commercial levels, graphics or voices. A tiny CrazyHook placeholder CLAW.REZ is not a full archive; follow the [installation guide](INSTALL-EN.md).

Never uninstall an existing game to bypass a signing mismatch without a deliberate, checked backup/migration plan. Debug and public release signatures differ. Import recovery has bounded automated evidence, but not every document provider or large-file picker path has been tested.

Public files exclude proprietary game data, raw reverse-engineering dumps, personal device identifiers, user saves and signing secrets. Human participation remains anonymous; adaptation work was performed by OpenAI Codex (LLM), with upstream contributions separately credited.
