# Menu fixture lifecycle and Android 15 / 16 KB

2026-11-08. Investigation, fixture changes and technical tests by OpenAI Codex (LLM), guided by anonymous human requirements. This is a test-runner correction, not a production gameplay fix or natural campaign clear.

Main APK: debug40 x86_64 from `f11b80f`, SHA-256 `a5ccd78d0e97de265364a0b50360de0f8efaf6983cf6151b14010e8071a47bee`. Corrected test companion SHA-256: `7a4d7cd2a472d6957dfffb4d367c982e0383e75b395d7ca0809afd02bec0b984`. The project-owned Android 15/API35 emulator reported **16384-byte pages**; native ELF checks passed. Private Polish data was a fixture, not a novice installation. This does not certify physical ARM hardware.

## Failure and correction

The original fixture threw `Settings not focused` inside Android's main Looper and crashed the target. The assertion originated in `MenuTouchTest`, not production game code. UI failures now return to the instrumentation thread, so a failed check does not become a target-process fatal exception.

Waiting for focus alone did not resolve the lifecycle assumption. Android replaced the settings Activity during rotation; WindowManager recorded the relaunch, while a retained monitor reference could never regain focus. The fixture now tracks the currently resumed settings instance and resolves it on the main thread for each settings operation. Focus verification and action happen together. It still refuses unfocused input; rotation was not disabled and no global input was added.

## Verified results and limits

`todo-regression-api35-16k-0.4.40-r5` passed all three children: PL/EN menu sequences, audio sliders and disabled shared-sound checks (318 localized image states per language); six focused-window jump cases; and four save-provider error dialogs/dismissals across PL/EN. No target/unattributed crash was recorded. Installed main APK identity stayed unchanged; config/progress matched the fresh baseline after each child.

Earlier `a`, `r2`, `r3`, `r4` attempts remain failed evidence. Failed attempts after exception transport was corrected recorded no target crash. Visual screenshots still require human review. The intermittent API21 menu attempt is separate; the corrected fixture has not yet been rerun there. Debug41 filename mapping is a separate artifact and does not inherit these runtime passes automatically. No physical phone was operated by this emulator batch.
