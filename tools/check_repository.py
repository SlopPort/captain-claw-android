"""Check the staged/tracked source distribution, excluding generated and private data."""
from pathlib import Path
import json
import subprocess

port=Path(__file__).resolve().parents[1]
git=['git','-c','safe.directory='+port.as_posix(),'-C',str(port)]
names=subprocess.check_output(git+['ls-files','-z']).decode('utf-8').split('\0')
names=[n for n in names if n]
forbidden=('private-signing/','upstream/','build/','dist/','reports/','.gradle/','.npm-cache/',
           'app/build/','app/.cxx/','tooling/node_modules/',
           'app/src/main/assets/music/','app/src/main/assets/controllers/','app/src/main/assets/import-support/')
errors=[]
total=0
for name in names:
    path=port/name
    if name.startswith(forbidden) or path.suffix.lower() in ('.apk','.aab','.rez','.pat','.keystore','.jks'):
        errors.append('Excluded artifact tracked: '+name)
    if not path.is_file():
        errors.append('Missing file: '+name)
        continue
    total+=path.stat().st_size
    if path.stat().st_size>10*1024*1024: errors.append('Large file: '+name)
    if path.suffix=='.py':
        try: compile(path.read_text(encoding='utf-8'),name,'exec')
        except (SyntaxError,UnicodeError) as error: errors.append(str(error))
print(json.dumps({'source_files':len(names),'bytes':total,'errors':errors},indent=2))
raise SystemExit(bool(errors))
