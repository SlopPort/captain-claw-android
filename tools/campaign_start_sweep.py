"""Load every campaign map with isolated saves and preserve continuous logs.

OpenAI Codex. This verifies startup only, not natural traversal or boss balance.
No global Android input, health edits, teleports or network changes are used.
"""
import argparse
import json
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb,PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--seconds',type=int,default=8)
    args=parser.parse_args()
    rows=[]
    for level in range(1,15):
        with CampaignSession(args.report+'-level'+str(level),level=level) as session:
            session.command('campaignmap');time.sleep(max(3,args.seconds))
            assert session.pid in adb('shell','pidof','pl.pazur.port').split(),'Game exited'
            log=session.logs()
            assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log,'Game crashed'
            memory=adb('shell','dumpsys','meminfo','pl.pazur.port')
            (session.report/'memory.txt').write_text(memory,encoding='utf-8')
            session.capture('start')
            row=dict(level=level,passed=True,natural_playthrough=False,
                     fixtures=['isolated map start'],observed_seconds=max(3,args.seconds))
            (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
            rows.append(row);print(json.dumps(row),flush=True)
    path=PORT/'reports'/(args.report+'-summary.json')
    path.write_text(json.dumps(dict(passed=True,levels=rows),indent=2),encoding='utf-8')


if __name__=='__main__':main()
