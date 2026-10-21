"""Read attack sound references in the exact APK XML and user-owned loose assets.

Writes metadata only to ignored reports. Missing/silent definitions are findings,
not permission to invent replacement recordings or change original sound design.
"""
import argparse
import copy
import json
import struct
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from io import BytesIO
from audit_combat import merge, PORT


def animation_events(path):
    data=path.read_bytes();header=struct.unpack_from('<8I',data);position=32+header[4];events=[]
    for frame in range(header[3]):
        flag=struct.unpack_from('<H',data,position)[0];position+=20
        if flag==2:
            end=data.index(0,position);name=data[position:end].decode('ascii');position=end+1
            if header[1]!=1:events.append((frame,name))
    assert position==len(data),path.name
    return events


def event_sound(event,animation):
    value=event.replace('_','/')
    if 'LEVEL/' in value:
        value='/'+animation.lstrip('/').split('/')[0]+'/SOUNDS'+value[value.index('/'):] + '.WAV'
    else:
        root,tail=value.split('/',1);value='/'+root+'/SOUNDS/'+tail+'.WAV'
    return value.upper()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);args=parser.parse_args()
    report=PORT/'reports'/args.report;report.mkdir(parents=True,exist_ok=False)
    assets=PORT.parent/'Assets';definitions={};cache={}
    with zipfile.ZipFile(PORT/'app/build/outputs/apk/debug/app-debug.apk') as apk:
        with zipfile.ZipFile(BytesIO(apk.read('assets/import-support/ASSETS.ZIP'))) as support:
            for name in support.namelist():
                if 'ACTOR_PROTOTYPES/' in name.upper() and name.upper().endswith('.XML'):
                    root=ET.fromstring(support.read(name));prototype=root.get('ActorPrototypeName')
                    if prototype:definitions[prototype]=root
    def resolve(name):
        if name not in cache:
            root=copy.deepcopy(definitions[name]);parent=root.get('Parent')
            cache[name]=merge(copy.deepcopy(resolve(parent)),root) if parent else root
        return cache[name]
    rows=[]
    for prototype in sorted(definitions):
        root=resolve(prototype);enemy=root.find('EnemyAIComponent')
        if enemy is None or 'Base' in prototype:continue
        pattern=root.findtext('AnimationComponent/AnimationPath','')
        sounds=enemy.findall('Sounds/Sound')
        for component in root:
            for action in component.findall('Attacks/AttackAction'):
                name=action.findtext('Animation');animation=pattern.rsplit('/',1)[0]+'/'+name.upper()+'.ANI'
                path=assets/animation.lstrip('/').upper();references=[]
                if path.exists():
                    references=[event_sound(event,animation) for _,event in animation_events(path)]
                sound_type='RangedAttack' if 'Ranged' in component.tag else 'MeleeAttack'
                references += [sound.get('SoundName').upper() for sound in sounds if sound.get('SoundType')==sound_type]
                missing=[value for value in references if not (assets/value.lstrip('/')).is_file()]
                rows.append(dict(prototype=prototype,state=component.tag,animation=animation,animation_exists=path.exists(),
                                 effects=sorted(set(references)),missing=sorted(set(missing)),
                                 no_effect_defined=not references))
    player=[]
    for name in ('SWIPE','JUMPSWIPE','DUCKSWIPE','KICK','UPPERCUT','PISTOL','MAGIC','POSTDYNAMITE'):
        animation='/CLAW/ANIS/'+name+'.ANI';path=assets/animation.lstrip('/')
        references=[event_sound(event,animation) for _,event in animation_events(path)]
        player.append(dict(animation=animation,effects=references,missing=[v for v in references if not (assets/v.lstrip('/')).exists()]))
    result=dict(player=player,enemies=rows,attack_actions=len(rows),
                missing_actions=sum(bool(row['missing']) for row in rows),silent_definitions=sum(row['no_effect_defined'] for row in rows))
    (report/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('attack_actions','missing_actions','silent_definitions')}))


if __name__=='__main__':main()
