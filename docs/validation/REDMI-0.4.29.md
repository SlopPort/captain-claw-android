# Redmi follow-up — 0.4.29

OpenAI Codex (LLM), 2026-10-24. The human explicitly made Redmi available again
for regression checks and removal of this project's obsolete test files. No
Huawei USB/network settings or other projects were changed. No campaign traversal.

Redmi Note 8, Android 16, ARM64 debug 0.4.29-dev/code41, exact APK SHA-256:
`39c004705c2e0ee57cdd6a23e0ebbc5d3ca35ab981581d766568b7431c67bdbc`.
The in-place update from 0.4.27 retained config, saves and language byte for byte.
Main data REZ remained identical to the verified installation archive. These
results extend the [Huawei regression batch](USER-REGRESSIONS-0.4.29.md);
they do not retroactively change that batch's device allocation.

| Check | Result | Limit |
| --- | --- | --- |
| Raw Android Start pause/resume | Three cycles passed | App-local virtual/raw routing; no physical Bluetooth/USB test |
| Catnip acquisition, expiry, reacquisition | All passed; music-switch timer recorded 0/0/0 ms, PCM present, no in-game preparation | Millisecond timer resolution, not literally zero latency or an all-frame FPS guarantee; console applies bonus |
| Directions on text-only Game Over, then touch return | Up/Down and return passed, no prior focus assertion | Technical last-life fixture |
| Death with Catnip and six rapid touches | One cycle passed, no native/Java fatal log | Not every lifecycle/touch combination |
| Melee after real Soldier hit, hero below 32 px step | Both sides passed: queued/consumed tap, sword contact, Soldier HP10 ->0, hero HP90 ->80 | Isolated active AI, correct facing before fixture; no healing/protection during observation; not natural stairs or original parity certification |

Original config/progress were restored and verified after fixtures. The final
cleanup also checked config/save/language against pre-update bytes. No signed
release, ARMv7 or emulator retest was performed in this batch.

## Bounded cleanup

Removed only the obsolete Download installation ZIP and two old test screenshots,
**61,442,833 bytes of known files**, after copying them to ignored private reports
on the computer and verifying their hashes. The ZIP passed its integrity check;
its complete REZ matched the game's active REZ. No commercial data was published.
The test companion `pl.pazur.port.test` was then uninstalled. Main package
`pl.pazur.port`, installed data, engine support, progress and settings were kept.
No broad Downloads/cache deletion, recursive shared-storage cleanup, save removal
or other-project uninstallation occurred. Free-space changes also include APK
replacement and unrelated normal Android activity; known removed file sizes are
not a promise of an identical filesystem free-space delta.

The test companion must be reinstalled before future instrumentation. It is not
needed to play. The main game remains ready for the human's campaign testing.
There is no active fixture on Redmi. Confirm allocation again if another task
starts using it; no further phone interaction is needed for this completed batch.

Private report prefixes: redmi-maintenance-2026-10-24, pause-powerup-redmi-0.4.29,
game-over-pad-focus-redmi-0.4.29, melee-recovery-redmi-0.4.29-{side},
game-over-powerup-rapid-redmi-0.4.29. Backups and raw evidence stay outside Git.
