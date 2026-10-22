# English UI follow-up / Angielski interfejs

Requested 2026-10-22; implementation pending after the current campaign/compatibility and vertical-combat work. Plan by OpenAI Codex (LLM). Existing English README and installation instructions are not equivalent to English in-game UI.

Required scope:

- Android launcher/import, progress/error/retry messages, file tools, backup/restore, controller bindings, vibration and descriptions for accessibility.
- Native touch labels, pause/help text and diagnostics presented to players. Keep diagnostic detail out of ordinary player flows.
- OpenClaw menu text currently supplied as original PCX images: inventory language dependencies before replacing or translating it. A Polish game archive does not automatically contain English menu art or voice recordings. Do not distribute commercial English assets.
- New encounter/finale captions and generated credits where applicable. Preserve upstream attribution and the LLM disclosure in both languages.
- Explicit Polish/English selection with a documented default, persisted without rewriting imported game data or progress. Verify restart and update behavior; do not change bindings when switching language.

Use Android string resources for Android screens and a small shared native lookup for native labels. Avoid concatenating sentences or using bilingual text as a substitute for a selected-language interface. Test long labels, small displays and controller-only navigation. English documentation must accurately state any remaining dependence on the user's original game-data language.

No claim of a complete English translation is made at this checkpoint. Original voice dubbing and copyrighted menu art are a separate data/license matter from translating our own interface.
