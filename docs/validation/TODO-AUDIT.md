# Comment and performance audit — 0.4.7

OpenAI Codex (LLM) reviewed selected engine paths on 2026-10-20. This is not evidence that the game is bug-free or that a full playthrough passed. Paths below are relative to `upstream/OpenClaw/OpenClaw/Engine/`. Findings describe this historical checkpoint; later changes are documented separately.

| Finding | Assessment and action |
| --- | --- |
| `GameApp/BaseGameApp.cpp`, empty `SaveGameOptions` | A real gap in audio-setting persistence. Android now saves enabled states and music/effects volumes on backgrounding and orderly shutdown, using temporary-file replacement and preserving other configuration. A forced kill before backgrounding still does not guarantee saving. |
| `UserInterface/UserInterface.cpp`, two `VoiceOn` conditions and no `VoiceOff` | Confirmed source defect. Voice/Ambient menu controls mainly change button visibility; independent channel handling is incomplete. This remained open: correcting the typo alone would not fix audio switching. |
| `Actor/Components/PhysicsComponent.cpp`, old ladder TODO | Climb-ending fix already present in 0.4.6 and tested on the real first ladder of level 1. Exact comparison with the original Windows game was not performed. |
| Pickup/aura/ambient components' `VGenerateXml` returns null | Incomplete export/serialization; not by itself evidence of a normal-gameplay bug. |
| `KinematicComponent::RemoveCarriedBody` | Elevator-after-passenger-exit TODO needs reproduction on a specific elevator before changing physics. |
| `CrumblingPeg`, animation-end comment | Current frame-change handling already stops and hides the object. The comment may be stale; a map trial is needed. |
| Original death-effect and aura-effect TODOs | Visual differences do not establish faulty damage calculations. |

## Optimization

The debug engine already used `-O2`, but dependencies including Box2D did not. CMake option `PAZUR_OPTIMIZE_DEPENDENCIES` now enables `-O2` for them by default. Diagnostic symbols and assertions remain, without `fast-math` or a physics-step change.

The touch stick previously drew circles and edges every frame. It now uses three small textures (about 115 KiB) with the same dimensions and colors. The cache is rebuilt after renderer resource loss; unsupported renderers use the previous drawing path.

Huawei P9 Lite, Android 10 / LineageOS, approximately 2 GB RAM, 1920×1080, touch controls visible, music and effects enabled at 22050 Hz. Each level-opening scene ran for 40 seconds with a stationary, unprotected hero. Values exclude the first 300-frame batch:

| Scene | Before: FPS / frame p95 | After: FPS / frame p95 |
| --- | --- | --- |
| Level 1 | 22.9–23.0 / 49 ms | 60.0–60.2 / 18 ms |
| Level 13 | 18.3 / 62 ms | 42.5–43.9 / 25–26 ms |

Before logs: local `reports/fps-phases-baseline-0.4.7/`; after: `reports/fps-phases-optimized-0.4.7/`. Both scenes started with audio and no detected process crash. In level 1, world-update time fell from about 11.6 to 7.1 ms; rendering including GPU/vsync waiting fell from about 31.8 to 9.4 ms. Compilation and caching changed together, so this comparison does not isolate their individual contributions.

These short measurements do not guarantee 60 FPS everywhere, sustained thermal behavior or complete physics compatibility. Resolution and asset quality were not reduced. The memory query returned a system summary instead of reliable app PSS, so it supports no RAM-usage conclusion. Raw logs remain local and outside public source archives.

## Final checks

APK 0.4.7-dev, SHA256 `cec99ab20a247bae106303a932e0e55abc4bc6417e7c30a0b56f9ecf6db22465`: ARM64 and ARMv7 built; ELF libraries, ZIP/16 KiB alignment and APK signature checked. Physical-phone tests covered ARM64, not a separate ARMv7 device.

- `reports/audio-options-0.4.7/`: background save/restart readback passed, preserving other values, attributes and significant prompt whitespace. The first trial exposed TinyXML whitespace removal; this was fixed before the final test.
- `reports/ladder-optimized-0.4.7/`: real first ladder of level 1, climb ending, repeated Up, descent, jump and side exit passed.
- `reports/combat-optimized-verified-0.4.7/`: all 13 controlled hit/repeated-contact trials passed. The earlier trial stopped at the focus check because Android 10 names the dumpsys field differently. The parser was corrected without disabling the safeguard.
- `reports/jump-touch-optimized-0.4.7/`: six jump cases passed. Engine-event-to-motion latency was 28–30 ms; short tap rise 73.5–74.1 px; long hold about 155 px. Each hold caused one jump. Multitouch, no accidental attack after pointer drift, pause and background/resume passed. This is software timing, not physical finger-to-screen latency.

Configuration, progress and display settings were restored after testing. Idle and held stick screenshots were inspected. FPS logs preceded a small XML-whitespace fix and the addition of an audio test command; the final regression tests concern the SHA256 above. A full playthrough was not performed.
