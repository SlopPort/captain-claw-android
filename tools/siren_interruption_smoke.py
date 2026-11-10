"""Real-projectile Siren cancellation regression; OpenAI Codex (LLM).

Isolated fixed-patrol arena, protected/teleported player, directly spawned pistol
projectiles, temporary saves/config/support are explicit technical fixtures.
Projectiles use real physics/health/state callbacks; enemy HP is never edited.
This is not natural gameplay, campaign traversal or an original-runtime test.
Slow-frame/audio-failure/visibility tests are NOT claimed by this helper.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import time

from android_package import installed_apk_sha256
from campaign_session import CampaignSession

PORT = Path(__file__).resolve().parents[1]
SHOT = re.compile(r'Pazur siren shot: actor=(\d+) shot=(\d+) tick=(\d+)')


class RecordedSession(CampaignSession):
    """Record restoration success even when a case raises inside the context."""
    restored = False
    restoration_error = None

    def __exit__(self, *exc):
        try:
            super().__exit__(*exc)
            self.restored = True
        except BaseException as error:
            self.restoration_error = repr(error)
            raise


def wait_match(session, pattern, after=0, seconds=10):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        session.ensure_log_stream()
        log = session.logs()
        if 'Fatal signal' in log or 'FATAL EXCEPTION' in log:
            raise RuntimeError('Game crashed; inspect retained native.log')
        found = pattern.search(log, after)
        if found:
            return found
        time.sleep(.02)
    raise RuntimeError('Missing evidence within deadline: ' + pattern.pattern)


def actor_shots(log, actor, start=0, end=None):
    return [dict(number=int(row[2]), tick=int(row[3]), position=row.start())
            for row in SHOT.finditer(log, start, len(log) if end is None else end)
            if int(row[1]) == actor]


def assess_interruption(log, actor, first, hit, next_first=None, dead=False):
    """Reject a late shot which failed to interrupt any still-pending burst."""
    before = actor_shots(log, actor, first.start(), hit.start())
    assert before and before[0]['number'] == 1, before
    assert len(before) < 4, 'Hit arrived after all notes; no cancellation was tested'
    assert [row['number'] for row in before] == list(range(1, len(before) + 1)), before
    later = actor_shots(log, actor, hit.end(), next_first.start() if next_first else None)
    assert not later, ('Pending notes escaped after health/state callback', later)
    row = dict(first_tick=int(first[3]), notes_before_hit=before,
               old_health=int(hit[1]), new_health=int(hit[2]),
               projectile_hit_confirmed=True, cancelled_pending_notes=True,
               dead=dead)
    if dead:
        assert int(hit[2]) <= 0, row
    else:
        assert 0 < int(hit[2]) < int(hit[1]), row
        assert next_first is not None
        interval = (int(next_first[3]) - int(first[3])) & 0xffffffff
        assert 4000 <= interval < 15000, ('Recovery not retained or unexpected delay', interval)
        row['next_first_tick'] = int(next_first[3])
        row['first_note_interval_ms'] = interval
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True, help='New basename under reports/')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', args.report):
        parser.error('Use a simple fresh report basename')
    if not os.environ.get('ANDROID_SERIAL'):
        parser.error('Select the currently authorized device through ANDROID_SERIAL')
    report = PORT / 'reports' / args.report
    report.mkdir(parents=True, exist_ok=False)
    result = dict(passed=False, natural_playthrough=False,
                  enemy_health_edited=False, player_protected=True,
                  fixed_patrol=True, projectile_spawn_fixture=True,
                  interruption_and_death_tested=False,
                  not_covered=['slow game-update deltas', 'missing/undecodable audio',
                               'visibility/aggro exit', 'original-runtime parity'],
                  cases=[])
    session = RecordedSession(args.report, level=1, apk_support=True)
    try:
        installed = installed_apk_sha256()
        local = hashlib.sha256((PORT / 'app/build/outputs/apk/debug/app-debug.apk').read_bytes()).hexdigest()
        result.update(apk_sha256=installed, local_apk_sha256=local)
        assert installed == local, 'Installed APK differs from support archive source'
        inventory = json.loads((PORT / 'reports/combat-audit/inventory.json').read_text(encoding='utf-8'))
        with session:
            for index in (5, 8):
                proto = inventory[index]
                assert proto['type'] == f'Level{11 if index == 5 else 12}_Siren', proto
                dy = 55 - proto['body']['height'] / 2
                for distance in (70, -70):
                    case = dict(index=index, actor_type=proto['type'], distance=distance,
                                passed=False, hits=[])
                    result['cases'].append(case)
                    start = len(session.logs())
                    session.command(f'combatstagefixed {index} {distance} {dy}')
                    session.command('invincible 1')
                    # Setup/USB acknowledgement can outlast most of the first
                    # burst. Observe a future first note, never a historical one
                    # emitted while protection/setup was still being installed.
                    observation_ready = len(session.logs())
                    status = wait_match(session, re.compile(
                        r'target=' + re.escape(proto['type']) + r' target_id=(\d+) target_hp=(\d+)'), start)
                    actor = int(status[1])
                    assert int(status[2]) == proto['health'], status.group(0)
                    case['actor_id'] = actor
                    # Same capture groups as SHOT: actor, ordinal, tick.
                    first_pattern = re.compile(r'Pazur siren shot: actor=(' + str(actor) + r') shot=(1) tick=(\d+)')
                    first = wait_match(session, first_pattern, observation_ready)
                    nonlethal = 0
                    for attempt in range(8):
                        # Spawn inside the target sensor. This is explicitly a
                        # projectile fixture, not an ordinary player shot/input.
                        # No direct AddHealth or enemy state invocation occurs.
                        session.command(f'campaignshot pistol {200000 + distance - 2} {1045 + dy}')
                        hit_pattern = re.compile(
                            r'Pazur projectile hit: [^\r\n]* target=' + re.escape(proto['type']) +
                            r' damage=\d+ type=\d+ health=(-?\d+)->(-?\d+)')
                        hit = wait_match(session, hit_pattern, first.end())
                        assert int(hit[2]) < int(hit[1]), 'Projectile did not reduce health'
                        if int(hit[2]) <= 0:
                            wait_match(session, re.compile(r'Pazur enemy defeated: ' + re.escape(proto['type'])), first.end())
                            # Observe past a complete original recovery period;
                            # do not restage/delete the corpse to hide stale notes.
                            deadline = time.monotonic() + 4.5
                            while time.monotonic() < deadline:
                                session.ensure_log_stream()
                                time.sleep(.05)
                            row = assess_interruption(session.logs(), actor, first, hit, dead=True)
                            row['observed_after_death_seconds'] = 4.5
                            case['hits'].append(row)
                            assert nonlethal >= 1, 'Death passed but nonlethal interruption was not exercised'
                            case['passed'] = True
                            break
                        next_first = wait_match(session, first_pattern, hit.end(), seconds=15)
                        row = assess_interruption(session.logs(), actor, first, hit, next_first)
                        case['hits'].append(row)
                        nonlethal += 1
                        first = next_first
                    assert case['passed'], 'Target did not die through bounded actual projectile hits'
                    print(json.dumps(case), flush=True)
            assert 'Fatal signal' not in session.logs() and 'FATAL EXCEPTION' not in session.logs()
            result['interruption_and_death_tested'] = True
        assert session.restored, 'Session did not verify config/save restoration'
        result['passed'] = True
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        result['restoration_verified'] = session.restored
        result['restoration_error'] = session.restoration_error
        (report / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
