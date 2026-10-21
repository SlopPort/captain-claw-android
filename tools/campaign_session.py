"""Isolated campaign testing, app-local input, continuous evidence and save restoration.

Written by OpenAI Codex. Starting a level directly or teleporting is a fixture,
never evidence of naturally traversing the campaign. No global Android input.
"""
import copy
import json
import subprocess
import time
import xml.etree.ElementTree as ET
from gamepad_quit_smoke import adb, REMOTE, PORT


class CampaignSession:
    def __init__(self, report, level=1):
        self.report=PORT/'reports'/report
        self.level=level;self.pid='';self.ticket=0
        self.stream=None;self.output=None;self.backed_up=False

    def logs(self):
        path=self.report/'native.log'
        return path.read_text(encoding='utf-8',errors='replace') if path.exists() else ''

    def wait(self, marker, seconds=45, after=0):
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            text=self.logs()[after:]
            if 'Fatal signal' in text or 'FATAL EXCEPTION' in text:raise RuntimeError('Game crashed')
            if marker in text:return
            time.sleep(.1)
        raise RuntimeError('Missing marker: '+marker)

    def command(self, value):
        self.ticket+=1;tag='campaign-'+str(self.ticket)
        with (self.report/'commands.jsonl').open('a',encoding='utf-8') as out:
            out.write(json.dumps(dict(time=time.time(),command=value))+'\n')
        temporary=self.report/'command.tmp'
        temporary.write_text(tag+'|'+value+'\n',encoding='ascii')
        adb('push',str(temporary),REMOTE+'combat-command.tmp')
        adb('shell','mv',REMOTE+'combat-command.tmp',REMOTE+'combat-command.txt')
        deadline=time.monotonic()+12
        while time.monotonic()<deadline:
            reply=adb('shell','cat',REMOTE+'combat-response.txt',check=False).strip()
            if reply==tag+'|done':return
            if reply.startswith(tag+'|rejected:'):raise RuntimeError(reply)
            if self.pid not in adb('shell','pidof','pl.pazur.port',check=False).split():raise RuntimeError('Game exited')
            time.sleep(.1)
        raise RuntimeError('No acknowledgement: '+value)

    def capture(self, label):
        # Read-only screenshot; does not interact with another foreground app.
        adb('shell','screencap','-p',REMOTE+'campaign-test.png')
        adb('pull',REMOTE+'campaign-test.png',str(self.report/(label+'.png')))

    def __enter__(self):
        self.report.mkdir(parents=True,exist_ok=True)
        if (self.report/'config.original.xml').exists():raise RuntimeError('Use a new report name; preserve prior evidence')
        for name in ('combat-command.txt','combat-response.txt','startup_commands.txt'):
            if subprocess.run(['adb','shell','test','-e',REMOTE+name],capture_output=True).returncode==0:
                raise RuntimeError('Existing diagnostic file: '+name)
        adb('shell','am','force-stop','pl.pazur.port')
        adb('pull',REMOTE+'config.xml',str(self.report/'config.original.xml'))
        adb('pull',REMOTE+'SAVES.XML',str(self.report/'saves.original.xml'))
        self.backed_up=True
        try:
            config=ET.parse(self.report/'config.original.xml')
            for path,value in [('DebugOptions/SkipMenu','true'),('DebugOptions/SkipMenuToLevel',str(self.level)),
                               ('GlobalOptions/LoadAllLevelSaves','false')]:config.find(path).text=value
            flag=config.find('DebugOptions/PreviewIncompleteLevel14')
            if flag is None:flag=ET.SubElement(config.find('DebugOptions'),'PreviewIncompleteLevel14')
            flag.text='true' # Enables the diagnostic mailbox, not god mode.
            config.write(self.report/'config.test.xml',encoding='utf-8',xml_declaration=True)
            original=ET.parse(self.report/'saves.original.xml')
            root=ET.Element(original.getroot().tag)
            level=copy.deepcopy(original.find('Level'))
            level.find('LevelNumber').text=str(self.level)
            checkpoint=copy.deepcopy(level.find('Checkpoint'))
            for node in list(level.findall('Checkpoint')):level.remove(node)
            for key,value in [('CheckpointNumber',0),('Score',0),('Health',100),('Lives',3),
                              ('BulletCount',10),('MagicCount',5),('DynamiteCount',3)]:checkpoint.find(key).text=str(value)
            level.append(checkpoint);root.append(level)
            ET.ElementTree(root).write(self.report/'saves.test.xml',encoding='utf-8',xml_declaration=True)
            adb('push',str(self.report/'config.test.xml'),REMOTE+'config.xml')
            adb('push',str(self.report/'saves.test.xml'),REMOTE+'SAVES.XML')
            adb('shell','am','start','-n','pl.pazur.port/.LauncherActivity')
            deadline=time.monotonic()+30
            while time.monotonic()<deadline:
                pids=adb('shell','pidof','pl.pazur.port',check=False).split()
                if pids:self.pid=pids[0];break
                time.sleep(.2)
            if not self.pid:raise RuntimeError('No game process')
            self.output=(self.report/'native.log').open('wb')
            self.stream=subprocess.Popen(['adb','logcat','--pid='+self.pid,'-s','SDL/APP','libc','AndroidRuntime'],
                stdout=self.output,stderr=subprocess.DEVNULL)
            self.wait('Level loaded !');self.wait('Pazur simulation clock reset');time.sleep(.3)
            return self
        except BaseException:
            self.__exit__(None,None,None);raise

    def __exit__(self, *_):
        if self.stream:
            self.stream.terminate()
            try:self.stream.wait(timeout=5)
            except subprocess.TimeoutExpired:self.stream.kill();self.stream.wait(timeout=5)
        if self.output:self.output.close()
        if self.backed_up:
            adb('shell','am','force-stop','pl.pazur.port')
            for remote,local in [('config.xml','config.original.xml'),('SAVES.XML','saves.original.xml')]:
                adb('push',str(self.report/local),REMOTE+remote)
            for name in ('combat-command.txt','combat-response.txt','combat-command.tmp','campaign-test.png'):
                adb('shell','rm','-f',REMOTE+name)
            print('Original configuration and saves restored',flush=True)
