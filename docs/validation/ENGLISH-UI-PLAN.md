# English UI follow-up / Angielski interfejs

Requested 2026-10-22. Partial implementation in 0.4.13-dev by OpenAI Codex (LLM). Existing English README and installation instructions are not equivalent to English in-game UI.

## Implemented and checked

Android launcher/import messages, controller settings and save/vibration tools now use default English and Polish Android resources. Explicit language selection is available before data import and under PAD settings after import. First use follows the system language (Polish for `pl`, English otherwise); explicit selection is persisted independently of bindings, saves and imported archives. The phone's system language is never changed.

Native touch labels and the added Omar encounter/finale captions use a small ASCII lookup compatible with SDL_gfx's font. Android writes `ui-language.txt` atomically before starting the engine; these labels change on the next game launch. This avoids rebuilding button textures every frame or rewriting game data. Generated attribution cards already contain English credits and the LLM disclosure.

`language-settings-0.4.12.txt` passed actual Android instrumentation for PL/EN controller/file screens, native preference serialization and unchanged saves/bindings. `language-native-preview-0.4.12` additionally launched an isolated level in English; its screenshot was visually inspected and shows JUMP, ATTACK, SHOOT, WEAPON, PAUSE and TEST MODE fitting their controls. Both trials preceded the final 0.4.13 resource-key cleanup; final-build checks are recorded separately. Original preferences/configuration/progress were restored. This is not a test of physical controller transport or every translated error path.

## Remaining scope

Final ARM build `language-selection-0.4.13` passed the same checks plus actual selection of English in the language dialog, Activity recreation and refreshed visible sword-action text. Its isolated native screenshot was also captured. APK SHA-256: `994a2f1b94c256aebd642e23f761103619d6737b9d45f86bd495d130d0532eaa`. The earlier `language-native-preview-0.4.13` screenshot was visually inspected before this last Java-only chooser adjustment. This does not validate the original menu-art language.

`language-preview-ready-0.4.13` connects screenshot automation before starting SDL and requires a focused game window with the Android PAD overlay before capture. Its image was visually inspected with all English controls present. The earlier `language-selection` capture omitted the overlay; that capture alone was not a valid overlay-layout pass. No production rendering change was needed. API-21 selection evidence and its test-harness fixes are recorded in [compatibility](ANDROID-COMPATIBILITY.md).

The launcher disables language switching while its import worker is active, preventing Activity recreation from leaving a running import attached to the old screen and allowing another import. This is a source-reviewed concurrency guard; a full mid-import file-picker interaction test remains open. `language-import-guard-0.4.13` passed the same PL/EN screen/selection/native-preview instrumentation on Huawei after the guard. APK SHA-256: `f0df9125bb970fc735a39c306ae52366a8240d8ff20736af78790820e5e432e2`.

The original bitmap menu art, original help pages and recorded voices still follow the user's game data. Some low-level validation/operating-system error details remain English. The existing legacy touchscreen-help images are neutral placeholders; translating our controls does not make those complete help pages. No claim of a complete game translation is made.

Required scope:

- Android launcher/import, progress/error/retry messages, file tools, backup/restore, controller bindings, vibration and descriptions for accessibility.
- Native touch labels, pause/help text and diagnostics presented to players. Keep diagnostic detail out of ordinary player flows.
- OpenClaw menu text currently supplied as original PCX images: inventory language dependencies before replacing or translating it. A Polish game archive does not automatically contain English menu art or voice recordings. Do not distribute commercial English assets.
- New encounter/finale captions and generated credits where applicable. Preserve upstream attribution and the LLM disclosure in both languages.
- Explicit Polish/English selection with a documented default, persisted without rewriting imported game data or progress. Verify restart and update behavior; do not change bindings when switching language.

Use Android string resources for Android screens and a small shared native lookup for native labels. Avoid concatenating sentences or using bilingual text as a substitute for a selected-language interface. Test long labels, small displays and controller-only navigation. English documentation must accurately state any remaining dependence on the user's original game-data language.

Original voice dubbing and copyrighted menu art are a separate data/license matter from translating our own interface. Do not replace original voices with invented recordings or bundle commercial English assets.
