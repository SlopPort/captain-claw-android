"""Check combat animation frames and map placements against extracted original assets."""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import io
import json
import re
import xml.etree.ElementTree as ET
import zipfile

PORT = Path(__file__).resolve().parents[1]
REPORT = PORT/'reports/combat-audit'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--apk',type=Path,default=PORT/'app/build/outputs/apk/debug/app-debug.apk')
args=parser.parse_args()
provenance=json.loads((REPORT/'provenance.json').read_text(encoding='utf-8'))
assert provenance['apk_sha256']==hashlib.sha256(args.apk.read_bytes()).hexdigest(),'Rerun audit_combat.py for this APK'
inventory = json.loads((REPORT/'inventory.json').read_text(encoding='utf-8'))
lines = (REPORT/'assets.txt').read_text(encoding='utf-8').splitlines()
animations = {parts[1]: int(parts[2]) for line in lines
              if (parts := line.split('|'))[0] == 'ANI'}
requested = set((REPORT/'animation-requests.txt').read_text().splitlines())
errors = [f'Missing animation: {path}' for path in sorted(requested-animations.keys())]
checks = 0
for enemy in inventory:
    root = ET.parse(REPORT/(enemy['prototype']+'.xml')).getroot()
    directory = root.findtext('AnimationComponent/AnimationPath').rsplit('/', 1)[0]
    actions = [(directory+'/'+a['animation'].upper()+'.ANI', a['frame']) for a in enemy['attacks']]
    actions += [(a['path'], a['frame']) for a in enemy['special_attacks'] if a['frame'] is not None]
    for path, frame in actions:
        checks += 1
        if not 0 <= frame < animations.get(path, 0):
            errors.append(f"{enemy['prototype']}: frame {frame} outside {path}")

prototypes = {e['prototype'] for e in inventory}
header = (PORT/'native/CombatPrototypes.h').read_text()
compiled = re.findall(r'^\s*(ActorPrototype_\w+)\s*,?\s*$', header, re.M)
if compiled != [e['prototype'] for e in inventory]:
    errors.append('Diagnostic prototype order differs from inventory')
counts = Counter()
custom_fields = []
with zipfile.ZipFile(args.apk) as apk:
    support=apk.read('assets/import-support/ASSETS.ZIP')
with zipfile.ZipFile(io.BytesIO(support)) as archive:
    mappings = {}
    for level in range(1, 15):
        root = ET.fromstring(archive.read(f'LEVEL_METADATA/LEVEL{level}.XML'))
        mappings[level] = {e.get('logic'): e.get('actorPrototype')
                           for e in root.findall('LogicsToActorPrototypes/LogicToActorPrototype')}
    for line in lines:
        row = line.split('|')
        if row[0] != 'OBJ':
            continue
        level = int(row[1])
        prototype = mappings[level].get(row[2])
        if prototype not in prototypes:
            continue
        counts[level, row[2], prototype] += 1
        if any(int(v) for v in row[6:8]) or any(int(v) for cell in row[8:] for v in cell.split(',')):
            custom_fields.append(row)
coverage = {'objects': sum(counts.values()), 'rows': [
    {'level': level, 'logic': logic, 'prototype': prototype, 'objects': count}
    for (level, logic, prototype), count in sorted(counts.items())],
    'wwd_nondefault_combat_fields': custom_fields}
(REPORT/'map-coverage.json').write_text(json.dumps(coverage, indent=2), encoding='utf-8')
result = {'prototypes': len(inventory), 'animations': len(requested),
          'attack_frame_checks': checks, 'map_placements': coverage['objects'],
          'custom_wwd_fields': len(custom_fields), 'errors': errors}
(REPORT/'asset-validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
raise SystemExit(bool(errors))
