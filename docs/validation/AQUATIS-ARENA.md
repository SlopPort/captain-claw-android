# Aquatis arena implementation

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Written and tested by OpenAI Codex (LLM), 2026-10-21. This is an implementation and evidence log, not certification of original-game equivalence or a completed natural playthrough.

## Sources and boundaries

The original [Claw design document](https://www.bestoldgames.net/download/games/claw/claw-design-bible.pdf), section 13.12.2.4, describes a stationary boss with tentacle and close-range attacks. The [Claw Recluse game help](https://captainclaw.net/en/game.html) describes clearing tentacles and throwing dynamite into the hole to dislodge a stalactite. Local user-owned WWD objects supply exact arena object positions and the five stalactites. Original animations and art remain in the user's REZ and are not copied into project sources or the APK.

The added code is a new implementation by Codex. It is not copied or decompiled original game logic. It retains the existing OpenClaw boss's 100 HP, death/gem handling and generic close-range attack. Tentacles have 50 HP (three existing 20-damage pistol contacts or one magic claw); this balance choice and all timing/hitbox values require comparison with actual original gameplay before claiming fidelity.

## Behavior

- The converter preserves the original three tentacles, dynamite supply, crack and five stalactites rather than dropping them.
- Tentacles use original idle, attack, hit, sinking and respawn animations. Their attack area is created once at the strike frame; dead tentacles disable collision on update, outside Box2D's contact callback.
- A player-owned dynamite projectile must detonate near the crack after all tentacles are down. The ordinary projectile fuse and explosion still run. Other projectile damage cannot directly hurt Aquatis.
- The selected stalactite falls visually before applying a 20 HP hit through HealthComponent. Surviving hits restore the tentacles. The fifth hit uses the inherited boss defeat and gem path.
- Dynamite pickup replacements are limited to one live pickup, using a weak reference. Arena discovery happens when world loading finishes so collecting the original supply before staging cannot prevent the fight.
- Death/reset cancels the pending rock and restores original rock positions, boss health and tentacles. The dedicated ordinary-input regression passed.

## Evidence

Huawei P9 Lite, Android 10 / LineageOS, 2 GB RAM:

- `aquatis-arena-contact1`: five real dynamite-fuse/rock hits, boss defeat and level 13 loaded. The script failed afterward because it expected the wrong level-title string; evidence is retained, not relabeled as a fully passing run.
- `aquatis-arena-rules2`: full scripted regression passed, including wrong-location explosion, uncleared-tentacle blocking, direct bullet immunity, tentacle respawns, gem and next level. Fixtures: teleports, player invincibility, direct spawning of ordinary projectiles. No boss/tentacle health edits.
- `aquatis-player-throw1`: failed; setup missed the post and placed the player underwater.
- `aquatis-player-throw2/3/4-capture`: failed from the real post. Telemetry showed the missing receptacle let thrown sticks fly through the crack and explode elsewhere; the first receptacle hitbox was also smaller than its real image.
- `aquatis-player-throw5-bounds`: passed with a normal approximately 1500 ms charged throw from the actual post. The receptacle now uses the imported crack sprite's extent (60×128 pixels in the standard data), captures a stick that enters it, and preserves the normal fuse before the stalactite falls. This test still uses setup teleports, protection, infinite ammo and spawned bullets to clear tentacles; the full ordinary-input/resupply/reset test is a separate gate.

## APK upgrades

`aquatis-player-fight-reset1` passed the complete controlled fight using ordinary sword attacks and charged dynamite throws, actual ammo consumption and collection of the real supply/replacements. After the first rock hit, a real water death reduced lives from three to two and restored boss health to 100, all three tentacles to 50 and the five rocks to their original heights. Five further rock hits defeated the boss; collecting the real gem and advancing the score screen loaded level 13. No projectiles were spawned and no health or ammunition values were edited. Setup teleports and protection during combat remain explicit fixtures, so this is not a natural traversal of level 12.

The APK now supplies engine XML separately in `.engine-support/ASSETS.ZIP`. The launcher verifies the bundle hash and installs updates atomically before SDL starts. Imported `CLAW.REZ`, the original imported `ASSETS.ZIP`, configuration and saves are not replaced. `aquatis-arena-rules2` used this path with the older imported archive still present, confirming `Using APK engine support` in the runtime log.

Android lint passed without errors at minSdk 21; remaining warnings were reviewed separately. Physical runtime evidence here is Android 10, not every Android version.

This encounter report does not declare a finished version 1.0.
