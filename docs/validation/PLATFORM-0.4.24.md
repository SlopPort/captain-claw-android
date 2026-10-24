# Moving-platform observation — 0.4.24

OpenAI Codex (LLM). This update adds opt-in diagnostic observation and ordinary
input scheduling; it does not change platform movement, jump physics, health,
damage or collision rules. The powder-keg fix from 0.4.23 remains present.

APK SHA-256: `583ec1d605527ba812e7da3da510a52dc4e08a2cc94f84c4733592051f2cc0a2`.
Both ARM variants built. Physical observations below used ARM64.

| Observation | Device | Takeoff | Rise | Result |
| --- | --- | --- | --- | --- |
| Real horizontal platform, ordinary 650 ms right / 600 ms jump | Redmi, Android 16 | 30 ms | 155 px | Boarded and carried |
| Same platform, wait for observed leftward return | Redmi, Android 16 | 35 ms | 155 px | Boarded and carried |
| Same observed return window | Huawei, Android 10 | 30 ms | 155 px | Boarded and carried |

Evidence is local in ignored `reports/platform-redmi-0.4.24-a`,
`reports/platform-redmi-0.4.24-sync`, `reports/platform-huawei-0.4.24-sync`.
Raw traces show hero support (`ground=1`), stable y around 4394, and changing x
with the platform after the directional input ends. No fatal signal occurred;
original configuration/save backups were restored after each observation.

**These are controlled fixtures, not natural campaign completion.** Setup removes
enemies/projectiles, initializes hero HP100/ammo99 on a remote arena floor, then
places the hero at the real ledge (3446,4351). The real local terrain and moving
platform remain unchanged. No health/ammo/position changes occur during the
observed jump. No shots are fired. The synchronization loop reads real traces
and waits; it neither freezes nor repositions the platform.

The read-only trace also exposed a vertical elevator at x4259, with map-defined
y limits 4395..4858. This revises the earlier suspicion of a lower dead end:
its route still requires natural boarding verification, but the elevator must
be considered before calling the area a trap. Inspection alone is not proof of
natural escape. The earlier natural attempts remain documented in
[NATURAL-CAMPAIGN-0.4.23.md](NATURAL-CAMPAIGN-0.4.23.md).

Diagnostics now allow a plain simultaneous jump/move without the previously
scheduled sword swing and an ordinary Shift input to cycle weapons. These are
app-local SDL keyboard events, not controller tests or direct ammo edits.
The new platform trace uses weak references and reads positions/velocities;
it does not query a newly created physics body's bounds.

Open: natural boarding with enemies active, the lower elevator route, all 14
levels and final ending. No new 55/60 FPS claim or complete Android matrix is
made from these observations.
