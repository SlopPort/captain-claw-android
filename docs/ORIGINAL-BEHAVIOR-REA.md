# Original-behavior investigation with REA

Investigation date: 2026-10-24. Tool: [Reverse Engineer Anything](https://github.com/morluto/rea), rea-agents 6.7.0 with Ghidra 12.1.4. Analysis and port implementation were performed by OpenAI Codex (LLM), following human bug reports.

## Scope and limits

The input was a player-supplied, local Windows CLAW.EXE, file version 1.4.5.0,
from a CrazyHook distribution, not a certified untouched 1997 executable.
SHA-256: `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`.
Community structure definitions supplied naming hints; static instructions and
REA output supplied behavioral evidence. Decompilation is not original source
code or a runtime experiment. No executable, assets, or decompiled functions
are redistributed here. Analysis used a temporary project, closed afterward.

## Receiving a hit and counterattacking

The Captain Claw state dispatcher at `0x416ee0` calls melee input handling from
standing, walking, jumping/falling and crouching states. Its hurt state (`0x1f`)
instead calls the hurt update at `0x41d3f0`, without calling melee dispatch.
The hurt update returns the actor to standing (`0x18`) when that animation ends.

**Conclusion:** attacking during the hurt animation is not supported by this
static evidence; attacking after recovery is supported. This does not prove
that every higher enemy can be hit from every stair position. Repeated hits,
actual attack rectangles and animation timing still matter.

The port's 400 ms pending-melee-tap window is an intentional input accommodation,
not a claim that the original used the same buffer. No new original immunity
duration has been established. In particular, the value 1500 written to player
data offset `0x114` is named RunningSpeedTime by the community mapping; it must
not be presented as evidence of 1500 ms damage immunity.

Evidence:
- State dispatcher: `ev_a67f5bdd15e10db298be5a71d2653e4cfe8d08abd3fe096a0d8579ba99f068a1`
- Hurt recovery: `ev_e6476c5e0f4e7bd0d5e05de83b28842e6c65c18314fc07c6590979739ddce418`
- Melee dispatcher: `ev_22b6c7e45b63f1632c21b7b5e351f29f8a3cdd7feefe8b29cd5594d19abf60a5`

## Stable platform ends

The inspected executable stores a rectangular movement extent. After hurt
recovery its horizontal extent is -16 to +16 pixels. Ground support reads tile
information below the movement rectangle, with multiple horizontal probes in
the main actor update. A teeter state/animation also exists. This differs from
the port's previous rounded lower collision fixture.

The Android adaptation replaces only Claw's lower circular fixture with a flat
sole, keeping the previous lowest point and the upper fixtures. Other actors
retain their fixtures. This follows the rectangular-support principle; it is
not certified pixel-for-pixel parity with the original tile solver.

Huawei fixtures on 0.4.30 show stable support at both ends with partial sole
overlap, stable crouching, and falling once the sole no longer overlaps. The
standing height shifts by approximately 0.7 px because Box2D polygon contacts
use a different skin. The full first-ladder/seam/exit/jump matrix also passed.
These isolated fixtures do not certify natural campaign traversal.

Evidence: support query `0x4cddf0`,
`ev_20a74eb2982ac3b4c46ad4d4f5e678d1b8fc80c4dbba6d81d23821986af53cfc`,
and the dispatcher/recovery evidence above.

## Important differences still requiring care

- Original attack construction at `0x41f270` selects different rectangles and
  damage for standing swipe, crouch swipe, kick, uppercut and jumping swipe.
  Ordinary standing swipe writes 5 damage, whereas the existing port uses 10.
  Actor origins and animation windows differ, so copying rectangle constants
  directly would not establish parity and could introduce new bugs.
- Original target selection allows a vertical position difference below 100 px.
  Selecting a nearby target does not mean the actual attack rectangle hits it.
- The Soldier dispatcher and CaptainClawHit entry were not recognized as full
  functions by this analysis. Raw instruction reads were available, but this
  is not sufficient to claim a complete enemy damage/timing reconstruction.
- Original runtime behavior on the reported natural staircase remains untested.
  The human tester should check the same location after the input/foot changes.

Attack construction evidence:
`ev_4dac6420a6262ee02313141af6508d5c51f0bd4ba144a87068a3552d9b1717bf`.
Target-selection evidence:
`ev_d425740111805ce19ba62fa12332ad63aa3935b9f12aa1b692e679d74daa5b28`.
