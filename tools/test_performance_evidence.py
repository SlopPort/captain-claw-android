"""Regression for the observed background-process false positive, by Codex."""
from performance_evidence import assess_observation


def batches(count, fps=60):
    return [dict(fps=fps, p95_ms=18, max_ms=25) for _ in range(count)]


def main():
    complete = batches(239)
    assert assess_observation(complete, 1200, 1200.2, '', 55)['passed']
    missing = assess_observation(batches(133, 54), 1200, 1200.2, '')
    assert not missing['passed'] and 'frame_evidence_does_not_cover_observation_duration' in missing['reasons']
    duplicated = assess_observation(batches(480),1200,1200.2,'')
    assert not duplicated['passed'] and 'frame_evidence_exceeds_observation_duration' in duplicated['reasons']
    background = assess_observation(complete, 1200, 1200.2, 'Entered background', 55)
    assert not background['passed'] and not background['active_foreground_continuous']
    assert not assess_observation(complete,1200,1200.2,'Pazur pad context: mode=2',55)['passed']
    low = list(complete);low[50] = dict(fps=54, p95_ms=27, max_ms=29)
    floor = assess_observation(low, 1200, 1200.2, '', 55)
    assert not floor['passed'] and floor['batch_fps_floor_met'] is False
    assert not assess_observation([], 1200, 1200.2, '')['passed']
    assert not assess_observation(batches(10), 1200, 50, '')['passed']
    # A long skipped loop remains explicitly visible, never invented as FPS.
    gap = assess_observation(batches(237),1200,1200.2,'Pazur frame gap: interval=10000 ms simulation_skipped=1',55)
    assert gap['passed'] and gap['explicit_skipped_gap_seconds']==10
    print('PASS: complete run, missing/excess coverage, background, FPS floor, empty/short run, explicit skipped gap')


if __name__ == '__main__':main()
