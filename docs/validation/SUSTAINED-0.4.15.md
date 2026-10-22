# Twenty-minute dense-scene observation

OpenAI Codex (LLM), 2026-10-22. Report: `reports/sustained-level9-0.4.15` (local, not redistributed with commercial screenshots/data).

Same physical Huawei P9Lite Android 10, ARM64. Installed 0.4.15-dev APK SHA-256 `36719447575c7b5f2bd49d9da8dad835f2d22068a465bfe45d9ce7d9776947d3`. Existing level-nine geometry at setup teleport (11027,5500), settled hero (11027,5554.6), explicit protection, no movement/shots or ammo edits. This observes live enemies in a dense scene; it is not campaign traversal or a full device thermal characterization. USB internet/charging remained as configured by the user.

- Requested observation 1200 seconds, measured 1200.856 seconds. Process remained alive; no observed fatal crash. Configuration and saves restored afterward.
- 234 batches of 300 loop intervals. Approximate overall FPS from equal-frame batch harmonic mean: **58.449** (batch values rounded to 0.1 FPS). First 30 and last 30 batch arithmetic means were both **58.513**. No sustained FPS decay is established in this one scene/run; this is not a guarantee against thermal throttling elsewhere.
- Batch FPS ranged **48.7–60.2**. Largest observed interval **64 ms**; largest batch p95 **26 ms**. Therefore this does **not** pass steady 60 FPS.
- Reported battery temperature was **28.0 C before / 35.0 C after**. Battery temperature is not CPU temperature. Before/after memory/battery reports and complete native logs remain local; a point memory sample is not peak-memory/leak proof.
- The performance harness now streams logcat continuously, without clearing system logs, so a long run cannot silently lose early batches when the ring buffer wraps. The startup surface was 1800x1020/logical847x480; sampling required the corrected settled 1920x1080/logical853x480 and did not mix viewports.

Po polsku: dwadzieścia minut tej ciężkiej sceny nie spowodowało awarii ani widocznego trwałego spadku średniej wydajności. Cel stabilnych 60 FPS nie został osiągnięty. Wynik dotyczy konkretnego APK, telefonu i sceny; nie zastępuje przejścia wszystkich poziomów.
