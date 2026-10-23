# Captain Claw for Android

[Polski](README.md) · **[Install step by step](docs/INSTALL-EN.md)**

A native Android adaptation of [OpenClaw](https://github.com/pjasicek/OpenClaw), using game data supplied from the user's own copy of Claw. C++/SDL, ARM64 and ARMv7, minimum build API 21. Compatibility with every Android version or device is not established.

Current development version: **0.4.24-dev**. A final 1.0 release remains in preparation. The bilingual **[Road to 1.0](docs/ROADMAP-1.0.md)** separates completed work and release gates. Recent changes protect checkpoint/next-level saves and prepare direct Android activity restoration. See [0.4.18 persistence and clean-source build evidence](docs/validation/ATOMIC-PROGRESS-0.4.18.md), [0.4.17 startup](docs/validation/STARTUP-0.4.17.md) and [twenty-minute dense-scene observation](docs/validation/SUSTAINED-0.4.15.md). Controlled [campaign evidence](docs/validation/CAMPAIGN-1.0.md) is not a natural playthrough.

**Language:** before data import, or under **PAD → Language / Język**, choose Polski or English. Android screens, menu text and our help support both languages; in-game labels change after restarting the game. Voices, backgrounds and original score-screen artwork depend on your game data. [PL/EN menus and 0.4.16 evidence](docs/validation/MENU-LANGUAGE-0.4.16.md).

Select your own complete **CLAW.REZ** directly, or use a prepared game-data.zip. PAD → Save backups and vibration provides save export/import and optional haptics. These workflows/designs are inspired by Claw Web, Arthur Boss and contributors; see [credits](NOTICE.md) and the [validation report](docs/validation/PORT-0.4.8.md). A 168-byte placeholder REZ with loose Assets still requires ZIP preparation.

Install a prepared APK, then select your complete `CLAW.REZ` or `game-data.zip` in the application. You do not need development tools to install a prepared APK and data package. The [installation guide](docs/INSTALL-EN.md) also explains how to prepare data from your own PC installation. Commercial game data is excluded from public sources.

## What changed

The adaptation adds an Android build and data importer, touch stick and action buttons, touch jump handling, a wider view without stretching sprites, audio configuration, level 14 components and an Omar encounter/finale. It also fixes several ordinary enemy health and collision issues. Gamepad support is being validated separately. Existing gameplay and the engine come from OpenClaw; this is not a new engine written from scratch. See the detailed [upstream difference table](docs/UPSTREAM-DIFF.md) (Polish).

## Transparency and current limits

All adaptation work in this development session — code, documentation, investigation and automated test execution — was performed by an LLM coding agent (OpenAI Codex), guided by a human's requirements and feedback. The human supplied hardware and a game installation. Upstream authors retain their attribution. See bilingual [development notes and known issues](docs/DEVELOPMENT-NOTES.md).

Controlled tests covered 45 ordinary enemy variants, 1,415 initial placements across 14 levels, 16 projectile enemy types from both sides and 13 collision cases. These are not a completed natural playthrough or proof of exact Windows balance. The finale is staged in the engine rather than reproducing the original movie.

Current campaign tests use a Huawei P9 Lite with Android 10 and 2 GB RAM; earlier builds also ran on a Redmi Note 8 with Android 16. After optimization many scenes approach 60 FPS, but a dense level-nine scene measured approximately 57–59 FPS. Sustained 60 FPS throughout the campaign is not established. These are scene-specific measurements, not performance guarantees. Minimum API 21 and packaged ABIs are build settings, not proof of runtime compatibility; see the [compatibility matrix](docs/validation/ANDROID-COMPATIBILITY.md). Bluetooth and USB transport tests must be reported individually.

Campaign work remains in progress. Complete controlled Aquatis and Marrow encounters and their next-level transitions passed with explicitly documented teleports/player protection. This is not natural traversal of all fourteen maps or a ready 1.0 release. See the [release gates](docs/validation/CAMPAIGN-1.0.md) and [attack-audio audit](docs/validation/ATTACK-AUDIO.md).

## Controls

Tap **PAD** at the bottom centre to bind physical buttons or triggers to gameplay/menu actions. Changes save automatically; Restore defaults is available. [Detailed instructions, English and Polish](docs/CONTROLLER.md).

Touch: left stick moves, climbs and crouches. Jump is at the bottom right, attack beside it and shoot above. A short tap produces a useful low jump; holding increases height. BRON changes weapon; PAUZA opens the menu.

Default Android key names: BUTTON_A for jump, BUTTON_X for melee, BUTTON_B for shooting, BUTTON_Y for weapon change, BUTTON_START for pause. Left stick/D-pad moves. Buttons and triggers can be assigned in PAD; labels depend on the controller mode. Do not assume printed labels match Android's mapping.

## Build from source

Install Git, Python 3.11+, JDK 17+, Android SDK/Build Tools 35, NDK 27.2.12479018 and CMake 3.22.1. Set JAVA_HOME and ANDROID_HOME. Then run:

```sh
python tools/bootstrap.py
./gradlew '-Pabis=arm64-v8a,armeabi-v7a' :app:assembleDebug
```

On Windows use `tools/build.ps1 -Abis 'arm64-v8a,armeabi-v7a'`. Output: `app/build/outputs/apk/debug/app-debug.apk`. Dependencies are pinned in sources.lock.json. Bootstrap downloads open-source dependencies and applies the engine patch; it does not download the commercial game.

The adaptation and OpenClaw use GPL-3.0; see [LICENSE.txt](LICENSE.txt). Dependencies retain their own licenses and attribution in [NOTICE.md](NOTICE.md). The source license does not grant rights to redistribute Claw's commercial graphics, sound, music, maps or videos. No expiry of those rights is assumed.

New: [touch audio sliders and physical Huawei PL/EN checks](docs/validation/MENU-AUDIO-0.4.19.md), [180 controlled combat fixtures](docs/validation/VERTICAL-45-0.4.18.md), [archived rejected experiments](experiments/README.md).

[0.4.21: abandoned-import cleanup](docs/validation/IMPORT-CLEANUP-0.4.21.md) and [physical Redmi Android 16 evidence](docs/validation/REDMI-0.4.21.md).

[Detailed English build instructions](docs/BUILDING.en.md).

[0.4.22: reject malformed configuration before import](docs/validation/CONFIG-IMPORT-0.4.22.md). [Redmi: twenty-minute dense-scene observation on 0.4.21](docs/validation/SUSTAINED-REDMI-0.4.21.md), harmonic 59.998 FPS with an occasional 65 ms frame. This does not close natural-campaign or the accepted Huawei performance gate.

[0.4.23: powder-keg crash fix](docs/validation/POWDER-KEG-0.4.23.md). Redmi Android 16 + Huawei Android 10: PASS. Natural campaign: in progress; not complete.

[0.4.24: real moving-platform boarding observation](docs/validation/PLATFORM-0.4.24.md). Controlled observations passed on Redmi and Huawei; [the natural campaign remains incomplete](docs/validation/NATURAL-CAMPAIGN-0.4.23.md).

[Natural checkpoint and normal menu reload](docs/validation/NATURAL-CHECKPOINT-0.4.24.md). Level 1 / checkpoint 1 reached; full campaign remains incomplete.

For contributors: [current handoff](docs/HANDOFF.md), [contributing](CONTRIBUTING.en.md), [publication checks](docs/PUBLISHING.md).
