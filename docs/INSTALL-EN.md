# Step-by-step installation

[Polska instrukcja](INSTALL-PL.md)

This is a test version. You need an Android phone, this port's APK and a `game-data.zip` package prepared from your own copy of Claw. The APK installs the application. The ZIP contains game data. Do not unpack the ZIP on your phone.

## I already have the APK and prepared data package

1. Copy both files to your phone's **Download** folder. For USB transfer, unlock the phone, select **File transfer**, open the phone storage on your computer and copy the files into Download.
2. Open **Files** on the phone, open **Downloads**, then tap the file ending in `.apk`.
3. If Android blocks installation, follow the displayed Settings link and allow this Files application to install apps. Return and tap **Install**. Labels vary between Android versions. You can turn this permission off afterwards.
4. Open **Kapitan Pazur**. Tap **Wybierz dane gry** (Select game data).
5. In the system file picker, open **Downloads** and select `game-data.zip`. Wait for the import; the game starts automatically.
6. Future launches do not require importing the data again.

You do not need USB debugging, ADB, Android Studio or a GitHub account. To update, install the newer APK over the existing application. Its signing key must match. A signature conflict does not mean your phone is damaged. Uninstalling removes application data and game saves: back up saves first.

## I own the PC game but do not have the ZIP

Renaming `CLAW.REZ` to ZIP will not work. The package also needs support files used by the port. Preparing it currently requires a computer; importing a bare REZ file is not implemented yet.

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
