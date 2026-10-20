"""Combat fixtures using real game physics and app-local SDL input; restore user files."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import shlex
import subprocess
import time
import xml.etree.ElementTree as ET

PORT = Path(__file__).resolve().parents[1]
REMOTE = '/sdcard/Android/data/pl.pazur.port/files/'
ADB = ['adb']
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mode', choices=['baseline', 'regression', 'enemies'], default='baseline')
parser.add_argument('--report', default='combat-baseline')
parser.add_argument('--indices', nargs='+', type=int)
parser.add_argument('--phase', choices=['both','incoming','outgoing'], default='both')
parser.add_argument('--ranged-fixture', action='store_true', help='Observe actual projectile contacts outside melee range')
args = parser.parse_args()
if args.mode!='enemies' and args.phase!='both': parser.error('--phase is only for --mode enemies')
REPORT = PORT/'reports'/args.report


def adb(*command, check=True):
    return subprocess.run(ADB+list(command),check=check,capture_output=True,text=True).stdout


ticket_number=0

def console(command):
    global ticket_number
    ticket_number+=1
    ticket=str(ticket_number)
    command_file=REPORT/'command.txt'
    command_file.write_text(ticket+'|'+command+'\n',encoding='ascii')
    # One transport round trip; all safety checks still precede writing the mailbox.
    script=f'''[ "$(pidof pl.pazur.port)" = {shlex.quote(pid)} ] || exit 31
dumpsys activity activities | grep -E 'topResumedActivity=|mResumedActivity=|ResumedActivity:' | grep -F 'pl.pazur.port/.GameActivity' >/dev/null || exit 32
printf '%s\\n' {shlex.quote(ticket+'|'+command)} > {REMOTE}combat-command.tmp
mv {REMOTE}combat-command.tmp {REMOTE}combat-command.txt
n=0
while [ "$n" -lt 80 ]; do
 [ "$(cat {REMOTE}combat-response.txt 2>/dev/null)" = {shlex.quote(ticket+'|done')} ] && exit 0
 [ "$(pidof pl.pazur.port)" = {shlex.quote(pid)} ] || exit 33
 sleep 0.1
 n=$((n+1))
done
exit 34
'''
    result=subprocess.run(ADB+['shell','sh'],input=script,text=True,capture_output=True,timeout=20)
    if result.returncode:
        raise RuntimeError(f'App-local command stopped (process/focus/ack check {result.returncode}): {result.stderr}')


def log():
    return adb('logcat','-d','--pid='+pid,'-s','SDL/APP','libc','AndroidRuntime')


def status(query=True):
    assert pid in adb('shell','pidof','pl.pazur.port',check=False).split(), 'Game process exited'
    previous=log().count('Pazur probe status:')
    if query: console('combatstatus')
    text = log()
    if query: assert text.count('Pazur probe status:') > previous, text[-3000:]
    matches = re.findall(r'Pazur probe status: claw=(-?\d+) duck=(\d) x=([\d.-]+) y=([\d.-]+) box=([\d,-]+) target=(\S+) target_id=(\d+) target_hp=(-?\d+) target_max=(-?\d+)',text)
    assert matches, text[-3000:]
    fields=matches[-1]
    return dict(claw=int(fields[0]),duck=int(fields[1]),x=float(fields[2]),y=float(fields[3]),
                box=list(map(int,fields[4].split(','))),target=fields[5],target_id=int(fields[6]),
                target_hp=int(fields[7]),target_max=int(fields[8]))


def stage(index=-1, distance=80, dy=0, passive=False):
    console(f'{"combatdummy" if passive else "combatstage"} {index} {distance} {dy}')
    time.sleep(.45)
    return status(query=False)


def capture(name):
    adb('shell','screencap','-p',REMOTE+'combat-test.png')
    adb('pull',REMOTE+'combat-test.png',str(REPORT/(name+'.png')))


def hitbox_cases():
    results=[]
    for duck in [False,True]:
        for side in ([1,-1] if args.phase!='outgoing' else []):
            for height in [-25,30,65]:
                stage()
                held=None
                try:
                    if duck:
                        console('combatkey down 5000')
                        held=True
                        time.sleep(.25)
                    before=status()
                    console(f'combatshot {height} {side}')
                    time.sleep(.7)
                    row=status()
                    row.update(duck_fixture=duck,duck_before=before['duck'],side=side,height=height)
                    row['expected_health']=100 if height==65 or duck and height==-25 else 90
                    row['passed']=row['claw']==row['expected_health'] and row['duck_before']==int(duck)
                    results.append(row)
                    print(json.dumps(row),flush=True)
                    if height==30 and side==1: capture('duck' if duck else 'standing')
                finally:
                    if held: console('combatkey release 0')
    return results


def enemy_cases():
    inventory=json.loads((PORT/'reports/combat-audit/inventory.json').read_text())
    for index in args.indices if args.indices is not None else range(len(inventory)):
        enemy=inventory[index]
        prototype=enemy['prototype']
        bird=prototype.endswith('_Seagull')
        fish=prototype.endswith('_Fish')
        crab=prototype.endswith('_HermitCrab')
        dy=-150 if bird else 0 if fish else 55-enemy['body']['height']/2
        distance=100 if bird else 50 if fish else 70
        if args.ranged_fixture: distance=250
        row={'index':index,'prototype':prototype,'expected_health':enemy['health'],'incoming':[], 'spawn_health_correct':True}
        adb('logcat','-c')
        for side in ([1,-1] if args.phase!='outgoing' else []):
            console('invincible 0')
            initial=stage(index,side*distance,dy)
            row['spawn_health_correct'] &= initial['target_max']==enemy['max_health'] and initial['target_hp']==enemy['health']
            start=len(log())
            time.sleep(.35)
            state=status()
            evidence=log()[start:]
            hit=state['claw']<100 or 'target=Claw damage=0' in evidence
            if args.ranged_fixture: hit=hit and 'Pazur projectile hit:' in evidence
            for _ in range(4 if args.ranged_fixture else 1):
                if hit: break
                time.sleep(1)
                state=status()
                evidence=log()[start:]
                hit=state['claw']<100 or 'target=Claw damage=0' in evidence
                if args.ranged_fixture: hit=hit and 'Pazur projectile hit:' in evidence
            assert state['claw']>0, 'Player died in incoming fixture; do not revive within the same scene'
            console('invincible 1')
            row['incoming'].append({'side':side,'claw_health':state['claw'],'effect_or_damage':hit,
                                    'attack_frames':evidence.count('Pazur attack frame:'),
                                    'projectile_contacts':evidence.count('Pazur projectile hit:')})
        if args.phase=='incoming':
            row['passed']=row['spawn_health_correct'] and all(r['effect_or_damage'] for r in row['incoming'])
            (REPORT/f'enemy-{index:02d}.log').write_text(log(),encoding='utf-8')
            yield row
            continue
        # Actual player input; protection is limited to these outgoing-attack fixtures.
        outgoing_dy=20 if fish or bird else dy
        initial=stage(index,75,outgoing_dy,passive=not crab)
        row['spawn_health_correct'] &= initial['target_max']==enemy['max_health'] and initial['target_hp']==enemy['health']
        console('invincible 1')
        console('combatkey right 70')
        start=len(log())
        for _ in range(10 if crab else 5):
            console('combatkey sword 50')
            time.sleep(.35)
        state=status()
        evidence=log()[start:]
        for _ in range(8):
            if 'Pazur enemy defeated:' in evidence or 0<=state['target_hp']<enemy['health']: break
            console('combatkey sword 50')
            time.sleep(.35)
            state=status()
            evidence=log()[start:]
        defeated='Pazur enemy defeated:' in evidence
        row['sword']={'target_hp':state['target_hp'],'defeated':defeated,
                      'damage_observed':defeated or 0<=state['target_hp']<enemy['health'],
                      'player_protected':True,'target_offensive_ai_disabled':not crab}
        stage(index,70 if crab else 170,outgoing_dy,passive=not crab)
        console('invincible 1')
        console('combatkey right 70')
        low_target=fish or bird or enemy['body']['height']<=51
        if low_target: console('combatkey down 5500')
        start=len(log())
        for _ in range(10 if crab else 3):
            console('combatkey pistol 50')
            time.sleep(.45)
        state=status()
        evidence=log()[start:]
        for _ in range(12):
            if 'Pazur enemy defeated:' in evidence or 0<=state['target_hp']<enemy['health']: break
            console('combatkey pistol 50')
            time.sleep(.45)
            state=status()
            evidence=log()[start:]
        defeated='Pazur enemy defeated:' in evidence
        row['pistol']={'target_hp':state['target_hp'],'defeated':defeated,
                       'damage_observed':defeated or 0<=state['target_hp']<enemy['health'],
                       'player_protected':True,'target_offensive_ai_disabled':not crab,'crouching':low_target}
        row['passed']=row['spawn_health_correct'] and all(r['effect_or_damage'] for r in row['incoming']) and row['sword']['damage_observed'] and row['pistol']['damage_observed']
        (REPORT/f'enemy-{index:02d}.log').write_text(log(),encoding='utf-8')
        if not row['passed'] or index in [0,13,44]: capture(f'enemy-{index:02d}')
        yield row


REPORT.mkdir(parents=True,exist_ok=True)
(REPORT/'package.json').write_text(json.dumps({
    'apk_sha256':hashlib.file_digest((PORT/'app/build/outputs/apk/debug/app-debug.apk').open('rb'),'sha256').hexdigest(),
    'assets_sha256':hashlib.file_digest((PORT/'build/game-data/ASSETS.ZIP').open('rb'),'sha256').hexdigest(),
    'mode':args.mode,'phase':args.phase,'indices':args.indices,'ranged_fixture':args.ranged_fixture
},indent=2),encoding='utf-8')
adb('shell','am','force-stop','pl.pazur.port')
for name in ['config.xml','SAVES.XML']:
    adb('pull',REMOTE+name,str(REPORT/name))
config=ET.parse(REPORT/'config.xml')
config.find('DebugOptions/SkipMenu').text='true'
fixture_level=1
if args.mode=='enemies':
    inventory=json.loads((PORT/'reports/combat-audit/inventory.json').read_text(encoding='utf-8'))
    selected=args.indices if args.indices is not None else list(range(len(inventory)))
    levels={int(re.search(r'_Level(\d+)_',inventory[i]['prototype'])[1]) for i in selected}
    if len(levels)!=1:
        raise SystemExit('Enemy fixtures must share one source level; use combat_matrix.py for all levels')
    fixture_level=levels.pop()
config.find('DebugOptions/SkipMenuToLevel').text=str(fixture_level)
save=ET.parse(REPORT/'SAVES.XML')
if not any(e.findtext('LevelNumber')==str(fixture_level) for e in save.findall('Level')):
    level=copy.deepcopy(save.find('Level'))
    level.find('LevelNumber').text=str(fixture_level)
    level.find('LevelName').text=f'Combat fixture {fixture_level}'
    for checkpoint in list(level.findall('Checkpoint')):
        if checkpoint.findtext('CheckpointNumber')!='0': level.remove(checkpoint)
    save.getroot().append(level)
save.write(REPORT/'saves-test.xml',encoding='utf-8',xml_declaration=True)
preview=config.find('DebugOptions/PreviewIncompleteLevel14')
if preview is None: preview=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
preview.text='true'
config.find('Audio/MusicOn').text='false'
config.find('Audio/SoundOn').text='false'
config.write(REPORT/'config-test.xml',encoding='utf-8',xml_declaration=True)
results=[]
try:
    adb('push',str(REPORT/'config-test.xml'),REMOTE+'config.xml')
    adb('push',str(REPORT/'saves-test.xml'),REMOTE+'SAVES.XML')
    adb('logcat','-c')
    adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity')
    time.sleep(2)
    pid=adb('shell','pidof','pl.pazur.port').strip().split()[0]
    deadline=time.monotonic()+40
    while 'Level loaded !' not in log() and time.monotonic()<deadline: time.sleep(.5)
    assert 'Level loaded !' in log(),log()[-3000:]
    time.sleep(1)
    console('invincible 0')
    if args.mode in ['baseline','regression']:
        results=hitbox_cases()
        inventory=json.loads((PORT/'reports/combat-audit/inventory.json').read_text())
        index=next(i for i,r in enumerate(inventory) if r['prototype']=='ActorPrototype_Level14_Chameleon')
        stage(index,180)
        console('combatduplicate')
        matches=re.findall(r'Pazur probe duplicate: before=(\d+) first=(\d+) second=(\d+)',log())
        assert matches,log()[-3000:]
        before,first,second=map(int,matches[-1])
        results.append({'case':'duplicate projectile callback','before':before,'first':first,'second':second,
                        'passed':before-first==1 and first==second})
        print(json.dumps(results[-1]),flush=True)
    elif args.mode=='enemies':
        for row in enemy_cases():
            results.append(row)
            (REPORT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
            print(json.dumps(row),flush=True)
    (REPORT/'native.log').write_text(log(),encoding='utf-8')
finally:
    if 'pid' in globals():
        (REPORT/'native.log').write_text(log(),encoding='utf-8')
        (REPORT/'crash.log').write_text(adb('logcat','-d','-b','crash'),encoding='utf-8')
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ['config.xml','SAVES.XML']:
        adb('push',str(REPORT/name),REMOTE+name)
    for name in ['combat-test.png','combat-command.tmp','combat-command.txt','combat-response.txt']:
        adb('shell','rm','-f',REMOTE+name)
    (REPORT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('Config and saves restored',flush=True)
if args.mode in ['regression','enemies'] and not all(row['passed'] for row in results):
    raise SystemExit('Combat regression failed')
