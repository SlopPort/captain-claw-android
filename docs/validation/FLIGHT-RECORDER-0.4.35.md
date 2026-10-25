# Background recorder validation — 0.4.35

OpenAI Codex (LLM), 2026-10-25, following an anonymous human request. The recorder helps investigate the still-open level 2 platform report; it does not fix that blockage.

## Implementation

See [player/developer instructions and format](../BACKGROUND-DEBUGGING.md). Sampling is on the game thread; formatting and file I/O run on one worker thread. There are 600 fixed sample slots, eight saved contacts per sample, one pending job per report class, two rolling destinations and two candidate destinations. A completed file is replaced by rename after the temporary file closes. No new dependency, network transfer or Android permission was added. Non-debug NDEBUG builds use empty recorder entry points.

## Huawei ARM64 checks

Physically tested debug APK SHA256: `4c97cf35bd48eb09016e7eb1f4b947528841e101781bf5f79ae5b59e42821a10`, version code 47, 0.4.35-dev. It was installed in place without uninstalling.

`tools/check_flight_recorder.py` used an explicitly teleported level 2 wall fixture and ordinary timed SDL right input. This is not natural campaign evidence. After setup, combat diagnostics were disabled with the quiet command; recording continued independently.

- Recorder disabled for 25 seconds: report files did not change.
- Recorder enabled for 70 seconds: both rolling slots reached exactly 600 samples. Retained tick spans were about 64 seconds, consistent with a minimum 100 ms sample interval and frame scheduling.
- An intentional wall push created a `blocked-candidate` file with 25 samples and recorded right-action input. This validates the trigger, not a real bug verdict. Only one candidate slot was needed in this run; rotation into the second candidate slot is structurally bounded but not independently exercised here.
- The rolling files were 266,164 and 266,061 bytes; the candidate file was 9,619 bytes. At most eight contacts were saved per sample. This one run retained 541,844 bytes total; these are observed sizes, not a universal exact disk budget.
- In the last four reported frame windows, enabled and disabled modes both measured 60.2 FPS with p95 frame time 18 ms. This short sequential comparison at one level 2 location does not certify every scene, thermal state or the campaign FPS minimum.
- `tools/collect_game_debug.py` copied all three complete reports while leaving the phone files unchanged. Reports remain ignored locally; raw collision data is not published.

The first checker mistakenly treated Android exec-out's missing-file error text for the unused fourth slot as a report (exit status was zero). The reader was corrected to require the format signature. The already completed run and retained files were revalidated without replaying the device session. That checker failure is retained; it was not a recorder-file corruption.

## Storage-failure fixture

The writer's temporary pathname was obstructed by a directory in the app's own data folder; no real disk was filled. The first attempt used an empty directory, which normal C++ remove() cleanup could remove, invalidating the test's cleanup assumption. A revised nonempty, owned obstruction was used to test sustained failure and later recovery. The revised check passed: one warning during sustained failure, game process stayed alive, and periodic writing resumed within seven seconds after removing the obstruction. Configuration/saves were restored and byte-checked. Only the owned file/directory is removed, nonrecursively.

## Limits

This records gameplay/physics observations, not arbitrary application state, audio events, every frame/input pulse or a complete crash dump. Automatic candidates can be ordinary walls. Recent samples can be lost on abrupt termination before a periodic write. Thread-creation failure and physical ENOSPC/power loss were not injected. ARMv7 build coverage is separate from physical runtime coverage. No Redmi or full campaign run is claimed. User settings and saves are restored and byte-checked by each owned fixture.

## Build and final installation

Debug builds passed for ARM64 and ARMv7. The combined APK SHA256 is `1161b8033069291aab591e873ba9f26fb1c07d3d1296bb6134df3412f59ad118`. Every ARM64 native library in it is byte-identical to the ARM64 APK used for the measurements above. The combined APK was installed in place on Huawei and the normal launcher reopened. ARMv7 was built, not physically run. No signed public release was produced by this batch; the existing public test release remains 0.4.32.
