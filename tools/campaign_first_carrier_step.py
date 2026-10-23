"""Observe and attempt first upper L1 carrier in an owned natural campaign.

OpenAI Codex (LLM). Owner must be idle and paused; no fixture setup, teleport,
resource edits or platform changes. An early phase accounts for observed host
mailbox latency, but is not a universal timing guarantee. Validate the landing
instead of continuing a planned route from the wrong floor. Reports are private.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    session = CampaignSession(args.report)
    if not (session.report/'config.original.xml').is_file():
        raise RuntimeError('Missing owned-session backup')
    if (session.report/'input.json').exists():
        raise RuntimeError('Owner has pending input')
    session.pid = adb('shell', 'pidof', 'pl.pazur.port').strip().split()[0]
    session.ticket = time.time_ns()
    result = {'ordinary_input_only': True, 'passed': False}
    running = False
    try:
        session.command('menukey escape'); running = True
        session.command('combatstatus')
        hp, x, y = re.findall(r'probe status: claw=(-?\d+).*?x=([-\d.]+) y=([-\d.]+)', session.logs())[-1]
        result['start'] = [int(hp), float(x), float(y)]
        if int(hp) <= 0 or not 8470 < float(x) < 8630 or not 4100 < float(y) < 4130:
            raise RuntimeError('Start must be alive on the upper approach ledge')
        distance = 8607-float(x)
        if abs(distance) > 5:
            duration = round(abs(distance)/337.5*1000)
            session.command(f"combatkey {'right' if distance > 0 else 'left'} {duration}")
            time.sleep(duration/1000+.1)
            session.command('combatkey release 0')
        start = len(session.logs())
        session.command('platformtrace firstcarrier 10000')
        deadline = time.monotonic()+9
        pattern = r'platform position: label=firstcarrier tick=(\d+) id=\d+ x=([-\d.]+) y=4182.00 vx=([-\d.]+)'
        while time.monotonic() < deadline:
            samples = re.findall(pattern, session.logs()[start:])
            if samples and 8680 <= float(samples[-1][1]) <= 8710 and float(samples[-1][2]) > 0:
                result['phase'] = samples[-1]
                break
            time.sleep(.02)
        else:
            raise RuntimeError('No fresh early carrier window')
        session.command('combatjumpattack 600 0 right 650')
        time.sleep(1.05)
        session.command('combatkey release 0')
        session.command('combatstatus')
        hp, x, y = re.findall(r'probe status: claw=(-?\d+).*?x=([-\d.]+) y=([-\d.]+)', session.logs())[-1]
        result['landing'] = [int(hp), float(x), float(y)]
        support = re.findall(r'platform hero: label=firstcarrier tick=(\d+) x=([-\d.]+) y=([-\d.]+).*?ground=(\d)', session.logs()[start:])
        result['support_sample'] = support[-1] if support else None
        # Falling to y4434 is a miss even though that lower floor is solid.
        result['passed'] = (int(hp) > 0 and 8750 < float(x) < 9030 and 4080 < float(y) < 4130
                            and bool(support) and support[-1][3] == '1'
                            and abs(float(support[-1][2])-float(y)) < 5)
        if not result['passed']:
            raise RuntimeError('Upper carrier landing not established')
    except Exception as error:
        result['error'] = str(error)
    finally:
        if running:
            try:
                session.command('combatkey release 0')
                session.command('menukey escape')
                session.capture('first-carrier-verified')
            except Exception as error:
                result['cleanup_error'] = str(error)
                temporary = session.report/'input.tmp'
                temporary.write_text('{"stop":true}', encoding='utf-8')
                temporary.replace(session.report/'input.json')
        (session.report/'first-carrier-verified.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result), flush=True)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
