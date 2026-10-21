# Captain Claw for Android

[Polski](README.md) · **[Install step by step](docs/INSTALL-EN.md)**

A native Android adaptation of [OpenClaw](https://github.com/pjasicek/OpenClaw), using game data supplied from the user's own copy of Claw. C++/SDL, ARM64 and ARMv7, minimum build API 21. Compatibility with every Android version or device is not established.

Current version: 0.4.10-dev. Touch now exits Game Over; see the bilingual [gameplay audit](docs/validation/BUG-AUDIT-2026-10-21.md). SDL draw batching improves measured Huawei map starts without reducing image quality; see the [FPS results and limits](docs/validation/FPS-0.4.9.md). Select your own complete **CLAW.REZ** directly, or use a prepared game-data.zip. PAD → Save backups and vibration provides save export/import and optional haptics. These workflows/designs are inspired by Claw Web, Arthur Boss and contributors; see [credits](NOTICE.md) and the [validation report](docs/validation/PORT-0.4.8.md), including remaining issues. A 168-byte placeholder REZ with loose Assets still requires ZIP preparation.

Install a prepared APK, then select your complete `CLAW.REZ` or `game-data.zip` in the application. You do not need development tools to install a prepared APK and data package. The [installation guide](docs/INSTALL-EN.md) also explains how to prepare data from your own PC installation. Commercial game data is excluded from public sources.

## What changed

The adaptation adds an Android build and data importer, touch stick and action buttons, touch jump handling, a wider view without stretching sprites, audio configuration, level 14 components and an Omar encounter/finale. It also fixes several ordinary enemy health and collision issues. Gamepad support is being validated separately. Existing gameplay and the engine come from OpenClaw; this is not a new engine written from scratch. See the detailed [upstream difference table](docs/UPSTREAM-DIFF.md) (Polish).

## Transparency and current limits

All adaptation work in this development session — code, documentation, investigation and automated test execution — was performed by an LLM coding agent (OpenAI Codex), guided by a human's requirements and feedback. The human supplied hardware and a game installation. Upstream authors retain their attribution. See bilingual [development notes and known issues](docs/DEVELOPMENT-NOTES.md).

Controlled tests covered 45 ordinary enemy variants, 1,415 initial placements across 14 levels, 16 projectile enemy types from both sides and 13 collision cases. These are not a completed natural playthrough or proof of exact Windows balance. The finale is staged in the engine rather than reproducing the original movie.

Previous hardware measurements used a Redmi Note 8 with Android 16: approximately 60 FPS in warmed level 1 and 54 FPS in level 13. Version 0.4.8 also ran on Huawei P9 Lite with 2 GB RAM and Android 10: many map starts approach 60 FPS, levels 8/9/13 are lower and level 6 varies substantially. These are scene-specific observations, not performance guarantees; see the [measurement limits](docs/validation/PORT-0.4.8.md). Bluetooth and USB input use SDL; real transport tests must be reported individually.

## Controls

Tap **PAD** at the bottom centre to bind physical buttons or triggers to gameplay/menu actions. Changes save automatically; Restore defaults is available. [Detailed instructions, English and Polish](docs/CONTROLLER.md).

Touch: left stick moves, climbs and crouches. Jump is at the bottom right, attack beside it and shoot above. A short tap produces a useful low jump; holding increases height. BRON changes weapon; PAUZA opens the menu.

Default Android key names: BUTTON_A for jump, BUTTON_X for melee, BUTTON_B for shooting, BUTTON_Y for weapon change, BUTTON_START for pause. Left stick/D-pad moves. Buttons and triggers can be assigned in PAD; labels depend on the controller mode. Do not assume printed labels match Android's mapping.

## Build from source

Install Git, Python 3.11+, JDK, Android SDK/Build Tools 35, NDK 27.2.12479018 and CMake 3.22.1. Set JAVA_HOME and ANDROID_HOME. Then run:

```sh
python tools/bootstrap.py
./gradlew '-Pabis=arm64-v8a,armeabi-v7a' :app:assembleDebug
```

On Windows use `tools/build.ps1 -Abis 'arm64-v8a,armeabi-v7a'`. Output: `app/build/outputs/apk/debug/app-debug.apk`. Dependencies are pinned in sources.lock.json. Bootstrap downloads open-source dependencies and applies the engine patch; it does not download the commercial game.

The adaptation and OpenClaw use GPL-3.0; see [LICENSE.txt](LICENSE.txt). Dependencies retain their own licenses and attribution in [NOTICE.md](NOTICE.md). The source license does not grant rights to redistribute Claw's commercial graphics, sound, music, maps or videos. No expiry of those rights is assumed.
