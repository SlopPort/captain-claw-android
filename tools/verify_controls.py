"""Verify the multi-touch device test's native input state transitions."""
from pathlib import Path
import argparse
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('report', nargs='?', type=Path,
    default=Path(__file__).resolve().parents[1] / 'reports/joystick-0.4.1/native.log')
report = parser.parse_args().report
text = report.read_text(encoding='utf-8-sig')
states = [tuple(map(int, groups)) for groups in re.findall(
    r'Pazur controls: left=(\d) right=(\d) jump=(\d) attack=(\d) fire=(\d) up=(\d) down=(\d)', text)]
expected = [
    (0,1,0,0,0,0,0), (0,1,1,0,0,0,0), (0,0,1,0,0,0,0), (0,0,0,0,0,0,0),
    (0,1,0,0,0,1,0), (0,0,0,0,0,1,0), (0,0,0,0,0,0,1),
    (1,0,0,0,0,0,0), (0,0,0,0,0,0,0),
    (0,1,0,0,0,0,0), (0,0,0,0,0,0,0),
    (0,0,1,0,0,0,0), (0,0,0,0,0,0,0),
]
assert any(states[i:i+len(expected)] == expected for i in range(len(states))), states
for required in [(0,0,0,1,0,0,0), (0,0,0,0,1,0,0)]:
    assert required in states, ('Action button was not reached', required, states)
assert states[-2:] == [(0,1,0,0,0,0,0), (0,0,0,0,0,0,0)], ('Focus loss did not release stick', states[-2:])
print('PASS: stick+jump, independent release, diagonals, dead zone, ownership, shared action, cancellation, action buttons and focus reset')
