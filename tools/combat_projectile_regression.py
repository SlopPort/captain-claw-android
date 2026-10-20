"""Repeat incoming projectile types after the body-registration contact guard."""
from pathlib import Path
import json
import re
import subprocess
import sys

port=Path(__file__).resolve().parents[1]
inventory=json.loads((port/'reports/combat-audit/inventory.json').read_text())
failures=[]
for level in range(1,15):
    indices=[str(i) for i,e in enumerate(inventory)
             if int(re.search(r'_Level(\d+)_',e['prototype'])[1])==level and
             (any(a['projectile'] for a in e['attacks']) or
              any(a['kind']=='CannonFireAnim' for a in e['special_attacks']))]
    if not indices: continue
    result=subprocess.run([sys.executable,'-B',str(port/'tools/combat_device_smoke.py'),
        '--mode','enemies','--phase','incoming','--ranged-fixture','--indices',*indices,
        '--report',f'combat-ranged-final-0.4.2-level{level}'])
    if result.returncode: failures.append(level)
print('Failed projectile source levels:',failures,flush=True)
raise SystemExit(bool(failures))
