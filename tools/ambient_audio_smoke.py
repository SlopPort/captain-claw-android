"""Measure real local-ambient sensor/mixer gain and muted-entry behavior.

OpenAI Codex (LLM). Uses a synthetic sensor with a user-supplied stock sound,
not a natural route. No microphone, audio recording or commercial attachment.
Each session restores user config/progress; scalar mixer statistics stay private.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from gamepad_quit_smoke import PORT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    apk = installed_apk_sha256()
    rows = []
    for muted in (False, True):
        with CampaignSession(args.report + ('-muted' if muted else '-gain')) as session:
            session.command('combatstage -1 80 0')
            session.command('audioquiet')
            session.command('audiooptions ' + ('0' if muted else '1') + ' 0 10 0')
            session.command('audiotrace 1')
            start = len(session.logs())
            session.command('ambientfixture')
            session.wait('Pazur ambient gain:', after=start)
            setup = re.search(r'Pazur ambient gain: intrinsic=(\d+) chunk=(\d+) channel=(\d+) paused=(\d+)', session.logs()[start:])
            assert setup, 'No production ambient mixer state'
            intrinsic, chunk, channel, paused = map(int, setup.groups())
            assert intrinsic == 100 and chunk == 128, 'Master gain leaked into cached chunk'
            assert channel == (0 if muted else 12) and paused == int(muted), setup.groups()

            def measure(label):
                begin = len(session.logs())
                session.command('audiomeasure ' + label)
                time.sleep(.8)
                session.command('audioreport')
                found = re.search(r'audio mix: label=' + label + r' buffers=(\d+) audible=(\d+) nonzero=(\d+) peak=(\d+)', session.logs()[begin:])
                assert found, 'Missing post-mix output'
                result = dict(label=label, **dict(zip(('buffers', 'audible', 'nonzero', 'peak'), map(int, found.groups()))))
                assert result['buffers'] > 0
                rows.append(result)
                return result

            if muted:
                zero = measure('ambient_muted_entry')
                assert zero['nonzero'] == 0 and zero['peak'] == 0, zero
                session.command('audiooptions 1 0 10 0')
                resumed = measure('ambient_unmuted')
                assert resumed['peak'] > 0, resumed
            else:
                low = measure('ambient_low')
                session.command('audiooptions 1 0 100 0')
                high = measure('ambient_high_live')
                assert low['peak'] > 0 and high['peak'] > 0
                ratio = low['peak'] / high['peak']
                # SDL channel gain 12/128 plus integer rounding, same source loop.
                assert .07 < ratio < .12, ('Nonlinear or stale ambient master gain', ratio)
                rows.append(dict(low_to_high_peak_ratio=ratio))
                session.command('audiooptions 0 0 100 0')
                assert measure('ambient_muted_live')['nonzero'] == 0
                session.command('audiooptions 1 0 100 0')
                assert measure('ambient_resumed_live')['peak'] > 0
            session.command('audiotrace 0')
    result = dict(passed=True, apk_sha256=apk, rows=rows,
                  natural_playthrough=False, fixture='synthetic local-ambient sensor, production component and SDL mixer',
                  microphone_or_recording=False, original_config_and_progress_restored=True)
    (PORT / 'reports' / (args.report + '-results.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
