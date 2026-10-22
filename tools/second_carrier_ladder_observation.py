"""Observe the real second carrier / ladder transfer; OpenAI Codex (LLM).

The standalone fixture removes enemies, sets HP100/ammo99 and initially places
Claw on the real x9236 ledge. It is not a natural campaign pass. transfer() itself
only observes support and sends ordinary SDL input; an existing natural owner
may use it without any fixture setup. World platforms and terrain stay unchanged.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256


def transfer(session):
    """From the real x9236 ledge, board and hold Up before reaching the ladder."""
    start = len(session.logs())
    session.command('platformtrace nextcarrier 10000')
    deadline = time.monotonic() + 8
    pattern = r'platform position: label=nextcarrier tick=(\d+) id=\d+ x=([-\d.]+) y=4176.00 vx=([-\d.]+)'
    phase = None
    while time.monotonic() < deadline:
        samples = re.findall(pattern, session.logs()[start:])
        if samples:
            tick, x, vx = samples[-1]
            if 9360 <= float(x) <= 9390 and float(vx) < 0:
                phase = dict(tick=int(tick), x=float(x), vx=float(vx))
                break
        time.sleep(.02)
    if phase is None:
        raise RuntimeError('No second-carrier boarding window')
    session.command('combatjumpattack 600 0 right 650')
    # Hold Up during the boarding jump, before slow status-query round trips.
    # A natural catnip pickup changes horizontal speed and the landing offset;
    # waiting until after boarding can carry Claw beyond the ladder sensor.
    for _ in range(3):
        session.command('combatkey up 2000')
        time.sleep(2.1)
    session.command('combatkey release 0')
    session.command('combatstatus')
    session.command('ladderstatus')
    health, x, y = re.findall(r'probe status: claw=(-?\d+).*?x=([-\d.]+) y=([-\d.]+)', session.logs())[-1]
    result = dict(ordinary_input_only=True, board=phase, health=int(health), x=float(x), y=float(y))
    result['passed'] = result['health'] > 0 and abs(result['x']-9568) < 3 and abs(result['y']-3528.6) < 3
    if not result['passed']:
        raise RuntimeError('Second-carrier ladder transfer failed: ' + str(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    result = dict(natural_playthrough=False, apk_sha256=installed_apk_sha256(),
                  fixture='enemies removed; HP100/ammo99; initial position 9236,4114; remote arena floor')
    with CampaignSession(args.report, level=1) as session:
        session.command('combatstage -1 80 0')
        session.command('campaignposition 9236 4114')
        time.sleep(.4)
        result.update(transfer(session))
        session.command('menukey escape')
        session.capture('after')
        (session.report/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
