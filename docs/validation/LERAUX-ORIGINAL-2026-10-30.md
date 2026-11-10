# Le Rauxe original-behavior investigation

Date: 2026-10-30. Read-only static investigation by OpenAI Codex (LLM), prompted by an anonymous human report that the first boss blocks almost every hit and attacks too frequently.

## Scope and limits

The admitted target is the player-supplied CrazyHook-distributed x86 CLAW.EXE, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. It is not certified as a pristine 1997 release. REA with Ghidra 12.1.4 analyzed an immutable snapshot. This is behavioral interpretation of machine code, not original source, a Windows playthrough, or proof of encounter balance. Proprietary disassembly, decompilation, and input binaries remain private.

## Supported observations

| Observation | Interpretation and limit |
| --- | --- |
| Constructor `0x480cb0` loads the RAUX strike, advance, retreat/home, high/low hurt, and high/low block animations. | Blocking is a real part of this boss's implementation. Animation existence alone does not establish the rules deciding which incoming hits are blocked. |
| Boss Home update `0x481a60` samples a random integer modulo 121 and selects strike, forward/backward movement, or a jump-over helper according to a proximity classification. | The original decision loop is richer than unconditional repetition of one attack animation. Proximity meanings are inferred, not fully traced. |
| Shared Home continuation `0x44f210`, reached from that boss update, has a branch for classifications 3/4 that can strike or select a Home animation and call virtual slot `+0xac` with `rand % 301 + 300`. | This establishes an actual randomized 300–600 ms pause branch in the inspected executable. It does **not** establish that every original strike has a mandatory 300–600 ms cooldown. |
| Slot `+0xac` resolves to `0x440590`, which enters the named PAUSE state and stores duration and start time. | The preceding numeric range is a pause duration, not an unrelated damage value. |
| Boss hurt reaction `0x481810` calls `0x43f9a0` with 350, then selects high/low hurt or another reaction; `0x43f9a0` stores a duration and start time. | A 350 ms reaction-related timer exists. Its complete damage-gating use has not been traced here, so it must not be advertised as a fully verified invulnerability duration. |
| Boss hurt-state update `0x481ec0` can initiate another strike after the hurt animation's terminal condition. | Counterattacking after receiving a hit is supported. This does not prove that attacks should be blocked throughout every non-attacking state. |

## Recommendation

Correct independently reproducible implementation defects first. The port also unnecessarily reseeds the legacy global rand generator at attack entry; its Util::GetRandomNumber implementation uses an independently seeded mt19937, so that legacy reseed does not establish correlated parry rolls. A bounded randomized pause is better grounded than inventing a long fixed recovery delay, but applying 300–600 ms after **every** strike is still a documented port approximation rather than proven original timing parity. Keep it boss-specific and verify it in an actual encounter.

Do not claim that the port's 50% melee parry or 100% ranged parry matches the original: this focused analysis has not recovered the complete incoming-hit predicate. Do not broadly weaken all enemies or remove the boss's defensive identity based only on the reported difficulty. Establish standing, crouching, behind-the-boss, attack, and recovery behavior separately.

The public [Claw design document](https://ics.uci.edu/~frost/GameDesign/ClawDesignDoc.pdf) is historical design intent rather than runtime proof. Its partial projectile-blocking description cannot, by itself, determine the final executable's exact percentages.

## REA evidence index

- Constructor: `ev_3b621c15089cee39bb7be6702268d9fc364ff9599bae247776ba086dd81f7e85`.
- Boss Home: `ev_0a26ea186661fda08c508f8b17dc97fc433a806f2c497448f6e0a56ebe53a6d6`.
- Shared Home continuation: `ev_2696cc29a7e5431f28fd413f49a6f8458ed0bc3c5219f15bd0fd44e5b08f1a73`.
- Pause setter: `ev_69a5c8f8e4a7fc6fd654570b7683477ac2b0134498501821831afb48b5786986`.
- Boss hurt reaction: `ev_b48084fc784601d638cbbe99bf126af286fd456e64ebb896cfa53628d0ab9b04`.
- Reaction timer setter: `ev_4a7524f3924ad5c1b752b5d2de515e8d88961a13fc3efaca61f691865788eecf`.
- Boss hurt update: `ev_d13102535156c1d6775aaf6f34f5a207cbb616a53ab631ac686dea6d219b03ca`.

This index makes local analysis reproducible against the recorded target digest; it does not redistribute proprietary implementation text.

## Port correction and baseline

The current port's original LaRaux configuration had no attack delay and repeated its single strike animation whenever Claw remained close. A protected real-encounter fixture on debug35 recorded consecutive uninterrupted strikes about 0.35 seconds apart and ordinary crouching sword attacks reducing boss HP from 100 to 70. This disproves a blanket claim that the current port always blocks every attack; protection/teleport setup means it does not establish encounter fairness under normal damage.

Debug36 adds optional AttackDelay/MaxAttackDelay range support, enabled only for LaRaux at 300–600 ms. Each attack cycle receives a selected pause, including the first attack. It is intentionally a port cadence approximation of the observed original Home pause branch, rather than a full implementation of original movement choices or exact per-strike timing. Other actors keep their configured fixed delays. The boss range path does not reseed the random generator at each strike. Existing 50% melee and 100% ranged parry configuration is unchanged because original exact probabilities remain unresolved. On final debug36 APK `63478ba59d551d37ef9c1fffe3cf473287de09a4dc8c763eb213adc4eeb1c013`, the protected real-encounter test measured ten consecutive intervals from 0.707 to 0.932 seconds, median 0.8385 seconds. Ten ordinary sword taps reduced boss HP from 100 to 70; boss HP was never edited. This confirms the new cadence and damage path, not natural no-protection fairness or a complete boss victory. The test restored user files byte for byte.

REA initially rejected an obsolete `provider` argument and no-target requests; retry used the advertised `provider_id` schema. Unrecognized callback labels were kept as unresolved boundaries rather than invented pseudocode. The task-local session was closed cleanly and the original binary was not modified.
