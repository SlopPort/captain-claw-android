# Floor joins, wall support and Catnip — 0.4.32

2026-10-24. OpenAI Codex (LLM) implemented the investigation, changes and automated
checks following anonymous human reports and two private gameplay recordings.
The human confirmed the clips were recorded after the day's update: running in
place was cleared only by jumping, and could recur on returning to the same spot.
Recordings and extracted frames remain private, not repository assets.

## Reproduction and changes

The square lower corners introduced by our 0.4.30 flat-foot adaptation exposed a
floor-join snag. On Huawei debug31, walking at a 1 or 2 px raised floor segment
stopped after about 20.6–20.9 px in both directions. Jumping was not part of the
fixture. Earlier idle-edge checks missed traversal across small height changes.

Android32 keeps the flat bearing surface, but bevels its outer 2 px over a 3 px
height. This preserves the original lowest point and a 32 px flat support span
for the standard body. It avoids reverting to the old rounded capsule, which
rolled off platform ends. Head, upper body and other actors retain their shapes.

A separate inherited issue counted every foot-sensor/solid overlap as ground,
including wall sides. Each new overlap resets accumulated jump height. This can
explain an apparent extra boost without proving a second jump button event.
Android32 requires a near-sole downward ray hit with an upward-facing normal and
rejects upward player motion relative to the surface. Tracked contacts balance
begin/end counts and refresh after every physics step, including overlaps that
persist while the actor moves. Other actors and existing one-way/ladder paths
retain their handling. The near-sole tolerance is 2.5 px; it is a port solver
choice, not a claimed original Monolith constant.

[REA combat/jump findings](../ORIGINAL-BEHAVIOR-REA-2.md) also established that
Catnip doubles ordinary melee damage. The inherited absolute 100 was replaced
with double the port's existing base: 20 standing, 10 crouching. Normal 10/5,
weapon projectiles, attack geometry and ordinary hurt-immunity timing are unchanged.

## Exact Huawei runtime evidence

Main ARM64 debug32 APK SHA-256:
`3b2a0e995e6882f762d653a9e02a422d1e914009016164033464dda104eb1d17`.
Both ARM64 and ARMv7 native builds succeeded. These physical observations used
Huawei / LineageOS Android 10 / 2 GB RAM; ARMv7 runtime is not claimed here.

| Test | Result |
| --- | --- |
| Walk across 1/2 px joins, both sides | All four crossed without jump, advancing 399.6–406.1 px in the test input instead of stopping near 21 px. |
| Tall segmented wall, one held jump | Rise 155 px normally, 205 px with Catnip, matching the configured caps; no elevated wall support accepted. |
| Partial-edge support/crouch | 16 cases passed: stable partial overlap on both ends, stable crouching and falling when fully outside. |
| Full first-ladder/cap/seam/exit/jump matrix | 73 sampled states and 988 trace samples; requested assertions passed; zero stuck-grounded-fall cases. |
| First persistent checkpoint activation, then walk right/left/right without jump | Checkpoint 1 written; X 6881.9 → 6909.6 → 6858.2 → 6914.2, Y remained 4990.9. |
| Real moving level-one platform | Boarded and carried; 155 px jump, process alive. |
| Melee after real hit, Soldier 32 px above, both sides | Pending tap consumed after hurt and target defeated. Hero HP 90 to 70/80; this does not certify original encounter balance. |
| Game Over corner taps | Both returned to main menu with the process alive. |
| Ordinary/Catnip sword contacts | Standing 10/20; crouching 5/10, verified by real contact and target HP changes. |

Five stationary-fall trace candidates were retained in the ladder matrix, but
none met the stuck-grounded-fall criterion. They are candidates, not five proven
bugs or a claim that every animation issue is fixed. The checkpoint check uses
a known checkpoint fixture; it does not identify the exact location in both
human clips or prove every checkpoint/respawn path. Source tracing confirms that
ordinary death already clears velocity and climbing state; a bare teleport
function is not the whole respawn implementation. No unproven wholesale respawn
reset was added.

All scenarios are controlled fixtures, not natural campaign progress. Some
explicitly remove enemies or use invincibility, as stated in their tool headers.
The user's original settings and progress are restored. No Redmi was used.
A human should retry both recorded locations; the synthetic reproduction and
regression matrix do not certify every real-map seam.

## Reproduction tools

Select the allocated device with `ANDROID_SERIAL`; read each tool's header first.
Use a fresh report name. Do not run two owners against one device simultaneously.

- `tools/floor_seam_smoke.py --report NAME --expect-fixed`
- `tools/wall_jump_smoke.py --report NAME`
- `tools/flat_foot_smoke.py --report NAME --expect-flat`
- `tools/ladder_smoke.py --report NAME --first-map-ladder --expect-fixed --edges --bottom --idle-edges --seam-audit --seam-exits --seam-jumps`
- `tools/checkpoint_walk_smoke.py --report NAME`
- `tools/platform_boarding_observation.py --report NAME --synchronize`
- `tools/catnip_damage_smoke.py --report NAME` (`--expect-legacy` measures the old 100-damage behavior)

No original Windows runtime parity, all-campaign completion, all-controller
compatibility or all-map FPS minimum is claimed. Broader release gates remain
in the roadmap; the current known download is identified in the installation guide.
