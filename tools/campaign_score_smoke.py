"""Collect the real level-one end item, then test touch-only score progression.

Explicit fixture: teleports to an existing pickup. Not a natural playthrough.
"""
import argparse
import hashlib
import json
import time
import xml.etree.ElementTree as ET
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb, REMOTE, PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--level',type=int,choices=(1,3,5,7,9,11),default=1)
    parser.add_argument('--expect-blocked',action='store_true')
    args=parser.parse_args();result={}
    next_level=args.level+1
    marker='Level name: Claw - Level '+str(next_level)
    with CampaignSession(args.report,level=args.level) as session:
        session.command('campaignmap')
        before=len(session.logs())
        session.command('campaignfinish')
        session.wait('Score screen initialized OK',after=before)
        # Let the score intro request its regional voice line before skipping.
        time.sleep(8)
        session.capture('score-before')
        for _ in range(12):
            session.command('padvirtual tap 320 240');time.sleep(.35)
            if marker in session.logs()[before:]:break
        if not args.expect_blocked:session.wait(marker,after=before)
        time.sleep(2);session.capture('score-after')
        advanced=marker in session.logs()[before:]
        adb('pull',REMOTE+'SAVES.XML',str(session.report/'progress.xml'))
        save=ET.parse(session.report/'progress.xml')
        unlocked=any(v.findtext('LevelNumber')==str(next_level) and v.find("Checkpoint/CheckpointNumber").text=='0' for v in save.findall('Level'))
        result=dict(start_level=args.level,next_level=next_level,next_level_loaded=advanced,next_level_saved=unlocked,touch_block_expected=args.expect_blocked,
            passed=unlocked and advanced!=args.expect_blocked,
            fixture='teleport to existing end pickup; app-local SDL mouse events',natural_playthrough=False,
            apk_sha256=hashlib.file_digest((PORT/'app/build/outputs/apk/debug/app-debug.apk').open('rb'),'sha256').hexdigest())
        (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result),flush=True)
        assert result['passed'],result


if __name__=='__main__':main()
