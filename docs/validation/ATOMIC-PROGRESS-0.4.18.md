# Progress persistence and rejected FPS experiment

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-22. Development checkpoint; controller testing excluded.

## Native progress

Inherited checkpoint and next-level saves opened SAVES.XML directly through TinyXML, truncating the previous file before the new document had finished writing. Android now writes a sibling temporary file, checks serialization/flush/fsync/close, and atomically renames it over the old target only on success. A failed save keeps the previous target and displays a PL/EN error. The same helper syncs audio configuration before publication. Desktop engine paths retain their inherited behavior.

`SaveFiles` operations are serialized within the app process. Applying a pending import cannot race another thread publishing a replacement pending file, then remove that newer request. Initial save creation uses the same monitor; native startup occurs afterward on the SDL thread.

`atomic-xml-boundaries-0.4.18-r2`: **18 desktop cases passed**, compiling the actual production helper with the pinned TinyXML sources. Existing/absent target, failure and real child-process death at four boundaries (written/flushed/synced/before publication), preservation and successful retry; actual temporary-file open and publication failures also preserve the old target. The first compile attempt lacked the compiler runtime on PATH and failed before executing cases; retained as a harness failure. This is Windows filesystem evidence, not Android process-death, full-disk or sudden-power-loss certification. Directory metadata durability remains filesystem-dependent.

Phone ARM64 checkpoint/reload and score-to-level-two checks passed on APK SHA-256 `873c23510c180ae3899730fef27cd35204b1f75171afcce92b2291e446247638` (ARM64 + ARMv7, versionCode 30). `atomic-checkpoint-0.4.18-r3` observed a real checkpoint collision, the atomic-save marker, process restart and menu reload near (6882,4991.6). The fixture teleports to an existing checkpoint and uses isolated saves; it is not normal traversal. `atomic-score-0.4.18-r3` observed atomic next-level publication and loaded level two through focused-window touch. Original config/progress restored, no controllers or global input.

The earlier `atomic-checkpoint-0.4.18` used APK `62a62095f787acd04d38adbd75ff155143900a0557da578914f97c39680ae8fe`: checkpoint persistence succeeded, but menu reload failed because the diagnostic mailbox rejected the new local menu-key command outside gameplay. The gate was corrected; the failed report is retained. Production save behavior did not change between these two ARM candidates. The six-key menu sequence now uses SDL keyboard events, without virtual controller attachment.

`atomic-map-starts-0.4.18-r3-level1` through `level14` all passed on the same ARM candidate: isolated map starts, three seconds of observation each, settled logical viewport 853x480, no observed crash. This is explicitly not level traversal, boss balance, prolonged stability or all-map 60 FPS coverage. The map-sweep tool now records installed-package SHA for future runs; these original rows preceded that metadata addition.

Separate final-source x86_64 APK SHA-256 `87d78366dc8c65ecf98cbd032f13d0a618ce4093ea3f58ee03ac490be08fdffb` ran on the API-35 16 KB emulator. Android feature/file tests passed. `compat-api35-16k-0.4.18-level` **failed** its 100 ms jump criterion: one takeoff, 37.0 px rise, 116 ms effective hold, 173 ms takeoff. No claim that this is solely an emulator issue. Separately labeled `compat-api35-16k-0.4.18-held-menu/level` passed a 600 ms jump (151.3 px, 605 ms effective hold, 100 ms takeoff), atomic next-level save and exit/score/level-two load. Longer-hold success does not erase short-tap failure. Fixture config/progress restored after both. The emulator was synced and closed; the phone's USB internet remained unchanged.

## Rejected ownership experiment

Diagnostic ARM64-only APK SHA-256 `2d533e934f316548232629f0d937269b90790d7ce97748cf36a5743f9e0704a7`, versionCode 30. This APK predates the atomic-progress changes and is **not the final 0.4.18 package**. It compared borrowing an already-owned image pointer during rectangle calculation with the inherited weak/shared pointer round trip. No geometry cache, reduced resolution, physics or AI changes.

Same Huawei Android 10, level-nine setup teleport (11027,5500), settled (11027,5554.6), explicit protection, observe-only, unchanged USB internet/charging, same settled 853x480. Three 90-second off/on/off runs, 18 equal-frame batches each. Excluding each first batch, harmonic mean of rounded batch FPS:

| Mode / local report | FPS | Mean render ms | Battery before/after |
| --- | ---: | ---: | --- |
| off / bounds-0.4.18-off-a | 58.735 | 6.321 | 32/33 C |
| on / bounds-0.4.18-on | 59.043 | 6.290 | 33/33 C |
| off / bounds-0.4.18-off-b | 58.525 | 6.319 | 33/34 C |

Render-time change about 0.03 ms is too small here to establish a worthwhile improvement; FPS differences are not attributed conclusively to the pointer change. Experiment, command and switch were removed. Raw APK/logs/source snapshot remain local. No 60 FPS claim follows. Config/saves restored after every run; battery temperature is not CPU temperature.

## Clean-source build of 0.4.17

Archived revision `9fa0738732c0da611f1c7d497a5e6d75f0dc7a2f`, no uncommitted source copied. Fresh local clones at all pinned dependency commits, fresh FreeType submodule and native build objects, patches applied from the archive. Gradle offline used the existing installed toolchain/dependency cache. Both ARM ABIs built in about six minutes. This is a clean-source build, not a clean-machine/download-bootstrap test or byte-reproducibility guarantee.

`clean-source-0.4.17` APK SHA-256 `ee74b8fe6ee24729586d3f473de152826b93cdca7b83e2f07faf78bb7bf94b8d` was installed on Huawei. `clean-source-runtime-0.4.17` passed direct GameActivity entry and six focused-window jump/multitouch/focus cases, then restored config/progress. No controller or global system input was used. APKs from different build paths need not have identical hashes; the tested clean build is identified separately from the original incremental 0.4.17 package.
