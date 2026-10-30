"""Measure enemy attack frames in protected fixtures; OpenAI Codex (LLM).

Requires an explicitly allocated device and preserves user configuration/saves.
No natural campaign completion or original-Windows runtime parity is implied.
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


def summarize_frames(log):
    """Keep each animation separate: multi-action sequences have unequal gaps.

    Wall-clock intervals may include state changes. These are emission events,
    not accepted hits on Claw, and a single event gives no repeat estimate.
    """
    samples = {}
    for line in log.splitlines():
        event = re.search(r'Pazur attack frame: actor=(\S+) animation=(\S+) frame=(\d+)', line)
        stamp = re.search(r'\d\d-\d\d (\d+):(\d+):([\d.]+)', line)
        if event and stamp:
            hours, minutes, seconds = map(float, stamp.groups())
            samples.setdefault(event.group(2), []).append(hours * 3600 + minutes * 60 + seconds)
    result = []
    for animation, timestamps in samples.items():
        intervals = [round(after - before, 4) for before, after in zip(timestamps, timestamps[1:])]
        result.append(dict(animation=animation, events=len(timestamps), intervals_s=intervals,
                           median_s=statistics.median(intervals) if intervals else None))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--indices', type=int, nargs='+',
                        default=[14, 16, 20, 22, 27, 28, 33, 35, 0, 1, 4, 5, 9, 10, 13])
    parser.add_argument('--seconds', type=float, default=7)
    parser.add_argument('--distance', type=float, default=70)
    parser.add_argument('--duck', action='store_true')
    args = parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):
        parser.error('Select the authorized device using ANDROID_SERIAL')
    if not 3 <= args.seconds <= 30:
        parser.error('seconds must be between 3 and 30')
    if not 20 <= args.distance <= 600:
        parser.error('distance must be between 20 and 600')
    if args.duck and args.seconds > 5.5:
        parser.error('duck samples are limited to 5.5 seconds (one bounded input hold)')
    inventory = json.loads((PORT / 'reports/combat-audit/inventory.json').read_text())
    if any(index < 0 or index >= len(inventory) for index in args.indices):
        parser.error('Invalid enemy index')
    # Reject stale generated index ordering before touching the phone's saves.
    native = (PORT / 'native/CombatPrototypes.h').read_text()
    names = re.findall(r'ActorPrototype_Level\d+_\w+', native.split('static const char*')[0])
    if names != [enemy['prototype'] for enemy in inventory]:
        raise RuntimeError('Native fixture inventory mismatch')
    apk_sha = installed_apk_sha256()
    local = PORT / 'app/build/outputs/apk/debug/app-debug.apk'
    if apk_sha != hashlib.sha256(local.read_bytes()).hexdigest():
        raise RuntimeError('Installed APK differs from local support source')
    results = []
    with CampaignSession(args.report, level=1, apk_support=True) as session:
        for index in args.indices:
            enemy = inventory[index]
            dy = 55 - enemy['body']['height'] / 2
            session.command(f'combatstage {index} {args.distance} {dy}')
            session.command('invincible 1')
            if args.duck:
                session.command('combatkey down 6000')
            start = len(session.logs())
            time.sleep(args.seconds)
            animations = summarize_frames(session.logs()[start:])
            row = dict(index=index, prototype=enemy['prototype'], window_s=args.seconds,
                       distance_px=args.distance, duck_input=args.duck, dy_px=dy,
                       animations=animations, observed=bool(animations))
            # Requested posture does not prove the AI selected its low attack.
            # Preserve animation names and unobserved cases for manual review.
            results.append(row)
            print(json.dumps(row), flush=True)
        result = dict(apk_sha256=apk_sha, natural_playthrough=False, player_protected=True,
                      enemy_hp_edited=False, results=results,
                      fixture='isolated flat arena; enemies removed between cases; no player attacks; '
                              'selected initial separation; intervals can include state transitions')
        (session.report / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
