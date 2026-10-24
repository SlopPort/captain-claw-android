# Startup physics cost and post-jump animation — 0.4.11

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

Code, work and tests by OpenAI Codex (LLM), 2026-10-21. The human reported behavior
and supplied Huawei P9 Lite VNS-L21, 2 GB RAM, LineageOS / Android 10. Physics
originates in OpenClaw and bundled Box2D by Erin Catto/contributors. Changes are
marked in source and retain upstream licenses.

## Diagnosis

Level 9's first physics step took about 60–68 ms, including about 46–57 ms outside
Collide/Solve/TOI. Step source inspection points mainly to initial potential-contact
batch preparation. No Step(0) warmup, contact work moved into loading, solver change
or simulation-timing change.

The initial experiment rejected impossible pairs only after tree search, showed
no convincing benefit and was removed. Retained `pair-filter-9-off-a`,
`pair-filter-9-on`, `pair-filter-9-off-b`: first steps 59.66 / 57.96 / 65.16 ms;
first-batch maximum frames 73 / 78 / 82 ms. Dense-scene results also showed no gain.
Some starts used 847×480 versus 853×480 windows; these differences are not speedups.

## Final change

A new map's initial search batch contains all active collision proxies. Every
contact admitted by Box2D needs at least one dynamic body: the existing unconditional
b2Body::ShouldCollide rule, before user filtering.

If the batch contains **every distinct active proxy**, searching from dynamic
endpoints still finds every permitted pair. Other pairs would be rejected anyway.
Pair sorting, contact creation, user filters and solver are unchanged. Ordinary
partial batches keep the old search.

Completeness checks sorted unique IDs and ignores removed proxies. Entry count
alone is insufficient: repeated touches of one proxy do not cover the others.
The generic broad-phase uses an optional query-start eligibility callback, without
depending on game actor classes.

`physics-pairs-unfiltered` in game data restores the old algorithm at next launch.
`tools/gameplay_perf_smoke.py --pair-filter off|on` owns it only during a test,
removes its own marker in restoration and refuses to overwrite an existing one.
Both modes can be compared in one APK.

## Equivalence test

`tests/box2d_pair_filter_test.cpp`, run via `tools/test_box2d_pair_filter.ps1`
with host MSYS2 UCRT64 g++ 15.1: two worlds, variant on/off, 600 steps with varied
dt and 10/8 solver iterations. Positions, angles, velocities, sleeping, contact
counts, filter calls and all 7003 ordered Begin/End/PreSolve/PostSolve callbacks
matched.

The scene includes merged static tiles, sensors, a kinematic platform, projectile,
a collision-blocking joint, body-type changes, fixture/body creation/removal,
activation and mask changes. A thousand repeated touches of one proxy verify a
partial batch is not mistaken for complete. This tests pinned Box2D on the host,
separate from device results; it does not prove whole-game Windows parity.

## Same-APK device comparison: off/on/off

Reports: `query-subset-9-off-a`, `query-subset-9-on`, `query-subset-9-off-b`.
Each starts a fresh process on real level 9 and observes 20 seconds, without
teleports, protection or ammo changes. All use initial 1800×1020 surface,
847×480 logical, then 1920×1080 after bars hide. Resolution/filtering unchanged;
music/effects enabled.

| Measurement | Off A | On | Off B |
|---|---:|---:|---:|
| First Box2D step | 57.52 ms | 21.92 ms | 66.13 ms |
| Time outside Collide/Solve/TOI | 46.41 ms | 10.22 ms | 55.24 ms |
| First-batch maximum frame | 72 ms | 38 ms | 83 ms |
| FPS of subsequent full batches | 59.9–60.2 | 60.0–60.2 | 60.2 |
| Bodies / contacts after first step | 3197 / 268 | 3197 / 268 | 3197 / 268 |

The initial hitch improved, **without a demonstrated sustained-FPS increase**.
Even 38 ms exceeds a 60 FPS frame budget. A/B/A helps distinguish warmup but does
not fully control CPU temperature/system load or promise 60 FPS everywhere.

## All level starts

`tools/level_boot_smoke.py --levels 1 2 3 4 5 6 7 8 9 10 11 12 13 14 --frequency 22050 --effects-on --preview-level14 --hold-seconds 18 --report all-levels-0.4.11`:
14/14 loaded without crashes, with music/effects and valid physics counters.
Level 14 used diagnostic preview, others ordinary starts. No teleports,
protection or forced attacks. Phone USB tethering/network remained unchanged.

FPS excludes the first 300-frame batch, leaving only 1–3 full batches per start.
The maximum includes startup to retain hitches. PSS is one process-memory sample,
not a peak.

| Level | FPS after first batch | Worst p95 after startup | Maximum frame in full trial | PSS MiB |
|---|---:|---:|---:|---:|
| 1 | 60.2 | 18 ms | 38 ms | 130.4 |
| 2 | 60.2 | 18 ms | 33 ms | 140.7 |
| 3 | 60.2 | 18 ms | 32 ms | 177.0 |
| 4 | 60.0–60.2 | 18 ms | 26 ms | 130.7 |
| 5 | 60.2 | 20 ms | 41 ms | 148.7 |
| 6 | 60.1 | 18 ms | 74 ms | 186.7 |
| 7 | 60.2 | 18 ms | 40 ms | 141.6 |
| 8 | 60.1–60.2 | 18 ms | 30 ms | 163.2 |
| 9 | 60.2 | 18 ms | 32 ms | 161.9 |
| 10 | 60.0–60.2 | 18 ms | 55 ms | 160.0 |
| 11 | 60.0–60.2 | 18 ms | 32 ms | 144.4 |
| 12 | 60.2 | 18 ms | 30 ms | 140.5 |
| 13 | 60.2 | 18 ms | 26 ms | 180.3 |
| 14 | 60.2 | 20 ms | 30 ms | 160.0 |

These are neither whole-map tests nor natural campaign clears. Hitches remain,
notably 74 ms on level 6 and 55 ms on level 10; their subsystem cause was not
assigned without more profiling.

## First ladder

Ten short up/down trials at the real first level-one ladder's center/sides:
247 samples, per-frame state transitions, zero fall-animation samples. Six short
descend/sideways trials: 200 samples, also zero. These initial results did not
resolve the user's report.

A later top-walking case failed because teleport setup retained the previous
climbing state. Setup now exits climbing before independent walking/jump cases;
production ladder behavior was unchanged. `first-ladder-seam-trace` and
`first-ladder-sideways-exits` retain observations and this failure.

After clarification (“top and jump”), twelve short/full jumps from the top/just
below it were tested, stationary or with later left/right input. Reproduction:
at about x1392,y4304 and x1492,y4312, Claw stood grounded while `fall` persisted
for seconds. Some final reads in that first long run failed after Android's
ring log wrapped. The helper now streams complete logs locally rather than using
log length as cursor. This was not a game crash.

`first-ladder-precise-baseline` confirmed `ground=1`, `falling=0`, `jumping=0`,
zero horizontal speed but vertical residuals about 2.45×10⁻⁷ to −1.37×10⁻⁷ m/s.
PhysicsComponent compared Box2D float velocity against double DBL_EPSILON, so
VOnStopMoving did not restore standing animation.

The first `1e-5 m/s` tolerance failed the matrix: right-corner corrections around
−0.00048 m/s still left the wrong animation. `first-ladder-top-jump-fixed` retains
that failure; pass criteria were not relaxed.

The final change uses `0.01 m/s` tolerance only for the vertical stop-animation
callback (0.75 pixels/s at 75 px/m), still requiring ground contact/stopped state.
It changes no physical velocity, forces, shapes, jump or filters. It does not
repeat landing events/sounds/vibration. Climbing, hurt and death retain their guards.

`first-ladder-top-jump-fixed2`: 12/12 cases, 555 samples; top, descend, ladder
jump and walking checks passed. No grounded stationary fall animation lasted
at least 300 ms with below-tolerance speed and position change within 0.25 px.
Four isolated stop-transition samples are not automatically bugs. Tests use setup
teleports/protection but ordinary SDL input and real map collisions/ladder.

Final-APK `combat-0.4.11-final`: 13/13 projectile/contact cases, both sides,
three heights, standing/crouching and duplicate projectile-hit callbacks.
These controlled contacts do not audit every enemy/stair. Balance/hitbox geometry
were unchanged.

The fourteen-map startup series and A/B/A used the final Box2D algorithm before
the last animation fix. The final APK separately passed ladder/contact checks.
The earlier performance artifact is not presented as byte-identical to it.

## Final APK and limits

`dist/kapitan-pazur-0.4.11-debug-universal.apk`, versionCode 23, SHA-256:
`530237efc559b76f99b1f5ac0bcd60cdf0317d9aeabcfb2e6bac5e1f6cc34c13`.

- ARM64/ARMv7 builds, ABI checks, ARM64 ELF 16 KiB, zipalign and v1/v2 signature
  passed. Both patches apply to clean pinned sources and match working trees
  after CRLF normalization.
- `jump-touch-0.4.11-final`: 6/6, one jump per press, short 70.6–73.5 px, held
  154.3–155 px, app event → takeoff 16–20 ms. Multitouch, release, focus and no
  accidental attack/shoot after finger slides passed. Not hardware latency.
- `game-over-touch-0.4.11-final`: actual final death → Game Over → touch → menu passed.
- `dense-9-0.4.11-final`: setup teleport to (11027,5500), protected hero, 25 s
  observation without attacks/ammo changes. First batch 55.4 FPS / max 47 ms;
  subsequent 56.9–58.8 FPS, p95 19–20 ms, maxima 21–23 ms. **Still below steady
  60 FPS**; no sustained-FPS improvement is claimed for this scene.
- All trials restored config/progress and removed owned markers/mailboxes. USB,
  tethering, Bluetooth/network unchanged. Game data/private reports stay outside
  the repository/source archive.

Remaining at this checkpoint: dense-scene cost, hitches, stair combat and further
ladder/edge coverage. Natural full campaign completion and every-situation Windows
parity were unverified.
