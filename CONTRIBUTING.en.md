# Contributing

[Polski](CONTRIBUTING.md) · [Current handoff](docs/HANDOFF.md) · [Build](docs/BUILDING.en.md)

This is a development adaptation of OpenClaw, not a completed 1.0. Read the handoff
before changing gameplay. Adaptation code, investigation and documentation so far
were performed by OpenAI Codex (LLM), with human requirements and hardware feedback.
Keep inherited authorship and dependency notices intact.

## Start here

1. Clone this repository into a dedicated folder. Never copy a local game installation
   into the repository. Follow the build guide and pinned `sources.lock.json`.
2. Make a task branch. Keep unrelated projects, build outputs and device sessions
   separate. Do not change global Git identity or sign another project out of GitHub.
3. Read the relevant validation report. A map loading, a controlled fixture and a
   natural playthrough are different kinds of evidence.

## Where changes belong

| Area | Source |
| --- | --- |
| Touch and controller input | `native/PlatformInput.cpp`, `app/src/main/java/pl/pazur/port/ControllerSettingsActivity.java` |
| Launcher, data selection | `app/src/main/java/pl/pazur/port/LauncherActivity.java`, `GameFiles.java` |
| Import recovery and save files | `ImportTransaction.java`, `SaveFiles.java` in that Java directory |
| Native diagnostics | `native/CombatProbe.cpp`; some commands deliberately alter fixtures |
| Engine changes | edit ignored `upstream/OpenClaw/`, then `python tools/export_patch.py` |
| Reproducible dependency revisions | `sources.lock.json`, `patches/` |
| Test tools and reviewed evidence | `tools/`, `docs/validation/` |

Commit the exported patch, not the dependency checkout. Run
`python tools/check_patches.py` after engine edits. Do not reset the dependency
checkout or change its pinned revision to hide a patch mismatch.

## Checks and evidence

Run `python tools/check_repository.py` for source/documentation changes. Production
changes also need the relevant build and behavioral checks: build both ARM ABIs
for native changes, verify APK packaging, test changed input/physics/import paths
on a suitable device. Do not claim a check passed when it was not run. Documentation
or test-tool-only edits do not require rebuilding an unchanged game APK.

Explain the problem, final behavior, exact APK/revision, test setup and limitations.
Keep failed attempts when they affect interpretation. Comments should explain
invariants, lifetime, timing and failure handling, not repeat obvious statements.
Do not label upstream code as newly written by an LLM.

## Several people and phones

Select `ANDROID_SERIAL` in each test process. Only one owner may operate the game
on a particular phone at a time. Never run `adb kill-server` for a device-specific
problem: the server is shared. Do not change USB tethering, reboot or disconnect a
phone supplying internet. Current phone allocation must be agreed for the session;
private serials belong in local environment variables, not committed documentation.

Read [testing scope](docs/TESTING.md). Current ordinary-input campaign driver:
`tools/campaign_play.py`. A resumed natural run must use an unchanged save actually
written by the game. `campaignposition`, `pegtrial`, `combatstage`, `campaignfinish`
and similar fixture commands must not be used as natural-playthrough evidence.
Legacy `checkpoint_smoke.py` uses global Android input and is not an approved
current test. Owned sessions preserve user files; verify restoration after failure.

## Publication boundary

No game archives, extracted maps/art/audio/video, test saves, raw reports, device
identifiers, signing keys or credentials in commits, issues or releases. Follow
[publication checks](docs/PUBLISHING.md). The source license does not grant rights
to redistribute the commercial game. Use a PR for reviewable changes after publication.
