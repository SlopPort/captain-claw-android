"""Compare GPU pixels of original/atlas tiles, then verify atlas memory release.

OpenAI Codex. Isolated map start; no controller/global input or gameplay health
edits. Explicit diagnostic rendering/readback, not a gameplay FPS measurement.
"""
import argparse
import json
import re
import time
from android_package import installed_apk_sha256
from campaign_session import CampaignSession


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--levels',nargs='+',type=int,choices=range(1,15),default=[1,9,14])
    args=parser.parse_args();apk=installed_apk_sha256()
    for level in args.levels:
        with CampaignSession(args.report+'-level'+str(level),level=level) as session:
            start=len(session.logs());session.command('tileatlas 1');time.sleep(2)
            session.command('tileatlas validate')
            session.wait('Pazur tile atlas validation:',after=start)
            log=session.logs()[start:]
            builds=[dict(plane=n,sources=int(c),width=int(w),height=int(h),bytes=int(b),held=int(total))
                    for n,c,w,h,b,total in re.findall(r'Pazur tile atlas built: plane=(\S+) sources=(\d+) size=(\d+)x(\d+) bytes=(\d+) held=(\d+)',log)]
            pixels=[dict(plane=n,compared=int(c),mismatches=int(m))
                    for n,c,m in re.findall(r'Pazur tile atlas pixels: plane=(\S+) compared=(\d+) mismatches=(\d+)',log)]
            summaries=re.findall(r'Pazur tile atlas validation: tested=(\d+) passed=(\d+) held=(\d+)',log)
            result=dict(passed=False,level=level,apk_sha256=apk,builds=builds,pixels=pixels,
                        natural_playthrough=False,diagnostic_gpu_readback=True)
            (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            assert builds and pixels and summaries,'No atlas pixel evidence'
            assert int(summaries[-1][0])>0 and summaries[-1][0]==summaries[-1][1],summaries
            assert all(row['mismatches']==0 and row['compared']>0 for row in pixels),pixels
            assert all(row['held']<=16*1024*1024 and row['bytes']<=8*1024*1024 for row in builds)
            before=len(session.logs());session.command('tileatlas 0');session.command('tileatlas validate')
            session.wait('Pazur tile atlas validation:',after=before)
            assert 'Pazur tile atlas validation: tested=0 passed=0 held=0' in session.logs()[before:],'Atlas memory retained after disabling'
            assert installed_apk_sha256()==apk,'Package changed during pixel comparison'
            result.update(passed=True,memory_released_on_disable=True)
            (session.report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            print(json.dumps(result),flush=True)


if __name__=='__main__':main()
