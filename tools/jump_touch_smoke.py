"""Measure real app-local touch latency and jump height; restore user files and display."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET

PORT=Path(__file__).resolve().parents[1]
REMOTE='/sdcard/Android/data/pl.pazur.port/files/'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--baseline',action='store_true')
parser.add_argument('--report',default='jump-touch-0.4.3')
parser.add_argument('--size')
args=parser.parse_args()
REPORT=PORT/'reports'/args.report
REPORT.mkdir(parents=True,exist_ok=True)
def adb(*cmd,check=True):
    return subprocess.run(['adb',*cmd],check=check,capture_output=True,text=True).stdout

original_size=adb('shell','wm','size')
override=re.search(r'Override size: (\d+x\d+)',original_size)
adb('shell','am','force-stop','pl.pazur.port')
for name in ('config.xml','SAVES.XML'): adb('pull',REMOTE+name,str(REPORT/name))
config=ET.parse(REPORT/'config.xml')
config.find('DebugOptions/SkipMenu').text='true'
config.find('DebugOptions/SkipMenuToLevel').text='1'
preview=config.find('DebugOptions/PreviewIncompleteLevel14')
if preview is None: preview=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
preview.text='true'
config.write(REPORT/'config-test.xml',encoding='utf-8',xml_declaration=True)
try:
    if args.size: adb('shell','wm','size',args.size)
    adb('push',str(REPORT/'config-test.xml'),REMOTE+'config.xml')
    adb('logcat','-c')
    output=adb('shell','am','instrument','-w','-r','-e','layout','baseline' if args.baseline else 'final',
               'pl.pazur.port.test/pl.pazur.port.JumpTouchTest')
    (REPORT/'instrumentation.log').write_text(output,encoding='utf-8')
    assert 'INSTRUMENTATION_CODE: 0' in output,output
    log=adb('logcat','-d','-s','SDL/APP','libc','AndroidRuntime')
    (REPORT/'native.log').write_text(log,encoding='utf-8')
    assert 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log
    pattern=r'Pazur jump trace: label=(\S+) queue_ms=(\d+) takeoff_ms=(-?\d+) rise=([\d.]+) hold_ms=(\d+) jumps=(\d+)'
    rows=[dict(label=n,queue_ms=int(q),takeoff_ms=int(t),rise=float(h),effective_hold_ms=int(d),jumps=int(j))
          for n,q,t,h,d,j in re.findall(pattern,log)]
    assert len(rows)==6,rows
    result={'baseline':args.baseline,'size':args.size or 'physical','cases':rows,
        'apk_sha256':hashlib.file_digest((PORT/'app/build/outputs/apk/debug/app-debug.apk').open('rb'),'sha256').hexdigest()}
    if not args.baseline:
        by_name={r['label']:r for r in rows}
        assert all(by_name[n]['rise']>=50 and by_name[n]['jumps']==1 for n in ('hold10','hold100','drift100')),rows
        assert by_name['hold700']['rise']>150 and by_name['hold1800']['jumps']==1,rows
        assert all(0<=r['takeoff_ms']<=65 for r in rows),rows
        drift=log.split('Pazur console command: combatjumpmeasure drift100',1)[1].split('Pazur jump trace: label=drift100',1)[0]
        assert 'attack=1' not in drift and 'fire=1' not in drift,drift
        result['drift_no_unintended_action']=True
        states=[tuple(map(int,v)) for v in re.findall(r'Pazur controls: left=(\d) right=(\d) jump=(\d) attack=(\d) fire=(\d) up=(\d) down=(\d)',log)]
        for state in ((0,1,1,0,0,0,0),(0,0,1,0,0,0,0),(0,0,0,1,0,0,0),(0,0,0,0,1,0,0)):
            assert state in states,(state,states)
        assert states[-1]==(0,0,0,0,0,0,0),states[-4:]
        for name in ('jump-multitouch.png','jump-layout.png','jump-focus.png','jump-pause.png'):
            adb('pull',REMOTE+name,str(REPORT/name))
    result['passed']=True
    (REPORT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)
finally:
    (REPORT/'native.log').write_text(adb('logcat','-d','-s','SDL/APP','libc','AndroidRuntime'),encoding='utf-8')
    adb('shell','am','force-stop','pl.pazur.port')
    if args.size: adb('shell','wm','size',override.group(1) if override else 'reset')
    for name in ('config.xml','SAVES.XML'): adb('push',str(REPORT/name),REMOTE+name)
    for name in ('combat-command.tmp','combat-command.txt','combat-response.txt','jump-multitouch.png','jump-layout.png','jump-focus.png','jump-pause.png'):
        adb('shell','rm','-f',REMOTE+name)
    assert adb('shell','wm','size').strip()==original_size.strip()
    print('Config, saves and display restored',flush=True)
