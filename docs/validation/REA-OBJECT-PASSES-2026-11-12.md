# Object update, contact ordering and removal — 2026-11-12

OpenAI Codex (LLM) performed this static follow-up to the [platform timing review](REA-PLATFORM-UPDATES-2026-11-12.md). Exact target identity and the whole-audit contract remain in the [full audit](REA-FULL-AUDIT.md). Human identity is omitted. Original bytes, instructions and pseudocode remain private. No target execution, device operation or game behavior changed.

## Identifying the missing virtual targets

Engine initialization `0x4cf730` constructs a manager at engine `+8` and installs vtable `0x5143b8`. REA's read of that table binds slot `+0x1c` to `0x4c9680` and slot `+0x38` to `0x4c9ac0`. Both targets lie outside the initial inventoried function bodies. They were decoded as bounded regions, not silently declared new complete functions.

The previously joined slice loop `0x46cfe0` calls those same receiver offsets in that order for every slice, with argument 0 for the update slot. This closes the targets for the observed default constructed manager path. Alternate construction/subclasses and the complete outer state lifecycle remain open.

Evidence: initializer `ev_5b9f89bd48e9cb12117e5cfdc7a075703abba901226f652f02d9b4f431273cbb`; target reference `ev_710674313d7c071d0cc50c300dfa281c6734cbec40088dee8a0e05e3f88783d3`; vtable bytes `ev_69518f6844b0ad1aa08b026c96eeb79d82c53571a2ae049dfddff6d923351cd0`.

## Update and deferred maintenance

Region `0x4c9680` initializes/reset two scratch collections and walks the manager's object list, saving the next node before invoking logic. A nonzero argument refreshes the timing difference from the clock import; argument 0 preserves the already published interval, as needed by the slice path.

For each object, auxiliary countdown helper `0x4ca0f0` consumes that interval. It returns 1 only while a nonzero countdown remains; zero or expiration returns 0, allowing the next gate. An auxiliary count at `+0x24` then suppresses/decrements by one invocation; otherwise the callback pointer at auxiliary `+0x10` is invoked with the object. Thus the registered StandardElevator callback can participate in the per-slice update when this object's countdown/count gates allow it. This is not a statement that every registered callback runs in every slice.

After the callback, owner flag `+8` bit `0x10000` queues removal; otherwise bit `0x20000` queues reordering. The removal collection is processed after the main traversal. Selected removal paths invoke a logic callback with operation `0x1d`, remove the list node and erase identity entries from maps at manager `+0x48/+0x2c`, then invoke the object's deleting virtual method. An object flag `0x800` takes a shorter destruction path. The reorder collection clears `0x20000`, removes the old list node and reinserts without repopulating identity maps.

Insertion helper `0x4c9a20` optionally inserts identity entries into both maps and places the object according to field `+0x74`, with an exception for peers carrying `0x20000`; it stores the list node at object `+0x78`. `0x4c99c0` directly removes/deletes through corresponding paths, while `0x4c9dd0` removes a supplied node and both map entries without deleting the object. Valid pointers and initialized collections remain preconditions.

These observations establish specific removal paths, not complete callback mutation safety or carrier-pointer lifetime. No clearing of every other object's selected-carrier pointer is proved by these routines. Do not equate owner flag `+8` bit `0x10000` with a same-valued bit in a separate movement-result word without tracing the actual assignment.

Evidence: region entry `ev_d9d9da3d5ad34ad0a35276f8ab8c39f76668d2ff3daec353acb0ce558d392b3c`; countdown `ev_f272e11727bbed535e9f4daa6f51fc5bc257673462368dc2fa4d56fc94cbbc11`; insertion `ev_c8903a6b2d9ccee3c5fd7e585b718996e08347b5974ae30fddc1d1efe5005b75`; direct removal `ev_d6824f7356636392875616d4461af64a92d02f6ad7490a9a2ceabc1128736bf6`; detach `ev_5ee27f7f732848036d96d2ed613479cbd8552ab9afe41cc69de1ead72766a080`.

## Ordered contact pass and distinct rectangles

Region `0x4c9ac0` traverses unordered pairs from the object list. It excludes pairs according to object flag 1 and differing flag `0x40000`, then considers both directional interactions separately. Further flags and category/mask combinations can suppress either direction; overlap alone is insufficient.

For a direction with target A and source B, it compares A's translated rectangle `+0x144..+0x150` with B's translated rectangle `+0x154..+0x160`, rejecting `INT_MIN` left-bound sentinels. The first direction uses rectangle helper `0x4cac90`; the reverse uses `0x4c9cf0`, which translates the same respective records. Both use inclusive signed edge comparisons, so an exactly touching edge can satisfy this geometric predicate. This joins distinct incoming/outgoing geometry consumers; it does not prove a common terrain-body shape.

For this direction, `B[+0xe8] & A[+0xec]` selects the target hit action, while `A[+0xe8] & B[+0xf0]` selects the source notification. If selected and installed, B's auxiliary callback at owner `+0x88` runs **first**, with B's partner field `+0x8c` set to A. The target action then either calls A's handler at owner `+0x80`, with partner field `+0x84` set to B, or takes the numeric-health branch described below. The reverse direction repeats with A/B swapped. Callbacks may change state before the remaining work; no simultaneous-damage or symmetric acceptance guarantee follows.

`0x4ca3d0` joins the target notification path. With target flag 8 set, it subtracts source `+0x120` from target `+0x128`; a nonpositive result writes operation `0x1c` to target auxiliary `+0x1c`. Otherwise it invokes the installed target callback if present. The contact pass contains the equivalent operation inline in its first direction and calls this helper in the reverse direction. Timer, interruption, parry and invulnerability acceptance inside individual actor callbacks remain separate dependencies.

Evidence: region entry `ev_53691c38ffee3f8575bf597cbee151cfa2b302d624ef71529d9e3d51bb9bfbe6`; rectangle helper `ev_347de7046e673f11dca3c9b1e1aea0e1311dc2b6b2b189a464a23e97756824ec`; translated-actor helper `ev_843b07da9dabc367c75cd8f63c0c4ecf175c1d170754aa745505ce919fe9d0cc`; target action `ev_5e7374faaa2440c00ea248f752c7237a62c88c01593f7613c827e40af8b09a24`.

## Other work inside the slice

`0x46eac0` updates an input-suppression countdown and selects normal input processing or a clearing helper. It also contains conditional Windows command/close messages and a later inactivity timer. Those control conditions are retained; the full application input/message lifecycle is not closed.

Plane helpers `0x4d2e20` and `0x4d2e90` reject a missing spatial helper, derive integer center coordinates from bounds or flagged floating calculations, then call `0x4d5b30`/`0x4d5cf0`. The first underlying routine skips unchanged centers and queries three spatial collections. The other scans objects with flag/region-dependent detach, notification and destruction branches. These are partial spatial-activation joins, not proof that every registered object is always in the active update list. Spatial collection callbacks, camera state, float-to-integer inputs and every offscreen branch remain open.

Evidence: input update `ev_a810d482710185ab17688eaca9e99fb40e3f9bbb325f047e5fde66c362a58404`; plane helpers `ev_e1d2bda16f0efaa271c1394523c963c8c6405d3e616af3076b4e912ce0f74d52`, `ev_f43d8fd60452706adc0c3942faa262e616276026f26dd7a20452ae71e4fa3d32`; spatial routines `ev_d06c7bc46b62c5c46bc3c9763d1ef6091f4e795d00acbbab88768cef96a8bb5c`, `ev_aef3659487eb0e1979e6ee63f2cc77febae3f8e17391d4a23d783b3492281c0a`.

## Port comparison and disposition

The port uses Box2D contacts and `AreaDamageComponent`/`HealthComponent` rather than this pair loop. `AreaDamageComponent::VOnApply` computes an SDL intersection for the impact point but requests the health change after that conditional, relying on the earlier contact/application path. Do not treat that optional impact rectangle as an independent overlap gate or patch it without tracing the caller. Existing Android contact diagnostics are opt-in; no such test was run here.

The original nested traversal can consider a quadratic number of object pairs before its category/geometry filters. Reproducing that traversal is not required to preserve accepted contact behavior in a Box2D port. This is a static complexity observation, not a measured original bottleneck or a claim about the current Android frame rate.

The original geometric predicate is two-dimensional: vertical separation can prevent a hit, but touching edges may qualify before callback filtering. Exact hero/enemy rectangles, facing/animation state, per-target recovery and the source-notification-before-target-action order must all be joined before deciding whether a diagonal counterattack should succeed. These generic methods do not close the human-reported stair combat or boss-block issue and do not justify enlarging all attack boxes.

The two supplemental regions contain 333 decoded instruction starts with complete bounded traversal, while call contracts remain explicit gaps. Thirteen further initial-inventory functions receive partial reviews. The engine initializer and spatial/input routines retain wider unresolved branches; none is declared a fully understood subsystem. Full audit and natural campaign acceptance remain open.
