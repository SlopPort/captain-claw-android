# Code guide / Mapa kodu

Adaptation changes in this session were made by an LLM; upstream source retains its original authorship. This guide explains entry points and reasons for the non-obvious design choices. It does not claim that every inherited source line has been reviewed or commented.

| Source | Responsibility and important constraint |
|---|---|
| `app/.../LauncherActivity.java` | Imports only the exact required ZIP entries into application storage. The allowlist excludes path traversal and save replacement. It currently accepts a prepared ZIP, not bare REZ. |
| `app/.../GameActivity.java` | Hosts SDL and Android lifecycle handling. Device input must remain scoped to the game. |
| `app/.../ControllerSettingsActivity.java` | Captures physical Android button codes or triggers, swaps occupied assignments within each action group and atomically saves the binding file. PL/EN UI; bindings currently shared by devices. |
| `native/android_main.cpp` | Android startup, paths and engine entry. |
| `native/PlatformInput.cpp` | Tracks held keys separately for touch and controller. Only changes to the union reach the game, so one source cannot release another source's key. Runs on the SDL thread. |
| `native/TouchControls.cpp` | Finger ownership, stick, action regions, minimum touch jump hold and cached UI. Cancellation must release keys. Cached textures avoid repeatedly drawing larger controls with expensive primitives. |
| `native/GamepadControls.cpp` | SDL controller mapping, axis hysteresis, menus, hotplug and focus changes. Context transitions require neutral controls; disconnect must release movement. Virtual-pad commands are diagnostic scaffolding, not hardware-test evidence. |
| `native/CombatProbe.cpp` | Opt-in controlled arenas, jump measurements and app-local command mailbox. Combat commands require active gameplay; virtual button releases also work when paused. Test protection/teleports must never be reported as normal play. |
| `native/OmarEncounterComponent.cpp` | Adaptation's encounter and engine-staged finale. Exact equivalence to the original game is unverified. |
| `native/LavaGeyserComponent.cpp` | Level 14 hazard behavior. |
| `patches/openclaw-android.patch` | Changes to the pinned OpenClaw tree: integration, rendering, resources, audio, AI, health and collisions. Generated with `tools/export_patch.py`, not a second independent source tree. |
| `asset-overrides/` | Local XML prototype/metatada changes combined with support assets by the packer. |
| `tools/pack_assets.py` | Creates a separate package from the user's PC game. Does not modify that installation or download the game. |
| `tools/prepare_game_data_gui.py` | Bilingual GUI around the existing bootstrap/packer. Worker thread handles subprocess output; Tk updates stay on the UI thread. |
| `tools/bootstrap.py`, `sources.lock.json` | Fetch pinned open-source dependencies and apply the patch. Preserve unexpected local changes instead of silently resetting them. |
| `tools/prepare_runtime_assets.py` | Generates redistributable music support and the Android-only controller database before building. Licenses remain in APK assets. |

Komentarze w kodzie opisują przyczyny, własność obiektów, granice testów i wymagania dotyczące zwalniania wejścia. Dziennik ustaleń i otwartych problemów jest w [DEVELOPMENT-NOTES.md](DEVELOPMENT-NOTES.md); wyniki i zakres prób w `validation/`. Nie wszystkie historyczne komentarze OpenClaw ani dokumenty są przetłumaczone. Nie deklarujemy pełnego przeglądu odziedziczonego silnika.

0.4.8: `ImportSupport` validates a complete REZ and installs XML/generated support plus a local system font. `SaveFiles` canonicalizes bounded saves, rejects invalid structure/values and atomically applies staged imports with backup; `FileToolsActivity` hosts Android document intents. `HapticFeedback` is an opt-in SDL/Android adaptation of Claw Web's event design. Actor updater caching preserves component-ID order and filters only exact types inheriting the empty base VUpdate, guarded by a member-pointer type trait. Box2D's Android profiling clock uses monotonic signed nanoseconds; physics timestep/solver counts are unchanged. Both engine and SDL patches are reproducible through bootstrap/export tools.

0.4.7: `BaseGameApp::SaveGameOptions` preserves existing XML and saves only live audio controls before audio teardown or on backgrounding. Whitespace condensation is temporarily disabled while reading so significant spaces in other values survive. Phase samples split input/events/update/render wall time; render includes GPU/vsync waiting and is not CPU usage. `PAZUR_OPTIMIZE_DEPENDENCIES` enables `-O2` for dependencies without disabling assertions. The joystick cache follows the same reset/fallback rules as action buttons. `tools/audio_options_smoke.py` checks background saving, restart loading and preservation of unrelated XML values/attributes.
