"""Verify the whole-screen Game Over instruction using app-local corner taps.

OpenAI Codex (LLM). Select the allocated device with ANDROID_SERIAL.
No global Android input, physical controller or natural campaign traversal.
Each fixture restores the original configuration and progress on exit.
"""
import argparse
import json
import os
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report', required=True)
args = parser.parse_args()
if not os.environ.get('ANDROID_SERIAL'):
    raise RuntimeError('Select an allocated device with ANDROID_SERIAL')
apk = installed_apk_sha256()
for label, x, y in [('top-left', 10, 10), ('bottom-right', 630, 470)]:
    with CampaignSession(args.report + '-' + label, level=1) as session:
        session.command('combatlastlife')
        session.wait('Pazur game over menu opened', seconds=15)
        start = len(session.logs())
        session.command(f'padvirtual tap {x} {y}')
        session.wait('Changing to: 3', seconds=30, after=start)
        time.sleep(1)
        assert session.pid in session.process_ids(), 'Game process exited'
        result = dict(position=[x, y], returned_to_menu=True,
                      apk_sha256=apk, natural_playthrough=False)
    result['original_config_and_progress_restored'] = True
    (session.report / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result), flush=True)
