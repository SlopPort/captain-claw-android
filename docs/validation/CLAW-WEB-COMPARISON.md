# Claw Web source comparison

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Later integration, attribution and Android results: [0.4.8](PORT-0.4.8.md).
This audit preserves the state before that integration.

Date: 2026-10-20. Static audit by Codex (LLM). Our revision: `f376b10` /
0.4.7-dev. Claw Web:
[`e723d3d48b5ba2cc723751209954cfc46c82d202`](https://github.com/arthurboss/claw-web/tree/e723d3d48b5ba2cc723751209954cfc46c82d202).
Shared OpenClaw ancestor: `5ee5740ca98377c76b13b50c84f610b0066a4717`,
present in both histories.

## Findings and limits

The checked revision did not contain a finished finale implementation replacing
our additions. Its README's “Full Game: All 14 levels” claim was not supported
by the inspected sources. It does contain valuable browser integration, direct
REZ import, save tools and haptics missing from our then-current port. Widescreen,
joystick and controller support developed in parallel: shared goals do not prove
identical implementation or that all Android work was unnecessary.

This compares source against the shared base. Its build was not run or benchmarked
on Huawei, and no full playthrough was performed. Neither completeness of our
version nor a performance advantage over Claw Web is claimed.

## Differences at these revisions

| Area | Checked Claw Web revision | Our 0.4.7 port |
|---|---|---|
| Platform | WebAssembly, HTML/JS, installable PWA, service worker, offline support | Native Gradle/NDK APK, ARM64 + ARMv7, Android system importer |
| Level 14 | No `LEVEL_METADATA/LEVEL14.XML`; its only tracked LEVEL14 path asset is the loading screen. No Omar component or our new prototypes | Metadata, platforms/traps, geysers, LavaHand/LavaMouth, TigerGuard/Chameleon, custom Omar and finale staging. Original parity/full traversal unconfirmed |
| Level 13 | `Chameleon` maps to `ActorPrototype_Null` | 54 placements restored; fade behavior |
| Hits and health | HealthComponent/ProjectileAIComponent differences mainly add haptics; ClawPhysics implements SetVelocity, without our contact/active-crouch fixes | HP/death, single projectile contact, foot sensor and crouch-bounds fixes; 13 Huawei regressions passed |
| Ladders | PhysicsComponent changes only landing threshold `>2` → `>0`; no top-reattachment guard | Climb completion/reattachment guard; actual level-one first-ladder test passed |
| Joystick/buttons | HTML/CSS Pointer Events, pointer capture, joystick/D-pad, vibration and responsive layout; JS KeyboardEvents | SDL eight-direction joystick, multitouch, independent key ownership alongside controller, 110 ms minimum jump pulse, texture cache |
| Short jump | `setupHoldButton` releases on pointerup/cancel; no analogous minimum hold found in this path | Touch adaptation: about 74 px on Huawei, one jump per hold, engine timing 28–30 ms |
| Controller | Browser Gamepad API, hotplug, fixed C++/JS mappings, gameplay vibration | SDL_GameControllerDB, native Android codes, capture/remapping UI, focus/hotplug; human-assisted physical GameSir tests |
| Haptics | HapticFeedback layer with damage/explosion/footstep/landing events | No custom vibration implementation; functional advantage for Claw Web |
| Widescreen | Widescreen/display settings and browser layout | More world without sprite distortion, anchored HUD/menus; parallel work |
| Game data | Direct user `CLAW.REZ`, stored in IndexedDB | Prepared `game-data.zip`; preparation less convenient than direct REZ |
| Progress | localStorage, JSON import/export/reset from menu | App-directory SAVES.XML; no equally convenient progress import/export UI |
| Audio settings | C++ SaveGameOptions still a stub; this alone does not prove every browser setting is lost | Android persists enabled states/volumes on background/exit; restart and unrelated-field preservation passed |
| Loading | Narrower menu/font preload, on-demand metadata, browser cache/offline infrastructure | Broader CLAW/GAME/STATES preload and early metadata loading; optimization candidate |
| FPS | No same-phone measurement; renderer change count is not performance proof | Short stationary Huawei samples: level 1 about 60 FPS, level 13 about 43 FPS; no whole-game benchmark |

## Why “14 levels” alone is insufficient

1. [README](https://github.com/arthurboss/claw-web/blob/e723d3d48b5ba2cc723751209954cfc46c82d202/README.md) claims all 14 levels.
2. [Metadata directory](https://github.com/arthurboss/claw-web/tree/e723d3d48b5ba2cc723751209954cfc46c82d202/Build_Release/ASSETS/LEVEL_METADATA) contains levels 1–13, without 14.
3. [BaseGameApp.cpp](https://github.com/arthurboss/claw-web/blob/e723d3d48b5ba2cc723751209954cfc46c82d202/OpenClaw/Engine/GameApp/BaseGameApp.cpp#L1423) builds `/LEVEL_METADATA/LEVEL<n>.XML`; a missing file returns `false`, and GetLevelMetadata returns NULL. No fallback generating level-14 metadata was found.
4. [build_wasm.sh](https://github.com/arthurboss/claw-web/blob/e723d3d48b5ba2cc723751209954cfc46c82d202/build_wasm.sh#L31) rebuilds ASSETS.ZIP from that source directory. No tracked alternative ZIP with the complete level was found.
5. [LEVEL13.XML](https://github.com/arthurboss/claw-web/blob/e723d3d48b5ba2cc723751209954cfc46c82d202/Build_Release/ASSETS/LEVEL_METADATA/LEVEL13.XML#L34) disables Chameleon through ActorPrototype_Null.


A level-selector entry/loading image does not implement enemies, traps or finale.
An unpublished revision or differences between deployed site and these sources
remain possible.

## Useful integration candidates

1. **Direct CLAW.REZ import.** The biggest installation simplification. We need a
   redistributable support package with known licenses and Polish-data variants.
   Do not copy another ASSETS.ZIP/game art without checking provenance.
2. **Progress import/export through the system picker.** A useful functional
   model; Android must replace EM_ASM/localStorage. Existing SAVES.XML can remain.
3. **Narrower preload.** Compare cold-start time, memory and first-use hitches.
   Their BaseGameApp is useful reference; some “lazy loading” already uses
   OpenClaw's existing cache.
4. **Optional controller/phone vibration.** Event/preset organization could be
   adapted to SDL/Android output. Defaults and low-end cost need testing.
5. **Small gameplay fixes to reproduce separately:** preserve final-death pose,
   SetVelocity instead of assert, and empty attack-action validation. Our AI
   validation already uses the first sensor; do not mechanically replace it
   with their index check.

No candidate was integrated into production code during this comparison. Source
inspection preceded changes; wholesale engine replacement was not justified.

## Shared base and additional work

- Both projects inherit most engine/gameplay from OpenClaw; we do not claim it.
- Widescreen, touch and controllers exist in both. Earlier comparison might have
  reduced parallel design/testing, but saved time cannot be honestly quantified
  without earlier integration.
- Our APK, Android lifecycle/import, GameSir remapping, ladder/combat fixes,
  level-14 additions and Huawei tests remain concrete additional work. No
  equivalents were found in this Claw Web revision.
- Their PWA/offline, browser audio, progress export, haptics and direct-REZ
  convenience are concrete additional work in their project.

GPLv3 permits code collaboration subject to license, attribution and change-notice
requirements. It does not automatically grant rights to original game assets.
This is not a complete legal or file-by-file licensing audit of Claw Web.
