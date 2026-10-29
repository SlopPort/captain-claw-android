# Touch layouts and multiplayer menu removal — 2026-10-29

Implementation, automated tests and screenshot review by OpenAI Codex (LLM), guided by human requirements. Physical target: authorized Huawei P9 Lite; no other phone was operated. Installed through `adb install -r`, without uninstalling or changing USB/network settings.

## Changes

Android menus omit MULTIPLAYER_BUTTON. Options → Controls opens the existing Android settings screen with four persistent touch layouts: Classic, Comfort (larger actions), Jump beside attack (swapped jump/melee), and Left-handed (mirrored actions/stick). Native hit testing and drawing share the transformed rectangles. Layout changes release held touch keys and invalidate cached textures. Physical pad bindings remain available.

## Verification

- Debug application and instrumentation builds passed for ARM64 and ARMv7. Existing compiler warnings remain.
- `check_repository.py`, `check_patches.py`, `verify_apk.py`, and `git diff --check` passed. Patch application matches 55 engine files and one SDL file.
- Huawei focused-window menu automation passed in Polish and English on initial APK SHA-256 `f8f5dd6b252c3fe2535d7552b3db742c2c5718883ef002d96dc8a8d86aebea60`.
- Screenshot review found incorrectly encoded Polish characters in new descriptions. After correction, Polish menu automation passed again on installed final APK SHA-256 `80bde742f8f3dfa9f984b9671aa5f225dc9f206f1e3485a25e779c29e876aa36`. Final Polish screenshot was reviewed; text and selection are readable. Only resource encoding changed in the production application between those APKs.
- Each language run checked entry through Options → Controls, all four radio selections, saved preferences, the native-facing getter, return focus, and the normal help/levels/audio/credits/quit path. Logs confirm native layout reloads. Multiplayer removal was asserted. No target crash in successful runs.
- Original configuration, saves, language preferences and touch layout selection were restored by the test owners. Private raw evidence is under `reports/controls-menu-2026-10-29-final-{pl,en}` and `reports/controls-menu-2026-10-29-utf8-pl`.

## Failed attempts and limits

The first test sent UP to the game after DOWN opened Android settings; its focus guard raised an exception. The test now suppresses UP when that window loses focus. A second attempt incorrectly expected an explicit preference for the already-selected default; the test now accepts the default value. A test-build attempt needed the SDK environment path, and another caught a test variable typo; both were corrected before successful runs.

No natural campaign traversal, physical pad compatibility sweep, comfort study or gameplay exercise of every layout was performed. Menu and persistence coverage does not establish those properties. ARMv7 was built, not physically exercised in this batch. Final source newline normalization does not change resource content.
