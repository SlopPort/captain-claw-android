# Android menu audit — 2026-10-30

Implementation and source review by OpenAI Codex (LLM), guided by anonymous human feedback.

## Findings and changes

The main menu removed Multiplayer in an earlier change but retained its vertical gap. Other inherited rows were disabled because their destination pages did not exist. Android now omits unsupported actions before constructing menu items and compacts the three affected action lists.

The packaged source definitions in `Build_Release/ASSETS/MENU.xml` have no destination pages for Replay movies, Custom level, Upload scores, Players or Display. Those rows are omitted along with Multiplayer. Controls and Difficulty remain: since the 2026-10-29 change they open working Android settings, despite having no XML destination page. Saving remains an implemented information page explaining checkpoints and backups.

Main-menu action tops are now y210/245/280/315/350 for Single player, Options, Credits, Help and Quit. Single-player New game, Load game, Saving and Back use y210/245/280/315. Full Options uses y225/260/295/330 for Difficulty, Controls, Audio and Back. These are logical 640×480 menu coordinates.

Pause menus, confirmation pages, level grids and audio-slider coordinates retain their existing layout. Voice and Ambient remain disabled explanations of the shared Effects setting, rather than independent audio toggles. Their inherited visibility/state events still have valid named targets.

## Verification and remaining work

- A host XML destination audit confirmed exactly six omitted rows in the main definitions and none in the pause definitions; Controls and Difficulty were retained.
- Both changed C++ files passed whitespace checks.
- The translation coverage tool derives exclusions from the actual APK XML and requires matching native removal logs. An absent translation cannot silently count as an intentionally removed row.

At the time of this source audit, no new APK was compiled or installed for these changes. Physical navigation, touch rectangles, gamepad focus and visual review in both languages remain pending. Source inspection is not runtime proof.

## Final runtime validation

Huawei ARM64 debug36 APK `63478ba59d551d37ef9c1fffe3cf473287de09a4dc8c763eb213adc4eeb1c013` passed `menu_language_smoke.py` in Polish and English. Both runs visited the expected 17-page transition sequence, opened working Controls/Difficulty settings through actual focused-window touches, exercised layout/movement/difficulty selections and restored settings. There were no attributed or unattributed fatal/crash records in these menu runs.

The updated translation audit passed all 103 expected item names in each language, with exactly the six intended omissions confirmed by runtime removal logs. Main, Options and Single-player screenshots were inspected in Polish; Main and Options were inspected in English. Text fits and removed-row gaps are gone. Proprietary background screenshots stay private. Physical controller navigation and pause-menu traversal were not separately retested in this batch.
