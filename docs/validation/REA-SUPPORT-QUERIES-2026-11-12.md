# Terrain support and settling queries — 2026-11-12

OpenAI Codex (LLM) performed this static review of the exact supplied EXE identified in the [full audit](REA-FULL-AUDIT.md). The human remains anonymous. Findings use retained REA dossiers and checked assembly, not execution of the original game. No production behavior, APK or device changed.

## Support transition query

Routine `0x4cd350` samples the translated horizontal span of owner geometry `+0x134..+0x140` at proposed bottom plus one. Samples use owner stride `+0xf8`; the [known initializer](REA-TILE-PARTITION-2026-11-12.md) sets it to 10, but all later mutations are not joined. Crossing the final X ends the scan; it does not force an unsampled final endpoint.

The support conditions are more specific than merely finding a non-clear cell:

- A below-foot category 1 or 2 supplies support only if the cell one pixel above is neither 1 nor 2. The routine checks a transition into the surface, not arbitrary overlap inside solid geometry.
- Category 3 can supply support at a transition where the below-foot query is 3 and the query one pixel above is not 3, provided the owner is not in mode 6. This explicitly distinguishes standing at a ladder top from the climbing mode. The repeat point query at the same below-foot coordinates is retained as observed behavior.
- If no sampled position satisfies a support condition, owner mode `+0xe4` becomes 4. The returned proposed Y is unchanged; this helper itself does not perform a falling displacement.

Coordinates are clamped for map lookup and sentinel tile entries behave as clear. Valid map/descriptor storage, geometry and stride remain prerequisites. This is not a proof that every partially overlapped edge is sampled or that the original has the same edge stability as the Android port.

Evidence: `ev_67a9371a07c6152c4c322fdc417ca5b7dd3948f524e2073bc94013de3a2732d2`.

## Joined movement caller

`0x4cca90` invokes side collision queries according to X direction and the upper query for a decreasing Y request. It checks requested ladder entry before the support query: one flag selects a probe above the top, another below the bottom; category 3 selects mode 6. Flag `0x10` can request centering using another helper's interval. That interval helper's contract remains incomplete.

An owner flag chooses between terrain support `0x4cd350` and a separate object-support helper. The caller finally writes resolved X/Y into owner `+0x5c/+0x60`. These are joined operations, not a full interpretation of all movement flags and modes.

Assembly passes four stack arguments to `0x4cd350`, whose return consumes 16 bytes; its pseudocode displays only three arguments. The fourth argument's behavioral role is not established. Likewise, settling routine `0x4ce420` consumes eight argument bytes although its pseudocode displays only one parameter. Do not reconstruct ABI contracts from decompiler signatures alone.

Caller evidence: `ev_0934014c1e75c8fe1809312c63b788c7cf50f9d40b1a2f5d21a22dd37f33438b`.

## Downward settling query

`0x4ce420` rejects uninitialized geometry (left bound `INT_MIN`) or a missing map. It probes at owner X and current geometry bottom, then advances downward one pixel at a time until finding category 1, 2 or 3 or reaching map height. Sentinel entries do not stop the search. On success it adjusts owner Y so the geometry bottom is one pixel above the selected support coordinate and returns 1; failure returns 0 without that coordinate write. A support hit at the initial probe can therefore produce a one-pixel upward adjustment.

The hero dispatcher `0x416ee0` directly calls this routine at `0x417076` and `0x417305`; the caller passes the owner and a second stack value. Those call sites are established, but their complete surrounding initialization/state transitions are not reviewed. Do not describe settling as an unconditional per-frame gravity rule or attribute a natural checkpoint snag to it from these calls alone.

Evidence: settling `ev_501feed537758b666d9e66df444695138d836944f03cb093f58f935ec169589f`; hero dossier `ev_e634c4c6867e119530f052cac623bc19c4648ab5c8bfc6e298001fac6f218218`.

## Horizontal clear-span query

`0x4ce620` samples along a horizontal interval in the appropriate direction using a supplied step and explicitly checks the destination after its loop. It returns 0 on category 1 and 1 otherwise; categories 2/3 are not blocking for this particular predicate. This is not a universal rule for terrain collision. Zero/negative step and integer-overflow preconditions are not locally validated; actual caller values remain to be joined before claiming an original hang or safety property.

Evidence: `ev_25ad1002b1aaaf270b147ba57f8b728d1f4bd4c1d9255f6a70791548c45a6b39`.

## Port comparison and caller-search limits

The port's `PhysicsContactListener::HasRealFootSupport` already rejects rising relative motion, uses current fixture bounds and requires a short ray to hit an upward-facing surface. Its persistent support refresh is an existing Android correction; the original surface-transition check does not invalidate or reopen that fix. Sampling integer cells and testing Box2D surface normals have different boundaries and tolerances; equivalence is not established by their shared purpose.

Original ladder-top support is derived from category transitions. In the port, `BaseGameLogic::CreateSinglePhysicsTile` adds a 64×10 ground cap using `ClawLevelUtil::TryGetTopLadderInfo`, which looks up level metadata. Coverage of every real ladder cap and the separate merging branch remains open. Do not replace one approach with the other without scene/data tests. The natural campaign remains the human tester's responsibility.

A private search of 4,005 cached initial dossiers found 21 candidates combining literal `+0x4c` access with selected virtual slots. This is a heuristic, not exhaustive receiver-aware call resolution. Three inspected candidates were unrelated: `0x4d0d30` traverses named resource entries, while `0x4d6680`/`0x4d6aa0` invoke stream-like operations on a supplied receiver. They do not establish calls to the tile boundary family. Raw candidate contexts stay private; unresolved boundary-method callers remain unresolved.

The four terrain/movement functions above have partial reviews. Remaining dependencies include receiver/layout validity, all stride and mode mutations, centering/object-support helpers, complete hero states, actual map placement and runtime acceptance. The full machine-code audit is not complete.
