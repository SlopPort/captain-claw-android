# Joystick and widescreen — 0.4.1

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

20 October 2026, Redmi Note 8, Android 16, ARM64. Version 0.4.1-dev (13).
Raw evidence/configurations are local in ignored `reports/`, not in the repository.

## Changes

An eight-direction joystick replaces the four arrows. Its dead zone is 14 units
and maximum displacement is 48. The first finger owns it even outside its circle;
a second finger cannot take over. Jump, attack, shoot and weapon selection work
independently. Touch cancellation, focus loss and entering menus release controls.
Up/down retain climbing, crouching and looking functions. Jump is separate.
Displacement chooses direction; movement retains the game's existing speed.

Logical height stays 480; width follows the window aspect ratio, with a minimum
of 640. A 2340×1080 display gives 1040×480: 62.5% more horizontal world view.
Camera/HUD use window dimensions, and action buttons anchor to the right. Both
axes use the same nearest-neighbor scale, without stretching or blur. Noninteger
scales can make individual source pixels differ by one screen pixel in width;
no artificial sprite detail is added. Menus and score screens remain centered
4:3; pause overlays the full world. Menu touch coordinates include the offset.
The finale/Omar hint are centered and his dimming covers the whole screen.

## Verified tests

- Actual Android multitouch: joystick+jump, independent release, diagonals,
  up/down/left, dead-zone return, no second-finger takeover, shared action button
  and cancellation. Touch attack, shooting, pause/resume and home-screen return
  also passed without a stuck direction. Log: `joystick-0.4.1/native.log`;
  checker: `tools/verify_controls.py`.
- The same tests with temporary device sizes 1920×1080 (853×480 logical) and
  1440×1080 (640×480 logical). These simulate aspect ratios on one phone, not
  extra devices. Evidence/screenshots: `aspect-controls-0.4.1/`. Display size,
  configuration and save were restored.
- Ordinary starts of levels 1, 13 and 14, music/effects and no crashes. PSS:
  186526, 352177 and 251627 KiB respectively. Short warmed level-14 samples:
  59.9 FPS, p95 18 ms, maximum 25 ms. Initial samples include loading/hitches.
  Evidence: `widescreen-0.4.1/`.
- Longer warmed samples: level 1, 60 FPS, p95 18 ms, maximum 18–19 ms; level 13,
  59.6–60 FPS, p95 18 ms, maximum 19–24 ms. PSS: 182198 and 361291 KiB.
  Logs/memory: `widescreen-steady-0.4.1/`. Separate loading samples from steady work.
- Controlled complete Omar fight/finale: victory, full dimming, amulet, 4:3 score
  and menu return. Screenshots inspected. Teleports, protection and granted
  resources mean this does not establish balance. Evidence:
  `finale-widescreen-0.4.1-final/`. Earlier `finale-widescreen-0.4.1/` started at
  incorrect 42050,1900 and did not trigger staging; correct point: 41820,1940.
- Both ABIs (ARM64/ARM32) built; v1/v2 signature, ZIP and ARM64 16 KiB alignment,
  exported patch checked. Installed APK hash matches the distribution file.

At this checkpoint, older Android, ARM32 execution, 1–2 GB phones and actual
16 KiB pages were unverified. Short tests do not replace a full playthrough or
thermal soak. A wider view exposes more objects; load depends on the level.
