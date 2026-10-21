# Step-by-step installation

[Polska instrukcja](INSTALL-PL.md)

This is a test version. From 0.4.8, you need an Android phone, this port's APK and **CLAW.REZ from your own copy of Claw**. A prepared `game-data.zip` also works. Do not rename or unpack these files.

## Easiest: APK + CLAW.REZ

1. Open your own PC game folder. Copy `CLAW.REZ` and the APK to your phone's Download folder.
2. Install the APK using the steps below, then open Kapitan Pazur.
3. Tap **Wybierz dane gry** (Select game data), choose **CLAW.REZ** and wait. The game starts automatically. No Python or ZIP preparation is needed.
4. You only import once.

The direct REZ workflow is inspired by Claw Web (Arthur Boss and contributors); Android implementation and validation are local adaptations. Original game artwork comes from your REZ. If a Polish installation has additional loose `Assets`, the ZIP workflow below also includes those files. Direct REZ uses only the archive contents.

**CrazyHook / a 168-byte REZ:** this is a placeholder, not the complete game. Prepare the ZIP from the loose `Assets` folder using the instructions below.

## Save backups and vibration

In the game, tap **PAD**, then **Save backups and vibration**. Export writes XML to a location you choose. Import accepts this port's XML (not Windows saves or Claw Web JSON); quit through the game menu and launch again to apply it. The previous save remains as `SAVES.before-import.xml` in app storage. Vibration is optional and off by default. Controller rumble support depends on its mode and Android driver.

## I already have the APK and prepared data package

1. Copy both files to your phone's **Download** folder. For USB transfer, unlock the phone, select **File transfer**, open the phone storage on your computer and copy the files into Download.
2. Open **Files** on the phone, open **Downloads**, then tap the file ending in `.apk`.
3. If Android blocks installation, follow the displayed Settings link and allow this Files application to install apps. Return and tap **Install**. Labels vary between Android versions. You can turn this permission off afterwards.
4. Open **Kapitan Pazur**. Tap **Wybierz dane gry** (Select game data).
5. In the system file picker, open **Downloads** and select `game-data.zip`. Wait for the import; the game starts automatically.
6. Future launches do not require importing the data again.

You do not need USB debugging, ADB, Android Studio or a GitHub account. To update, install the newer APK over the existing application. Its signing key must match. A signature conflict does not mean your phone is damaged. Uninstalling removes application data and game saves: back up saves first.

## I own the PC game but do not have the ZIP

In 0.4.8 you can select the REZ directly as described above. The ZIP workflow below remains available for older APKs, installations with additional loose assets and reproducible packaging.

**Easier Windows option:** install Python 3.11+ with Tcl/Tk and Git, extract the sources, then double-click `Prepare-game-data.cmd`. Select EN and choose `CLAW.REZ`. The window shows the resulting ZIP location. The first run needs internet. This new wizard still needs a clean-computer usability test; use the terminal steps below if it does not open.

1. Download and extract the port's source project. Install Python 3.11 or newer and Git. On Windows, enable Python's **Add to PATH** option.
2. Open a terminal in the extracted project folder containing README.md. On Windows, open that folder in File Explorer, type `powershell` in its address bar and press Enter.
3. Run `python tools/bootstrap.py` and wait. Internet access is required to download open-source dependencies. This does not download the commercial game.
4. Run `python tools/pack_assets.py --game-root "C:\Games\Claw"`. Replace the example path with your own game folder containing `CLAW.REZ`. Keep the quotation marks, particularly for paths containing spaces.
5. Find the resulting `build/game-data.zip` inside the project folder. Copy it to the phone and follow the steps above. The original PC installation is not modified.

You do not need to build an APK if you already have the installer. [Building from source](BUILDING.md) is a separate developer workflow.

## Troubleshooting

- **Cannot find the ZIP:** open Download in the system picker; select the archive itself.
- **Invalid or incomplete package:** create it with the port's packaging tool. Zipping the entire PC game folder does not produce the required structure.
- **App not installed:** record the exact message, Android version and APK filename. Do not delete your saves without a backup.
- **Crashes or slow gameplay:** report the phone model, Android version, level and action immediately before the problem. Android 5+ is the build minimum, not confirmed compatibility with every device.

The port's code is open source. Original Claw game data has separate copyright and is excluded from public source distributions. Owning files does not automatically grant permission to redistribute them. See [credits and licenses](../NOTICE.md).
