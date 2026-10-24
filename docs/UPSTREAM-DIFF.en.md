# Work beyond OpenClaw

Baseline: [pjasicek/OpenClaw](https://github.com/pjasicek/OpenClaw), pinned commit `5ee5740ca98377c76b13b50c84f610b0066a4717`. OpenClaw already provides the C++/SDL engine, REZ/image loading, Box2D physics, the hero, most ordinary enemy AI, menus and much of the gameplay. This port does not claim to have written that foundation or recovered original Monolith source code.

The Android implementation, tests and documentation in this adaptation were produced by OpenAI Codex (LLM), guided by human requirements and feedback. Upstream projects retain their authorship and licenses. Source counts describe scope, not independent originality or campaign completeness.

| Area | Adaptation work | Evidence / implementation |
| --- | --- | --- |
| Android packaging | Gradle/CMake/NDK project, ARM64/ARMv7, API 21 minimum, 16 KB alignment, SDLActivity and app-private storage | app/, CMakeLists.txt, native/android_main.cpp |
| Installation | System document picker, full REZ or prepared ZIP, bounded validation and recoverable multi-file publication | ImportSupport.java, ImportTransaction.java, [recovery tests](validation/IMPORT-RECOVERY.md) |
| Touch | Analog-style direction control, larger action buttons, independent fingers, captured touch movement, useful short jumps, cached control drawing | native/TouchControls.cpp, [viewport/touch tests](validation/PORT-0.4.14.md) |
| Widescreen | Uniform scaling with fixed logical height, more visible world, anchored HUD, menu/score coordinate handling and live viewport updates | OpenClaw patch |
| PL/EN UI | Language selection, Android screens, native action/finale labels, locally rendered menu/help/attribution text | [menu evidence](validation/MENU-LANGUAGE-0.4.16.md) |
| Progress | Validated backup/restore, atomic initial saves, pending-import replay preserving the previous backup, preparation on direct native entry, atomic checkpoint/next-level publication | [startup](validation/STARTUP-0.4.17.md), [native persistence](validation/ATOMIC-PROGRESS-0.4.18.md) |
| Performance | Optimized native dependencies, ThinLTO/O3, component lookup/update changes, narrower asset preload, SDL draw batching, clock reset after loading and phase measurements | [batching](validation/FPS-0.4.9.md), [sustained scene](validation/SUSTAINED-0.4.15.md) |
| Audio | FreePats/TiMidity packaging, lower-memory audio profile, ownership fixes, saved audio options, five missing attack-sound mappings and mixer-signal measurements | [attack sounds](validation/ATTACK-AUDIO.md) |
| Terrain/combat | Ladder-top release, edge/contact-lifetime fixes, restoration of omitted enemies, projectile damage once per hit, crouch geometry and above/below contact diagnostics | [reported bugs](validation/BUG-AUDIT-2026-10-21.md), [vertical combat](validation/VERTICAL-COMBAT.md) |
| Bosses/finale | Additional encounter mechanisms and a staged ending integrated through actor/event patches | [controlled campaign evidence](validation/CAMPAIGN-1.0.md) |
| Controllers | SDL mapping database integration, dead zones, lifecycle/input ownership and user remapping | Existing support; broad physical testing deferred, with later specific input bugs handled separately |
| Compatibility/tools | Locked sources, reproducible patches, ABI/ELF checks, map/enemy audits, local-window tests, API-21/API-35 and actual 16 KB emulator trials, clean-source build | tools/, tests/, [Android evidence](validation/ANDROID-COMPATIBILITY.md) |

Direct REZ installation, save backup/restore UX and optional haptics were inspired by [Claw Web](https://github.com/arthurboss/claw-web), Arthur Boss and contributors, with separate Android integration. Full attribution is in [NOTICE](../NOTICE.md). SDL, Box2D, libwap and other libraries are not new implementations by this project.

The 0.4.18 OpenClaw patch modifies 53 source files, with 1402 added and 135 removed lines. The port also has 26 native files and 21 override XML files. [Machine-readable inventory](upstream-diff-0.4.18.json). These figures include diagnostics and adapted/inherited integrations; they are not a measure of novel algorithms, correctness or hours saved.

Commercial game data, backgrounds and recorded dialogue remain supplied by the player. No Windows DLL/FFI/x86 address hooks are executed on Android. The ending is a staged engine sequence, not a recreation of the original movie. Controlled boss wins and technical exits do not establish a natural campaign playthrough, original-game parity or stable 60 FPS on every level. Rejected performance experiments remain documented rather than being advertised as improvements. Remaining release gates are listed in [Road to 1.0](ROADMAP-1.0.md).

Further Android adaptation work: [touch audio sliders](validation/MENU-AUDIO-0.4.19.md), [abandoned-import cleanup](validation/IMPORT-CLEANUP-0.4.21.md), [configuration validation before publication](validation/CONFIG-IMPORT-0.4.22.md). These are adaptation/test changes; inherited game code/assets are not attributed to the LLM.

## Additional implementation and historical detail

- Version 0.4.29 adds a prepared music cache of at most three tracks, safe directional navigation on text-only menus and a single melee tap buffered for up to 400 ms during hurt. The buffer is an intentional accommodation, not established Monolith behavior. [Reproductions and checks](validation/USER-REGRESSIONS-0.4.29.md).
- PCX transparency-index handling and format/path portability fixes support Polish game resources. The lower-memory audio profile uses 22050 Hz/1024, instrument fallbacks and a smaller cache, with buffer-ownership fixes. See `tools/prepare_music_bank.py`, `profiles/` and the engine patch.
- Widescreen uses a fixed logical height of 480. Ladder changes release the hero at the top and prevent repeated attachment while Up remains held; Android menu directions can repeat without repeating confirmation.
- Level 14 additions include platform/trap/launcher/geyser prototypes, LavaHand, LavaMouth, chameleons and guards. The Omar encounter includes two phases, dialogue, reset, surrender and a staged ending using user-supplied artwork.
- Aquatis adds tentacle/dynamite/stalactite arena behavior. Marrow fills previously empty parrot/bridge/transfer methods. These parameters require further original-game comparison: [Aquatis](validation/AQUATIS-ARENA.md), [Marrow](validation/MARROW-ENCOUNTER.md).
- Support-file updates are atomic; score screens accept touch; missing optional WAVs can be skipped; generated credit cards and PNG completeness checks avoid bundling commercial replacements. See `EngineSupport.java`, `tools/prepare_import_support.py` and `tools/credits_png.py`.
- Ordinary-enemy work restores 54 level-13 chameleons and fixes patrol direction, health/death, projectile damage once per hit, foot-sensor damage and active crouch bounds. A one-off level-7 projectile-contact failure did not recur after a registration guard, but its root cause was not conclusively established.

Components integrate through OpenClaw's actor factory/events. `tools/export_patch.py` records changes against the pinned commit; `git apply --reverse --check` in the engine checkout checks correspondence. The patch is not a second independent engine implementation.

Historical **0.4.3** inventory: 34 engine files changed, 572 added/45 removed lines, 11 native files and 17 override XML files, in addition to Android sources, tests, tools and build configuration. See [the retained statistics](upstream-diff-statistics.json). These counts and the 0.4.18 counts above belong to their recorded versions; they are not current-source counts or completeness claims.

For the later flat-foot and hurt-state investigation, see [REA evidence and limitations](ORIGINAL-BEHAVIOR-REA.md). The patch includes original integration work and adapted upstream behavior; none of these counts measures independent originality or exact game parity.
