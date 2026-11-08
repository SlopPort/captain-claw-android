# Active Soldier vertical combat and hurt recovery

2026-11-08. Investigation and automated fixture by OpenAI Codex (LLM), guided by an anonymous human.

Huawei P9 Lite / Android 10, main ARM64 debug41 APK SHA-256:
`4bcf15bade79c4047cd6b387b02ae5b0c35b7596f19528f167041a5416d8f187`.

This addresses the report of repeated stagger when Claw stands below a level-1 sword enemy. It is an isolated solid-step fixture, **not the reported natural stair location or an original-game comparison**. Enemy offensive AI and ordinary incoming damage remained active. Setup initialized hero HP to 100 and unused pistol ammunition to 99; no healing/protection occurred during observation. Each action used a fresh process, waited for a confirmed additional live enemy hit and restored its fresh config/progress backup afterward.

## 32 px observed outcomes

Each reaction began at 90 HP. HP below is the final observation, after the action and release interval; it is not an attack cadence measurement. Enemy left/right describes its position relative to Claw.

| Enemy side | Requested reaction | Final HP | Enemy defeated | Actual attack / jump evidence |
| --- | --- | --- | --- | --- |
| Left | Standing sword | 85 | Yes | Uppercut; no jump |
| Right | Standing sword | 90 | Yes | Uppercut; no jump |
| Left | Crouching sword | 75 | No | Duck swipe; no jump |
| Right | Crouching sword | 75 | No | Duck swipe; no jump |
| Left | Short jump attack toward enemy | 60 | No | Jump swipe; jump observed |
| Right | Short jump attack toward enemy | 85 | Yes | Standing swipe; **no jump observed** |
| Left | Long jump away | 85 | No | Jump observed; moved 260.4 px away |
| Right | Long jump away | 90 | No | Jump observed; moved 338.1 px away |

Both standing counter attempts produced an uppercut, a sword-area contact with Soldier and a `10 -> 0` Soldier health event carrying the same source as that area. No player shots were requested. The diagnostic helper's generic `enemy_damage_observed` field alone is not attribution proof; this conclusion also uses those contact/health events.

The requested short rightward jump did not occur, even though a sword attack subsequently defeated the target. **Do not count that row as a successful jump reaction.** Investigate hurt-state input acceptance and actual takeoff timing separately. Crouching did not defeat this higher target; a low sword area missing a high body is not automatically a collision defect. The leftward short jump remained vulnerable to further hits. None of these outcomes establishes original balance or a guarantee that every reaction is safe.

## Reproduction and remaining scope

Select only an allocated device and run:

```text
python tools/vertical_combat_smoke.py --report unique-report-name --prototype ActorPrototype_Level1_Soldier --height 32 --above enemy --react-after-hit --actions standing duck jump escape
```

Raw evidence is private under `reports/todo-active-soldier-recovery-0.4.41-h32-*`; all eight observations completed. Configuration/progress restoration messages were retained. The tool records observations, not a blanket fairness pass.

COMBAT-01 remains open pending the reported natural geometry, versioned original hurt/re-hit evidence and human recheck. COMBAT-02 also remains open: 16/48/64 px, hero-above cases, ascent/descent and relevant projectiles are not covered by this eight-row sample. Do not globally change attack speed, reach or invulnerability from these results alone.

## Jump-only control and input ordering

The helper now accepts `--attack-delay-ms 0` for jump-only input, using the diagnostic command's existing zero-delay meaning. Two additional active-enemy trials used that option, otherwise retaining the 32 px enemy-above setup, both directions and 250 ms jump/move holds. Both produced a jump and no sword animation. Both continued taking damage (final HP 65 left / 60 right); this is not proof of a safe escape. Configuration/progress were restored. Private raw evidence: `todo-active-soldier-jump-only-0.4.41-h32-*`.

The failed rightward combined-input row contains a further enemy hit between the sampled pre-reaction state and the actual command. Relative to that last hit, the jump/attack command arrived about 146 ms later, buffered sword input was logged at 261 ms and buffer consumption at 345 ms. No takeoff was recorded. The configured jump hold was 250 ms from the command. Therefore the sampled 90 HP is **not** a claim that input arrived at exactly that HP or a fixed delay after damage.

Relevant source boundaries:

- `ClawControllableComponent::CanMove()` rejects movement while taking damage and during standing/duck attacks.
- `PhysicsComponent::VUpdate()` clears requested movement and returns before its jumping section while `CanMove()` is false.
- At the end of `damage1`/`damage2`, `ClawControllableComponent` restores the physical state and immediately invokes a still-valid buffered `OnAttack()`.
- The controller submits held jump movement each update; the diagnostic command schedules sword separately after 80 ms in the combined-input case.

This ordering is consistent with hurt followed by buffered sword suppressing a short held jump. The jump-only control arrived at a different offset after a later hit (about 222 ms in the rightward case), so the two runs do not isolate sword buffering as the sole cause. A synchronized native-time input trial is needed before changing priority or buffering policy. Original Claw hurt/jump rules remain unverified; no production behavior was changed by this investigation.

## 48 px follow-up and facing correction

The same exact debug41 ran eight enemy-above cases at 48 px, then a complete eight-case repeat after correcting fixture preparation. The first left-standing row requested its hero attack at X=200060 while the enemy was left of X=200000: the attack faced **away**. A short directional input during hurt had not reliably turned Claw. That row cannot establish a vertical reach miss. Original raw observations are retained as `todo-active-soldier-recovery-0.4.41-h48-*`.

The helper now requests facing before spawning the enemy, as the narrower melee-recovery fixture already did. It records that setup input and whether the requested posture was actually observed; these are not blanket fairness assertions. In the repeat's left-standing row the area was instead at X=199940, contacted Soldier and produced its `10 -> 0` health event. No production game code changed.

Passing preparation/reproduction does not require every action to win. The corrected repeat, `todo-active-soldier-recovery-0.4.41-h48-r2-*`, measured:

| Enemy side | Requested reaction | Final HP | Enemy defeated | Observed action |
| --- | --- | --- | --- | --- |
| Left | Standing sword | 85 | Yes | Kick; correct-side contact/health event |
| Right | Standing sword | 85 | Yes | Swipe |
| Left | Crouching sword | 75 | No | Duck swipe |
| Right | Crouching sword | 70 | No | Duck swipe |
| Left | Short jump attack toward enemy | 65 | No | Kick; no jump observed |
| Right | Short jump attack toward enemy | 65 | No | Jump observed, but sword animation was a standing swipe |
| Left | Long jump away | 80 | No | Jump swipe; moved 332.1 px away |
| Right | Long jump away | 90 | No | Jump swipe; moved 327.7 px away |

Pre-reaction samples were 90 HP; further hits can occur before the command arrives. AI stayed active and there was no protection/healing during the observed action. The shared session restored fresh configuration/progress after each case. Differences between attempts also involve input timing and attack selection: the current port randomly selects standing kick/uppercut/swipe without a sword powerup. Do not interpret a kick as a guaranteed sword animation or pin RNG to manufacture a balanced result.

The [original-behavior investigation](../ORIGINAL-BEHAVIOR-REA.md#important-differences-still-requiring-care) already records separate original attack rectangles/damage and warns that target eligibility does not prove contact. It does not establish original-runtime hurt recovery or fairness on the reported staircase. 16/64 px, hero-above cases, relevant projectiles and the natural report remain open; this 48 px observation does not close COMBAT-01/02.

## 64 px: measured reach asymmetry

Eight further active-enemy trials used the corrected pre-spawn facing setup at 64 px (`todo-active-soldier-recovery-0.4.41-h64-*`). All completed as observations with fresh config/progress restoration; they are **not eight winning or fairness passes**. No hero protection or healing occurred during the observed actions.

| Enemy side | Requested reaction | Final HP | Enemy defeated | Observed action |
| --- | --- | --- | --- | --- |
| Left | Standing sword | 60 | No | Swipe; no jump |
| Right | Standing sword | 60 | No | Kick; no jump |
| Left | Crouching sword | 70 | No | Duck swipe |
| Right | Crouching sword | 75 | No | Duck swipe |
| Left | Short jump attack | 60 | No | Standing swipe; no jump observed |
| Right | Short jump attack | 60 | No | Jump observed; attack animation was kick |
| Left | Long jump away | 85 | No | Jump swipe; moved 215.0 px away |
| Right | Long jump away | 75 | No | Jump observed; no attack animation captured; moved 216.9 px away |

Pre-reaction samples were again 90 HP. The right-standing sample shows a concrete geometric difference: Soldier's recorded body spans Y=935..1035, while the hero requests a 50x25 attack centered at Y=1063.9. That request is below the higher target. The enemy's recorded attack area spans Y=964..1005 and contacts the hero body beginning at Y=1003. Thus the enemy can hit in this setup while the sampled standing hero attack does not reach. This is not an integer-overlap error inferred solely from a sprite screenshot. Requests still must be distinguished from actual created/contacting bodies.

### Rechecking cached original evidence

The retained REA/Ghidra attack-construction evidence was read again, not replaced by a new original-runtime experiment. Subject: supplied CrazyHook-distributed CLAW.EXE SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`, constructor `0x41f270`, evidence `ev_4dac6420a6262ee02313141af6508d5c51f0bd4ba144a87068a3552d9b1717bf`.

The constructor stores different bounds for named animation branches. Its right-facing stored tuples at fields `+0x154/+0x158/+0x15c/+0x160` include swipe `(30,-2,112,19)`, punch `(0,-2,56,19)` and uppercut `(0,-19,56,19)`; horizontal reversal negates and exchanges the horizontal limits. The ordinary swipe branch also stores base damage 5. These are concise independent numeric findings, not redistributed decompiled functions.

The current port instead shares a 50x25 ordinary damage area for swipe/kick/uppercut/duck swipe, centered at offset `(±60,+20)`. Jump swipe shifts that center to `(±65,+10)`. The existing base scale is 10 standing / 5 crouching. This is an established implementation difference; **the original actor-origin mapping, collision consumers and full animation windows still need joining before using those tuples as Android geometry**. Copying constants or globally enlarging the hero box would not establish parity.

The existing original hurt-dispatch finding supports waiting for recovery before attacking; it does not prove that a lower-standing hero must always counter a higher enemy without jumping. The port's pending attack tap is explicitly an accommodation. This reach asymmetry and short-input ordering remain COMBAT-01 research/reproduction work. 16 px, hero-above combinations, projectiles and the natural staircase are still missing from the wider COMBAT-02 acceptance scope.

## Additional 16 px and hero-above coverage

The same exact debug41 completed eight enemy-above 16 px reactions after a confirmed hit, with facing requested before enemy spawn. Both standing counters defeated Soldier; both crouching attacks missed. The left short-jump attack jumped and defeated the target, while the right short-jump request produced a standing swipe without a sampled jump and defeated it. Both long jump-away requests moved away. Final HP was 85 except crouching cases (70); no healing/protection occurred during observation. Private evidence: `todo-active-soldier-recovery-0.4.41-h16-*`.

Twenty-four separate **hero-above** observations then completed: nominal steps 16/32/48/64 px, enemy left/right, requested standing/crouching/jump attack. Each checked the actual initial foot-height relation before acting and restored fresh config/progress. No target/unattributed fatal line was found in the 24 logs. These runs kept offensive AI active but **did not use the after-confirmed-hit prerequisite**, so they are not matched timing controls for the enemy-above recovery runs.

| Nominal step | Standing attack sampled | Duck swipe sampled | Jump state sampled |
| --- | --- | --- | --- |
| 16 px | 1 of 2 | 1 of 2 | 0 of 2 |
| 32 px | 2 of 2 | 1 of 2 | 2 of 2 |
| 48 px | 2 of 2 | 2 of 2 | 1 of 2 |
| 64 px | 2 of 2 | 2 of 2 | 1 of 2 |

Counts describe the requested posture in the sampled trace, **not wins, attack acceptance on every update, or correctness of every requested combination**. For example, the 16 px left crouch/jump requests instead sampled standing kicks, and the 32 px right crouch request sampled uppercut. A defeated enemy does not turn those into verified crouching/jumping tests. Conversely, absent sampled animation is not proof that a brief animation never occurred. Both 64 px standing trials defeated the lower target, unlike the enemy-above 64 px standing trials; this is an observed directional difference, not original balance certification.

Private evidence: `todo-soldier-heroabove-matrix-0.4.41`, four successful driver exits and six individual records per height. This adds setup/action observations for all four requested heights in both relations, but does not close ascent/descent, projectiles, all ordinary families or the unresolved posture/input behavior.

## Per-update short-jump displacement measurement

The helper now offers `--measure-jump`, using the **existing** native `combatjumpmeasure` command. It captures displacement during each playing update over the measurement window instead of relying solely on approximately 100 ms animation samples. It requires the corresponding result marker and retains missing/duplicate-measurement failures. The native metric labels upward displacement as takeoff/jumps; movement on a carrier or knockback could also move a baseline, so that metric alone is not universal proof of jump-state acceptance. Diagnostic queue time zero is not a touchscreen latency result.

Two extra enemy-above 32 px, after-hit combined jump/sword trials measured:

| Enemy side | Measured rise | First upward motion | Recorded hold | Sampled attack | Enemy defeated |
| --- | --- | --- | --- | --- | --- |
| Left | 83.3 px | 33 ms | 251 ms | Jump swipe | No |
| Right | 0.0 px | Not observed (`-1`) | 264 ms | Standing swipe | Yes |

The right trial's zero upward displacement throughout the window confirms that its absent sampled jump was not merely an animation missed between samples. It does not isolate one cause: another enemy hit can occur between the pre-reaction sample and actual input, and buffered attack/recovery ordering still requires a synchronized comparison. Adding the measurement command changes remote setup timing; these are new trials, not retroactive measurements of the earlier rows. Both restored fresh user files. No production code or APK changed. Private evidence: `todo-measured-hurt-jump-0.4.41-h32-*`.

```text
python tools/vertical_combat_smoke.py --report unique-report-name --prototype ActorPrototype_Level1_Soldier --height 32 --above enemy --react-after-hit --actions jump --measure-jump
```

COMBAT-01/02 remain open. Future work should distinguish held jump intent at recovery from the pending sword tap, preserve ordinary recovery/invulnerability rules, and validate any control accommodation without claiming it reproduces an original buffer. The original actor-origin/collision join, relevant projectiles and human-reported natural stairs are still separate requirements.

## Timing clarification: zero rise is not alone a buffer defect

Reading the exact zero-rise trial's event timestamps changed the interpretation: jump input was logged at 16:53:10.400, a **new Soldier hit** at 10.413, and the pending sword consumed after hurt at 10.747. The recorded jump hold ended after 264 ms, before that recovery. Thus this specific lack of takeoff is consistent with damage interrupting input; it does not prove that a still-held jump was stolen by the buffer.

Two additional right-side 32 px controls held input for about 700 ms:

| Requested sword delay | Recorded hold | First upward motion | Rise |
| --- | --- | --- | --- |
| 80 ms | 713 ms | 460 ms | 155.0 px |
| No sword | 710 ms | 221 ms | 99.1 px |

Both moved upward and restored fresh user files. In the sword case, hurt ended/buffer consumption was logged about 195 ms after input, while upward motion began later. The trials still began at different offsets after enemy damage, so subtracting 221 from 460 does **not** isolate the cost of sword buffering. Private evidence: `todo-held-through-hurt-0.4.41-h32-*` and `todo-held-through-hurt-no-sword-0.4.41-h32-*`.

The next diagnostic step is owner-scoped, game-thread input triggered after observed health loss, using the existing key scheduler and movement measurement. It must not bypass hurt, synthesize damage/recovery or change the pending-melee accommodation before the ordering is established.

Follow-up: [debug42 implements that bounded experiment and records four observations](UPDATE-0.4.42.md). Its initial measurement failure is retained and explicitly invalidated. Those newer results do not retroactively change this APK's evidence.
