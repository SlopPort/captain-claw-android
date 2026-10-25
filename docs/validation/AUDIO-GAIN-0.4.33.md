# Android sound-effect gain — 0.4.33

OpenAI Codex (LLM), 2026-10-25; anonymous human bug report. No proprietary recordings are included.

## Finding and change

The Huawei configuration enabled effects at 10% and music at 8%. SDL_mixer multiplies chunk gain by channel gain. The inherited implementation applied the master effects setting to both. At 10%, quantized gain was approximately 0.9% before any per-effect attenuation. This can mask quieter combat effects under music, although it does not prove that every reported missing sound has this cause.

Android now sets chunk gain from the individual effect percentage and channel gain from the master slider. Desktop behavior is unchanged. Existing user volume preferences remain unchanged. The fix applies to all effects using this playback path; no replacement recordings were added.

## Physical checks

Huawei ARM64 debug 0.4.32 was measured first at 100% and then 10%. Sword, pistol, Officer and level 13/14 Chameleon playback requests were accepted and produced nonzero mixed PCM. Silence at idle was checked with music disabled.

The device was updated in place to ARM64 debug 0.4.33-dev, version code 45, without uninstalling. Exact APK SHA256: `e205a4dddd47bb5874e65ccc193ca599ad76df245b2ef1b444b657cd8543c83b`.

Repeat the same fixture with `python tools/attack_audio_smoke.py --sound-volume 10 --report YOUR-UNIQUE-REPORT`, selecting only an authorized device through a process-local ANDROID_SERIAL. Fixtures temporarily load controlled scenes, not natural campaign progress. Do not run while the player is playing.

Both low-volume runs passed. Mixed signed-16-bit PCM peak values:

| Fixture | Before at 10% | After at 10% |
| --- | ---: | ---: |
| idle | 0 | 0 |
| sword | 151 | 2267 |
| pistol | 255 | 3934 |
| officer | 255 | 3067 |
| chameleon13 | 251 | 3023 |
| chameleon14 | 370 | 4510 |

These are mixed-output observations, not isolated waveform gain ratios; enemy timing and other sounds can differ. No microphone was used and no audio was recorded. The test asserts actual mixer output, not what the listener heard. Configuration and saves were restored and byte-checked after each run. The game was reopened afterward.

## Limits

Only ARM64 debug was built and run for this change. No Redmi, ARMv7 runtime, public signed 0.4.33 APK, all-enemy/all-pickup sweep or campaign certification is claimed. Hurt effects were not independently isolated by this fixture. Human listening confirmation remains open; investigate specific remaining silent events separately. Public signed distribution remains 0.4.32-test.
