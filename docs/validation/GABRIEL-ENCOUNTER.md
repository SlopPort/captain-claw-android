# Gabriel encounter

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Audit and test tooling by OpenAI Codex (LLM), 2026-10-22.

The inherited encounter uses a sword-contact button to raise the cannon. Gabriel chooses the cannon action through his ordinary AI. A raised-cannon shot subtracts 25 HP through inherited engine code; the test must not invoke that callback or edit health. Four such shots should defeat the 100 HP boss and create the existing gem.

The cannon's inherited vertical animation frame callback is empty: unlike its horizontal shot, the vertical shot currently has no visible cannonball projectile and applies its damage when `Fire()` starts. This is an inherited presentation/timing limitation, not established original-game parity. Do not change the mechanic before validating ordinary button/cannon operation.

`tools/gabriel_smoke.py` uses isolated saves, player protection, actual actor positions, setup teleports and ordinary sword events. The `campaignposition` setup fixture resets remaining fall velocity; the normal console teleport preserves it, so repeated attempts could arrive far below the button before the attack frame. It does not change button collision, activate the cannon, spawn projectiles or edit boss health.

- `gabriel-button-fight1`: failed expected-button-sound assertion. The first test incorrectly recognized a GabrielPirate death as a Gabriel death because of a shared name prefix. Fixed to match the exact boss name; no pass claim.
- `gabriel-button-fight2-live-position`: confirmed actual button position, but the fixture retained terminal fall speed and missed it. Stopped by closing only the game; original config/saves restored.
- `gabriel-button-fight3-reset-velocity`: reset velocity but separate USB commands still allowed the player to fall past the button before the sword event. Stopped; config/saves restored.
- `gabriel-button-fight4-trace`: eight-attempt diagnostic failed. A higher start landed on the upper platform, above the hanging button.
- `gabriel-button-fight5-near-trace`: eight-attempt diagnostic failed. Near-button trace showed the player at Y 4773 approximately 0.12 seconds after setup, but below it before the delayed attack frame. The new fixture queues the same ordinary sword key event together with positioning; it does not directly activate the button.

Original recordings and images remain in the user's game data. The open-source distribution contains only code, XML references and evidence descriptions.

`gabriel-button-fight6-atomic-input` passed: real sword contacts with the button, accepted button effect, four inherited 25 HP cannon hits, exact boss defeat, real gem collection, score and level 9 loading. Observed health: 100, 75, 50, 25. No direct boss-health/cannon callback edits or synthetic completion events. Positioning/protection remain explicit fixtures, so this does not establish natural traversal or original-game fidelity.
