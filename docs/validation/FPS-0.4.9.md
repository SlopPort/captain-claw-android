# FPS optimization — 0.4.9

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Codex (LLM), 2026-10-21. Huawei P9 Lite VNS-L21, LineageOS Android 10, about
2 GB RAM, 1920×1080 display. Resolution, aspect ratio, nearest filtering, visible
touch controls, music/effects at 22050 Hz and 0.4.8 update/physics rules were kept.

## Baseline

Repeated 0.4.8 measurement: `reports/fps-baseline-0.4.9`, 35 seconds per map start,
no protection, excluding the first 300-active-frame batch:

| Level | FPS |
|---|---|
| 8 | 56.4–57.9 |
| 9 | 52.6–56.1 |
| 13 | 56.1–59.5 |

Level 9 update took about 10 ms and render/present about 8 ms. Component profiling
identified animation as the largest update cost, but profiler overhead means it
is not itself an FPS benchmark. Box2D retains 10/8 solver iterations.

## Cause and change

The Android entry point selects `opengles2` via `SDL_HINT_RENDER_DRIVER`. In the
pinned SDL, explicit selection defaults to `batching = SDL_FALSE`, executing the
queue per command rather than submitting commands together. Setting
`SDL_HINT_RENDER_BATCHING=1` enables the existing queue.
[Source: pinned SDL_render.c](https://github.com/libsdl-org/SDL/blob/5d249570393f7a37e037abf22cd6012a4cc56a71/src/render/SDL_render.c#L1008),
especially driver selection/batching override around line 1069.

This integrates SDL functionality, not a new renderer. Draw order/texture state
remain; game code does not interleave SDL with direct OpenGL calls. No reduction
in image size, enemies, animation speed or logic frequency.

`render-batching-off` in app data disables batching at next launch, allowing
same-APK comparison and a local fallback for driver problems. Saves/data remain.

## Comparison method

`python tools/render_batch_smoke.py --levels 8 9 13 --hold-seconds 35 --report fps-batching-ab`
runs off/on/off. Each uses the same APK/settings and temporary level unlocks.
The script requires the expected mode log and preserves an existing opt-out;
its child restores config/progress. Battery state is recorded before each pass.
CPU/GPU frequency, temperature and performance mode are not forced.

Only stationary starts are measured, not whole routes, all fights, long-play
heat or other GPU drivers. FPS counts active simulation only. Render time includes
presentation wait, not pure GPU time.

An existing immersive-start race sometimes reads 1800×1020 before system bars
hide, selecting 847×480, or 1920×1080 → 853×480. Physical screen/screenshots stay
1920×1080; the first case has a small margin. Initial level-8/9 pairs differed,
limiting comparison. Level 9 with batching was wider (853×480 versus 847×480);
level 13 matched at 847×480. This is a separate startup-size bug, not a deliberate
benchmark quality reduction. The tool now logs actual logical dimensions.

## Off/on/off results

Same APK, `reports/fps-batching-ab`: mean of six successive 300-active-frame
batches after excluding the first:

| Level | Off | On | Off again |
|---|---:|---:|---:|
| 8 | 56.90 | 60.20 | 56.42 |
| 9 | 54.22 | 60.20 | 54.98 |
| 13 | 57.93 | 60.17 | 57.05 |

With batching, p95 was 17–18 ms; without it 19–22 ms. Reported 60.2 means roughly
60 FPS due to clock precision/measurement, not an increased refresh rate.
Battery temperatures before runs: 31 / 32 / 32°C, not CPU/GPU temperatures or
proof of no throttling. Lower FPS after disabling again at similar temperature
supports a batching benefit, subject to the viewport limits above.

Level-8 screenshots in both modes were inspected: world, sprites, transparency,
HUD and controls render. Animation phases differ and the margin reflects startup
size; pixel-identical frames are not claimed.

## Final APK: all maps and touch

`reports/all-levels-0.4.9`: 25 seconds after confirmed load/audio on each map;
stationary unprotected hero, ordinary enemies active. First 300-frame batch
excluded. All 14 loaded with audio and no detected process crash. Below are batch
mean ranges and worst p95, measuring the engine loop rather than physical display
presentation of every frame.

| Level | FPS | Maximum p95 (ms) | Warmed batches | Logical view |
|---|---|---:|---:|---|
| 1 | 60.2 | 18 | 4 | 847×480 |
| 2 | 60.2 | 18 | 4 | 853×480 |
| 3 | 60.2–60.4 | 18 | 3 | 853×480 |
| 4 | 60.2 | 18 | 4 | 853×480 |
| 5 | 60.1–60.2 | 20 | 4 | 847×480 |
| 6 | 60.2–60.4 | 18 | 3 | 847×480 |
| 7 | 60.2 | 18 | 4 | 847×480 |
| 8 | 60.2 | 18 | 4 | 847×480 |
| 9 | 60.2 | 18 | 4 | 847×480 |
| 10 | 60.2 | 18 | 4 | 847×480 |
| 11 | 60.2 | 18 | 4 | 847×480 |
| 12 | 60.2–60.3 | 18 | 4 | 847×480 |
| 13 | 60.2 | 18 | 4 | 847×480 |
| 14 | 60.1–60.2 | 21 | 4 | 853×480 |

Levels 5/14 have less even frame timing despite about 60 FPS. Initial batches
included hitches such as 113 ms on level 6 and 129 ms on level 10. Warmup does not
remove every hitch. PSS snapshots about 132–187 MiB are neither peak memory nor
full GPU cost.

`reports/jump-touch-0.4.9`: six passes, short rise about 74 px, held 155 px;
app-event-to-takeoff 18–22 ms (earlier 0.4.8: 29–31 ms), not full hardware latency.
Finger slides do not trigger neighboring actions. Movement+jump, pause and
background-return cases passed.

`reports/gameplay-perf-9-0.4.9`: 45 seconds of repeated left/right movement, sword,
jump, shooting and crouch at the real level-9 start. There were 54 input commands;
observed x moved from 1594 to 1733 and back, rather than relying only on command
acks. No teleport/protection/extra ammo; HP100 before/after. First batch:
58.3 FPS, p95 20 ms, maximum 67 ms. Next eight: 60.0–60.3 FPS, p95 18 ms,
maxima 18–23 ms. Passed, original config/save restored. This short section is
neither a whole-map benchmark nor every-enemy combat coverage.

APK: `dist/kapitan-pazur-0.4.9-debug-universal.apk`, 0.4.9-dev (21), ARM64/ARMv7.
SHA-256: `60283884da15886c70844b20e35c9dd894166d79d83b4133be48173dedbb7812`.
Both ABIs, ARM64 16 KiB segments, zipalign and v1/v2 signatures passed. The usual
apksigner warning about Gradle META-INF metadata remains. Commercial game data
is absent from the APK/source package. These short samples do not establish
sustained whole-level performance or 60 FPS throughout the campaign.
