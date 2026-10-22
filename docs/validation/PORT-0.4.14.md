# Live viewport checkpoint 0.4.14

OpenAI Codex (LLM), 2026-10-22. Development version, not final 1.0. [Remaining gates, Polish and English](../ROADMAP-1.0.md).

## Corrected window handling

Android initially supplied different surfaces before immersive bars disappeared: examples include 1800x1020 and 1800x1080. The engine selected logical widths 847 and 800, then only logged the later real 1920x1080 resize. This left different visible world widths across launches. It also made performance runs with different widths unsuitable for direct comparison.

The Android resize handler now updates renderer logical size and camera width from the actual window aspect, retaining logical height 480 and uniform scaling. It does not resize the Android window recursively, lower output resolution or change physics. Touch state is released across a changed coordinate space. Menu/score rendering continues to center its 640x480 content inside the wider view.

## Actual ARM candidate

`dist/kapitan-pazur-0.4.14-dev.apk`, versionCode 26, SHA-256 `8e2c6dc4157fc27f4aad42e072dae39b632f1cdd80218bf9d7892e7d928ee536`. ARM64 and ARMv7 built; ELF ARM64 16 KB alignment, ZIP alignment and signature checks passed. This is not actual 16 KB runtime proof.

Physical Huawei Android 10 results on this exact candidate:

- `viewport-window-jump-0.4.14`: six app-window touch cases passed, plus multitouch, sword/shoot buttons, finger cancellation, pause/resume and own-app background/return. Takeoff measurements were 19–21 ms; 10/100 ms taps rose about 74 px and held jumps about 155 px, with one takeoff even for an 1800 ms hold. These timings begin at injected Android window events, not the physical touch sensor. Original progress/configuration was restored.
- The same test observed actual 1920x1080 → 1800x1020 → 1920x1080 events across focus changes, with logical width updating 853 → 847 → 853. No device display override or global input was used.
- `viewport-window-score-0.4.14` passed an actual level-one end pickup, Android window taps on the score screen and level-two load. Setup teleport is explicit, not natural traversal.
- `viewport-window-game-over-0.4.14` passed actual last-life death, Game Over and return to the main menu through an app-window tap.
- `campaign-start-viewport-0.4.14-level1..14`: all fourteen maps loaded, stayed alive for the declared three-second observation and produced screenshots/memory records at settled logical 853x480. Isolated saves were used; no teleport/protection/HP edits. This is startup/render coverage, not traversal.

Android 5 emulator native/menu/100 ms jump/exit-to-level-two also passed in `compat-api21-viewport-0.4.14-menu/level`. Separate x86_64 test APK SHA-256: `6758d0c95bd7f30abd08f769a3bc04851621c7ae883902253f71ac4948d8a911`; observed viewport 853x480, jump rise 57.9 px, effective hold 107 ms and takeoff 73 ms in emulation. No physical Android-5 device or original-game fidelity is established.

## Same-APK ABI comparison

The ARM APK above was installed explicitly as ARM64, then ARMv7, then ARM64 again on the Huawei. Each run sampled 45 seconds at level-nine position (11027, 5500), using declared teleport/protection and the same settled 853x480 viewport. Reports: `abi-perf-0.4.14-arm64-a`, `abi-perf-0.4.14-armv7`, `abi-perf-0.4.14-arm64-b`. Mean FPS after the initial batch was respectively 58.200 / 51.614 / 58.775. Battery temperature after each run was 33.0 C; this is not CPU temperature. Point PSS was respectively 174624 / 168586 / 172927 KiB, not peak memory.

ARMv7 was slower here and saved only about 4–6 MiB at those measurement points. It remains a compatibility option, not a recommended performance setting for this Huawei. These results do not establish an ABI rule for every phone or scene. The ARMv7 native/menu/jump/exit checks also passed in `compat-armv7-viewport-0.4.14-menu/level`. ARM64 was restored and verified afterward, with original configuration/saves restored.

## Android 15: unresolved jump failure

The separate x86_64 APK above passed native initialization/menu on the API-35 emulator in `compat-api35-viewport-0.4.14-menu`. Its level trial **failed** the declared 600 ms jump: only 25.8 px rise, 702 ms effective hold and 701 ms input-to-takeoff. Frames around the jump took roughly 90–543 ms. No viewport change occurred during that jump. Large update intervals remain an open engine/input investigation; software emulation neither proves nor excludes the same problem on physical devices.

The separately declared `compat-api35-viewport-exit-only-0.4.14-menu/level` passed initialization and technical exit/score/level-two loading **without testing a jump** (`jump_verified: false`). This does not override the failed jump. Its older JSON retained the unused default requested hold value; the harness now emits null when jump coverage is skipped. Both reports retain their actual scope. The task emulator was closed; phone USB internet was not changed. No physical Android-15 or 16 KB runtime claim is made.

## Rejected render-cache experiment

An opt-in same-image invalidation experiment was measured in the earlier diagnostic APK `cda2705573ad57b1dddc38bcad9c4b26d7b2ff2525a72f07495201f630e101d7`. At identical settled 853x480, the off/on/off runs had post-initial-batch mean FPS 59.413 / 58.825 / 58.763. Only 11511 of 1268919 image-set calls were skipped in the enabled run (about 0.9%). This did not establish a useful improvement; the experiment and its command were removed from 0.4.14. Raw reports and code snapshots remain locally.

An earlier incomplete run used width 800 for its off case, and its on command was not acknowledged during startup. It is not valid comparative evidence. Performance tools now wait for the simulation-ready marker and can require a declared settled viewport; they record subsequent viewport events and the installed APK hash. The resize fix is a correctness change, not a claimed cache speedup. Steady 60 FPS throughout the campaign remains open.
