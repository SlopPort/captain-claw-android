# Native-entry preparation and progress safety

OpenAI Codex (LLM), 2026-10-22. Development work; results must identify the exact APK. Controller testing is excluded.

## Changes

Android can restore GameActivity without opening LauncherActivity first. Preparation now also runs from SDLActivity.getArguments(), which the pinned SDL version calls on SDLMain's worker thread before nativeRunMain. This path recovers interrupted data imports under the shared import lock, checks required data, installs the matching engine support bundle, writes the selected native language and applies pending progress before native code reads files. Existing launcher preparation remains a convenient early check; it is no longer the sole gate.

Preparation errors return a native startup-aborted sentinel before SDL/game initialization and open a localized Retry/Close screen with access to save tools. No native assert is used to report preparation failure. File-operation details can still contain English system messages. No device storage/network settings are changed.

Initial progress creation now validates the packaged defaults and writes through a synced temporary file plus rename. A process interruption cannot expose a partially written initial SAVES.XML. A leftover temporary file can be replaced on retry; existing progress is never reset automatically, including a damaged existing file. This is not a promise to repair arbitrary corrupt native saves or guarantee filesystem metadata persistence after power loss.

A pending save import can survive process death after publication but before pending-file removal. Replaying that same canonical payload now keeps the original pre-import backup, instead of overwriting it with the imported progress. This addresses replay of the same transaction; distinct new imports still take a new backup.

## Validation status

ARM64 + ARMv7 candidate SHA-256 `04940bc2d0a7b5a3ae5033cf68feb9785ab9896b7dbbb6cafce352c95aec0a1f`, version 0.4.17-dev (29), installed on Huawei Android 10. `startup-features-0.4.17.txt` passed the actual Android parser/filesystem fixtures for missing startup files, engine support/language preparation, initial save creation/retry, preservation of an existing empty save, and pending-import replay retaining the backup. Tiny REZ filename/size fixtures in this test are not native commercial-data parsing coverage.

`startup-direct-0.4.17` started GameActivity directly in the instrumentation process, bypassing LauncherActivity, then passed six focused-window jump, multitouch, focus and viewport checks. Measured takeoff 19–21 ms; short jump 73.5–74.1 px, held jump up to 155 px. Config/saves were restored. This exercises the direct entry path, not a complete real-system low-memory restoration scenario.

`startup-import-process-0.4.17` passed intentional process death after publication and again during recovery, for empty/partial/full original file sets, on this same installed APK. Its tiny isolated fixtures do not replace real game data. ABI/library alignment verification also passed. Native preparation-error UI and actual low-storage conditions remain to be exercised; no final campaign/60 FPS claim follows from these checks.

## Polski

Przygotowanie danych obejmuje również bezpośrednie wznowienie ekranu gry przez Androida. Pierwszy zapis jest tworzony atomowo, a powtórzenie przerwanego importu zapisu zachowuje kopię wcześniejszego postępu. Nie resetujemy po cichu istniejących zapisów. Wyniki uruchomienia trzeba dopisać po sprawdzeniu konkretnego APK; dokument sam nie potwierdza ukończenia testów.
