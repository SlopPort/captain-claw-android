# Recoverable game-data import

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-22. Introduced in 0.4.15-dev. This closes a source-review risk with measured process-interruption coverage, not every installation/release gate.


The previous importer replaced five files sequentially without rollback. The new implementation first preserves existing files, writes a journal, then publishes the prepared set. On the next launch, unfinished work is recovered before checking whether the game is ready. Recovery runs off the UI thread. Import/recovery operations are serialized within the process.

Interruption before the commit point restores the previous set, including empty or partial installations. Interruption after commit retains the complete new set. Backups survive until recovery finishes, so recovery itself can be interrupted and repeated. A malformed journal blocks startup and keeps backups rather than guessing. Saves, bindings and language preferences are outside the replacement allowlist.

Replacing existing data needs additional free space for the old set. Running out of storage can interrupt preparation/recovery; do not manually delete the backups. Free storage and restart the app.

## Evidence and limits

- `python tools/check_import_transaction.py`: 61 cases against the actual production Java class. Interruptions after every backup, journal publication, each live-file publication and commit; interruptions after every restoration; empty/partial/full prior sets; injected I/O exceptions; corrupt journal rejection; repeated recovery and unchanged save sentinels. Desktop Windows required the guarded replacement fallback where rename cannot overwrite a file.
- `tools/import_recovery_smoke.py`: actual instrumented app-process death after publishing the third file, then another death during restoration, followed by a fresh-process verification. Empty/partial/full original sets pass on Huawei Android 10. Tiny fixtures live only in `import-transaction-test`, never in the real game-data root. The initial report `import-process-recovery-0.4.15` used APK SHA-256 `d85c612e16d30552057f7a71a3637f04d149ea94954baea0106f4d32fed48fe2`, before the later launcher picker-result deferral; later exact-candidate results must be recorded separately.
- `import-startup-touch-0.4.15`: launcher startup and six focused game-window jump cases pass after the picker-result deferral. Takeoff 19–25 ms, short rise 73–74 px, held rise about 155 px; these are injected window-event timings, not physical screen latency. Multitouch, action drift/cancellation and focus transitions also pass. Original configuration/progress was restored.

The transaction tests do not validate a novice's file-picker workflow, large real-data replacement, actual full-disk behavior or sudden power-loss durability. File contents are synced; directory-metadata durability still depends on the filesystem. This is a recoverable multi-file transaction, not an atomic live-directory switch: the native engine must not start until recovery succeeds. The launcher enforces this order. A recreated launcher's document-picker result is deferred until its storage check finishes; a full picker/recreation interaction remains to be exercised.

Final 0.4.15 candidate SHA-256 `36719447575c7b5f2bd49d9da8dad835f2d22068a465bfe45d9ce7d9776947d3`: `import-process-recovery-0.4.15-final-r2` passes all three actual process-death/rollback modes after the launcher deferral. `import-features-0.4.15.txt` passes existing real Android save/parser/support checks. `import-language-0.4.15` passes PL/EN settings, selection/recreation and native English preview; its screenshot was visually inspected. An earlier final-run attempt failed before fixture creation because AGP rewrote the first instrumentation registration; the separate test manifest now preserves a runner slot before additional checks. That report is retained as a harness failure, not an engine failure or passing recovery trial.

## 0.4.21 follow-up

[Staging cleanup and repeated actual process-death tests](IMPORT-CLEANUP-0.4.21.md) add safe reclamation of abandoned extraction files. Historical 61-case results above remain historical; the expanded production-class suite has 64 cases.
