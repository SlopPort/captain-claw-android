"""Protected custom-melee runtime fixtures; OpenAI Codex (LLM).

Requires an explicitly selected authorized device and an installed current APK.
The fixture checks real engine state/window logs, not original Windows runtime
equivalence. CampaignSession preserves and restores the user's saves/config.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256

PORT = Path(__file__).resolve().parents[1]


def parse(log, marker, actor):
    rows = []
    for line in log.splitlines():
        if marker not in line or f'actor={actor} ' not in line:
            continue
        rows.append(dict(re.findall(r'(\w+)=([^\s]+)', line.split(marker, 1)[1])))
    return rows


def assess_crab(log):
    windows = parse(log, 'Pazur original window:', 'Level7_HermitCrab')
    opened = [row for row in windows if row['enabled'] == '1']
    assert len(opened) >= 3, windows
    assert all(int(row['image']) in (203, 204) for row in opened), windows
    # An open/close pair proves the window does not remain after the strike.
    assert len([row for row in windows if row['enabled'] == '0']) >= 2, windows
    frames = parse(log, 'Pazur attack frame:', 'Level7_HermitCrab')
    assert frames and all(int(row['frame']) == 3 for row in frames), frames
    contacts = parse(log, 'Pazur original contact:', 'Level7_HermitCrab')
    assert contacts and all(int(row['image']) in (203, 204) and int(row['damage']) == 5 for row in contacts), contacts
    pairs = []
    active = None
    for line in log.splitlines():
        if 'actor=Level7_HermitCrab ' not in line:
            continue
        row = dict(re.findall(r'(\w+)=([^\s]+)', line))
        if 'Pazur original window:' in line:
            if row['enabled'] == '1':
                assert active is None, ('Duplicate open', row)
                active = dict(opened=int(row['tick']), contacts=[])
            elif active is not None:
                active['closed'] = int(row['tick'])
                duration = active['closed']-active['opened']
                assert 75 <= duration <= 165, active
                assert len(active['contacts']) <= 1, active
                pairs.append(active)
                active = None
        elif 'Pazur original contact:' in line:
            assert active is not None, ('Contact outside window', row)
            active['contacts'].append(row)
    assert len(pairs) >= 2, pairs
    return dict(passed=True, windows=windows, completed_windows=pairs, emissions=frames, contacts=contacts)


def assess_fish(log, actor, direction):
    moves = parse(log, 'Pazur original melee:', actor)
    finished = parse(log, 'Pazur original finish:', actor)
    assert moves and finished, (moves, finished)
    first = finished[0]
    assert len(moves) >= 2, ('Fish did not enter another attack', moves, finished)
    assert first['animation'] == 'strike1' and int(first['direction']) == direction, first
    x, start, target = (float(first[key]) for key in ('x', 'start', 'target'))
    assert 40 <= abs(start-target) <= 100, first
    assert (x-target)*direction >= -1, first
    assert 0 < int(first['elapsed']) <= 1500, first
    return dict(passed=True, first_move=moves[0], first_finish=first)


def assess_tiger(log):
    moves = parse(log, 'Pazur original melee:', 'Level14_TigerGuard')
    assert {row['animation'] for row in moves} >= {'strike1', 'strike3', 'frontflip'}, moves
    # Knife repeats retain the existing decision deadline; each new deadline
    # denotes an independent attack entry, not a new gate for every knife.
    decisions = []
    for row in moves:
        if not decisions or row['next_entry'] != decisions[-1]['next_entry']:
            decisions.append(row)
    assert len(decisions) >= 5, decisions
    for row in decisions:
        delay = int(row['next_entry'])-int(row['clock'])
        assert 1250 <= delay <= 2000, row
        if row['animation'] == 'strike1':
            assert 2 <= int(row['repeats']) <= 4, row
    for before, after in zip(decisions, decisions[1:]):
        assert int(after['clock']) >= int(before['next_entry']), (before, after)
    assert all(row['animation'] != 'strike2' for row in moves), moves
    contacts = parse(log, 'Pazur original contact:', 'Level14_TigerGuard')
    assert contacts, 'Tiger moves never produced a real contact'
    assert {int(row['damage']) for row in contacts} >= {15,20}, 'Both knife and lunge must hit in this fixture'
    assert all((int(row['damage']) == 15 and int(row['image']) >= 202) or
               int(row['damage']) == 20 for row in contacts), contacts
    return dict(passed=True, decisions=decisions, moves=moves, contacts=contacts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--mode', choices=('all', 'crab', 'fish', 'tiger'), default='all')
    parser.add_argument('--tiger-seconds', type=float, default=55)
    args = parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):
        parser.error('Select the authorized device using ANDROID_SERIAL')
    installed = installed_apk_sha256()
    assert installed == hashlib.sha256((PORT/'app/build/outputs/apk/debug/app-debug.apk').read_bytes()).hexdigest(), 'Installed APK mismatch'
    inventory = json.loads((PORT/'reports/combat-audit/inventory.json').read_text(encoding='utf-8'))
    result = dict(passed=False, apk_sha256=installed, natural_playthrough=False,
                  player_protected=True, enemy_hp_edited=False, cases=[])
    with CampaignSession(args.report, level=1, apk_support=True) as session:
        try:
            session.command('combatrayzero')
            assert 'Pazur zero ray regression:' in session.logs()
            def stage(index, distance):
                dy = 55-inventory[index]['body']['height']/2
                session.command(f'combatstagefixed {index} {distance} {dy}')
                session.command('invincible 1')
                time.sleep(.2)
                start = len(session.logs())
                session.command(f'combatstagefixed {index} {distance} {dy}')
                session.command('invincible 1')
                return start
            if args.mode in ('all', 'crab'):
                for distance in (70, -70):
                    start = stage(34, distance)
                    time.sleep(4)
                    row = assess_crab(session.logs()[start:].rsplit('Pazur probe stage:', 1)[-1])
                    row.update(actor='Level7_HermitCrab', distance=distance)
                    result['cases'].append(row)
            if args.mode in ('all', 'fish'):
                for index, actor in ((3, 'Level11_Fish'), (6, 'Level12_Fish')):
                    for distance in (50, -50):
                        start = stage(index, distance)
                        time.sleep(1)
                        # Fixed patrol is deliberately motionless. Leave and
                        # re-enter its real sensor to verify the same actor can
                        # commit another lunge after completing the first.
                        session.command('campaignposition 200400 1045')
                        time.sleep(.2)
                        destination = 200050 if distance > 0 else 199950
                        session.command(f'campaignposition {destination} 1045')
                        time.sleep(1)
                        row = assess_fish(session.logs()[start:], actor, -1 if distance > 0 else 1)
                        row.update(actor=actor, distance=distance)
                        result['cases'].append(row)
            if args.mode in ('all', 'tiger'):
                start = stage(13, 75)
                time.sleep(args.tiger_seconds)
                row = assess_tiger(session.logs()[start:])
                row.update(actor='Level14_TigerGuard')
                result['cases'].append(row)
            assert 'Fatal signal' not in session.logs() and 'FATAL EXCEPTION' not in session.logs()
            result['passed'] = True
        finally:
            (session.report/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
