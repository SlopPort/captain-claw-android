# Active Tiger Guard follow-up / Aktywny Tiger Guard

OpenAI Codex (LLM), 2026-10-22. Physical Huawei Android 10, ARM64 APK SHA-256 `cfc586439527bb6e4f063d4d6b7b526aa8fa64e2c9f44d6fccc7e7889c7672cf`. Report prefix `active-tiger-0.4.21`.

## Completed observations and aborted fixture

Actual level-14 Tiger Guard, normal health/damage, offensive AI and parry enabled. Each fresh process uses a prepared 48 px step in an isolated arena; setup initializes hero HP 100/ammo 99, with no HP edits during the action, no protection and no shots. Original configuration/progress restored.

| Enemy initially above | Hero damage after initial sample | Accepted hero animation | Horizontal displacement |
| --- | --- | --- | --- |
| Left, standing sword | 40 HP | none observed | -19.6 px |
| Right, standing sword | 30 HP | uppercut; enemy damage observed | +19.6 px |
| Left, jump/away/attack | 20 HP | jumpswipe | +219.6 px away |
| Right, jump/away/attack | 10 HP | jumpswipe | -219.3 px away |

Escape inputs hold jump/direction for 1000 ms and schedule sword at 450 ms. Trace samples show only 21.5/21.7 px upward displacement relative to the initial sample; `jumping=1` was not observed. Accepted jumpswipe does not establish a full-height jump. The hero moved away in both cases and survived the observation; that is not immunity to pursuit or indefinite safety. Tiger movement changed vertical separation during each live trial, so the initial 48 px step is not a constant body-height gap.

The next hero-above/left standing case failed the initial geometry gate before executing its measured action: the acrobatic enemy had already jumped above the hero during the status round-trip. The run aborted, preserving this failure and all four completed cases. No eight-case success or hero-above coverage is claimed. The test tool now additionally writes a structured `invalid-fixture.json` for future occurrences without weakening its assertion; this older failed case retains its original raw logs.

This records a sword command without an observed accepted attack animation in one case, and available away movement in the two escape cases. The missing animation requires further input/hurt-state analysis; its cause is not proved by this trace alone. It does not establish original-game parity, natural stair fairness or a general fix for stunlock. No AI, hitbox or damage change was made based on these incomplete observations.

## Polski

Z aktywnym Tiger Guardem dwie próby ucieczki dały około 219 px ruchu w bok, przy utracie 10/20 HP; bohater przeżył obserwację. Próby stania zakończyły się utratą 30/40 HP, a po jednej stronie nie zaobserwowano przyjętej animacji ataku. Skok nie osiągnął pełnej wysokości. Kolejny scenariusz przerwano, ponieważ przeciwnik zdążył wyskoczyć i nie zachował się żądany układ wysokości. To jawne ograniczenie próby, nie potwierdzenie błędu hitboxa ani zaliczenie całego audytu walki.
