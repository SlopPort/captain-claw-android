"""One ordinary boarding jump in an already owned, paused natural campaign.

OpenAI Codex (LLM). The persistent campaign_play owner must remain running and
idle. This helper does not enter a fixture context, touch saves, teleport, alter
resources or freeze platforms. It observes a real return window, sends normal
SDL input, then restores the same paused-menu state before returning.
"""
import argparse
import json
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb
from platform_boarding_observation import wait_boarding_window


def wait_vertical_window(session, after, upper=False):
    deadline = time.monotonic() + 9
    pattern = r'platform position: label=boarding tick=(\d+) id=\d+ x=4259.00 y=([-\d.]+) vx=[-\d.]+ vy=([-\d.]+)'
    import re
    while time.monotonic() < deadline:
        samples = re.findall(pattern, session.logs()[after:])
        if samples:
            tick, y, vy = samples[-1]
            reached = float(y) <= 4440 and float(vy) < 0 if upper else float(y) >= 4770 and float(vy) > 0
            if reached:
                return dict(tick=int(tick), y=float(y), vy=float(vy))
        time.sleep(.02)
    raise RuntimeError('Vertical elevator window not observed')


def wait_start_elevator(session, after):
    import re
    deadline = time.monotonic() + 8
    pattern = r'platform position: label=boarding tick=(\d+) id=\d+ x=([-\d.]+) y=5071.00 vx=([-\d.]+)'
    while time.monotonic() < deadline:
        samples = re.findall(pattern, session.logs()[after:])
        if samples:
            tick, x, vx = samples[-1]
            if float(x) >= 6340 and float(vx) > 0:
                return dict(tick=int(tick), x=float(x), vx=float(vx))
        time.sleep(.02)
    raise RuntimeError('Start elevator did not reach the ladder approach')



def wait_upper_window(session, after):
    """Wait on the real y4182 carrier for a normal jump to the next ledge."""
    import re
    deadline = time.monotonic() + 8
    pattern = r'platform position: label=boarding tick=(\d+) id=\d+ x=([-\d.]+) y=4182.00 vx=([-\d.]+)'
    while time.monotonic() < deadline:
        samples = re.findall(pattern, session.logs()[after:])
        if samples:
            tick, x, vx = samples[-1]
            if 8810 <= float(x) <= 8850 and float(vx) > 0:
                return dict(tick=int(tick), x=float(x), vx=float(vx))
        time.sleep(.02)
    raise RuntimeError('Upper carrier departure window not observed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--leave', action='store_true', help='Jump from the rightward platform to the real far ledge')
    parser.add_argument('--vertical', action='store_true', help='Board the x4259 elevator naturally and jump onto the real upper ledge')
    parser.add_argument('--cavity', action='store_true', help='Descend the real x5916 shaft, ride its start elevator and climb the real ladder')
    parser.add_argument('--upper', action='store_true', help='Jump from the real y4182 carrier towards the next respawn flag')
    parser.add_argument('--observe', action='store_true', help='Read nearby moving-platform positions without moving the hero')
    args = parser.parse_args()
    assert args.label.replace('-', '').isalnum()
    assert sum([args.leave, args.vertical, args.cavity, args.observe, args.upper]) <= 1
    session = CampaignSession(args.report)
    assert (session.report/'config.original.xml').is_file(), 'No owned campaign backup'
    assert not (session.report/'input.json').exists(), 'Campaign owner is busy'
    session.pid = adb('shell', 'pidof', 'pl.pazur.port').strip().split()[0]
    session.ticket = int(time.time()*1000)
    session.command('menukey escape')
    start = len(session.logs())
    session.command('platformtrace boarding 10000')
    if args.observe:
        assert not args.cavity and not args.vertical and not args.leave
        time.sleep(.6)
        phase = {'observation_only': True}
    elif args.upper:
        phase = wait_upper_window(session, start)
        session.command('combatjumpattack 600 0 right 650')
    elif args.cavity:
        assert not args.vertical and not args.leave
        session.command('combatkey left 300')
        time.sleep(1.1)
        phase = wait_start_elevator(session, start)
        # Let the platform carry the hero into the ladder column. Walking
        # here adds its velocity and can overshoot the narrow ladder.
        session.command('combatkey jump 350')
        session.command('combatkey up 1800')
        time.sleep(1.9)
    elif args.vertical:
        assert not args.leave
        phase = wait_vertical_window(session, start)
        session.command('combatkey jump 600')
        time.sleep(.9)
        ride_start = len(session.logs())
        session.command('platformtrace boarding 10000')
        top = wait_vertical_window(session, ride_start, upper=True)
        phase['upper_window'] = top
        session.command('combatjumpattack 600 0 right 600')
    else:
        phase = wait_boarding_window(session, start, rightward=args.leave)
        move = 700 if args.leave else 650
        session.command(f'combatjumpattack 600 0 right {move}')
    time.sleep(.8)
    session.command('combatkey release 0')
    session.command('combatstatus')
    session.command('menukey escape')
    session.capture(args.label)
    result = dict(ordinary_input_only=True, trigger_platform=phase)
    (session.report/(args.label+'.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result), flush=True)
    print(session.logs()[start:][-2200:], flush=True)


if __name__ == '__main__':
    main()
