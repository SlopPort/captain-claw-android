"""Red Tail effective-delay fixture; OpenAI Codex (LLM), not campaign evidence."""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from enemy_timing_regression import events, assess


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if not os.environ.get("ANDROID_SERIAL"):parser.error("Select the authorized device with ANDROID_SERIAL")
    with CampaignSession(args.report,level=13,apk_support=True) as session:
        session.command('invincible 1')
        session.command('teleport 37176 2021')
        time.sleep(23)
        start=len(session.logs())
        session.command('campaignmap')
        bosses=re.findall(r'kind=boss .*name=(\S+) x=([-\d.]+) y=([-\d.]+) hp=(-?\d+)',session.logs()[start:])
        assert bosses,'No live Red Tail found'
        name,x,y,hp=bosses[-1]
        assert name=='Level13_RedTail',name
        start=len(session.logs())
        session.command(f'campaignposition {float(x)-55} {float(y)-5}')
        time.sleep(7)
        row=assess(events(session.logs()[start:],name,'strike8'),1,50,750,1050)
        row.update(apk_sha256=installed_apk_sha256(),natural_playthrough=False,player_protected=True,boss_hp_edited=False,boss_hp_initial=int(hp))
        (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
