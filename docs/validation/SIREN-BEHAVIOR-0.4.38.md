# Siren behavior reconstruction in debug 0.4.38

Adaptation and review by OpenAI Codex (LLM), guided by anonymous human requirements. Upstream authorship remains separate.

## Evidence and implementation

The supplied CrazyHook-distributed CLAW.EXE has SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`; it is not certified pristine. This is executable analysis, not recovered original source or observed original-Windows gameplay. The previous [custom-event report](ORIGINAL-CUSTOM-EVENTS-0.4.37.md) records the REA bindings; private bounded inspection of entry `0x48d640` and update `0x48d7b0` supplies the following behavior:

- First note at image 202 (zero-based strike1 frame 1), without the former arbitrary 500 ms pre-animation delay.
- At most four projectiles, with 300 ms between emissions. Slow updates emit at most one projectile, without a catch-up volley.
- A 4000 ms entry gate starts at the first note, rather than adding that delay before every projectile.
- Singing ends according to the singing sound's duration; an ANI loop cannot restart a burst. Hurt/death cancels pending notes while retaining recovery.
- Projectile origin is 28 pixels ahead and 10 pixels above the owner; horizontal speed is 200 pixels/s in either direction. The port converts this explicitly to 200/75 physics units and avoids the generic left-projectile XML helper's integer truncation.

These rules are opt-in XML settings on level 11 Siren, inherited by level 12. Other ranged enemies keep their existing policy. Timers advance with game updates, so pausing does not consume recovery. Cooldown expiry wakes a patrolling Siren, without interrupting a hurt or parry state.

An independent source review caught the missing expiry wakeup before device validation; it was corrected. Duration lookup uses the resource cache, and the current prototype has exactly one singing sound. Missing/undecodable audio yields zero/negative duration and early state termination; no invented minimum singing length was added. Exact original handling of damaged/custom asset sets is not certified.

## Validation boundary

See [update results](UPDATE-0.4.38.md) for exact tested artifacts and physical results. The reproducible [Siren test](../../tools/siren_behavior_smoke.py) uses an isolated fixed-patrol arena, temporary player protection and both facing directions for both inherited level variants. It checks burst size/order, spacing, recovery and launch geometry; it is not campaign traversal, original-Windows timing measurement or a fairness test.

The first device attempt exposed a fixture-only assertion: a zero patrol speed requires IsAlwaysIdle. The fixed arena now sets both values in memory, without changing installed game prototypes or user saves. The failed attempt is retained privately; restoration ran after it.
