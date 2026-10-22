# Vertical melee audit / Walka na różnych wysokościach

Initial measurements by OpenAI Codex (LLM), 2026-10-22. Investigation in progress; this is not a passed fairness audit or original-game comparison.

Fixture clarification from source review: `combatstage/combatdummy` initializes hero health to 100, disables protection and supplies pistol ammo 99 **before** the initial sample. Damage is then ordinary, with no health edits during the observed action; no shots are fired in these melee trials. The earlier tool header's broad wording “no health edits” was inaccurate and has been corrected. `VScaleActor(...,2.0)` in setup restores standing fixture collision masks in this engine; it does not multiply the hero's geometry dimensions. These trials remain controlled setups, not evidence of conserving normal campaign health/ammo.

Po polsku: przed pomiarem scena ustawia zdrowie bohatera na 100 i amunicję pistoletu na 99, bez ochrony. Podczas obserwowanej akcji nie podmieniamy zdrowia. Poprzednie ogólne sformułowanie o braku edycji HP było zbyt szerokie; nie traktujemy tych prób jako normalnego przejścia gry z zachowaniem zasobów.

## Active officer, 48 px step

`vertical-officer-48-0.4.12` comprises eight fresh-process trials. The officer uses its level-one source assets and ordinary AI/10 HP. Setup uses isolated geometry and actor placement; player protection is off and no shots are fired. Fixture setup supplies pistol ammo, explicitly unrelated to these melee trials. Each row samples health after the input and a short observation interval; screenshot capture continues afterward, so the final sampled health is not a survival guarantee.

| Higher character | Enemy side | Hero input | Player HP lost after initial sample | Enemy damage observed | Hero attack animations observed |
| --- | --- | --- | --- | --- | --- |
| Enemy | Left | Standing attack | 70 | No | swipe |
| Enemy | Left | Short jump/attack | 70 | No | none |
| Enemy | Right | Standing attack | 20 | Yes, defeated | uppercut |
| Enemy | Right | Short jump/attack | 70 | No | none |
| Hero | Left | Standing attack | 50 | No | none |
| Hero | Left | Jump/attack | 60 | No | jumpswipe |
| Hero | Right | Standing attack | 70 | No | none |
| Hero | Right | Jump/attack | 30 | No | jumpswipe |

The apparently asymmetric standing result also selected different inherited random melee animations (swipe versus uppercut). It is not proof of a left/right hitbox bug. Several requested attacks never began during repeated `damage1`/`damage2` animations; these rows cannot independently prove geometric misses. In one enemy-above case a 250 ms jump press occurred entirely during hurt recovery and no takeoff was observed. The earlier long scripted stairs trial did jump but later died under continued attacks; its command timed out during the death/respawn transition and is not a passing escape test.

The officer generated approximately half-second repeated hits in the sampled close-range fixtures. This is evidence for further recovery/counterattack investigation, not a decision to change invulnerability or enemy speed without original-game comparison. Initial active body rectangles were recorded for both actors; foot-support sensors are not treated as hurt bodies.

## Next separation tests

Repeat geometry trials with offensive AI explicitly removed, retaining real collision/damage/parry, to distinguish accepted hero attack overlap from hurt-interrupted input. Keep these separate from active-AI trials. Then test longer-held jump/escape, crouching, additional offsets, enemy archetypes and actual map geometry. Do not enlarge reach or edit health to obtain a desired result. See [the full case plan](VERTICAL-COMBAT-PLAN.md).

The later diagnostic builds add body-rectangle logs, hero-above solid geometry and optional passive setup only. No production hitbox, attack damage, invulnerability or recovery timing has been changed by this audit.

## Passive geometry separation and exact contacts

`vertical-officer-48-passive` contains twelve trials (both higher characters, both sides, standing/jumping/crouching). With offensive AI disabled, standing attacks defeated the 10 HP officer in all four standing cases; crouching attacks removed 5 HP in all four crouching cases. Parry and ordinary physics remained enabled. Jump trials did not hit; animation acceptance and the moving attack position must be reviewed before interpreting those misses.

The follow-up `vertical-contact-48-passive` recorded actual area creation and contact on the lower hero's left. Both a standing kick (10 damage) and crouching swipe (5 damage) created area `(199894,1050,51,26)` against officer body `(199895,951,49,100)`. Their integer rectangles overlap by one pixel vertically. No extra damage reach was introduced. This is a narrow contact, not evidence that every diagonal arrangement is reachable.

`vertical-officer-48-escape` observed takeoff in all four active cases. When the hero started above, both cases moved away and lost 10 HP. When the officer started above, both cases suffered continued hits and did not establish a lasting escape. These are not validated long-held directional escape tests: the diagnostic command caps jump hold at 1000 ms even when supplied 1500, and holds direction for only 250 ms. The script's `escape` label describes an attempted input, not proven sustained movement or survival. Preserve this limitation when interpreting the reports.

The diagnostic APK built in `build-area-contact-probes.log` compiled for ARM64 and ARMv7 and ran the two exact-contact trials on Huawei Android 10. Original configuration and saves were restored after each trial. Natural map stairs, other enemy types, remaining heights and original-game parity are still open.

## Additional heights, sustained escape and shorter bodies

The first 0.4.13 iteration (`5ccf38b86262bcc53369792021d446377a876c0ef942d7bb9ca03410d67b3ed7`) ran these additional officer cases:

| Step height | Passive standing, enemy above | Passive standing, hero above |
| --- | --- | --- |
| 16 px | Both sides hit/defeat | Both sides hit/defeat |
| 32 px | Both sides hit/defeat | Both sides hit/defeat |
| 48 px (earlier batch) | Both sides hit/defeat | Both sides hit/defeat |
| 64 px | Both sides miss | Both sides hit/defeat |

The 64 px crouching cases likewise missed from below and dealt 5 damage from above. An observed hero-above standing area at y=986..1012 overlaps officer body y=999..1099; an enemy-above body's bottom is about 1035 while the grounded hero area begins at 1050. These are geometry-dependent outcomes, not symmetric vertical reach or proven original-game parity.

`vertical-officer-48-held-0.4.13` holds jump and the away direction for 1000 ms, with an ordinary sword input scheduled at 450 ms. All four trials observed takeoff and displacement away from the opponent. Enemy-above trials lost 20 and 10 HP after the initial sample; hero-above trials lost 10 HP each. None observed player death during the captured interval. This establishes an available escape in these isolated cases, not indefinite safety from pursuing AI or a natural staircase test.

The final Java chooser APK (`994a2f1b94c256aebd642e23f761103619d6737b9d45f86bd495d130d0532eaa`) ran `vertical-officer-jump150-0.4.13`: four accepted jumping swipes, 250 ms jump hold, 20 ms direction hold, 150 ms attack delay. All missed. Enemy-above areas at y=919..945 passed above the body starting at y=951; hero-above areas were higher still. Recording accepted animation and actual area location prevents these from being misreported as dropped sword input.

`vertical-rat-48-0.4.13` on the same final APK covers eight passive cases with the actual 5 HP level-one Rat prototype. From below, standing and crouching attacks defeated the rat on both sides. From above, all four attacks passed above the shorter body (rat starts around y=1058; grounded hero area ends around 1028). One boundary contact against the higher left rat had integer `SDL_HasIntersection=false` while Box2D delivered contact/damage at the touching edge. Integer rounding and Box2D skin are different geometries; do not add an integer-overlap health gate based on this diagnostic flag alone.

These tests still do not cover every normal enemy, natural map route, projectile trajectory or descending attack. The script now accepts a source prototype and loads its own level, records installed APK hashes, and separates direction duration, jump hold and attack delay. Existing reports retain their original results and limitations.

## Later jump phase and soldier

`vertical-officer-jump450-0.4.13` hit/defeated the higher passive officer on both sides with an ordinary jumping swipe scheduled at 450 ms. The trace before the left contact has `falling=1`, `jumping=0`, positive vertical speed 7.5656 and y=948.99; its area then spans y=966..992 inside the enemy body. This verifies two descending attacks, not every airborne trajectory. The contrasting 20 ms input (`vertical-officer-jump20-0.4.13`) showed a standing swipe followed by takeoff but no created damage area; it cannot be treated as an accepted jumping-swipe geometry test.

`vertical-soldier-48-0.4.13` used final guarded-import APK `f0df9125bb970fc735a39c306ae52366a8240d8ff20736af78790820e5e432e2`: all eight passive higher/lower left/right cases hit. Standing attacks defeated the 10 HP soldier; crouching attacks removed 5 HP. `vertical-soldier-held-0.4.13` observed jumps and away movement in all four active cases, without death during the recorded interval. HP losses after initial samples were 30/10 for enemy-above and 30/30 for hero-above. This enemy can also shoot; total HP loss is not solely the measured sword-area contacts, and moving beyond melee range does not establish immunity to its projectiles. Active damage-source interpretation and original-game comparison remain open.
