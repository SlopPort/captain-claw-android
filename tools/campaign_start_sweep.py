"""Load every campaign map with isolated saves and preserve continuous logs.

OpenAI Codex. This verifies startup only, not natural traversal or boss balance.
No global Android input, in-action health edits, teleports or network changes.
Each map starts with an isolated checkpoint-zero save: HP 100, three lives,
10 bullets, five magic shots and three dynamite; user progress is restored.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256
from gamepad_quit_smoke import adb,PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--seconds',type=int,default=8)
    parser.add_argument('--expect-logical-size',type=int,nargs=2,metavar=('W','H'))
    parser.add_argument('--production',action='store_true',help='Disable the preview flag and diagnostic mailbox; no campaignmap command')
    parser.add_argument('--levels',type=int,nargs='+',default=list(range(1,15)))
    args=parser.parse_args()
    assert all(1<=level<=14 for level in args.levels),'Invalid campaign map'
    rows=[]
    apk_sha256=installed_apk_sha256()
    for level in args.levels:
        with CampaignSession(args.report+'-level'+str(level),level=level,diagnostics=not args.production) as session:
            if not args.production:session.command('campaignmap')
            time.sleep(max(3,args.seconds))
            assert session.pid in session.process_ids(),'Game exited'
            log=session.logs()
            assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log,'Game crashed'
            if args.production:
                assert 'Pazur console command:' not in log,'Unexpected diagnostic command'
                assert 'NOT LOADED:' not in log and 'LEVEL14 PREVIEW:' not in log,'Unimplemented level actor'
            viewports=re.findall(r'Pazur viewport: physical=(\d+)x(\d+) logical=(\d+)x(\d+)',log)
            if args.expect_logical_size:
                assert viewports and list(map(int,viewports[-1][2:]))==args.expect_logical_size,viewports
            memory=adb('shell','dumpsys','meminfo','pl.pazur.port')
            (session.report/'memory.txt').write_text(memory,encoding='utf-8')
            session.capture('start')
            row=dict(level=level,passed=True,natural_playthrough=False,
                     apk_sha256=apk_sha256,preview_diagnostics=not args.production,
                     viewport_events=viewports,
                     fixtures=['isolated map start'],observed_seconds=max(3,args.seconds))
            assert installed_apk_sha256()==apk_sha256,'Package changed during map sweep'
            (session.report/'results.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
            rows.append(row);print(json.dumps(row),flush=True)
    path=PORT/'reports'/(args.report+'-summary.json')
    path.write_text(json.dumps(dict(passed=True,levels=rows),indent=2),encoding='utf-8')


if __name__=='__main__':main()
