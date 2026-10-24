# REA comparison: combat and jump semantics

Date: 2026-10-24. Investigation by OpenAI Codex (LLM), guided by anonymous human
reports. This extends [the initial REA notes](ORIGINAL-BEHAVIOR-REA.md), using the
same player-supplied CLAW.EXE and its recorded SHA-256. It is static executable
analysis, not recovered original source or a Windows runtime test. Proprietary
code and raw analysis stay private; this document records behavioral facts only.

## Confirmed differences and their implications

| Topic | Inspected executable | Port through 0.4.31 | Interpretation |
| --- | --- | --- | --- |
| Catnip sword bonus | Ordinary attack damage 5 becomes 10; crouch 2 becomes 4 | Ordinary 10, crouch 5, but Catnip sets either to 100 | Inherited OpenClaw behavior strongly over-amplifies the bonus. Android 0.4.32 changes only the bonus to double the existing base: 20 standing, 10 crouched. Base balance is retained. |
| Soldier health | Constructor selects base 3 on level 1, 7 otherwise, then applies a float multiplier | Public prototypes use 10 on level 1, 20 on level 2 | Raw HP alone is misleading; compare the number of successful hits. |
| Soldier damage | Constructor writes base damage 10, then a multiplier | Melee and projectile prototypes use 10 | Constructor values do not establish every attack's collision or timing. |
| Holding jump | Jump begin starts a 250 ms sustain counter; jump update cancels it on release and otherwise decrements it while applying upward motion | Height-limited hold plus release clamp; touch/controller add different minimum hold accommodations | Original variable-height jumping is supported by code evidence. Exact trajectory equivalence is unproven. |
| Receiving a hit | Hurt update can translate horizontally using the actor's existing X velocity and elapsed time | Inherited hurt handling disables gravity and zeros velocity; computed knockback application is commented out | Confirmed difference worth reproducing on natural stairs. Exact original hit-entry impulse and immunity timing remain unresolved. |

The level-1 and level-2 initialization routines both set the health/damage factors
to 1.0. At those constructor defaults, original standing hits needed are 1/2,
versus port 1/2; crouched hits are 2/4 in both. This arithmetic does not prove
encounter parity, but explains why simply replacing port HP with 3/7 would be
wrong. Runtime cheats, later modifications and other enemy types are outside
that comparison. Global `0x5360ac` is assigned the level number by the level
initializer; it must not be mislabelled as a difficulty setting.

## Runtime check of the inherited Catnip value

Huawei ARM64 debug31, APK
`c31507c5541f3c94675b7563337dc151ac3b5cafde6b9e131b69401349d1c8cc`,
produced real sword contacts and actual Soldier health changes:

| Action | Damage | Target HP before/after |
| --- | ---: | --- |
| Standing | 10 | 10 to 0 |
| Crouching | 5 | 10 to 5 |
| Catnip standing | 100 | 10 to -90 |
| Catnip crouching | 100 | 10 to -90 |

These are passive test targets, not campaign traversal. Each case uses a fresh
process. Earlier harness attempts used an unknown key name and did not attack;
a reused arena also removed attached sparkle actors and caused a diagnostic
assertion when enabling Catnip. Those failures are retained privately and are
not labelled natural gameplay bugs or successful damage measurements.

## Other source findings requiring separate tests

- Generic enemy hurt XML contains `InvulnerabilityTime`, but the inherited generic
  state does not parse it. Soldier values are zero; some bosses have separate
  logic. A field in XML is not proof that it protects an actor at runtime.
- Soldier has no parry state. Missing sword contact must not automatically be
  explained as a random parry.
- Hero ordinary melee/projectile damage uses the same 500 ms immunity gate;
  death tiles are an exception. This is a port value, not a verified original one.
- Catnip updates port running speed immediately, but its jump-height cap is copied
  when not already jumping. Mid-air pickup/expiry parity remains unresolved.
- The generic physics zero-displacement branch has an impossible nested positive
  displacement check. It deserves a targeted animation reproduction, not a blind
  change or an assertion that it caused every observed falling animation.

## Evidence ledger

- Soldier constructor `0x48dd90`: `ev_774d929b2f2e38aedc93530535facf2882f4e2488feeea877422051284d48bbb`.
- Raw instructions preserving float multiplication omitted by decompiler display:
  `ev_7e1e8a5696c65e9baab44b6d5ea78a390277a949604a5e79d17dd8a0b4f3642e`.
- Static scalar data (1.0 values): `ev_580bd9f6921bcd1cae03f3831549518147ba646791cbbbe6a7133edbf2a1efd8`.
- Level-number initializer: `ev_32a3f704d9a744753ef68bd3025588da162f0ac35fe504ea553e8f4c728bbc93`.
- Level-1 factors: `ev_784324e2a3433db251b9775d309bbc5b1632ba4d35e9a6e243691a23e9f7c844`.
- Level-2 factors: `ev_2ea6394af470c4a4b0ccd9b527af18f359e0a22068f393fefd98e5e7f6ac53f7`.
- Catnip attack construction: `ev_4dac6420a6262ee02313141af6508d5c51f0bd4ba144a87068a3552d9b1717bf`.
- Hurt motion/recovery: `ev_e6476c5e0f4e7bd0d5e05de83b28842e6c65c18314fc07c6590979739ddce418`.
- Jump begin: `ev_7af2052c3e270d9ffe4a78d23b8354df9f0ba0dfa42873786092bfee0e6dd77b`.
- Jump update: `ev_bde50c17feffe407fbd2ed890e41704c47cd355dc48949c08bb463696e52f347`.

Port comparison locations: ControllableComponent::OnAnimationFrameChanged /
OnHealthChanged; PhysicsComponent::VUpdate; Soldier actor prototype XML;
Converters::CreateActorData; generic TakeDamageAIStateComponent. The 100 damage,
hurt freeze, 500 ms immunity and unused generic immunity field were present in
the pinned upstream OpenClaw source, not introduced by the Android adaptation.
