"""Siren original-pattern device regression; OpenAI Codex (LLM).

Fixed patrol, teleport and protected player are technical fixtures, not campaign.
No original resources or personal identifiers are published. User files restored.
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


def assess(log):
    shots = [tuple(map(int, row)) for row in re.findall(
        r'Pazur siren shot: actor=(\d+) shot=(\d+) tick=(\d+)', log)]
    assert shots, 'No Siren emissions'
    groups = []
    for actor, shot, tick in shots:
        if shot == 1:
            groups.append([])
        assert groups, shots
        groups[-1].append((actor, shot, tick))
    complete = [group for group in groups if len(group) == 4]
    assert len(complete) >= 2, groups
    assert all([row[1] for row in group] == list(range(1, len(group) + 1)) and len(group) <= 4 for group in groups), groups
    spacing = [b[2] - a[2] for group in complete for a, b in zip(group, group[1:])]
    assert all(280 <= value <= 370 for value in spacing), spacing
    intervals = [b[0][2] - a[0][2] for a, b in zip(groups, groups[1:])]
    assert intervals and all(4000 <= value <= 4400 for value in intervals), intervals
    geometry = [tuple(map(float, row)) for row in re.findall(
        r'Pazur siren geometry: actor=\d+ offset=([-\d.]+),([-\d.]+) speed=([-\d.]+),([-\d.]+)', log)]
    assert len(geometry) == len(shots), (len(geometry), len(shots))
    assert all(abs(abs(x) - 28) < .01 and y == -10 and abs(abs(vx) - 200/75) < .001 and vy == 0 and x*vx > 0 for x, y, vx, vy in geometry), geometry
    return dict(passed=True, completed_bursts=len(complete), total_emissions=len(shots),
                within_burst_ms=spacing, first_note_intervals_ms=intervals, geometry=geometry)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select the authorized device using ANDROID_SERIAL')
    apk_hash=installed_apk_sha256()
    assert apk_hash == hashlib.sha256((PORT/'app/build/outputs/apk/debug/app-debug.apk').read_bytes()).hexdigest()
    result=dict(apk_sha256=apk_hash,natural_playthrough=False,player_protected=True,fixed_patrol=True,cases=[])
    with CampaignSession(args.report,level=1,apk_support=True) as session:
        try:
            for index in (5, 8):
                # Indices resolve to levels 11/12 Sirens in audit_combat inventory.
                inventory=json.loads((PORT/'reports/combat-audit/inventory.json').read_text(encoding='utf-8'))
                assert 'Siren' in inventory[index]['type'],inventory[index]
                dy=55-inventory[index]['body']['height']/2
                for distance in (70,-70):
                    session.command(f'combatstagefixed {index} {distance} {dy}')
                    session.command('invincible 1')
                    time.sleep(.3)
                    start=len(session.logs())
                    session.command(f'combatstagefixed {index} {distance} {dy}')
                    session.command('invincible 1')
                    time.sleep(10.5)
                    observed=session.logs()[start:].rsplit('Pazur probe stage:',1)[-1]
                    row=assess(observed)
                    row.update(index=index,distance=distance)
                    result['cases'].append(row)
                    print(json.dumps(row),flush=True)
            assert 'Fatal signal' not in session.logs() and 'FATAL EXCEPTION' not in session.logs()
            result['passed']=True
        finally:
            (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')


if __name__=='__main__':main()
