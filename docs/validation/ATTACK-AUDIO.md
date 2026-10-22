# Attack audio / Dźwięki ataków

Audit and implementation by OpenAI Codex (LLM), 2026-10-21. Original recordings stay in the user's game archive; the APK contains XML references only.

## Findings

Claw's original ANI events reference `SWORDSWISH.WAV`, `UPPERCUT1.WAV`, `GUNSHOT.WAV`, the magic voice/effect and `DYNATHRW.WAV`. A standing melee action randomly selects swipe, kick or uppercut in inherited OpenClaw logic. A kick's sound therefore is not necessarily the sword swish. Voice lines have separate random playback conditions and are not expected on every action.

The exact APK/XML audit initially found 76 enemy attack actions, no missing files among their defined effect references, and eight actions without any configured effect. Five of these missing definitions now reference their existing corresponding recordings:

| Definition | Original recording connected |
| --- | --- |
| Katherine, level 4 | `KATHERINE/WHIP1.WAV` |
| Wolvington, level 6 | `WOLVINGTON/UPPERCUT.WAV` |
| Marrow, level 10 | `MARROW/STAB2.WAV` |
| Chameleon, levels 13 and 14 | `CHAMELEON/TONGUESTRIKE.WAV` in each level |

The new audit still flags Red Tail's kick and the Tiger Guard's two melee actions as lacking a dedicated effect reference. This alone does not prove a bug in original gameplay. No guessed voice recording or unrelated effect was automatically substituted for these attacks. Impact, blocking and damage sounds are separate from the attack's own effect.

## Actual output measurements

The opt-in `AudioProbe` counts nonzero samples and peak amplitude from SDL's existing post-mix callback. It neither records audio nor accesses the microphone. Music is muted and existing sound channels stopped in the isolated test; original phone config and saves are restored afterward.

- `attack-audio-mixer1`: idle was silent; Claw sword swish and gunshot produced nonzero samples. The enemy fixture accidentally selected a rat instead of the officer, so the whole run failed its expected-file assertion and is preserved as such.
- `attack-audio-mixer2`: officer and both chameleon effects were accepted and produced mixed output. The standing player attack randomly chose uppercut instead of swipe, so the specific sword assertion failed despite a valid melee sound. The revised test crouches to select duckswipe deterministically.
- `attack-audio-mixer3`: all checks passed. Idle output was zero; duckswipe, pistol, officer and both chameleons produced nonzero mixed samples with their expected effect requests. The probe preserves the existing music-audit callback.
- `boss-campaign-level4-audio` and `boss-campaign-level6-audio`: real boss melee requests included the newly connected WHIP1/UPPERCUT effect; both fights and next-level saves passed with explicit teleport/player-protection fixtures.

These measurements validate the game's generated audio, not the phone speaker, Bluetooth audio routing, system volume or a human listening test. No claim of full audio parity with the Windows original is made.

Po polsku: zamachy, wystrzały i trafienia mają odrębne dźwięki; głosy postaci mogą być losowe. Uzupełniono pięć brakujących przypisań do istniejących nagrań. Testy mierzą rzeczywisty sygnał z gry, a nie samą obecność pliku WAV.
