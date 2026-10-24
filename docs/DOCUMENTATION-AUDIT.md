# Documentation clarity audit

Updated 2026-10-24. Three separate OpenAI Codex (LLM) review workers corrected
independent documentation groups; the primary agent checked links, historical
hash retention and publication boundaries. The human remains anonymous.

## Completed corrections

- English explanatory prose throughout the public Markdown documentation,
  including historical validation and rejected experiments. Real Polish UI
  labels remain quoted where a player needs to recognize them.
- Player-first README; numbered installation instructions; distinctions between
  APK, source ZIP, full CLAW.REZ, placeholder REZ and prepared game-data.zip.
- Unique Polish evidence merged before removing bilingual duplication. Dates,
  measured values, failures, hashes, attribution and test limitations retained.
- One current state in HANDOFF; old phone allocations and build results clearly
  historical. Earlier results do not certify the latest APK or grant access to
  a device currently used by another task.
- Build and contribution guides consolidated while preserving old link paths.
- Actual English app-owned importer and language-dialog images, with provenance
  and Android-variant limits in [image notes](images/README.md).
- Relative Markdown/HTML image links checked. No historical SHA-256 values lost.
- Source/privacy checks exclude game assets, player data and signing credentials.

## Test APK distribution

A signed development APK is publicly available at
[v0.4.32-test](https://github.com/SlopPort/captain-claw-android/releases/tag/v0.4.32-test).
Anonymous download was verified and its SHA-256 matched the local published file.
The guide identifies the exact APK, and the release includes a checksum file,
source revision, signing identity and runtime limitations. This is not release 1.0.
See [binary validation](validation/RELEASE-0.4.32.md).

## External checks still required

These cannot honestly be marked complete using this developer computer alone:

1. A new user follows the instructions on a clean computer, including the optional
   Tk preparation wizard and initial dependency downloads. Installed tools and
   cached repositories do not constitute this test.
2. Additional Android installer/file-picker variants receive screenshot-guided
   examples after testing on those systems. Current images show the app's own
   Huawei/Android 10 UI, not every manufacturer's system screens.

These checks remain release gates rather than hidden claims. They do not prevent
publishing clearly labelled development sources or a test APK. Report a confusing
step with its heading and exact message; never attach copyrighted game data,
private signing material or personal device identifiers.
