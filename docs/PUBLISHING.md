# Publication

Destination: public `SlopPort/captain-claw-android`. This is the Captain Claw
Android adaptation only; another project's concurrent publication must use its
own repository and local checkout. Do not change global credentials, global Git
identity, another project's remote, or force-push shared history.

The adaptation source is GPL-3.0, with dependency-specific licenses retained in
`NOTICE.md`, `licenses/` and packaged license notices. This is not a license for
the commercial Claw game. Do not assume copyright expiry. Do not publish CLAW.REZ,
extracted game resources, maps, music, speech, videos or game-data.zip. OpenClaw
and other upstream authors retain attribution. Adaptation work so far is explicitly
credited to OpenAI Codex (LLM), with human requirements and feedback.

Before publishing new changes:

1. `python tools/check_repository.py` checks tracked/staged source files.
2. `python tools/check_public_history.py` scans reachable historical blobs and
   changed paths, including removed files. Optionally supply a local ignored
   `--private-pattern-file` containing identifiers that must not be published.
   Never commit this pattern file. This heuristic does not replace reviewing art,
   licenses, binary provenance and intended public content.
3. Review `git diff --cached`, `git status`, authors and the exact remote. Raw
   reports, screenshots, player saves, signing keys and credentials stay local.
4. Authenticate the intended account through the normal Git/browser login flow.
   A browser login is not automatically a Git login. Never paste tokens into an
   issue, commit, remote URL, script or chat. Do not reuse another account by accident.
5. Push the reviewed branch normally to the verified project repository. For a
   first publication, use an empty repository; never overwrite unrelated work.

Keep APK releases separate from source publication. The current APK is a debug
signed development build; do not label it a final 1.0 or silently change its signing
key for existing users. Any later binary release must identify its exact source
revision, checksums, source availability, license notices, validation and limitations.
No commercial game-data bundle is a release asset.

Historical first-publication audit: the initial local reachable-history scan inspected
596 blobs (5,679,023 bytes), found none of its excluded paths/credential/private
identifier patterns, and showed adaptation commits authored as Codex. This is a
bounded scan result, not a comprehensive legal or security guarantee. Rerun for each publication batch. Do not put a person's real name in project
credits or commit identity without their request; upstream attribution is preserved.


Scanner validation: four isolated host Git fixtures passed
(clean history, deleted data file retained in history, deleted dummy credential
retained in history, private identifier pattern). Fixture credentials were fake;
no actual game archive or real token was added. Raw fixture reports remain local.
