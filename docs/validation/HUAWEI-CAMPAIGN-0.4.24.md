# Huawei campaign continuation and log recovery

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-23. Device: Huawei P9 Lite, Android 10,
2 GB RAM. Redmi was reserved for another task and was not operated in this run.
The USB tether and shared ADB server were not intentionally restarted.
APK: 0.4.24-dev, SHA-256
`583ec1d605527ba812e7da3da510a52dc4e08a2cc94f84c4733592051f2cc0a2`.
No game physics, collision, combat parameters or game assets changed in this work.

The continuation loads the exact game-written level-one checkpoint from the
[earlier natural run](NATURAL-CHECKPOINT-0.4.24.md) through the normal menu.
Its recorded resources are preserved: HP100, zero spare lives, pistol6, magic2,
dynamite3. The Huawei user's own files are backed up separately. Subsequent play
uses ordinary app-local keys and read-only observations, with no teleport,
resource replenishment, protection or added world geometry.

Observed natural progress:

- Crumbling pegs and both horizontal carrier/ladder transfers passed on Huawei.
- The real vertical elevator and upper ladder passed after a longer held jump.
  An earlier short-jump attempt missed and safely returned to the lower cap.
- Leaving the upper cap promptly, jumping onto the ledge and crouching allowed
  an ordinary pistol shot to defeat the Soldier; the hero retained HP30.
- The next flag ledge and ladder were reached. The two cyclic pegs at x10608
  and x10740 passed without catnip. Their pickups raised HP30 to HP60.
- The next group was not cleared. One peg was reached, then a later off-phase
  landing fell to the lower floor. The Officer there was defeated normally.
  Subsequent ordinary pickups raised health to HP85. Recovery attempts from
  the real trigger elevator are retained, including missed landings.

This is partial route coverage, not a level-one clear, full campaign pass,
minimum-FPS result or release 1.0. Local evidence is in the ignored report
`natural-campaign-huawei-0.4.24-resume1`; no map dumps or commercial data are
included in Git.

The logcat client stopped while the game kept running. The cause of the stream
interruption was not established. Several observer timeouts therefore had no
fresh samples; they are not evidence of failed jumps or a game crash. The stale
results and later fresh-log failures remain separate in the local evidence.

The test owner now detects a terminated **own logcat client**, reconnects from
its last recorded timestamp and appends evidence. It does not restart the ADB
server, game, USB connection or another device. A separate owned-reader helper
supports already running older owners and has an explicit stop marker.
An actual interrupted-client trial on Huawei recovered fresh native status
with the same game process. This improves test reliability; it is not an APK
performance or gameplay fix. Timestamp overlap can repeat the last log line;
observers must continue to consume sample ticks only once.


## Final tool verification

The owner-idle integration test (`log-recovery-huawei-0.4.24-owner`) also passed:
its own logcat client was terminated, the idle loop reconnected, and an ordinary
status-query step completed with the same game process. No ADB-server restart
was requested. After cleanup, configuration and save pulled from Huawei were
byte-identical both to the integration-test backups and to the natural-run
original backups (`restoration.json`). The natural campaign remains incomplete.
