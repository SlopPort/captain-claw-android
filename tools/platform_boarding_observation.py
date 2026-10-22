"""Observe ordinary jumps onto a real moving level-one platform.

OpenAI Codex (LLM). Explicit controlled fixture, NOT a natural campaign run:
combatstage removes enemies/projectiles and initializes HP100/ammo99 on a remote
arena floor; campaignposition then places the hero on the real level-one ledge.
The real platform and nearby map collision are unchanged. No state edits occur
during the measured jump. Original player files are restored by CampaignSession.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256


def wait_boarding_window(session, after, timeout=8):
    """Read real platform samples; never move/freeze the platform or hero."""
    deadline = time.monotonic() + timeout
    pattern = r'platform position: label=boarding tick=(\d+) id=\d+ x=([-\d.]+) y=4466.00 vx=([-\d.]+)'
    while time.monotonic() < deadline:
        samples = re.findall(pattern, session.logs()[after:])
        if samples:
            tick, x, vx = samples[-1]
            if 3770 <= float(x) <= 3810 and float(vx) < 0:
                return dict(tick=int(tick), x=float(x), vx=float(vx))
        time.sleep(.02)
    raise RuntimeError('No returning-platform boarding window observed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--wait', type=float, default=0)
    parser.add_argument('--move', type=int, default=650)
    parser.add_argument('--synchronize', action='store_true')
    args = parser.parse_args()
    assert 0 <= args.wait <= 4 and 20 <= args.move <= 2000
    result = dict(apk_sha256=installed_apk_sha256(), natural_playthrough=False,
                  fixture='isolated real level-one platform; enemies removed; HP100/ammo99; teleport setup',
                  move_ms=args.move, wait_seconds=args.wait)
    with CampaignSession(args.report, level=1) as session:
        session.command('combatstage -1 80 0')
        session.command('campaignposition 3446 4351')
        time.sleep(.4 + args.wait)
        trace_start = len(session.logs())
        session.command('platformtrace boarding 10000')
        session.command('combatjumpmeasure boarding')
        if args.synchronize:
            result['trigger_platform'] = wait_boarding_window(session, trace_start)
        start = len(session.logs())
        session.command(f'combatjumpattack 600 0 right {args.move}')
        time.sleep(3)
        session.command('combatkey release 0')
        session.command('combatstatus')
        session.command('menukey escape')
        session.capture('after')
        observed = session.logs()[start:]
        rows = [dict(tick=int(t), x=float(x), y=float(y), ground=int(ground))
                for t, x, y, ground in re.findall(
                    r'platform hero: label=boarding tick=(\d+) x=([-\d.]+) y=([-\d.]+).*?ground=(\d)', observed)]
        result['samples'] = rows
        result['boarded'] = any(v['ground'] and 3500 < v['x'] < 3900 and 4380 < v['y'] < 4420 for v in rows)
        result['alive'] = session.pid in session.process_ids()
        result['jump_trace'] = re.findall(r'Pazur jump trace:.*', observed)
        (session.report/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps({k: v for k, v in result.items() if k != 'samples'}), flush=True)


if __name__ == '__main__':
    main()
