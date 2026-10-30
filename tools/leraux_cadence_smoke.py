"""Measure real Le Rauxe cadence and ordinary sword damage in a saved fixture.

OpenAI Codex (LLM). Teleport and player invincibility are setup, not campaign or
original-parity evidence. Boss HP is never edited. User files are restored.
"""
import argparse,json,re,time,statistics
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from enemy_timing_regression import events


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);a=p.parse_args()
 with CampaignSession(a.report,level=2,apk_support=True) as s:
  s.command('invincible 1');s.command('teleport 23642 3954');time.sleep(23)
  def boss():
   start=len(s.logs());s.command('campaignmap')
   matches=re.findall(r'kind=boss .*name=(\S+) x=([-\d.]+) y=([-\d.]+) hp=(-?\d+)',s.logs()[start:]);assert matches
   name,x,y,hp=matches[-1];return dict(name=name,x=float(x),y=float(y),hp=int(hp))
  initial=boss();s.command(f"campaignposition {initial['x']-65} {initial['y']-5}")
  start=len(s.logs());time.sleep(9)
  observed=s.logs()[start:];times=[]
  for line in observed.splitlines():
   if 'Pazur attack frame: actor=Level2_LaRaux' in line:
    match=re.search(r'\d\d-\d\d (\d+):(\d+):([\d.]+)',line);h,m,sec=map(float,match.groups());times.append(h*3600+m*60+sec)
  # Debug37 uses the original event-1 frame (4), after its port-specific delay.
  cycle=None;emissions=[]
  for kind,tick,value in events(observed,'Level2_LaRaux','strike'):
   if kind=='cycle':cycle=(tick,value)
   elif cycle:
    elapsed=tick-cycle[0]
    assert value==4 and 300<=cycle[1]<=600,(cycle,value)
    assert cycle[1]+205<=elapsed<=cycle[1]+335,(cycle,elapsed)
    emissions.append(dict(delay_ms=cycle[1],elapsed_ms=elapsed,frame=value));cycle=None
  assert len(emissions)>=4,emissions
  intervals=[b-a for a,b in zip(times,times[1:])]
  assert len(intervals)>=4,intervals
  assert .6<statistics.median(intervals)<1.2,intervals
  before=boss();s.command('combatkey right 20');time.sleep(.08);s.command('combatkey down 6000')
  for i in range(10):
   if i==5:s.command('combatkey down 6000')
   s.command('combatkey sword 80');time.sleep(.55)
  after=boss();assert after['hp']<before['hp'],(before,after)
  result=dict(passed=True,apk_sha256=installed_apk_sha256(),natural_playthrough=False,player_protected=True,boss_hp_edited=False,emission_timing=emissions,intervals=intervals,median_interval_s=statistics.median(intervals),before=before,after=after,parry_probabilities_changed=False,original_exact_cadence_verified=False)
  (s.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
