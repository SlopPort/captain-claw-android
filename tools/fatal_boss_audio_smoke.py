"""Observe real fatal hero damage and accepted Red Tail hurt audio.

OpenAI Codex (LLM). Technical fixtures, never campaign or original-parity
evidence. Hero case: active Soldier, setup HP100/ammo99, no healing/protection.
Boss case: real arena/intro, protected and repositioned hero, ordinary melee,
no boss HP edits. Measures accepted resources plus combined mixer output,
not isolated voice PCM or a human listening judgment. Fresh files restored.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from android_log_evidence import crash_evidence
from gamepad_quit_smoke import PORT
from vertical_combat_smoke import state


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--case',choices=('hero','redtail','both'),default='both')
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):parser.error('Select an allocated device')
    report=(PORT/'reports'/args.report).resolve()
    if not report.is_relative_to((PORT/'reports').resolve()):parser.error('Report must stay under reports')
    apk=installed_apk_sha256();rows=[]

    def finish(session,label,start,expected):
        session.command('audioreport')
        log=session.logs()[start:]
        mixes=re.findall(r'audio mix: label='+label+r' buffers=(\d+) audible=(\d+) nonzero=(\d+) peak=(\d+)',log)
        assert len(mixes)==1,'Missing/ambiguous post-mix observation'
        b,a,n,p=map(int,mixes[0])
        accepted=[s.lower() for s in re.findall(r'audio sound: label='+label+r' accepted=1 path=(\S+)',log)]
        assert expected in accepted,'Expected resource was not accepted: '+expected
        assert b>0 and n>0 and p>0,'No nonzero mixed output'
        crashes=crash_evidence(session.logs())
        assert crashes['target_pids'] and not crashes['target_crashes'] and not crashes['unattributed_crashes'],crashes
        return dict(label=label,expected_resource=expected,expected_request_count=accepted.count(expected),
                    buffers=b,audible_buffers=a,nonzero_samples=n,peak=p,accepted_resources=accepted,
                    crash_evidence=crashes)

    if args.case in ('hero','both'):
        with CampaignSession(f'{args.report}/hero',level=1) as session:
            session.command('audiooptions 1 0 100 100');session.command('audiotrace 1')
            session.command('audioquiet');session.command('audiomeasure herofatal')
            prototypes=re.findall(r'ActorPrototype_\w+',(PORT/'native/CombatPrototypes.h').read_text())
            start=len(session.logs())
            session.command(f'combatstage {prototypes.index("ActorPrototype_Level1_Soldier")} 80 0')
            target=state(session);deadline=time.monotonic()+40;fatal=None
            while time.monotonic()<deadline:
                hits=re.findall(r'actor=Claw health=(\d+)->(-?\d+) source=(\d+)',session.logs()[start:])
                fatal=next((list(map(int,h)) for h in hits if int(h[0])>0 and int(h[1])<=0 and int(h[2])==target['enemy_actor_id']),None)
                if fatal:break
                time.sleep(.2)
            assert fatal,'No actual fatal Soldier hit in bounded observation'
            # Wait for ordinary death/fade/respawn. The mailbox intentionally
            # rejects audio commands while the engine is paused during fading.
            session.wait('Pazur pad context: mode=2',after=start,seconds=15)
            fade=session.logs().index('Pazur pad context: mode=2',start)
            session.wait('Pazur pad context: mode=1',after=fade,seconds=20)
            row=finish(session,'herofatal',start,'/level1/sounds/deathtile.wav')
            assert row['expected_request_count']==1,'Duplicate fatal sound request'
            assert state(session)['player_hp']>0,'Ordinary respawn did not recover hero health'
            row.update(fatal_health_change=fatal,ordinary_respawn_observed=True,player_protected=False,
                       original_death_cue_verified=False)
        row['fresh_config_and_progress_restored']=True;rows.append(row)
        (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
        print(json.dumps(row),flush=True)

    if args.case in ('redtail','both'):
        with CampaignSession(f'{args.report}/redtail',level=13,apk_support=True) as session:
            session.command('invincible 1');session.command('teleport 37176 2021');time.sleep(23)
            session.command('audiooptions 1 0 100 100');session.command('audiotrace 1')
            session.command('audioquiet');session.command('audiomeasure redtailhurt')
            start=len(session.logs());hit=None;initial_hp=None
            for attempt in range(16):
                offset=len(session.logs());session.command('campaignmap')
                bosses=re.findall(r'kind=boss .*name=Level13_RedTail x=([-\d.]+) y=([-\d.]+) hp=(\d+)',session.logs()[offset:])
                assert bosses,'No live real-arena Red Tail'
                x,y,hp=map(float,bosses[-1])
                if initial_hp is None:initial_hp=int(hp)
                session.command(f'teleport {x-75:.1f} {y-5:.1f}')
                session.command('combatkey right 30');time.sleep(.1)
                session.command('combatkey sword 100');time.sleep(.65)
                hits=re.findall(r'actor=Level13_RedTail health=(\d+)->(-?\d+) source=(\d+)',session.logs()[start:])
                hit=next((list(map(int,h)) for h in hits if int(h[0])>int(h[1])>0),None)
                if hit:break
            assert hit,'No accepted nonfatal melee hit in bounded arena trial'
            row=finish(session,'redtailhurt',start,'/level13/sounds/redtail/01040006.wav')
            assert re.search(r'area contact: source='+str(hit[2])+r' target=Level13_RedTail damage=\d+',session.logs()[start:]),'Missing ordinary melee contact attribution'
            row.update(boss_initial_hp=initial_hp,health_change=hit,attack_attempts=attempt+1,
                       player_protected=True,boss_health_edited=False,actual_arena=True)
        row['fresh_config_and_progress_restored']=True;rows.append(row)
        (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
        print(json.dumps(row),flush=True)
    assert installed_apk_sha256()==apk,'Installed APK changed'
    (report/'results.json').write_text(json.dumps(dict(passed=True,apk_sha256=apk,cases=rows,
        natural_playthrough=False,human_listening_tested=False,isolated_voice_pcm=False),indent=2),encoding='utf-8')


if __name__=='__main__':main()
