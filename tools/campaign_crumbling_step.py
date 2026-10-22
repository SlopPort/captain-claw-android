"""Chain ordinary jumps across a real crumbling-peg section in an owned run.

OpenAI Codex (LLM). Reads opt-in hero support samples and sends ordinary SDL
keys only. Never creates a fixture, edits resources or moves platforms/hero.
The persistent campaign_play owner must be idle and paused. On failure it is
asked to stop, preserving its last real save and restoring the user's files.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb


def landing(session, after, target, base_y):
    deadline = time.monotonic() + 3
    pattern = r'platform hero: label=crumbs tick=(\d+) x=([-\d.]+) y=([-\d.]+).*?ground=(\d)'
    airborne = False
    last_tick = -1
    while time.monotonic() < deadline:
        for tick, x, y, ground in re.findall(pattern, session.logs()[after:]):
            # Log reads overlap. Consume each sample once; replaying an old
            # grounded sample after a newer airborne one is not a landing.
            if int(tick) <= last_tick:
                continue
            last_tick = int(tick)
            if ground == '0' and float(y) < base_y - 10:
                airborne = True
            elif ground == '1' and airborne:
                state = dict(tick=int(tick), x=float(x), y=float(y))
                if abs(state['x']-target) > 45 or not 4100 < state['y'] < 4520:
                    raise RuntimeError('Unexpected support after jump: ' + str(state))
                return state
        time.sleep(.02)
    raise RuntimeError('No ordinary landing observed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--targets', type=float, nargs='+', required=True)
    args = parser.parse_args()
    assert args.label.replace('-', '').isalnum()
    session = CampaignSession(args.report)
    assert (session.report/'config.original.xml').is_file()
    assert not (session.report/'input.json').exists()
    session.pid = adb('shell', 'pidof', 'pl.pazur.port').strip().split()[0]
    session.ticket = int(time.time()*1000)
    result = dict(ordinary_input_only=True, targets=args.targets, landings=[])
    try:
        session.command('menukey escape')
        session.command('combatstatus')
        x, base_y = map(float, re.findall(r'probe status:.*?x=([-\d.]+) y=([-\d.]+)', session.logs())[-1])
        session.command('platformtrace crumbs 10000')
        for target in args.targets:
            duration = round((target-x)/337.5*1000)
            if not 20 <= duration <= 1500:
                raise ValueError('Target is outside a bounded rightward jump')
            after = len(session.logs())
            session.command(f'combatjumpattack 300 0 right {duration}')
            state = landing(session, after, target, base_y)
            result['landings'].append(state)
            x, base_y = state['x'], state['y']
        session.command('combatkey release 0')
        session.command('combatstatus')
        result['final_health'] = int(re.findall(r'probe status: claw=(-?\d+)', session.logs())[-1])
        if result['final_health'] <= 0:
            raise RuntimeError('Player died during the ordinary route')
        session.command('menukey escape')
        session.capture(args.label)
        result['passed'] = True
    except BaseException as error:
        result.update(passed=False, error=str(error))
        incoming = session.report/'input.json'
        if not incoming.exists():
            temporary = session.report/'input.tmp'
            temporary.write_text(json.dumps({'stop': True}), encoding='utf-8')
            temporary.replace(incoming)
        raise
    finally:
        (session.report/(args.label+'.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
