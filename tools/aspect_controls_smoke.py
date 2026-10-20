"""Exercise real touch events at 16:9 and 4:3, restoring device size and user files."""
from pathlib import Path
import json
import re
import subprocess
import sys

PORT = Path(__file__).resolve().parents[1]
REPORT = PORT / 'reports/aspect-controls-0.4.1'
REMOTE = '/sdcard/Android/data/pl.pazur.port/files/'


def adb(*args):
    return subprocess.run(['adb', *args], check=True,
                          capture_output=True, text=True).stdout


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    original_size = adb('shell', 'wm', 'size')
    override = re.search(r'Override size: (\d+x\d+)', original_size)
    adb('shell', 'am', 'force-stop', 'pl.pazur.port')
    for name in ['config.xml', 'SAVES.XML']:
        adb('pull', REMOTE+name, str(REPORT/name))
    results = []
    try:
        for size, label, expected in [('1080x1920', '16-9', 'logical=853x480'),
                                      ('1080x1440', '4-3', 'logical=640x480')]:
            adb('shell', 'am', 'force-stop', 'pl.pazur.port')
            adb('shell', 'wm', 'size', size)
            adb('logcat', '-c')
            output = adb('shell', 'am', 'instrument', '-w', '-r',
                         'pl.pazur.port.test/pl.pazur.port.ControlSmokeTest')
            (REPORT/(label+'-instrumentation.log')).write_text(output, encoding='utf-8')
            assert 'INSTRUMENTATION_CODE: 0' in output, output
            log = adb('logcat', '-d', '-s', 'SDL/APP', 'libc', 'AndroidRuntime')
            log_file = REPORT/(label+'-native.log')
            log_file.write_text(log, encoding='utf-8')
            assert expected in log, log
            assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log
            subprocess.run([sys.executable, '-B', str(PORT/'tools/verify_controls.py'),
                            str(log_file)], check=True)
            for name in ['control-multitouch', 'control-pause', 'control-focus-resume']:
                adb('pull', REMOTE+name+'.png', str(REPORT/(label+'-'+name+'.png')))
            results.append({'aspect': label, 'expected_viewport': expected, 'passed': True})
            print(json.dumps(results[-1]), flush=True)
    finally:
        adb('shell', 'am', 'force-stop', 'pl.pazur.port')
        adb('shell', 'wm', 'size', override.group(1) if override else 'reset')
        for name in ['config.xml', 'SAVES.XML']:
            adb('push', str(REPORT/name), REMOTE+name)
        (REPORT/'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
        assert adb('shell', 'wm', 'size').strip() == original_size.strip()
        print('Device size, config and saves restored', flush=True)


if __name__ == '__main__':
    main()
