"""Private, resumable REA stdio mailbox for the full native-code audit.

OpenAI Codex (LLM). Uses installed REA/Ghidra; does not install software,
change client registration, execute the target, or operate Android devices.
Requests/results may contain proprietary disassembly and must stay in reports.
One request is outstanding at a time. A transport timeout ends this worker;
it never silently re-imports a target or replays an uncertain operation.
"""
import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time

PORT = Path(__file__).resolve().parents[1]
ALLOWED = frozenset(('open_binary', 'close_binary', 'binary_session',
    'binary_overview', 'list_procedures', 'list_segments', 'list_strings',
    'analyze_function', 'batch_decompile', 'procedure_info', 'procedure_callers',
    'procedure_callees', 'procedure_references', 'procedure_pseudo_code',
    'procedure_assembly', 'read_function_instructions', 'inspect_analysis_view',
    'inspect_native_instruction', 'inspect_address_context', 'read_bytes',
    'xrefs', 'resolve_native_call_targets', 'resolve_containing_procedure',
    'search_strings', 'search_procedures', 'inspect_pe_resources'))


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2), encoding='utf-8')
    # Windows readers/scanners can briefly prevent replacement. Retry only the
    # completed local write, never the REA request or target analysis itself.
    for attempt in range(40):
        try:
            temporary.replace(path)
            return
        except PermissionError:
            if attempt == 39: raise
            time.sleep(.05)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True)
    parser.add_argument('--seconds', type=int, default=14400)
    args = parser.parse_args()
    root = (PORT / 'reports' / args.report).resolve()
    if not root.is_relative_to((PORT / 'reports').resolve()):
        parser.error('Private mailbox must stay under reports')
    root.mkdir(parents=True, exist_ok=True)
    # Exclusive lifetime lock; a stale file needs an actual process audit.
    lock = (root / 'worker.lock').open('x')
    lock.write(str(os.getpid())); lock.close()
    node = PORT / 'upstream/rea-node-local/node-v22.23.4-win-x64/node.exe'
    cli = PORT / 'tooling/node_modules/rea-agents/scripts/rea.mjs'
    env = os.environ.copy()
    env.update(GHIDRA_INSTALL_DIR=str(PORT / 'upstream/ghidra-local/ghidra_12.1.4_PUBLIC'),
               JAVA_HOME='C:/Program Files/Android/Android Studio/jbr',
               REA_ANALYSIS_PROVIDER='ghidra', REA_GHIDRA_STARTUP_TIMEOUT_MS='300000')
    process = None
    messages = queue.Queue()
    counter = 0
    failure = None
    with (root / 'mcp.stderr.log').open('a', encoding='utf-8') as errors:
        try:
            process = subprocess.Popen([str(node), str(cli), '--mcp'], cwd=PORT,
                env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=errors, text=True, encoding='utf-8', bufsize=1)

            def read():
                for line in process.stdout:
                    try: messages.put(json.loads(line))
                    except ValueError: pass
                messages.put(None)
            threading.Thread(target=read, daemon=True).start()

            def rpc(method, params, timeout=600):
                nonlocal counter
                counter += 1
                process.stdin.write(json.dumps(dict(jsonrpc='2.0', id=counter,
                    method=method, params=params)) + '\n'); process.stdin.flush()
                end = time.monotonic() + timeout
                while time.monotonic() < end:
                    try: value = messages.get(timeout=min(1, max(.01, end-time.monotonic())))
                    except queue.Empty: continue
                    if value is None: raise RuntimeError('REA transport closed')
                    if value.get('id') == counter: return value
                raise TimeoutError(method)

            save(root / 'initialize.json', rpc('initialize', dict(protocolVersion='2024-11-05',
                capabilities={}, clientInfo=dict(name='CaptainClaw-full-audit', version='1'))))
            process.stdin.write(json.dumps(dict(jsonrpc='2.0', method='notifications/initialized'))+'\n')
            process.stdin.flush()
            catalog = rpc('tools/list', {})
            save(root / 'tools.json', catalog)
            names = {t['name'] for t in catalog.get('result', {}).get('tools', [])}
            # A resumed mailbox has saved open_binary output, but a new MCP
            # process has no active target. Reopen explicitly before any work.
            opening = rpc('tools/call', dict(name='open_binary', arguments=dict(
                path=str(PORT.parent/'CLAW.EXE'), provider_id='ghidra')))
            save(root/('session-'+str(os.getpid())+'-open.json'), opening)
            if opening.get('error') or opening.get('result', {}).get('isError'):
                raise RuntimeError('Target open failed; see private session evidence')
            save(root / 'ready.json', dict(pid=os.getpid(), tools=sorted(names & ALLOWED)))
            end = time.monotonic() + args.seconds
            while time.monotonic() < end and not (root / 'stop').exists():
                pending = [p for p in sorted(root.glob('*.request.json'))
                           if not p.with_name(p.name.replace('.request.', '.response.')).exists()]
                if not pending: time.sleep(.2); continue
                # Re-read priority requests between small batches, so a newly
                # identified dependency need not wait behind the entire binary.
                for path in pending[:16]:
                    if time.monotonic() >= end or (root / 'stop').exists(): break
                    request = json.loads(path.read_text(encoding='utf-8'))
                    if request['name'] not in names & ALLOWED:
                        raise ValueError('Operation not admitted by audit worker')
                    # Exact target only; other provider operations are read-only.
                    if request['name'] == 'open_binary' and Path(request['arguments']['path']).resolve() != (PORT.parent/'CLAW.EXE').resolve():
                        raise ValueError('Wrong analysis target')
                    save(root / 'active.json', dict(request=path.name, started=time.time()))
                    response = rpc('tools/call', request)
                    save(path.with_name(path.name.replace('.request.', '.response.')), response)
                    recovered = False
                    if response.get('result', {}).get('isError'):
                        texts = response['result'].get('content', [])
                        error = json.loads(next(x['text'] for x in texts if x['type'] == 'text')).get('error', {})
                        limits = error.get('details', {}).get('reported_limits', {})
                        retained = limits.get('evidence_id')
                        if error.get('code') == 'resource_constraint' and limits.get('boundary') == 'mcp-response' and retained:
                            # The analysis completed; export retained Evidence
                            # before closing this ephemeral session. No truncation
                            # or repeated decompilation is used for recovery.
                            bundle_path = root/(path.stem+'.evidence-bundle.json')
                            exported = rpc('tools/call', dict(name='export_evidence_bundle',
                                arguments=dict(path=str(bundle_path), overwrite=False)))
                            save(root/(path.stem+'.export.json'), exported)
                            if exported.get('error') or exported.get('result', {}).get('isError'):
                                raise RuntimeError('Retained Evidence export failed')
                            bundle = json.loads(bundle_path.read_text(encoding='utf-8'))
                            record = next(r for r in bundle['records'] if r['evidence_id'] == retained)
                            if record['operation'] != request['name']:
                                raise RuntimeError('Retained operation mismatch')
                            save(root/(path.stem+'.retained-evidence.json'), record)
                            recovered = True
                    if response.get('error') or (response.get('result', {}).get('isError') and not recovered):
                        raise RuntimeError('REA request failed; saved response requires review before resuming')
                    save(root / 'active.json', dict(completed=path.name, finished=time.time()))
        except Exception as error:
            failure = repr(error)
        finally:
            if process:
                if failure is None:
                    try: rpc('tools/call', dict(name='close_binary', arguments={}), timeout=45)
                    except Exception as error: failure = repr(error)
                process.stdin.close()
                try: process.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    process.terminate(); process.wait(timeout=15)
            save(root/'worker.closed.json', dict(closed=True, failure=failure,
                returncode=process.returncode if process else None))
            (root/'worker.lock').unlink()
    if failure: raise RuntimeError(failure)


if __name__ == '__main__':
    main()
