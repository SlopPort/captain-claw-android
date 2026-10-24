# Import on a full filesystem

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-23. Production `ImportTransaction.java` from
0.4.24-dev was compiled unchanged together with
`tools/java/pl/pazur/port/ImportFullDiskChecks.java`: JDK 21 `--release 8`,
Android build-tools 35.0.0 D8 `--min-api 21`. No APK or production code changed.

Actual runtime: task-owned Android 5.0.2/API 21 x86_64 emulator, root-shell
`app_process`, dedicated **8 MiB tmpfs** at `/data/local/tmp/pazur-import-space`.
The mount and 8192k limit were verified; the final test checks them before writing.
Only that filesystem was filled, with a 16 MiB hard write bound. No phone-wide
filling, phone operation or ADB-server restart. Fixtures use dummy old/staged
1 MiB REZ-shaped files, small other required files and a separate save sentinel.

| Case | Actual result |
| --- | --- |
| Full disk before backup | Real ENOSPC refused commit. Old files/save verified byte for byte. Releasing the filler allowed startup cleanup, preserving originals. |
| Full disk during rollback | After first-file publication, fill tmpfs and deliberately interrupt. Real ENOSPC blocked recovery. Backup/save remained intact. Releasing space and calling startup recovery twice restored all originals and removed staging/journal. |

Both cases passed with the final test source. Existing 64 host boundary checks
also passed. Ignored local evidence: `reports/full-disk-api21-backup-final.txt`,
`full-disk-api21-rollback-final.txt`, `full-disk-mount.txt`, `full-disk-classes/`.
Two initial software-only boots failed to become usable; hardware acceleration
resolved emulator setup. These are environment failures, not app failures.

Recovery requires free space for its restore copy. It keeps the backup and blocks
startup rather than accepting mixed data. Existing launcher messages in PL/EN
already ask to free storage and retry. This is production transaction coverage
on Android, **not** SAF/document-picker UX, large real-data import, normal app-UID
permissions, power-loss durability or universal filesystem coverage. The emulator
and mount were closed afterward. A no-mount negative probe produced only Android's
`Killed` output; retain that failure, **do not count it as a verified guard test**.

### Reproduction outline

Use only a task-owned rooted emulator, with both fixed paths absent before setup.
Compile the two Java sources to Java 8 class files, convert to DEX with D8, and
package `classes.dex` in a JAR. Verify the selected emulator belongs to your task.
Create the fixed empty directory, mount tmpfs with `size=8m,mode=0700`, and check
`/proc/mounts`. Push the test JAR to `/data/local/tmp/pazur-import-checks.jar`.
Run each mode in the root shell, explicitly addressing that emulator:

```text
CLASSPATH=/data/local/tmp/pazur-import-checks.jar app_process /system/bin pl.pazur.port.ImportFullDiskChecks backup
CLASSPATH=/data/local/tmp/pazur-import-checks.jar app_process /system/bin pl.pazur.port.ImportFullDiskChecks rollback
```

Require both PASS lines; Android 5 remote exit status alone is insufficient.
Unmount the fixed tmpfs, remove its empty directory and the test JAR, then close
only your emulator. Never fill a phone or substitute its real game-data path.
