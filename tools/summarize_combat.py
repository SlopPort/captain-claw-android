"""Require complete, unique combat coverage before marking a release verified."""
from pathlib import Path
import hashlib
import json

port=Path(__file__).resolve().parents[1]
inventory=json.loads((port/'reports/combat-audit/inventory.json').read_text())
rows=[]
for level in range(1,15):
    path=port/f'reports/combat-matrix-0.4.2-level{level}/results.json'
    if path.exists(): rows+=json.loads(path.read_text())
seen=[r['prototype'] for r in rows]
missing=sorted({e['prototype'] for e in inventory}-set(seen))
failures=[r['prototype'] for r in rows if not r['passed']]
duplicates=sorted({name for name in seen if seen.count(name)>1})
maps_path=port/'reports/combat-all-maps-0.4.2/results.json'
maps=json.loads(maps_path.read_text()) if maps_path.exists() else []
regression_path=port/'reports/combat-final-regression-0.4.2/results.json'
regression=json.loads(regression_path.read_text()) if regression_path.exists() else []
projectiles=[]
for path in (port/'reports').glob('combat-ranged-final-0.4.2-level*/results.json'):
    projectiles+=json.loads(path.read_text())
level7_path=port/'reports/combat-level7-final-0.4.2/results.json'
level7=json.loads(level7_path.read_text()) if level7_path.exists() else []
complete=(not missing and not failures and not duplicates and
          {r['level'] for r in maps}==set(range(1,15)) and
          all(r['enemy_scan_valid'] and r['crash_free'] and r['loaded'] and r['music_pcm'] for r in maps) and
          len(regression)==13 and all(r['passed'] for r in regression) and
          len(projectiles)==16 and all(r['passed'] and len(r['incoming'])==2 and
              all(i['projectile_contacts']>0 for i in r['incoming']) for r in projectiles) and
          len(level7)==4 and all(r['passed'] for r in level7))
result={'complete':complete,'enemy_variants':len(rows),'passed':len(rows)-len(failures),
        'missing':missing,'failures':failures,'duplicates':duplicates,
        'maps':len(maps),'map_enemies':sum(len(r['enemy_scan']) for r in maps),
        'regression_cases':len(regression),
        'final_projectile_variants':len(projectiles),'final_level7_variants':len(level7),
        'apk_sha256':hashlib.file_digest((port/'app/build/outputs/apk/debug/app-debug.apk').open('rb'),'sha256').hexdigest()}
(port/'reports/combat-audit/final-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
raise SystemExit(not complete)
