# Movement options and three difficulty presets — 2026-10-29

Implementation and automated validation by OpenAI Codex (LLM), guided by human requirements. Authorized physical device: Huawei P9 Lite. No other phone was operated. The existing debug app was updated with `adb install -r`; it was not uninstalled.

## Behavior

Options → Controls retains four layouts and adds fixed/floating joystick or directional buttons, joystick dead-zone adjustment, and individual size/position sliders for jump, melee, shoot, weapon and pause. The editor reset removes only button adjustments. Drawing and touch use the same transformed, screen-clamped rectangles. Directional touches can leave and re-enter a direction, and release/cancel clears held inputs.

Options → Difficulty offers exactly Easy (damage taken 50%, pickup healing 150%), Normal (100%/100%, default), and Hard (150%/50%). Fractional positive effects round upward. Damage scaling is restricted to the player and excludes death tiles. Healing scaling is applied in the health-pickup path, leaving save loading and direct health restoration untouched. Lives, ammunition, enemy health, damage dealt by the player, checkpoints, invulnerability duration and movement physics are unchanged.

## Verified

Final application SHA-256: `e75748e3a2cd1712f2b05c8eb5f7197af7ade68b5cdca33e3e6e6e9fcb111c91` (local debug 0.4.35-dev).

- ARM64 and ARMv7 application and instrumentation builds passed; existing compiler warnings remain.
- Repository check, APK ELF/package verification, diff whitespace check and clean patch application passed. Engine patch matches 56 changed source files; SDL patch matches one.
- `gameplay_options_smoke.py --report gameplay-options-2026-10-29-final` passed on Huawei: four layouts × three movement modes; direction drag-out/re-entry; release clears movement; custom button bounds. Actual player HealthComponent damage from a base 10 was 5/10/15. Healing conversion plus AddHealth was 15/10/5. This is an isolated technical fixture, not natural gameplay.
- `menu_language_smoke.py --report gameplay-options-menu-2026-10-29-final --languages pl en` passed. Both runs opened Controls and Difficulty through actual in-game menu touches, selected all movement and difficulty choices, checked native-facing preference getters, exercised editor slider touch/release and verified saved values, then navigated normal help/levels/audio/credits/quit pages. No target crash in these runs.
- Test owners restored configuration and saves byte for byte, and restored language/control preferences after temporary changes.

- Final Polish visual run `gameplay-options-visual-2026-10-29-pl` passed on the same APK. Movement, difficulty and button-editor screenshots were inspected: Polish text, controls and percentage labels are readable.

## Failed attempt and limits

The first balance fixture lowered health after disabling invulnerability. Lowering health triggered the normal hurt observer and re-enabled protection, so damage was correctly blocked. Fixture setup now clears protection after setting health. The production damage rule was not changed to accommodate the fixture. An initial compile also exposed inherited min/max macros; native clamps now use macro-safe standard-library calls.

These checks do not establish natural campaign completion, physical ARMv7 runtime coverage, long-term performance or ergonomic preference. Healing conversion was tested with AddHealth, not by collecting every food type. Enemy and death-tile exclusions were reviewed in source; no complete boss regression sweep was performed. Private evidence remains under reports/ and build/.
