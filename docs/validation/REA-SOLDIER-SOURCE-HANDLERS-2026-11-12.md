# Soldier source handlers and Android hit deduplication

Independent analysis by OpenAI Codex (LLM). This continues the [Soldier receiver audit](REA-SOLDIER-HIT-ACCEPTANCE-2026-11-12.md) for the same supplied CLAW.EXE, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. Six additional initial-inventory functions receive bounded, partial reviews. No gameplay change or runtime equivalence is claimed.

## Original source-category dispatch

The previously joined common receiver `0x43f9c0` performs token and elapsed-time rejection **before** the following handlers. Their absence of a local timer setter does not bypass the inherited gate or reset a previously stored interval. Exact installed-vtable reads and function assembly support this table:

| Incoming category | Slot / method | Observed behavior after common acceptance |
| --- | --- | --- |
| `0x20` | `+0x4c` / `0x44edb0` | Scalar damage, impact feedback, source flag `+8 |= 0x10000`, low hurt entry |
| `0x2000000` | `+0x50` / `0x44ede0` | Scalar damage, impact feedback, low hurt entry; conditional elemental effect creation |
| `0x10` | `+0x54` / `0x44ef40` | Scalar damage, impact feedback, low hurt entry |
| `0x1000000` | `+0x58` / `0x44ef70` | Scalar damage, impact feedback, **2000-unit** gate setter, low hurt entry |
| `0x1000` | `+0x5c` / `0x44efa0` | Motion-limit writes, virtual transition and trajectory calculation; no direct scalar-damage call |

These numeric categories are not all certified weapon names. A projectile constructor's unrelated auxiliary `+0xe8` floating-point field must not be confused with actor category `+0xe8`. Source flags, actor flags and geometry fields likewise require their exact structure context.

The category-`0x20` source flag write is concrete. Whether and when it removes or otherwise consumes the source needs its consumer; this report does not call the flag a proved immediate destruction operation.

The category-`0x2000000` method tests logic `+0x474` only **after** damage and hurt entry. A nonzero value suppresses this method's extra effect creation, not its preceding health subtraction. For global values `0x26b8`, `0x26b9` or `0x26ba`, it requests fire, lightning or ice effect resources, stores the created object, configures its animation and sets flag 2. Resource availability, allocation failure handling, effect lifetime and flag consumption remain dependencies. Other global values return without this extra effect.

The category-`0x1000` method initializes three pairs of motion limits, invokes installed slot `+0x7c`, then derives three velocity components from source auxiliary coordinates and the receiver's double-precision motion state. It has small-result and near-zero-acceleration branches plus square-root/division paths. The installed transition at `0x4406c0` acts only in owner mode 1: it selects an update callback, initializes motion, sets mode 8 and LS_JUMP, and selects an animation. These observations support a motion-transition contract; source identity, valid input ranges, numerical edge behavior and the complete caller contract remain unresolved. Treating every common hit callback as health damage would be incorrect.

The **300-unit** category-2 gate from the preceding report and this **2000-unit** gate are separate source-handler policies using the same setter. Full outer clock normalization remains open. No single replacement invulnerability duration is justified by these constants.

## Android deduplication is already present, with different scope

The current [projectile component](../../upstream/OpenClaw/OpenClaw/Engine/Actor/Components/AIComponents/ProjectileAIComponent.cpp) rejects inactive projectiles, null targets, the source actor and targets already inserted into its `m_HitActors` set. Insertion occurs before looking up health and before `AddHealth` can reject damage. A target whose damage request is refused is therefore still recorded by that projectile. This is a concrete ordering similarity, but its key is **projectile instance plus target identity**, whereas the reviewed original receiver uses a victim-side last global hero attack token and a separate elapsed gate. They are not interchangeable contracts.

Ordinary melee is created through [Claw animation handling](../../upstream/OpenClaw/OpenClaw/Engine/Actor/Components/ControllableComponent.cpp) as an area-damage actor. Its [area component](../../upstream/OpenClaw/OpenClaw/Engine/Actor/Components/AreaDamageComponent.cpp) inherits the [pickup observer](../../upstream/OpenClaw/OpenClaw/Engine/Actor/Components/PickupComponents/PickupComponent.cpp), which is registered with the [trigger component](../../upstream/OpenClaw/OpenClaw/Engine/Actor/Components/TriggerComponents/TriggerComponent.cpp). [Physics contact handling](../../upstream/OpenClaw/OpenClaw/Engine/Physics/PhysicsContactListener.cpp) delivers trigger entry.

The trigger tracks overlapping actor entries and suppresses another notification while that actor remains represented. Leaving removes one entry; a later entry after all overlaps end can notify again. Area damage itself has no lifetime target-hit set and returns false from application, leaving destruction to its duration path. Thus the checked suppression is per continuous overlap, not a proved once-per-swing token contract. This is a static behavioral distinction, **not evidence that a natural short-lived melee actor actually hits twice**. Contact lifetime, fixture ordering and attack duration still need a joined scene-level check.

Existing foot-sensor damage exclusions and projectile multi-fixture deduplication remain in place. The earlier broad comparison must not be read as claiming that the port lacks all duplicate-hit protection. No production edit, device use or campaign result follows from this report.

## Provenance and remaining work

The source-category mapping comes from common receiver Evidence `ev_b5087d54100b89febee215ba2d92acaa069181feb0cd4f4d96cfb182e1e07e62`. Exact installed table reads: `ev_955fddf4e7a4d7a97717a3b813898a18b60cd70803b4a0fe9d963533a06fa82e` and `ev_a59c18a11d18926c8872fb8bc7673c77263fd0d2daddc0fc4ae5b0a6e6e2fcc0`.

| Method | REA dossier Evidence |
| --- | --- |
| `0x44edb0` | `ev_c97ed94afa9c05e20d58b5cc6a113a2ce919129d20faab998f2a87394e2798f9` |
| `0x44ede0` | `ev_44044ff3d40a85a4c8dc997f83f03aa35ae4c60e9341140b8b1a92136804a974` |
| `0x44ef40` | `ev_ddf7a5e67dcdfa5ac5e9a55ddad8ff8110399768d44baf29ef1a938558a43910` |
| `0x44ef70` | `ev_f3b36af24aef52a0eaa450bafb03f6cfa7273aabc1111338ba2216f60316ba1d` |
| `0x44efa0` | `ev_5968265f97517ec533bbfc188c34ce9c7760905064f2a6d9baab0e305220c622` |
| `0x4406c0` | `ev_ea20f482ac9848c3c24d5a11a6fe020e22b882e71dd15c2126ad0eb2a7b47146` |

Next obligations include certified source constructors/categories, shared-gate clock and token changes outside hero melee, source-consumption flags, effect cleanup, numerical preconditions and full hurt-state exit behavior. The natural diagonal-fight report remains unresolved. Raw commercial bytes, assembly and pseudocode stay private; these independent explanations do not establish original source recovery or whole-file audit completion.
