# Platform displacement, restored support and update slices — 2026-11-12

OpenAI Codex (LLM) performed this static follow-up to the [ladder/carrier review](REA-LADDER-CARRIERS-2026-11-12.md). Target identity and the whole-audit completion contract remain in the [full audit](REA-FULL-AUDIT.md). Human identity is omitted. Raw commercial code and dossiers remain private. No target execution, phone operation or gameplay change occurred.

## A joined platform writer and passenger consumer

The literal registration table names callback `0x4a05c0` **StandardElevator**. Its prologue reads the supplied actor and that actor's auxiliary logic block; the movement writes below are to the actor itself, not the auxiliary structure.

Its normal moving states write signed X/Y displacements at actor `+0x174/+0x178`, then add those same values to actor position `+0x5c/+0x60`. For ordinary nonnegative configured rates and timing inputs, a moving axis uses the low 32 bits of the rate/timing product divided unsigned by 1000, applies direction and limits the displacement magnitude to 16. An axis already at its directional limit receives zero. Both directional target tests must be satisfied before changing between states 1000 and 1001; the observed code does not clamp each new position to the exact endpoint. Input overflow, negative rates and exceptional timing require their own bounds analysis rather than real-number arithmetic assumptions.

Initialization assigns exact actor category field `+0xe8 = 0x80`, joining it to the landing/retention predicates already reviewed. It also initializes geometry from image/configuration records, applies a special level/resource geometry case, fills absent movement bounds/rates, and sets its first movement state. Those descriptor/resource and randomization paths remain partial; no universal platform hitbox or default trajectory is inferred from one branch. Actor flags `+0x180` bits 1/2 select rider-sensitive stop/start branches that clear displacement before an early return; the shared global rider pointer's lifecycle remains open.

Shared motion routine `0x4df490` checks the passenger's support flag and selected-object pointer, then adds selected-object `+0x174/+0x178` to passenger X/Y and synchronizes its floating position state before its own movement query. This establishes these fields as **displacements applied per motion update** for the joined platform path, rather than raw velocity. It does not establish how many times the writer/consumer execute per rendered frame or that all platform classes share this writer.

Evidence: registry `ev_a0162601b97d4058ade6152e23adcfe39066a5d253a50d8378183689aaa58f4b`; platform `ev_de67d7e2c50569f5cf84f7da268ff32af4b5f71595f5c7a37dfcb4b69ce31b03`; shared motion `ev_85106caf5d4139a62ca15aa4739e47cb785a9d79e39f3f58f12ab623cbb7c79b`.

## Update-slice dependency

`0x42c650` copies three supplied timing values into globals `0x535920/24/28` and mirrors the first/second into `0x5aafdc/0x5aafd8`. The latter second value is the platform multiplier above.

Its joined caller `0x46cfe0` saves the three current values, computes `ceil(second / 18)` using unsigned division/remainder, and advances the first/third through slices of 18 with a final remainder. Before each slice it publishes that slice's values through `0x42c650`; it then calls an update helper and manager virtual slots, with additional plane helpers between selected slices. It restores the saved timing tuple after the loop. Zero elapsed input performs no slice. The body also has a later hero/image-selection branch, which is not closed by reviewing the slice loop.

This prevents describing the platform's 16-pixel cap as necessarily a per-rendered-frame cap. The [later object-pass review](REA-OBJECT-PASSES-2026-11-12.md) joins the default manager targets and countdown/count-gated logic callback path inside each slice. Complete active membership, alternate construction, outer clock units and all timing-global writers remain dependencies. Millisecond interpretation is consistent with the division by 1000 and nearby clock usage, but the complete upstream clock-to-loop contract is not yet established. Large/signed-overflow elapsed values also require caller constraints.

In the port, `BaseGameApp.cpp` passes measured SDL elapsed milliseconds to `BaseGameLogic::VOnUpdate`. Its active `if (true)` branch passes that interval directly to physics, and `ClawPhysics::VOnUpdate` calls `Box2D::Step(msDiff / 1000.0f,10,8)`. The inactive alternative is not evidence of active substepping. These checked paths differ from the original slice mechanism; no change to the port's loop or claim about natural collision failure is made here.

Evidence: setter `ev_3ac387a79a6ce4710f33c31f74488b4121b650e16b7af3f88c00b79ad0f4857e`; slice caller `ev_caf53182610503059fd6155eb6a64d9efbfd23e6adf9b3dd835681d44854c901`.

## Selected-object initialization and restoration

Creation paths `0x4c90f0` and `0x4c92c0` explicitly zero actor `+0x98`, together with several callback pointers, before their final initialization/registration. Their allocation, virtual initialization, constructor/destructor dependencies and exceptional paths are not fully reviewed. This establishes two initialization paths, not all object lifetime invariants.

Object operation dispatcher `0x4c7930` handles a bounded observed code set. For code 3 it saves selected-object identity `selected[+0x188]` into actor `+0x184`, or zero if none exists, then invokes the logic callback with a temporary operation value. For code 8, a zero saved identity or failed engine lookup clears actor `+0x98`; a successful lookup stores the resolved pointer. It subsequently invokes the corresponding logic callback and base dispatcher. Other branches call stream-like serialization helpers. Callers must still establish when these operation codes occur; this is evidence for identity-based restoration, not proof of the complete save/load or live-removal lifecycle.

Lookup wrapper `0x4fc9aa` writes its output only on success. Its helper `0x4fc945` selects bucket `(unsignedId >> 4) % bucketCount`, walks the chain for an exact key and returns the matching node or null. It computes the division before checking bucket storage; a valid nonzero bucket count and well-formed chain are caller/constructor prerequisites. Table construction, identifier reuse and removal synchronization remain open, so no dangling-pointer or divide-by-zero bug is asserted from this helper alone.

Evidence: creation `ev_32604726e994a112803676b4eb07226bc19e6a920f276970550585869cf8a0a7`, `ev_dfe5237b0240a7a23878d97151965d863a4ffce2c8c445b58f6b1f4f944d1c1b`; operation dispatcher `ev_1311ab0caa2693a20dcdf62b5115fd0bcd011a39b79b837e6861c9e5bc40e4be`; lookup `ev_b4f15a911142b57699b8404c1385c321bf02e8645ae975e89db4d9723e779ef3`; bucket helper `ev_1180356143a63df31c4e43ef18a7c4456e7108d1f9b519fca7f2b31bb23e849f`.

## Avoiding offset-only field identities

A cached-instruction scan retained 74 candidates using numeric offsets `+0x178` or selected `+0x98` references. They are not 74 proved carrier accesses. For example, auxiliary constructor `0x4ca0b0` initializes its own `+0x178` alongside buffer/list fields, and object factories store that auxiliary allocation at actor `+0x7c`. These are different receivers from actor displacement `+0x178`; they must not be merged into one global field meaning. Evidence: `ev_bea996e1eb7590fad9e8484c55077615a764dc40de0374bf5b84365119bdfcd3`.

The port's relevant `KinematicComponent`/`PathElevatorComponent` paths use Box2D speed, carried-body lists and external speed assignment. The checked kinematic path also delays reevaluating start-behavior passenger removal by more than 100 ms. The exact original StandardElevator-to-port actor conversion and every stop/start subtype remain unjoined; these source paths are not declared a one-to-one equivalent. Contact/pointer lifetime and real frame-spike behavior still need separate comparisons.

Nine additional initial-inventory functions receive partial reviews, and shared motion's existing review gains the platform-displacement join. The later object-pass report joins specific deferred/direct removal paths. The full machine-code audit, selected-carrier pointer lifetime and human campaign acceptance remain open.

Registry regeneration previously reset every callback row to unreviewed. The generator now joins explicit function/region decisions after checking their target identity and retains which review source supplied the status. Successful registration or decoding still cannot create a semantic pass. Synthetic coverage-contract tests exercise decision preservation, bounded-region provenance, absent decisions and stale-source removal; they do not test gameplay parity. The actual registry was regenerated without queuing new acquisition requests.
