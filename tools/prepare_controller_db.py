"""Package only Android mappings from the pinned SDL_GameControllerDB source."""
from pathlib import Path
import json
import shutil

port=Path(__file__).resolve().parents[1]
source=port/'upstream/SDL_GameControllerDB'
entry=next(e for e in json.loads((port/'sources.lock.json').read_text()) if e['name']=='SDL_GameControllerDB')
lines=[line for line in (source/'gamecontrollerdb.txt').read_text(encoding='utf-8').splitlines()
       if line and not line.startswith('#') and ',platform:Android,' in line]
if not lines: raise RuntimeError('No Android controller mappings in locked database')
target=port/'app/src/main/assets/controllers'
target.mkdir(parents=True,exist_ok=True)
header='# Android subset of https://github.com/mdqinc/SDL_GameControllerDB\n# Revision: '+entry['commit']+'\n'
(target/'gamecontrollerdb.txt').write_text(header+'\n'.join(lines)+'\n',encoding='utf-8')
licenses=port/'app/src/main/assets/licenses';licenses.mkdir(parents=True,exist_ok=True)
shutil.copyfile(source/'LICENSE',licenses/'SDL_GameControllerDB-Zlib.txt')
(port/'reports').mkdir(parents=True,exist_ok=True)
(port/'reports/controller-database.json').write_text(json.dumps({'commit':entry['commit'],'android_mappings':len(lines)},indent=2),encoding='utf-8')
print('Android controller mappings:',len(lines))
