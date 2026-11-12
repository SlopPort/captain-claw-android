# Bullet constructor, virtual methods and shared motion

OpenAI Codex (LLM), 2026-11-12. Follow-up to the [unowned callback review](REA-REGISTRY-COVERAGE-2026-11-12.md) within the [full REA audit](REA-FULL-AUDIT.md). Target: supplied CrazyHook-distributed `CLAW.EXE`, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`; REA 6.7.0 / Ghidra 12.1.4. Static findings are not original source, pristine-1997 certification or runtime observations.

## Joined constructor and virtual targets

The registered Bullet wrapper calls constructor **`0x411650`**, which first invokes shared constructor `0x4757f0`, then installs the vtable at **`0x50ced8`**. The two zero stores at object offsets `+0x50/+0x54` belong to one 64-bit field in the surrounding motion layout; they must not be interpreted as two separate motion components. A common image-set fallback is requested only when the owner's image metadata is absent.

Constructor Evidence: `ev_19423d69e14c48bd1f0504b86f454f100a4f4f7b3ee0df1e4c392d8d295ce77b`; shared constructor: `ev_475f99bdb9c80e04ca5dd076c29747bb8980de8ff37e15f0c8280ad65a9ef28c`. The complete bounded vtable read is `ev_dd1fc60a7d3ea0a710c02a61c5c3c0a601976479eee038b22e4b153d1923cb20`.

Only slots actually joined to these call paths are classified here. Reading adjacent words does not establish the vtable's complete extent.

| Slot | Stored target | Observed boundary |
| --- | --- | --- |
| `+0x0c` | `0x4cf5d0` | One return instruction with 4-byte argument cleanup; no gameplay operation in this observed slot |
| `+0x10` | `0x475ac0` | Lookup/invocation through a shared state-function map |
| `+0x14` | `0x4066f0` | Deferred callbacks followed by slot `+0x40` |
| `+0x18` | `0x475d50` | Image-derived geometry initialization, then slot `+0x44` |
| `+0x28..+0x3c` | `0x4ce9b0` | Same return-only target at all six observed slots |
| `+0x40` | `0x4df490` | Shared movement and terrain reconciliation |
| `+0x44` | `0x475df0` | Falling-state entry and movement-mode change |

The `0x4cf5d0` return has instruction Evidence `ev_872900809a8920a1da3addf123bd75cbd00707e676c9533114c1f16684698e04`. Its tiny bounded contract is reviewed; this does not close projectile behavior. The return-only target at `0x4ce9b0` has Evidence `ev_81403d4061986144978ada2a4987387daec47861ee34eda5918fa19642eddb18`.

## Geometry and state entry

The unowned method **`0x475d50`** was inspected through 45 actual REA instructions. When graph metadata is available, it writes the same image-derived bounds into two owner records beginning at `+0x134` and `+0x154`. The four calculations match the independently observed graph-bound helper `0x406490`: two differences supply the lower bounds and two sums minus one supply the inclusive upper bounds. Helper Evidence: `ev_de4fac249559bd2437d3654a0645d9cb125b1418b3122ab6d169a74f4b7c9630`. First-instruction Evidence for the unowned initializer: `ev_2044628ecf458a8e5567f93ad9aafd8dcc178b703df8073bdac92199ec1616db`.

These are geometry records, not yet proof of each collision consumer, an actual supplied frame's rectangle, world-coordinate anchoring or equality with an Android fixture. Do not turn the arithmetic into a global hitbox-size change.

The initializer then invokes the joined `+0x44` target. **`0x475df0`** preserves the previous state code, selects **LS_FALLING**, optionally changes animation and sets the owner's movement mode to **8**. The shared constructor had earlier selected mode **7** for its initial movement synchronization. Thus a mode-7 constant seen in the constructor does not establish the mode used by all later updates.

Falling-entry Evidence: `ev_856dfc445c15b91555de3467111dd3d272d256561cd864dc972799dd206c7625`. Binder `0x475bd0` associates LS_FALLING with `0x475e50`: `ev_5b0f712b6243ec963fef14744e42cfd11791e263d99b647cfc35126f6b2a7f90`. That update advances an optional animation and propagates an observed movement-result bit to an owner flag: `ev_19c55531903572c7b3a9461b1d9653a5a095f6147c3d7042dd23f3e6f079c85f`. The complete meaning and consumers of that flag remain unjoined.

## Shared update and motion: partial comparison

Forwarder `0x4def40` invokes three virtual stages around state-table/name lookup. The joined post stage `0x4066f0` can consume deferred callbacks and then invoke the actual `+0x40` movement target. This resolves several targets that were previously just unexplained virtual calls; it does not prove every feasible state sequence.

The movement routine `0x4df490` advances the motion state relative to a shared clock, submits movement through a terrain-query path and reconciles actual returned coordinates. The inspected normal-axis path in `0x403c30` contains the familiar velocity-times-delta plus half-acceleration-times-delta-squared term, followed by bounds/clamp handling. Floating-stack inputs, all axes, special cases, collision flags and the complete clock contract still require review. Do not describe the entire routine as recovered from that formula alone.

Evidence: forwarding `ev_e6f348cf0e26551bd6088851ce246dcfdbfe7be1d69f3dc29982327ce97e2c88`; post stage `ev_ccb306fa491760ba9d4eeb390aa63934eca84a604c92cf4f56dd0fe00c345d43`; movement `ev_85106caf5d4139a62ca15aa4739e47cb785a9d79e39f3f58f12ab623cbb7c79b`; motion arithmetic `ev_d741d6c9f42a5f90db7198577e8486e3bb7b7107381d25d790db77bb5b75b426`.

Current port sources use XML/component construction, `ProjectileAIComponent` and Box2D. `ClawPhysics::VOnUpdate` submits its supplied elapsed milliseconds to the Box2D step; projectile contact damage is applied through the health component with per-target tracking. Those are concrete adaptation paths. The original rectangle consumers, incoming-hit acceptance, projectile categories, resource-specific launch values and lifetime are not yet joined well enough to certify equivalence or prescribe a physics rewrite. Existing Android contact and sound fixes remain separate evidence.

## Allocation candidate narrowed by the actual default handler

The earlier wrapper review retained a zero-allocation-result path reaching a virtual access through zero. Joining allocator **`0x4fcaea`** shows that it retries allocation according to a configured callback; an absent callback or one that returns false can permit null. However, the **initial stored callback is `0x4fcad0`**, which enters `0x4fb15d` and the C++ exception-throw path. A decompiler's printed trailing return after that call is not evidence that the default handler returns normally.

Evidence: allocator `ev_497c3e28c1c699ba9de9181dde0e96b6dec466f3fb893c0635de8bb5accf8e56`; initial pointer `ev_0cd7fe1d157d5bd0e84105806f34d4989825472155c818ca1ab5b967a2ce33e0`; handler `ev_26cc7b5509dc503994f9d1a94a03b2e21f9fe009995b4dd18962ff118b23f4a0`; throw helper `ev_9eb6da138a7561069ee36efad45ba80b74c265a9e486a39abdc4fa0002054c14`.

The suspicious zero-result branch is therefore **not a confirmed ordinary out-of-memory null dereference**. Whether runtime code replaces/clears the callback, and which exception handlers accept allocation failure, remains open. This initial-file observation does not certify all runtime configurations or justify copying a suspected failure path to Android.

## Coverage and remaining work

Fifteen further initial-inventory functions received evidence-linked **partial** reviews. The two additional unowned regions contain 45 initializer instructions and one prepare-slot instruction. Their code is tracked separately from the original function-body union; supplementary decoded bytes do not invent new function boundaries or close the full audit.

The saved ledger now has **33 partial initial-inventory reviews**. Across the three supplemental regions, **142 distinct decoded instruction starts cover 415 bytes outside acquired function bodies**. This is supplementary instruction evidence, not 415 semantically certified bytes or a new whole-file completion percentage. The original function-body denominator remains unchanged.

Continue with rectangle consumers, terrain/movement flags, specific projectile constructors/resources, state transitions, deferred callback lifetime and incoming-hit acceptance. Raw bytes, complete pseudocode, instruction records and `bullet-vtable-chain.json` remain in the ignored private audit directory. No APK, game data or production behavior changed.
