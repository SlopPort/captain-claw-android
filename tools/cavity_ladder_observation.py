"""Controlled observation of the real start-elevator/ladder transfer.

OpenAI Codex (LLM). Not a natural campaign pass: setup removes enemies, uses
HP100/ammo99 and places the hero on a real ledge. All subsequent movement,
boarding and climbing uses ordinary SDL keys; real map/platforms stay unchanged.
Original user files are restored by CampaignSession, including on failure.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from gamepad_quit_smoke import PORT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    result = dict(natural_playthrough=False, apk_sha256=installed_apk_sha256(),
                  fixture='enemies removed; HP100/ammo99; initial position 6018,4351; remote arena floor')
    with CampaignSession(args.report, level=1) as session:
        session.command('combatstage -1 80 0')
        session.command('campaignposition 6018 4351')
        time.sleep(.4)
        session.command('menukey escape')
        with (session.report/'helper-output.txt').open('w', encoding='utf-8') as output:
            subprocess.run([sys.executable, str(PORT/'tools/campaign_platform_step.py'),
                            '--report', args.report, '--label', 'controlled-transfer', '--cavity'],
                           stdout=output, stderr=subprocess.STDOUT, check=True)
        states = re.findall(r'probe status: claw=(-?\d+).*?x=([-\d.]+) y=([-\d.]+)', session.logs())
        health, x, y = states[-1]
        result.update(health=int(health), x=float(x), y=float(y))
        result['passed'] = result['health'] > 0 and abs(result['x']-6368) < 3 and abs(result['y']-4744.6) < 3
        (session.report/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result), flush=True)
    assert result['passed'], result


if __name__ == '__main__':
    main()
