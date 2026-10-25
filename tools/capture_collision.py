"""Capture a transient debug collision state without enabling combat fixtures.

OpenAI Codex (LLM). Select an authorized device with ANDROID_SERIAL. The game
must be running unpaused; output and screenshot stay in ignored local reports.
Never upload the screenshot/map data or device-specific diagnostics by default.
"""
import argparse
import os
from pathlib import Path
import subprocess
import time
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True, help='New local report folder name')
    args = parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):
        raise RuntimeError('Select the allocated device with ANDROID_SERIAL')
    port = Path(__file__).resolve().parents[1]
    report = (port / 'reports' / args.report).resolve()
    if not report.is_relative_to((port / 'reports').resolve()):
        raise ValueError('Report must remain inside the local reports directory')
    report.mkdir(parents=True, exist_ok=False)
    remote = '/sdcard/Android/data/pl.pazur.port/files/'

    def adb(*values):
        return subprocess.check_output(['adb', *values], stderr=subprocess.PIPE)

    for name in ('collision-snapshot.request', 'collision-snapshot.txt'):
        if b'present' in adb('shell', 'if [ -e '+remote+name+' ]; then echo present; fi'):
            raise RuntimeError('Existing capture file: '+name)
    ticket = uuid.uuid4().hex
    request = report / 'request.txt'
    request.write_text(ticket, encoding='ascii')
    adb('push', str(request), remote+'collision-snapshot.request')
    try:
        deadline = time.monotonic()+10
        while time.monotonic() < deadline:
            # A single read may race the writer; require its explicit terminator.
            result = subprocess.run(['adb', 'exec-out', 'cat', remote+'collision-snapshot.txt'], capture_output=True)
            if result.returncode == 0 and result.stdout.endswith(b'end\n'):
                (report/'collision.txt').write_bytes(result.stdout)
                (report/'screen.png').write_bytes(adb('exec-out', 'screencap', '-p'))
                adb('shell', 'rm', '-f', remote+'collision-snapshot.txt')
                print('Captured read-only collision state; no gameplay input or save edits.')
                return
            time.sleep(.1)
        raise RuntimeError('No snapshot: requires an unpaused debug build 0.4.34 or later')
    finally:
        # Remove only our still-pending request, never another capture owner.
        pending = subprocess.run(['adb', 'exec-out', 'cat', remote+'collision-snapshot.request'], capture_output=True)
        if pending.stdout.decode('ascii', errors='replace').strip() == ticket:
            adb('shell', 'rm', '-f', remote+'collision-snapshot.request')


if __name__ == '__main__':
    main()
