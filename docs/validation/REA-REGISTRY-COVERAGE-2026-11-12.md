# Registered callbacks outside the initial function inventory

OpenAI Codex (LLM), 2026-11-12. Independent findings from REA 6.7.0 / Ghidra 12.1.4, supplied CrazyHook-distributed `CLAW.EXE`, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. Part of the [whole-file audit](REA-FULL-AUDIT.md). No target execution, phone test, production change or original-source recovery is claimed.

## Inventory expansion

The assembly of registration `0x401000` contains **212 calls through virtual slot `+0x1c`**. At every call, the inspected argument sequence supplies literal flags, a name address and a callback address. These observations produce **212 registration rows and 209 distinct callback addresses**. Repeated callback addresses are retained as aliases rather than counted as different implementations. Registry Evidence: `ev_a0162601b97d4058ade6152e23adcfe39066a5d253a50d8378183689aaa58f4b`.

Ghidra's defined-string inventory supplied 208 of those names. Bounded complete REA reads recovered the other four, including NUL termination:

| Name | Name address | Evidence ID |
| --- | --- | --- |
| Fish | `0x520b60` | `ev_9c7877cf0d929b38040c2adf0b10c76cf1fc7058e460a74814c4a02b270c17c7` |
| Omar | `0x520c7c` | `ev_d6c171eb1174f4f7d63bdc460f3625b8d247bad821cde2ff903bea4e915fc182` |
| Rat | `0x520d5c` | `ev_c8134fa0fb3e7bce162de05734b8a7b2396efde9d351123fd80de6fd14ee199a` |
| Raux | `0x520d60` | `ev_9b0b784d0842c1faf16877395f69cddfd6435d86554a8e76a25c9b6efebf297f` |

**163 distinct callback addresses lie outside the initially acquired function bodies and are not inventoried function entries.** Direct REA instruction inspection returned decoded instructions with no owning procedure at **162** addresses. The remaining address, **WeaponFrame at `0x494550`**, has a registration reference but an undecodable instruction result. This means unavailable decoding in the current provider model, not proof that the callback is invalid or unused. Its Evidence is `ev_cb4858b50b44604b560f6fad253b47bde1bb2e4d653f8e9a14e941977b07b11f`.

These are additional code seeds, not 163 newly proved independent function boundaries. Do not add them mechanically to the 4,012-function denominator or mark their bodies reviewed. Registration also does not prove that a particular stock map instantiates every object.

## Bullet: bounded instruction review

The registered Bullet callback at **`0x410510`** has no owning procedure in the provider model, despite decoded code and its registration reference. A conservative REA instruction traversal observed **96 instructions** within the selected uncovered range. It follows observed direct branches, retains conditional fallthrough, records calls without traversing their callees and stops at returns. Call returnability is explicitly unreviewed; this is not an original runtime trace or an automatically recovered function boundary.

The computed jump at `0x41053c` initially left a coverage gap. Assembly establishes the bounded incoming code range, zeroes the lookup register, loads a byte from one table and indexes a five-entry destination table. A complete 101-byte REA read joins both tables: Evidence `ev_038fce8a15398bd910a32b72f4e55a4f9a16c09aa6cfca31a2a97fb3514ba576`.

For input codes 0..80, the recovered table selects separate paths for **0, 29, 30 and 80**, with the remaining codes selecting the shared path. Other inspected branches distinguish 81, 82, 83 and 1000. These are observed numeric dispatch values; this report does not assign unproved event names to them.

The code-0 path requests a **376-byte object**, invokes constructor `0x411650` on a nonzero result, calls a virtual slot and stores the resulting instance. Other paths invoke further virtual slots or forward through `0x4def40`. Constructor, virtual-method identities, message lifecycle and the forwarded routine remain unjoined. Eleven call sites retain explicit contract/returnability gaps after resolving the table.

The callback also contains an explicit zero-allocation-result branch that reaches a virtual access through zero. Whether the allocator can actually return zero under this installation's configuration remains unestablished. This is a **static failure-path candidate**, not an observed crash, a new Android defect or an instruction to reproduce that behavior in the port.

The wrapper remains a **partial semantic review**. It does not determine projectile speed, damage, hit rectangles, re-hit policy or lifetime. The port's `ActorFactory.cpp` and `AIComponents/ProjectileAIComponent.cpp` use XML component construction, physics and events; architectural correspondence is not behavioral equivalence.

## Reproducibility and limits

- [`rea_registry_seeds.py`](../../tools/rea_registry_seeds.py) checks target identity, extracts literal registration sequences, preserves unsupported patterns and compares callback addresses against the acquired body ledger. Missing defined strings do not erase otherwise observed callbacks. Raw names and instruction results remain private.
- [`rea_code_region.py`](../../tools/rea_code_region.py) saves a resumable bounded instruction worklist. A drained worklist does not imply semantic completion: computed jumps, undecodable bytes, calls and edges outside the selected range retain explicit gaps. The table join is stored separately with its REA Evidence and bounding instructions.
- Nine [synthetic coverage-contract checks](../../tests/test_rea_code_coverage.py) passed: branch/fallthrough distinction, returns, unknown/computed flows, call-returnability limits and missing/mismatched registration names. They validate collector behavior, not game mechanics.

Private evidence: `registry-callback-ledger.json`, `registry-callback-summary.json`, `registry-seed-instruction-checks.json`, `bullet-dispatch-join.json` and `region-0x410510.json` under the ignored audit directory. No commercial bytes or generated pseudocode are committed. Continue with callback bodies, shared dispatch/data dependencies and their port comparisons; whole-code audit completion remains unproved.
