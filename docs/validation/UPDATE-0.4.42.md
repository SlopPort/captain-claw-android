# Debug 0.4.42: input after actual enemy damage

Prepared by OpenAI Codex (LLM), 2026-11-08. This is a diagnostic development build, not a new public release or a natural campaign acceptance result. Public downloads remain [0.4.41-test](RELEASE-0.4.41.md).

## Artifact and change

The corrected ARM64/ARMv7 debug APK has versionCode **54**, versionName **0.4.42-dev**, SHA-256 `2af60b03c18d393bb632080507c90f7d3ac8ccd90c0f3bb91f61367ab66f29ad`. Huawei P9 Lite with LineageOS Android 10 ran ARM64. ARMv7 was built and inspected, not runtime-tested in this batch.

`combatjumpafterhit <hold_ms> <sword_delay_ms> <left|right>` arms an opt-in watch on the current hero. After observed health loss, it sends ordinary SDL jump/direction inputs and an optional delayed sword through the existing diagnostic scheduler. It does not manufacture damage, recovery or attacks, and changes no gameplay recovery, reach, immunity, jump height or input priority. The watch cancels on pause, owner replacement, death or timeout. These cancellation branches are code-inspected, not yet all runtime-exercised.

An initial diagnostic APK (`75a89df735e280d26773e6bacc6fc8f4edaf2d5d785e56c15abaf5a2ed9fa338`) exposed a measurement bug: the poll timestamp preceded input emission, so unsigned elapsed time could underflow and finish the trace immediately. Its four zero-duration traces are **invalid movement evidence**. The corrected trace samples time after emission; the driver now rejects missing/invalid hold durations. Failed evidence remains private in `todo-hurt-jump-order-0.4.42`; corrected results are in `todo-hurt-jump-order-0.4.42-r2`.

## Controlled results

An active level 1 Soldier stood 32 px above the hero on an isolated step. Each case used a fresh process, setup HP100/ammo99, and no protection/healing during the action. Input began after an actual Soldier hit; USB command latency did not determine its position within the hurt animation. Direction was right in these four cases. This is not a natural staircase, physical touch latency test or original-game comparison.

| Requested jump hold | Sword delay | Recorded hold | First upward motion | Maximum rise | Enemy at final query |
| --- | --- | --- | --- | --- | --- |
| 250 ms | None | 261 ms | None | 0.0 px | Alive |
| 250 ms | 80 ms | 252 ms | None | 0.0 px | Defeated |
| 700 ms | None | 720 ms | 363 ms | 88.7 px | Alive |
| 700 ms | 80 ms | 712 ms | 631 ms | 72.6 px | Defeated |

Short input ended during hurt. Longer held input produced upward motion in both cases. In the long sword case the buffered attack was consumed 324 ms after input, the Soldier died at 415 ms, and upward motion began at 631 ms. This demonstrates an observable ordering in this port: recovery and a standing attack can delay upward motion while jump remains held. It does not establish the original timing or justify silently changing attack/jump priority. Each row is one observation; attack variants and encounter phase were not identical randomized controls, so the difference between rows is not a universal causal delay.

All four protocol runs restored fresh configuration/progress byte-for-byte and reported no target or unattributed fatal crash. Protocol success does not mean every action won, the encounter is balanced, or COMBAT-01/02 are complete. Natural stair geometry, both facings, other offsets/projectiles and original recovery policy remain separate requirements.

## Installation and static checks

The initial debug41-to-debug42 update passed without uninstalling and preserved seven external game/configuration/progress files. Installing the corrected APK at the same version also preserved those seven files. Neither snapshot contained private preference XML, so existing private preferences were **not** tested. Private reports: `todo-upgrade-0.4.42` and `todo-reinstall-0.4.42-r2`.

The corrected APK passed known-pattern privacy checks (375 members), both-ABI packaging/ELF checks, and the source patch consistency check. These do not certify arbitrary assets, physical 16 KB ARM hardware or the separately signed public production package. Build output is retained privately in `todo-debug42-rebuild.log`.

## Unarmed diagnostic regression

The corrected exact APK passed the sequential `touch-jump`, `game-over`, `save-errors` and `ambient` cases on Huawei. The runner verified fresh configuration/progress restoration and unchanged installed APK after every case. Private report: `todo-regression-0.4.42-r2/results.json`. The jump trace recorded one upward cycle for each of six normal fixture inputs, including short, long and drift cases. These are bounded app-local inputs, not a physical multitouch or controller test. No previous debug41 emulator/menu/boss result is automatically transferred to debug42.
