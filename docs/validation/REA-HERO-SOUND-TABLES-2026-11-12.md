# Hero hit dispatch tables and sound requests — 2026-11-12

OpenAI Codex (LLM) performed this static follow-up to the [hero hit-entry review](REA-HERO-HIT-ENTRY-2026-11-12.md). The exact supplied target and full-audit limits remain in the [audit overview](REA-FULL-AUDIT.md). Human identity is omitted. No original execution, phone test, sound playback or gameplay change occurred. Raw bytes/instructions remain private.

## Closing four computed transfers

The previous independent traversal recorded four unresolved indexed jumps. Each has an observed unsigned compare/above branch that limits the index to 0..3 before reading a four-byte target from the respective table. The existing exact REA byte carrier covers all four tables and targets. The reviewed targets were added explicitly as bounded-region entry points, not invented function definitions.

| Jump | Table | Four observed targets |
| --- | --- | --- |
| `0x41e2cb` | `0x41ea74` | `0x41e2d2`, `0x41e2ed`, `0x41e308`, `0x41e323` |
| `0x41e367` | `0x41ea84` | `0x41e36e`, `0x41e389`, `0x41e3a4`, `0x41e3bf` |
| `0x41e682` | `0x41ea94` | `0x41e689`, `0x41e69b`, `0x41e6ad`, `0x41e6d4` |
| `0x41e726` | `0x41eaa4` | `0x41e72d`, `0x41e763`, `0x41e792`, `0x41e7bd` |

The resulting worklist contains **666 decoded instruction starts**, up from 475: **191 added starts**. It has no pending entries or unresolved computed transfer among those four jumps, but retains **44 call-contract gaps**. The initial traversal is preserved privately as a separate snapshot, together with guards, table bytes, targets and the same byte-Evidence identity. Additional native REA sample checks compare new branch instructions against the independent decoder. This closes these local dispatch targets, not all possible external entries or the entire hit function.

Byte source: `ev_921afbdac125960c66a578c3192625b01c3f588e361cadb538830c97af14f7f3`.

## What the added branches do

The first/third tables select among resource identifiers `GAME_HIT1` through `GAME_HIT4`; the second/fourth select `CLAW_1110048` through `CLAW_1110051`. These names were verified by a bounded, complete REA read with NUL termination, not inferred from nearby strings. They are resource identifiers, not redistributed audio or dialogue; they do not prove a clip's language or availability in an installed dataset.

Branches test a sound-manager field and attempt a lookup, using either a wrapper or the underlying map directly. Missing resources skip the playback request and rejoin the subsequent hit logic. The added instruction blocks contain no direct hero-health writes. Their helper side effects and backend failures still require their own contracts; silence must not be equated to rejected damage.

The random selector calls `0x4a595b`. Its ordinary path obtains a per-thread data pointer, advances a 32-bit linear congruential state and returns a 15-bit value. The observed low-two-bit selection therefore lies in 0..3; the explicit compare still provides the local dispatch guard. Thread-data allocation/initialization and all random consumers are not closed by this observation.

Evidence: resource-key read `ev_e45653fb84dd766d934af9399567862dd486e8b30905f13f55678a77e6c3ad04`; random helper `ev_ccc7d3baebce1a8e8c619f0aa059877782a3c21dcc8cab49291504fcddd39393`.

## Lookup and playback boundaries

`0x45a4e0` initializes its local result to zero, calls map lookup on manager `+0x10` and returns the resulting value. Wrapper `0x4fc6b4` writes an output only when its underlying node lookup succeeds. `0x4fc65e` hashes a NUL-terminated key with multiplier 33 and signed-byte additions, selects a bucket modulo the configured bucket count, then walks nodes until its comparison helper reports equality. Valid terminated storage, a nonzero count and well-formed chains remain preconditions; no malformed-resource crash is asserted from absent local checks alone.

Comparison helper `0x4a5ab6` uses the ordinary string comparator in one configuration and a locked multibyte-aware path in another. Complete locale/lead-byte table initialization and locking/error behavior remain open. Do not call the map case-insensitive or presume arbitrary Unicode normalization from its resource-key use.

Playback wrapper `0x421bb0` rejects requests when the global enable flag is clear or the unsigned difference between current timing and the resource's prior request time is below its configured threshold. It updates the prior-request timestamp **before** calling backend helper `0x4b3da0`. A failed backend attempt can therefore still consume this request interval. Threshold values, reset paths and clock continuity remain separate obligations; this is not a newly demonstrated missing-audio bug.

`0x4b3da0` checks a backend-associated field, obtains a playback object and attempts several parameter setters and a start operation. The setter/start calls are made before its combined success result is evaluated; it does not short-circuit after the first failed setter. Exact parameter units, playback-object lifetime and device-specific backend behavior remain partial.

Evidence: lookup wrapper `ev_e68ff7255cd1c3054f9015313fb84c9473b494eda62f8aeb1807882ded998468`; output wrapper `ev_7c4169acbb57f1e6fd79bc4febdf824fb362f4292d55b6c944fb4ef25535f886`; node lookup `ev_28279dc4185cd9a0a8fc366eeb3322fe64779301960027d609504e84d71472fc`; comparator `ev_7d1ce673c569514777c06f7e8a67e12fb737f142b0f9eaec69ef0ddc52dfd947`; request gate `ev_8ace50c88009aaa49e4f29101e306945c49f4a49494b9b313d2fcd9ac23ee177`; backend wrapper `ev_db449627b040e7281bfb413fc18d8c533864dac9a10f8e9f5b9f5258cad1c2ae`.

## Port comparison and retained findings

The current port's `ClawControllableComponent::OnHealthChanged` selects a take-damage sound and triggers a sound-request event. That establishes a comparable request path, not equivalence of the two original resource-selection stages, per-resource throttling, mixer behavior or localization. Earlier Android sound-loading/playback corrections are not reopened by these static findings. No phone, resource-import or audible-output test was run here.

The earlier category-mask/850-unit countdown and health-before-repeated-reaction findings remain bounded as documented. The newly joined sound-choice branches do not resolve Soldier/Officer source categories, invulnerability acceptance, natural stair combat or full runtime parity. Seven further inventoried helper functions receive partial reviews; the hero entry remains partial with explicit call gaps. The full machine-code audit is still open.
