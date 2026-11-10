# Original custom attack events: 0.4.37 follow-up

OpenAI Codex (LLM) checked the ten configured actions which have no ANI event-1 marker in the [0.4.36 inventory](ENEMY-ATTACK-INVENTORY-2026-10-30.md). All their ANI word-6 values are zero, rather than another common event number. Their original handlers must be checked individually: the absence of a shared marker does not itself indicate a broken attack.

Analysis used [REA](https://github.com/morluto/rea), Ghidra 12.1.4 and bounded Capstone instruction inspection of the supplied CrazyHook-distributed x86 executable, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. This executable is not certified pristine. Original source code was not recovered; no original-Windows runtime measurements were made. Proprietary assets, pseudocode and raw instruction evidence remain private.

## Coverage and decisions

Indices below are zero-based. An image identifier is the original ANI image ID, not an event marker. Matching a damage-onset image does not prove matching damage duration, complete AI, hit acceptance or repeat cadence.

| Family / configured actions | Original custom behavior recovered | Port comparison / decision |
|---|---|---|
| Siren, levels 11 and 12, ranged strike1 (2 actions) | Singing callback `0x48d7b0` detects image **202**, starts its singing/burst flag, sets a 4000 ms attack-entry cooldown and emits up to four SirenBullet projectiles with 300 ms spacing. ANI strike1 image 202 is index **1**, at nominal offset 180 ms. | Port previously selected index 2, offset 280 ms. Aligning its first projectile to **index 1** corrects a supported 100 ms animation-phase difference. The port still fires one projectile per attack and uses its existing delay; burst/repeat policy remains an explicit approximation. |
| Red Tail, level 13, melee strike8 (1 action) | Kick entry `0x4836b0` selects constructor field +0x4a0, bound to strike8. Kick callback `0x483780` exposes the attack rectangle on image **402**. | strike8 image 402 is index **1**, matching the port. Preserve this frame. The original rectangle stays active through its state rules; a port transient hitbox is not certified equivalent. |
| Red Tail, level 13, ranged strike4 (1 action) | Gun entry `0x483ae0` selects field +0x494, bound to strike4. Gun callback `0x483c70` emits one RedTailBullet on image **209**, guarded by a per-state flag. | strike4 image 209 is index **3**, matching the port. Preserve this frame. |
| Tiger Guard, level 14, low strike1 (1 action) | Knife entry `0x498ca0` selects strike1 via +0x338. Knife callback `0x498de0` exposes its damage rectangle on image **202**. | strike1 image 202 is index **1**, matching the port low attack. This does not prove the port's player-crouch selection rule matches the original move selection. |
| Tiger Guard, level 14, standing strike2 (1 action) | Original constructor `0x497e30` loads strike1 and strike3 for its attack fields. Its custom attack selection chooses knife/lunge/front-flip paths, rather than a simple standing/duck pair. No direct use of strike2 was established in this pass. | Preserve the configured port frame **2** pending reconstruction of the complete move set. Its similarity to artwork or another image ID is not sufficient to claim original parity. |
| Aquatis body, level 12, strike1 (1 action) | High-punch entry `0x405770` loads +0x490, bound by constructor `0x404d80` to strike1. High-punch callback `0x4057d0` exposes a punch rectangle on image **204**. | strike1 image 204 is index **3**, matching the configured body attack. Preserve this frame. Separate native tentacles, arena activation and encounter decisions are outside this one-action comparison. |
| Fish, levels 11 and 12, strike1 (2 actions) | Registration `0x443330` binds separate Strike and JumpStrike callbacks. Strike callback `0x444190` detects image 202 for a **sound**; its damage-rectangle path is driven by movement/apex comparisons, not that image test. | Port frame **2** also refers to image 202, but that coincidence does not establish original damage onset. Preserve it until movement/attack geometry is reconstructed. |
| Hermit Crab, level 7, strike1 (1 action) | Registration `0x44b810` binds ES_STRIKE to `0x44cba0`; constructor `0x44bce0` binds +0x338 to strike1. Its strike callback exposes the rectangle while image **203 or 204** is active, subject to animation completion conditions. | These are indices **3 and 4**, whereas the port hits at index 4 only. The original active window starts 20 ms earlier in ANI metadata, but copying its onset alone does not reproduce the sustained window. Keep the current value pending a proper duration/geometry change. |

## Siren first-projectile boundary

The original Siren constructor `0x48cf20` initializes the projectile-spacing timer start and duration (+0x4a8/+0x4ac) to zero. Singing entry `0x48d640` resets its burst count and flag. When image 202 is reached, the update enables the burst and then tests the spacing timer in that same update. The first-ever projectile is therefore eligible immediately at index 1. Subsequent projectiles set a 300 ms spacing duration; normal completed bursts are separated by the 4000 ms entry gate, so their first projectiles are also eligible at that image.

The port's existing attack period is longer than 300 ms, so selecting index 1 is a supported phase correction for its single-shot representation. It does **not** implement the original four-projectile pattern, 4000 ms attack-entry gating, sound-length-dependent singing duration or all interruption paths. Nominal offsets 180 and 280 ms exclude the port's component delay and update quantization.

## Other timing policies are not simple frame corrections

Both recovered Red Tail kick/gun entries set a shared next-action duration to `rand() % 501 + 1000`, or **1000-1500 ms**, and record the game clock. The Home and eligibility paths still govern what happens afterward. The port's corrected placement of a 750 ms melee XML delay repairs an ignored setting; it does not reproduce that original decision policy.

Tiger Guard attack entry `0x4988e0` first checks its elapsed timer, then stores `rand() % 751 + 1250`, or **1250-2000 ms**, before selecting among three custom moves. Its modulo-101 thresholds are 40 and 80; these are not evidence for a universal 590 ms melee cycle. Reconstruct move selection, movement, consecutive knife actions and return paths together before changing its overall attack rate.

Fish requires a movement-dependent attack comparison. Hermit Crab requires an active damage window. Neither can be faithfully repaired by applying the shared event-1 rule to a marker which does not exist.

## Evidence ledger and limitations

| Original procedure | Evidence |
|---|---|
| Red Tail registration `0x482200` | `ev_47c581904b34f0333b7a9d46e9b4e79711f1c0b47c2c4319f229be3f6eb4ba5b` |
| Red Tail kick entry `0x4836b0` | `ev_b9b37a49c704f7b9a7028ab3abd0b17449261717c483f8ccb9a8b5b6d53c3127` |
| Red Tail gun entry `0x483ae0` | `ev_de4ccfade85e86df0df27251c9d30ff7370df84563eec1f1efd308d35dc7ae79` |
| Siren registration `0x48cc50` | `ev_c5be80ed54e4866471db16c7e22ddb00dc883bf0b5ffa8700dff9eb08eef3caa` |
| Siren constructor `0x48cf20` | `ev_3305ca0111110c7171a6cfe142c4ec3e61a4f65981aa59c68cbe61926c28bd53` (previous pass) |
| Tiger Guard registration `0x497ac0` | `ev_1ed431e8f21ef8f505c8c26e716bb3c55b6d5ba6093ce5b8d628fee98b94fdf4` |
| Tiger Guard knife entry `0x498ca0` | `ev_16e92d790a8eb1ff9ae0a250cc43c9aca2f5e69465f89b9cacc50d5406128102` |
| Fish registration `0x443330` | `ev_7ec8800a67fa0eedbe44f3140d8745cdb783c3b877f7bb0d392592cdd963d35f` |
| Fish constructor `0x4435f0` | `ev_8d6d607f896c79e467dbf5249f473971b786aa4811738f9273e8a0c9b83b7b8f` |
| Aquatis registration `0x404820` | `ev_1ecbb41d51585c1de5728bab0ec808479b330d313705db23c642e82d2d60b406` |
| Aquatis constructor `0x404d80` | `ev_c95b251a47e0ed1d51645d45ed8f9888720f6d12406b928c36692f9ad9f58ac5` |
| Hermit Crab registration `0x44b810` | `ev_983562c5b238b64d16220c3d7cd00c61068676665884be058441611f1970a677` |
| Hermit Crab constructor `0x44bce0` | `ev_1ed176516444ab89581cce09cc333e078426637bd20c9d31becce8cdeb819204` |

Most custom update callbacks are labels which this Ghidra provider refused to decompile. Their registration bindings are verified by REA; their comparisons, rectangle writes, timers and projectile creation were checked through bounded disassembly of the same immutable mapped PE bytes. This distinction is deliberate: the report does not claim provider pseudocode where none exists. Numeric ANI frame/image crosswalks were read from the supplied local assets without publishing their content.

All ten actions now have a concrete original-handler comparison or an explicit reconstruction boundary. Full original AI equivalence, original-Windows execution tests, sustained damage-window parity and campaign completion remain unverified. See also the [shared-handler corrections](ORIGINAL-HANDLERS-0.4.37.md).
