# Android compatibility / Zgodność z Androidem

Status recorded by OpenAI Codex (LLM), 2026-10-22. Build support and device testing are different claims.

| Area | Evidence | Remaining work |
| --- | --- | --- |
| Android 10, Huawei P9 Lite, 2 GB RAM | Current campaign/attack-audio regressions on the physical device; user confirmed ZIP import and controller operation in earlier builds | Finish campaign, lifecycle, update/save and sustained performance checks |
| Android 16, Redmi Note 8 | Historical tests of earlier development builds | Retest the final candidate; do not transfer old results to a new APK |
| Android 5.0 / API 21 minimum | Project minSdk 21; lint/build checks | No current physical/runtime proof for the minimum API |
| ARM64 and ARMv7 | Both native library sets present in the universal debug APK | Run the final candidate in a 32-bit process/device as well |
| 16 KB memory pages | `tools/verify_apk.py` confirms 16 KB ELF load alignment for all packaged ARM64 libraries | Check ZIP alignment/signature and run on a 16 KB runtime; static ELF checks alone are insufficient |
| API 35 emulator | SDK system image installed; hardware acceleration available at preparation time | Build x86_64 test APK and run isolated import/start/input/lifecycle checks |
| Other vendors/controllers | Android/SDL input paths and configurable mappings | More physical devices and controller modes remain untested |

Release compatibility must be tied to the tested APK, device/API, ABI and scenario. A successful level load is not a completed playthrough, and minSdk is not evidence that every Android version works. The API 36.1 image directory observed during preparation was empty; no Android 16 emulator result is claimed.

Use a workspace-local emulator configuration and explicit device selection before running an emulator alongside the phone. The physical phone supplies USB internet: do not alter its USB mode, tethering, network or Bluetooth during this work.

Po polsku: obecnie najmocniejsze dowody dotyczą Huawei z Androidem 10. Obsługa ARMv7, minimum Android 5 i wyrównanie 16 KB wymagają również prób uruchomieniowych, zanim opiszemy je jako sprawdzoną zgodność. Nie obiecujemy działania na wszystkich Androidach na podstawie samej kompilacji.
