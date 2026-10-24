"""Host-only publication/failure tests for the real game-data ZIP writer.

OpenAI Codex (LLM). Synthetic inputs only. ENOSPC is injected; no disk is filled.
Only the owned child process is killed, inside a verified private report folder.
This is not a clean-computer GUI test or Android import/playthrough evidence.
"""
import errno,json,os,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
from unittest.mock import patch
from pack_assets import PACKAGE_FILES,write_game_archive,validate_game_root,validate_rez,build_rez

port=Path(__file__).resolve().parents[1]
reports=port/'reports';reports.mkdir(exist_ok=True)
rows=[]
with tempfile.TemporaryDirectory(prefix='pack-check-',dir=reports) as temporary:
    root=Path(temporary).resolve()
    assert root.is_relative_to(reports.resolve())
    source=root/'input';source.mkdir()
    for name in PACKAGE_FILES:(source/name).write_bytes(('synthetic '+name).encode())
    output=root/'game-data.zip'
    write_game_archive(source,output)
    old=output.read_bytes();originals={p.name:p.read_bytes() for p in source.iterdir()}
    with zipfile.ZipFile(output) as packed:
        assert set(packed.namelist())==set(PACKAGE_FILES) and packed.testzip() is None
        for name in PACKAGE_FILES:assert packed.read(name)==originals[name]
    rows.append('successful five-file publication and CRC')
    real_write=zipfile.ZipFile.write;calls=[0]
    def full_disk(self,*args,**kwargs):
        calls[0]+=1
        if calls[0]==2:raise OSError(errno.ENOSPC,'Injected full disk')
        return real_write(self,*args,**kwargs)
    with patch.object(zipfile.ZipFile,'write',full_disk):
        try:write_game_archive(source,output)
        except OSError as error:assert error.errno==errno.ENOSPC
        else:raise AssertionError('Missing ENOSPC failure')
    assert output.read_bytes()==old and not list(root.glob('game-data-*.tmp'))
    rows.append('mid-write ENOSPC preserves previous ZIP')
    with patch.object(zipfile.ZipFile,'testzip',return_value='CLAW.REZ'):
        try:write_game_archive(source,output)
        except ValueError:pass
        else:raise AssertionError('CRC failure accepted')
    assert output.read_bytes()==old and not list(root.glob('game-data-*.tmp'))
    rows.append('CRC failure preserves previous ZIP')
    with patch('pack_assets.os.replace',side_effect=PermissionError('Injected locked destination')):
        try:write_game_archive(source,output)
        except PermissionError:pass
        else:raise AssertionError('Locked destination accepted')
    assert output.read_bytes()==old and not list(root.glob('game-data-*.tmp'))
    rows.append('locked output preserves previous ZIP')
    # Stop a real process after its first ZIP entry, before completion/replace.
    child_script=root/'child.py';marker=root/'writing'
    child_script.write_text("import sys,time,zipfile\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nfrom pack_assets import write_game_archive\nreal=zipfile.ZipFile.write\ndef slow(self,*a,**k):\n real(self,*a,**k)\n Path(sys.argv[4]).write_text('writing')\n time.sleep(60)\nzipfile.ZipFile.write=slow\nwrite_game_archive(Path(sys.argv[2]),Path(sys.argv[3]))\n",encoding='utf-8')
    child=subprocess.Popen([sys.executable,str(child_script),str(port/'tools'),str(source),str(output),str(marker)])
    try:
        until=time.monotonic()+10
        while not marker.exists() and time.monotonic()<until:
            assert child.poll() is None,'Child exited before writing';time.sleep(.05)
        assert marker.exists(),'Child did not reach write boundary'
        child.kill();child.wait(timeout=10)
    finally:
        if child.poll() is None:child.kill();child.wait(timeout=10)
    assert output.read_bytes()==old
    # A hard kill may leave an ignored temporary ZIP. Delete only owned files.
    for partial in root.glob('game-data-*.tmp'):
        assert partial.resolve().parent==root;partial.unlink()
    rows.append('real process termination preserves previous ZIP')
    for name,data in originals.items():assert (source/name).read_bytes()==data
    rows.append('all synthetic input bytes unchanged')
    game=root/'game';game.mkdir()
    for data in [None,bytes(30),bytes(168)]:
        if data is not None:(game/'CLAW.REZ').write_bytes(data)
        try:validate_game_root(game)
        except ValueError:pass
        else:raise AssertionError('Incomplete installation accepted')
    assets=game/'Assets';assets.mkdir();(assets/'OWN.TXT').write_text('synthetic',encoding='ascii')
    validate_game_root(game)
    rebuilt=root/'rebuilt.rez';build_rez(assets,rebuilt,game/'CLAW.REZ');validate_rez(rebuilt)
    try:validate_rez(game/'CLAW.REZ')
    except ValueError:pass
    else:raise AssertionError('Placeholder accepted as complete REZ')
    rows.append('missing/truncated/placeholder rejection and synthetic loose-data repack')
    complete=root/'complete';complete.mkdir();(complete/'CLAW.REZ').write_bytes(rebuilt.read_bytes())
    validate_game_root(complete)
    (complete/'Assets').mkdir();(complete/'Assets'/'PATCH.TXT').write_text('partial override')
    try:validate_game_root(complete)
    except ValueError:pass
    else:raise AssertionError('Full REZ plus partial overrides silently repacked')
    rows.append('complete REZ accepted; ambiguous partial loose overrides rejected')

result=dict(passed=True,checks=rows,real_disk_exhaustion=False,clean_machine=False,phone_access=False)
(reports/'pack-assets-checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
