# Powder-keg regression and campaign status — 0.4.23

OpenAI Codex (LLM) performed this work. The port remains based on OpenClaw;
this is a correction to diagnostic code added by this adaptation.

During an ordinary level-one campaign attempt on Redmi / Android 16,
a pistol shot at a powder keg aborted 0.4.22. The native stack was
`ProjectileAIComponent::OnCollidedWithActor -> HealthComponent ->
ExplodeableComponent::VOnHealthBelowZero -> ActorTemplates::CreateAreaDamage ->
ClawPhysics::VGetAABB`, ending in `Could not find actor to retrieve AABB`.

The diagnostic creation log queried an explosion body's bounds immediately.
Box2D was still processing a contact, so the engine correctly deferred body
creation until its world was unlocked. The diagnostic query ran too early.
0.4.23 logs requested geometry without querying physics at creation. Actual
contact bounds remain in `AreaDamageComponent` logs. Damage, blast size,
physics scheduling, collision rules and enemy behavior are unchanged.

Validation on APK SHA-256
`7b428f35c357bebb26757ae9bac1d8153ee5136ecc525783be646016fe42379c`:

- Both ARM ABIs built successfully; packaged libraries passed ABI/alignment checks.
- An isolated real level-one keg shot reproduced the old assertion on Redmi.
- The same crouching shot passed on Redmi / Android 16 and Huawei / Android 10:
  keg health decreased, explosion was requested, actual damage contacts occurred,
  and the process survived without a fatal signal.
- Two earlier baseline fixture attempts missed the keg and hit an officer;
  those failed fixture results are retained and are not counted as passes.
- Original configuration and save files were restored after each isolated test.
- Patch export/reapply matched 53 OpenClaw and one SDL modified source files.

The isolated regression teleports the hero for setup, then fires through normal
SDL input. **It is not natural campaign evidence.** Raw local evidence remains
in ignored `reports/barrel-redmi-0.4.22-baseline-r3`,
`reports/barrel-redmi-0.4.23-r1` and `reports/barrel-huawei-0.4.23-r1`.

The interrupted natural attempt used normal health/ammunition/lives, one death,
ordinary respawn, platform jumps, a real catnip pickup and later health/ammunition
pickups. It reached the lower area around x4308/y4864 in level 1. It did not
complete level 1 or the campaign. A lower-route return remained unresolved;
this is an observation requiring investigation, not a confirmed original-game
mismatch. The persistent save had not reached a disk-save checkpoint before
the crash; the respawn flag alone did not save that session for app restart.
A new natural attempt starts on 0.4.23 rather than claiming reconstructed progress.

The driver now waits for full requested key durations and permits simultaneous
ordinary jump/movement/sword input. Read-only map queries and local WWD inventory
help plan routes; they do not move the hero or modify terrain. All commercial
map data, dumps, screenshots and private device identifiers remain outside Git.

Follow-up: the first 0.4.23 natural attempt also exposed a driver timeout during
the normal death fade. This was a test-tool failure, not an established game bug.
The driver now retries only the explicit transition rejection for at most
30 seconds and pauses before screenshot transfer.
