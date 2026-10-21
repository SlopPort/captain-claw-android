"""Sample production ladder physics/animation in an isolated app-local fixture."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',default='ladder-baseline')
    parser.add_argument('--expect-fixed',action='store_true')
    parser.add_argument('--first-map-ladder',action='store_true',help='Check the leftmost ladder cap on the real level 1 map')
    parser.add_argument('--edges',action='store_true',help='Also check falling off both ledge sides and rejection of air jumps')
    parser.add_argument('--bottom',action='store_true',help='Check held Down when a ladder ends on a solid floor')
    parser.add_argument('--idle-edges',action='store_true',help='Measure idle drift near both platform edges; positive inset means the body centre is inside')
    parser.add_argument('--seam-audit',action='store_true',help='Trace short inputs at and beside the actual first ladder cap')
    parser.add_argument('--seam-exits',action='store_true',help='Trace short sideways exits after starting descent at the real cap')
    parser.add_argument('--seam-jumps',action='store_true',help='Trace short/full jumps at and just below the first cap, with late sideways input')
    parser.add_argument('--jump-case',choices=['jump_'+s+'_'+str(h)+'_'+d for s in ('cap','below') for h in (100,250) for d in ('none','left','right')],help='Select one jump trace instead of the full matrix')
    args=parser.parse_args()
    if args.jump_case:args.seam_jumps=True
    if args.seam_audit or args.seam_exits or args.seam_jumps:args.first_map_ladder=True
    if args.idle_edges:args.edges=True
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=True)
    for name in ('combat-command.txt','combat-response.txt'):
        if subprocess.run(['adb','shell','ls',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing diagnostic mailbox: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'):adb('pull',REMOTE+name,str(report/name))
    config=ET.parse(report/'config.xml')
    config.find('DebugOptions/SkipMenu').text='true'
    config.find('DebugOptions/SkipMenuToLevel').text='1'
    flag=config.find('DebugOptions/PreviewIncompleteLevel14')
    if flag is None:flag=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
    flag.text='true'
    config.write(report/'config-test.xml',encoding='utf-8',xml_declaration=True)
    ticket=0;pid='';rows=[];checks_passed=False;log_stream=None;log_output=None;stuck_fall=[]

    def logs():
        if log_stream is not None:return (report/'native-live.log').read_text(encoding='utf-8',errors='replace')
        return adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')

    def command(value):
        nonlocal ticket
        ticket+=1;tag='ladder-'+str(ticket)
        local=report/'command.tmp';local.write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(local),REMOTE+'combat-command.tmp')
        adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if tag+'|done' in adb('shell','cat',REMOTE+'combat-response.txt',check=False):return
            time.sleep(.1)
        raise RuntimeError('No acknowledgement: '+value)

    def sample(label):
        pattern=r'Pazur ladder status: x=([\d.-]+) y=([\d.-]+) bottom=(-?\d+) climb=(\d) ladder=(\d) ground=(\d) vy=([\d.-]+) animation=(\S+) paused=(\d)'
        previous=len(re.findall(pattern,logs()))
        command('ladderstatus')
        deadline=time.monotonic()+3
        matches=list(re.finditer(pattern,logs()))
        while len(matches)<=previous and time.monotonic()<deadline:
            time.sleep(.05);matches=list(re.finditer(pattern,logs()))
        assert len(matches)>previous,'Missing fresh ladder status'
        match=matches[-1]
        x,y,b,c,l,g,v,a,p=match.groups()
        row=dict(label=label,x=float(x),y=float(y),bottom=int(b),climb=int(c),ladder=int(l),ground=int(g),vy=float(v),animation=a,paused=int(p))
        rows.append(row);print(json.dumps(row),flush=True)

    try:
        adb('push',str(report/'config-test.xml'),REMOTE+'config.xml')
        adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity');time.sleep(2)
        pid=adb('shell','pidof','pl.pazur.port').strip().split()[0]
        # Keep the full stream locally: Android's finite log ring can overwrite
        # early cases during a long matrix. Never use string length as a cursor.
        log_output=(report/'native-live.log').open('wb')
        log_stream=subprocess.Popen(['adb','logcat','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime'],
            stdout=log_output,stderr=subprocess.DEVNULL)
        deadline=time.monotonic()+45
        while 'Level loaded !' not in logs() and time.monotonic()<deadline:time.sleep(.5)
        assert 'Level loaded !' in logs()
        time.sleep(.5)
        if args.first_map_ladder:
            command('laddermap')
            caps=[tuple(map(int,r)) for r in re.findall(r'Pazur ladder map: level=1 x=(\d+) top=(\d+) tile=\d+',logs())]
            assert caps,'No real ladder cap found'
            x,top=min(caps)
            command('invincible 1')
            command('teleport '+str(x+32)+' '+str(top-55))
            time.sleep(.8);sample('map_top')
            command('combatkey down 600');time.sleep(.2);sample('map_middle')
            command('combatkey release 0');time.sleep(.1)
            command('combatkey up 2500');time.sleep(1.8);sample('holding_top')
        else:
            x,top=199968,768
            command('ladderstage');time.sleep(.4);sample('bottom')
            command('combatkey up 5500');time.sleep(4);sample('holding_top')
        command('combatkey release 0');time.sleep(.8);sample('released_top')
        command('combatkey up 2000');time.sleep(1);sample('up_again')
        command('combatkey release 0');time.sleep(.5)
        command('combatkey down 600');time.sleep(.2);sample('descending')
        command('combatkey release 0');time.sleep(.2)
        sample('before_ladder_jump')
        command('combatjumpmeasure ladder_jump')
        command('combatkey jump 250');time.sleep(.2);sample('jump_off')
        command('combatkey release 0')
        if args.seam_audit:
            for offset in (-28,-16,0,16,28):
                for direction in ('down','up'):
                    label='seam_'+str(offset)+'_'+direction
                    command('combatkey release 0')
                    command('teleport '+str(x+32+offset)+' '+str(top-55));time.sleep(.8)
                    command('laddertrace '+label+' 2500')
                    command('combatkey '+direction+' 100');time.sleep(.3)
                    command('combatkey release 0');time.sleep(2.2)
                    sample(label)
        if args.seam_exits:
            for duration in (60,100,180):
                for direction in ('left','right'):
                    label='exit_'+str(duration)+'_'+direction
                    command('combatkey release 0')
                    command('teleport '+str(x+32)+' '+str(top-55));time.sleep(.8)
                    command('laddertrace '+label+' 3500')
                    command('combatkey down '+str(duration));time.sleep(.25)
                    command('combatkey '+direction+' 100');time.sleep(.3)
                    command('combatkey release 0');time.sleep(2.7)
                    sample(label)
            # Teleport is only a position change: it deliberately does not
            # rewrite production climbing state. Finish climbing before the
            # unrelated cap walk/jump checks below instead of carrying that
            # test-only state into them.
            command('combatkey up 2000');time.sleep(2.3)
            command('combatkey release 0');time.sleep(.3)
        if args.seam_jumps:
            for start in ('cap','below'):
                for hold in (100,250):
                    for side in ('none','left','right'):
                        label='jump_'+start+'_'+str(hold)+'_'+side
                        if args.jump_case and args.jump_case!=label:continue
                        command('combatkey release 0')
                        command('teleport '+str(x+32)+' '+str(top-55));time.sleep(.4)
                        command('combatkey up 1500');time.sleep(1.7)
                        command('combatkey release 0');time.sleep(.3)
                        if start=='below':
                            command('combatkey down 100');time.sleep(.3)
                            command('combatkey release 0');time.sleep(.2)
                        command('laddertrace '+label+' 4500')
                        command('combatkey jump '+str(hold))
                        # Deliberately later than takeoff, not a simultaneous
                        # button chord: inspect returning beside the cap.
                        if side!='none':command('combatkey '+side+' 100')
                        time.sleep(4.7);sample(label)
            command('teleport '+str(x+32)+' '+str(top-55));time.sleep(.4)
            command('combatkey up 1500');time.sleep(1.7)
            command('combatkey release 0');time.sleep(.3)
        time.sleep(2.3)
        # Further edge cases: horizontal exit and Up+Jump from the cap.
        time.sleep(.5);command('teleport '+str(x+32)+' '+str(top-55));time.sleep(.8)
        command('combatkey right 350');time.sleep(.2);sample('walk_off_top')
        command('combatkey release 0');time.sleep(.5)
        command('teleport '+str(x+32)+' '+str(top-55));time.sleep(.8);sample('before_top_jump')
        command('combatkey up 900');command('combatkey jump 350');time.sleep(.15);sample('up_jump_top')
        command('combatkey release 0')
        if args.expect_fixed:
            by={r['label']:r for r in rows}
            for label in ('holding_top','released_top','up_again'):
                r=by[label];assert not r['climb'] and 'climb' not in r['animation'],r
            assert by['descending']['climb'] and by['descending']['y']>by['released_top']['y']+5,rows
            assert not by['jump_off']['climb'],rows
            # Endpoint screenshots may catch the descent after a successful jump.
            # Use per-frame maximum height instead of comparing late positions.
            trace=re.search(r'Pazur jump trace: label=ladder_jump .*rise=([\d.]+)',logs())
            assert trace and float(trace.group(1))>10,'No upward ladder jump recorded'
            assert by['walk_off_top']['x']>by['released_top']['x']+15 and not by['walk_off_top']['climb'],rows
            assert by['up_jump_top']['y']<by['before_top_jump']['y']-10 and not by['up_jump_top']['climb'],rows
        if args.bottom:
            command('ladderstage');time.sleep(.5)
            command('combatkey up 500');time.sleep(.8);sample('bottom_ascending')
            command('combatkey down 3000');time.sleep(1.6);sample('bottom_holding_down')
            command('combatkey release 0');time.sleep(.4);sample('bottom_released')
            command('combatkey up 500');time.sleep(.25);sample('bottom_up_again')
            command('combatkey release 0')
            by={r['label']:r for r in rows}
            row=by['bottom_holding_down']
            assert row['ground'] and not row['climb'] and 'climb' not in row['animation'],row
            # The isolated floor is at y=1100. A grounded flag alone previously
            # hid penetration below that surface while descent stayed active.
            assert 1095<=row['bottom']<=1102 and abs(row['vy'])<.1,row
            assert by['bottom_up_again']['y']<by['bottom_released']['y']-10,by
        if args.edges:
            command('edgestage')
            for side,start,direction in [('right',206115,'right'),('left',205885,'left')]:
                command('combatkey release 0')
                command('teleport '+str(start)+' 713');time.sleep(.7);sample('edge_'+side+'_stand')
                command('combatkey '+direction+' 300');time.sleep(.12);sample('edge_'+side+'_fall')
                command('combatkey release 0')
                command('combatjumpmeasure air_'+side)
                command('combatkey jump 250');time.sleep(3);sample('edge_'+side+'_land')
                command('combatkey release 0');time.sleep(1)
            by={r['label']:r for r in rows}
            for side in ('right','left'):
                assert by['edge_'+side+'_stand']['ground'],by
                fall=by['edge_'+side+'_fall']
                assert not fall['ground'] and fall['vy']>0 and not fall['climb'],fall
                land=by['edge_'+side+'_land']
                assert land['ground'] and abs(land['y']-2313)<5,land
                trace=re.search(r'Pazur jump trace: label=air_'+side+r' .*rise=([\d.]+).*jumps=(\d+)',logs())
                assert trace and float(trace.group(1))<2 and int(trace.group(2))==0,'Unexpected air jump: '+side
            if args.idle_edges:
                for side,edge,sign in [('right',206128,1),('left',205872,-1)]:
                    for inset in (20,5,1,-1,-5,-15):
                        command('combatkey release 0')
                        start=edge-sign*inset
                        command('teleport '+str(start)+' 713');time.sleep(.15)
                        label='idle_'+side+'_'+str(inset)
                        sample(label+'_before');time.sleep(1.2);sample(label+'_after')
                        row=rows[-1]
                        # Do not call a capsule rolling off after its centre has
                        # crossed the edge an inward-slide bug. Record outside
                        # cases without deciding equivalence with Windows.
                        if inset>0:
                            assert row['ground'] and abs(row['x']-start)<2 and abs(row['y']-712.6)<2,row
        if args.expect_fixed:checks_passed=True
    finally:
        if log_stream is not None:
            log_stream.terminate()
            try:log_stream.wait(timeout=5)
            except subprocess.TimeoutExpired:log_stream.kill();log_stream.wait(timeout=5)
        if log_output is not None:log_output.close()
        native_log=logs() if pid else ''
        if pid:(report/'native.log').write_text(native_log,encoding='utf-8')
        trace_pattern=r'Pazur ladder trace: label=(\S+) tick=(\d+) x=([\d.-]+) y=([\d.-]+) ground=(\d) ladder=(\d) climb=(\d) vx=([\d.-]+) vy=([\d.-]+) animation=(\S+)'
        traces=[dict(label=l,tick=int(t),x=float(x),y=float(y),ground=int(g),ladder=int(a),climb=int(c),
            vx=float(vx),vy=float(vy),animation=anim) for l,t,x,y,g,a,c,vx,vy,anim in re.findall(trace_pattern,native_log)]
        # Candidates are observations, not automatically bugs: a single landing
        # transition can legitimately precede its animation update by one frame.
        stationary_fall=[r for r in traces if 'fall' in r['animation'] and abs(r['vy'])<.01 and abs(r['vx'])<.01]
        streak=None
        for row in traces:
            stationary=row['ground'] and 'fall' in row['animation'] and abs(row['vy'])<.01 and abs(row['vx'])<.01
            if not stationary:streak=None;continue
            if streak is None or streak['label']!=row['label'] or abs(streak['x']-row['x'])>.25 or abs(streak['y']-row['y'])>.25:
                streak=row
            elif row['tick']-streak['tick']>=300 and not any(v['label']==row['label'] for v in stuck_fall):
                stuck_fall.append(dict(label=row['label'],duration_ms=row['tick']-streak['tick'],x=row['x'],y=row['y']))
        if args.expect_fixed and args.seam_jumps and stuck_fall:checks_passed=False
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'):adb('push',str(report/name),REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp'):adb('shell','rm','-f',REMOTE+name)
        (report/'results.json').write_text(json.dumps({'rows':rows,'fixed_assertions_requested':args.expect_fixed,
            'fixed_checks_passed':checks_passed if args.expect_fixed else None,
            'edges_requested':args.edges,'bottom_requested':args.bottom,
            'idle_edges_requested':args.idle_edges,
            'seam_audit_requested':args.seam_audit,
            'seam_exits_requested':args.seam_exits,
            'seam_jumps_requested':args.seam_jumps,
            'trace_samples':len(traces),'trace_labels':sorted({r['label'] for r in traces}),
            'stationary_fall_candidates':stationary_fall,
            'stuck_grounded_fall':stuck_fall,
            'apk_sha256':hashlib.file_digest((PORT/'app/build/outputs/apk/debug/app-debug.apk').open('rb'),'sha256').hexdigest()},indent=2),encoding='utf-8')
    if args.expect_fixed and args.seam_jumps:assert not stuck_fall,stuck_fall


if __name__=='__main__':main()
