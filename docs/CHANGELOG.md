# Adaptation changelog

Entries describe changes in their recorded builds. Linked reports define the exact tested APK, hardware, methods and limitations. Historical results do not automatically certify the current source or release 1.0. Adaptation work was performed by OpenAI Codex (LLM), guided by human requirements and feedback; upstream authorship is preserved.

## 0.4.31 — clearer Game Over screen

Separates the Game Over heading from its instruction so the title does not resemble a second action. The instruction describes returning to the main menu by touching the screen. [UI behavior and verification](GAME-OVER-UI.md). Public documentation is being consolidated in English; Polish game UI remains supported.

## 0.4.30 — stable platform-edge collision

An Android player flat-foot fixture replaces the rounded lower contact while retaining the head and other body/sensor behavior. Controlled ledge/crouch and ladder checks are scoped in the [REA/terrain report](ORIGINAL-BEHAVIOR-REA.md). This is not proof of pixel-exact original behavior or a natural campaign clear.

## 0.4.29 — pause, bonus music, Game Over and short attacks

Raw Start remains a pause/menu fallback even with custom pause binding. Level and bonus music preparation moves to loading, with a cache bounded to three tracks. Text-only Game Over navigation no longer triggers the reproduced assertion or an unbounded focus search; its message describes returning to the menu. One melee tap during hurt can wait up to 400 ms for the animation to finish and is cleared on death. This is an intentional accommodation, without changing hitboxes or immunity, not verified original behavior.

[Huawei reproductions and final APK checks](validation/USER-REGRESSIONS-0.4.29.md); [later Redmi follow-up](validation/REDMI-0.4.29.md). The original final-APK batch was Huawei-only. Version 0.4.28 was a local intermediate reproduction package; Redmi was not used for that batch. These technical checks do not certify the campaign or every physical controller.

## 0.4.27 — export lifecycle and save validation

Fixed the reproduced late-export `BadTokenException` and acceptance of unclosed XML, a second root or duplicate metadata. Valid saves remain supported. Added lifecycle/framing checks, isolated signed ARM64/ARMv7 controls tests, actual file-picker checks on both phones and test-launch diagnostics. The active audit of 45 variants retains failed fixtures. No native physics/balance changes. [Android 5/10/15/16 evidence and limits](validation/READINESS-0.4.27.md). Human campaign QA remains open.

## 0.4.26 — import and release signing

Scrollable installer. Actual picker cancellation and full-REZ stream checks on Android 10/16 restore test data afterwards. [Scope](validation/IMPORT-FLOW-0.4.26.md). A separate local release identity was prepared; release builds require signing configuration. Keys/passwords never belong in public sources. [Signing guide](RELEASE-SIGNING.md).

The [terrain/active-height audit](validation/TERRAIN-HEIGHTS-0.4.25.md) applies to 0.4.25. Six debug native libraries remain identical; physics/balance did not change. This is not a complete campaign or release 1.0.

## 0.4.25 — accessible screens and release preparation

Original app icon without commercial game art, localized save-tool credits and scrollable save tools. An inaccessible Back button was reproduced on a small emulator with 200% font scaling; both languages passed after the fix. Explicit modern Android backup/transfer exclusions retain the automatic-backup opt-out; manual save export remains. Touch diagnostics read the installed APK's checksum. Bounded retries of explicit exit teleports are counted technical fixtures, not campaign evidence. No native-engine, physics or balance changes. [Packages, results and retained failures](validation/READINESS-0.4.25.md).

## 0.4.24 — platform measurements and a natural checkpoint

Opt-in platform movement observations and ordinary jump scheduling without an extra hit. Real boarding/carrying checks passed on Redmi/Huawei; physics was unchanged. The first persistent level-1 checkpoint was reached naturally and loaded through the normal menu with matching score, lives and ammo. The full campaign remains incomplete. [Platform observations](validation/PLATFORM-0.4.24.md), [natural checkpoint/reload](validation/NATURAL-CHECKPOINT-0.4.24.md).

## 0.4.23 — powder-keg explosion crash

Fixed a premature explosion-body bounds query in adaptation diagnostics. The crash was found during a natural campaign attempt, reproduced on the old version and checked after the fix on both phones. Damage and blast size were unchanged. [Evidence](validation/POWDER-KEG-0.4.23.md).

## 0.4.22 — configuration validation before import

Configuration XML is validated before replacing data: root, closing tags, entities and size bound. Rejection shows a PL/EN message and preserves existing data. Eleven malformed cases were rejected on Huawei, Redmi Android 16 and an Android-5 emulator; two failed parser iterations remain in local reports. Both ARM builds passed clean compilation; the resulting parser, phone jumps and exits were checked. [Results](validation/CONFIG-IMPORT-0.4.22.md).

A separate twenty-minute Redmi 0.4.21 observation averaged 59.998 FPS in one dense scene. [Limits and stalls](validation/SUSTAINED-REDMI-0.4.21.md).

## 0.4.21 — import cleanup and Android 16

Abandoned import staging files are removed after successful startup recovery or an import failure. Backups are preserved with a malformed journal. Sixty-four boundary cases and Huawei/Android-5 tests were recorded. Updating Redmi from 0.4.3 retained saves/configuration; jump, multitouch and touch exits passed on Android 16. [Import](validation/IMPORT-CLEANUP-0.4.21.md), [Redmi](validation/REDMI-0.4.21.md).

## 0.4.20 — distinguish parry from missed contact

Diagnostics record the existing parry roll and health result without changing damage or drawing another random value. Optional quieter measurements are not advertised as an optimization. All fourteen maps started on Huawei without the preview flag. [Results and limits](validation/PARRY-PERF-0.4.20.md).

## 0.4.19 — touch audio settings

Volume sliders support drag/cancellation, save atomically and retain the selected channel when a finger crosses rows. Muting no longer re-enables unsupported separate voice/ambient controls. PL/EN checks on Huawei Android 10 and an Android-5 emulator covered 109 named labels per language. [Scope and APK hashes](validation/MENU-AUDIO-0.4.19.md).

## 0.4.18 — atomic progress saves

Checkpoint and level-completion saves no longer truncate the old file before the new file is complete. A shared helper checks writing, synchronization and replacement, with a PL/EN failure message. Save imports are serialized across threads. Real checkpoint/restart/reload, score transition and all fourteen map starts passed. A small FPS experiment was rejected rather than advertised as an optimization. [Exact APKs, results and limits](validation/ATOMIC-PROGRESS-0.4.18.md).

## 0.4.17 — preparation on every launch path

A directly restored game activity also prepares engine support, language, import recovery and progress off the UI thread. The first save is atomic; replaying interrupted import preserves the previous-progress backup. Both architectures passed a clean build and the APK was checked on Huawei. [Evidence](validation/STARTUP-0.4.17.md).

## 0.4.16 — PL/EN menus and 16 KB pages

Locally rendered PL/EN menus, help and attribution avoid bundling commercial English menu art. Unsupported inherited buttons are disabled, touch regions are readable, Android settings overlay menus, and fonts are shared during a load. Huawei checks covered both languages, jump, score and Game Over return. A separate Android-15 emulator with real 16 KB pages passed PL/EN menus, native-library loading, jump and a level exit. This was not a natural campaign or 60 FPS certification. [Exact APK and limits](validation/MENU-LANGUAGE-0.4.16.md).

## 0.4.9 — SDL draw batching

Explicit batching restores a queue disabled by SDL's default after selecting GLES2. Same-APK off/on/off samples at levels 8/9/13 approached 60 FPS from approximately 57/54/58 FPS. Resolution, filtering, physics and logic speed were unchanged. A local opt-out restores the previous path for driver problems. [Method, results and limits](validation/FPS-0.4.9.md).

## 0.4.8 — Claw Web workflows, optimization and audit

Direct REZ import, validated save export/import with a previous-progress backup, optional vibration and narrower preloading credit inspiration/adaptation from Claw Web (Arthur Boss and contributors). ThinLTO/O3, component-lookup caching and skipped inherited empty updates preserve image quality and solver settings. Frame timing resets after loading and samples only active gameplay. Audited ladder bottoms/contact lifetime; fixed the Box2D diagnostic clock and newer-Android USB receiver compatibility. [Results and remaining limits](validation/PORT-0.4.8.md). Natural campaign completion remains unverified.

## 0.4.7 — saved audio and FPS

Fixed empty audio-option writes on Android while preserving unrelated configuration. Optimized native dependencies in debug and cached stick rendering. Short stationary Huawei P9 Lite samples changed from approximately 23 to 60 FPS at level 1, and 18 to 43 FPS at level 13, without lowering resolution. [Comment audit, remaining issues and measurement limits](validation/TODO-AUDIT.md).

## 0.4.6 — ladders and controller settings access

Climbing ends when the ladder no longer extends above the feet; holding Up at the top no longer repeatedly attaches. At that version, PAD moved away from health to the bottom of the screen; this is historical layout, not its permanent location. Android menus accept repeated controller Up/Down without repeating confirmation. [Details and original-game comparison limits](validation/LADDERS.md).

## 0.4.5 — configurable controller bindings

Physical button/trigger capture, saved/default bindings and separate menu actions. A Java/JNI/SDL queue avoids ambiguous device-button translation. A test confirmed sword damage after assigning L1; the user subsequently confirmed correct operation.

## 0.4.4 — controllers and source organization

SDL_GameControllerDB, hotplug/disconnect handling, dead zones, pause input and Android shutdown fixes, installation guides and a local Git project excluding commercial game data. Guides originally existed in PL/EN; public explanatory documentation is now maintained in English.

## 0.4.3 — touch and jump

Larger thumb-oriented action buttons, action symbols, finger ownership until release, direct event dispatch, a minimum 110 ms short-tap hold and cached action drawing. [Measurements](validation/JUMP-TOUCH.md).

## 0.4.2 — combat

Audited 45 variants and 1,415 placements. Restored 54 level-13 chameleons; fixed health/death, patrol direction, projectile contacts and the active crouch body. A one-off contact failure with an undetermined root cause remains recorded.

## 0.4.1 — stick and widescreen

Eight-direction stick with independent fingers; wider world view without distorted graphics; HUD anchoring and centered-menu handling.

## 0.4.0 — Omar and ending

Two-phase encounter, dialogue, surrender, retry reset and an engine-staged ending; guard acrobatics and chameleon disappearance. This is an engine interpretation, not reproduction of the original movie.

## 0.3.x — finale components

Further level-14 platforms, traps, launchers, geysers, LavaHand and LavaMouth. Controlled tests did not establish full completion or parameter parity with Windows.

## 0.1–0.3 — Android foundation

Gradle/CMake/NDK, SDLActivity, ARM64/ARMv7, data import, Polish PCX support, touch, portability/audio fixes, TiMidity/FreePats music and a lower-memory profile.
