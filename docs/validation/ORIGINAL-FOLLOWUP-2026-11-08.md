# Original-behavior follow-up: remaining custom policies

2026-11-08. Static investigation and independent explanations by OpenAI Codex (LLM), guided by anonymous human feedback. This is not original source, a decompiler transcript or original Windows runtime evidence.

## Reference and evidence ownership

Reference: supplied CrazyHook-distributed CLAW.EXE, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`, not certified pristine 1997. Matching cached REA/Ghidra evidence was reused and bounded instructions/vtables were checked against that immutable executable. Raw listings remain private under the dated `todo-*-original-2026-11-07` report directories. Addresses below identify the examined boundaries; no new REA Evidence ID is invented for direct bounded decoding.

These findings narrow TODO questions. A written specification alone does not close runtime, natural-play or full-parity gates.

## Crab: rectangle and re-hit boundary (COMBAT-05)

Constructor `0x44bce0` captures the current sprite rectangle through `0x406490`, inflates it by 15 horizontal and 10 vertical pixels, and caches it. The helper combines four image-metadata fields into `(c-a, d-b, c+a-1, d+b-1)`. Binding those fields to the actual PID resource and constructor image remains necessary before replacing port geometry.

Strike callback `0x44cba0` publishes that cached rectangle at images 203/204 and mirrors horizontal bounds as `(-right,-left)`. The 200 ms gate in this callback controls sound replay, not repeated damage. No outgoing per-target latch was found locally; an incoming Crab-hit latch is a different path. The shared player receiver/token/immunity rules remain unresolved. Keep current configured geometry and per-window deduplication until that shared boundary is established; absence of a local latch does not justify damage every frame.

## Fish: distinct states, not a vertical lunge (COMBAT-06)

Home `0x443a80` requires the shared proximity classification and matching swimming direction. With a higher hero, the observed draw below 80 in integer domain 0..100 can enter JumpStrike; another eligible in-bounds branch uses a draw below 90 for ordinary Strike. Shared region priority matters: a central class-4 rectangle can shadow class 3, so simply expanding the current melee sensor would change decisions.

Ordinary Strike is the already implemented captured-X horizontal lunge at 180 px/s. JumpStrike entry/update `0x443c00` / `0x443ee0` is separate: fixed relative target X +/-150 and screen Y waterline-150, Y acceleration 2000, image-202 chomp cue, and distinct terrain/out-of-water recovery. The inherited field `+0x88` is physics position Z, not a speed. Initial solver arithmetic can be derived, but a calculated initial vector is not a measured flight duration or proof of identical integration.

The shared lower-edge tile routine `0x4cd610` can set state 1, consumed by JumpStrike to enter OutOfWater `0x4442c0`. Recovery update `0x4443b0` uses 60 px/s floundering, a 250 ms facing gate and waterline/swim-bound checks. Full call order, resource-bound rectangles and accepted re-hit behavior remain unjoined. Implementing a guessed jump from the existing generic sensor would not close COMBAT-06.

## Tiger Guard: one safe continuation, other flags still bounded (COMBAT-07)

The successful front-flip captured-target crossing in `0x499020` enters `0x498ca0(1)`: exactly one knife follows, without a new random 2-4 chain or decision gate. Current source prepares this narrow continuation for debug40, retaining direction, committed targets and the existing deadline. It still needs exact-candidate device verification. Mere animation wrap, boundary exit and timeout are not relabelled successful crossings.

Other findings are deliberately separate. Knife's local outgoing rectangle can persist across repeated animations; its shared damage acceptance is unresolved. The flag written by Home/lunge/front-flip controls forwarding of callback `0x499390`, not demonstrated blanket health immunity. Knife can inherit it. The Home/obstacle graph includes additional classifications, world queries and a distinct back-flip. Do not add invulnerability, repeated contact damage or automatic refacing from these incomplete observations.

## Siren: cancellation and audio fallback (COMBAT-08)

No new stock-data defect was proved by the static review. The port clears pending notes when leaving the state or dying and retains the recovery deadline. Both local original and port logic emit a due note before checking singing expiry; a slow update must not be simulated merely by sleeping the host script.

A newly constructed original Siren with a null singing resource retains zero duration, can emit its first note and return Home in the same update; recovery is independently installed. The port's same-frame guard defers zero-duration termination until the next update. A sufficiently long next update can therefore permit one due follow-up before exit. This is a documented fallback difference, not permission to invent a 900/1000 ms replacement duration. SDL mixer-unavailable `-1`, missing resource and original decoder failure are separate cases. Muting a valid decoded sound does not make its duration zero.

`tools/siren_interruption_smoke.py` exercises real projectile callbacks and records pending-note cancellation, re-entry and death separately. Its existence is not a passed test. Original visibility dispatch, corrupt-resource loading and game-clock pause behavior remain bounded unknowns.

## Le Rauxe: conditional pause and consumed attack tokens (BOSS-02)

Home `0x481a60` selects actions by nested player-origin regions and random branches. Shared continuation `0x44f210` adds a 300-600 ms Home pause only when the actor remains in Home and the applicable class-3/4 branch does not select an immediate action. A successful transition skips that continuation pause. This does not support a delay after every strike.

Incoming melee `0x481810` installs a 350 ms interval, including when it blocks. Dispatcher `0x43f9c0` first rejects an already seen player-derived attack token; a new token is stored before checking elapsed time. A token first seen too early may remain consumed after the interval expires. Token creation/lifetime and category mapping must be established before implementing this as port immunity. The previously recovered ordinary block predicate remains 100/1001 and is not a blanket rule for every damage path.

Moves check arena bounds, destination support and headroom. The long jump targets the opposite arena edge, not an arbitrary short hop over the hero. Hurt completion can request an immediate action independently of the Home pause. Current cadence/hit acceptance remains an explicitly bounded port accommodation until these paths are joined.

Key cached REA references: Home `ev_0a26ea186661fda08c508f8b17dc97fc433a806f2c497448f6e0a56ebe53a6d6`; continuation `ev_2696cc29a7e5431f28fd413f49a6f8458ed0bc3c5219f15bd0fd44e5b08f1a73`; incoming melee `ev_b48084fc784601d638cbbe99bf126af286fd456e64ebb896cfa53628d0ab9b04`.

## Gabriel: persistent request, death-entry counter (BOSS-04)

Pirate death callback `0x4865f0` decrements the active boss counter when the encounter exists and is not complete, then continues shared death processing. The slot is released at death entry, not after corpse destruction. The current live-actor/health adaptation is close for ordinary deaths but not proven identical for arbitrary removal. The original summon counter also increments after allocation failure; reproducing that failure behavior is not a robustness requirement.

The boss sets a boolean fire request at image 401 (`0x445db7`). Cannon update `0x448130` can retain it while earlier reset/rise/lower branches return. Consumption invokes the firing selector and clears the request; multiple unconsumed requests coalesce. Current direct Fire calls can drop the opportunity while the cannon is busy. A boolean pending-request policy should preserve it through transitions, consume once, and clear on reset/end, with an explicit port readiness contract. That change is not yet implemented or verified in debug40.

Reset `0x4480b0` clears local and boss requests; encounter reset `0x446bc0` clears count/signals and requests cannon reset. All interruption/reset callers and original firing-state side effects still need joining before claiming full parity. Preserve the existing two-pirate limit.

## Acceptance boundary

For a production change, verify both directions, entry/leave/death/reset, one effect per intended action, actual contacts and negative cases on the exact APK. Keep speculative geometry/immune-state changes out of narrow proven fixes. Technical fixtures do not replace the human's natural campaign, original-runtime recordings or final compatibility checks. Remaining tasks stay visible in [TODO](../../TODO.md).
