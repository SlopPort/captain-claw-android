# Active Soldier recovery on a 32 px step

2026-11-08. Investigation and automated fixture by OpenAI Codex (LLM), guided by an anonymous human.

Huawei P9 Lite / Android 10, main ARM64 debug41 APK SHA-256:
`4bcf15bade79c4047cd6b387b02ae5b0c35b7596f19528f167041a5416d8f187`.

This addresses the report of repeated stagger when Claw stands below a level-1 sword enemy. It is an isolated solid-step fixture, **not the reported natural stair location or an original-game comparison**. Enemy offensive AI and ordinary incoming damage remained active. Setup initialized hero HP to 100 and unused pistol ammunition to 99; no healing/protection occurred during observation. Each action used a fresh process, waited for a confirmed additional live enemy hit and restored its fresh config/progress backup afterward.

## Observed outcomes

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
