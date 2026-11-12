# Ladder centering, exit and object support — 2026-11-12

OpenAI Codex (LLM) performed this static follow-up to the [support review](REA-SUPPORT-QUERIES-2026-11-12.md), on the exact supplied EXE identified in the [full audit](REA-FULL-AUDIT.md). The human remains anonymous. No original execution, phone operation, APK installation or gameplay change occurred. Raw REA instructions and pseudocode remain private.

## Ladder centering interval

`0x4cdd50` clamps the requested X/Y to map bounds and looks up the containing tile. Sentinel entries return 0 without changing either output. For a valid entry it returns the tile's world X origin and that origin plus the configured **tile width minus one**, then returns 1. It does not inspect the double-tile inner rectangle or search for the narrow category-3 region.

The already joined movement callers `0x4cca90` and `0x4ccc60` first require their ladder probe to report category 3; movement flag `0x10` then enables averaging this interval and updating X. Their integer midpoint truncates toward zero. This closes the previously unknown centering interval; complete entry-flag setup remains open.

The port's `PhysicsComponent::AttachToLadder` instead centers on the overlapping ladder fixture AABB. Equal tile origins/widths would still give a one-pixel difference for a positive 64-pixel interval: the inclusive integer midpoint of 0..63 is 31, while an edge interval 0..64 has center 32. This is an arithmetic illustration, not a demonstrated misalignment of an installed ladder. Inner sensor offsets and actor coordinate conventions also matter. Do not shift every ladder from this example.

Evidence: `ev_4a8badaf06d01f15919252eb7cef35860a32dc2cd8dfbd4324ff70acbd716719`.

## Leaving the top of a ladder

`0x4cda30` scans upward at a fixed X, beginning one pixel above a supplied start Y and including a supplied lower numeric limit. It stops at the first sentinel or non-category-3 pixel, writes that sampled Y plus one, and returns 1. A reversed/empty interval or an entirely category-3 interval returns 0 without output. Clamping applies to lookup coordinates; the recorded output follows the scan coordinate. Map, output-pointer and arithmetic validity remain preconditions.

The normal mode-dispatch path of `0x4cc920` sends mode 6 to `0x4ccf20`; a separate engine-flag override is outside this join. For decreasing or unchanged Y, that routine first applies the upper collision query. If neither the probe above the head nor below the feet is category 3, it invokes the upward scan over the old-to-resolved-bottom interval. Success with a returned boundary numerically greater than the resolved owner Y selects mode 1 and places the geometry bottom one pixel above that boundary. Side collision is applied afterward. For increasing Y it uses the lower query, retaining mode 1 when that query lands; otherwise, absence of category 3 at both probes selects mode 4.

The port already has `CompleteLadderAscent`, `HasClimbSpaceAbove` and a real-cap query in `PhysicsComponent.cpp`, including the leafy-ladder mounting correction. These use fixture/cap coordinates and bounded tolerances rather than the original integer scan. The observed original exit rule supports keeping the explicit mounting transition; it does not prove parity of every ladder segment or invalidate the existing correction.

Evidence: scan `ev_c7a2c9f0e93e5e665052382a4a6539c5ea1c12093334b8a92a2a2f8ddced12da`; mode-6 routine `ev_68eb129b156c5e8ad770cd39c8ae5e15030079693e1dfa98186a089562be8cc5`; dispatcher `ev_d758217efbd173342c56ee38bdee1c0003089615ec547d92c269a076cd71a6f8`.

## Acquiring object support

`0x4cdb30` runs only when movement flag 8 is enabled. It traverses an engine-owned linked list and tries entries whose field `+0xe8` equals **exactly `0x80`**, not merely entries containing that bit. On the first successful landing predicate, it stores the selected object at owner `+0x98`, sets mode 1 and owner flag `+8` bit `0x10`, then returns 1. No accepted candidate returns 0. List order therefore controls the first accepted match; complete list/lifetime ownership remains unjoined.

Predicate `0x4cdbc0` checks owner geometry at `+0x134..+0x140` against candidate geometry at `+0x144..+0x14c`, translated by their positions. It rejects left-bound sentinels of **-1**, which must not silently be equated to the separate `INT_MIN` initializer sentinel. It also rejects an upward proposed owner move.

Let `S` be candidate top, `oldBottom`/`newBottom` the owner bottoms, and `d = min(candidate[+0x178],0)`. It requires `oldBottom <= S-d` and inclusive horizontal overlap. If old and new bottom are equal, success requires `newBottom == S-1`; otherwise it requires `newBottom >= S-1`. Success writes resolved owner Y as `S - ownerBottomOffset - 1`; failure leaves that output untouched. The meaning and update timing of candidate `+0x178` remain unknown: it is not labelled velocity or frame delta from this consumer alone.

`0x4ccc60` is the joined caller: it tries object landing before the lower terrain query, uses the resolved Y on success and skips that terrain query when mode is already 1. Its subsequent ladder-entry and side-recheck branches remain separately recorded; this is not an automatic statement that object support always wins in every movement mode.

Evidence: acquisition `ev_8db1bc1537de8018efccb2aa794faeac56bce878701b765864905967bc6d4a1b`; predicate `ev_d70051d691166f4af9adf6228915b55d0468c27a7de5947bea18f1e7a5321fef`; caller `ev_bff5340419dcf611bc2f27a21a4131e7101796b1433890b41db60ea31ada1023`.

## Retaining object support

`0x4cdc90`, called by `0x4cca90`, requires a non-null previously selected object, movement flag 8, exact type/category field `0x80`, left geometry bounds unequal to -1 and inclusive horizontal overlap. It returns true only when the proposed owner bottom equals candidate top minus one. It does not itself move either object, clear the selected pointer, or validate its lifetime.

The landing predicate consumes six 32-bit arguments although its pseudocode exposes five; the acquisition caller visibly supplies six. The retention predicate consumes five. Preserve these assembly contracts when reconstructing interfaces; do not drop an apparently unused argument based on pseudocode alone.

The port uses one-way-ground contacts, moving-platform contact state and contact geometry/velocity tests in `PhysicsContactListener.cpp`, together with platform handling in `PhysicsComponent.cpp`. These are different support representations. Original carrier motion updates, pointer clearing/removal, all movement flags, actual dimensions and corresponding port transitions remain to be joined before proposing a gameplay change.

Evidence: `ev_f10c84175cbee14d58bf37c5319f317f77a9bb796d59be3e5e3c4461b38c13c8`.

## Coverage disposition

Six further initial-inventory functions receive partial reviews; the earlier `0x4ccc60` review gains the joined landing relationship. Full natural ladder/platform acceptance remains the human tester's task. No reported snag, wall-jump, carrier lifetime or entire collision subsystem is declared resolved by these static contracts.
