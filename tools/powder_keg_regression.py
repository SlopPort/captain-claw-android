"""Regression for a real powder-keg shot; this is NOT campaign traversal.

OpenAI Codex (LLM). A fresh level-one fixture teleports only for setup. The shot
uses ordinary SDL input. Health, ammo, damage and immunity are not altered.
Original user configuration and saves are restored even if the game aborts.
"""
import argparse
import json
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--expect-crash', action='store_true')
    args = parser.parse_args()
    result = dict(apk_sha256=installed_apk_sha256(), natural_playthrough=False,
                  fixture='fresh level 1; teleport 3470 4840; ordinary crouching pistol shot',
                  expected_crash=args.expect_crash)
    with CampaignSession(args.report, level=1) as session:
        session.command('teleport 3470 4840')
        time.sleep(.7)
        # Teleport preserves facing; a brief real movement faces the keg.
        session.command('combatkey right 20')
        time.sleep(.1)
        session.command('combatkey release 0')
        session.command('combatstatus')
        session.capture('before')
        start = len(session.logs())
        try:
            session.command('combatkey down 2000')
            session.command('combatkey pistol 100')
            time.sleep(1.5)
            session.command('combatkey release 0')
            session.command('combatstatus')
            session.capture('after')
        except RuntimeError as error:
            result['error'] = str(error)
        log = session.logs()[start:]
        result['keg_damaged'] = 'POWDERKEG/* health=1->' in log
        result['missing_body_assertion'] = 'Could not find actor to retrieve AABB' in log
        result['fatal_signal'] = 'Fatal signal' in log
        result['alive'] = session.pid in session.process_ids()
        result['explosion_requested'] = 'Pazur area requested:' in log
        result['actual_explosion_contact'] = 'damage=50 area=' in log
        result['passed'] = result['keg_damaged'] and (
            result['missing_body_assertion'] and result['fatal_signal']
            if args.expect_crash else
            result['alive'] and not result['fatal_signal'] and result['explosion_requested']
            and result['actual_explosion_contact'])
        (session.report/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result), flush=True)
    assert result['passed'], result


if __name__ == '__main__':
    main()
