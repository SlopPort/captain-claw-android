"""Exercise production TinyXML atomic writes and child-process death boundaries.

OpenAI Codex. Desktop filesystem evidence, not Android full-disk/power-loss
coverage. Requires g++ (or CXX); creates only a new task report directory.
"""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

port=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report',default='atomic-xml-boundaries-0.4.18')
report=(port/'reports'/parser.parse_args().report).resolve()
if not report.is_relative_to((port/'reports').resolve()):raise ValueError('Report must stay under reports')
report.mkdir(exist_ok=False)
compiler=os.environ.get('CXX') or shutil.which('g++')
if not compiler:raise RuntimeError('Set CXX to a C++11 compiler')
environment=dict(os.environ);environment['PATH']=str(Path(compiler).parent)+os.pathsep+environment.get('PATH','')
source=report/'probe.cpp'
source.write_text(r'''
#include "AtomicXml.h"
#include <cstdlib>
#include <cstring>
static int selected=-1;static bool crash=false;
static bool boundary(PazurXml::Boundary point) {
    if(int(point)!=selected)return true;
    if(crash)std::_Exit(77);
    return false;
}
int main(int argc,char** argv) {
    if(argc!=4)return 5;
    selected=std::atoi(argv[3]);crash=std::strcmp(argv[2],"crash")==0;
    TiXmlDocument document;document.Parse("<GameSaves><New>321</New></GameSaves>");
    return PazurXml::Save(document,argv[1],boundary)?0:1;
}
''',encoding='utf-8')
tiny=port/'upstream/OpenClaw/ThirdParty/Tinyxml'
executable=report/('probe.exe' if os.name=='nt' else 'probe')
with (report/'compile.txt').open('wb') as log:
    subprocess.run([compiler,'-std=c++11','-O2','-static-libgcc','-static-libstdc++',
        '-I'+str(port/'native'),'-I'+str(tiny),str(source),
        *[str(tiny/(name+'.cpp')) for name in ('tinyxml','tinyxmlparser','tinyxmlerror','tinystr')],
        '-o',str(executable)],env=environment,stdout=log,stderr=subprocess.STDOUT,check=True)
rows=[];old=b'<GameSaves><Old>100</Old></GameSaves>'
def run(target,mode,point):
    return subprocess.run([str(executable),str(target),mode,str(point)],env=environment,check=False).returncode
for present in (False,True):
    for mode in ('fail','crash'):
        for point in range(4):
            folder=report/(str(int(present))+'-'+mode+'-'+str(point));folder.mkdir();target=folder/'SAVES.XML'
            if present:target.write_bytes(old)
            code=run(target,mode,point)
            assert code==(77 if mode=='crash' else 1),(mode,point,code)
            assert (target.read_bytes()==old) if present else not target.exists()
            assert run(target,'ok',-1)==0,'Retry failed'
            assert ET.parse(target).findtext('New')=='321'
            rows.append(dict(existing=present,mode=mode,boundary=point,old_preserved=True,retry_passed=True))
for failure in ('open','publish'):
    folder=report/failure;folder.mkdir();target=folder/'SAVES.XML'
    if failure=='open':
        target.write_bytes(old);Path(str(target)+'.tmp').mkdir()
    else:target.mkdir();(target/'sentinel').write_bytes(old)
    assert run(target,'ok',-1)==1
    assert (target.read_bytes() if failure=='open' else (target/'sentinel').read_bytes())==old
    rows.append(dict(io_failure=failure,old_preserved=True))
result=dict(passed=True,cases=len(rows),rows=rows,actual_child_process_death=True,
            platform=os.name,android_power_loss_or_full_disk_test=False)
(report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=True,cases=len(rows),actual_child_process_death=True)),flush=True)
