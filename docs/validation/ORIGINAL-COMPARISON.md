# Original-game comparison / Porównanie z oryginałem

Scope checked by OpenAI Codex (LLM), 2026-10-22. Detailed behavioral comparison remains future work after the current release-gate tests.

## Source provenance

- [pjasicek/OpenClaw](https://github.com/pjasicek/OpenClaw) describes itself as a reimplementation of Captain Claw. Its GPL source is our engine baseline, not original Monolith source.
- [Claw Recluse technical support](https://captainclaw.net/en/support.html), maintained by the Claw/CrazyHook community, states that original Claw source is not publicly available and explains why CrazyHook uses injection instead. This is attributed evidence, not proof that no private copy exists.
- The user's local installation provides the original executable, archives, level objects, animation events, recordings and related material. Data and observed behavior can be compared; those files are not automatically source code or open-source distributable assets.
- Original design documents describe intent at their revision date. They can differ from shipped gameplay. New reconstructed timings, damage gates and encounter parameters must be labeled as such.

No original Monolith C/C++ source has been established as available to this project. Do not present a source diff against OpenClaw as a diff against the original game. If purported original sources are found later, establish provenance and terms before adopting them or changing attribution.

## Evidence to collect

Compare the same version, map location, difficulty, action and relative geometry. Record jump tap/hold trajectories, ladder attach/leave/top behavior, platform edges, vertical-offset attacks, damage/recovery/invulnerability, enemy reach and boss sequences. Keep original-game observations separate from OpenClaw source behavior and this adaptation's changes. Timing comparisons need controlled frame rate; a video or a design paragraph alone is not exact timing proof.

Track each finding as confirmed match, measured difference, intentional adaptation or unknown. Preserve original recordings/art outside public source and APK; report measurements and source references instead. Never claim the entire port matches the original from a few successful encounter tests.

Po polsku: porównamy zachowanie oryginalnej gry z portem i osobno sprawdzimy różnice względem OpenClaw. Nie mamy potwierdzonego dostępu do oryginalnego kodu Monolith, więc nie obiecujemy porównania linia po linii z tym kodem.
