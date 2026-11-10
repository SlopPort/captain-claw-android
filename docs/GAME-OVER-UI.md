# Game Over screen

The Android Game Over screen contains a heading, not a list of two choices.
A fresh touch anywhere invokes the existing return-to-main-menu action.
Keyboard/controller confirmation also returns to the main menu.

The previous Polish wording was `Koniec gry / Dotknij ekranu: menu główne`.
Version 0.4.31 separates the larger heading from the instruction with a divider:

- Polish heading: `Koniec gry`
- Polish instruction: `Dotknij dowolnego miejsca, aby wrócić do menu głównego`
- English heading: `Game Over`
- English instruction: `Tap anywhere to return to the main menu`

The instruction describes the whole screen, rather than a small button hit area.
The change renders original text locally and does not redistribute commercial
bitmap lettering. Implemented by OpenAI Codex (LLM), following human feedback.

Validation results must identify the APK and actual device. A last-life test
fixture is not evidence of a natural campaign playthrough.

## Validation on Huawei / Android 10

Debug APK 0.4.31-dev (ARM64 and ARMv7 packaged), SHA-256:
`c31507c5541f3c94675b7563337dc151ac3b5cafde6b9e131b69401349d1c8cc`.
The ARM64 runtime was tested. Both native ABI builds succeeded.
The real last-life death path opened Game Over, an app-local touch returned to
main menu, and no native/Java fatal error occurred. The Polish screenshot was
visually inspected: heading, divider and complete instruction are visible.
Original config and progress were restored by the test helper. No Redmi access
was used. This is not a physical-controller or natural campaign test.

Additional app-local taps at logical coordinates (10, 10) and (630, 470), outside
the text card, both returned to menu. Reproduce with
`python tools/game_over_anywhere_smoke.py --report unique-report-name`
after selecting the allocated device with `ANDROID_SERIAL`. Original settings,
progress and controller bindings were byte-identical after all tests.

## Debug41 recheck

2026-11-08, OpenAI Codex (LLM). Exact Huawei ARM64 debug41 APK SHA-256
`4bcf15bade79c4047cd6b387b02ae5b0c35b7596f19528f167041a5416d8f187`.
The earlier fixed `(630, 470)` coordinate is outside the text card, but is not
the screen's right corner at a logical width of 853. The helper now derives
the viewport from runtime evidence and checks crash attribution.

Fresh fixtures passed at `(10, 10)` and `(843, 470)` on the actual `853x480`
viewport: last-life death opened Game Over, an app-local SDL diagnostic tap
returned to the main menu, the process remained alive, and no target or
unattributed fatal line was found. Each fixture restored its own fresh
configuration/progress backup. The Polish before-screen was visually inspected:
the larger heading, separator and complete whole-screen instruction are visible.
This does not establish private preference preservation or a physical touch
test at every pixel. The separate debug41 Android-window center-tap regression
also passed; natural deaths during campaign play remain the human's test.
