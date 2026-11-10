# Checkpoint reload, ordinary death and movement

2026-11-08. Automated reproduction and analysis by OpenAI Codex (LLM), guided by anonymous human reports.

Huawei P9 Lite / LineageOS Android 10, main ARM64 debug41 APK SHA-256:
`4bcf15bade79c4047cd6b387b02ae5b0c35b7596f19528f167041a5416d8f187`.

## Two separate paths

Both fixtures activated the real level-1 checkpoint through collision after diagnostic placement, observed the atomic progress-save path, restarted the process and loaded checkpoint 1 through real app-local menu keys. Neither injected checkpoint/save events nor traversed the natural route. Fresh user configuration/progress were restored and verified byte-for-byte by the shared session at exit. No target or unattributed fatal error was recorded.

| Path | Start of movement | Right | Reverse left | Return right | HP during movement |
| --- | --- | --- | --- | --- | --- |
| Menu checkpoint reload | X=6881.9 | 6911.9 | 6855.4 | 6912.8 | 100 throughout |
| Ordinary death then checkpoint respawn | X=6873.0 | 6901.0 | 6845.0 | 6901.3 | 100 throughout |

Y stayed at 4990.9 in every listed movement sample. Requests were 80 ms Right, 160 ms Left and 160 ms Right; **no jump** was requested. Both paths exceeded their bounded horizontal displacement assertions. They do not establish a pixel-exact response latency or all-terrain traversal.

## Ordinary death setup and initial failed trial

After the menu reload, the death fixture moved Claw to an isolated arena and spawned an active level-1 Soldier. The arena helper removes other enemies/projectiles, initializes HP100 and pistol ammo99, and clears protection. No shots, healing or protection were applied during the observed enemy damage. The fatal health event's source matched the spawned Soldier. Remaining lives were checked from the freshly game-written checkpoint; this was not the last-life Game Over path.

The initial death trial **failed** when its fixed five-second wait attempted a diagnostic read during the legitimate death fade (`game not running`). Fatal HP loss is followed by the death animation and then a separate fade process. Its raw evidence and data-restoration result were retained. This is not counted as a successful respawn test or evidence of a game defect.

The corrected trial waited for the fade's paused context and then confirmed return to running context before reading the hero. Claw respawned at `(6873.0, 4990.9)` with positive HP and moved in both directions as listed above. It did not bypass the fade, synthesize a respawn event or reopen a menu to unstick the game.

## Reproduce and limits

Select only an allocated device, then use either existing helper option:

```text
python tools/checkpoint_local_smoke.py --report unique-reload-report --walk-after-reload
python tools/checkpoint_local_smoke.py --report unique-death-report --walk-after-reload --ordinary-death
```

Both cases are also selectable as `checkpoint-reload-walk` / `checkpoint-respawn-walk` in the regression batch tool. Private evidence: `todo-checkpoint-reload-walk-0.4.41`, failed `todo-checkpoint-death-respawn-walk-0.4.41`, passing `todo-checkpoint-death-respawn-walk-0.4.41-r2`.

MOVE-09 remains broader: this does not cover every checkpoint near ladders/platforms, crouching, repeated deaths, preserved held input or the user's unreproduced natural snag. MOVE-01's level-2 blockage is separate. Natural campaign acceptance remains with the human. These technical fixtures do not certify original-game parity or the separately signed production package identity.
