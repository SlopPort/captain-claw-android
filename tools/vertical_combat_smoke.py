"""Measure real vertical melee contacts without declaring all misses to be bugs.

OpenAI Codex. Each action starts a fresh process/isolated solid-step fixture.
Offensive AI is active unless --passive; normal damage remains active. Setup
initializes hero HP to 100 and pistol ammo to 99, without protection. No health
edits occur during the observed action and no shots are fired here.
"""
import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path
from campaign_session import CampaignSession
from gamepad_quit_smoke import PORT, adb


def state(session):
    start=len(session.logs());session.command('combatstatus');log=session.logs()[start:]
    match=re.search(r'probe status: claw=(-?\d+) duck=(\d) x=([-\d.]+) y=([-\d.]+) box=([\d,-]+) target=(\S+) target_id=(\d+) target_hp=(-?\d+) target_max=(-?\d+)',log)
    assert match,'Missing combat state'
    hp,duck,x,y,box,name,actor,target_hp,target_max=match.groups()
    target_box=re.search(r'probe target box: actor=\S+ box=([\d,-]+)',log)
    return dict(player_hp=int(hp),duck=duck=='1',position=[float(x),float(y)],
                player_box=list(map(int,box.split(','))),enemy=name,enemy_hp=int(target_hp),
                enemy_max=int(target_max),enemy_box=list(map(int,target_box[1].split(','))) if target_box else None)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--height',type=int,choices=(16,32,48,64),default=48)
    parser.add_argument('--prototype',default='ActorPrototype_Level1_Officer',help='Exact prototype from native/CombatPrototypes.h; loads its own source level')
    parser.add_argument('--jump-direction-ms',type=int,choices=range(20,2001),metavar='20..2000',default=250)
    parser.add_argument('--attack-delay-ms',type=int,choices=range(20,1001),metavar='20..1000',default=80)
    parser.add_argument('--jump-hold-ms',type=int,choices=range(20,1001),metavar='20..1000',default=250)
    parser.add_argument('--actions',nargs='+',choices=('standing','jump','duck','escape'),default=['standing','jump'])
    parser.add_argument('--passive',action='store_true',help='Disable enemy offensive AI to separate geometric misses from interrupted hero input; parry remains')
    parser.add_argument('--above',choices=('enemy','hero'),help='Run only one vertical relation')
    parser.add_argument('--side',type=int,choices=(-1,1),help='Run only one enemy side')
    args=parser.parse_args()
    # Hash the package actually installed, not a build output that another ABI
    # build can replace while the phone is under test. No APK data is printed.
    package=adb('shell','pm','path','pl.pazur.port').strip()
    base=next(line.removeprefix('package:') for line in package.splitlines() if line.endswith('/base.apk'))
    digest=hashlib.sha256()
    with subprocess.Popen(['adb','exec-out','cat',base],stdout=subprocess.PIPE) as process:
        while chunk:=process.stdout.read(65536):digest.update(chunk)
        assert process.wait()==0,'Cannot hash installed APK'
    apk_sha256=digest.hexdigest()
    prototypes=re.findall(r'ActorPrototype_\w+', (PORT/'native/CombatPrototypes.h').read_text())
    enemy=prototypes.index(args.prototype)
    level=int(re.search(r'_Level(\d+)_',args.prototype)[1])
    rows=[]
    for above in ((args.above,) if args.above else ('enemy','hero')):
        for side in ((args.side,) if args.side else (-1,1)):
            for action in args.actions:
                label=f'{args.report}-{above}-{side}-{action}'
                with CampaignSession(label,level=level) as session:
                    command='combatstairs' if above=='enemy' else 'combatheroabove'
                    setup_start=len(session.logs())
                    session.command(f'{command} {enemy} {side*80} {args.height}'+(' passive' if args.passive else ''))
                    assert f'hero_above={int(above=="hero")} passive={int(args.passive)}' in session.logs()[setup_start:],'Wrong diagnostic build/setup'
                    initial=state(session)
                    assert initial['enemy']!='none' and initial['enemy_box'] and initial['enemy_hp']>0,'Missing live enemy fixture'
                    # Compare supporting height, not body centers: a short rat
                    # on a step can still have its center below a tall hero's.
                    player_y=initial['player_box'][1]+initial['player_box'][3]
                    enemy_y=initial['enemy_box'][1]+initial['enemy_box'][3]
                    if (player_y<enemy_y) != (above=='hero'):
                        # Live acrobatic AI can leave the step before the ADB
                        # status round-trip. Preserve evidence; never count this
                        # as an executed action or weaken the geometry gate.
                        (session.report/'invalid-fixture.json').write_text(json.dumps(dict(
                            apk_sha256=apk_sha256,prototype=args.prototype,above=above,side=side,
                            requested_action=action,fixture_established=False,action_executed=False,
                            initial=initial,reason='Requested vertical relation no longer present'),indent=2),encoding='utf-8')
                        raise AssertionError('Requested vertical relation not established')
                    start=len(session.logs())
                    direction='right' if side>0 else 'left'
                    session.command('laddertrace vertical-'+action+' 2600')
                    if action in ('jump','escape'):
                        if action=='escape':direction='left' if side>0 else 'right'
                        session.command(('combatjumpattack 1000 450 '+direction+' 1000') if action=='escape' else
                                        f'combatjumpattack {args.jump_hold_ms} {args.attack_delay_ms} {direction} {args.jump_direction_ms}')
                    else:
                        session.command('combatkey '+direction+' 70')
                        if action=='duck':session.command('combatkey down 1600')
                        session.command('combatkey sword 100')
                    time.sleep(1.2);after=state(session)
                    session.command('combatkey release 0');time.sleep(1.2)
                    final=state(session);session.capture('after')
                    evidence=session.logs()[start:]
                    contacts=[dict(source=int(source),target=target,damage=int(damage),
                                   area=list(map(int,area.split(','))),body=list(map(int,body.split(','))),
                                   integer_overlap=overlap=='1')
                              for source,target,damage,area,body,overlap in re.findall(
                                  r'area contact: source=(\d+) target=(\S+) damage=(\d+) area=([\d,-]+) body=([\d,-]+) integer_overlap=(\d)',evidence)]
                    created=[dict(source=int(source),damage=int(damage),box=list(map(int,box.split(','))))
                             for source,damage,box in re.findall(r'area created: source=(\d+) damage=(\d+) box=([\d,-]+)',evidence)]
                    defeated=bool(re.search(r'Pazur enemy defeated: '+re.escape(initial['enemy'])+r'\s*$',evidence,re.M))
                    row=dict(apk_sha256=apk_sha256,prototype=args.prototype,source_level=level,above=above,side=side,step_height=args.height,action=action,
                             initial=initial,after=after,final=final,enemy_defeated=defeated,
                             player_damage=initial['player_hp']-final['player_hp'],
                             enemy_damage_observed=defeated or 0<=final['enemy_hp']<initial['enemy_hp'],
                             offensive_ai_disabled=args.passive,
                             area_contacts=contacts,
                             area_created=created,
                             parry_decisions=[dict(actor=n,damage_type=int(t),chance=int(c),roll=int(v),resisted=b=='1')
                                 for n,t,c,v,b in re.findall(r'Pazur parry decision: actor=(\S+) type=(\d+) chance=(\d+) roll=(\d+) resisted=(\d)',evidence)],
                             resistance_events=[dict(actor=n,delta=int(d),damage_type=int(t),health=int(h))
                                 for n,d,t,h in re.findall(r'Pazur damage resisted: actor=(\S+) delta=(-?\d+) type=(\d+) hp=(-?\d+)',evidence)],
                             jump_input=dict(hold_ms=1000 if action=='escape' else args.jump_hold_ms,
                                             direction_ms=1000 if action=='escape' else args.jump_direction_ms,
                                             attack_delay_ms=450 if action=='escape' else args.attack_delay_ms) if action in ('jump','escape') else None,
                             attack_animations_observed=sorted(set(re.findall(r'animation=(swipe|kick|uppercut|jumpswipe|duckswipe)\b',evidence))),
                             jump_observed=bool(re.search(r'jumping=1',evidence)),
                             player_death_observed=bool(re.search(r'combat: actor=Claw health=\d+->0\b',evidence)),
                             protected=False,natural_playthrough=False,
                             fixture_initializes_hero_hp_to_100=True,fixture_sets_pistol_ammo_to_99=True,
                             health_edited_during_action=False,
                             interpretation='Observed outcome only; overlap/fairness needs review')
                    (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
                    rows.append(row);print(json.dumps(row),flush=True)
    (PORT/'reports'/(args.report+'-summary.json')).write_text(json.dumps(rows,indent=2),encoding='utf-8')


if __name__=='__main__':main()
