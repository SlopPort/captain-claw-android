"""Verify measured jump behavior, touch ownership and targeted release regressions."""
from pathlib import Path
import hashlib
import json

port=Path(__file__).resolve().parents[1]
apk=port/'app/build/outputs/apk/debug/app-debug.apk'
digest=hashlib.file_digest(apk.open('rb'),'sha256').hexdigest()
baseline=json.loads((port/'reports/jump-baseline-0.4.2/results.json').read_text())
reports=[]
for name in ('jump-touch-0.4.3','jump-touch-0.4.3-16-9','jump-touch-0.4.3-4-3'):
    folder=port/'reports'/name
    result=json.loads((folder/'results.json').read_text())
    assert result['passed'] and result['apk_sha256']==digest,result
    assert len(result['cases'])==6
    assert all(0<=r['takeoff_ms']<=65 and r['jumps']==1 for r in result['cases'])
    by_name={r['label']:r for r in result['cases']}
    assert all(by_name[n]['rise']>=50 for n in ('hold10','hold100','drift100'))
    assert abs(by_name['hold700']['rise']-baseline['cases'][3]['rise'])<5
    log=(folder/'native.log').read_text(encoding='utf-8')
    drift=log.split('Pazur console command: combatjumpmeasure drift100',1)[1].split('Pazur jump trace: label=drift100',1)[0]
    assert 'attack=1' not in drift and 'fire=1' not in drift
    reports.append(result)
assert max(r['takeoff_ms'] for r in reports[0]['cases']) < min(r['takeoff_ms'] for r in baseline['cases'])
regression=json.loads((port/'reports/jump-combat-regression-0.4.3/results.json').read_text())
assert len(regression)==13 and all(r['passed'] for r in regression)
levels=json.loads((port/'reports/jump-normal-levels-0.4.3/results.json').read_text())
assert {r['level'] for r in levels}=={1,13}
assert all(r['loaded'] and r['music_pcm'] and r['crash_free'] for r in levels)
result={'passed':True,'apk_sha256':digest,'touch_aspects':3,'measured_jumps':18,
        'physical_takeoff_ms_before':[r['takeoff_ms'] for r in baseline['cases']],
        'physical_takeoff_ms_after':[r['takeoff_ms'] for r in reports[0]['cases']],
        'short_tap_rise_before':baseline['cases'][0]['rise'],
        'short_tap_rise_after':reports[0]['cases'][0]['rise'],
        'full_jump_rise':reports[0]['cases'][3]['rise'],
        'hitbox_regressions':len(regression),'normal_levels':[r['level'] for r in levels]}
(port/'reports/jump-release-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
