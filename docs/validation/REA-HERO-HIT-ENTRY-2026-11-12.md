# Hero hit entry and category filtering — 2026-11-12

OpenAI Codex (LLM) performed this bounded static review of the supplied EXE identified in the [full audit](REA-FULL-AUDIT.md). The human remains anonymous. No original execution, phone test or gameplay change occurred. Commercial bytes and decoded output remain private.

## Faster acquisition with explicit evidence layers

The registered `CaptainClawHit` entry `0x41e210` is outside the initial Ghidra function inventory. An earlier private Capstone decode of the same target was retained as a hypothesis/reference; it was not relabelled REA instruction Evidence or a complete review. The [subsequent table follow-up](REA-HERO-SOUND-TABLES-2026-11-12.md) resolves the four computed transfers described in this initial checkpoint and extends the entry to 666 decoded starts, with 44 call-contract gaps still open.

REA now supplied an exact complete 2,224-byte read beginning at that entry: `ev_921afbdac125960c66a578c3192625b01c3f588e361cadb538830c97af14f7f3`. The [independent traversal tool](../../tools/rea_decode_region.py) uses installed Capstone 5.0.7 in x86-32 mode. Its bounded worklist decoded **475 instruction starts**, with **four unresolved computed jumps and 26 call-contract gaps**. Calls are not followed or assumed to return with certainty; possible fallthrough is retained with an explicit gap. Unsupported exception/privileged flow, overlaps, undecodable bytes and outside edges stay visible. Traversal completion does not mean semantic or full-function completion.

Four instruction samples at entry and selected branch/return paths match native REA/Ghidra on bytes and instruction lengths. Those samples do not certify every local decoding or control-flow classification. The inventory labels this decoder separately, verifies every decoded instruction against the exact REA byte carrier and counts instruction-address/byte unions rather than summing overlapping sources. The registry preserves the independent-decoder label when joining a partial region review. Neither tool creates a semantic pass from acquisition.

The decoder and evidence-carrier tests use synthetic bytes only. They cover conditional/loop branches, returns, calls, computed/outside transfers, truncation, overlapping starts, budget limits and exception flow; carrier checks reject changed bytes, different targets and incomplete reads. These checks do not execute the game or prove gameplay parity.

The optional host tool requires Python and locally installed Capstone (this run: 5.0.7); it does not download a decoder or execute the target. Supply an existing complete REA `read_bytes` response in the private report directory:

```text
python tools/rea_decode_region.py --report AUDIT_FOLDER --bytes-response READ_BYTES_RESPONSE.json --seed 0x41e210
```

Existing output is preserved rather than silently overwritten. Additional seed/dispatch-table coverage requires an explicit reviewed follow-up. The initial snapshot left four computed transfers unresolved; the linked follow-up records their guards/targets and preserves that snapshot separately.

## Incoming partner and distinct source paths

The entry reads the source object from hero `+0x84`, matching the [manager's target-notification path](REA-OBJECT-PASSES-2026-11-12.md). A null partner returns without processing. The method then branches on the source category at `+0xe8`; some paths heal or collect resources rather than inflict damage. Callback return value 1 must therefore not be interpreted as proof of accepted damage.

For the observed category-4 damage path, source flags and a player-data source-pointer comparison can exit before reaction setup. The path sets auxiliary `+0x130` to **850**, then later clears category bit 4 from hero `+0xec` and obtains the source's numeric damage at `+0x120`; zero is promoted to one.

A different shared damage path sets the same 850 value, but clears both bits `4 | 0x1000000` from hero `+0xec`. It also has source-specific consumption/effect branches. Its category `0x40`/special identifier case takes a separate route. These are not one uniform hit rule or a complete source-category taxonomy.

For the common health-decrement path, a positive damage value is subtracted from hero `+0x128`. Nonpositive resulting health goes to the death helper. **Only after that subtraction** does the surviving path check whether auxiliary state is already `0x1f` and skip repeated reaction setup. Being in the hurt animation is therefore not itself proved to reject all damage. Actual earlier manager masks and source-specific branches determine whether this path can be reached again.

The initial four unresolved computed jumps include random-choice table branches. The linked follow-up joins their targets and a bounded sound-request chain. Effect/audio backend dependencies, death handling, all source categories and exceptional paths remain incomplete. The later [Soldier receiver follow-up](REA-SOLDIER-HIT-ACCEPTANCE-2026-11-12.md) joins category 4 at Soldier initialization; later mutations, Officer mapping and natural diagonal encounters remain uncertified.

## Joining mask restoration

The already acquired hero dispatcher `0x416ee0` provides the matching consumer: at `0x417f71` it reads the **same auxiliary `+0x130`**, decreases it by current timing value `0x535924`, and on expiration clears it and restores hero category-mask bits `4 | 0x1000000`. This is a joined **category-filter countdown**, not merely a name inferred from an isolated constant.

The observed 850 value belongs to that auxiliary record. It is distinct from player-data `+0x114`, written as 1500 during hurt recovery, which earlier notes correctly refused to call damage immunity. The complete outer clock/mode contract remains open; do not equate every 850-unit countdown to a universal wall-clock immunity duration. Different source paths clear different mask bits, even though the restoration adds both.

Hurt update `0x41d3f0` separately carries the owner using selected-platform displacement, advances animation-driven horizontal motion, applies the movement query and returns to standing state `0x18` on its animation-completion condition. It restores incoming/body geometry and several player-state fields. This reinforces that recovery animation, movement, input and category filtering are separate mechanisms. The whole hero dispatcher is still only partially reviewed; these joined sites do not close all its states.

Evidence: dispatcher `ev_e634c4c6867e119530f052cac623bc19c4648ab5c8bfc6e298001fac6f218218`; hurt update `ev_c0a2a48ea93ecf1002a61c241ea005c0648c88084092833e0d0689022118827d`. Native cross-check Evidence references and byte-carrier digest are retained in the private region record.

## Port comparison and disposition

The current port's `ClawControllableComponent` initializes its take-damage duration to **500 ms**, starts `HealthComponent` invulnerability on accepted damage and clears it when that timer ends unless a powerup still requires protection. Boss entry/exit also assign 500. That is a checked port policy, not the same mechanism as category-mask suppression in the EXE.

Changing the port's single timer to 850 would not by itself reproduce the source-specific bit clearing, notification order, hurt-state timing or permitted sources. Preserve the existing behavior until source categories, mask setup/reset paths, actual health acceptance and human stair tests are joined. This report does not supersede existing input-buffer or foot-support fixes, and does not claim a newly reproduced stun-lock bug.

The hero entry region and two inventoried hero functions receive **partial** reviews. Full enemy/boss hit receivers, original runtime behavior, the remaining call contracts and the whole machine-code audit remain open.
