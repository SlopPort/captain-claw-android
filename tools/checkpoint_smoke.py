"""Controlled checkpoint save/reload test; restore original config/save afterwards."""
from pathlib import Path
import subprocess
import time
import xml.etree.ElementTree as ET

PORT = Path(__file__).resolve().parents[1]
REPORT = PORT / 'reports/checkpoint-fixture'
REMOTE = '/sdcard/Android/data/pl.pazur.port/files/'
ADB = ['adb']


def adb(*args, check=True):
    return subprocess.run(ADB + list(args), check=check, capture_output=True, text=True)


def launch():
    adb('shell', 'am', 'force-stop', 'pl.pazur.port')
    adb('shell', 'am', 'start', '-n', 'pl.pazur.port/.LauncherActivity')


def key(code):
    adb('shell', 'input', 'keyevent', str(code))
    time.sleep(0.3)


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    if adb('shell', 'ls', REMOTE+'startup_commands.txt', check=False).returncode == 0:
        raise RuntimeError('Existing startup commands: preserve them before running this test')
    adb('pull', REMOTE+'config.xml', str(REPORT/'config-before.xml'))
    adb('pull', REMOTE+'SAVES.XML', str(REPORT/'saves-before.xml'))
    tree = ET.parse(REPORT/'config-before.xml')
    tree.find('DebugOptions/SkipMenu').text = 'true'
    tree.find('DebugOptions/SkipMenuToLevel').text = '1'
    tree.write(REPORT/'config-test.xml', encoding='utf-8', xml_declaration=True)
    (REPORT/'startup_commands.txt').write_text('teleport 6873 4970\n', encoding='ascii')
    try:
        adb('push', str(REPORT/'config-test.xml'), REMOTE+'config.xml')
        adb('push', str(REPORT/'startup_commands.txt'), REMOTE+'startup_commands.txt')
        launch()
        saved = False
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            time.sleep(1)
            adb('pull', REMOTE+'SAVES.XML', str(REPORT/'saves-after.xml'))
            doc = ET.parse(REPORT/'saves-after.xml')
            if any(n.text == '1' for n in doc.findall('./Level/Checkpoint/CheckpointNumber')):
                saved = True
                break
        if not saved:
            raise RuntimeError('Checkpoint 1 was not saved')
        print('PASS: collision at checkpoint 1 persisted its save', flush=True)
        adb('shell', 'am', 'force-stop', 'pl.pazur.port')
        adb('shell', 'rm', REMOTE+'startup_commands.txt')
        adb('push', str(REPORT/'config-before.xml'), REMOTE+'config.xml')
        launch()
        time.sleep(2)
        key(66)  # Single player
        key(20)  # Load game
        key(66)
        key(66)  # Level 1
        key(20)  # Saved checkpoint 1
        key(66)
        time.sleep(7)
        adb('shell', 'screencap', '-p', REMOTE+'checkpoint-reload.png')
        adb('pull', REMOTE+'checkpoint-reload.png', str(REPORT/'checkpoint-reload.png'))
        log = adb('logcat', '-d', '-t', '1200', '-s', 'SDL/APP', 'libc').stdout
        (REPORT/'reload.log').write_text(log, encoding='utf-8')
        print('Reload sequence complete; inspect checkpoint-reload.png and reload.log', flush=True)
    finally:
        adb('shell', 'am', 'force-stop', 'pl.pazur.port')
        adb('push', str(REPORT/'config-before.xml'), REMOTE+'config.xml')
        adb('push', str(REPORT/'saves-before.xml'), REMOTE+'SAVES.XML')
        adb('shell', 'rm', '-f', REMOTE+'startup_commands.txt')
        print('Original configuration and save restored', flush=True)


if __name__ == '__main__':
    main()
