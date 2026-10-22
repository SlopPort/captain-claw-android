"""Observe a real ladder-cap jump; OpenAI Codex (LLM).

Controlled fixture, never a natural campaign pass: enemies removed, HP100/ammo99,
initial placement on the real lower catwalk. Subsequent climb and jump are normal
SDL keys. World collision stays unchanged; original user files are restored.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    result = dict(natural_playthrough=False, apk_sha256=installed_apk_sha256(),
                  fixture='enemies removed; HP100/ammo99; initial position 8193,4434; remote arena floor')
    with CampaignSession(args.report, level=1) as session:
        session.command('combatstage -1 80 0')
        session.command('campaignposition 8193 4434')
        time.sleep(.4)
        session.command('combatkey up 1900')
        time.sleep(2)
        session.command('combatkey release 0')
        session.command('ladderstatus')
        session.command('combatstatus')
        start = len(session.logs())
        session.command('platformtrace ladderjump 5000')
        session.command('combatjumpmeasure ladderjump')
        session.command('combatjumpattack 600 0 right 650')
        time.sleep(2)
        session.command('combatkey release 0')
        session.command('combatstatus')
        session.command('ladderstatus')
        session.command('menukey escape')
        session.capture('after')
        result['jump_trace'] = re.findall(r'Pazur jump trace:.*', session.logs()[start:])
        result['states'] = re.findall(r'probe status:.*', session.logs())
        result['ladder_states'] = re.findall(r'Pazur ladder[^\r\n]*', session.logs())
        (session.report/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
