# Natural checkpoint and menu reload — 0.4.24

OpenAI Codex (LLM) performed and documented this work. Status: **first persistent
checkpoint reached naturally; level 1 and the full campaign remain incomplete**.
APK SHA-256: `583ec1d605527ba812e7da3da510a52dc4e08a2cc94f84c4733592051f2cc0a2`.

The owned Redmi / Android 16 run starts from an isolated standard level-one save
(HP100, lives3, pistol10, magic5, dynamite3). Subsequent traversal uses ordinary
app-local SDL input and read-only observations: no teleport, invulnerability,
health/ammo edits, generated projectiles or added terrain. Ordinary deaths,
respawns, pickups and one End Life menu action are retained, not rolled back.

The run passed the early ladders, both routes around the first moving platform,
the vertical elevator, the second respawn flag, four static stone steps, the
next ladder, enemies and the real start elevator / lower ladder transfer.
An early lower-ladder attempt overshot and died; that failure remains recorded.
The corrected sequence first passed an explicitly controlled Huawei fixture,
then passed during the natural Redmi run. A controlled fixture is not counted
as natural traversal.

At the first persistent checkpoint the game emitted
`Pazur progress atomically saved` and wrote these values itself:

| Field | Saved and reloaded value |
| --- | --- |
| Level / checkpoint | 1 / 1 |
| Score | 43900 |
| Health | 100 |
| Spare lives | 0 |
| Pistol / magic / dynamite | 6 / 2 / 3 |

The natural collision position was approximately (6867.6,4991.6). The exact save
snapshot SHA-256 is
`6931269371ecc6bc82754bea9f4dd61953bfe5df41952f26b72313247ee38159`.
It is byte-identical to the file copied when the owned run ended. Original user
configuration and save files were then re-read and matched their backups byte
for byte. The ongoing continuation owns separate backups and restores them on exit.

The first resume-driver attempt used the debug new-level shortcut and therefore
started checkpoint zero; it was stopped without traversal and is not a reload
pass. The corrected driver starts the ordinary menu, chooses Load game, La Roca,
and checkpoint 1 using keyboard events. The supplied game-written XML is copied
unchanged. The engine places the hero near (6873,4991.6). Runtime observations
confirm HP100, lives0, pistol6, magic2 and dynamite3; the screenshot shows score43900.
Weapons are cycled normally and returned to the pistol. No position/resource
restoration command is used to obtain these results.

Local evidence (ignored, no game data or private device ids added to Git):
`reports/natural-campaign-0.4.24-run1`,
`reports/natural-campaign-0.4.24-resume1` (rejected driver attempt),
`reports/natural-campaign-0.4.24-resume2/normal-resume-proof.json`,
`reports/cavity-huawei-0.4.24-r1` (controlled transfer fixture).

Open observations: getting hit on the first moving platform was followed by
losing support and falling. This needs a controlled reproduction and comparison
before changing gameplay. A missed fourth stone step led into a lower pocket;
this was a route error, not established as a physics bug. The checkpoint write
also produced a logged 61.9 ms frame, so these diagnostics do not establish a
55/60 FPS minimum. Remaining maps, bosses and final ending are still release gates.

## Further continuation

The ordinary continuation crossed the crumbling pegs at x7502,7631,
7758 and reached the static catwalk near x7900 with HP100. The observer initially
re-read older support samples and falsely reported a bad landing; consuming each
sample only once fixed this test-tool error. A subsequent natural repetition
also crossed all four landings with HP100. No platform timing or collision was
changed. The continuation defeated the catwalk Officer with a normal pistol shot
and climbed the x8224 ladder. It later lost its last life under enemy fire; this
failure is retained in `natural-campaign-0.4.24-resume3`, not counted as a pass.

The suspected ladder-jump failure was separately observed without enemies
(`ladder-jump-redmi-0.4.24-r1`): ordinary ascent ended at (8224,4104.6), climb=0,
ground=1. A normal 600 ms jump with 650 ms right movement took off after 31 ms,
rose 155 pixels and landed at (8448.8,4114.6), ground=1. The earlier natural
1700 ms right input ran past the short upper catwalk and fell onto the lower one.
This evidence does not justify a physics change. The isolated fixture removes
enemies and sets HP100/ammo99 before initial placement; it is not a campaign pass.

The fourth continuation repeated the real peg crossing, boarded the y4182 moving
platform and reached the next ledge near (9063,4114), HP60. It then died to repeated
Officer hits near (9094,4114). Input acceptance under hurt recovery remains an
open combat-fairness check; the loss is not hidden and level 1 remains incomplete.
No invulnerability, recovery, reach or enemy timing parameters were changed.
Local evidence: `natural-campaign-0.4.24-resume4`.

## Later route attempts

The fifth ordinary continuation defeated the next Officer by firing from the
moving platform, reached x9236 with HP70 and boarded the second carrier. A late
jump began at x9606.8, outside the ladder column x9568; it fell and reached Game
Over. This is retained as a failed route, not a ladder-collision fix.
The sixth continuation instead held Up early and attached to that ladder:
HP60, x9568, y3548. The helper stopped its test 19.4 pixels below the cap because
it did not allow enough held-input time for both the carrier return and ascent.
It restored the user files; this is a test-duration failure, not a death or a
completed ascent. The seventh attempt died to a Soldier before this transfer:
a requested pistol action during hurt recovery had not defeated it. Blindly
continuing after a requested attack is therefore not a reliable route controller.
The game APK was unchanged throughout these attempts.

`second-carrier-ladder-redmi-0.4.24-r1` separately confirms the ordinary early-Up
sequence reaches x9568,y3528.6, HP100 in an explicit controlled fixture. The
reusable observer now allows three two-second Up holds, accounting for variation
in the platform's return timing. This fixture removes enemies and initializes
HP100/ammo99 before initial placement. It is not natural campaign completion.

The eighth natural attempt confirmed a Soldier defeat before departure but again
missed the second ladder after boarding. The controlled landing offset was not
representative of every natural state: a real catnip pickup changes movement
speed. The helper's status-query round trips also allowed the carrier to move
past the sensor before Up began. The observer now presses Up during the boarding
jump, rather than waiting for post-landing queries. Controlled candidate r3
(`second-carrier-ladder-redmi-0.4.24-r3`) reaches the cap at (9568,3528.6), HP100.
This is still not a complete natural-route or campaign pass. Earlier r1/r2
controlled passes remain evidence only for their own fixture and input timing.

## Natural ninth continuation

The corrected ordinary sequence now passes in the natural run too:
`natural-campaign-0.4.24-resume9/second-carrier-natural-ladder.json` records HP60,
x9568,y3528.6 at the ladder cap. The following ordinary left jump boarded the
real x9442 vertical elevator. Riding it and a short jump with held Up reached
the next ladder cap x9568,y2440.6, HP30 (`tower-transfer.json`). The next Soldier
subsequently killed the hero; the attempted longer jump/shot did not survive.
Level 1 remains incomplete. This is incremental natural route coverage, not a
single uninterrupted clear, all-level pass, FPS guarantee or 1.0 release.
After ending this owned run the real device configuration and save were pulled
again and matched both original backups byte for byte (`restoration.json`).

[Huawei continuation and log-reader recovery](HUAWEI-CAMPAIGN-0.4.24.md).
