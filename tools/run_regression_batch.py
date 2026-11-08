"""Run selected existing device fixtures sequentially with exact-build evidence.

OpenAI Codex (LLM). Requires an explicitly allocated ANDROID_SERIAL and an
idle game. This is technical fixture coverage, never a natural playthrough.
Child tools own their temporary configuration; this runner verifies restoration
and stops on any failure. It never overwrites saves to repair a failed child.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from android_package import installed_apk_sha256

PORT = Path(__file__).resolve().parents[1]
REMOTE = '/sdcard/Android/data/pl.pazur.port/files/'
CASES = {
    'floor-seams': ('floor_seam_smoke.py', '--expect-fixed'),
    'wall-jump': ('wall_jump_smoke.py',),
    'forest': ('forest_motion_smoke.py',),
    'ladder-pause': ('ladder_pause_smoke.py',),
    'ladder-held-pause': ('ladder_held_pause_smoke.py',),
    'checkpoint-reload-walk': ('checkpoint_local_smoke.py', '--walk-after-reload'),
    'checkpoint-respawn-walk': ('checkpoint_local_smoke.py', '--walk-after-reload', '--ordinary-death'),
    'rope': ('rope_attached_smoke.py',),
    'melee-recovery': ('melee_recovery_smoke.py',),
    'audio-low': ('attack_audio_smoke.py', '--sound-volume', '10'),
    'audio-high': ('attack_audio_smoke.py', '--sound-volume', '100'),
    'touch-jump': ('window_touch_regression.py', '--scenario', 'jump'),
    'game-over': ('window_touch_regression.py', '--scenario', 'game-over'),
    'score': ('window_touch_regression.py', '--scenario', 'score'),
    'menus': ('menu_language_smoke.py', '--audio-sliders'),
    'ambient': ('ambient_audio_smoke.py',),
    'pause-bonus': ('pause_powerup_smoke.py',),
    'lifecycle': ('lifecycle_smoke.py',),
    'gameplay-options': ('gameplay_options_smoke.py',),
    'save-errors': ('save_error_messages_smoke.py',),
    'siren-interruption': ('siren_interruption_smoke.py',),
    'flight-recorder': ('check_flight_recorder.py',),
    'import-recovery': ('import_recovery_smoke.py',),
    'late-save-activity': ('late_save_activity_smoke.py',),
    'cyclic-platforms': ('gameplay_perf_smoke.py', '--level', '1', '--cyclic-pegs'),
    # Twenty-minute stability evidence, not a passing 55 FPS claim. A missed
    # FPS target alone is optional under the human's 2026-11-08 scope decision.
    'stability-heavy': ('gameplay_perf_smoke.py', '--level', '9', '--seconds', '1200',
                        '--scene', '11027', '5500', '--protect-player', '--observe',
                        '--quiet-diagnostics', '--expect-logical-size', '853', '480'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--cases', nargs='+', choices=CASES, required=True)
    args = parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):
        parser.error('Select an explicitly allocated device with ANDROID_SERIAL')
    report = (PORT / 'reports' / args.report).resolve()
    if not report.is_relative_to((PORT / 'reports').resolve()):
        parser.error('Report must stay under reports')
    report.mkdir(parents=True, exist_ok=False)

    def adb(*command):
        return subprocess.check_output(['adb', *command], timeout=30)

    def snapshot():
        return {name: hashlib.sha256(adb('exec-out', 'cat', REMOTE + name)).hexdigest()
                for name in ('config.xml', 'SAVES.XML')}

    for name in ('combat-command.txt', 'combat-command.tmp', 'combat-response.txt'):
        occupied = adb('shell', 'if [ -e ' + REMOTE + name + ' ]; then echo occupied; fi')
        if b'occupied' in occupied:
            raise RuntimeError('Another diagnostic owner may be active: ' + name)
    original = snapshot()
    # Save an emergency copy, but never automatically replace potentially newer data.
    for name in original:
        data = adb('exec-out', 'cat', REMOTE + name)
        if hashlib.sha256(data).hexdigest() != original[name]:
            raise RuntimeError('User files changed during baseline capture; stop')
        (report / name).write_bytes(data)
    apk = installed_apk_sha256()
    result = dict(passed=False, apk_sha256=apk, original_file_hashes=original,
                  natural_playthrough=False, physical_controller_test=False,
                  fixture_scope='Existing child assertions; see child reports for protection, AI and geometry',
                  rows=[])
    try:
        for case in args.cases:
            script, *options = CASES[case]
            child_report = args.report + '-' + case
            command = [sys.executable, str(PORT / 'tools' / script), '--report', child_report, *options]
            started = time.monotonic()
            print('START ' + case, flush=True)
            with (report / (case + '-driver.log')).open('wb') as output:
                child = subprocess.run(command, cwd=PORT, stdout=output, stderr=subprocess.STDOUT)
            restored = snapshot() == original
            same_apk = installed_apk_sha256() == apk
            row = dict(case=case, exit_code=child.returncode,
                       elapsed_seconds=round(time.monotonic() - started, 1),
                       files_restored=restored, apk_unchanged=same_apk)
            result['rows'].append(row)
            (report / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
            print(json.dumps(row), flush=True)
            if child.returncode or not restored or not same_apk:
                raise RuntimeError('Stopped after failed child/build/restoration check: ' + case)
        result['passed'] = True
    finally:
        (report / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
