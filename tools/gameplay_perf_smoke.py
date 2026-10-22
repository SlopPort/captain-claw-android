"""Exercise movement, jump and attacks at a real map start; restore user progress.

App-local input only. Optional labelled real-map teleport/protection fixtures;
defaults use neither. This performance scene is not a playthrough.
"""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--level',type=int,choices=range(1,15),default=9)
    parser.add_argument('--seconds',type=int,default=45)
    parser.add_argument('--report',default='gameplay-perf-0.4.9')
    parser.add_argument('--scene',type=int,nargs=2,metavar=('X','Y'),help='Controlled teleport into existing map geometry')
    parser.add_argument('--protect-player',action='store_true',help='Explicitly labelled player protection for observing enemy attacks')
    parser.add_argument('--observe',action='store_true',help='Observe live enemies without moving or attacking')
    parser.add_argument('--cyclic-pegs',action='store_true',help='Controlled ordinary-jump trials on actual level-one cyclic platforms')
    parser.add_argument('--pair-filter',choices=('on','off'),help='Compare early Box2D pair rejection in the same APK; restores fallback marker')
    parser.add_argument('--expect-logical-size',type=int,nargs=2,metavar=('W','H'),help='Reject comparisons made with another settled viewport')
    args=parser.parse_args()
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=True)
    pair_marker='physics-pairs-unfiltered'
    if args.pair_filter and subprocess.run(['adb','shell','test','-e',REMOTE+pair_marker],capture_output=True).returncode==0:
        raise RuntimeError('Existing pair-filter fallback marker; leave it untouched')
    for name in ('combat-command.txt','combat-response.txt','SAVES.pending.xml','import-transaction'):
        if subprocess.run(['adb','shell','test','-e',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing diagnostic mailbox: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'):adb('pull',REMOTE+name,str(report/name))
    config=ET.parse(report/'config.xml')
    config.find('DebugOptions/SkipMenu').text='true'
    config.find('DebugOptions/SkipMenuToLevel').text=str(args.level)
    flag=config.find('DebugOptions/PreviewIncompleteLevel14')
    if flag is None:flag=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
    flag.text='true' # Opt-in app-local diagnostic input, also on earlier levels.
    for field,value in [('MusicOn','true'),('SoundOn','true'),('Frequency','22050'),('ChunkSize','1024')]:
        config.find('Audio/'+field).text=value
    config.write(report/'test.xml',encoding='utf-8',xml_declaration=True)
    saves=ET.parse(report/'SAVES.XML')
    if not any(level.findtext('LevelNumber')==str(args.level) for level in saves.findall('Level')):
        level=copy.deepcopy(saves.find('Level'));level.find('LevelNumber').text=str(args.level)
        saves.getroot().append(level)
    saves.write(report/'saves-test.xml',encoding='utf-8',xml_declaration=True)
    pid='';ticket=0;actions=[];pair_marker_created=False
    reader=None;log_output=None
    def logs():
        if reader is not None:return (report/'native.log').read_text(encoding='utf-8',errors='replace')
        return adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')
    def command(value):
        nonlocal ticket
        ticket+=1;tag='perf-'+str(ticket)
        (report/'command.tmp').write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(report/'command.tmp'),REMOTE+'combat-command.tmp')
        adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if tag+'|done' in adb('shell','cat',REMOTE+'combat-response.txt',check=False):return
            time.sleep(.1)
        raise RuntimeError('No app-local response: '+value)
    try:
        if args.pair_filter=='off':
            (report/'pair-fallback.tmp').write_bytes(b'')
            pair_marker_created=True
            adb('push',str(report/'pair-fallback.tmp'),REMOTE+pair_marker)
        adb('push',str(report/'test.xml'),REMOTE+'config.xml')
        adb('push',str(report/'saves-test.xml'),REMOTE+'SAVES.XML')
        adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity');time.sleep(2)
        pid=adb('shell','pidof','pl.pazur.port').strip().split()[0]
        # Stream continuously: a twenty-minute run can wrap logcat's ring and
        # invalidate character offsets or silently lose its earliest samples.
        log_output=(report/'native.log').open('wb')
        reader=subprocess.Popen(['adb','logcat','--pid='+pid,'-v','threadtime','-s','SDL/APP','libc','AndroidRuntime'],
                                stdout=log_output,stderr=subprocess.DEVNULL)
        deadline=time.monotonic()+45
        while 'Pazur simulation clock reset' not in logs() and time.monotonic()<deadline:time.sleep(.5)
        assert 'Level loaded !' in logs() and 'Pazur simulation clock reset' in logs(),'Simulation not ready'
        settled=re.findall(r'Pazur viewport: physical=(\d+)x(\d+) logical=(\d+)x(\d+)',logs())
        if args.expect_logical_size:
            assert settled and list(map(int,settled[-1][2:]))==args.expect_logical_size,'Unexpected settled viewport: '+str(settled)
        assert 'Pazur renderer batching: 1' in logs()
        if args.pair_filter:
            assert 'Pazur physics pair filtering: '+('1' if args.pair_filter=='on' else '0') in logs()
        if args.protect_player:command('invincible 1')
        if args.scene:command('teleport '+str(args.scene[0])+' '+str(args.scene[1]));time.sleep(1)
        command('combatstatus');start=len(logs())
        if args.cyclic_pegs:
            assert args.level==1 and not args.protect_player and not args.scene
            for source,target in [((4651,4034),(4545,3971)),((4545,3971),(4453,3902))]:
                before=len(logs())
                command('pegtrial '+' '.join(map(str,(*source,*target))))
                limit=time.monotonic()+12
                while 'Pazur peg result:' not in logs()[before:] and time.monotonic()<limit:time.sleep(.2)
                assert 'Pazur peg result:' in logs()[before:],'No platform trial result'
                command('combatstatus')
                adb('shell','screencap','-p',REMOTE+'level-test.png')
                adb('pull',REMOTE+'level-test.png',str(report/('peg-'+str(source[0])+'.png')))
        battery_before=adb('shell','dumpsys','battery')
        (report/'battery-before.txt').write_text(battery_before,encoding='utf-8')
        measurement_started=time.monotonic()
        deadline=measurement_started+args.seconds
        # Short back-and-forth keeps the player near the spawn platform while
        # scrolling layers, animating, breaking nearby crates and creating shots.
        sequence=[('right',400,.5),('sword',100,.35),('left',400,.5),
                  ('jump',250,1.1),('pistol',100,.35),('down',400,.5)]
        while time.monotonic()<deadline:
            if args.observe:
                time.sleep(.5)
                continue
            for key,duration,wait in sequence:
                if time.monotonic()>=deadline:break
                command('combatkey '+key+' '+str(duration));actions.append(key);time.sleep(wait)
                if len(actions)<=4:command('combatstatus')
        command('combatkey release 0');command('combatstatus')
        log=logs()
        rows=[dict(fps=float(f),p95_ms=int(p),max_ms=int(m)) for f,p,m in re.findall(
            r'Pazur frame sample: fps=([\d.]+) p95=(\d+) ms max=(\d+) ms',log[start:])]
        snapshots=[dict(health=int(h),x=float(x),y=float(y)) for h,x,y in re.findall(
            r'Pazur probe status: claw=(\d+) duck=\d x=([\d.-]+) y=([\d.-]+)',log)]
        moved=bool(snapshots) and any(abs(v['x']-snapshots[0]['x'])>10 or abs(v['y']-snapshots[0]['y'])>10 for v in snapshots)
        alive=pid in adb('shell','pidof','pl.pazur.port',check=False).split()
        passed=alive and (moved or args.observe) and len(rows)>=3 and 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log
        result={'level':args.level,'actions':actions,'frame_samples':rows,'passed':passed,
            'requested_observation_seconds':args.seconds,'measured_observation_seconds':time.monotonic()-measurement_started,
            'observed_positions':snapshots,'movement_observed':moved,
            'fixture':'controlled real-map scene' if args.scene else 'real map start',
            'observation_only':args.observe,'scene':args.scene,
            'early_pair_filtering':args.pair_filter,
            'player_invincible_fixture':args.protect_player,'teleported':bool(args.scene),'ammo_modified':False,
            'apk_sha256':None}
        # A concurrent emulator build can replace the local build output with
        # another ABI. Identify the installed binary, not a workstation path.
        installed=adb('shell','pm','path','pl.pazur.port').strip().splitlines()[0]
        assert installed.startswith('package:'),installed
        adb('pull',installed[len('package:'):],str(report/'installed.apk'))
        result['apk_sha256']=hashlib.file_digest((report/'installed.apk').open('rb'),'sha256').hexdigest()
        result['apk_hash_source']='installed Android package'
        package=adb('shell','dumpsys','package','pl.pazur.port')
        abi=re.search(r'primaryCpuAbi=(\S+)',package)
        result['primary_cpu_abi']=abi[1] if abi else None
        (report/'memory-after.txt').write_text(adb('shell','dumpsys','meminfo','pl.pazur.port'),encoding='utf-8')
        temperature_before=re.search(r'\btemperature:\s*(-?\d+)',battery_before)
        if temperature_before:result['battery_temperature_c_before']=int(temperature_before[1])/10
        battery_after=adb('shell','dumpsys','battery')
        (report/'battery-after.txt').write_text(battery_after,encoding='utf-8')
        temperature=re.search(r'\btemperature:\s*(-?\d+)',battery_after)
        if temperature:result['battery_temperature_c_after']=int(temperature[1])/10
        result['box2d_steps']=[dict(total_ms=float(t),collide_ms=float(c),solve_ms=float(s),toi_ms=float(i),
            other_ms=float(o),bodies=int(b),contacts=int(n)) for t,c,s,i,o,b,n in re.findall(
            r'Pazur Box2D (?:step|slow): total=([\d.]+) collide=([\d.]+) solve=([\d.]+) toi=([\d.]+) other=([\d.]+) ms bodies=(\d+) contacts=(\d+)',log)]
        viewport=re.search(r'Pazur display: physical=(\d+)x(\d+) logical=(\d+)x(\d+)',log)
        if viewport:
            sw,sh,lw,lh=map(int,viewport.groups())
            result.update(startup_surface=[sw,sh],logical_size=[lw,lh])
        viewport_events=[dict(surface=[int(w),int(h)],logical=[int(lw),int(lh)]) for w,h,lw,lh in
                         re.findall(r'Pazur viewport: physical=(\d+)x(\d+) logical=(\d+)x(\d+)',log)]
        result['viewport_events']=viewport_events
        if viewport_events:result['settled_viewport']=viewport_events[-1]
        if args.expect_logical_size:
            during=re.findall(r'Pazur viewport: physical=\d+x\d+ logical=(\d+)x(\d+)',log[start:])
            assert viewport_events and all(list(map(int,v))==args.expect_logical_size for v in during),'Viewport changed during comparison'
        (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        if args.cyclic_pegs:
            trials=re.findall(r'Pazur peg result: landed=(\d) rise=([\d.]+)',log)
            result.update(fixture='actual cyclic platforms; controlled teleport and timed ordinary input',
                teleported=True,peg_trials=[dict(landed=v=='1',rise=float(r)) for v,r in trials])
            result['passed']=passed and len(trials)==2 and all(v=='1' for v,r in trials) and log.count('catnip=0')==2
            (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        adb('shell','screencap','-p',REMOTE+'level-test.png')
        adb('pull',REMOTE+'level-test.png',str(report/'after.png'))
        print(json.dumps(result),flush=True)
        assert result['passed'],'Incomplete trial or crashed process; see report'
    finally:
        if reader is not None:
            reader.terminate();reader.wait(timeout=5);log_output.close()
        elif pid:(report/'native.log').write_text(logs(),encoding='utf-8')
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'):adb('push',str(report/name),REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp'):
            adb('shell','rm','-f',REMOTE+name)
        if pair_marker_created:adb('shell','rm','-f',REMOTE+pair_marker)
        print('Original config and saves restored',flush=True)


if __name__=='__main__':main()
