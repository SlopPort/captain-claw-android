"""Test whether a normal charged player throw can reach Aquatis's crack.

Teleport/protection/infinite ammo and clearing tentacles with spawned pistol
projectiles are explicit setup fixtures. The tested dynamite comes exclusively
from ordinary player fire input, charge timing and unchanged throw physics.
"""
import argparse
import json
import time
from campaign_session import CampaignSession


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',required=True)
    args=parser.parse_args()
    with CampaignSession(args.report,level=12) as session:
        session.command('invincible 1');session.command('infiniteammo 1')
        session.command('teleport 37154 3570');session.wait('Pazur Aquatis fight started')
        session.command('teleport 37680 3520');time.sleep(.4)
        for x,y in [(37397,3608),(37523,3612),(37648,3614)]:
            for _ in range(3):session.command(f'campaignshot pistol {x-65} {y}');time.sleep(.3)
        session.command('padvirtual attach')
        for _ in range(2):
            session.command('padvirtual button y 1');time.sleep(.15)
            session.command('padvirtual button y 0');time.sleep(.25)
        success=None
        for charge in (2000,1500,1300,1100,1000,700,400):
            session.command('combatkey right 30');time.sleep(.15)
            # Land on the actual narrow post; the earlier x=37750 fixture
            # missed its left edge and tested firing from underwater instead.
            session.command('teleport 37790 3400');time.sleep(1)
            session.command('combatstatus')
            start=len(session.logs())
            session.command('combatkey pistol '+str(charge));time.sleep(charge/1000+3)
            session.capture('charge-'+str(charge))
            if 'Pazur Aquatis crack explosion: accepted' in session.logs()[start:]:
                success=charge;break
        result=dict(passed=success is not None,charge_ms=success,natural_playthrough=False,
                    tested_input='normal player fire, actual charged dynamite throw',
                    setup=['teleports','player protection','infinite ammo','tentacle projectile fixtures'])
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)
        assert result['passed'],'No tested normal throw reached the crack'


if __name__=='__main__':main()
