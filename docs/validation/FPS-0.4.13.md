# Dense level-nine baseline

OpenAI Codex (LLM), Huawei P9 Lite / Android 10 / 2 GB RAM, 2026-10-22. No claim of a new performance improvement or steady 60 FPS.

`dense-9-0.4.13` observed the existing map scene at (11027,5500) for 60 seconds. Setup teleport and player protection are explicit fixtures; no attacks, movement or ammo edits were used. The player settled at (11027,5554.6). Music/effects remained enabled at the script's declared 22050 Hz profile. Original config/saves were restored, and USB internet was untouched.

Actual installed ARM APK SHA-256: `f0df9125bb970fc735a39c306ae52366a8240d8ff20736af78790820e5e432e2`. Twelve frame batches: first 56.1 FPS / p95 22 ms / max 37 ms, then 57.5–59.7 FPS / p95 19–20 ms / maxima 21–27 ms. Surface at startup 1800x1020, logical size 847x480. Representative later averages: physics 4.78–4.93 ms, actors 5.44–5.48 ms, total update 10.36–10.55 ms, render/presentation about 6.27–6.31 ms. Render phase includes presentation and is not a separate GPU-only measurement.

`dense-profile-9-0.4.13` separately measured a five-second instrumented component window at the same scene, with the same labeled teleport/protection. Recorded totals: AnimationComponent 600.33 ms, PhysicsComponent 279.24 ms, TreasurePickupComponent 148.62 ms. Per-call timing adds overhead, including a clock floor even for nearly empty updates; these totals guide investigation and are not an FPS benchmark or exclusive CPU allocation. Remaining top entries and original logs are retained locally.

`tools/scene_profile_smoke.py` now uses CampaignSession's isolated saves, streamed logging and restoration for a declared real-map scene. Any proposed optimization must be measured against the same APK/viewport/scene and retain animation events, attack frames, collision behavior, sound and visual quality. Full campaign-wide 60 FPS remains an open requirement.
