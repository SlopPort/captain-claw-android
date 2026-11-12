# Soldier hit acceptance: token, time and hurt state

Independent analysis by OpenAI Codex (LLM). Target: supplied CrazyHook-distributed CLAW.EXE, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. This is a static, bounded follow-up to the [whole-file audit](REA-FULL-AUDIT.md), not recovered original source or certified Windows/Android parity.

## Joined receiver

The Soldier dispatcher at `0x48dc20` constructs logic through `0x48dd90` and stores the initialized pointer in actor auxiliary `+0x18`. This joins the previously reviewed LogicHit forwarding path to a concrete receiver. Two unsigned guards constrain its indexed input to 0..80; an exact 81-byte indirection table selects only five pointer-table entries. The resolved construction/message branches add **96 independently decoded instruction starts**. Eleven call-contract gaps remain; bounded traversal completion does not certify the whole dispatcher.

The constructor calls inherited initialization at `0x44d900` and installs vtable `0x51124c`. Exact REA reads join these slots:

| Slot | Target | Bounded role |
| --- | --- | --- |
| `+0x1c` | `0x44f7c0` | Hit receiver; optional elemental death-resource selection, then shared hit dispatch |
| `+0x44` | `0x405170` | Scalar HP subtraction |
| `+0x48` | `0x44ecb0` | Source-category-2 contact response |
| `+0x60` | `0x44f1e0` | Transition to LS_HOME |

Inherited initialization assigns actor category **4**, mask `0x3001032`, last attack token -1 and initially zero elapsed-gate fields. Thus the [hero hit-mask follow-up](REA-HERO-HIT-ENTRY-2026-11-12.md) now has a concrete initialized Soldier category to compare with its category-4 suppression. Later mutations and complete source classification remain open; this is not blanket immunity against all enemies.

## Rejection order matters

At `0x43f9c0`, the shared path:

1. Reads the global hero's player-data attack token and rejects an unchanged token.
2. Records a new token **before** checking unsigned elapsed time against the stored interval.
3. Dispatches the incoming source category to its virtual handler when time permits.
4. Checks the victim's HP and dispatches death handling when appropriate.

Hero attack setup at `0x41f270` increments the same player-data field. Therefore an attack rejected by the elapsed gate has already consumed its token at this stage; continuing contact from that token does not simply become eligible when time expires. The shared preamble also precedes non-hero category branches, whose complete interactions need further review.

The category-2 handler at `0x44ecb0` accepts damage only when the current state is neither LS_HITLOW nor LS_HITHIGH. It invokes scalar damage, requests impact feedback, calls `0x43f9a0` with **300**, and selects the high/low hurt entry. The setter records the interval and current global clock separately. These are elapsed-time units; complete outer clock normalization remains an explicit dependency.

If already in either hurt state, that handler instead calls slot `+0x60`. Its installed method clears horizontal motion, saves the prior state and selects LS_HOME, without the scalar subtraction on that branch. This is state-dependent hit acceptance, not proof of a random Soldier parry mechanic.

The scalar method at `0x405170` contributes **11 independent instruction starts**: when HP is initially positive, it subtracts source damage without a zero clamp. It contains no timer or parry test itself. Its simplicity cannot justify removing caller gates.

## Current Android comparison

The checked [health implementation](../../upstream/OpenClaw/OpenClaw/Engine/Actor/Components/ControllerComponents/HealthComponent.cpp) changes HP before notifying observers. [Enemy AI](../../upstream/OpenClaw/OpenClaw/Engine/Actor/Components/EnemyAI/EnemyAIComponent.cpp) then enters its hurt state for a surviving damaged enemy. The [hurt-state implementation](../../upstream/OpenClaw/OpenClaw/Engine/Actor/Components/EnemyAI/EnemyAIStateComponent.cpp) raises AI priority until animation completion; its initializer does not parse `InvulnerabilityTime`, and its update is empty. The [level-1 Soldier prototype](../../asset-overrides/ACTOR_PROTOTYPES/LEVEL1/LEVEL1_SOLDIER.XML) contains that setting with value zero.

These checked paths do not implement the original token-before-time rejection ordering or its already-hurt LS_HOME branch. The subsequent [source-handler and deduplication comparison](REA-SOLDIER-SOURCE-HANDLERS-2026-11-12.md) joins existing projectile hit sets and trigger overlap suppression; neither should be mistaken for an absence of all duplicate-hit protection. AI interruption priority is not itself HP immunity. Existing hit-sound fixes remain intact.

No gameplay change follows from this report. In particular, neither these gates nor numeric HP differences alone explain the reported natural stair fight. Complete attack reach, hero recovery/input, source lifetimes and terrain placement still matter. No campaign or phone result is claimed.

## Evidence and remaining work

REA Evidence for the dispatcher byte carrier: `ev_865fe6a5d0dc4dd555deb05cba6ddc8dfabd798be1f748fb04fe718d9bcd8b03`; scalar carrier: `ev_695cac9c096f80efe2d5f31301a92882f98403678cbdead0746b1527c8015ad4`. Capstone 5.0.7 independently decodes those exact REA-returned bytes; its results are not relabelled as Ghidra instruction Evidence or newly established function boundaries.

Vtable reads: `ev_955fddf4e7a4d7a97717a3b813898a18b60cd70803b4a0fe9d963533a06fa82e`, `ev_a59c18a11d18926c8872fb8bc7673c77263fd0d2daddc0fc4ae5b0a6e6e2fcc0`. Constructor: `ev_928ad5d609195703ab7bcc717e3121cef52aaf48bc0016097aa29bf66ee0b817`; inherited initialization: `ev_c51c504396e9999d8359068a656d0f43823140e58c2cef0ea18dbec0193bae80`.

Hit dispatch: `ev_b5087d54100b89febee215ba2d92acaa069181feb0cd4f4d96cfb182e1e07e62`; category-2 handler: `ev_cca9c5e69aae2e4d0df5afd3ffcc68d750926497f8b12cecf765d1e90045079f`; interval setter: `ev_273c71d9fc0e0a2f0b9d0e1bedcb53d7e3b3ccb25741dc9f05dbdef532ecd5b9`; LS_HOME method: `ev_b7965a42f27ef01349cc68939ff34fa63d5d1b64dafa516cc37e4f5d1e683297`. Token producer: `ev_2e6bbd6ed72f8cb4514ef6c268268e9ce3956e7f71d46864924d4326490a4954`.

Eight initial-inventory function reviews and both supplemental regions remain explicitly partial. Next: join the port's contact/source deduplication, original non-hero source handlers and clock contract. Resource failures, complete state transitions, allocation policy, dynamic mutations and natural scene equivalence remain unresolved. Raw bytes, assembly and pseudocode remain private.
