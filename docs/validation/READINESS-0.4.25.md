# 0.4.25-dev readiness

OpenAI Codex (LLM), 2026-10-23. Human owns campaign playtesting. No physical-pad
tests. Redmi was initially offline; the later [physical Redmi results](REDMI-0.4.25.md)
are recorded separately. Huawei USB tethering/settings were left unchanged.

## Changes

- Original GPL-3.0 geometric vector icon, with no commercial game artwork.
- Save-tool attribution translated into PL/EN, preserving upstream authors/LLM credit.
- Scrollable save tools: a small emulator with font scale 2.0 reproduced an
  unreachable Back button. Same test passed in both languages after the change.
- Explicit Android-12+ automatic-backup/device-transfer exclusions, consistent
  with the existing opt-out. Manual save export/import remains available.
  [Android's documented behavior](https://developer.android.com/identity/data/autobackup)
  explains why allowBackup alone is insufficient on some devices. OEM transfer
  behavior was not physically tested; do not claim universal enforcement.
- Touch evidence now hashes the installed APK, avoiding attribution to another
  ABI's mutable local build output. Technical exit fixtures record their bounded
  placement count; this is not a game-completion shortcut for natural testing.

Native engine libraries, physics, combat balance and game resources did not change.
Both ARM packages below have identical bytes for all six native shared libraries.

## Exact packages

| Package | SHA-256 |
| --- | --- |
| ARM64 + ARMv7, latest scroll candidate | `6175b1b450ca7f46ede0910a884e3608d104e4a86251822aa6c6b4a57d6ca955` |
| ARM, preceding candidate used for sustained observation | `6ab3b9c47b648278eb80cbfb9192437839441ea9886b4d8f96222ad7512b6286` |
| Separate x86_64 scroll candidate | `eb660e1fcf298d451223d88b0eef5e6073e40bb1e524a559c95e5e541a41e999` |
| Separate x86_64 before scroll | `eb36b82ea69a2954921c3774b96e8db0ad8f15e8af032b3d35a873b054fc9859` |

Version code 37, min API 21, target API 35. ARM ABI/ELF LOAD checks, 16 KB ZIP
alignment and signature verification passed. This remains a debug-signed candidate,
not a production-signed 1.0. Lint: **0 errors, 30 warnings**, no suppressions added.
Compared with the original 33-warning audit, icon, credit text and extraction-rule
warnings were addressed. Existing SDL and remaining warnings are not erased.

## Completed runtime evidence

Huawei Android 10, preceding `6ab3…` candidate: real parser/save/support checks,
PL/EN Activity checks, three small import-recovery fixture modes with actual
process deaths during publication and rollback, and all six touch/jump cases
passed. Before/after configuration, progress and bindings matched byte for byte.
`reports/readiness-huawei-0.4.25/`, `import-recovery-huawei-0.4.25-final/`,
`jump-touch-huawei-0.4.25-final/` contain ignored raw evidence. Those exact-package
results are not silently relabelled as tests of the later scroll APK.

API 21 x86_64, `eb36…`: feature and language checks and actual native/menu/100 ms
jump/exit/score/level-two fixtures passed. The first attempt had pre-existing empty
config/save fixtures; it failed before game coverage. Known prior emulator fixtures
were supplied for retry. This is not SAF/file-picker installation coverage.

API 35 x86_64 with actual **16384-byte pages**, `eb660…`: large-font PL/EN footer
check and native/menu/declared 600 ms jump/exit/score/level-two trial passed
(`compat-api35-16k-0.4.25-r3`). One exit placement was needed in that successful run.
Initial system-service crashes invalidated the earlier language/ABI attempt.
A separate retry jumped successfully but missed the exit pickup and died to an
Officer; its cause remains unconfirmed. Both failures are retained. A later icon
preview encountered a **System UI ANR**, so it is not visual-icon validation.
The emulator is unstable; limited successful cases do not establish general
Android-15 stability or physical ARM 16 KB compatibility. Its size, density and
font scale were restored and that instance was closed.

## Open checks

The [full sustained Huawei observation](SUSTAINED-HUAWEI-0.4.25.md) completed:
approximately 58.99 FPS, minimum batch 57 FPS, single longest interval 31 ms.
It applies to the preceding exact APK listed above, not a universal minimum.
The final scroll x86_64 package also passed API-21 feature/PL/EN/footer checks
and native/menu/100 ms jump/exit/score/next-map fixtures
(`compat-api21-0.4.25-scroll`), with one exit placement. Emulator files were synced
before shutting down that task-owned instance.

Final ARM scroll candidate `6175b1…` on Huawei passed actual PL/EN/footer screens,
parser/save/support checks and all six touch/jump cases
(`jump-touch-huawei-0.4.25-scroll`). The lifecycle trial passed with zero drift
after resume and 178.88 px movement after fresh input (`lifecycle-huawei-0.4.25`).
That uses a virtual SDL controller and does not test physical Bluetooth hardware.
The test companion now registers the existing lifecycle instrumentation directly.

Sustained-test reliability was also checked on this exact ARM candidate: terminating
only the worker's own verified logcat client produced the explicit incomplete-log
failure and no success JSON, with config/save bytes restored. The Windows helper
verifies the ADB client's direct parent PID and command before termination;
it never restarts the shared server. A normal twenty-second observation then
passed with four batches and restoration. Reports:
`perf-reader-abort-huawei-0.4.25` and `perf-reader-positive-huawei-0.4.25`.

APK content inventory found no REZ/MIDI/WAV/MP3/OGG/movie entries. Music assets
are the pinned FreePats instrument bank; original game music still comes from
user-supplied data. Support ZIP non-XML content is the four documented generated
help/credit PNGs. Packaged dependency licence files were present. This is a bounded
inventory check, not a claim that filename matching proves copyright clearance.
Remaining gates include real document-picker/cancellation/large-data workflow,
physical ARM 16 KB coverage, sustained performance acceptance,
active combat/terrain and release signing. Natural campaign testing belongs to
the human. No claim of 1.0 readiness or all-level minimum FPS.

[Active Officer step evidence](ACTIVE-OFFICER-0.4.25.md) adds sixteen mixed
outcomes, four confirmed-after-hit escape cases and a diagnostic parser follow-up.
It does not close complete enemy/terrain coverage or original-game parity.

Final ARM candidate also passed Huawei's explicit ARMv7 native/menu/jump/exit/score/
next-map fixture (`compat-huawei-armv7-0.4.25`); ARM64 was restored afterwards.
Normal level 14 loaded with music, preview and diagnostic modes disabled, without
missing-actor messages (`normal-level14-huawei-0.4.25`). Neither test proves a
natural level clear. Final Huawei config/save hashes match the pre-session bytes.

Redmi's initial offline connection recovered. See [final Android-16 trials](REDMI-0.4.25.md)
for exact package identity, measured touch response and recovery evidence.
