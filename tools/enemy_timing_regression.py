"""Physical attack emission regression checks for debug37; OpenAI Codex (LLM).

Temporary protected arenas and synthetic frame-zero actions are fixtures only.
User files are restored by CampaignSession. Select an authorized device first.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import statistics
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256

PORT = Path(__file__).resolve().parents[1]


def events(log, actor, animation):
    result = []
    for line in log.splitlines():
        if f'actor={actor} animation={animation} ' not in line:
            continue
        tick = re.search(r' tick=(\d+)', line)
        if not tick:
            continue
        if 'Pazur attack cycle:' in line:
            result.append(('cycle', int(tick[1]), int(re.search(r' delay=(\d+)', line)[1])))
        elif 'Pazur attack frame:' in line:
            result.append(('hit', int(tick[1]), int(re.search(r' frame=(\d+)', line)[1])))
    return result


def assess(records, frame, offset, delay, period):
    """Check event timing as well as spacing; detect duplicate emissions per cycle.

    Timing tolerance covers update ordering, carried animation time and a slow
    device's frame pacing. Exact emission frame is asserted independently. It is intentionally much smaller than a whole standing animation.
    """
    cycles = []
    for kind, tick, value in records:
        if kind == 'cycle':
            cycles.append(dict(tick=tick, delay=value, hits=[]))
        elif cycles:
            cycles[-1]['hits'].append(dict(tick=tick, frame=value))
    complete = [cycle for cycle in cycles if cycle['hits']]
    assert len(complete) >= 3, cycles
    assert all(len(cycle['hits']) <= 1 for cycle in cycles), cycles
    assert all(len(cycle['hits']) == 1 for cycle in cycles[:-1]), cycles
    assert all(cycle['delay'] == delay for cycle in cycles), cycles
    assert all(cycle['hits'][0]['frame'] == frame for cycle in complete), cycles
    offsets = [cycle['hits'][0]['tick'] - cycle['tick'] for cycle in complete]
    assert all(max(0, delay + offset - 85) <= value <= delay + offset + 85 for value in offsets), offsets
    hits = [cycle['hits'][0]['tick'] for cycle in complete]
    intervals = [after - before for before, after in zip(hits, hits[1:])]
    assert abs(statistics.median(intervals) - period) <= 75, intervals
    return dict(passed=True, cycles=len(cycles), emissions=len(complete),
                first_event_offsets_ms=offsets, intervals_ms=intervals,
                median_interval_ms=statistics.median(intervals), expected_frame=frame)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):
        parser.error('Select the authorized device using ANDROID_SERIAL')
    apk = PORT / 'app/build/outputs/apk/debug/app-debug.apk'
    apk_sha = installed_apk_sha256()
    assert apk_sha == hashlib.sha256(apk.read_bytes()).hexdigest(), 'Installed APK mismatch'
    # index, actor name, animation, separation, frame, ANI offset, delay, cycle.
    cases = [
        (14, 'Officer', 'strike', 70, 3, 480, 0, 770),
        (16, 'Soldier', 'strike1', 70, 2, 60, 0, 630),
        (16, 'Soldier', 'strike', 250, 3, 750, 0, 1250),
        (20, 'Level3_CutThroat', 'strike2', 250, 6, 520, 250, 870),
        (22, 'Level3_RobberThief', 'strike1', 250, 5, 640, 100, 1100),
        (0, 'Level10_CrazyHook', 'strike1', 70, 2, 90, 250, 525),
        (33, 'Level7_BearSailor', 'strike1', 70, 2, 270, 0, 590),
        (10, 'Level13_Chameleon', 'strike1', 70, 1, 50, 150, 400),
        (27, 'Level5_TownGuard1', 'strike2', 70, 4, 310, 0, 570),
        (5, 'Level11_Siren', 'strike1', 70, 1, 180, 500, 1780),
    ]
    inventory = json.loads((PORT / 'reports/combat-audit/inventory.json').read_text(encoding='utf-8'))
    result = dict(apk_sha256=apk_sha, natural_playthrough=False, player_protected=True,
                  enemy_hp_edited=False, cases=[], synthetic_frame_zero=[])
    with CampaignSession(args.report, level=1, apk_support=True) as session:
        try:
            for index, actor, animation, distance, frame, offset, delay, cycle in cases:
                dy = 55 - inventory[index]['body']['height'] / 2
                # Load this actor's resources before timing its first cycle.
                # Cold diagnostic spawning can consume a frame budget from before
                # the actor existed; normal level loading resets that clock.
                session.command(f'combatstage {index} {distance} {dy}')
                session.command('invincible 1')
                time.sleep(.2)
                start = len(session.logs())
                session.command(f'combatstage {index} {distance} {dy}')
                session.command('invincible 1')
                time.sleep(4.5)
                row = assess(events(session.logs()[start:].rsplit('Pazur probe stage:', 1)[-1], actor, animation), frame, offset, delay, cycle)
                row.update(index=index, actor=actor, animation=animation)
                result['cases'].append(row)
                print(json.dumps(row), flush=True)
            for delay in (0, 150, 750):
                session.command(f'combatstagezero 33 70 5 {delay}')
                session.command('invincible 1')
                time.sleep(.2)
                start = len(session.logs())
                session.command(f'combatstagezero 33 70 5 {delay}')
                session.command('invincible 1')
                time.sleep(5)
                row = assess(events(session.logs()[start:].rsplit('Pazur probe stage:', 1)[-1], 'Level7_BearSailor', 'strike1'),
                             0, 0, delay, 590 + delay)
                row.update(delay_ms=delay, synthetic=True)
                result['synthetic_frame_zero'].append(row)
                print(json.dumps(row), flush=True)
            assert 'Fatal signal' not in session.logs() and 'FATAL EXCEPTION' not in session.logs()
            result['passed'] = True
        finally:
            (session.report / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
