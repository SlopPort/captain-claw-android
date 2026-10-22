# Vertical combat follow-up / Walka na różnych wysokościach

Requested 2026-10-22, after the current campaign/compatibility work. Prepared by OpenAI Codex (LLM). This is a test plan, not completed evidence.

Existing 0.4.2 combat tests and the level-one officer/stairs report provide starting evidence, but do not establish fairness for every vertical offset. Use actual attack contacts and active body bounds; proximity alone does not establish a hit.

| Dimension | Required cases |
| --- | --- |
| Relative height | Same floor; hero above and below at 16/32/48/64 px; offsets near actual attack/body boundaries |
| Side | Enemy on left and right; repeat after facing change |
| Hero state | Standing sword, crouched sword, ascending/descending jump sword; gun and magic where relevant |
| Enemy state | Idle, approaching, attack, recovery, blocked/hurt; relevant melee and projectile archetypes |
| Geometry | Controlled solid steps first; real stairs, platform lips and nearby ladders afterward |
| Outcome | Player/enemy HP delta, attack frame/area, active hurt-body bounds, animation/state, source identity and escape/counterattack opportunity |

Run enemies in their own source levels so their original animation events and recordings resolve correctly. Preserve user config, saves and controller bindings. Isolated geometry, teleports, protection or spawned actors must be labeled. Protection can observe attack attempts but cannot demonstrate normal damage or stunlock escape. Repeat actual-damage cases without protection.

Separate expected misses from bugs: a sword area that does not overlap the body should miss; a foot-support sensor must not count as the hurt body. Do not enlarge reach or normalize all enemy attacks solely to make higher/lower characters hit each other. Investigate asymmetry, invalid sensor hits, repeated damage and an enemy able to hit while the hero has no practical counter/escape. Compare disputed behavior with original-game evidence before changing balance.

Preserve failures, traces and APK identity. Original game observations, design-document descriptions and OpenClaw/new-code decisions must be reported separately. No claim is made that original Monolith source code is currently available in this repository.
