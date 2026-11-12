# Full executable audit with REA

Started 2026-11-12 by OpenAI Codex (LLM), following an explicit anonymous human request. **In progress.** This is a whole-file audit, not a claim that the earlier enemy investigations covered the whole engine.

## Target and tool identity

- Target: supplied CrazyHook-distributed `CLAW.EXE`, **1,409,024 bytes**.
- SHA-256: `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`.
- Local REA package: `rea-agents` **6.7.0**, from [morluto/rea](https://github.com/morluto/rea).
- Native provider: Ghidra **12.1.4**. The worker retains the actual tool catalog, response Evidence IDs and analysis profile; no client registration change or new tool installation is required.
- Independent header inspection: x86 PE32, image base `0x400000`, entry `0x4a65d9`.

This file is **not certified pristine 1997**. It is not the original source code. Static findings describe these exact bytes and their analysis model; they do not certify original Windows execution, undocumented data editions or Android equivalence.

## Initial inventory and coverage

Fresh REA `list_procedures` Evidence `ev_3e59c9d0b0386051ed287b7c1998e2da027760b2fc8df857a82cb40050f60df6` enumerates **4,405 functions: 4,012 internal and 393 external**, including **44 thunks**. Its full ordered result matches the earlier hash-matched inventory exactly. External import entries do not contain the implementation of Windows or other DLL functions. One dossier request for every internal address is now queued; successful acquisition is counted separately from semantic review.

The complete private ledger has one row per enumerated address. Its initial semantic-review count is **zero migrated rows**, not a claim that no previous investigation exists. Earlier findings must be joined to their exact function, evidence, limitations and port comparison before changing a row's review state. A successful tool call, generated pseudocode, recognized name or batch count cannot mark semantic review complete.

Independent PE header accounting, separate from REA Evidence:

| Section | Virtual address | Virtual bytes | File-backed bytes | Executable | Writable |
| --- | --- | ---: | ---: | --- | --- |
| `.text` | `0x401000` | 1,093,632 | 1,093,632 | Yes | Yes |
| `.rdata` | `0x50c000` | 81,920 | 81,920 | No | No |
| `.data` | `0x520000` | 585,728 | 77,824 | No | Yes |
| `.rsrc` | `0x5af000` | 147,792 | 147,968 | No | Yes |
| `.crazy` | `0x5d4000` | 4,096 | **0** | Yes | Yes |

There are **1,093,632 file-backed executable-section bytes** and **4,096 executable zero-fill bytes**. These are section ranges, not counts of decoded instructions. Function discovery alone does not classify all `.text` bytes: padding, embedded data, undiscovered entries, shared/tail blocks and indirect dispatch need explicit accounting. `.crazy` contains no stored machine-code bytes to decompile from the file. Whether runtime code populates it, and which external modules participate, remains unresolved; zero file size must not be reported as a completed runtime audit.

Instruction-byte coverage is currently **unknown**. Do not publish a semantic-completion percentage from the inventory count.

There are also **3,584 trailing file bytes** after the last file-backed section. Their role is unclassified. They must be accounted for separately rather than silently treating the PE section table as a complete file-content classification.

## First semantic observations: explicitly partial

- **Entry `0x4a65d9`:** the 253-byte detected body sets up an FS-based exception frame, records Windows-version fields, calls initialization helpers, obtains command-line/startup data and hands control to `0x4a3490`. Assembly supplies four application-call arguments; the current pseudocode shows only three. The inferred prototype is therefore insufficient for reconstructing the call contract. Exception, helper and exit semantics still need joined review. Evidence: `ev_64e6f5b715e7d90c568b9ca02d8471af1fe5c33264cd6df2a34f018916ea269e`.
- **Registration `0x401000`:** the dossier has 208 referenced strings and 212 unresolved calls, with repeated virtual registration-slot calls. Its final branch transfers to `0x50b4b7`. That extension belongs in the registration analysis; stopping at the detected function boundary would omit it. Names alone do not establish which callbacks stock maps instantiate. Evidence: `ev_a0162601b97d4058ade6152e23adcfe39066a5d253a50d8378183689aaa58f4b`.
- **Detected fragment `0x40223e`:** pseudocode looks empty, but the two decoded bytes restore a register from the stack and return. The joined extension described below now resolves this bounded continuation. It is not a separate no-op engine feature. Evidence: `ev_25efb242ed61baabb0ec3a34f1bde0c0f5b23bba7ee5732c73d411898cb35002`.

Port boundary: the Android build enters through [`native/android_main.cpp`](../../native/android_main.cpp), Java/SDL lifecycle and `RunGameEngine`; it intentionally replaces Windows CRT/WinMain startup. Actor construction uses OpenClaw's XML/component factory. Neither observation establishes one-to-one registration coverage or full initialization/cleanup equivalence. Startup and registration remain **partial**. The two-byte continuation is reviewed only within its joined stack contract; no game behavior was changed from these findings.

### Joined registration hook and external dependency

The extension `0x50b4b7` saves/restores EDX and uses a one-time flag set before loading the hook. It loads `CrazyHook` through `LoadLibraryA`, resolves the export named `CrazyHook` through `GetProcAddress`, and invokes the resolved pointer with the registration object from owner offset `+0x14`. The dynamic implementation is outside this EXE; neither function names nor this invocation establish what it registers or patches. Extension Evidence: `ev_dc52d38738981680366cf86f7dcee511973b54d0e9c3678a0d39e6e8a47b8288`.

The local load/symbol guards at `0x50b42d` and `0x50b432` share the null-result check. A null load or symbol result displays its context message and exits with code **666**; the non-null path returns the value. The load-entry fragment additionally stores the result before falling into the shared check. Provider boundaries and generated pseudocode do not imply independent normal calling conventions for these fragments. Evidence: `ev_b96328eb030ccfcb67d10948646e256659c261c76bc3fcc4b14ff0b2c580135c`, `ev_9d52454ef24bee59177b9f07d13e74da4f47734386af4918ffac1f4384407a27`.

The registration prologue saved ESI. After the extension restores its own EDX save, the instruction at `0x50b500` **jumps** to `0x40223e`, which restores ESI and returns using the existing stack. ReferenceManager classifies that transfer as a logical call, but assembly shows a jump: it does not push a new return address. This closes the tiny continuation's observed contract, not the whole registry. The application-entry routine at `0x4a3490` also ends with 16-byte argument cleanup, supporting the four-argument startup contract despite the three-parameter pseudocode. Evidence: `ev_cd8ba04d4bbdeb6cba9833b605fadbd3e15e1dc9382b4e237e72e60768ab77b0`.

A supplied `CrazyHook.dll` is present locally: **141,312 bytes**, SHA-256 `8f16b35bf105c8d8799db6df543dcecaca801153a3fcef7da261d74573d31318`. This is filesystem identity evidence, not an REA semantic audit of that DLL or evidence it executed. Its implementation remains a dependency; the current worker targets only the agreed EXE. The hook is stored in file-backed `.text`; its existence does not prove how the separate zero-fill `.crazy` section is used.

The Android port does not load this Windows DLL. Compare required gameplay behaviors individually; do not copy the loader, claim original callback parity or infer that this hook's platform dependency is a missing Android feature.

## Required work and completion contract

1. **Inventory and boundaries:** revalidate the target hash, preserve the provider profile, reconcile the full function list, imports, entry point, sections, function bodies and non-function executable ranges. Track overlaps and unresolved regions rather than silently excluding them.
2. **Evidence acquisition:** obtain bounded native dossiers for every internal function, including assembly, pseudocode where available, blocks, references, strings, direct/indirect calls and provider limitations. Keep failures and unavailable facets as explicit gaps. Import earlier exact-target evidence instead of repeatedly collecting it.
3. **Semantic review:** explain every function's inputs, state, outputs, side effects, conditions, timers, error/exit paths and relevant dependencies. Resolve dispatch tables, virtual calls and data layouts by evidence. Separate observations, inference and unknowns. Library/compiler helpers still require classification and boundary review; they are not silently removed from scope.
4. **Port comparison:** join reviewed behavior to the actual OpenClaw/adaptation path, classify match, discrepancy, intentional difference, not applicable or unresolved, and state player impact. Do not change game balance or collision geometry from an unjoined constant or speculative field name.
5. **Cross-system checks:** review startup/shutdown, resources, timing, rendering, input, movement, collision, damage/recovery, enemies, bosses, level objects, checkpoints/saves, menus, audio, presentation and failure handling. Individual-function summaries do not prove the complete call/state interaction.
6. **Coverage closure:** reconcile every function and executable range with the ledger, every unresolved indirect target and significant data dependency with a recorded result or explicit remaining dependency, and every port discrepancy with evidence and disposition. Do not declare the full audit complete while required behavior remains unreviewed or unsupported. Dynamic observations, if later used, retain their own exact configuration and limits.

The human owns natural campaign testing. This audit does not allocate phones, activate the deferred controller matrix, execute the original target automatically or claim a campaign clear.

## Private evidence and reproducibility

Raw responses and ledgers stay under ignored `reports/rea-full-audit-2026-11-12/`; commercial bytes, reconstructed pseudocode, raw assembly, resource payloads and personal paths must not be committed. Public findings are independent English explanations with exact identities, addresses, Evidence references and limitations. Preserve upstream authorship and explicit LLM adaptation disclosure.

- [`rea_audit_worker.py`](../../tools/rea_audit_worker.py) provides a serialized, allowlisted, task-local REA stdio mailbox. It reuses existing runtimes, writes responses atomically and does not replay an uncertain timed-out request automatically. A lock file alone is not proof of a live worker: inspect the actual process/session before recovery.
- [`rea_audit_inventory.py`](../../tools/rea_audit_inventory.py) checks the REA subject hash, creates the complete function ledger and independently parses PE section headers. Separate `reviews.json` entries require findings, evidence, limitations and a port comparison before recording a semantic status beyond unreviewed.
- [`rea_audit_queue.py`](../../tools/rea_audit_queue.py) queues missing internal-function dossiers from the exact inventory without overwriting previous attempts. All 4,012 internal addresses, including the entry dossier, are represented. External imports remain separate boundary-review obligations.

The private function-body map unions acquired Ghidra body ranges and records every remaining executable file range. This is **acquired body coverage**, not decoded-instruction, semantic or runtime coverage. While acquisition is incomplete, a gap can be an unacquired known function; it must not automatically be labelled undiscovered code.

The previously started debug44 importer-language work remains separate and unfinished; no installation, runtime success or publication is implied by this audit. Preserve its working-tree changes.

### Retained acquisition failures

The first collector stopped after a local Windows permission failure while replacing progress metadata; its last completed REA response was retained. A first resume incorrectly reused the saved open result without reopening the new ephemeral session, producing **576 explicit `target_unavailable` responses**. They are retained under private `failed-session-2/`, are not dossiers or reviewed functions, and were requeued only after verifying that no target analysis ran. The worker now reopens the target for each session, stops on any tool error and retries brief local replacement failures without repeating the REA operation. These are collector defects, not game crashes or failed semantic checks.

Acquisition first reached **1,313 complete function dossiers** before `0x4735d0` exceeded REA's approximately 10 MB MCP response budget. REA reported completed analysis and retained Evidence `ev_d39e633cd82ff4472df45a985965c713429848a3df3829b742a0802dc8393099`; the first error-stop implementation closed that session before exporting the retained record. The one explicitly queued reacquisition then **successfully exported the complete retained Evidence** through REA's `export_evidence_bundle`. Its original Evidence ID, target SHA-256 and procedure address match; the 7,105-byte function body has 1,661 decoded instructions and 25,618 pseudocode characters. The complete extracted record is 10,024,575 bytes when pretty-printed privately. The two transport-error receipts remain retained and are classified as recovered by that exact Evidence, not as two additional dossiers. This verifies transport recovery, not semantic understanding of the large function.

At that checkpoint, the acquired function-body union covers **341,861 executable-section bytes**; this is acquisition metadata, not semantic acceptance. One joined two-byte continuation is reviewed and three broader startup/registration entries remain partial. The inventory rejects different-target and duplicate-entry negative fixtures. Live totals may subsequently exceed this dated checkpoint; consult the private ledger and preserve exact Evidence identity.

### Subsequent acquisition and first audio comparison

The next saved checkpoint contains **3,240 complete dossiers**, **754,669 acquired function-body executable bytes**, **18 partial semantic reviews** and the single reviewed continuation. The [ambient-audio comparison](REA-AMBIENT-AUDIO-2026-11-12.md) joins named callbacks, constructors, gain, activation, spatial update and lower-level transition helpers. Fifteen function-specific reviews were recorded as partial; original table units, backend pan and several lifecycle joins remain unresolved. No phone or APK changed.

Ghidra failed decompilation at **`0x4f5a42`** with its reported low-level overlapping-input-varnodes error. That error is retained and does not count as a dossier. Separate body/instruction/reference requests were queued; the unchanged failing decompilation was not repeated. The worker now distinguishes this specific per-function decompiler limitation from session/transport failure so unrelated functions can continue while the gap stays visible. Alternate evidence is not silently relabelled a complete decompiler dossier.

## Current next action

The [hero sound-table follow-up](REA-HERO-SOUND-TABLES-2026-11-12.md) resolves four guarded indexed transfers and adds 191 instruction starts plus seven partial helper reviews. Verified resource keys and lookup/playback gates explain the added request branches; remaining backend, clock, actor-category and runtime dependencies stay open. The initial traversal snapshot is retained separately.

The [hero-hit entry follow-up](REA-HERO-HIT-ENTRY-2026-11-12.md) joins source-specific category-mask suppression, its auxiliary 850-unit countdown and restoration sites, with a partial hurt-update comparison. A new independent Capstone traversal consumes exact REA byte Evidence and labels its decoder separately; byte provenance is checked before adding coverage. The initial four computed jumps are joined in the subsequent table follow-up; 44 call contracts remain open after its expanded traversal. A single port timer change would not reproduce the original category filtering.

The [object-pass follow-up](REA-OBJECT-PASSES-2026-11-12.md) joins the default manager update/contact targets, per-slice countdown gates, deferred removal and directional hit geometry/notification order. Thirteen more inventoried functions and two supplemental regions have partial reviews. The new regions add 333 decoded instruction starts; three direct helper contracts are joined while other call/lifetime/actor-acceptance gaps remain explicit.

The [platform-update follow-up](REA-PLATFORM-UPDATES-2026-11-12.md) joins StandardElevator displacement writes, their passenger consumer, timing publication and an 18-unit slice loop, plus selected-object identity restoration. Nine further function reviews remain partial; ordinary removal, outer clock/callback scheduling and exact port subtype conversion are still open. Registry regeneration now preserves explicit review status instead of resetting it.

The [ladder/carrier follow-up](REA-LADDER-CARRIERS-2026-11-12.md) joins six further function bodies: full-tile centering, upward ladder exit scanning, mode-6 movement, object landing acquisition/predicate and retention. It refines the earlier falling-movement review. Carrier lifetime/updates, complete movement flag setup and natural scene parity remain open.

The [support/settling follow-up](REA-SUPPORT-QUERIES-2026-11-12.md) joins four more movement/terrain functions, including ladder-top transitions and two hero calls to downward settling. Existing Android foot-support fixes remain in place. A cached-evidence caller search retains unresolved candidates and rejects three misleading offset/slot matches; it does not close the boundary-family caller gap.

The [tile-query and partition follow-up](REA-TILE-PARTITION-2026-11-12.md) joins three previously unowned query methods, their factory/initialization paths and default terrain strides. A host comparison using the actual port converter records discrepancies in four of seven synthetic tile descriptions, with three passing controls. A read-only survey of the supplied 14 local levels finds 9,336 descriptors and no mask descriptors. This is a converter-level finding; natural scene impact and a production correction remain open. The saved ledger now has 99 partial and two reviewed initial-inventory functions, plus twenty-three decoded supplemental regions with 1,496 instruction starts (830 from REA/Ghidra and 666 independently decoded from REA byte Evidence); these are distinct coverage measures, not whole-program completion. The [double-tile boundary-family follow-up](REA-TILE-BOUNDARIES-2026-11-12.md) joins all eight directional entries at a bounded method-contract level; their callers remain incomplete.

The [registration coverage follow-up](REA-REGISTRY-COVERAGE-2026-11-12.md) now accounts for all 212 literal registration rows and 209 distinct callback addresses. It identifies 163 callback addresses outside acquired bodies, verifies 162 decoded/unowned entries, retains one unavailable decode and records a bounded partial Bullet-wrapper review. These new seeds do not automatically become complete functions or semantic passes. Four missing defined names were recovered from bounded REA reads.

The [projectile method-chain follow-up](REA-PROJECTILE-CHAIN-2026-11-12.md) joins the constructor-installed vtable, two further unowned methods, image-derived geometry, falling-state dispatch and shared motion boundaries. Fifteen more functions received partial reviews. Joining the actual initial allocation handler narrows the earlier null-result concern to a configuration-dependent candidate; it is not a proved ordinary out-of-memory crash. Supplemental decoded regions are now counted separately from inventoried function bodies.

The [terrain/contact follow-up](REA-TERRAIN-CONTACTS-2026-11-12.md) joins another 15 function reviews and three additional forwarding regions. It distinguishes movement-rectangle sampling from hit/attack/bump dispatch, records direction-dependent terrain modes and preserves receiver, stride and lifetime uncertainties. These findings do not close natural snag/combat reports or certify original repeated-hit policy.

### Complete acquisition of the initial function inventory

All initial **4,012 internal entries** now have body evidence: **4,011 complete REA dossier responses**, plus the instruction/body/reference evidence for the single decompiler failure at `0x4f5a42`. That alternate evidence describes a 467-byte body; it is not a recovered pseudocode result. The raw error remains visible. Its instruction Evidence is `ev_e056ddc361d87956c916cf1ff6d6dd036dc83124624bbb52f4602d3c5c777246`.

The acquired body union covers **820,587** of the **1,093,632** file-backed executable-section bytes. The remaining **273,045 bytes form 2,981 ranges outside those bodies**. This is not a semantic-completion ratio. No known internal entry remains unacquired, but the initial function inventory is demonstrably not the entire code inventory.

REA confirms a decoded instruction at **`0x410510`** with **no owning procedure**, and a data reference from registration at `0x4010a5`. The registry associates that callback with Bullet; its executable bytes lie inside an uncovered range. Evidence: `ev_09afe986e16892b74479cdf999ffd4624473a5259a707d77c7b81ca4692e5a67`. Another decoded instruction at **`0x4267e0`** has no owning procedure and an incoming data reference. Evidence: `ev_15b5debab7223362f46f3358991d2052f1ab24c27677e2cc1f4a7f048f3f579a`. These are decoded-code observations, not newly established full function boundaries.

The largest outside-body range is **11,223 bytes at `0x508856..0x50b42c`**. A complete bounded REA read returned that range, including mixed bytes; it must not be dismissed wholesale as alignment padding. Evidence: `ev_d3003b8ed0003341f2ec0265f80ee50687681b3b7cd6e127ee4a6b4ca2763c4b`. Raw bytes remain private. Meaning, control-flow ownership and possible exception/cleanup continuations require review.

The [ambient-audio comparison](REA-AMBIENT-AUDIO-2026-11-12.md) records the first 15 further partial function reviews and specific port differences. No production change, campaign result or additional device coverage is claimed.

Expand the coverage model to decoded code outside recognized functions, join callback/control-flow and data boundaries, and continue semantic/data/port reviews beyond the initial startup, registration and ambient-audio paths. Inspect the known decompiler gap using its actual instructions and migrate earlier focused findings only after checking their exact evidence and remaining boundaries. The earlier [behavior ledger](../ORIGINAL-BEHAVIOR-LEDGER.md) remains useful, but is not a whole-file coverage ledger. Full audit completion remains unproved.
