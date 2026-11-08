"""Validate continuous observation independently of process-survival checks.

OpenAI Codex (LLM). FPS is rounded to one decimal in 300-loop native batches.
Allow only the two partial boundary batches, rounding uncertainty and host poll
resolution; a living background process is not a sustained gameplay result.
"""
import math
import re


def assess_observation(rows, requested_seconds, measured_seconds, log, minimum_batch_fps=None):
    reasons = []
    values = [float(row['fps']) for row in rows]
    valid = bool(values) and all(math.isfinite(v) and v > .05 for v in values)
    if not valid:
        reasons.append('missing_or_invalid_frame_batches')
    if measured_seconds < requested_seconds:
        reasons.append('requested_observation_not_completed')
    background = bool(re.search(r'Entered background|Pazur pad context: mode=(?:0|2)\b', log))
    if background:
        reasons.append('game_left_active_foreground_during_measurement')
    lower = sum(300 / (v + .05) for v in values) if valid else 0
    upper = sum(300 / (v - .05) for v in values) if valid else 0
    gaps = [int(v) for v in re.findall(r'Pazur frame gap: interval=(\d+) ms simulation_skipped=1', log)]
    gap_seconds = sum(gaps) / 1000
    # A measurement can start/end between emitted full batches. Each edge can
    # omit at most one batch; use observed rounded FPS bounds rather than a
    # percentage tolerance which would hide minutes in a long observation.
    allowance = 2 * max((300 / (v - .05) for v in values), default=0) + .5 if valid else .5
    unaccounted = max(0, measured_seconds - upper - gap_seconds)
    if unaccounted > allowance:
        reasons.append('frame_evidence_does_not_cover_observation_duration')
    floor_met = None if minimum_batch_fps is None else valid and min(values) >= minimum_batch_fps
    if floor_met is False:
        reasons.append('requested_batch_fps_floor_not_met')
    return dict(passed=not reasons, reasons=reasons, active_foreground_continuous=not background,
                frame_batch_count=len(values), batch_duration_lower_seconds=lower,
                batch_duration_upper_seconds=upper, explicit_skipped_gap_seconds=gap_seconds,
                unaccounted_seconds=unaccounted, boundary_allowance_seconds=allowance,
                minimum_batch_fps=minimum_batch_fps, batch_fps_floor_met=floor_met,
                scope='300-loop batches with rounded FPS; not per-frame display telemetry')
