# Captain Claw for Android

An Android adaptation of [OpenClaw](https://github.com/pjasicek/OpenClaw), using **game files from your own PC copy of Claw**. This project does not include or download the commercial game.

**Development version, not a finished 1.0 release.** A complete natural playthrough has not been verified. A human tester owns campaign testing; automated checks use separately documented scenarios.

## Install and play

You need this port's **APK** (the Android installer) and your own complete **`CLAW.REZ`** (the PC game's data file). A prepared `game-data.zip` also works.

1. Download **`captain-claw-android-0.4.31-test.apk`** from [the test release](https://github.com/SlopPort/captain-claw-android/releases/tag/v0.4.31-test), under **Assets**, or [build one](docs/BUILDING.en.md). GitHub's **Source code (zip)** is source code, not an Android installer or game data. A finished 1.0 APK is not announced here.
2. Copy the APK and `CLAW.REZ` to **Downloads** on your phone.
3. Open the APK in the phone's **Files** app and install it.
4. Open **Kapitan Pazur**, tap **Choose game data**, and select `CLAW.REZ`. Wait for the import; the game starts automatically.

**[Full installation guide and troubleshooting](docs/INSTALL-EN.md).** A tiny placeholder `CLAW.REZ` with a separate `Assets` folder requires the guide's ZIP preparation steps.

Updates must use the same signing key as your installed app. **Uninstalling can delete saves.** Export a backup before uninstalling or changing to an APK with a different signature.

## Controls and language

- The left touch stick moves, climbs and crouches. The right buttons jump, attack and shoot. Hold jump longer to jump higher.
- In the Polish interface, **PAUZA** pauses and **BRON** changes weapon.
- **PAD** opens controller bindings and Android settings. Default Android A/X/B/Y actions are jump/melee/shoot/weapon; Start pauses. Printed letters may differ by controller mode. See the [controller guide](docs/CONTROLLER.md).
- Choose **Language / Język → English** before importing data, or later under **PAD**. Restart the game to apply in-game menu labels. Voices and original artwork depend on your own files: selecting English does not translate Polish audio. See [language limits](docs/GAME-LANGUAGE.md).
- **PAD → Save backups and vibration** exports progress to a file you choose. Backups use this port's XML format, not Windows saves or Claw Web JSON.

## What this adaptation adds

Android builds and data import, touch controls, controller bindings, save export/import, optional vibration, a wider view without stretched sprites, MIDI playback support, gameplay fixes, and additional level 14/Omar/finale work. The finale is staged in the engine rather than reproducing the original movie.

OpenClaw supplies the existing engine and much of the gameplay. See the [upstream comparison](docs/UPSTREAM-DIFF.md) for the adaptation's contributions and [NOTICE](NOTICE.md) for OpenClaw, Claw Web and dependency credits. Engine changes are patches to pinned dependency revisions.

## Test status and limitations

Reports identify the exact APK and setup. Results for older builds are not automatic proof for the current source.

- [0.4.29 regressions](docs/validation/USER-REGRESSIONS-0.4.29.md): pause, Catnip pickup audio, Game Over input and a short melee tap during hurt; [Redmi follow-up](docs/validation/REDMI-0.4.29.md).
- [Current Game Over screen](docs/GAME-OVER-UI.md) and [original-executable behavior investigation](docs/ORIGINAL-BEHAVIOR-REA.md): what was observed, changed and still remains uncertain.
- [Android compatibility matrix](docs/validation/ANDROID-COMPATIBILITY.md): tested devices, architectures and remaining gaps. Android 5/API 21 is the build minimum, not a guarantee for every phone.
- [Road to 1.0](docs/ROADMAP-1.0.md): remaining release requirements. Controlled map starts, combat fixtures and boss checks do not prove that all fourteen levels can be completed naturally.

The low-end target is Huawei P9 Lite, Android 10, 2 GB RAM. Many measured scenes approach 60 FPS; sustained 60 FPS throughout the campaign is not established. Measurements apply to the scenes and builds named in each report. Controller Bluetooth and USB modes require individual testing.

To report a problem, give the APK version, phone model, Android version, level, your action and the result. Do not attach game archives, signing keys or personal information. See [testing](docs/TESTING.md) for technical checks.

## Build or contribute

Read the [build guide](docs/BUILDING.en.md), [contribution guide](CONTRIBUTING.en.md) and [current handoff](docs/HANDOFF.md). Dependencies are pinned in `sources.lock.json`. Bootstrap downloads open-source dependencies and applies patches, not the commercial game.

With the development tools configured:

```sh
python tools/bootstrap.py
./gradlew '-Pabis=arm64-v8a,armeabi-v7a' :app:assembleDebug
```

On Windows use `./gradlew.bat`. The installer is `app/build/outputs/apk/debug/app-debug.apk`.

## Authorship and rights

All adaptation work in this development session — code, documentation, investigation and automated test execution — was performed by **OpenAI Codex, an LLM coding agent**, guided by an anonymous human's requirements and feedback. The human supplied hardware, a game installation and playtesting feedback. Upstream work remains credited to its authors.

The adaptation and OpenClaw use GPL-3.0; see [LICENSE.txt](LICENSE.txt) and [NOTICE.md](NOTICE.md) for dependency licenses and attribution. This does not grant rights to redistribute Claw's commercial game files. Copyright expiry is not assumed. Public sources exclude game archives, extracted game assets, private test data and signing credentials.

[REA](https://github.com/morluto/rea) is an investigation tool used during development, not a game dependency. Other research references are recorded in the development documentation.
