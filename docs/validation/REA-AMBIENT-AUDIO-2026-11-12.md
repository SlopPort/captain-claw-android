# Ambient audio: executable and port comparison

OpenAI Codex (LLM), 2026-11-12. Part of the [whole-file REA audit](REA-FULL-AUDIT.md), not a new audio implementation or a phone listening test. Target: supplied CrazyHook-distributed x86 `CLAW.EXE`, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. REA 6.7.0 / Ghidra 12.1.4. This is not original source or verified pristine-1997 behavior.

## Joined paths

The registration routine associates the AmbientSound and SpotAmbientSound callbacks with `0x402cd0` and `0x402e50`. Those callbacks reach different constructors: ordinary/interval area sounds use `0x4022d0` / `0x402400`; spot sounds use `0x402350`. This provides a stronger association than naming unrelated functions from nearby addresses.

| Original boundary | Observed behavior | Evidence ID |
| --- | --- | --- |
| Area callback `0x402cd0` | Builds an area from object fields, selects ordinary or interval sound, optionally installs another rectangle | `ev_1b5f3633d93bc289f7f910eacd580b3b2b95bccb270100afb9f926dfedd4c6f7` |
| Spot callback `0x402e50` | Captures the object's two coordinates, creates a spot source and later removes its tracked sound on the observed removal message | `ev_2b0fd1153a61a1baee6c11328a82132da50677d6ba9d9b8cb3760fbdabfa59eb` |
| Area initialization `0x402600` | Rejects a null sound; a missing or all-zero rectangle selects an integer sentinel, rather than a normal zero-size area | `ev_b8e9f225716d9d2a825fb32a3c7b94d6e4278442216818286d9d9fb12fbcbc2c` |
| Area update `0x402720` | Tests strict rectangle interiors, permits either of two configured rectangles, avoids duplicate activation and selects a 1000-unit fade path in applicable entry/exit branches | `ev_a39b2ac977cb7552247fa2bf2480638ed471b8426dc28f166e015f792987062c` |
| Gain changes `0x4026a0` / `0x402840` | Integer gain composition, clamping, and immediate-versus-scheduled application | `ev_d42d9fcbf2175c6793e04d5ad266f499f56d39ca8fbdc62323ffd709ea73e293`, `ev_6113181447c549ab2d9158873192dc51f084f44040c777e4b1ba6b2bdb359caa` |
| Activation `0x4028c0` | Start/stop flags and separate immediate/fade branches; disabled or missing subsystem gates can reject starting | `ev_0a50ade8afc327147a2f5ed819c59e1c0f1159d00b14c7f7d30b766ba5b104bd` |
| Spot update `0x402ac0` | Axis range gate, radial attenuation, signed horizontal parameter and start/stop policy | `ev_c3b042c30faaf222ec0fe6de1b2d3df849d022ab8db49ac7d0cc98d348fa6973` |
| Sound gain `0x4b3620` | Uses an index into a stored conversion table before the lower-level setter; the input is not automatically linear PCM amplitude | `ev_2037cd8a662dc80b80c3ac82537a911f4ca31d441be5d9a6e62ba6a12acd35c1` |
| Fade scheduling `0x4b36c0` | Zero duration applies immediately; nonzero duration creates a transition object with a target value, current value and completion mode | `ev_4ef74405ccc057d3c99174b2f2428a0b0a70b3571a6859a7c17661f34276bb6e` |
| Transition update `0x4b4510` | Sentinel time input selects `timeGetTime`; updates run only when the supplied clock value advances, completed transition objects are removed | `ev_28b72a794e331a9c5254df2929ace0ce8c0e63d4ebaee0fdb3a44af80c48786a` |

The clock and transition links support a millisecond interpretation of the 1000-unit calls. Exact interpolation and all pause/clock-wrap behavior still require the transition object's update implementation; do not call this a measured one-second waveform.

## Spot geometry: assembly matters

`0x402ac0` rejects a source when either absolute coordinate separation exceeds **640**; exactly 640 passes that axis gate. Inside the gate, assembly explicitly squares both separations, adds them, performs an x87 square root and converts the nonnegative distance to an integer. The conversion helper `0x4a59d0` temporarily selects truncation and restores the prior control word. Its Evidence is `ev_7f6c48082a2320e2ebdf25e526443c0f3a0d7e041e6f13f7496b2c545c6be18b`.

For this bounded position path, the raw attenuation index is the clamped result of subtracting integer distance divided by 12 from 100. A separate signed horizontal index uses absolute X separation divided by 4, capped at 100, with sign selected by source/listener ordering. That index reaches the sound-control helper; its final backend pan mapping is not yet recovered. The decompiler's parameterless floating conversion expression alone omitted the distance calculation, so it was checked against assembly.

These facts do not establish a globally audible radius, a linear acoustic falloff or stereo-channel amplitudes. Enabled-state gates, conversion tables, source volume, optional gain, backend operations and the actual listener position remain part of the chain.

## Comparison with current port sources

The checked paths are `Engine/Util/Converters.h`, `LocalAmbientSoundComponent.cpp`, `GlobalAmbientSoundComponent.cpp` and `Engine/Audio/Audio.cpp` in the prepared OpenClaw tree. The committed adaptation patch preserves the Android changes.

- **Source types are collapsed:** the converter handles SpotAmbientSound and AmbientSound through the same local component, chooses a trigger area from level fields and reduces its height when it exceeds its width. The EXE paths above distinguish area and point sources. Their geometry and lifecycle cannot be declared equivalent from a shared name.
- **Attenuation differs:** the local component applies SDL_mixer distance using Euclidean distance divided by half the selected area's diagonal, quantized to 0..255. This is different from the recovered fixed axis gate and integer radial index. Its shown update has no separate signed-horizontal/pan operation. This is a static fidelity difference, not a newly reproduced missing-sound defect.
- **Boundary behavior differs:** the local component uses physics trigger entry/exit, starts looping on entry and halts the channel on exit. The inspected original area path includes strict rectangle tests, a possible second rectangle and scheduled transitions. Runtime impact needs actual source/area data and entry/exit observations.
- **Gain units are not interchangeable:** the EXE conditionally subtracts 15 from one gain input above 5, performs signed integer percentage products, optionally applies another positive factor and clamps to 0..100 before table conversion. Field meanings and the table are not fully joined. Do not transplant that offset into SDL percentages or reverse the already verified Android correction for double master attenuation.
- **Existing port accommodations stay explicit:** the converter already reduces selected looping global sounds on levels 2/3/4. That adjustment is a port choice; this report does not establish its original equivalent or request its removal.

No production behavior, APK or game data changed for this comparison. Earlier gain/mute/ambient runtime passes retain their scope. Original audio parity and the broader AUDIO-01/03 acceptance remain open; this review does not reopen the solved gain or Catnip-loading fixes.

## Remaining joins

Recover the gain/pan conversion tables and setters, transition interpolation/completion and all relevant pause/reset/removal paths; bind original object fields to actual map data and listener coordinates; compare area/spot/global cases individually. Preserve typed distinctions between stock and custom assets, missing resources, mute and disabled backends. The associated ledger entries remain partial until their remaining contracts and port mapping are established. Raw assembly, full pseudocode and asset contents remain private.
