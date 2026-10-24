# Finale and enemies — 0.4.0, 2026-10-20

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Raw evidence/configurations are local in ignored `reports/`, outside this repository.
This is a historical implementation/test record; later versions need their own evidence.

**2026-10-22 / 0.4.12-dev follow-up:** `omar-campaign-current1` found a regression
in our new support bundle: two missing credits PNGs crashed menu initialization
after the finale. Original text-only credits cards, without portraits/game art,
and a packaging PNG-completeness check were added. `omar-campaign-credits-fixed`
passed both Omar phases, staging, score, menu return and absence of a level-15
save. It uses teleports, elements, infinite ammo and protection without changing
boss HP. This is not a natural map clear.

Omar and BossStager were added to ordinary level-14 loading. Level selection and
profile limits increased to 14; old limit-13 configuration is upgraded when read.
Level 13 completion can unlock 14. Finale score returns to menu without creating
a save for, or trying to load, level 15.

## Combat and staging

Omar has 200 HP. The first half requires the opposite element through a rotating
shield gap. A correct hit removes 25 HP and changes the shield; matching the
shield restores 25. Ordinary damage is blocked. The second half requires three
pistol hits then a crouching sword attack; a hit removes 25 and moves Omar to
the opposite side of the upper platform. Actual projectile/sword contacts apply
damage; dispatching a key alone does not.

The encounter uses the original shield/energy images and Omar animations.
Energy projectiles deal 20 damage. Eight shield pieces and at most 12 expiring
projectiles bound actor counts. Boss moves are deferred outside locked physics
steps. Player death resets phase, shield, counters, projectiles and position.
Arena entry sets a temporary upper-platform respawn without overwriting the
checkpoint save file.

Arena element swords respawn six seconds after collection, one of each type.
Phase two replenishes pistol ammo to at least 24. These are explicit port choices.
The post-third-bullet opening lasts 3.5 s, successful-hit delay 900 ms and
projectile speed 230 pixels/s. These values were neither recovered from machine
code nor compared frame-by-frame against Windows.

The introduction uses original STAGING dialogue, two-axis camera pans, boss name
and announcement. Surrender plays killfall, killfall2 and killfall3, holding the
last frame. Original gem, Adora and amulet images follow with brief Polish text,
then score. This is an engine recreation, not the original ending movie.
The announcement camera follows Omar's height; the frozen hero does not also
try to zero its vertical offset.

WALL, GONG, SIAMESE and AMULET decoration loading now handles unnumbered single
PID files. Score uses available AMMAKE.WAV rather than an absent English Claw
recording. A missing WAV no longer dereferences a null handle for duration.

## Enemies

TigerGuard uses frontflip/backflip, horizontal speed 2.6 and a 5 m/s jump.
Patrol limits remain; dodge interval is 2.4 s. It cannot start another dodge
while airborne. Other levels keep existing RollEnemyAIStateComponent parameters.
High/low attacks, blocking, loot and death remain active.

Chameleon fades from full visibility to alpha 32 and back over 6 s. Tongue attack
and hit reaction reveal it; death restores full visibility. Alpha is per actor.
Chameleon climbing and all TigerGuard moves were not reconstructed.

`tiger-polish-0.4.0` exposed an out-of-vector attack-action read when the dodge
interval ended before the attack animation. Visibility checks now use the first
action's fixed sensor, and dead enemies cannot reenter combat. The failed result
and crash stack remain retained.

A fight retry also exposed ordinary stop/landing callbacks interrupting Claw's
death animation, leaving a zero-health hero. Death state is now preserved through
the animation; only then does the existing respawn mechanism run.

## Evidence scope

`tests/omar_battle_test.cpp` ran as an ARM64 phone program: PASS for opposite
elements, healing, both phases, the three-bullet gate, death and reset. It
supplements gameplay trials rather than replacing them.

`--omar-fight` uses ordinary Android key events, temporary protection of the hero
only, developer teleports, element swords and infinite ammo. It does not directly
change Omar HP or delete him. It proves neither natural traversal, balance nor
reaching the arena from the start.

Earlier `omar-input-0.4.0-final` defeated Omar but crashed on a missing recording
when opening score. Its `crash_free=false` remains; it is not reported as PASS.

Redmi Note 8, Android 16, ARM64; music/effects enabled:

| Trial | Result | PSS KiB | Scope |
|---|---|---:|---|
| tiger-polish-0.4.0-final | PASS | 202455 | Dodges, attacks, unprotected hero damage, 14 s |
| chameleon-polish-0.4.0 | PASS | 202765 | Alpha 32 and 255, unprotected hero, 12 s |
| tiger-defeat-0.4.0 | PASS | 201383 | Ordinary attacks and guard death with hero protection |
| sword-resupply-0.4.0 | PASS | 202916 | Ice sword pickup/respawn, no protection |
| omar-reset-0.4.0-final | PASS | 200735 | Hit 200→175, lava death, respawn and fresh fight |
| finale-release-0.4.0 | PASS | 219801 | Eight hits, surrender, amulet, score and menu |
| normal-release-0.4.0: level 1 | PASS | 196070 | Ordinary start, 6 s, no protection |
| normal-release-0.4.0: level 13 | PASS | 360435 | Ordinary start, 6 s, no protection |
| normal-release-0.4.0: level 14 | PASS | 249820 | Ordinary non-preview start, 6 s, no protection |
| chameleon-defeat-0.4.0 | PASS | 200237 | Ordinary attacks and Chameleon death with hero protection |

In the reset trial, protection was disabled before real lava death. Respawned
Claw has fewer lives and appears in the arena; Omar restarts at full HP, without
manual HP editing.

`finale-release-0.4.0` tests the exact dist/ APK whose SHA-256 begins
`181402071ce6d346`. Finale, score and Polish-menu screenshots were inspected.
No crash or missing resource occurred during the scenario. PSS 219801 was taken
after menu return; separate `memory-during-battle.txt` measured 201882 KiB in
combat. Stable process samples were about 60 FPS, p95 17–18 ms; warmup,
teleports and screenshots had larger spikes. This is not a sustained load test.

APK inspection confirmed ARM64/ARM32, ARM64 segment/ZIP 16 KiB alignment and v1/v2
signature. The engine patch reverse-apply check passed. Installed APK matches
dist/, as does ASSETS.ZIP in its paired data package. Full hashes:
`distribution-0.4.0.json`; other checks: `apk-0.4.0.json`, `zipalign-0.4.0.txt`,
`signature-0.4.0.txt`. Configuration/saves were restored.

`omar-finale-0.4.0` confirmed all eight hits, surrender, amulet, score and menu
without a crash or missing resource references. Its script continued confirming
in the menu and started level 1; final PSS 260678 is not combat memory. The
scenario was corrected to stop input after menu return.

## Behavior sources

- [Claw Design Bible](https://ics.uci.edu/~frost/GameDesign/ClawDesignDoc.pdf):
  enemy/amulet-ceremony descriptions. A design document differs from the final game.
- [Richie Kleinhenz's walkthrough](https://captainclaw.net/en/walkthroughs.html):
  alternating elements and the three-bullet/crouching-attack sequence.
- Original local WORLD.WWD, PID, ANI, ANIMATION.TXT and WAV;
  geometry extraction: `asset-probe-14-omar.txt`.

At this checkpoint, full traversal, faithful balance, older Android, 1–2 GB
phones and physical 16 KiB pages remained unverified. Compiling ARM32 does not
prove its runtime behavior.
