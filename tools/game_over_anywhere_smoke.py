"""Verify the whole-screen Game Over instruction using app-local corner taps.

OpenAI Codex (LLM). Select the allocated device with ANDROID_SERIAL.
No global Android input, physical controller or natural campaign traversal.
Each fixture restores the original configuration and progress on exit.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from android_log_evidence import crash_evidence

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report', required=True)
args = parser.parse_args()
if not os.environ.get('ANDROID_SERIAL'):
    raise RuntimeError('Select an allocated device with ANDROID_SERIAL')
apk = installed_apk_sha256()
for label in ('top-left', 'bottom-right'):
    with CampaignSession(args.report + '-' + label, level=1) as session:
        session.command('combatlastlife')
        session.wait('Pazur game over menu opened', seconds=15)
        # The game can render wider than 640 logical pixels. A fixed x=630
        # was not the right corner on the default 853-wide viewport.
        viewports=re.findall(r'Pazur viewport: physical=\d+x\d+ logical=(\d+)x(\d+)',session.logs())
        assert viewports,'Missing viewport; refusing to guess the touch target'
        width,height=map(int,viewports[-1])
        x,y=(10,10) if label=='top-left' else (width-10,height-10)
        session.capture('game-over-before')
        start = len(session.logs())
        session.command(f'padvirtual tap {x} {y}')
        session.wait('Changing to: 3', seconds=30, after=start)
        time.sleep(1)
        assert session.pid in session.process_ids(), 'Game process exited'
        session.capture('game-over-after')
        crashes=crash_evidence(session.logs())
        assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],'Crash in game-over transition'
        result = dict(position=[x, y], returned_to_menu=True,
                      logical_viewport=[width,height],crash_evidence=crashes,
                      input='app-local SDL diagnostic tap, not Android MotionEvent',
                      apk_sha256=apk, natural_playthrough=False)
    result['original_config_and_progress_restored'] = True
    (session.report / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result), flush=True)
