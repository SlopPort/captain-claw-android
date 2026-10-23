# 0.4.27 safety and readiness / BezpieczeĹ„stwo i gotowoĹ›Ä‡

OpenAI Codex (LLM), 2026-10-23. Development candidate, **not 1.0**. Human campaign
playtesting and deferred physical controllers are outside this technical batch.

## Reproduced and fixed

1. An export provider completing after FileToolsActivity destruction caused a real
   WindowManager.BadTokenException. The old 0.4.26 emulator APK reproduced it after
   a complete canonical export. The callback now checks isFinishing/isDestroyed
   before showing a dialog. The operation may finish after Back; its old window
   receives no dialog. Keep the tools screen open until completion when exporting.
2. Save validation silently accepted a missing root closing tag, a second root,
   duplicate LevelName and duplicate LevelNumber. A structural stack and unique
   metadata flags now reject these documents. Prefix/suffix non-whitespace text
   was already rejected and remains covered. Canonical valid saves still pass.

The instrumentation provider is test-only. A gate waits for actual Activity
onDestroyed before allowing export completion. All six malformed-save cases are
memory-only and never replace user progress. No native gameplay/balance changes.

## Artifacts

| Artifact | SHA-256 |
| --- | --- |
| ARM debug, installed on both phones | e5ae5febf62b009578d320b391078e8b47b1d78825df7398e2bfa89e602e68cb |
| ARM signed production candidate | 010a6b710c088c3f3dc55379a49fafe2d060c3e471ccebcf9d0b26efc2dd9fb4 |
| ARM signed isolated releasecheck | ba5d00cba4450e47fc3642f7338799a02fb4788cda0169dd188134c1af9fd00e |
| Final x86_64 debug, both fixes | 833a95faf5e64da6978b389abb4691a43dbe08e7ba7bd5dd0e93eaf774a4a9c6 |
| Old ARM debug baseline 0.4.26 | f32e9e96e64b91dd12ea7eff0303a97ea3c7abf1d9b16fbe08f6fa4023a3cb1f |
| Old x86_64 baseline 0.4.26 | 8cd16cb2b73cffdb11177bd48d920783411431cda0c8272258843924236ad740 |

Version 0.4.27-dev/code39, min21/target35. ARM debug/release/test builds and debug
lint passed: zero errors, 29 retained warnings, without new suppressions. Existing
native override warnings remain. All six native libraries are unchanged from
0.4.26 within each build flavor; release differs from debug (NDEBUG).

## Exact-version checks

| Device/image | Six malformed cases rejected | Valid saves/features | PL/EN settings/footer | Late export, no crash |
| --- | --- | --- | --- | --- |
| Huawei P9 Lite, Android 10, ARM64 debug | pass | pass | pass | pass |
| Redmi Note 8, Android 16, ARM64 debug | pass | pass | pass | pass |
| API21 x86_64 emulator | pass | pass | pass | pass |
| API35 x86_64 emulator, actual 16 KB pages | pass | pass | not repeated in this batch | pass |

Phone updates and tests retained config/progress byte for byte. API21 additionally
passed native menu, a 100 ms diagnostic jump, technical exit/score confirmation
and level-2 save. A technical exit teleport is never campaign evidence. The
Android-5 late-export driver initially misread shell-v1 exit codes; its sentinel
fix and r2 passed. No game failure was inferred from that preflight refusal.

On Huawei, ten fresh ordinary level-8 starts produced rendered FPS batches without
log-reader reconnection, diagnostics disabled; files restored after each start.
This is bounded non-recurrence after an earlier unexplained start timeout, not a
proof that no loading fault can ever occur.

[Signed runtime and verification](RELEASE-0.4.27.md),
[active enemy audit](ACTIVE-NORMAL-0.4.26.md),
[full import tests and retained automation failures](IMPORT-FLOW-0.4.26.md),
[twenty-minute Huawei measurement](SUSTAINED-HUAWEI-0.4.25.md).

## Compatibility limits retained

The final API21 emulator needed its existing SD-card image explicitly attached;
without it an earlier 0.4.26 run had unavailable storage. This was setup failure.
On the actual-16-KB API35 image, old 0.4.26's 100 ms diagnostic jump rose only
36.9 px and failed the greater-than-40 px guard during severe emulator frame
stalls. A separately labelled 600 ms hold passed jump/exit/save. Keep the short
failure: it is not a physical touchscreen latency measurement and has not been
fixed by these Java changes. Final 0.4.27 has byte-identical native code and passed
the Java safety cases there; no fresh final-version short-jump pass is claimed.
No physical ARM16KB device or universal Android/FPS certification exists.

Private report prefixes: readiness-{redmi,huawei}-0.4.27,
late-save-api35-0.4.26-baseline-r2, late-save-api35-0.4.27-final-fixed,
late-save-{redmi,huawei}-0.4.27-fixed, late-save-api21-0.4.27-fixed-r2,
compat-api21-0.4.27, compat-api21-0.4.27-runtime-menu,
startup-level8-huawei-0.4.27. Raw files stay private, include user data and are
not required to build the public source. Reproduce with your own lawful game data.

## Polski

Naprawiono rzeczywistÄ… awariÄ™ po zamkniÄ™ciu ekranu eksportu i odrzucanie czterech
wczeĹ›niej przyjmowanych rodzajĂłw uszkodzonego XML. Testy poprawnych zapisĂłw,
PL/EN i obu telefonĂłw przeszĹ‚y bez zmiany postÄ™pu. Emulator Androida 5 takĹĽe
zaliczyĹ‚ skok i techniczny zapis nastÄ™pnego poziomu. Zachowujemy nieudanÄ… prĂłbÄ™
krĂłtkiego skoku na przeciÄ…ĹĽonym emulatorze 16 KB; nie ogĹ‚aszamy jej naprawy.
Wyniki nie zastÄ™pujÄ… przejĹ›cia kampanii ani prĂłb wszystkich urzÄ…dzeĹ„.
