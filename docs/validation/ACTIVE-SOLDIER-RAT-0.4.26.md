# Active Soldier/Rat

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-23. Exact debug APK SHA-256:
`f32e9e96e64b91dd12ea7eff0303a97ea3c7abf1d9b16fbe08f6fa4023a3cb1f`.
32 px isolated solid step, both sides and vertical relations, fresh process per
standing/jump/duck/escape action. Active AI, normal damage, no protection or
health edits during action. Setup HP100/pistol99; no pistol shots by the tester.

| Prototype/device | Cases | Observed target loss | Target defeats | Owner-source damage cases | Recorded hero death | Escapes airborne |
| --- | --- | --- | --- | --- | --- | --- |
| Soldier, Redmi Android 16 | 16 | 5 | 2 | 0 | 1 | 4/4 |
| Rat, Huawei Android 10 | 16 | 14 | 14 | 11 | 0 | 4/4 |

**Target loss is not proof of a successful Claw sword attack.** Rat explosion
source GUID matched the spawned Rat in eleven cases. Its 150x150 damage area can
hit the owner in this geometry. A follow-up with the updated parser again observed
Rat HP5 -> -45, source equal to its own actor ID. This verifies attribution, not
that self-damage is a game bug or different from original Claw. No balance change.
The parser now retains target ID, matching-name health/source events and an
owner-source flag, while preserving the meaning of the old target-loss field.

All 76 Soldier and 29 Rat recorded area contacts reported integer overlap. This
is not complete projectile collision coverage. Soldier projectile damage can
continue after a successful jump away; escape is not invulnerability.

The Soldier hero-above/right/standing case recorded Claw HP10 -> 0 after its
`final` state sample of HP20. Evidence includes screenshot capture after that
sample while active AI continues; snapshots and the full evidence window are not
atomic. Preserve both facts rather than replacing the event with a no-death claim.
Initial sampled Soldier HP was sometimes90 because a real hit preceded input.

Four separate Soldier escapes waited for a confirmed actual hit first. Input
started after sampled HP80; all four jumped and moved 246.6–341.1 px. Final sampled
HP70/70/60/50, no recorded death. Held jump+direction1000 ms, attack delayed450 ms;
not proof for every short tap/hurt-frame timing. The sample is subject to ADB
round-trip delay. No resources were replenished during an action.

Private evidence prefixes: `active-soldier32-redmi-0.4.26`,
`active-rat32-huawei-0.4.26`, `soldier-after-hit-huawei-0.4.26`, and
`rat-source-attribution-huawei-0.4.26`. Original config/save restored per case.
These37 cases do not certify all enemies/heights, natural stairs or original parity.
