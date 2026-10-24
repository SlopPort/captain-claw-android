# Normal-enemy audit — 0.4.2

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Controlled trials completed 20 October 2026. This is not a full map playthrough.
Machine summary: `combat-audit/final-validation.json`. Raw evidence/configurations
remain local in ignored `reports/`, outside the repository.

## Scope and assets

Inventory: 45 normal-enemy variants and 1415 WWD objects across 14 maps, excluding
bosses and enemies created later during play. Effective inherited XML prototypes
were inspected from the exact ASSETS.ZIP delivered to the phone.

All 73 animations and 71 attack-frame indices, including Rat cannons, exist and
fit within the original animations. Initial HP/body dimensions are positive and
structurally valid for all 45 prototypes. Evidence:
`combat-audit/asset-validation.json`, `inventory.json`, `map-coverage.json`.
Repeat using `tools/audit_combat.py`, `tests/combat_assets_probe.cpp` extraction,
then `tools/verify_combat_assets.py`.

## Gameplay changes

- Restored 54 level-13 Chameleons previously mapped to a null prototype, using
  level-13 images/animations and the shared Chameleon behavior.
- The support sensor no longer takes projectile/damage-area hits. It extends
  below the real body to detect ground; shots below the feet previously lost HP.
- A projectile damages a given actor at most once, including repeated contacts
  and piercing projectiles. Separate projectiles can still hit independently.
- Crouched active-body bounds exclude disabled head/torso pieces. Their collisions
  already disabled, but the bounds query previously returned standing dimensions.
- Patrol starts with the image's facing direction, instead of always right.
- Health handling uses the correct initialization source, avoids duplicate death,
  does not react to healing as damage, and ignores further damage after death.
- Projectile hit points use the active body's left/right edges symmetrically.
- Projectile contacts require matching physical-body/actor registrations. An
  unregistered/replaced body is skipped before bounds queries or damage.

## Phone method

Redmi Note 8, Android 16, ARM64. Only the running app reads test commands; keys go
directly to SDL. The script checks process/foreground window and aborts on loss.
No global Android keys. Configuration/save restored after each batch.

Incoming-attack tests use real AI, no hero protection and enemies on both sides.
Sword/pistol tests use passive stationary targets and a protected hero, measuring
hits/HP/death rather than natural difficulty. Crab is the exception: its idle
shield has 100% parry, so offense remained enabled and hits used shield openings.
The earlier passive Crab correctly took no damage. Low targets are shot from a
crouch. Siren checks also inspect freeze, as its projectile need not remove HP.
Seagulls/cannons use other mechanisms than the shared melee attack frame.

Each group runs on its source map. An early Mercat fixture on level 1 asserted
when creating the trident effect, absent from level 1's LEVEL_* assets. That is
an invalid fixture limitation, not proof of a natural level-11 crash. Other early
helper failures removed actors without scene notification or tried to resume a
dying hero. Helpers were corrected; those trials were not relabeled successful.

## Results and limits

Before the fix, a shot below the feet removed 10 HP, and one projectile removed
1 HP twice. Initial regression passed 12 height/direction/crouch combinations
plus repeated-contact coverage: 13/13. Final app-local input repeat also passed
13/13: `combat-final-regression-0.4.2/results.json`.

The 45-variant matrix passed after adapting the Crab fixture to its actual
vulnerability. The first level-7 BearSailor trial asserted while reading an
unregistered projectile body's bounds: `combat-level7-failed-0.4.2/crash.log`.
A fresh-process retry passed. The mismatch's cause remains unconfirmed. A
registration guard was added without claiming it proves the cause fixed. The
final package then passed 16 ranged variants at 250 pixels, four level-7 types
and 13 hitbox checks. Each ranged variant contacted Claw from both sides.
`Pazur ignored unregistered projectile contact` also includes ordinary contacts
from removed projectiles with cleared actor pointers; alone it does not reproduce
the earlier registry mismatch.

Windows balance parity is unconfirmed. Original WWDs contain 84 objects with
nonzero health/damage fields; interpretation was not changed globally without
proof of semantics. They are recorded in `map-coverage.json`. Asset validation,
load inspection and controlled combat do not replace every-map traversal,
natural-terrain attack observations or frame-by-frame Windows comparison.
Other Android versions and 1–2 GB phones still needed separate devices at this
checkpoint.

A final level-7 Pirate trial initially parried three bullets (HP 25→25); the
prototype has 50% bullet parry and 33% sword parry. Retry confirmed damage
(25→5). Original: `combat-level7-final-0.4.2/results-before-parry-retry.json`;
retry: `combat-pirate-final-0.4.2/`. Parry probabilities were unchanged.

The complete 45-variant matrix preceded the final body-registration guard.
Afterward, the final APK passed the contact regressions, four level-7 variants
and all-map inspection. Evidence: `combat-matrix-0.4.2-level*/`,
`combat-ranged-final-0.4.2-level*/`, `combat-level7-final-0.4.2/`,
`combat-all-maps-0.4.2/`. [HP/body table](enemy-health.csv).

Loaded-map inspection confirmed 1415/1415 expected actors, positive initial HP,
valid body dimensions and 54 level-13 Chameleons. All 14 processes stayed alive
in short music/effects trials. Post-load PSS: 191.0–345.4 MiB; not long-play memory
or evidence of low-memory-device smoothness.

| Level | Normal enemies | Valid HP and bodies |
|---|---:|---|
| 1 | 54 | yes |
| 2 | 72 | yes |
| 3 | 90 | yes |
| 4 | 88 | yes |
| 5 | 132 | yes |
| 6 | 140 | yes |
| 7 | 124 | yes |
| 8 | 174 | yes |
| 9 | 118 | yes |
| 10 | 90 | yes |
| 11 | 75 | yes |
| 12 | 102 | yes |
| 13 | 113 | yes |
| 14 | 43 | yes |
