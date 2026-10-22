"""Verify an installed native ABI in a real process, menu and map transition.

OpenAI Codex implementation. Install the APK with adb --abi beforehand. This
script does not change USB/network settings and restores original user saves.
Level start/exit teleports are fixtures, not natural campaign traversal.
"""
import argparse
import json
import re
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--abi',choices=('armeabi-v7a','arm64-v8a'),required=True)
    args=parser.parse_args()
    package=adb('shell','dumpsys','package','pl.pazur.port')
    assert 'primaryCpuAbi='+args.abi in package,'Installed ABI differs from requested test'
    for menu in (True,False):
        name=args.report+('-menu' if menu else '-level')
        with CampaignSession(name,level=1,start_menu=menu) as session:
            (session.report/'package.txt').write_text(package,encoding='utf-8')
            maps=adb('shell','run-as','pl.pazur.port','cat','/proc/'+session.pid+'/maps')
            (session.report/'process-maps.txt').write_text(maps,encoding='utf-8')
            library_lines=[line for line in maps.splitlines() if 'libopenclaw.so' in line]
            assert library_lines,'Engine absent from process maps'
            expected='/lib/arm/' if args.abi=='armeabi-v7a' else '/lib/arm64/'
            assert any(expected in line for line in library_lines),'Unexpected engine library path'
            session.capture('menu' if menu else 'level-start')
            if not menu:
                session.command('combatjumpmeasure abi-jump')
                session.command('combatkey jump 100');time.sleep(2)
                traces=re.findall(r'Pazur jump trace: label=abi-jump .*rise=([\d.]+).*jumps=(\d+)',session.logs())
                assert traces and float(traces[-1][0])>40 and int(traces[-1][1])==1,traces
                session.command('campaignfinish');session.wait('Score screen initialized OK')
                for _ in range(12):
                    session.command('padvirtual tap 320 240');time.sleep(.35)
                    if 'Level name: Claw - Level 2' in session.logs():break
                session.wait('Level name: Claw - Level 2')
            result=dict(passed=True,abi=args.abi,process_library_verified=True,
                        main_menu=menu,level1_jump_and_exit=not menu,natural_playthrough=False)
            (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            print(json.dumps(result),flush=True)


if __name__=='__main__':main()
