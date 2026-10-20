"""Produce an experimental OpenClaw config, preserving upstream gameplay settings."""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

PORT = Path(__file__).resolve().parents[1]


def prepare(source, output):
    tree = ET.parse(source)
    root = tree.getroot()
    changes = {
        'Display/UseVerticalSync': 'true',
        'Display/IsFullscreen': 'true',
        # The engine reserves 16 channels for speech; leave 16 for effects.
        'Audio/MixingChannels': '32',
        'Audio/MusicVolume': '8',
        'Audio/MusicOn': 'true',
        'Audio/Frequency': '22050',
        'Audio/ChunkSize': '1024',
        'Assets/ResourceCacheSize': '64',
        'ControlOptions/TouchScreen/Enable': 'true',
        'DebugOptions/SkipMenuToLevel': '1',
        'DebugOptions/LastImplementedLevel': '14',
    }
    size = root.find('Display/Size')
    if size is None:
        raise ValueError('Missing Display/Size')
    size.set('width', '640')
    size.set('height', '480')
    for key, value in changes.items():
        node = root.find(key)
        if node is None:
            raise ValueError(f'Missing upstream setting: {key}')
        node.text = value
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(tree)
    tree.write(output, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=PORT / 'upstream/OpenClaw/Build_Release/config.xml')
    parser.add_argument('--output', type=Path, default=PORT / 'profiles/low-end.xml')
    args = parser.parse_args()
    prepare(args.source, args.output)
