# Ladder, edges and active heights / Drabiny, krawędzie i wysokości

OpenAI Codex (LLM), 2026-10-23. Huawei Android 10, debug 0.4.25 APK SHA-256:
`6175b1b450ca7f46ede0910a884e3608d104e4a86251822aa6c6b4a57d6ca955`.
Controlled fixtures only; the human retains natural campaign testing.

## Ladder and edges

`ladder-final-0.4.25` completed 73 state reads and 1001 trace samples. Assertions
passed for held Up at the real first ladder cap, release/re-press, Down entry,
jump off, return to climb from a solid bottom, leaving both ledges, rejection of
air jumps, and idle centres 1/5/20 px inside both edges. Inside-centre cases stayed
supported with less than 2 px drift. Outside-centre cases fell; this is not proof
of parity with original Windows Claw. Short sideways inputs during the ladder's
top transition sometimes remained in topclimbdown; they are observations, not a
claim that all interruption timings have been made identical to the original.

The cap/below-cap 100/250 ms jump matrix with no/left/right late input found no
grounded, stationary falling-animation streak lasting at least 300 ms. A single
transition frame remains a candidate, not automatically a bug. Natural geometry
can land on different ledges after rightward jumps. No new physics fix was applied.

**Metadata correction:** this running legacy helper hashed mutable local build
output at completion. A parallel 0.4.26 build changed that output while the phone
remained on 0.4.25. The raw JSON field is retained but must not identify the tested
package. `package-provenance.json` records the actual installed package above.
The helper now hashes the installed APK before mutations. Do not silently relabel
this evidence as a 0.4.26 runtime test.

## Active Officer, 16 and 64 px

Eight cases at each height, both sides, hero/enemy above, standing sword or
jump-away escape. Offensive AI and normal damage active; no health edits during
an action. Setup initializes HP100 and pistol99; no pistol shots were fired.

| Height | Higher | Side | Action | Hero HP lost | Enemy damage | Jump | Horizontal travel px |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | enemy | -1 | standing | 50 | False | False | 0.0 |
| 16 | enemy | -1 | escape | 20 | False | True | 274.6 |
| 16 | enemy | 1 | standing | 10 | True | False | 0.0 |
| 16 | enemy | 1 | escape | 10 | False | True | -285.8 |
| 16 | hero | -1 | standing | 50 | False | False | 0.0 |
| 16 | hero | -1 | escape | 10 | False | True | 341.8 |
| 16 | hero | 1 | standing | 20 | True | False | 0.0 |
| 16 | hero | 1 | escape | 10 | False | True | -341.7 |
| 64 | enemy | -1 | standing | 70 | False | False | -19.6 |
| 64 | enemy | -1 | escape | 10 | False | True | 242.5 |
| 64 | enemy | 1 | standing | 70 | False | False | 0.0 |
| 64 | enemy | 1 | escape | 10 | False | True | -307.7 |
| 64 | hero | -1 | standing | 50 | False | False | 0.0 |
| 64 | hero | -1 | escape | 10 | False | True | 340.7 |
| 64 | hero | 1 | standing | 10 | True | False | 0.0 |
| 64 | hero | 1 | escape | 10 | False | True | -341.4 |

All sixteen cases completed without hero death; all eight escape actions became
airborne and moved away. Standing attacks had mixed outcomes. At 64 px the
Officer's 130x50 attack area can still intersect the hero's tall body near the
feet. Claw's normal attack area is narrower, 50x25. This alone does not establish
a wrong hitbox. Hurt states can reject the short directional/attack input, leaving
the hero facing away; an issued input is not proof of an effective facing change.
Animation choice also includes random melee variants. Do not label misses as
collision bugs or left/right fairness failures without controlling these factors.

Every recorded contact in these cases reported integer AABB overlap. Requests
are kept separate from confirmed contacts and legacy body-creation logs.
Private prefixes: `active-officer16-huawei-0.4.25` and
`active-officer64-huawei-0.4.25`. Earlier [32 px trials](ACTIVE-OFFICER-0.4.25.md)
include actual-after-hit reactions. This remains partial active-enemy coverage,
not proof of all enemy/projectile/boss behaviour.

## Polski

Audyt drabiny zakończył się 73 odczytami i 1001 próbkami animacji. Trzymanie góry
na szczycie nie uruchamia wspinania. W próbach skoków przy szczycie nie wykryto
zablokowanej animacji spadania przez co najmniej 300 ms. Postać stojąca środkiem
1/5/20 px wewnątrz izolowanej krawędzi pozostawała podparta; środek poza krawędzią
może prowadzić do zsunięcia. Zgodność tego zachowania z oryginałem jest nieznana.

Dodano 16 prób aktywnego oficera na wysokościach 16 i 64 px. Wszystkie osiem
ucieczek oderwało bohatera od podłoża. Trafienia szablą były mieszane. Wąski zasięg
Pazura, stan otrzymywania obrażeń, zwrot postaci i losowy wariant ataku wymagają
oddzielnego traktowania. Nie zmienialiśmy balansu ani nie uznajemy tego za pełny
audyt wszystkich przeciwników. Błąd metadanych starego narzędzia opisano jawnie;
surowe wyniki i nieudane próby pozostają zachowane.
