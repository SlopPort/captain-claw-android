# Marrow encounter

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Experimental implementation by OpenAI Codex (LLM), 2026-10-21/22.

Inherited OpenClaw parrot update and bridge activation methods were empty. The new implementation follows the sequence described in [Claw Recluse game help](https://captainclaw.net/en/game.html): three parrot hits open the bridge; five successful sword hits trigger carrying Marrow across. This is new code, not recovered original game logic. Original WWD positions, images, animations and recordings remain in the user's game archive, outside source/APK distribution.

The boss retains inherited 150 HP, melee damage/parries and defeat/gem handling. Contact cooldowns, flight, carry and bridge timings are implementation choices awaiting comparison with original gameplay. During carry the boss body is disabled; patrol boundaries are recalculated at landing. Bridge physics mutations occur during updates outside locked contact callbacks. Reset and negative phase gates need dedicated regressions.

`tools/marrow_smoke.py` uses ordinary sword/jump input with isolated saves, teleports and player protection. It does not edit boss health or inject phase/completion events. This is not natural campaign traversal.

Evidence in ignored local reports:

- `marrow-arena-observe1`: real boss warp, arena and parrot flight observed.
- `marrow-contact-fight1/2-short-jump`: bridge opened, sword phase did not complete within the fixture's attempts.
- `marrow-contact-fight3-trace`: stopped for timing diagnosis; short jump landed before the next USB/mailbox attack command. Original config/saves explicitly restored.
- `marrow-contact-fight4-medium-jump`: both carry transitions observed, boss reached 20 HP; interrupted before completion. No complete-pass claim. Original config/saves restored before run 5.
- `marrow-contact-fight5-complete`: first phase/carry passed; second phase reached 80 HP. Stopped deliberately by closing only the game to replace the USB-timed fixture. The script confirmed restoration of original config/saves. Not a complete pass.
- `marrow-contact-fight6-scheduled`: two full carry phases passed; stopped during the last phase to add ordinary forward movement during the jump. The stationary fixture could remain outside sword reach at the ledge. Saves/config restored.
- `marrow-contact-fight7-forward-jump`: all three parrot/bridge/sword phases, two carries, actual boss defeat and a real boss gem were observed. The script failed afterward because the dead boss actor had already disappeared before its next position query. Not a full transition pass. The query now accepts an exact boss-defeat log when the actor is absent.

The diagnostic `combatjumpattack` schedules ordinary jump, direction and sword key events on the game thread, avoiding USB latency. It never calls damage/phase functions. No boss hitbox, sword reach or health values were changed to make the fixture pass.

`marrow-contact-fight8-transition` passed: three real parrot/bridge/sword phases, two carries, boss defeat, real gem collection, score confirmation and level 11 loading. Original config/saves were restored. Fixtures remain isolated level start, teleports and player protection; no health edits. Dedicated death/reset, negative phase-gate and original-game timing comparisons remain open.

`marrow-death-reset-0.4.12` subsequently passed the death/reset gate: after the first carry and boss health 100, protection was disabled and Claw placed in the existing arena pit. A real death reduced lives from three to two, restarted the encounter and restored Marrow to 150 HP on the initial side. Three new parrot hits reopened the bridge, and a complete three-phase rematch, boss gem and level 11 transition passed. No health edits or synthetic death/reset events were used. Protection was restored for the rematch; this remains a controlled test, not natural traversal. Negative phase gates and original timing/balance parity remain open.

This encounter report does not declare a finished version 1.0.
