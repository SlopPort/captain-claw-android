# Native diagnostic filename privacy

2026-11-08. Investigation, changes and automated checks by OpenAI Codex (LLM), guided by an anonymous human. No private filename/account value is reproduced here.

## Identified disclosure and distribution action

The exact previously published APKs were matched to release metadata/checksums before action:

| Artifact | SHA-256 | Finding |
| --- | --- | --- |
| 0.4.31-test | `ee385cb56418d4a2bcdc25adc9678ed10c07a4bb06af51e421a01d86959a0a51` | Build-account directory path in both SDL libraries |
| 0.4.32-test | `ba47b306408048e2523840e86872411ac6afc8eea75e7780549abbc99811553e` | Same type of path in both SDL libraries |
| Local debug40 | `2383a7d6d789a77c9504b9f459e575e394aca48817e4e704528c3f3b41134f9b` | Known private path in SDL/OpenClaw, both ARM ABIs |

The debug40 match was localized to native `.rodata`, not just debug symbols. The identified disclosure was an assertion/diagnostic source filename; the content checker identified no credential-pattern finding in the checked public32 artifact. This is not an exhaustive security guarantee.

Both old public releases were changed to **private drafts**, with API responses confirming `draft: true`. Files, exact hashes and pre-change metadata were retained privately; no source/tag history was removed. Do not republish those binaries. A separate anonymous HTTP verification timed out and is not counted as successful access verification. Withdrawal cannot erase copies already obtained by others.

## Fix and bounded verification

Clang filename-prefix mapping now replaces build-user, NDK, source and build-directory prefixes with generic diagnostic roots. It applies before dependency subdirectories, covering SDL as well as the engine. Assertions remain enabled; neither stripping symbols nor disabling assertions is the chosen fix.

Debug **0.4.41-dev / code 53**, ARM64+ARMv7, built successfully. APK SHA-256 `4bcf15bade79c4047cd6b387b02ae5b0c35b7596f19528f167041a5416d8f187`, 34,661,850 bytes. Both ABI/native alignment checks passed. `check_apk_privacy.py` checked 375 outer/support members with the local private patterns and found **zero** private/credential markers. The same tool correctly rejected public32 for its two SDL matches.

This is a known-pattern UTF-8/UTF-16LE content check, not independent copyright clearance or proof that no possible personal identifier exists. The pattern file remains ignored/private. Signed production/releasecheck and archived-source artifacts subsequently passed their own scans; see [exact identities and bounded runtime evidence](UPDATE-0.4.41.md). The production APK remains unpublished and has not been runtime-tested under its exact package identity. Debug41 is not a certified 1.0 release and does not inherit debug40 runtime passes automatically.
