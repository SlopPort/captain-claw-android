"""Codex: compare support at platform ends, including partial foot overlap.

Isolated real physics; invincibility prevents catch-floor death between cases.
No campaign progress, enemy balance or original-engine parity is inferred.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--report',required=True)
p.add_argument('--expect-flat',action='store_true')
a=p.parse_args()
if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select an allocated device')
apk=installed_apk_sha256();rows=[]
with CampaignSession(a.report,level=1) as s:
    s.command('edgestage');s.command('invincible 1')
    def state():
        start=len(s.logs());s.command('ladderstatus')
        found=re.search(r'ladder status: x=([\d.-]+) y=([\d.-]+) bottom=(-?\d+) climb=(\d) ladder=(\d) ground=(\d) vy=([\d.-]+) animation=(\S+) paused=(\d)',s.logs()[start:])
        assert found,'Missing fresh status'
        x,y,b,c,l,g,vy,anim,pause=found.groups()
        return dict(x=float(x),y=float(y),bottom=int(b),climb=int(c),ladder=int(l),ground=int(g),vy=float(vy),animation=anim)
    for side,edge,sign in [('left',205872,-1),('right',206128,1)]:
        for inset in (20,5,1,-5,-10,-15,-24):
            # Teleport alone preserves fall velocity. Reset the temporary
            # fixture before each placement, or a previous fall can invalidate
            # the next edge observation before its first sampled frame.
            s.command('edgestage');s.command('combatkey release 0');start=edge-sign*inset
            s.command('teleport '+str(start)+' 713');time.sleep(.2)
            before=state();time.sleep(1.2);after=state()
            stable=bool(after['ground'] and abs(after['x']-start)<2 and abs(after['y']-712.6)<2)
            row=dict(side=side,inset=inset,before=before,after=after,stable=stable)
            rows.append(row);print(json.dumps(row),flush=True)
            if a.expect_flat:
                if inset>=-15:assert stable,('Partial foot support lost',row)
                else:assert not stable and after['y']>760,('Outside body still supported',row)
        s.command('edgestage');s.command('teleport '+str(edge+sign*10)+' 713');time.sleep(.2)
        s.command('combatkey down 1000');time.sleep(.7);duck=state()
        row=dict(side=side,duck_partial_overlap=True,after=duck)
        rows.append(row)
        if a.expect_flat:assert duck['ground'] and abs(duck['y']-712.6)<2,('Crouch lost flat foot',row)
        s.command('combatkey release 0')
    assert s.pid in s.process_ids(),'Game exited'
    result=dict(passed=True,apk_sha256=apk,flat_support_required=a.expect_flat,
                invincible_fixture=True,natural_playthrough=False,rows=rows)
result['original_config_and_progress_restored']=True
(s.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
