"""Derive enemy cadence metadata from the exact APK XML and user-owned ANI files.

OpenAI Codex (LLM). No original resources are copied. Nominal animation cycles are not measured AI
attack intervals: decisions, interrupts, collision and game updates matter.
"""
import argparse
import copy
import hashlib
import io
import json
import struct
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from audit_combat import PORT, merge


def read_ani(path):
    data=path.read_bytes(); header=struct.unpack_from('<8I',data)
    position=32+header[4]; durations=[]; original_events=[]
    for _ in range(header[3]):
        frame=struct.unpack_from('<9H2B',data,position)
        if frame[6]==1: original_events.append(len(durations))
        durations.append(frame[5]); position+=20
        if frame[0]==2: position=data.index(0,position)+1
    if position!=len(data): raise ValueError('Unexpected ANI trailing bytes: '+path.name)
    return dict(frames=len(durations),durations_ms=durations,duration_ms=sum(durations),original_event1_frames=original_events,sha256=hashlib.sha256(data).hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apk',type=Path,default=PORT/'app/build/outputs/apk/debug/app-debug.apk')
    parser.add_argument('--assets',type=Path,default=PORT.parent/'Assets')
    parser.add_argument('--report',type=Path,default=PORT/'reports/enemy-cadence-2026-10-30')
    parser.add_argument('--markdown',type=Path)
    args=parser.parse_args()
    with zipfile.ZipFile(args.apk) as apk: support=apk.read('assets/import-support/ASSETS.ZIP')
    raw={}
    with zipfile.ZipFile(io.BytesIO(support)) as archive:
        for name in archive.namelist():
            if name.upper().startswith('ACTOR_PROTOTYPES/') and name.upper().endswith('.XML'):
                element=ET.fromstring(archive.read(name))
                if element.get('ActorPrototypeName'): raw[element.get('ActorPrototypeName')]=(name,element)
    cache={}
    def resolve(name,chain=()):
        if name in chain: raise ValueError('Prototype inheritance cycle')
        if name not in cache:
            root=copy.deepcopy(raw[name][1])
            if root.get('Parent'): root=merge(copy.deepcopy(resolve(root.get('Parent'),chain+(name,))),root)
            cache[name]=root
        return cache[name]
    rows=[]; special=[]; special_animations=[]; issues=[]; hazards=[]
    for prototype,(source,_) in sorted(raw.items()):
        root=resolve(prototype)
        if 'BASE' in source.upper() or not (root.find('EnemyAIComponent') is not None or root.find('OmarEncounterComponent') is not None or root.find('AquatisTentacleComponent') is not None): continue
        actions=[]; directory=root.findtext('AnimationComponent/AnimationPath','').rsplit('/',1)[0]
        for component in root:
            delay=int(component.findtext('AttackDelay','0'))
            maximum=max(delay,int(component.findtext('MaxAttackDelay',str(delay))))
            group=[]
            for action in component.findall('Attacks/AttackAction'):
                name=action.findtext('Animation',''); path=args.assets/(directory+'/'+name+'.ANI').lstrip('/').upper()
                ani=read_ani(path) if path.is_file() else None
                index=int(action.findtext('AttackAnimFrameIdx','0'))
                for field in ('AttackDelay','MaxAttackDelay'):
                    if action.find(field) is not None:
                        issues.append(dict(prototype=prototype,state=component.tag,kind='ignored_action_delay',field=field,value=action.findtext(field),effective_component_value=component.findtext(field,'0')))
                entry=dict(state=component.tag,animation=name,frame=index,damage=int(action.findtext('Damage','0')),ani=ani,delay_ms=[delay,maximum])
                entry['event_offset_in_animation_ms']=sum(ani['durations_ms'][:index]) if ani else None
                entry['matches_original_event1_marker']=bool(ani and index in ani['original_event1_frames'])
                entry['frame_valid']=bool(ani and 0<=index<ani['frames'])
                actions.append(entry); group.append(entry)
            if group and all(a['ani'] for a in group):
                total=sum(a['ani']['duration_ms'] for a in group)
                for entry in group: entry['sequence_cycle_ms']=[total+delay,total+maximum]
            if not group and ('Attack' in component.tag or any(x in component.tag for x in ('PunkRat','Gabriel','Marrow','Aquatis','Omar'))):
                special.append(dict(prototype=prototype,state=component.tag,fields={c.tag:c.text.strip() for c in component if c.text and c.text.strip() and not list(c)}))
        for component in root:
            for field in component:
                if not field.text or list(field): continue
                if field.tag.endswith('Anim') or field.tag in ('DiveInAnimation','DiveOutAnimation'):
                    base=directory
                    if field.tag.startswith('Cannon') and component.findtext('CannonActorPrototype'):
                        base=resolve(component.findtext('CannonActorPrototype')).findtext('AnimationComponent/AnimationPath','').rsplit('/',1)[0]
                    path=args.assets/(base+'/'+field.text.strip()+'.ANI').lstrip('/').upper()
                    if path.is_file(): special_animations.append(dict(prototype=prototype,field=field.tag,animation=field.text.strip(),ani=read_ani(path)))
        rows.append(dict(prototype=prototype,source=source,actions=actions))
    # Spawners and environmental threats are not ordinary EnemyAI prototypes.
    # Keep their coverage separate rather than inflating the enemy count.
    for prototype,(source,_) in sorted(raw.items()):
        if 'BASE' in source.upper(): continue
        root=resolve(prototype)
        for tag in ('ProjectileSpawnerComponent','LavaGeyserComponent','LavaMouthComponent'):
            component=root.find(tag)
            if component is None: continue
            fields={c.tag:c.text.strip() for c in component if c.text and c.text.strip() and not list(c)}
            directory=root.findtext('AnimationComponent/AnimationPath','').rsplit('/',1)[0]
            animation=component.findtext('FireAnim') or root.findtext('AnimationComponent/AnimationName')
            path=args.assets/(directory+'/'+animation+'.ANI').lstrip('/').upper() if animation else None
            ani=read_ani(path) if path and path.is_file() else None
            hazards.append(dict(prototype=prototype,state=tag,fields=fields,animation=animation,ani=ani))
    result=dict(apk_sha256=hashlib.sha256(args.apk.read_bytes()).hexdigest(),support_sha256=hashlib.sha256(support).hexdigest(),prototype_count=len(rows),attack_count=sum(len(r['actions']) for r in rows),missing_animation_count=sum(a['ani'] is None for r in rows for a in r['actions']),enemies=rows,special_states=special,special_animations=special_animations,issues=issues,hazards=hazards,original_marker_mismatches=sum(bool(a['ani'] and a['ani']['original_event1_frames'] and not a['matches_original_event1_marker']) for e in rows for a in e['actions']),actions_without_event1=sum(bool(a['ani'] and not a['ani']['original_event1_frames']) for e in rows for a in e['actions']))
    args.report.mkdir(parents=True,exist_ok=True)
    (args.report/'inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    if args.markdown:
        lines=['# Packaged enemy attack timing inventory - 2026-10-30','','Generated with `python tools/audit_enemy_cadence.py --markdown docs/validation/ENEMY-ATTACK-INVENTORY-2026-10-30.md`.','',f"APK SHA-256: `{result['apk_sha256']}`.",'',f"Coverage: **{len(rows)} concrete enemy/encounter prototypes**, **{result['attack_count']} configured attack actions**, **{result['missing_animation_count']} missing ANI files**. Bosses are included; special state machines are listed below. **{result['original_marker_mismatches']} actions select a different frame from the original ANI event-1 marker; {result['actions_without_event1']} have no event-1 marker and need their custom original handler traced.**",'','All numbers are milliseconds. Frame indices start at zero. The original event-1 column is decoded ANI metadata: REA traced raw word 6 into the original interpreter result, used by shared strike and Soldier firing. A matching marker alone does not certify a custom handler or full timing parity. ANI totals are metadata from user-owned original assets; delays and damage-frame selection come from inherited packaged port XML. No original resources are included.','','**Cycle is the nominal uninterrupted full attack sequence**, with delay once per sequence. Multiple actions share the total; do not add their repeated cycle cells. Event offsets are within each animation. Delay precedes the first animation only. Contact damage, hurt/parry interruptions, movement and visibility alter observed intervals.','','The engine advances at most one animation frame per game update and carries residual time. Setting the same animation does not reset it. Frame-zero callbacks and state transitions require runtime checking: these nominal offsets are not a promise of exact first-hit timing or measured DPS. Difficulty affects damage/healing, not cadence.','','| Prototype | State / animation | Frames / ANI duration | Damage frame / animation offset | Added delay | Nominal sequence cycle | Original ANI event-1 frames |','|---|---|---:|---:|---:|---:|---|']
        for row in rows:
            if not row['actions']: lines.append(f"| {row['prototype']} | Special / contact AI; see below | - | - | - | - | - |")
            for a in row['actions']:
                ani=a['ani']; timing=f"{ani['frames']} / {ani['duration_ms']}" if ani else 'missing ANI'
                delay='-'.join(map(str,a['delay_ms'])) if a['delay_ms'][0]!=a['delay_ms'][1] else str(a['delay_ms'][0])
                bounds=a.get('sequence_cycle_ms',[]); cycle=(str(bounds[0]) if bounds and bounds[0]==bounds[1] else '-'.join(map(str,bounds))) or '?'
                lines.append(f"| {row['prototype']} | {a['state'].replace('AIStateComponent','')} / {a['animation']} | {timing} | {a['frame']} / {a['event_offset_in_animation_ms']} | {delay} | {cycle} | {(', '.join(map(str,ani['original_event1_frames'])) or 'none / custom') if ani else '?'} |")
        lines+=['','## States outside the generic sequence formula','','These scalar XML fields are inventory clues, not complete cadence calculations. Native encounter timers need separate source review.','']
        for entry in special:
            fields='; '.join(f'{k}={v}' for k,v in entry['fields'].items())
            lines.append(f"- **{entry['prototype']} / {entry['state']}**: {fields or 'no scalar XML timing fields'}.")
        lines+=['','### Special animation metadata','','| Prototype | Field / animation | Frames | ANI duration |','|---|---|---:|---:|']
        for item in special_animations:
            lines.append(f"| {item['prototype']} | {item['field']} / {item['animation']} | {item['ani']['frames']} | {item['ani']['duration_ms']} |")
        lines+=['','## Ignored timing fields','','These are parser/configuration defects; no balance change is made by this audit.','']
        for item in issues:
            lines.append(f"- **{item['prototype']} / {item['state']}**: action-level `{item['field']}={item['value']}` is ignored; component-level effective value is `{item['effective_component_value']}`.")
        lines+=['','## Separate spawner and environmental-threat coverage','','These are not additional ordinary enemy variants. Min/max spawn delay is added before the fire animation; it is not the whole shot interval. Map conversion can override fields.','']
        for item in hazards:
            fields='; '.join(f'{k}={v}' for k,v in item['fields'].items())
            duration=f"; fire ANI={item['ani']['duration_ms']} ms" if item['ani'] else '; ANI duration unresolved/generated'
            lines.append(f"- **{item['prototype']} / {item['state']}**: {fields}{duration}.")
        lines+=['','Native/map-generated Aquatis tentacles are additional actors, not packaged EnemyAI prototypes. Their timers and the Laser contact actor need source/terrain analysis; they are not assigned a fabricated generic attack cycle.','','## Reproducibility and limitations','','The script uses `audit_combat.merge`, matching engine first-element-by-path inheritance. ANI frames use `<9H2B` after `<8I` and the image path; duration is the sixth 16-bit field. NUL-terminated event names are skipped. Trailing bytes fail validation. Private JSON records per-frame durations and hashes; the public table contains derived metadata.','','Frame-zero findings: Bear Sailor crouched melee and Cut Throat ranged actions target frame zero. `AnimationComponent::SetAnimation` calls `OnAnimationFrameStarted` but does not notify frame-changed observers on reset; the generic attack observer listens to frame-changed. A fresh state therefore waits until the first wrap to frame zero, rather than delivering the event at nominal offset zero. This warrants a dedicated runtime test before changing timing.\n\nThis inventory does not establish original executable parity. OpenAI Codex (LLM) produced the tooling and report. Human original-Windows captures are still needed for runtime parity. See the [comparison and measured results](ENEMY-ATTACK-AUDIT-2026-10-30.md) and [special encounter timing](SPECIAL-ENEMY-CADENCE-2026-10-30.md).']
        args.markdown.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('prototype_count','attack_count','missing_animation_count','apk_sha256')}))


if __name__=='__main__': main()
