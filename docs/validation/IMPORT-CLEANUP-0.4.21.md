# Import staging cleanup / Sprzątanie roboczych danych importu

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

## Polski

Nieudany import mógł zostawić dużą kopię roboczą danych aż do kolejnej próby importu. Teraz aplikacja sprząta ją po poprawnym odzyskaniu danych, również po ponownym uruchomieniu i bezpośrednim wznowieniu ekranu gry. Nie usuwa zapisów gracza ani nie zgaduje zawartości uszkodzonego dziennika. Próby na Huawei i emulatorze Androida 5 przeszły, podobnie jak 64 próby granic operacji i rzeczywiste ubijanie procesu w trzech wariantach wcześniejszej instalacji. Nadal trzeba sprawdzić rzeczywisty brak miejsca i pełną obsługę selektora plików.
