"""Physical debug-recorder checks; controlled wall fixture, never campaign evidence.

OpenAI Codex (LLM). Preserves config/saves and owns only its optional off marker.
Select the allocated device with ANDROID_SERIAL. This takes about two minutes.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from campaign_session import CampaignSession
from gamepad_quit_smoke import adb,REMOTE,PORT


def files():
    result={}
    for kind in ('rolling','event'):
        for slot in (0,1):
            name=f'flight-{kind}-{slot}.txt'
            row=subprocess.run(['adb','exec-out','cat',REMOTE+name],capture_output=True)
            # Some Android exec-out variants return status 0 with cat's missing-file
            # message on stdout. Accept only the recorder's explicit format.
            if row.returncode==0 and row.stdout.startswith(b'Pazur flight recorder 1 '):
                result[name]=row.stdout
    return result


def check_storage(report_name):
    # Exact nonrecursive app-local target; refuse any existing file/directory.
    temporary=REMOTE+'flight-rolling-0.txt.tmp'
    if 'present' in adb('shell','if [ -e '+temporary+' ]; then echo present; fi'):
        raise RuntimeError('Existing writer temporary path; do not remove it')
    owned=False
    try:
        adb('shell','mkdir',temporary);owned=True
        obstruction=PORT/'reports'/(report_name+'-owned-obstruction.txt')
        obstruction.write_text('owned write-failure fixture',encoding='ascii')
        adb('push',str(obstruction),temporary+'/owned-obstruction.txt')
        with CampaignSession(report_name+'-storage',level=2,diagnostics=False) as session:
            time.sleep(12)
            log=session.logs()
            assert log.count('Pazur recorder: local write failed; gameplay continues')==1
            assert session.process_ids(),'Game exited on write failure'
            before=files().get('flight-rolling-0.txt')
            adb('shell','rm','-f',temporary+'/owned-obstruction.txt')
            adb('shell','rmdir',temporary,check=False);owned=False
            time.sleep(7)
            after=files().get('flight-rolling-0.txt')
            assert after and after!=before and after.endswith(b'end\n'),'Writer did not recover'
            result=dict(passed=True,injected_failure='temporary path is an owned directory',
                        real_disk_full=False,one_warning=True,game_survived=True,recovered=True)
            (session.report/'results.json').write_text(json.dumps(result,indent=2))
            print(json.dumps(result),flush=True)
    finally:
        if owned:
            adb('shell','rm','-f',temporary+'/owned-obstruction.txt')
            adb('shell','rmdir',temporary,check=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True)
    parser.add_argument('--storage-only',action='store_true')
    args=parser.parse_args()
    if not os.environ.get('ANDROID_SERIAL'):raise RuntimeError('Select allocated device')
    if args.storage_only:
        check_storage(args.report);return
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=False)
    marker='flight-recorder-off'
    if 'present' in adb('shell','if [ -e '+REMOTE+marker+' ]; then echo present; fi'):
        raise RuntimeError('Existing off marker: leave its owner in control')
    owned=False;results={}
    try:
        for enabled,seconds in [(False,25),(True,70)]:
            if not enabled:
                (report/'off-marker').write_bytes(b'recorder-check')
                adb('push',str(report/'off-marker'),REMOTE+marker);owned=True
            elif owned:
                adb('shell','rm','-f',REMOTE+marker);owned=False
            previous=files()
            with CampaignSession(args.report+('-on' if enabled else '-off'),level=2) as session:
                session.command('campaignposition 2460 4900');time.sleep(.6)
                session.command('combatkey right 3500')
                session.command('benchmarkquiet')
                # Ordinary inputs expire without further mailbox commands. Quiet
                # mode leaves the combat diagnostics flag false while recording.
                time.sleep(seconds)
                current=files()
                log=session.logs()
                fps=[float(v) for v in re.findall(r'frame sample: fps=([\d.]+)',log)]
                p95=[int(v) for v in re.findall(r'frame sample: fps=[\d.]+ p95=(\d+)',log)]
                row=dict(seconds=seconds,fps_last=fps[-4:],p95_ms_last=p95[-4:])
                if not enabled:
                    assert previous==current,'Disabled recorder changed report files'
                    row['no_writes']=True
                else:
                    assert 3<=len(current)<=4,'Expected rolling slots and a candidate report'
                    assert all(f'flight-rolling-{slot}.txt' in current for slot in (0,1))
                    parsed={}
                    for name,data in current.items():
                        assert data.startswith(b'Pazur flight recorder 1 ') and data.endswith(b'end\n')
                        samples=[v.split() for v in data.decode().splitlines() if v.startswith('S ') and not v.startswith('S tick')]
                        assert 0<len(samples)<=600 and len(data)<1024*1024
                        assert all(int(v[-1])<=8 for v in samples)
                        parsed[name]=dict(samples=len(samples),bytes=len(data),first_tick=int(samples[0][1]),last_tick=int(samples[-1][1]))
                        (report/name).write_bytes(data)
                    assert any(v['samples']==600 for k,v in parsed.items() if 'rolling' in k),'Ring did not fill'
                    assert any(b'reason=blocked-candidate' in v for k,v in current.items() if 'event' in k),'No candidate freeze'
                    assert any(int(v.split()[9])&2 for data in current.values() for v in data.decode().splitlines() if v.startswith('S ') and not v.startswith('S tick')),'Right input not recorded'
                    row['files']=parsed
                results['on' if enabled else 'off']=row
                print(json.dumps(dict(enabled=enabled,**row)),flush=True)
    finally:
        if owned:adb('shell','rm','-f',REMOTE+marker)
    results.update(passed=True,natural_campaign=False,apk_sha256=hashlib.sha256((PORT/'app/build/outputs/apk/debug/app-debug.apk').read_bytes()).hexdigest())
    (report/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')


if __name__=='__main__':main()
