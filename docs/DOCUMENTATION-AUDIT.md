# Documentation clarity audit — 2026-10-24

A separate OpenAI Codex (LLM) agent audited the public documentation after an
explicit human request. Its main edits were reviewed by the primary agent.
Human identity remains anonymous; upstream authors retain their attribution.

## Completed

- English default README prioritizes installation and clearly states development status.
- Installation distinguishes the APK, repository source ZIP, complete CLAW.REZ,
  placeholder REZ and prepared game-data.zip.
- Four ordered installation stages precede backups, optional packaging and troubleshooting.
- Old English/Polish guide paths remain working redirects.
- Relative links resolve. Repository and public-history privacy checks passed.
- Older APK validation is explicitly not proof of current-source compatibility.

## Remaining work

1. Establish a clearly identified public test APK download location, with version,
   checksum and signing/update guidance. No finished 1.0 release is implied.
2. Test installation and the preparation wizard on a clean computer with a new user.
3. Add useful screenshots for representative Android installation/import screens.
4. Rewrite HANDOFF with one dated current-state section; historical allocations
   and builds must not masquerade as current instructions.
5. Finish translating older public prose into English. Preserve quoted Polish UI
   labels, exact historical measurements, artifact hashes and limitations.

## Translation candidate inventory

The following heuristic inventory finds Polish diacritics in tracked Markdown,
excluding the newly reviewed entry guides and deliberate Game Over UI quotations.
It is a candidate list, not proof that every line needs translation or that all
ASCII-only Polish prose has been detected. Some documents already have English
sections; remove ambiguity and duplication without erasing evidence.

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [NOTICE.md](../NOTICE.md)
- [docs/BUILDING.md](../docs/BUILDING.md)
- [docs/CHANGELOG.md](../docs/CHANGELOG.md)
- [docs/CODE-GUIDE.md](../docs/CODE-GUIDE.md)
- [docs/CONTROLLER.md](../docs/CONTROLLER.md)
- [docs/DEVELOPMENT-NOTES.md](../docs/DEVELOPMENT-NOTES.md)
- [docs/GAME-LANGUAGE.md](../docs/GAME-LANGUAGE.md)
- [docs/HANDOFF.md](../docs/HANDOFF.md)
- [docs/PUBLISHING.md](../docs/PUBLISHING.md)
- [docs/RELEASE-SIGNING.md](../docs/RELEASE-SIGNING.md)
- [docs/ROADMAP-1.0.md](../docs/ROADMAP-1.0.md)
- [docs/TESTING.md](../docs/TESTING.md)
- [docs/UPSTREAM-DIFF.md](../docs/UPSTREAM-DIFF.md)
- [docs/validation/ACTIVE-NORMAL-0.4.26.md](../docs/validation/ACTIVE-NORMAL-0.4.26.md)
- [docs/validation/ACTIVE-OFFICER-0.4.25.md](../docs/validation/ACTIVE-OFFICER-0.4.25.md)
- [docs/validation/ACTIVE-SOLDIER-RAT-0.4.26.md](../docs/validation/ACTIVE-SOLDIER-RAT-0.4.26.md)
- [docs/validation/ACTIVE-TIGER-0.4.21.md](../docs/validation/ACTIVE-TIGER-0.4.21.md)
- [docs/validation/ANDROID-COMPATIBILITY.md](../docs/validation/ANDROID-COMPATIBILITY.md)
- [docs/validation/AQUATIS-ARENA.md](../docs/validation/AQUATIS-ARENA.md)
- [docs/validation/ATOMIC-PROGRESS-0.4.18.md](../docs/validation/ATOMIC-PROGRESS-0.4.18.md)
- [docs/validation/ATTACK-AUDIO.md](../docs/validation/ATTACK-AUDIO.md)
- [docs/validation/BUG-AUDIT-2026-10-21.md](../docs/validation/BUG-AUDIT-2026-10-21.md)
- [docs/validation/CAMPAIGN-1.0.md](../docs/validation/CAMPAIGN-1.0.md)
- [docs/validation/CAMPAIGN-RETRIES-0.4.24.md](../docs/validation/CAMPAIGN-RETRIES-0.4.24.md)
- [docs/validation/CLAW-WEB-COMPARISON.md](../docs/validation/CLAW-WEB-COMPARISON.md)
- [docs/validation/COMBAT-AUDIT.md](../docs/validation/COMBAT-AUDIT.md)
- [docs/validation/CONFIG-IMPORT-0.4.22.md](../docs/validation/CONFIG-IMPORT-0.4.22.md)
- [docs/validation/FPS-0.4.11.md](../docs/validation/FPS-0.4.11.md)
- [docs/validation/FPS-0.4.9.md](../docs/validation/FPS-0.4.9.md)
- [docs/validation/GAMEPAD.md](../docs/validation/GAMEPAD.md)
- [docs/validation/HUAWEI-CAMPAIGN-0.4.24.md](../docs/validation/HUAWEI-CAMPAIGN-0.4.24.md)
- [docs/validation/HUAWEI-P9-LITE.md](../docs/validation/HUAWEI-P9-LITE.md)
- [docs/validation/IMPORT-CLEANUP-0.4.21.md](../docs/validation/IMPORT-CLEANUP-0.4.21.md)
- [docs/validation/IMPORT-FLOW-0.4.26.md](../docs/validation/IMPORT-FLOW-0.4.26.md)
- [docs/validation/IMPORT-FULL-DISK.md](../docs/validation/IMPORT-FULL-DISK.md)
- [docs/validation/IMPORT-RECOVERY.md](../docs/validation/IMPORT-RECOVERY.md)
- [docs/validation/JOYSTICK-WIDESCREEN.md](../docs/validation/JOYSTICK-WIDESCREEN.md)
- [docs/validation/JUMP-TOUCH.md](../docs/validation/JUMP-TOUCH.md)
- [docs/validation/LADDERS.md](../docs/validation/LADDERS.md)
- [docs/validation/LEVEL14-FINALE.md](../docs/validation/LEVEL14-FINALE.md)
- [docs/validation/MARROW-ENCOUNTER.md](../docs/validation/MARROW-ENCOUNTER.md)
- [docs/validation/MENU-AUDIO-0.4.19.md](../docs/validation/MENU-AUDIO-0.4.19.md)
- [docs/validation/MENU-LANGUAGE-0.4.16.md](../docs/validation/MENU-LANGUAGE-0.4.16.md)
- [docs/validation/NATURAL-CAMPAIGN-0.4.23.md](../docs/validation/NATURAL-CAMPAIGN-0.4.23.md)
- [docs/validation/NATURAL-CHECKPOINT-0.4.24.md](../docs/validation/NATURAL-CHECKPOINT-0.4.24.md)
- [docs/validation/ORIGINAL-COMPARISON.md](../docs/validation/ORIGINAL-COMPARISON.md)
- [docs/validation/PARRY-PERF-0.4.20.md](../docs/validation/PARRY-PERF-0.4.20.md)
- [docs/validation/PLATFORM-0.4.24.md](../docs/validation/PLATFORM-0.4.24.md)
- [docs/validation/PORT-0.4.12.md](../docs/validation/PORT-0.4.12.md)
- [docs/validation/PORT-0.4.8.md](../docs/validation/PORT-0.4.8.md)
- [docs/validation/POWDER-KEG-0.4.23.md](../docs/validation/POWDER-KEG-0.4.23.md)
- [docs/validation/READINESS-0.4.25.md](../docs/validation/READINESS-0.4.25.md)
- [docs/validation/READINESS-0.4.27.md](../docs/validation/READINESS-0.4.27.md)
- [docs/validation/READINESS-2026-10-23.md](../docs/validation/READINESS-2026-10-23.md)
- [docs/validation/REDMI-0.4.21.md](../docs/validation/REDMI-0.4.21.md)
- [docs/validation/REDMI-0.4.25.md](../docs/validation/REDMI-0.4.25.md)
- [docs/validation/REDMI-0.4.29.md](../docs/validation/REDMI-0.4.29.md)
- [docs/validation/RELEASE-0.4.26.md](../docs/validation/RELEASE-0.4.26.md)
- [docs/validation/RELEASE-0.4.27.md](../docs/validation/RELEASE-0.4.27.md)
- [docs/validation/STARTUP-0.4.17.md](../docs/validation/STARTUP-0.4.17.md)
- [docs/validation/SUSTAINED-0.4.15.md](../docs/validation/SUSTAINED-0.4.15.md)
- [docs/validation/SUSTAINED-HUAWEI-0.4.25.md](../docs/validation/SUSTAINED-HUAWEI-0.4.25.md)
- [docs/validation/SUSTAINED-REDMI-0.4.21.md](../docs/validation/SUSTAINED-REDMI-0.4.21.md)
- [docs/validation/TERRAIN-HEIGHTS-0.4.25.md](../docs/validation/TERRAIN-HEIGHTS-0.4.25.md)
- [docs/validation/TODO-AUDIT.md](../docs/validation/TODO-AUDIT.md)
- [docs/validation/USER-REGRESSIONS-0.4.29.md](../docs/validation/USER-REGRESSIONS-0.4.29.md)
- [docs/validation/VERTICAL-45-0.4.18.md](../docs/validation/VERTICAL-45-0.4.18.md)
- [docs/validation/VERTICAL-COMBAT-PLAN.md](../docs/validation/VERTICAL-COMBAT-PLAN.md)
- [docs/validation/VERTICAL-COMBAT.md](../docs/validation/VERTICAL-COMBAT.md)
- [experiments/README.md](../experiments/README.md)
- [experiments/rejected/image-ownership/README.md](../experiments/rejected/image-ownership/README.md)
- [experiments/rejected/tile-atlas/README.md](../experiments/rejected/tile-atlas/README.md)
