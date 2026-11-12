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

Acquisition then reached **1,313 complete function dossiers** before `0x4735d0` exceeded REA's approximately 10 MB MCP response budget. REA reported completed analysis and retained Evidence `ev_d39e633cd82ff4472df45a985965c713429848a3df3829b742a0802dc8393099`; the first error-stop implementation closed that session before exporting the retained record. The saved transport error is not counted as a complete dossier. Recovery is now explicitly queued once, with a worker path that calls REA's `export_evidence_bundle` before closing, then extracts the exact complete retained Evidence. This avoids truncated pseudocode or a false successful-dossier count. Export recovery still needs its own successful result before it is reported as verified.

At that checkpoint, the acquired function-body union covers **341,861 executable-section bytes**; this is acquisition metadata, not semantic acceptance. One joined two-byte continuation is reviewed and three broader startup/registration entries remain partial. The inventory rejects different-target and duplicate-entry negative fixtures. Live totals may subsequently exceed this dated checkpoint; consult the private ledger and preserve exact Evidence identity.

## Current next action

Continue the live dossier acquisition, then join startup and the registration extension, examine executable-range gaps and migrate earlier focused findings only after checking their exact evidence and remaining boundaries. The earlier [behavior ledger](../ORIGINAL-BEHAVIOR-LEDGER.md) remains useful, but is not a whole-file coverage ledger.
