# Active Officer on a step

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-23. Huawei Android 10, ARM64 APK
`6175b1b450ca7f46ede0910a884e3608d104e4a86251822aa6c6b4a57d6ca955`.
Controlled fixtures; human owns natural campaign testing. No physical controller.

Sixteen fresh-process trials: level-one Officer, 32 px solid step, both sides
and both vertical relations, standing attack, jump attack, crouch attack and
jump-away with delayed attack. Offensive AI and damage stayed enabled. Setup
initializes hero HP100/pistol99; no health edits, protection or shots during
actions. This is isolated geometry, not the original map's natural stairs.

All 16 finished with no observed player death. Hero took damage in every case.
Target damage was observed in five cases, including three defeats. Four jump-away
cases moved 221–342 px away and cost 10–20 HP. Some requested jumps never became
airborne, and some requested attacks showed no attack animation while hurt.
These outcomes are not sixteen passing fairness verdicts.

| Higher actor | Enemy side | Action | Hero HP lost | Target HP loss observed |
| --- | --- | --- | --- | --- |
| Enemy | Left | Standing | 10 | Yes |
| Enemy | Left | Jump | 10 | Yes |
| Enemy | Left | Crouch | 50 | No |
| Enemy | Left | Escape | 20 | No |
| Enemy | Right | Standing | 60 | No |
| Enemy | Right | Jump | 50 | No |
| Enemy | Right | Crouch | 50 | Yes |
| Enemy | Right | Escape | 20 | No |
| Hero | Left | Standing | 10 | Yes |
| Hero | Left | Jump | 50 | No |
| Hero | Left | Crouch | 60 | Yes |
| Hero | Left | Escape | 10 | No |
| Hero | Right | Standing | 60 | No |
| Hero | Right | Jump | 60 | No |
| Hero | Right | Crouch | 60 | No |
| Hero | Right | Escape | 10 | No |

Four **additional after-hit** trials waited for an actual health decrease before
sending escape. Sampled pre-input HP: 90/80/90/90; final HP: 90/80/90/80. All
became airborne and moved 241–343 px away. Sampled foot separation before input
was 31–32 px, with the requested relation retained. These use a 1000 ms jump and
direction hold plus delayed attack; they do not establish the behavior of a short
tap at every hurt-animation frame. Poll/ADB latency remains part of the setup.

Current OpenClaw code rejects new attacks in TakingDamage and selects ground
kick/uppercut/swipe animations randomly. Normal melee requests use a 50x25 area;
crouching damage is halved. Therefore animation, hurt state, range and timing
must be separated before labelling a miss as a collision bug. This inspection
uses the patched tree based on pinned OpenClaw `5ee5740…`; original Monolith
behavior has not been established by this comparison. The active AI can also
move off the step during actions. Different RNG/attack phases are not controlled
paired evidence of a left/right defect. No balance, hitbox or AI change was made.

### Diagnostic parser correction

The original sixteen JSONs have an empty `area_created` legacy field. Since
0.4.23's crash fix, native diagnostics report `area requested` before deferred
body creation. Empty legacy data must not be interpreted as no attack or no body.
Requests and actual contact rectangles are distinct evidence. All retained
contact records in these sixteen cases had integer AABB overlap.

The parser now records `area_requests` separately and labels the old field as
legacy. The sweep leaves creation confirmation unknown when only deferred
requests exist. A real-log regression matched both request lines where the old
pattern matched none. One additional device trial confirmed the new fields:
six requests, six contacts, zero legacy creation lines. It did not damage the
Officer, unlike the earlier nominally same setup, reinforcing timing limits.
Original reports were not overwritten. Total: 16 action cases + 4 after-hit
cases + 1 parser follow-up, not complete enemy/height coverage.

Ignored evidence prefixes: `active-officer32-huawei-0.4.25`,
`active-officer32-after-hit-huawei-0.4.25`,
`active-officer32-parser-huawei-0.4.25`. Each owned run restores config/progress.
