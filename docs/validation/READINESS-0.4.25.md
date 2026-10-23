# 0.4.25-dev readiness / Przygotowanie wydania

OpenAI Codex (LLM), 2026-10-23. Human owns campaign playtesting. No physical-pad
tests. Redmi permission was granted, but ADB remained offline; no Redmi result
is claimed. Huawei USB tethering/settings were left unchanged.

## Changes / Zmiany

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

## Open checks / Otwarte próby

The sustained Huawei observation and final scroll-APK Huawei/API-21 follow-up
are recorded separately when complete. Do not infer their outcome from this file.
Remaining gates include real document-picker/cancellation/large-data workflow,
Redmi once online, physical ARM 16 KB coverage, sustained performance acceptance,
active combat/terrain and release signing. Natural campaign testing belongs to
the human. No claim of 1.0 readiness or all-level minimum FPS.

Po polsku: poprawiono brak dostępu do przycisku Wstecz przy dużej czcionce,
dodano własną ikonę i polski opis autorstwa narzędzi zapisów oraz jawne reguły
kopii danych dla nowych Androidów. Próby Huawei, Androida 5 i ograniczony test
16 KB mają przypisane dokładne APK. Błędy emulatora i nieudane próby pozostają
udokumentowane; nie udajemy, że wszystkie warunki wydania są spełnione.
