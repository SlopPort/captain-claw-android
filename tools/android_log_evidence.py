"""Attribute crashes in multi-process instrumentation logs, by OpenAI Codex.

Instrumentation restarts the game, so a single logcat --pid misses evidence.
Only PIDs carrying the port's own Pazur marker are attributed to the game.
Unparseable fatal lines fail closed; unrelated app failures stay in the report.
"""
import re


def line_pid(line):
    match=re.match(r'\d\d-\d\d\s+[\d:.]+\s+(\d+)\s+\d+\s+[VDIWEF]\s',line)
    if match:return int(match[1])
    match=re.match(r'[VDIWEF]/[^\(]+\(\s*(\d+)\)',line)
    return int(match[1]) if match else None


def crash_evidence(log):
    lines=log.splitlines()
    pids=sorted({pid for line in lines if 'SDL/APP' in line and 'Pazur ' in line if (pid:=line_pid(line)) is not None})
    target=[];foreign=[];unknown=[]
    for index,line in enumerate(lines):
        if 'FATAL EXCEPTION' not in line and 'Fatal signal' not in line:continue
        pid=line_pid(line);row=dict(pid=pid,line=line)
        nearby='\n'.join(lines[index:index+5])
        process=re.search(r'Process:\s*([^,\n]+),\s*PID:\s*(\d+)',nearby)
        if process and int(process[2])==pid:row['process']=process[1]
        if pid in pids or row.get('process')=='pl.pazur.port':target.append(row)
        elif pid is not None and row.get('process'):foreign.append(row)
        else:unknown.append(row) # An early native crash may precede our first marker.
    return dict(target_pids=pids,target_crashes=target,foreign_crashes=foreign,unattributed_crashes=unknown)
