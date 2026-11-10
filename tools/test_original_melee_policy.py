#!/usr/bin/env python3
"""Compile boundary assertions against the production custom-melee policy."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', help='C++ compiler (syntax-only; no host linker needed)')
    args = parser.parse_args()
    compiler = args.compiler or shutil.which('clang++')
    if not compiler:
        sdk = Path(os.environ.get('ANDROID_HOME', Path.home() / 'AppData/Local/Android/Sdk'))
        candidates = sorted(sdk.glob('ndk/*/toolchains/llvm/prebuilt/windows-x86_64/bin/clang++.exe'))
        compiler = str(candidates[-1]) if candidates else None
    compiler = compiler or shutil.which('g++')
    if not compiler:
        parser.error('Pass --compiler or install a C++ compiler / Android NDK')
    assertions = ['#include "OriginalMeleePolicy.h"', 'using namespace OriginalMeleePolicy;']
    # Modulo 101 is deliberately not approximated as percentages summing to 100.
    for roll in range(101):
        expected = 'Lunge' if roll < 40 else 'Knife' if roll < 80 else 'FrontFlip'
        assertions.append(f'static_assert(SelectTigerMove({roll}) == TigerMove::{expected}, "move {roll}");')
    for image in (0, 200, 201, 202, 203, 204, 205, 300):
        expected = 'true' if image in (203, 204) else 'false'
        assertions.append(f'static_assert(CrabDamageImage({image}) == {expected}, "crab image {image}");')
    assertions.extend([
        'static_assert(!PassedTarget(99,100,1), "right before target");',
        'static_assert(PassedTarget(100,100,1), "right exact target");',
        'static_assert(PassedTarget(101,100,1), "right overshoot");',
        'static_assert(!PassedTarget(101,100,-1), "left before target");',
        'static_assert(PassedTarget(100,100,-1), "left exact target");',
        'static_assert(PassedTarget(99,100,-1), "left overshoot");',
        'static_assert(PixelsPerSecondToPhysics(180) == 2.4, "fish speed units");',
        'static_assert(PixelsPerSecondToPhysics(300) == 4.0, "tiger lunge speed units");',
        'static_assert(PixelsPerSecondToPhysics(250) > 3.333 && PixelsPerSecondToPhysics(250) < 3.334, "flip speed units");',
    ])
    with tempfile.TemporaryDirectory(prefix='pazur-melee-policy-') as directory:
        source = Path(directory) / 'checks.cpp'
        source.write_text('\n'.join(assertions) + '\n', encoding='utf-8')
        subprocess.run([compiler, '-std=c++11', '-fsyntax-only', '-I', str(ROOT / 'native'), str(source)], check=True)
    print('PASS: 101 Tiger choices, 8 crab images, target crossing in both directions, 3 speed conversions')


if __name__ == '__main__':
    main()
