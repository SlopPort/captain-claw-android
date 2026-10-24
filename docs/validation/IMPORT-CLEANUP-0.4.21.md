# Import staging cleanup

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-22. Controller testing excluded.

## Problem and change

A rejected or process-interrupted extraction could retain a partial `import-staging/CLAW.REZ` until the next import attempt. On low-storage phones this could unnecessarily consume substantial space. Startup and ordinary failed-import handling now recover any live-file transaction first, then reclaim the fixed staging filenames under the existing import lock. Direct native-activity startup uses the same preparation. Active commit recovery deliberately does not discard its staging source. Unknown journal/staging contents are not guessed or recursively removed. Saves and bindings are outside the cleanup allowlist.

A failed rollback keeps its evidence and staging intact: cleanup cannot hide a damaged journal or substitute for successful recovery. Real full-disk behavior, filesystem power-loss durability and the complete document-picker workflow remain separate open checks.

## Exact builds

- ARM64 + ARMv7 APK 0.4.21-dev SHA-256 `cfc586439527bb6e4f063d4d6b7b526aa8fa64e2c9f44d6fccc7e7889c7672cf`.
- Separate emulator x86_64 APK SHA-256 `c396e4b084a9328a508d6c06e92e488a41dfd1879f8a91412f33d5485e9ebd50`.
- Both ARM architectures and ARM64 16 KB ELF load alignment passed package verification. Static alignment is not physical ARM 16 KB runtime coverage.

## Completed evidence

`check_import_transaction.py`: 64 checks of the actual production Java class, preserving old data and save sentinels across interruption boundaries, repeat recovery and injected I/O failures. Added checks reclaim abandoned extraction, retain staging behind malformed journals and refuse unknown staging contents. This is real host filesystem I/O, not an Android full-disk simulation.

`import-cleanup-features-huawei-0.4.21.txt` and `import-cleanup-features-api21-0.4.21.txt`: actual Android parser/filesystem tests passed, including a one-MiB abandoned staging file removed by `GameFiles.prepare` in an isolated startup fixture. No real game data is replaced.

`import-cleanup-process-huawei-0.4.21`: actual app-process death after the third publication, another death during rollback, then startup recovery for empty/partial/full prior installations. Original file sets and save sentinels preserved; staging reclaimed in all three modes. These are small isolated fixtures, not power-loss or SAF coverage.

`compat-huawei-armv7-0.4.21-menu/level`: actual 32-bit engine library mapping, menu, ordinary 100 ms jump, exit pickup, score and level-two loading passed on Huawei Android 10. ARM64 was restored after the trial. `compat-api21-0.4.21-menu/level`: the separate x86_64 package passed corresponding runtime checks on Android 5.0.2, including a 61.4 px short jump (113 ms effective hold, 85 ms takeoff under software emulation). No controller attachment or global Android input; ABI tests use app-local SDL pointer events on the score screen.


## Fresh committed-source build

`clean-source-0.4.21-r2` exported commit `b93af5a97f3a870debd176c90f5034bd97be81a5` (source ZIP SHA-256 `8e6c74aeed7a2cfc39b2f4f3dda5da7e7c17ac136306a782e400465f62844157`) and built fresh native objects for both ARM ABIs in 6m 1s. APK SHA-256 `a61c7a6eb1c3ab8065f4f7d7e92dd49a74a70a6adbfd4e298d139050720bb831`. It uses locally pinned Git dependencies and installed SDK/JDK/Gradle cache, not a fresh-machine download. The different binary hash is not a byte-reproducibility claim. Phone test results against the main `cfc586…` APK are not automatically assigned to this build.

The first `clean-source-0.4.21` attempt selected the host's old 32-bit Java 8 JRE and failed before compilation while reserving the Gradle heap. It remains a failed environment setup attempt. Explicit Android Studio JDK resolved it. The build helper now rejects an old/missing JDK before cloning dependencies; this preflight was checked against that old JRE.

`clean-source-redmi-0.4.21-jump` subsequently passed all six focused-window jump/multitouch cases and direct activity restoration on the exact clean-build `a61c7a…` APK: takeoff 18–20 ms, short rise 72.9–74.6 px, held rise 154.8–155 px. Config/progress restored; the more broadly tested `cfc586…` package was reinstalled with ARM64 afterwards. This runtime check is not menu/all-map coverage for the clean binary.
