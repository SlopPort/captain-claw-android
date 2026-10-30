# Level 3 ladder and rope investigation

Implementation and analysis by OpenAI Codex (LLM), following anonymous human feedback. Exact runtime results and retained failures are listed below.

## Leafy ladder summit

The owned Level 3 map uses two summit tiles. Public OpenClaw metadata places
667 caps at the tile origin and 668 caps five pixels below it. The WWD describes
668 climbing collision starting twelve pixels below the origin. The previous
sensor-based exit could therefore restore gravity with the feet nine pixels
below the actual one-way support surface. Releasing Up could then fall through.

The implementation now queries the nearby real ladder cap. It completes the
last twelve pixels of an ascending or neutral mount, positioning the sole two
pixels above that cap before restoring gravity. Downward input, falling and
ordinary intermediate ladder segments cannot trigger this mount assistance.
This is an accessibility/collision correction, not an original-engine parity claim.

Real fixtures: tile 668 at x=5952, tileY=6336 (capY=6341), and tile 667 at
x=7168, capY=6016. Centers are x=5984 and x=7200.

## Swinging vines

The public rope prototype defaults to 120 frames at 25 milliseconds. Actual map ropes override frame duration from the map swing-time property divided by 120, so their periods differ. Previously the hero and grab trigger moved
only when a sprite frame changed, in steps reaching roughly thirteen pixels.
The rope now owns its animation clock, catches up missed rope frames after a
slow update and interpolates hero/trigger placement between those same authored
points each game update, retaining each map rope's frame durations. The rope sprite still uses the original images; this
is not newly generated 60 FPS artwork. Enemy and attack animation clocks are
unchanged. Initial animation pause occurs after all component initialization.

`tools/forest_motion_smoke.py` defines isolated real-map summit, descent and
middle-segment cases plus read-only rope clock samples. It is not a natural
playthrough, and clock samples alone do not prove attached movement or visual
smoothness. No device test was performed by the investigation subagent.

## Retained attempts and scope

Before changing the installed app, tests used debug35 APK `e75748e3a2cd1712f2b05c8eb5f7197af7ade68b5cdca33e3e6e6e9fcb111c91`. An initial harness carried climbing state between diagnostic teleports, so its second-cap failure could not establish a clean baseline. A revised fresh-process harness still observed a paused airborne climb at cap667 after releasing Up; cap668 passed that particular placement. These synthetic placements do not reproduce every human approach or prove that cap668 always fails.

An intermediate debug36 test exposed an inherited `VGetPosition` stub and aborted when summit assistance first called it. The getter now returns the real Box2D body position. A later real rope attachment test exposed a transform call made during Box2D's locked contact callback; initial attachment is now deferred, while per-frame interpolation outside Step remains immediate. All failed fixture owners restored user configuration and saves byte for byte. Intermediate APKs were not published as release artifacts.

## Physical results

Huawei ARM64 debug36 final APK SHA256: `63478ba59d551d37ef9c1fffe3cf473287de09a4dc8c763eb213adc4eeb1c013`. Both ARM ABIs built and package alignment checks passed; ARMv7 was not physically run.

The pre-rope-callback-repair candidate `533f1b64c7ceed4a3669e75b5c362451701a572422dc65b0a368079aeaae6191` passed both real-map cap mount/release, descent and middle-pause cases. The same fresh-process-per-cap matrix then passed again on the final APK: both summit releases were standing/grounded with sole within two pixels of the cap; both descents and intermediate pauses remained climbing without a phantom floor. The earlier getter-crashing candidate was not retained as a passing result.

On the final build, `tools/rope_attached_smoke.py` used timed teleports near the real first rope, removed enemies and protected Claw. The real trigger attached the hero; no attachment callback was invoked directly. Eighteen observations remained attached and matched interpolated handle coordinates within 0.006 pixels, then ordinary jump input detached Claw. This verifies carrying/attachment consistency, not a natural approach or subjective animation quality. The original sprite images remain discrete, and a human smoothness recheck is still needed.

The final APK also passed the level1 first-map-ladder regression: summit hold/release/repeated Up, descent, ladder jump, walking off the top and Up+jump; a separate solid-floor bottom fixture stopped descent and allowed renewed ascent. These are controlled scenarios, not all ladder/edge combinations.
