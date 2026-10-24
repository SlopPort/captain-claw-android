# Touch and jumping — 0.4.3

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

20 October 2026. Redmi Note 8, Android 16. These changes concern touch controls;
keyboard jump physics remains dependent on hold duration.

Two causes of poor response were confirmed: extra key queuing after touch and
changing buttons when a finger moved. In the old layout, sliding left from Jump
released it and started an attack. A 10 ms pulse produced only 11.8 pixels of rise.

Touch now dispatches its event in the current game iteration. A button keeps its
finger until release; moving across a neighbor does not activate that neighbor.
A tap holds jump for at least 110 ms without delaying takeoff. Longer holds jump
higher. Focus loss and control reset release keys and cancel the minimum hold.

Buttons form an arc: Jump 120×120, Attack 104×104, Shoot 96×96 logical units.
Jump is bottom-right, Attack to its left, Shoot above. Symbols and hit margins
are larger. Thumb grouping was inspired by the
[mobile Dead Cells developers' account](https://www.gamedeveloper.com/design/porting-i-dead-cells-i-to-mobile-an-in-depth-breakdown),
without copying its assets.

| Hold / trial | Height before | Height after | Motion start before / after |
|---|---:|---:|---|
| hold10 | 11.8 px | 73.5 px | 41 / 25 ms |
| hold100 | 63.6 px | 73.5 px | 43 / 26 ms |
| hold250 | 154.1 px | 155.0 px | 43 / 26 ms |
| hold700 | 155.0 px | 155.0 px | 43 / 26 ms |
| hold1800 | 155.0 px | 155.0 px | 40 / 26 ms |
| drift100 | 33.7 px | 74.0 px | 42 / 27 ms |

Timing runs from the engine receiving the touch event to the first position
change above 2 pixels. It does not measure physical finger-to-display latency;
that needs a camera or suitable equipment. SDL queue-event age was recorded
separately. Six trials do not characterize the full latency distribution.

Larger circular buttons initially slowed rendering. Their two states are now
prepared once in small textures and copied each frame. Texture reserve is about
0.3 MiB; renderer reset recreates the cache. With music/effects after warmup:
level 1 about 60 FPS; level 13 about 54 FPS, versus about 53 FPS in the previous
APK with the same data. Level 13 remains limited; no all-map 60 FPS claim is made.

Passed: 18 jump measurements at three aspect ratios (physical 2340×1080, 16:9,
4:3), movement+jump and independent releases, attack/shoot, pause/background
return, 13 hitbox regressions and short level 1/13 starts with audio. Raw results:
`reports/jump-*`; summary: `tools/verify_jump_release.py`.

[A 2009 original-game player's account](https://forum.winehq.org/viewtopic.php?p=28959)
also describes lower jumps from taps and higher jumps from holding Space. No
frame-by-frame EXE measurement was performed. The 110 ms minimum is a touch
adaptation, not a claim about the exact Windows parameter.

## Huawei / 0.4.7

After library optimization and joystick caching, six jumps passed on Huawei
P9 Lite / Android 10: event-to-motion 28–30 ms, short rise 73.5–74.1 px, full
jump about 155 px. Multitouch, pause, background return and no accidental attack
when sliding passed. Raw evidence: `reports/jump-touch-optimized-0.4.7/`.
This is not full physical-touch latency. [Audit and FPS](TODO-AUDIT.md).
