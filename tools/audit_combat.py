"""Inventory effective enemy prototypes from the exact packaged support archive."""
from pathlib import Path
import argparse
import copy
import hashlib
import io
import json
import math
import xml.etree.ElementTree as ET
import zipfile

PORT = Path(__file__).resolve().parents[1]
REPORT = PORT/'reports/combat-audit'
BOSSES = {'laraux', 'katherine', 'wolvington', 'gabriel', 'marrow', 'marrowparrot', 'aquatis', 'redtail', 'omar', 'laser'}


def merge(parent, child):
    # Mirrors the engine's first-element-by-path TinyXML merge, including repeated tags.
    parent.attrib.update(child.attrib)
    if child.text and child.text.strip():
        parent.text = child.text
    for element in child:
        target = parent.find(element.tag)
        if target is None:
            parent.append(copy.deepcopy(element))
        else:
            merge(target, element)
    return parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apk',type=Path,default=PORT/'app/build/outputs/apk/debug/app-debug.apk')
    args=parser.parse_args()
    REPORT.mkdir(parents=True, exist_ok=True)
    # EngineSupport now installs the APK's canonical XML bundle. Imported
    # game-data/ASSETS.ZIP can be older and is not the effective engine source.
    with zipfile.ZipFile(args.apk) as apk:
        support=apk.read('assets/import-support/ASSETS.ZIP')
    (REPORT/'provenance.json').write_text(json.dumps(dict(
        apk_name=args.apk.name,apk_sha256=hashlib.sha256(args.apk.read_bytes()).hexdigest(),
        support_sha256=hashlib.sha256(support).hexdigest()),indent=2),encoding='utf-8')
    with zipfile.ZipFile(io.BytesIO(support)) as archive:
        raw = {}
        for name in archive.namelist():
            if name.upper().startswith('ACTOR_PROTOTYPES/') and name.lower().endswith('.xml'):
                element = ET.fromstring(archive.read(name))
                raw[element.get('ActorPrototypeName')] = (name, element)
    def resolve(name, chain=()):
        assert name not in chain, chain
        element = copy.deepcopy(raw[name][1])
        if element.get('Parent'):
            element = merge(resolve(element.get('Parent'), chain+(name,)), element)
        return element
    inventory, requests, errors = [], set(), []
    for prototype, (path, _) in sorted(raw.items()):
        root = resolve(prototype)
        if root.find('EnemyAIComponent') is None or 'BASE_' in path or 'BASE_ENEMY' in path:
            continue
        if any(prototype.lower().endswith('_'+boss) for boss in BOSSES):
            continue
        if root.find('HealthComponent') is None:
            continue
        health = int(root.findtext('HealthComponent/Health'))
        maximum = int(root.findtext('HealthComponent/MaxHealth'))
        body = root.find('PhysicsComponent')
        size = {k:float(v) for k,v in body.find('CollisionSize').attrib.items()}
        failures = []
        if not 0 < health <= maximum: failures.append('invalid health')
        if min(size.values()) <= 0: failures.append('invalid body size')
        if body.findtext('HasCapsuleShape') == 'true' and size['width'] >= size['height']:
            failures.append('invalid vertical capsule')
        actions = []
        special_actions = []
        animation_path = root.findtext('AnimationComponent/AnimationPath', '')
        for component in root:
            for action in component.findall('Attacks/AttackAction'):
                name = action.findtext('Animation')
                frame = int(action.findtext('AttackAnimFrameIdx', '0'))
                area = action.find('AttackAreaSize')
                damage = int(action.findtext('Damage', '0'))
                projectile = action.findtext('ProjectileProto') or action.findtext('ProjectilePrototype')
                if frame < 0: failures.append('invalid attack frame')
                ani = animation_path.rsplit('/',1)[0]+'/'+name.upper()+'.ANI'
                requests.add(ani)
                actions.append({'state':component.tag,'animation':name,'frame':frame,
                                'damage':damage,'area':area.attrib if area is not None else None,
                                'offset':action.find('AttackSpawnPositionOffset').attrib if action.find('AttackSpawnPositionOffset') is not None else None,
                                'projectile':projectile})
        for field in ['DiveInAnimation','DiveOutAnimation']:
            name=root.findtext('DiveAttackAIStateComponent/'+field)
            if name:
                ani=animation_path.rsplit('/',1)[0]+'/'+name.upper()+'.ANI'
                requests.add(ani)
                special_actions.append({'kind':field,'path':ani,'frame':None})
        punk=root.find('PunkRatAIStateComponent')
        if punk is not None:
            cannon=resolve(punk.findtext('CannonActorPrototype'))
            cannon_path=cannon.findtext('AnimationComponent/AnimationPath').rsplit('/',1)[0]
            for field, base, frame_field in [
                ('RatFireAnim',animation_path.rsplit('/',1)[0],'RatFireAnimFrameIdx'),
                ('RatRecoilAnim',animation_path.rsplit('/',1)[0],None),
                ('CannonFireAnim',cannon_path,'CannonFireAnimFrameIdx'),
                ('CannonIdleAnim',cannon_path,None)]:
                ani=base+'/'+punk.findtext(field).upper()+'.ANI'
                requests.add(ani)
                special_actions.append({'kind':field,'path':ani,'frame':int(punk.findtext(frame_field)) if frame_field else None})
        entry={'prototype':prototype,'type':root.get('Type'),'source':path,'health':health,
               'max_health':maximum,'body':size,'hurtboxes':[ET.tostring(f,encoding='unicode') for f in body.findall('ActorFixture')],
               'attacks':actions,'special_attacks':special_actions,'issues':failures}
        inventory.append(entry)
        errors.extend({'prototype':prototype,'issue':issue} for issue in failures)
        ET.ElementTree(root).write(REPORT/(prototype+'.xml'),encoding='utf-8')
    requests.update('/CLAW/ANIS/'+name+'.ANI' for name in ['SWIPE','KICK','UPPERCUT','JUMPSWIPE','DUCKSWIPE'])
    (REPORT/'inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
    (REPORT/'animation-requests.txt').write_text('\n'.join(sorted(requests))+'\n',encoding='ascii')
    (REPORT/'issues.json').write_text(json.dumps(errors,indent=2),encoding='utf-8')
    for row in inventory:
        print(row['prototype'],row['health'],row['body'],len(row['attacks']),row['issues'])
    print(f'{len(inventory)} regular enemy prototypes, {len(requests)} attack animations, {len(errors)} structural issues')


if __name__ == '__main__':
    main()
