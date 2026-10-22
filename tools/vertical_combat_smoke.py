"""Measure real vertical melee contacts without declaring all misses to be bugs.

OpenAI Codex. Each action starts a fresh process/isolated solid-step fixture.
Enemy offensive AI and normal damage remain active; no invincibility/health
edits. Fixture setup supplies pistol ammo, but no shots are fired here.
"""
import argparse
import json
import re
import time
from pathlib import Path
from campaign_session import CampaignSession
from gamepad_quit_smoke import PORT


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
    parser.add_argument('--actions',nargs='+',choices=('standing','jump','duck','escape'),default=['standing','jump'])
    parser.add_argument('--passive',action='store_true',help='Disable enemy offensive AI to separate geometric misses from interrupted hero input; parry remains')
    parser.add_argument('--above',choices=('enemy','hero'),help='Run only one vertical relation')
    parser.add_argument('--side',type=int,choices=(-1,1),help='Run only one enemy side')
    args=parser.parse_args()
    prototypes=re.findall(r'ActorPrototype_\w+', (PORT/'native/CombatPrototypes.h').read_text())
    officer=prototypes.index('ActorPrototype_Level1_Officer')
    rows=[]
    for above in ((args.above,) if args.above else ('enemy','hero')):
        for side in ((args.side,) if args.side else (-1,1)):
            for action in args.actions:
                label=f'{args.report}-{above}-{side}-{action}'
                with CampaignSession(label,level=1) as session:
                    command='combatstairs' if above=='enemy' else 'combatheroabove'
                    setup_start=len(session.logs())
                    session.command(f'{command} {officer} {side*80} {args.height}'+(' passive' if args.passive else ''))
                    assert f'hero_above={int(above=="hero")} passive={int(args.passive)}' in session.logs()[setup_start:],'Wrong diagnostic build/setup'
                    initial=state(session)
                    assert initial['enemy']=='Officer' and initial['enemy_box'],'Wrong enemy fixture'
                    player_y=initial['player_box'][1]+initial['player_box'][3]/2
                    enemy_y=initial['enemy_box'][1]+initial['enemy_box'][3]/2
                    assert (player_y<enemy_y) == (above=='hero'),'Requested vertical relation not established'
                    start=len(session.logs())
                    direction='right' if side>0 else 'left'
                    session.command('laddertrace vertical-'+action+' 2600')
                    if action in ('jump','escape'):
                        if action=='escape':direction='left' if side>0 else 'right'
                        session.command(('combatjumpattack 1500 450 ' if action=='escape' else 'combatjumpattack 250 80 ')+direction)
                    else:
                        session.command('combatkey '+direction+' 70')
                        if action=='duck':session.command('combatkey down 1600')
                        session.command('combatkey sword 100')
                    time.sleep(1.2);after=state(session)
                    session.command('combatkey release 0');time.sleep(1.2)
                    final=state(session);session.capture('after')
                    evidence=session.logs()[start:]
                    defeated=bool(re.search(r'Pazur enemy defeated: Officer\s*$',evidence,re.M))
                    row=dict(above=above,side=side,step_height=args.height,action=action,
                             initial=initial,after=after,final=final,enemy_defeated=defeated,
                             player_damage=initial['player_hp']-final['player_hp'],
                             enemy_damage_observed=defeated or 0<=final['enemy_hp']<initial['enemy_hp'],
                             offensive_ai_disabled=args.passive,
                             attack_animations_observed=sorted(set(re.findall(r'animation=(swipe|kick|uppercut|jumpswipe|duckswipe)\b',evidence))),
                             jump_observed=bool(re.search(r'jumping=1',evidence)),
                             player_death_observed=bool(re.search(r'combat: actor=Claw health=\d+->0\b',evidence)),
                             protected=False,natural_playthrough=False,
                             interpretation='Observed outcome only; overlap/fairness needs review')
                    (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
                    rows.append(row);print(json.dumps(row),flush=True)
    (PORT/'reports'/(args.report+'-summary.json')).write_text(json.dumps(rows,indent=2),encoding='utf-8')


if __name__=='__main__':main()
