# Double-tile boundary query family — 2026-11-12

OpenAI Codex (LLM) performed this bounded static review. The human remains anonymous. Target identity, descriptor initialization and the independent converter comparison are in the [tile report](REA-TILE-PARTITION-2026-11-12.md). Raw instructions remain private. No target execution, APK change or campaign test occurred.

## Joined methods and contracts

The observed double-tile vtable at `0x51418c` binds eight boundary-query entries, distinct from point-query slot `+0x18`. All eight have now been decoded through REA to their returns. None was present as an entry in the initial Ghidra function inventory. Completion of these bounded instruction worklists does not certify their callers or whole-program reachability.

Let `L,T,R,B` denote the configured inclusive rectangle, `W,H` the tile dimensions, and `I,O` its inside/outside attributes. The names below describe the direction of the selected boundary; they are not recovered original symbols. Comparisons are signed. The routines do not independently validate the descriptor, point against the entire tile, or output pointer storage.

| Descriptive query | Unfiltered / filtered entries | Required perpendicular span | Candidate from outside the rectangle | Candidate from within the rectangle |
| --- | --- | --- | --- | --- |
| Left boundary | `0x4d7500` / `0x4d7560` | `T <= y <= B` | If `x > R`, select `R,I` | If `L <= x <= R` and `L > 0`, select `L-1,O` |
| Upper boundary | `0x4d76b0` / `0x4d7710` | `L <= x <= R` | If `y > B`, select `B,I` | If `T <= y <= B` and `T > 0`, select `T-1,O` |
| Right boundary | `0x4d75d0` / `0x4d7640` | `T <= y <= B` | If `x < L`, select `L,I` | If `L <= x <= R` and `R < W-1`, select `R+1,O` |
| Lower boundary | `0x4d7780` / `0x4d77f0` | `L <= x <= R` | If `y < T`, select `T,I` | If `T <= y <= B` and `B < H-1`, select `B+1,O` |

If neither branch applies, the method returns 0 and does not write outputs. The unfiltered form accepts `(x,y,boundOutput,attributeOutput)`, writes both selected values and returns 1. The filtered form accepts `(x,y,requiredAttribute,boundOutput)` and succeeds only if the candidate attribute equals the requested value; a filter mismatch also leaves output untouched. All consume four 32-bit stack arguments. Caller behavior when no result is produced remains a separate obligation.

The vtable slot order is left pair `+0x20/+0x24`, upper pair `+0x28/+0x2c`, right pair `+0x30/+0x34`, lower pair `+0x38/+0x3c`. Address order alone would put these in a different order; the mapping comes from the retained vtable read, not that heuristic.

## Evidence

Vtable read: `ev_b853aa2a827fb35ff7895edb33e38cef948b5b32d8cc45ce205bafec072ff8b9`.

| Entry | Entry instruction Evidence |
| --- | --- |
| `0x4d7500` | `ev_1ac28ff01b5d26adafe1b128a94df4822ae25c9ffe18db219660e052f1b972e5` |
| `0x4d7560` | `ev_a028bc3a09aa37e7d0fc000480610dbb9a30ff33749bf670bf0d7ebceb05bd89` |
| `0x4d76b0` | `ev_9a42e75a0e7a58b9bb0924608dea78564fd818e528b74f8dd46a14409a1a3ad3` |
| `0x4d7710` | `ev_afc29c52ccae780ff0b400a4c73b212336f10c80b334f4f6edd7f9e25773ca12` |
| `0x4d75d0` | `ev_4dcd9ea735a7f36fbd01c3ff1c81067aabf0e23dda819594298fb7cc654a06bb` |
| `0x4d7640` | `ev_5bb4cfac3a3b6e365675d2a358271e22a27cf11cd450750142bbc76b8ba6d522` |
| `0x4d7780` | `ev_bdaa0c95fd493a471bc9f6c1dbbde12353b5e8504270be95fd70087983c8d252` |
| `0x4d77f0` | `ev_233a1a0489b1d6b872e15acc8cb077254b2fe590ca83e7fe590322f443359125` |

Each private region record retains every decoded instruction's own Evidence reference, branch destinations and traversal limits. The six newly acquired methods contain 230 distinct decoded instructions with no unresolved intra-region edges or calls. A selected traversal window is not a recovered function-body definition or a proof that surrounding bytes are padding.

## Port comparison and limits

### Adjacent size and type slots

Slot `+0x1c` is distinct from the boundary/point queries. Its single implementation `0x4cfdd0` returns 20, its double implementation `0x4cea60` returns 40, and its mask implementation `0x4ceb30` returns the low 32-bit dimension product plus 16. These are complete bounded arithmetic observations, consistent with descriptor sizes consumed by the previously joined initializers; the calling serialization/storage contract remains unjoined. They are not object allocation sizes (the factory allocates 16, 36 and 24 bytes).

Entry evidence: single `ev_6f9319a9230e8aa4c39955d2c5afaf405ed45fa995bdb26c8432a2f413cd5607`; double `ev_2abe51f7aa5c87dc09fcc373b79e9b6c83fb912079f296c8e505c429bf05443e`; mask `ev_38fe032f038dc59e29fa7b65f6d252bd611a3ad5a2c69d244c3bc61649f25e1a`. No overflow or storage validation exists in these tiny methods. The double type slot `+0x14` points to `0x4cb930`, which returns constant 2 without a memory operation: `ev_0e3be1d34099ecc7bc15233b42cba543f18a98417dde2a26ccd8f5bb4cb36ded`.

### Mask release boundary

The mask destructor's release helper `0x4fcb13` forwards its pointer to `0x4a6c59`. That routine treats null as a no-op and selects heap paths by global allocator mode: mode 3 tries one ownership lookup/release path, mode 2 another; unrecognized pointers and other modes reach Windows `HeapFree`. Lock/cleanup helpers surround the specialized paths. Ownership validation, coalescing, exceptional cleanup and allocator-global initialization are not fully joined, so this is a release-path boundary review rather than allocator correctness certification. Evidence: forwarding `ev_e88a7a4355f68a09503c1ebebdbcee7bda0c899b92630ae63230fde9d2f4b932`; dispatch `ev_3fd24d462081cde64d9c3496ff74cc8e2a06c883d606c3af67e9085aede373e9`.

The port delegates memory management to its C++/Android runtime. Copying the Windows heap implementation is not required; mask-buffer ownership and cleanup would still need explicit equivalence if that original format is implemented.

The observed `R`, `B`, `L-1` and `T-1` choices provide further independent support for inclusive rectangle semantics. The Android port constructs Box2D geometry; it does not directly implement this virtual query family. Its previously recorded conversion discrepancies remain bounded converter findings, without a proved natural scene cause.

The four previously reviewed terrain edge consumers invoke point-query slot `+0x18`. Do not attach these newly described boundary methods to hero movement merely because they share a vtable. Resolve actual call sites, receiver identity and the no-result convention before making that join. Mask and single-tile implementations of the other query slots remain separate work.

The port's `BaseGameLogic::CollideableTileCreatedDelegate` was also checked: runs merge only when exactly one non-clear rectangle spans the prototype width. The merged body preserves that rectangle's Y origin and height, so merging does not introduce an inclusive-height correction. Runs that cannot merge call `CreateSinglePhysicsTile` repeatedly. The merging branch bypasses that helper's extra ladder-cap creation; whether any actual ladder prototype/run meets the merge conditions is not established here. This is a retained source-path question, not a demonstrated missing platform or a proposed unconditional change.

All eight boundary entries remain **partial semantic reviews** because caller contracts, data validity and runtime usage are incomplete. No whole collision subsystem or full machine-code audit completion is claimed.
