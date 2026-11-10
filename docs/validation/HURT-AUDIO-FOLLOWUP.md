# Configured enemy hurt voices: follow-up

Prepared by OpenAI Codex (LLM), 2026-11-08. This investigation addresses AUDIO-01. It does not establish original-game audio timing or a complete human listening pass.

## Source and data findings

In debug42's source, `EnemyAIComponent` loads `SoundType="TakeDamage"` entries, but the ordinary health-change path and `TakeDamageAIStateComponent` do not play that list. Nonfatal health loss enters the hurt state and plays a generic impact sound. Fatal damage uses a separate configured death list. Hero hurt already selects its own voice list.

The extended `tools/audit_attack_audio.py` accepts `--apk` so a preserved exact artifact can be inspected while a newer build is being prepared. It resolves the packaged prototype inheritance using the existing audit merge. For APK SHA-256 `2af60b03c18d393bb632080507c90f7d3ac8ccd90c0f3bb91f61367ab66f29ad` with the locally supplied Polish assets:

- 33 inspected enemy prototypes configure a hurt voice and a standard hurt-animation entry.
- 32 corresponding animation files were available; none contained sound events duplicating the configured voice.
- The remaining Marrow Parrot entry names `NONE.ANI`, a placeholder rather than a verified decoded animation. Its custom behavior is not certified by the ordinary Soldier fixture.
- The selected Soldier's `HITHIGH`, `HITLOW` and `KILLFALL` files contained no sound events.
- The existing attack inventory found 75 action rows, no missing referenced sound files, and two definitions with no sound reference: Red Tail `STRIKE8` and Tiger Guard `STRIKE1`. Silence in a definition is not proof that replacement audio should be invented.

These are static findings, not proof that every configured voice reaches the speaker. Private metadata: `todo-audio-inventory-0.4.42/results.json`. Proprietary recordings and raw assets are not included in the repository.

The later availability audit also found 23 prototypes referencing absent hurt files: 22 used the legacy generic `LEVEL1/SOUNDS/HIT1.WAV` placeholder and one used Red Tail's incorrect directory. The correction therefore filters already-covered generic impacts rather than requesting those placeholders, and fixes Red Tail's data reference. The other ten configured hurt-file sets existed in the supplied data. This is not a claim that every set has been exercised at runtime.

## Bounded correction and test

The Android patch plays the existing configured voice list once when the ordinary hurt state is entered. Generic impact names and the missing legacy placeholder are filtered because the health-change path already emits its impact. An empty list remains silent. Red Tail's existing hurt-file reference now includes its `REDTAIL` directory. No audio files are added and damage, recovery, immunity, AI timing and the fatal-hit branch remain unchanged. Original runtime parity remains unverified.

`tools/hurt_death_audio_smoke.py` is prepared to check actual sword contacts with a passive 10 HP Soldier: crouched hits must cause 10-to-5 and 5-to-0 health changes, with the expected hurt/death request and nonzero mixer output. A separate active Soldier must cause a real nonfatal hero hit and the corresponding hero voice. Passive-target setup isolates outgoing audio and does not establish active combat balance. `--expect-missing-enemy-hurt` explicitly records the old missing-request baseline; it is not a passing fixed-game result. Hero death and subjective listening are separate coverage.

November 10 runtime follow-up: [exact debug43 evidence](UPDATE-0.4.43.md) records the reproduced debug42 missing voice, successful fixed Soldier hurt/death and hero-hurt cases, and an Officer check with one generic impact and no missing-placeholder request. The upgrade preserved checked user files. Later actual fatal hero damage produced the current death cue once and normal respawn; actual Red Tail arena damage produced the corrected hurt voice once. Original death-cue policy, wider family coverage and subjective listening remain open. The saved debug42 20-minute observation passed separately; it is not debug43 stability acceptance. See the [current release checklist](../RELEASE-1.0-CHECKLIST.md).
