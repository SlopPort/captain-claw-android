# Build from source

[Polski](BUILDING.md). To play, use an APK and the [installation guide](INSTALL-EN.md); compiling is only necessary if you want to build or modify the app yourself.

## Required tools

Install Git, Python 3.11 or newer, a **full JDK 17 or newer**, and Android Studio's SDK Manager components: Android SDK Platform 35, Build Tools 35.0.0, NDK 27.2.12479018 and CMake 3.22.1. This project uses Gradle 8.10.2 through its included wrapper. A separate Gradle installation is unnecessary. Android Studio's `jbr` folder can supply the JDK. An old Java 8/JRE installation is insufficient.

Open a terminal in the source folder containing `gradlew.bat` and `sources.lock.json`. Set `JAVA_HOME` to the JDK folder and `ANDROID_HOME` to the Android SDK folder. Example Windows PowerShell paths for a default Android Studio installation:

```powershell
$env:JAVA_HOME='C:/Program Files/Android/Android Studio/jbr'
$env:ANDROID_HOME="$env:LOCALAPPDATA/Android/Sdk"
python tools/bootstrap.py
./gradlew.bat '-Pabis=arm64-v8a,armeabi-v7a' :app:assembleDebug
```

On Linux/macOS, use `./gradlew` instead of `./gradlew.bat`; set the environment paths for your installation. If Python is named `python3`, use that command and set the `PYTHON` environment variable to it. On Windows, `tools/build.ps1 -Abis 'arm64-v8a,armeabi-v7a'` also invokes the build with default Android Studio paths when those environment variables are unset.

The first setup needs internet for pinned dependencies, Gradle plugins and any missing Android tools. Bootstrap applies this project's OpenClaw and SDL patches to the exact dependency revisions. The Gradle wrapper checks the distribution SHA-256. Build preparation generates support XML/art and obtains the pinned FreePats music bank; it does not download commercial Claw game data.

The resulting file is `app/build/outputs/apk/debug/app-debug.apk`. It supports ARM64 and ARMv7 and is signed with a local SDK debug key. It is a development package, not a production-key-signed release. Keep a consistent signing key for updates: Android rejects an update signed with a different key. Do not uninstall an existing app merely to bypass that failure; uninstalling can remove its data. No signing key belongs in the public source archive.

## Your own game data

After building, follow the player installation guide and select your own full CLAW.REZ. If your installation instead has a small placeholder REZ and a loose Assets folder, run:

```sh
python tools/pack_assets.py --game-root '/path/to/your/own/installation'
```

This creates `build/game-data.zip` for the app's file picker without modifying the source game installation. Commercial assets are not included in this source project or its APK.

## Validation and its limits

```sh
python tools/check_repository.py
python tools/check_patches.py
python tools/verify_apk.py app/build/outputs/apk/debug/app-debug.apk
```

The APK verifier checks both ARM libraries and static ARM64 ELF load alignment for 16 KB pages. Also use SDK Build Tools `zipalign -c -P 16 4` and `apksigner verify`. Static checks do not prove runtime support on every device.

`python tools/clean_source_build.py --revision HEAD --report clean-source-new` exports the selected committed Git revision and builds fresh native objects in a new report folder. It uses local pinned dependency repositories, installed SDK/JDK and the existing Gradle cache. It does not copy uncommitted changes or prove setup on a completely fresh machine, online dependency availability or byte-identical APK reproduction. Each report name must be new. Set the JDK variables first; the tool rejects missing/old Java before cloning dependencies.

For device tests, install Android platform-tools, enable USB debugging and put `adb` on PATH. With several devices connected, explicitly select `ANDROID_SERIAL`. Read [test scope](TESTING.md) before running a script: some fixtures replace test configuration/progress temporarily, and old scripts have different input methods. Current compatibility evidence is linked from the [English README](../README.en.md). Minimum API 21 is a package setting, not a guarantee for every Android 5+ phone.

Source changes, documentation and automated testing in this adaptation were performed by OpenAI Codex (LLM), guided by human requirements and feedback. Upstream code retains its authorship and licenses.
