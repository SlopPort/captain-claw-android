"""Compare SDL batching off/on/off on one APK; restore the device opt-out file.

Same map-start fixture, display, sound and data in each run. Alternating repeats
help expose drift but do not establish a thermal steady state or full-map FPS.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

PORT=Path(__file__).resolve().parents[1]
REMOTE='/sdcard/Android/data/pl.pazur.port/files/render-batching-off'


def adb(*args,check=True):
    return subprocess.run(['adb',*args],check=check,capture_output=True,text=True).stdout


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--levels',type=int,nargs='+',choices=range(1,15),default=[8,9,13])
    parser.add_argument('--hold-seconds',type=int,default=35)
    parser.add_argument('--report',default='render-batch-ab')
    args=parser.parse_args()
    report=PORT/'reports'/args.report
    report.mkdir(parents=True,exist_ok=True)
    existed=subprocess.run(['adb','shell','test','-e',REMOTE],capture_output=True).returncode==0
    backup=report/'original-opt-out'
    if existed:adb('pull',REMOTE,str(backup))
    rows=[]
    try:
        for index,mode in enumerate(('off','on','off')):
            adb('shell','am','force-stop','pl.pazur.port')
            if mode=='off':
                marker=report/'opt-out';marker.write_bytes(b'device benchmark\n')
                adb('push',str(marker),REMOTE)
            else:adb('shell','rm','-f',REMOTE)
            name=args.report+'-'+str(index)+'-'+mode
            battery=adb('shell','dumpsys','battery')
            command=[sys.executable,'-B',str(PORT/'tools/level_boot_smoke.py'),
                '--levels',*map(str,args.levels),'--frequency','22050','--effects-on',
                '--hold-seconds',str(args.hold_seconds),'--report',name,
                '--expect-log','Pazur renderer batching: '+('1' if mode=='on' else '0')]
            subprocess.run(command,cwd=PORT,check=True,env=os.environ.copy())
            data=json.loads((PORT/'reports'/name/'results.json').read_text(encoding='utf-8'))
            rows.append({'mode':mode,'battery_before':battery,'levels':data})
            (report/'results.json').write_text(json.dumps({'runs':rows,
                'apk_sha256':hashlib.file_digest((PORT/'app/build/outputs/apk/debug/app-debug.apk').open('rb'),'sha256').hexdigest()},indent=2),encoding='utf-8')
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        if existed:adb('push',str(backup),REMOTE)
        else:adb('shell','rm','-f',REMOTE)
        print('Original renderer opt-out restored',flush=True)


if __name__=='__main__':main()
