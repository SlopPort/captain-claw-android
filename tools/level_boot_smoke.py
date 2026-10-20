"""Device level/music smoke tests using temporary save/config fixtures."""
from pathlib import Path
import argparse
import copy
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET

PORT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--frequency', type=int, default=44100)
parser.add_argument('--effects-on', action='store_true', help='Include sound effects; PCM is then not isolated to music')
parser.add_argument('--combat-audit', action='store_true', help='Read actual regular-enemy health and body bounds at map load')
parser.add_argument('--report', default='level-boot')
parser.add_argument('--hold-seconds', type=int, default=16)
parser.add_argument('--levels', nargs='+', type=int, default=[1,2,3])
parser.add_argument('--display-size', help='Temporary Android display size, e.g. 720x1280; restored afterwards')
parser.add_argument('--preview-level14', action='store_true', help='Enable level 14 diagnostics (legacy flag name)')
parser.add_argument('--teleport', nargs=2, type=int, metavar=('X', 'Y'), help='Controlled collision fixture; requires one preview level')
parser.add_argument('--expect-log', action='append', default=[], help='Require this literal marker in final process log; repeatable')
parser.add_argument('--reject-log', action='append', default=[], help='Reject this literal marker in final process log; repeatable')
parser.add_argument('--attack-count', type=int, default=0, choices=range(0, 31), help='Send this many real melee key presses in preview mode')
parser.add_argument('--omar-reset', action='store_true', help='After one real hit, kill the player on lava and verify a fresh attempt')
parser.add_argument('--omar-fight', action='store_true', help='Controlled real-input boss encounter: console teleport/powerups, no direct boss health edits')
parser.add_argument('--invincible-fixture', action='store_true', help='Protect only the player during a controlled preview combat test')
args = parser.parse_args()
if args.teleport and (args.levels != [14] or not args.preview_level14):
    parser.error('--teleport requires --levels 14 --preview-level14')
if args.attack_count and (args.levels != [14] or not args.preview_level14):
    parser.error('--attack-count requires --levels 14 --preview-level14')
if args.invincible_fixture and not args.teleport:
    parser.error('--invincible-fixture requires a controlled --teleport preview fixture')
if args.omar_reset and not args.omar_fight:
    parser.error('--omar-reset requires --omar-fight')
if args.omar_fight and not (args.teleport and args.invincible_fixture):
    parser.error('--omar-fight requires the protected, controlled teleport fixture')
REPORT = PORT / 'reports' / args.report
REMOTE = '/sdcard/Android/data/pl.pazur.port/files/'
ADB = ['adb']


def adb(*args, check=True):
    return subprocess.run(ADB + list(args), check=check, capture_output=True, text=True)


def fight_omar(pid):
    def logs():
        return adb('logcat', '-d', '--pid='+pid, '-s', 'SDL/APP', 'libc', 'AndroidRuntime').stdout
    def console(command):
        adb('shell', 'input', 'keyevent', '68')
        time.sleep(.2)
        adb('shell', 'input', 'keyevent', '67')
        adb('shell', 'input', 'text', command.replace(' ', '%s'))
        adb('shell', 'input', 'keyevent', '66')
        time.sleep(.2)
        adb('shell', 'input', 'keyevent', '68')
        time.sleep(.3)
    def capture(name):
        adb('shell', 'screencap', '-p', REMOTE+'level-test.png')
        adb('pull', REMOTE+'level-test.png', str(REPORT/(name+'.png')))
    deadline = time.monotonic()+30
    while 'Pazur Omar fight started' not in logs() and time.monotonic() < deadline: time.sleep(.5)
    if 'Pazur Omar fight started' not in logs(): raise RuntimeError('Boss staging did not finish')
    capture('arena-staging')
    console('teleport 42300 2350')
    console('infiniteammo 1')
    adb('shell', 'input', 'keyevent', '--duration', '80', '21')
    capture('arena-console-teleport')
    for power, health in [('frostsword',175),('firesword',150),('frostsword',125),('firesword',100)]:
        console(power)
        deadline = time.monotonic()+28
        marker = f'->{health} bullets=0'
        while marker not in logs() and time.monotonic()<deadline:
            adb('shell','input','keyevent','--longpress','113')
            time.sleep(.2)
        capture(f'omar-health-{health}')
        (REPORT/'encounter-progress.log').write_text(logs(),encoding='utf-8')
        if marker not in logs(): raise RuntimeError(f'No actual elemental hit to health {health}')
        time.sleep(1)
        if args.omar_reset:
            console('invincible 0')
            console('teleport 41650 2800')
            deadline = time.monotonic()+25
            while time.monotonic()<deadline:
                tail = logs().split('Pazur Omar reset')
                if len(tail)>1 and 'Pazur Omar fight started' in tail[-1]: break
                time.sleep(.5)
            capture('omar-reset-after-death')
            (REPORT/'encounter-progress.log').write_text(logs(),encoding='utf-8')
            if 'Pazur Omar reset' not in logs() or 'Pazur Omar fight started' not in logs().split('Pazur Omar reset')[-1]:
                raise RuntimeError('Boss attempt did not reset after a real player death')
            return
    # Let the elemental sword expire; phase two uses the ordinary duck sword.
    time.sleep(31)
    for round in range(4):
        x = 42320 if round % 2 == 0 else 42090
        console(f'teleport {x} 1900')
        # Face right before firing at the boss standing on the platform.
        adb('shell','input','keyevent','--duration','70','22' if round % 2 == 0 else '21')
        time.sleep(.3)
        base = len(logs())
        target = 75-round*25
        deadline = time.monotonic()+25
        while f'->{target} bullets=0' not in logs()[base:] and time.monotonic()<deadline:
            current = logs()[base:]
            if 'bullets=3' not in current or current.rfind('opening closed') > current.rfind('bullets=3'):
                adb('shell','input','keyevent','--longpress','57')
                time.sleep(.35)
            else:
                held = subprocess.Popen(ADB+['shell','input','keyevent','--duration','1500','20'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                time.sleep(.25)
                adb('shell','input','keyevent','--longpress','113')
                held.communicate(timeout=5)
                time.sleep(.3)
        capture(f'omar-duck-round-{round}')
        (REPORT/'encounter-progress.log').write_text(logs(),encoding='utf-8')
        if f'->{target} bullets=0' not in logs()[base:]: raise RuntimeError(f'No actual duck hit to health {target}')
    time.sleep(9)
    capture('finale-amulet')
    time.sleep(11)
    capture('finale-score')
    for _ in range(8):
        adb('shell','input','keyevent','62')
        time.sleep(.35)
        tail = logs().split('Score screen initialized OK')[-1]
        if 'Changing to: 3' in tail: break
    if 'Changing to: 3' not in logs().split('Score screen initialized OK')[-1]:
        raise RuntimeError('Final score did not return to menu')
    capture('finale-menu')
    (REPORT/'encounter-progress.log').write_text(logs(),encoding='utf-8')
    if 'Pazur finale complete' not in logs(): raise RuntimeError('Finale did not complete via real input')


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    if args.display_size and not re.fullmatch(r'[1-9][0-9]*x[1-9][0-9]*', args.display_size):
        raise ValueError('Invalid display size')
    original_display = adb('shell', 'wm', 'size').stdout
    previous_override = re.search(r'Override size:\s*(\d+x\d+)', original_display)
    if (args.teleport or args.combat_audit) and adb('shell', 'ls', REMOTE+'startup_commands.txt', check=False).returncode == 0:
        raise RuntimeError('Existing startup commands: preserve them before running this test')
    adb('shell', 'am', 'force-stop', 'pl.pazur.port')
    adb('pull', REMOTE+'config.xml', str(REPORT/'config-before.xml'))
    adb('pull', REMOTE+'SAVES.XML', str(REPORT/'saves-before.xml'))
    save = ET.parse(REPORT/'saves-before.xml')
    template = save.find('./Level')
    if template is None:
        raise RuntimeError('No checkpoint fixture available')
    for number in args.levels:
        if not any(n.findtext('LevelNumber') == str(number) for n in save.findall('./Level')):
            level = copy.deepcopy(template)
            level.find('LevelNumber').text = str(number)
            level.find('LevelName').text = f'Test level {number}'
            for checkpoint in list(level.findall('Checkpoint')):
                if checkpoint.findtext('CheckpointNumber') != '0': level.remove(checkpoint)
            save.getroot().append(level)
    save.write(REPORT/'saves-test.xml', encoding='utf-8', xml_declaration=True)
    results = []
    fixture_created = False
    try:
        if args.display_size:
            adb('shell', 'wm', 'size', args.display_size)
        if args.teleport or args.combat_audit:
            fixture = REPORT/'startup_commands.txt'
            commands = 'invincible 1\n' if args.invincible_fixture else ''
            if args.teleport: commands += f'teleport {args.teleport[0]} {args.teleport[1]}\n'
            if args.combat_audit: commands += 'combatmap\n'
            fixture.write_text(commands, encoding='ascii')
            adb('push', str(fixture), REMOTE+'startup_commands.txt')
            fixture_created = True
        adb('push', str(REPORT/'saves-test.xml'), REMOTE+'SAVES.XML')
        for number in args.levels:
            config = ET.parse(REPORT/'config-before.xml')
            config.find('DebugOptions/SkipMenu').text = 'true'
            config.find('DebugOptions/SkipMenuToLevel').text = str(number)
            if args.combat_audit or args.preview_level14 and number == 14:
                preview_flag=config.find('DebugOptions/PreviewIncompleteLevel14')
                if preview_flag is None: preview_flag=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
                preview_flag.text='true'
            config.find('Audio/MusicOn').text = 'true'
            config.find('Audio/MusicVolume').text = '15'
            config.find('Audio/Frequency').text = str(args.frequency)
            config.find('Audio/ChunkSize').text = str(1024 if args.frequency == 22050 else args.frequency // 22)
            # Isolate synthesized music when checking non-zero PCM output.
            config.find('Audio/SoundOn').text = 'true' if args.effects_on else 'false'
            config.write(REPORT/f'config-{number}.xml', encoding='utf-8', xml_declaration=True)
            adb('shell', 'am', 'force-stop', 'pl.pazur.port')
            adb('push', str(REPORT/f'config-{number}.xml'), REMOTE+'config.xml')
            adb('shell', 'am', 'start', '-n', 'pl.pazur.port/.LauncherActivity')
            time.sleep(1)
            pid = adb('shell', 'pidof', 'pl.pazur.port').stdout.strip().split()[0]
            deadline = time.monotonic() + 40
            log = ''
            while time.monotonic() < deadline:
                time.sleep(1)
                log = adb('logcat', '-d', '--pid='+pid, '-s', 'SDL/APP', 'libc', 'AndroidRuntime').stdout
                if 'Level loaded !' in log and 'Pazur audio PCM: peak=' in log: break
                if 'Fatal signal' in log or 'FATAL EXCEPTION' in log: break
            (REPORT/f'level-{number}.log').write_text(log, encoding='utf-8')
            loaded = 'Level loaded !' in log
            music = 'playing=1 paused=0' in log and 'Pazur audio PCM: peak=' in log
            preview = args.preview_level14 and number == 14
            result = {'level': number, 'loaded': loaded, 'music_pcm': music, 'pid': pid,
                      'mode': 'controlled_level14' if preview else 'normal'}
            result['pcm_isolated_to_music'] = not args.effects_on
            if args.teleport: result['teleport_fixture'] = args.teleport
            result['player_invincible_fixture'] = args.invincible_fixture
            if args.combat_audit:
                result['mode']='normal_combat_audit'
                scanned=re.findall(r'Pazur map enemy: actor=(\S+) id=(\d+) hp=(-?\d+) max=(\d+) x=([\d.-]+) y=([\d.-]+) box=([\d,-]+)',log)
                result['enemy_scan']=[{'actor':n,'id':int(i),'health':int(h),'max_health':int(m),
                                       'x':float(x),'y':float(y),'body':list(map(int,b.split(',')))} for n,i,h,m,x,y,b in scanned]
                coverage=json.loads((PORT/'reports/combat-audit/map-coverage.json').read_text())
                expected=sum(r['objects'] for r in coverage['rows'] if r['level']==number)
                result['expected_regular_enemies']=expected
                result['enemy_scan_valid']=len(scanned)==expected and all(0<r['health']<=r['max_health'] and min(r['body'][2:])>0 for r in result['enemy_scan'])
            if preview:
                result['preview_marker'] = 'Pazur Omar ready:' in log
            if loaded:
                if args.omar_fight:
                    result["controlled_boss_inputs"] = True
                    fight_omar(pid)
                if args.attack_count:
                    time.sleep(0.5)
                    for _ in range(args.attack_count):
                        adb('shell', 'input', 'keyevent', '--longpress', '113')
                        time.sleep(0.15)
                    result['melee_key_presses'] = args.attack_count
                time.sleep(args.hold_seconds)
                adb('shell', 'screencap', '-p', REMOTE+'level-test.png')
                adb('pull', REMOTE+'level-test.png', str(REPORT/f'level-{number}.png'))
                memory = adb('shell', 'dumpsys', 'meminfo', 'pl.pazur.port').stdout
                (REPORT/f'memory-{number}.txt').write_text(memory, encoding='utf-8')
                # Android 10 uses TOTAL:, newer Android releases use TOTAL PSS:.
                match = re.search(r'TOTAL(?: PSS)?:\s+(\d+)', memory)
                if match: result['pss_kib'] = int(match.group(1))
                log = adb('logcat', '-d', '--pid='+pid, '-s', 'SDL/APP', 'libc', 'AndroidRuntime').stdout
                (REPORT/f'level-{number}.log').write_text(log, encoding='utf-8')
                result['frame_samples'] = [dict(fps=float(f), p95_ms=int(p), max_ms=int(m))
                    for f,p,m in re.findall(r'Pazur frame sample: fps=([\d.]+) p95=(\d+) ms max=(\d+) ms', log)]
                result['display_size'] = args.display_size or 'unchanged'
            alive = pid in adb('shell', 'pidof', 'pl.pazur.port', check=False).stdout.split()
            result['crash_free'] = alive and 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log
            result['expected_log_markers'] = {marker: marker in log for marker in args.expect_log}
            result['absent_log_markers'] = {marker: marker not in log for marker in args.reject_log}
            results.append(result)
            print(json.dumps(result), flush=True)
    finally:
        adb('shell', 'am', 'force-stop', 'pl.pazur.port')
        if args.display_size:
            adb('shell', 'wm', 'size', previous_override.group(1) if previous_override else 'reset')
        if fixture_created: adb('shell', 'rm', REMOTE+'startup_commands.txt')
        adb('push', str(REPORT/'config-before.xml'), REMOTE+'config.xml')
        adb('push', str(REPORT/'saves-before.xml'), REMOTE+'SAVES.XML')
        (REPORT/'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
        print('Original config and save restored', flush=True)
    if not all(r['loaded'] and r['music_pcm'] and r['crash_free'] and r.get('preview_marker', True)
               and r.get('enemy_scan_valid',True) and all(r['expected_log_markers'].values()) and all(r['absent_log_markers'].values()) for r in results):
        raise SystemExit('Level smoke test failed; see results.json and per-level logs')


if __name__ == '__main__':
    main()
