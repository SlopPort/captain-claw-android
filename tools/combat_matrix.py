"""Run each enemy in its own source level so LEVEL_* effects resolve correctly."""
from pathlib import Path
import json
import re
import subprocess
import sys

port=Path(__file__).resolve().parents[1]
inventory=json.loads((port/'reports/combat-audit/inventory.json').read_text(encoding='utf-8'))
failures=[]
for level in (list(map(int,sys.argv[1:])) or list(range(1,15))):
    indices=[str(i) for i,e in enumerate(inventory)
             if int(re.search(r'_Level(\d+)_',e['prototype'])[1])==level]
    result=subprocess.run([sys.executable,'-B',str(port/'tools/combat_device_smoke.py'),
        '--mode','enemies','--indices',*indices,'--report',f'combat-matrix-0.4.2-level{level}'])
    if result.returncode:
        failures.append(level)
print('Failed source levels:', failures, flush=True)
raise SystemExit(bool(failures))
