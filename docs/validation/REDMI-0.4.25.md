# Redmi 0.4.25 / Android 16

2026-10-23. Checks and document by OpenAI Codex (LLM); device allocated by the
human tester. Initial ADB offline state recovered without restarting the shared
ADB server or changing Huawei USB internet. The cause of the offline state is
unconfirmed; another client using ADB does not itself establish a cause.

## Package and scope

Physical Redmi Note 8, Android 16, ARM64. Upgrade from 0.4.24-dev to 0.4.25-dev
(code 37), debug-signed ARM package SHA-256:
`6175b1b450ca7f46ede0910a884e3608d104e4a86251822aa6c6b4a57d6ca955`.
Original config/save bytes were backed up before installation. No game data,
private device identifiers or raw logs are included in the public repository.

- Parser/save/support and pending-import checks passed.
- Actual PL/EN settings/file screens and Back-button revealability passed.
- Six app-local touch/jump trials passed. Takeoff latency from the app-local
  event was 18–22 ms; this excludes physical touchscreen/controller latency.
  Short tap rise was 76.4 px; 100 ms hold 73.5 px; 250/700/1800 ms holds 155 px.
  Pointer drift caused no unintended attack/fire; long hold caused one jump.
- Focus-loss/resume regression passed: held-axis drift 0 px, fresh input moved
  185.83 px. This uses a virtual SDL pad, not physical Bluetooth testing.
- Actual import publication/recovery process deaths passed for empty, partial
  and full rollback fixtures. Tiny isolated fixtures preserve real game data;
  this is not a full-size SAF/file-picker or storage-exhaustion test.
- Two last-life death/Game Over cycles returned to the menu by app-local touch.
- Android-window touch confirmed the score screen and opened level 2 after a
  labelled level-exit teleport. This is a map-transition fixture.
- Final config/save SHA-256 values match their pre-installation backups exactly.
  No controller-binding file existed before testing; none was introduced.

Private evidence prefixes: `readiness-redmi-0.4.25`, `jump-touch-redmi-0.4.25`,
`lifecycle-redmi-0.4.25`, `import-recovery-redmi-0.4.25`, `game-over-redmi-0.4.25`,
`score-window-redmi-0.4.25`.
The touch-layout screenshot was inspected: controls fit the landscape viewport,
PAD is below the play area centre, and health remains visible.

These are controlled regression checks, not natural campaign traversal,
all-device support, performance acceptance for every level, or 1.0 certification.

## Po polsku

Końcowy APK 0.4.25 przeszedł na Redmi z Androidem 16 kontrole zapisów, importu,
ekranów polskich i angielskich, sześciu wariantów skoku i powrotu do gry.
Zmierzono 18–22 ms od zdarzenia dotykowego w aplikacji do wybicia; nie jest to
pomiar opóźnienia fizycznego ekranu. Dwukrotnie wyszliśmy dotykiem z końca gry. Ekran wyników przyjął dotyk i
otworzył poziom 2 po testowym przeniesieniu do wyjścia. Zapisy i ustawienia
pozostały identyczne z kopiami sprzed instalacji.
Próby przerwania importu używały małych, odizolowanych danych. Naturalną kampanię
sprawdza człowiek; testy fizycznych padów pozostają odłożone.

Font-scale clarification: Redmi checks used its existing system font setting.
The explicit 2.0 font-scale reproduction and fix were verified on the separate
small-screen emulator, as recorded in [readiness](READINESS-0.4.25.md).

## Explicit ARMv7 follow-up / Osobna próba ARMv7

The same APK was installed explicitly with `--abi armeabi-v7a`. Actual process
library mappings confirmed 32-bit execution. Menu, 100 ms held jump, one exit
fixture placement, score and level 2 all passed (`compat-redmi-armv7-0.4.25`).
A finally block reinstalled ARM64; package inspection confirms ARM64 and
0.4.25-dev afterwards. This checks functionality, not 32-bit performance parity.

Ten sam APK uruchomiono jawnie jako 32-bitowy. Potwierdzono bibliotekę w procesie,
menu, skok i techniczne przejście do poziomu 2. Przywrócono ARM64. Nie jest to
dowód jednakowej wydajności obu wariantów.
