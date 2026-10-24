# Twenty-minute Redmi observation

OpenAI Codex (LLM), 2026-10-22. Physical Redmi Note 8, Android 16/API 36, ARM64, 4096-byte pages. Exact APK 0.4.21-dev SHA-256 `cfc586439527bb6e4f063d4d6b7b526aa8fa64e2c9f44d6fccc7e7889c7672cf`. Report `redmi-sustained-0.4.21`. No update was installed during observation.

## Method

Level nine, controlled teleport to (11027,5500), initial settled position (11027,5554.6), logical viewport 1040x480 on a 2340x1080 surface. Protected hero, no movement/attack input or ammunition changes. Music/SFX enabled, 22050 Hz, chunk size 1024. Quiet diagnostics removes verbose actor traces, preview badge and further mailbox polling; periodic frame/phase/physics counters remain. Ten-second warmup, then 1200.148 seconds of observation. Original config/progress restored afterwards; continuous log retained. Final position is explicitly unqueried because quiet mode disables commands. The last screenshot remains available.

## Measurements

Exclude the first 300-frame batch consistently with earlier comparisons; the following 239 batches are equal frame counts, so harmonic mean is used.

| Measurement | Result |
| --- | --- |
| Harmonic FPS | 59.998 |
| First 30 batches | 59.987 FPS |
| Last 30 batches | 60.000 FPS |
| Batch FPS range | 59.6–60.0 |
| Worst logged frame | 65 ms |
| Maximum batch p95 | 18 ms |
| Battery temperature before/after | 28.0 / 28.9 C |
| Post-observation app PSS | 233238 KiB, about 227.8 MiB |

The process remained alive and no fatal markers were observed. No sustained FPS decline appeared in this single scene. The 65 ms frame is retained; this is not perfectly even frame pacing. Battery readings are not CPU temperature; one post-run PSS reading is not a peak, memory trend or leak test. This stationary protected fixture does not establish natural gameplay, all-map 60 FPS, traversal-related loading or stability under every background load. Huawei uses a different viewport and hardware, so this is not an A/B hardware comparison or a resolution of its roughly 58–59 FPS dense-scene result. The 0.4.22 import-only update is a different APK and does not automatically inherit these measured numbers.
