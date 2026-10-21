"""Aquatis with ordinary sword/charged-throw input, real resupply and death reset.

Explicit fixtures: isolated level start, teleporting to existing objects and
player protection during fights. No spawned projectiles, infinite ammo, boss HP
edits or synthetic boss/finish events. Not a natural traversal of level twelve.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',required=True)
    parser.add_argument('--death-reset',action='store_true');args=parser.parse_args()
    with CampaignSession(args.report,level=12) as session:
        session.command('invincible 1')
        # Collect the EXISTING boss warp so its ordinary checkpoint is recorded.
        session.command('teleport 36407 2049')
        session.wait('Pazur Aquatis fight started')
        session.command('padvirtual attach')
        for _ in range(2):
            session.command('padvirtual button y 1');time.sleep(.1)
            session.command('padvirtual button y 0');time.sleep(.2)
        reset_done=False;round=0;strikes=0;resupplied=False
        while round<5:
            for x,y in [(37397,3608),(37523,3612),(37648,3614)]:
                session.command('combatkey right 30');time.sleep(.1)
                session.command(f'teleport {x-75} 3490');time.sleep(.8)
                for attempt in range(12):
                    session.command('combatkey sword 100');time.sleep(.55)
                    start=len(session.logs());session.command('campaignmap')
                    rows=re.findall(r'name=Level12_AquatisTentacle x=([-\d.]+) y=([-\d.]+) hp=(-?\d+)',session.logs()[start:])
                    matching=[int(hp) for px,py,hp in rows if abs(float(px)-x)<3]
                    assert matching,'Missing original tentacle'
                    if matching[-1]<=0:break
                else:raise AssertionError('Sword attacks did not clear tentacle')
            if round==3:
                # Real pickup collision replenishes the normally consumed ammo.
                session.command('teleport 37250 3490');time.sleep(1)
                resupplied=True
            session.command('combatkey right 30');time.sleep(.1)
            session.command('teleport 37790 3400');time.sleep(1)
            start=len(session.logs());session.command('combatstatus')
            ammo=re.findall(r'probe action: ammo=(\d+) remaining=(\d+)',session.logs()[start:])
            if ammo and int(ammo[-1][1])==0:
                session.command('teleport 37250 3490');time.sleep(1);resupplied=True
                session.command('teleport 37790 3400');time.sleep(1)
                start=len(session.logs());session.command('combatstatus')
                ammo=re.findall(r'probe action: ammo=(\d+) remaining=(\d+)',session.logs()[start:])
            assert ammo and ammo[-1][0]=='2' and int(ammo[-1][1])>0,'Dynamite unavailable'
            start=len(session.logs());session.command('combatkey pistol 1500')
            session.wait('Pazur Aquatis stalactite hit:',seconds=12,after=start)
            strikes+=1;session.capture('rock-'+str(strikes))
            if args.death_reset and not reset_done:
                start=len(session.logs())
                session.command('invincible 0');session.command('teleport 37912 3740')
                session.wait('Pazur Aquatis fight started',seconds=18,after=start)
                session.command('invincible 1')
                start=len(session.logs());session.command('campaignmap')
                log=session.logs()[start:]
                assert re.search(r'name=ActorPrototype_Level12_Aquatis .* hp=100',log),'Boss HP did not reset'
                assert len(re.findall(r'name=Level12_AquatisTentacle .* hp=50',log))==3,'Tentacles did not reset'
                assert 'lives=2' in log,'Expected a real lost life'
                rocks=re.findall(r'name=Level12_AquatisRock x=[-\d.]+ y=([-\d.]+)',log)
                assert len(rocks)==5 and all(3340<float(y)<3380 for y in rocks),'Stalactites not restored'
                reset_done=True;round=0
            else:round+=1
        session.wait('Pazur enemy defeated: ActorPrototype_Level12_Aquatis')
        time.sleep(2);session.command('campaignfinish');session.wait('Score screen initialized OK')
        for _ in range(12):
            session.command('padvirtual tap 320 240');time.sleep(.35)
            if 'Level name: Level - 13' in session.logs():break
        session.wait('Level name: Level - 13')
        result=dict(passed=True,natural_playthrough=False,player_input_fight=True,
                    infinite_ammo=False,spawned_projectiles=False,boss_health_edited=False,
                    real_dynamite_resupply=resupplied,real_death_reset=reset_done,rock_hits=strikes,
                    fixtures=['level start','teleports','protection during fights'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
