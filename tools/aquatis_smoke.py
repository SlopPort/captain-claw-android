"""Aquatis arena regression with explicit teleport/protection/projectile fixtures.

Never edits boss/tentacle HP or invokes damage callbacks. Uses real pistol
projectiles and dynamite physics/fuses. Does not establish a natural playthrough.
"""
import argparse
import json
import time
import re
from campaign_session import CampaignSession


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--observe',action='store_true')
    args=parser.parse_args()
    with CampaignSession(args.report,level=12) as session:
        assert 'Using APK engine support' in session.logs()
        session.command('invincible 1')
        session.command('teleport 37154 3570')
        session.wait('Pazur Aquatis fight started')
        time.sleep(7)
        session.command('campaignmap');session.capture('arena-start')
        if args.observe:return
        session.command('teleport 37780 3520');time.sleep(.4)
        before=len(session.logs())
        session.command('campaignshot dynamite 38050 3490');time.sleep(3)
        assert 'crack explosion: accepted' not in session.logs()[before:], 'Uncleared tentacles must block the crack'
        session.command('campaignshot pistol 37800 3600');time.sleep(.5)
        session.command('campaignmap')
        bosses=re.findall(r'name=ActorPrototype_Level12_Aquatis .* hp=(-?\d+)',session.logs())
        assert bosses and int(bosses[-1])==100,'Direct bullets must not hurt Aquatis'
        for round in range(5):
            session.command('teleport 37680 3520');time.sleep(.4)
            # These are projectile fixtures, not player input or ammo use.
            for x,y in [(37397,3608),(37523,3612),(37648,3614)]:
                for _ in range(3):
                    session.command(f'campaignshot pistol {x-65} {y}');time.sleep(.3)
            session.wait('Pazur Aquatis tentacle down',after=0)
            session.command('teleport 37780 3520');time.sleep(.4)
            if round==0:
                before=len(session.logs())
                session.command('campaignshot dynamite 37930 3490');time.sleep(3)
                assert 'crack explosion: accepted' not in session.logs()[before:], 'Explosion outside crack must not count'
            before=len(session.logs())
            session.command('campaignshot dynamite 38050 3490')
            session.wait('Pazur Aquatis stalactite hit:',seconds=15,after=before)
            session.command('campaignmap');session.capture('round-'+str(round+1))
        session.wait('Pazur enemy defeated: ActorPrototype_Level12_Aquatis')
        time.sleep(2)
        session.command('campaignfinish')
        session.wait('Score screen initialized OK')
        for _ in range(12):
            session.command('padvirtual tap 320 240');time.sleep(.35)
            if 'Level name: Level - 13' in session.logs():break
        session.wait('Level name: Level - 13')
        result=dict(passed=True,natural_playthrough=False,
                    fixtures=['teleports','player invincibility','real projectile spawning'],
                    boss_health_edited=False,negative_rules=['uncleared tentacles','direct bullet','wrong explosion location'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)


if __name__=='__main__':main()
