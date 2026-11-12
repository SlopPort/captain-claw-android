# Terrain rectangles and contact forwarding

OpenAI Codex (LLM), 2026-11-12. Part of the [full REA audit](REA-FULL-AUDIT.md), continuing the [projectile method chain](REA-PROJECTILE-CHAIN-2026-11-12.md). Target: supplied CrazyHook-distributed `CLAW.EXE`, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`; REA 6.7.0 / Ghidra 12.1.4. Static findings are not original source or runtime parity.

## Separate terrain and object-contact paths

The shared constructor `0x4088d0` conditionally registers **LogicHit, LogicAttack and LogicBump**, then attaches handler objects through name-resolution/setter routines. This is a separate chain from movement's terrain queries. Constructor Evidence: `ev_ec42959d21665a52cc5679eeb4aeb102cee51cf3e4bfc8a5af1c3a0b19dfa1ac`.

Three additional unowned regions each contain five decoded forwarding instructions. They recover the instance through the supplied object and tail-jump to different virtual slots:

| Registration | Callback | Slot | Entry-instruction Evidence |
| --- | --- | --- | --- |
| LogicHit | `0x4def10` | `+0x1c` | `ev_0c0a4d8c4fa991b7a6ad8d92408897aa2151370c41c62b67003fe60c97046eda` |
| LogicAttack | `0x4def20` | `+0x24` | `ev_9ef47d196f6e6f3f7a10558366771ce06b6f3a090bda901682df773bfa90d0b4` |
| LogicBump | `0x4def30` | `+0x20` | `ev_1ca753cd1ae55cd4391059824db1a6c8bcf81c41d46fbe57e6c957f141d5c418` |

The name-based attachments resolve through `0x4c7730`, `0x4c7810` and `0x4c78f0`. Their setters at `0x4c7690`, `0x4c7770` and `0x4c7850` use separate owner fields `+0x80`, `+0x88` and `+0x90`, allocate/reset a handler when needed and configure it through a virtual slot. A missing registration or failed allocation is checked locally; the constructor's wider response to failures remains unreviewed.

For the statically installed **Bullet** vtable, these three slots all point to `0x40b630`, which returns integer one. This is a joined target for this class, **not a recovered meaning of the return value**, a damage amount, an invulnerability policy or a repeated-hit rule. The shared constructor also introduces registrations outside the initial central registry, so central-registry enumeration alone cannot cover all object dispatch.

Setter Evidence: `ev_ee499141ec31b6bc7b0093afaf774bda89762c33a546597d8e4dffbfb48b2246`, `ev_e2052a273e4336ccc6a7ae1e84fc00fdc5fc890cf7ff6d5e8fe13dcea2ce7ef5`, `ev_e87f16785f185d930bc0dce9bbf91d9a1436748c29bf858dd153ded46f5ec23f`. Bullet return target: `ev_1bed0bf064e59e52f341bf58285a6b674e718b6906d158c846925412ecd21534`.

## Movement rectangle consumers

The earlier initializer wrote image-derived bounds at owner `+0x134/+0x138/+0x13c/+0x140`. The terrain consumers now establish how this particular record participates in movement:

- Right-side query `0x4cd090` probes translated `X + right`, over the top-to-bottom range. The left counterpart `0x4cd1f0` uses `X + left`. On the inspected blocking tile result, each restores the previous X rather than simply accepting the proposed X. Their result masks differ.
- Lower-edge query `0x4cd610` forms a lateral span from `X + left` to `X + right` and samples at proposed `Y + bottom + 1`. Upper-edge query `0x4cd8b0` uses proposed `Y + top - 1`. These observations join the field ordering to actual consumers, without relying only on an auxiliary header's names.
- Samples are converted to tile-local integer coordinates; out-of-map query coordinates are clamped to map bounds. Sentinel tile entries skip the tile callback. The callback returns a numeric tile category; not every category's concrete implementation is joined here.
- Sampling uses owner-provided strides. Do not assume that every intermediate pixel is tested. The side scans explicitly include their final vertical endpoint; the horizontal scans' exact sampled endpoint set depends on the stride and span. Positive/valid stride initialization remains a required precondition to investigate.

The distinct geometry record at `+0x154` is **not proved to share these terrain consumers**. Do not conflate movement support, attack rectangles, incoming-hit rectangles and graphics bounds or resize all of them from one record.

Evidence: right `ev_e73b079c1eec2ad20566e58670bc7d671712ff2ce46d95c1ed8074e017ced8c1`; left `ev_ff948b38fcf3b43442573245c4bb6c08417eb2e0f012fae47e6630457f117a11`; lower edge `ev_45e3b61fd79b420da02c993664610e93f8f95bbeaaa0879f6d0473ada6e80e6f`; upper edge `ev_961d3e640a3a5994287e70a32d1e74af265b569f92018b074d5c7fd7b6d2acf2`.

## Mode and result propagation

Wrapper `0x4cc7e0` can subdivide long movement according to query thresholds. An owner flag and mode **7** can bypass that subdivision. This is not a claim that every movement type uses the same subdivisions.

Dispatcher `0x4cc920` has a concrete mode-7 branch that writes the requested coordinates directly. Mode **8** chooses different paths according to the sign of the proposed Y change. The decreasing-Y branch can temporarily change mode and then restore 8 while adding a result bit; the other path can detect another mode change and add a different bit. The dispatcher additionally combines several result bits into `0x10000` and marks unchanged coordinates separately.

The already inspected falling update reads the movement result's `0x10000` bit and propagates a bit into owner flags. This join still does not establish the owner flag's full removal/lifetime contract. A search for direct consumers found other structures using the same numeric bit, including a candidate with dimension/allocation fields; matching an offset and constant is insufficient to identify an object-removal path.

Evidence: subdivision wrapper `ev_60fdc6ea202b5ac554ff749f56457d33393275e45205fd71ccce2b966d00742f`; mode dispatcher `ev_d758217efbd173342c56ee38bdee1c0003089615ec547d92c269a076cd71a6f8`; directional helpers `ev_bff5340419dcf611bc2f27a21a4131e7101796b1433890b41db60ea31ada1023`, `ev_f9923753cb36f9c6a7a9ffda45b831ac83455e33440b27d309abb686285a0580`.

## Port comparison and retained scope

The checked port paths are `ClawPhysics.cpp`, `PhysicsContactListener.cpp` and `AIComponents/ProjectileAIComponent.cpp`.

- The port uses Box2D bodies, fixtures and support contacts. The inspected original uses translated integer rectangle edges and tile queries. This supports a concrete architectural distinction; it does not certify the exact original footing for every level, slope, ladder cap or posture.
- The port's projectile-contact branch checks current body registration before looking up the projectile. Actor and static-terrain contacts then take different callbacks; its ladder-cap fixture has an explicit exemption. Compare those cases against original data and categories individually.
- The projectile component checks activity, source actor and per-target tracking before requesting a health change. The three original forwarding wrappers alone do not establish the receiver's damage acceptance, token lifetime, interruption or invulnerability rules. Keep existing Android deduplication until that full contract is joined.
- The geometry evidence does not close the reported natural level-2 snag, natural stair combat or human campaign acceptance. Existing flat-foot/floor-join fixes are not reopened merely because more original terrain code is now described.

Fifteen further functions and the three forwarding regions received **partial** reviews. No code behavior, APK, phone state or game data changed. Remaining joins include tile-category implementations, stride initialization, specific hit receivers and owner-flag lifetime. Raw instructions, full pseudocode and `collision-proxy-join.json` stay in the private audit directory.

The saved checkpoint contains 48 partial initial-inventory function reviews. Six formerly unresolved Bullet calls are now closed by the actual return-only target; five other call contracts remain partial. Earlier extraction reports were updated accordingly so later workers do not repeat the completed checks.
