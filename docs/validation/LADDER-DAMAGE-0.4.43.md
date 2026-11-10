# Ladder damage, jump-away and death: debug43

OpenAI Codex (LLM), 2026-11-10. Huawei P9 Lite, LineageOS Android 10, ARM64 debug43, SHA-256 `dfedd91134113cacf5f43dbdbe17e6575b0848a43710922eeaea86d777e35b8a`. No production behavior or APK changed for this test.

The previously missing MOVE-05 cases used an isolated production ladder and an active Soldier. Setup removed other enemies and initialized HP100/ammo99. Subsequent damage was real, including Soldier musket projectiles. No healing, protection or direct damage calls were used during observation. Inputs were app-local SDL events, not physical controls or a natural route.

## Completed observations

- **Recovery and jump-away:** the hero was attached at Y1018.4. After a further actual Soldier hit, held Up resumed climbing to Y907.0. Jump-plus-Right produced an actual `animation=jump`, `jumping=1` trace, then detached and landed at X200084.7, Y1043.9 with no climbing state retained. This does not claim that hurt itself preserves attachment: the trace also records a brief drop/recovery near the ladder bottom.
- **Death while attached:** earlier damage could drop the hero to the floor. After natural health loss reached 5 HP, a short Up input reattached him before the next real projectile. The last pre-fatal sample, **60 ms** before the 5-to-0 event, showed `ground=0 ladder=1 climb=1`. Normal death/fade/respawn then completed. The new hero stood at X689.0, Y4734.9 with no ladder/climbing state; fresh Right moved him to X722.4. This is sampled pre-fatal attachment evidence, not a new health or death callback.

Both sessions restored fresh configuration/progress, retained the installed APK hash and found no target or unattributed fatal crash. Private evidence: `todo-ladder-damage-0.4.43-20261110-r2/results.json` and child traces. `tools/ladder_damage_smoke.py` reproduces this bounded setup; the fatal setup currently waits for naturally observed 5 HP and is not a difficulty matrix.

## Retained insufficient-evidence attempt

The initial recovery case passed. Its death case correctly failed the intended-state assertion: fatal damage occurred **on the floor**, so it could not prove death while climbing. It restored user files and is retained in `todo-ladder-damage-0.4.43-20261110`. The correction changed the test setup, not gameplay, by reattaching after ordinary health loss. A yearless timestamp-parser warning was also removed from the helper.

Together with [first-ladder/bottom/cap evidence](LADDER-EDGES-0.4.41.md) and [neutral/held-release pause evidence](MOVEMENT-LIFECYCLE-0.4.42.md), these observations cover the named bounded technical cases of MOVE-05. Natural leafy-cap/transfer behavior remains MOVE-04; broader lifecycle and physical-input acceptance remain their own tasks. Original hurt-retention policy is not certified, and these completed cases should not be restarted after documentation-only or unrelated audio changes.
