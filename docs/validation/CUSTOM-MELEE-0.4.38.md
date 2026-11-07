# Custom melee reconstruction in 0.4.38

OpenAI Codex (LLM) implemented the changes below. The human remains anonymous.
This is a clean-room adaptation of observations from the supplied executable,
not recovered original source code. Existing OpenClaw code remains under its
upstream licence; no original executable, artwork or raw disassembly is included.

## Evidence and implementation

The reference is the same CrazyHook-distributed x86 `CLAW.EXE` used in the
[0.4.37 custom-event investigation](ORIGINAL-CUSTOM-EVENTS-0.4.37.md), SHA-256
`33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`.
It is not certified pristine. Prior REA/Ghidra registration evidence was reused;
bounded Capstone inspection of the same immutable PE established additional
movement, rectangle and timer rules. Private evidence is retained locally under
`reports/custom-melee-0.4.38`; proprietary instruction listings are not published.

| Enemy | Previous port behaviour | Implemented rule and original reference |
|---|---|---|
| Hermit Crab, level 7 | One stationary transient hitbox at frame 4 | A moving damage window opens at image 203 (frame 3), remains eligible during image 204 (frame 4), and closes on loop, interruption or state exit. Original strike callback `0x44cba0` exposes its rectangle at these two images. The ANI has five images: the window spans nominally 20 + 100 = 120 ms. |
| Fish, levels 11 and 12 | Stationary hit at image 202 | Strike entry `0x4440c0` exposes the rectangle immediately and sets horizontal speed to 180 pixels/second. Strike update `0x444190` restores its inert rectangle and exits after crossing the captured player X coordinate. Image 202 plays the chomp sound; it is not the damage-onset event. Both level variants now use this moving lunge. |
| Tiger Guard, level 14 | Standing strike2 versus crouch-selected strike1, plus an unrelated generic jumping roll | Original entry `0x4988e0` chooses a 1250â€“2000 ms entry gate and one of three moves using `rand() % 101`: values 0â€“39 lunge, 40â€“79 knife, 80â€“100 front-flip. Knife entry/update `0x498ca0` / `0x498de0` uses strike1 and repeats 2â€“4 times. Lunge entry/update `0x498a10` / `0x498b70` uses strike3 and horizontal travel at 300 pixels/second. Front-flip entry/update `0x498eb0` / `0x499270` uses frontflip, 250 pixels/second and a 100-pixel destination with a 1000 ms travel limit. |

The Tiger constructor binds strike1 and strike3; the previous standing strike2
was not supported by this evidence. The recovered knife rectangle is
`[-63,-58,0,-1]`, with base damage 15; the lunge rectangle is
`[-74,-39,-1,15]`, with base damage 20. The executable's referenced damage
multiplier at `0x524580` is 1.0. The port's existing player difficulty scaling
still applies after these base damage values. Health totals are unchanged.
Knife damage begins on image 202; lunge damage begins on image 402. The lunge
stops its horizontal velocity on image 800. The front-flip uses its animation's
visual motion without introducing the previous generic roll's physical jump.

The older report's description of Fish as requiring an unspecified
"movement/apex" comparison is superseded: the recovered fields in this Strike
path describe horizontal speed and X position, not a vertical jump apex.

## Integration and safety

`native/OriginalMeleeAttack.cpp` derives from the existing melee state and is
registered under its existing component identity on Android. Normal enemies
continue through the upstream implementation. Only XML with
`OriginalAttackPolicy` enables custom behaviour. Level 12 Fish inherits level 11.
The Tiger's obsolete crouch-only and generic roll components were removed.

Damage windows test the existing player physics AABB at the owner's current
position, then call the normal health component. Existing invulnerability,
damage feedback and difficulty handling remain in effect. Each target is
eligible once per window. No temporary damage body is left behind; the window
is cleared by state exit, animation mismatch or completion. Committed target IDs
are retained after entry-sensor exit, so a valid moving attack does not lose its
target simply because its entry sensor no longer overlaps. IDs are snapshotted
before health callbacks, resolved through the live actor registry to strong
references, and checked for positive health and an existing physics body before
reading an AABB. This avoids using a removed actor after a death callback.
Custom travel preserves vertical physics velocity and clears horizontal travel
when interrupted. World collisions and existing patrol borders remain active.
A bounded travel timeout prevents a solid wall trapping the attack state.

The Tiger's entry deadline is measured in game-update time and runs during the
current move. It is not inserted before every knife animation. An expired
deadline wakes only a patrol state, once, so it cannot cut short hurt or parry
animations. The state-exclusion flag used while selecting a successor is cleared
after selection; it must not prevent subsequent attack entries.

## Validation

`python tools/test_original_melee_policy.py` compiles assertions against the
production rule header. It passed with the installed NDK compiler: all 101 move
selector values, eight boundary image IDs, target crossings in both directions
and three physics-unit conversions. These checks establish arithmetic and
boundary behaviour, not in-game performance or complete AI equivalence.

`tools/custom_melee_smoke.py` is the physical regression fixture. It requires an
explicitly selected device, checks the installed APK hash, protects the player,
and uses `CampaignSession` to restore config and saves. It checks Crab windows
and contacts from both directions, Fish movement and repeated entry in both
directions at levels 11 and 12 (moving the protected player outside and back into
the fixed-patrol fixture's real sensor), and all three Tiger moves with repeated decision
deadlines and knife-chain bounds. Bounded diagnostic logs are disabled in normal
play. Final physical results and the exact APK are recorded in the release's
update report; the existence of this tool alone is not a passing test result.

## Remaining fidelity boundaries

This does not certify complete original AI. Crab and Fish preserve the existing
port's configured rectangle sizes and initial sensor ranges, rather than claiming
exact reconstruction of original PID-derived rectangles. The Fish's separate
original JumpStrike path and its original swimming-home eligibility are not
reconstructed here; the current importer provides a single Fish prototype per
level. Tiger uses the engine's current patrol, collision, hurt and parry systems;
the original per-state hit-reaction flag and the complete home/obstacle decision
graph are not recreated. Knife windows are reset between consecutive knife
animations, so exact original multi-knife contact persistence is unverified.
No original-Windows runtime timing measurements or natural campaign completion
were performed for this report. Map traversal and final encounter fairness
remain human testing tasks.

The physical follow-up initially observed all three Tiger moves but only knife contacts. A source/ANI recheck exposed premature lunge travel: original update `0x498b70` holds horizontal speed at zero on initial image 800 (500 ms), then enables 300 px/s travel on later images. The implementation now preserves that wind-up; otherwise it could cross the captured target before image 402 activated damage. The strengthened runtime test requires both 15-damage knife and 20-damage lunge contacts.
