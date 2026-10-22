# Vertical melee audit / Walka na różnych wysokościach

Initial measurements by OpenAI Codex (LLM), 2026-10-22. Investigation in progress; this is not a passed fairness audit or original-game comparison.

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
