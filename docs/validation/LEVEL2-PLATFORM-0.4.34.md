# Level 2 platform blockage â€” open investigation

OpenAI Codex (LLM), 2026-10-25, following an anonymous human report and private video. This report does not claim a collision fix.

## Observation

The human reports running in place while holding left on a small wooden platform with a crate below a Soldier. They did not try jumping in this occurrence. The video shows changing run animation without visible horizontal progress. A live screenshot matched the map neighborhood around the crate at (2460, 4956), below the Soldier initially placed at (2524, 4784). The screenshot establishes the location, not an exact live physics coordinate. Debug combat diagnostics were disabled during the human session; the transient contact state could not be read before a restart.

Private video, screenshots and map dumps remain outside Git. Map investigation used the user's own data. The local map reader initially failed with an incompatible DLL search path; selecting its matching UCRT runtime resolved this host-tool problem.

## Reproduction attempts on Huawei ARM64 debug 0.4.33

The real level map was used with explicitly teleported setup positions and ordinary timed SDL movement/jump events. This is technical fixture coverage, not campaign progression.

- Four horizontal walking cases crossed the internal platform join. Long rightward movement stopped at the real wall; long leftward movement fell to the lower floor as expected.
- Seven jump-entry timings were tried from the lower floor. Four reached the upper platform and could walk left afterward; three remained on the lower floor and also moved left. None reproduced the reported block.
- Six synthetic starting depths (Y4923 through Y4942) settled back to the upper surface and crossed left. These forced positions are not proof that all natural landing states recover.

The report remains open. Passing fixture cases do not invalidate the human recording and do not justify another speculative change to foot shape or collision tolerance.

## Live capture for the next occurrence

Debug 0.4.34 adds a read-only one-shot collision snapshot. It does not require PreviewIncompleteLevel14, enable combat fixtures, inject input, teleport, change health or write saves. Every 250 ms during physics updates, the debug build checks for a request file. A request produces hero position/velocity/ground state, fixture bounds and enabled/touching contact normals. This is compiled out when NDEBUG is defined; no release performance certification is implied.

Select only an allocated device through process-local ANDROID_SERIAL, then run:

```sh
python tools/capture_collision.py --report UNIQUE-LOCAL-REPORT
```

The game must be running and unpaused. Leave Claw blocked without jumping, changing direction or restarting until capture completes. Output and screenshot remain in ignored reports; inspect and redact before sharing. Existing capture files cause refusal rather than overwrite. A timed-out owner removes only its own pending request.

Configuration and saves were restored and byte-checked after each fixture. The normal game is reopened after diagnostic validation. The public signed test APK remains 0.4.32; this diagnostic debug update is not a public release or a fix for the recorded issue.

## Capture validation

ARM64 debug build and in-place Huawei installation passed. APK SHA256: `ec3310afba44c3ba003d65e44843a5dc9e2977cf986b7f7cd7300fdcc1571892`. In a temporary level 2 startup session with PreviewIncompleteLevel14 explicitly false, the capture produced hero state, five fixture records and three contact records, including non-touching contacts with zero normals. The request was consumed and the tool removed its output after copying it locally. Original configuration and saves were restored and byte-checked. No other device was used. The capture was tested on a stationary supported hero, not on the unresolved blocked state.
