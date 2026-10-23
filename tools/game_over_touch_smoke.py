"""Enter the real last-life death path and tap Game Over inside the app only."""
import argparse
import json
import subprocess
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT
from android_package import installed_apk_sha256


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',default='game-over-touch')
    parser.add_argument('--cycles',type=int,default=1)
    parser.add_argument('--powerup',action='store_true')
    parser.add_argument('--rapid-taps',type=int,choices=range(1,9),default=1)
    parser.add_argument('--expect-blocked',action='store_true',help='Baseline reproduction, not a passing exit test')
    args=parser.parse_args()
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=False)
    for name in ('combat-command.txt','combat-response.txt'):
        if subprocess.run(['adb','shell','test','-e',REMOTE+name],capture_output=True).returncode==0:
            raise RuntimeError('Existing diagnostic mailbox: '+name)
    adb('shell','am','force-stop','pl.pazur.port')
    for name in ('config.xml','SAVES.XML'):adb('pull',REMOTE+name,str(report/name))
    config=ET.parse(report/'config.xml')
    config.find('DebugOptions/SkipMenu').text='true'
    config.find('DebugOptions/SkipMenuToLevel').text='1'
    flag=config.find('DebugOptions/PreviewIncompleteLevel14')
    if flag is None:flag=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
    flag.text='true';config.write(report/'test.xml',encoding='utf-8',xml_declaration=True)
    apk_sha256=installed_apk_sha256()
    rows=[]
    try:
        for cycle in range(args.cycles):
            adb('shell','am','force-stop','pl.pazur.port')
            adb('push',str(report/'test.xml'),REMOTE+'config.xml')
            adb('push',str(report/'SAVES.XML'),REMOTE+'SAVES.XML')
            for name in ('combat-command.txt','combat-response.txt'):adb('shell','rm','-f',REMOTE+name)
            adb('logcat','-c')
            output=adb('shell','am','instrument','-w','-r','-e','scenario','game-over','-e','death_powerup',str(args.powerup).lower(),'-e','death_taps',str(args.rapid_taps),
                'pl.pazur.port.test/pl.pazur.port.JumpTouchTest')
            (report/('instrumentation-'+str(cycle)+'.log')).write_text(output,encoding='utf-8')
            log=adb('logcat','-d','-s','SDL/APP','libc','AndroidRuntime')
            (report/('native-'+str(cycle)+'.log')).write_text(log,encoding='utf-8')
            for name in ('game-over-before.png','game-over-after.png'):
                adb('pull',REMOTE+name,str(report/(str(cycle)+'-'+name)))
            opened='Pazur game over menu opened' in log
            exited=opened and 'Changing to: 3' in log.split('Pazur game over menu opened',1)[1]
            passed='INSTRUMENTATION_CODE: 0' in output and opened and exited!=args.expect_blocked
            passed=passed and 'Fatal signal' not in log and 'FATAL EXCEPTION' not in log
            row={'cycle':cycle,'game_over_opened':opened,'returned_to_menu':exited,
                'baseline_block_expected':args.expect_blocked,'expectation_met':passed,'powerup_active_before_death':args.powerup,'requested_taps':args.rapid_taps}
            rows.append(row);print(json.dumps(row),flush=True)
            assert passed,'See screenshots and native log'
    finally:
        adb('shell','am','force-stop','pl.pazur.port')
        for name in ('config.xml','SAVES.XML'):adb('push',str(report/name),REMOTE+name)
        for name in ('combat-command.txt','combat-response.txt','combat-command.tmp','game-over-before.png','game-over-after.png'):
            adb('shell','rm','-f',REMOTE+name)
        (report/'results.json').write_text(json.dumps({'cycles':rows,
            'apk_sha256':apk_sha256},indent=2),encoding='utf-8')
        print('Original config and saves restored',flush=True)


if __name__=='__main__':main()
