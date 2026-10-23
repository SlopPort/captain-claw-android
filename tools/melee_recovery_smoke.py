"""Codex: real enemy hit, ordinary 100 ms tap, recovery and attack traces.

Active Soldier on an isolated 32 px step. No protection/healing during action.
This checks tap handling, not original balance or natural terrain certification.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from vertical_combat_smoke import state
from gamepad_quit_smoke import PORT

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--report',required=True)
a=p.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select an allocated device')
index=re.findall(r'ActorPrototype_\w+',(PORT/'native/CombatPrototypes.h').read_text()).index('ActorPrototype_Level1_Soldier')
apk=installed_apk_sha256()
for side in (-1,1):
    with CampaignSession(a.report+'-'+str(side),level=1) as s:
        # Face the enemy before it exists. A tiny direction tap during hurt
        # can itself be rejected; do not mistake facing away for a hitbox miss.
        s.command('combatkey '+('left' if side<0 else 'right')+' 100')
        time.sleep(.25)
        s.command('combatstairs '+str(index)+' '+str(side*80)+' 32')
        initial=state(s);start=len(s.logs())
        s.command('combatmeleeafterhit');time.sleep(2)
        final=state(s);log=s.logs()[start:]
        assert 'Pazur melee after hit: sent hp=' in log,'No observed live enemy hit'
        assert 'Pazur melee buffer: queued during hurt' in log,'Tap did not enter hurt buffer'
        assert 'Pazur melee buffer: consumed after hurt' in log,'Tap lost before recovery'
        sources=[int(n) for n in re.findall(r'Pazur area requested: source=(\d+)',log)]
        assert any(n!=initial['enemy_actor_id'] for n in sources),'No post-recovery attack area'
        assert re.search(r'Pazur area contact: source=(\d+) target=Soldier ',log),'No verified sword contact with Soldier'
        row=dict(side=side,initial=initial,final=final,tap_buffered=True,tap_consumed=True,
                 target_loss_observed=final['enemy_hp']<initial['enemy_hp'],natural_playthrough=False)
    (s.report/'results.json').write_text(json.dumps(dict(passed=True,apk_sha256=apk,case=row,original_config_and_progress_restored=True),indent=2),encoding='utf-8')
    print(json.dumps(row),flush=True)
