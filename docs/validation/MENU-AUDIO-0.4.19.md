# Touch audio controls / Dotykowe suwaki dźwięku

OpenAI Codex (LLM), 2026-10-22. Work in progress; controller testing excluded.

## Implementation

The inherited menu exposed volume knobs, with keyboard volume events, but its mouse/touch handler only activated buttons. Android now captures a touch on either volume track until release/cancel. Dragging outside the row keeps control of the original channel; volume clamps at its endpoints and never toggles the mute label underneath. Existing backend limits remain sound 0..100 and music 0..20; this does not change audio balancing or MIDI/SFX quality. The last value is persisted once on release/cancellation through the existing atomic configuration writer. Focus loss, page return and a new press end stale capture.

Translated sound/music labels now occupy only the left part of the row, leaving the slider clear. Two simple original track lines are drawn before the inherited knobs. No commercial menu artwork is added to the package. Rendering remains confined to menus.

## Initial slider evidence

Candidate x86_64 APK SHA-256 `eb66d2fdc382a33d723e7c92d61226b48b26fc1cece4acb128b3d6c30a6a1cba`. `audio-menu-api21-0.4.19-en/pl` passed focused-window navigation plus six actual MotionEvent gestures: sound 0/100, music 0/20, sound drag crossing into the music row (sound 30, music unchanged 20), and ACTION_CANCEL committing sound 50. Config-file values and unchanged mute flags were checked; screenshots and native volume commits were retained. English maximum-volume layout was visually inspected. Config/progress/language restored. This candidate has not been tested on the physical phone.

## Confirmed mute-state bug

The additional `audio-toggle-baseline-api21-0.4.19-en` test failed on that same APK: mute/unmute XML events re-enabled independent voice/ambient controls, although their backend shares the master Sound switch. Initialization-only disabling was insufficient. The baseline failure is retained. Android SetState now preserves the disabled invariant for those controls.

Corrected x86_64 APK SHA-256 `162d76864337cb3427ae83895274e055eb993af02a5cc5522aafdc01ee66ab94`: `audio-fixed-api21-0.4.19-en/pl` passed all 17 navigation transitions, six slider gestures, mute/unmute attempts and the disabled-state invariant for every logged voice/ambient item. Actual-APK translation coverage passed 109/109 named elements in both languages. The separately compiled ARM64 + ARMv7 candidate SHA-256 is `8809cd2c01a9b6b6bd6f9fedabad96516387c669549426a98b51b6381a1b1c2b`; its ELF coverage/alignment checks passed, but physical-phone runtime remains pending until the ongoing 0.4.18 combat sweep finishes. Do not transfer emulator results to that ARM APK.

## Polski

Dodano przeciąganie suwaków dotykiem, zachowanie wybranego kanału przy przesunięciu palca na drugi wiersz i zapis po puszczeniu/anulowaniu. Próby suwaków w PL/EN na emulatorze Androida 5 przeszły. Dodatkowy test potwierdził ponowne włączanie niedziałających osobnych kontrolek głosów i otoczenia po wyciszeniu; poprawiona kompilacja przeszła ponownie tę próbę w obu językach. Telefon pozostaje przy osobnym audycie walki na 0.4.18, więc nie przypisujemy mu wyników emulatora 0.4.19. Kandydat ARM jest przygotowany do późniejszej próby.
