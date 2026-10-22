# Above/below standing-sword baseline: 45 prototypes

OpenAI Codex (LLM), 2026-10-22. Exact ARM APK `873c23510c180ae3899730fef27cd35204b1f75171afcce92b2291e446247638`. These are controlled fixtures, not an active-combat fairness pass or a natural campaign.

All **180 cases / 45 prototypes** completed in 3050.4 seconds on Huawei Android 10, with fresh processes and original config/save hashes restored after every prototype. Every case created an attack area; no fatal marker was found in the retained logs. There were **130 contacts with the target**, **117 observed HP decreases**, **32 defeats**, **50 cases without a target contact**, and **13 contacts without HP decrease**. The table reports HP loss, not whether geometric contact occurred. Maximum HP values observed were 5, 10, 20, 25, 30 and 40.

Setup uses an isolated configured 48 px step, initializes hero HP to 100 and pistol ammo to 99, disables protection, and removes offensive attack/roll states while keeping collision, damage auras and parry. No health edits occur during the observed actions, no pistol shots are fired. Aerial/swimming actors may float relative to the step; the actual body-bottom separation is reported rather than silently calling every separation 48 px. This does not test their natural flight/swimming behavior or ordinary map stairs.

The 13 contact-without-HP cases occur on CrazyHook variants (levels 9/10), RedTailPirate variants (7/8/13), TigerGuard and HermitCrab. Parry/resistance is retained, so these must not be relabeled as hitbox misses. Source review found a 33% melee-parry setting for the selected RedTailPirate/TigerGuard/CrazyHook variants; the old logs do not directly identify every resistance decision. New diagnostic tracing is being used in separate follow-up cases without changing those chances or RNG calls. Directional HP asymmetry in four prototype rows remains an observation, not a confirmed direction bug.

Po polsku: ukończono 180 prób obejmujących wszystkie 45 wariantów, po obu stronach i przy obu relacjach wysokości. Kontakt szabli wystąpił w 130 próbach, spadek HP w 117. Trzynaście kontaktów bez obrażeń wymaga rozróżnienia parowania/odporności, a nie powiększania hitboxów. Scena ustawia przed pomiarem 100 HP i 99 nabojów; nie zmienia HP podczas akcji. Ofensywne stany AI są wyłączone, parowanie i obrażenia kontaktowe pozostają. To nie pełne aktywne walki ani przejście kampanii.

Legend / legenda: **damage** = target HP decrease or defeat observed; **no damage** = no decrease observed, including possible parry. Left/right refers to the enemy's position relative to the hero. Actual body-bottom gaps are measured from recorded AABBs.

| Variant | Initial max HP | HP loss, enemy above: left/right | HP loss, hero above: left/right | Actual body-bottom gap px |
| --- | ---: | --- | --- | ---: |
| Level10_CrazyHook | 30 | damage / damage | no damage / no damage | 48–48 |
| Level10_PegLeg | 20 | no damage / no damage | damage / damage | 48–48 |
| Level10_Seagull | 5 | no damage / no damage | damage / damage | 21–75 |
| Level11_Fish | 5 | no damage / no damage | no damage / no damage | 9–87 |
| Level11_Mercat | 30 | no damage / no damage | damage / damage | 48–48 |
| Level11_Siren | 30 | no damage / no damage | damage / damage | 48–48 |
| Level12_Fish | 5 | no damage / no damage | no damage / no damage | 9–87 |
| Level12_Mercat | 30 | no damage / no damage | damage / damage | 48–48 |
| Level12_Siren | 30 | no damage / no damage | damage / damage | 48–48 |
| Level13_BearSailor | 30 | damage / damage | damage / damage | 48–48 |
| Level13_Chameleon | 20 | damage / damage | no damage / no damage | 47–51 |
| Level13_RedTailPirate | 25 | no damage / damage | no damage / damage | 48–48 |
| Level14_Chameleon | 20 | damage / damage | no damage / no damage | 47–63 |
| Level14_TigerGuard | 40 | no damage / damage | no damage / damage | 48–48 |
| Level1_Officer | 10 | damage / damage | damage / damage | 48–48 |
| Level1_Rat | 5 | damage / damage | no damage / no damage | 32–63 |
| Level1_Soldier | 10 | damage / damage | damage / damage | 48–48 |
| Level2_Officer | 20 | damage / damage | damage / damage | 48–48 |
| Level2_PunkRat | 5 | damage / damage | no damage / no damage | 48–48 |
| Level2_Soldier | 20 | damage / damage | damage / damage | 48–48 |
| Level3_CutThroat | 25 | damage / damage | damage / damage | 47–48 |
| Level3_Rat | 5 | damage / damage | no damage / no damage | 48–48 |
| Level3_RobberThief | 20 | damage / damage | damage / damage | 48–48 |
| Level4_CutThroat | 25 | damage / damage | damage / damage | 48–48 |
| Level4_Rat | 5 | damage / damage | no damage / no damage | 31–48 |
| Level4_RobberThief | 20 | damage / damage | damage / damage | 48–48 |
| Level5_Seagull | 5 | no damage / no damage | damage / damage | 21–75 |
| Level5_TownGuard1 | 20 | damage / damage | damage / damage | 48–48 |
| Level5_TownGuard2 | 25 | damage / damage | damage / damage | 48–48 |
| Level6_Rat | 5 | damage / damage | no damage / no damage | 34–49 |
| Level6_Seagull | 5 | no damage / no damage | damage / damage | 21–75 |
| Level6_TownGuard1 | 20 | damage / damage | damage / damage | 48–48 |
| Level6_TownGuard2 | 25 | damage / damage | damage / damage | 48–48 |
| Level7_BearSailor | 30 | damage / damage | damage / damage | 48–48 |
| Level7_HermitCrab | 5 | no damage / no damage | no damage / no damage | 48–48 |
| Level7_RedTailPirate | 25 | damage / damage | no damage / no damage | 48–48 |
| Level7_Seagull | 5 | no damage / no damage | damage / damage | 21–75 |
| Level8_BearSailor | 30 | damage / damage | damage / damage | 48–48 |
| Level8_GabrielPirate | 25 | damage / damage | damage / damage | 48–48 |
| Level8_PunkRat | 5 | damage / damage | no damage / no damage | 48–48 |
| Level8_RedTailPirate | 25 | damage / no damage | damage / no damage | 48–48 |
| Level8_Seagull | 5 | no damage / no damage | damage / damage | 21–75 |
| Level9_CrazyHook | 30 | damage / no damage | damage / damage | 48–48 |
| Level9_PegLeg | 20 | no damage / no damage | damage / damage | 48–48 |
| Level9_Seagull | 5 | no damage / no damage | damage / damage | 21–75 |
