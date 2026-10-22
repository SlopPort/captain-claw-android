"""Drive a natural campaign through bounded, app-local SDL keyboard input.

OpenAI Codex (LLM). Starts one isolated standard level-one save, then preserves
normal resource carry-over. No teleport, protection, HP/ammo edits or subsequent
level selection. A JSON input file is consumed between paused steps; write it to
input.tmp first, then rename atomically to input.json. Logs and screenshots stay
in the ignored reports directory. Exiting restores the player's original files.
Only real game checkpoints persist progress; a screenshot is not a saved game.
"""
import argparse
import json
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb, REMOTE
from android_package import installed_apk_sha256

KEYS = {'left', 'right', 'up', 'down', 'jump', 'sword', 'pistol', 'weapon', 'release'}
QUERIES = {'campaignmap', 'laddermap', 'combatstatus', 'ladderstatus'}


def validate(request):
    if set(request) - {'stop', 'keys', 'combo', 'query', 'wait'}:
        raise ValueError('Unknown request field')
    for key, duration in request.get('keys', []):
        if key not in KEYS or not isinstance(duration, int) or not 0 <= duration <= 2000:
            raise ValueError('Invalid ordinary key/duration')
    combo = request.get('combo')
    if combo:
        if set(combo) != {'jump', 'attack', 'direction', 'move'}:
            raise ValueError('Combo requires jump, attack, direction and move')
        if combo['direction'] not in ('left', 'right'):
            raise ValueError('Invalid direction')
        for name, limit in [('jump', 1000), ('attack', 1000), ('move', 2000)]:
            if not isinstance(combo[name], int) or not (0 if name == 'attack' else 20) <= combo[name] <= limit:
                raise ValueError('Invalid combo duration')
    if request.get('query') and request['query'] not in QUERIES:
        raise ValueError('Only read-only queries are permitted')
    if not isinstance(request.get('wait', .3), (int, float)) or not 0 <= request.get('wait', .3) <= 3:
        raise ValueError('Wait must be 0..3 seconds')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    with CampaignSession(args.report, level=1) as session:
        print(json.dumps({'ready': True, 'apk_sha256': installed_apk_sha256()}), flush=True)
        session.command('combatstatus')
        session.capture('initial')
        session.command('menukey escape')
        counter = 0
        try:
            while True:
                incoming = session.report/'input.json'
                if not incoming.exists():
                    time.sleep(.1)
                    continue
                counter += 1
                archived = session.report/f'input-{counter:04}.json'
                incoming.rename(archived)
                request = json.loads(archived.read_text('utf-8-sig'))
                validate(request)
                if request.get('stop'):
                    break
                session.command('menukey escape')
                time.sleep(.15)
                start = len(session.logs())
                deadline = time.monotonic()
                combo = request.get('combo')
                if combo:
                    # Existing command schedules ordinary keyboard input only.
                    deadline = time.monotonic() + max(combo['jump'], combo['attack'], combo['move'])/1000
                    session.command(f"combatjumpattack {combo['jump']} {combo['attack']} {combo['direction']} {combo['move']}")
                for key, duration in request.get('keys', []):
                    deadline = max(deadline, time.monotonic() + duration/1000)
                    session.command(f'combatkey {key} {duration}')
                time.sleep(max(0, deadline - time.monotonic()) + request.get('wait', .3))
                if request.get('query'):
                    session.command(request['query'])
                # Death fade temporarily stops game logic for about three seconds.
                # Rejection during that transition is not a game crash.
                retry_until = time.monotonic() + 30
                while True:
                    try:
                        session.command('combatkey release 0')
                        session.command('combatstatus')
                        break
                    except RuntimeError as error:
                        if 'rejected: game not running' not in str(error) or time.monotonic() >= retry_until:
                            raise
                        time.sleep(.3)
                session.command('menukey escape')
                print(session.logs()[start:][-4000:], flush=True)
                # Pause before the slow screenshot transfer: enemies should not
                # receive extra attack time merely because evidence is saved.
                session.capture(f'step-{counter:04}')
                print(json.dumps({'step': counter, 'paused': True}), flush=True)
        finally:
            adb('pull', REMOTE+'SAVES.XML', str(session.report/'campaign-progress.xml'))


if __name__ == '__main__':
    main()
