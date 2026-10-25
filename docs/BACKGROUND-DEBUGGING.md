# Local background gameplay recorder

Implemented by OpenAI Codex (LLM), under anonymous human direction. Available in debug 0.4.35 and later. This is a diagnostic recorder, not a breakpoint debugger or a fix for the open level 2 blockage.

## For the player

Play normally. The debug app records movement history automatically while the game runs; no cable or computer is needed for recording. If Claw blocks again, tell the maintainer promptly. Leave the game running without a jump or restart when possible, so a live collision snapshot can supplement the history. A restarted game can overwrite older rolling reports, and later candidates eventually replace the two saved candidate reports.

Nothing is uploaded automatically. The recorder does not request Android permissions, read other apps, record the microphone, take screenshots or collect account/device identifiers. Reports contain level coordinates, game input and collision metadata. Keep raw reports private until reviewed; do not publish proprietary map dumps or gameplay media as part of a source commit.

## What it keeps

- Up to 600 samples, taken no more often than every 100 ms during physics updates: approximately the latest minute of active gameplay at normal frame rates. Pauses and low frame rates can stretch the wall-clock interval.
- Hero position and velocity; ground/ladder/climb/fall/jump flags and foot-contact count; current animation; seven game-action input bits; physics timestep and Box2D step time.
- Up to eight contact records per sample, prioritizing physical contacts before sensors. Total/saved counts expose truncation. Contact records include enabled/touching flags, sensor status, normal orientation and the other fixture's bounds/type.
- Two rotating rolling files, normally refreshed every five seconds, and two rotating candidate files. A debug worker writes files; the game thread only samples/copies bounded data. Each file is written separately and renamed on completion. There is one pending job of each kind, so slow storage cannot grow an unlimited work queue; a newer pending report replaces an older pending report if the worker falls behind.

A candidate is generated after roughly 750 ms of horizontal action input plus a running animation with near-zero displacement/velocity, grounded and not climbing. Candidates are limited to one every 15 seconds. **Pushing an ordinary wall intentionally also qualifies.** These reports identify something to inspect; they are not automatic proof of a bug.

The recorder does not capture every frame or every short input pulse. It does not trace audio playback, Java/import failures, all enemies or every CPU subsystem. A process crash can lose the latest unflushed samples; power-loss durability is not guaranteed. It runs inside the game, not as an Android service after the game closes. A write/thread creation failure does not deliberately stop gameplay. Storage-write failure recovery has separate limits in the validation report.

## Retrieve a report

Only an allocated phone may be accessed. Set ANDROID_SERIAL in the current process; never commit its value or restart the shared ADB server. Then, from the repository root:

```sh
python tools/collect_game_debug.py --report UNIQUE-LOCAL-REPORT
```

This copies existing complete recorder files into ignored `reports/` without restarting the app, injecting input or changing phone files. Headers distinguish sessions; the four files may span different sessions. There is no automatic upload. On an unpaused debug build, supplement it with `tools/capture_collision.py` for current fixture bounds.

Phone files are `flight-rolling-0.txt`, `flight-rolling-1.txt`, `flight-event-0.txt` and `flight-event-1.txt` in the app's own data directory. There are four completed-report destinations and four fixed temporary pathnames. Interrupted writes may leave temporary files; reused slots overwrite them, so filename count remains bounded. Existing reports survive app termination until their slots are replaced.

For an A/B test, a developer may create `flight-recorder-off` in that same directory **before starting the game process**. Remove only a marker you own and restart to re-enable. This does not change game configuration or saves. The recorder implementation is compiled out under NDEBUG; the public signed 0.4.32 test APK does not contain it.

## Format

The first line identifies format/build, session and reason. `S` data rows contain tick, level, X/Y, VX/VY, flags, foot contacts, action mask, timestep, physics milliseconds, animation, total contacts and saved contacts. Associated `C` rows follow each sample. Header rows label the columns; `end` marks a complete file.

Flags: ground=1, ladder=2, climb=4, falling=8, jumping=16. Action mask: left=1, right=2, up=4, down=8, jump=16, attack=32, fire=64. These are observed logical SDL action events, not arbitrary keyboard text or raw controller identifiers. Contact normals use Box2D fixture A→B orientation; `hero_is_a` tells which side belongs to Claw.

[Physical validation and limits](validation/FLIGHT-RECORDER-0.4.35.md) · [Open platform report](validation/LEVEL2-PLATFORM-0.4.34.md).
