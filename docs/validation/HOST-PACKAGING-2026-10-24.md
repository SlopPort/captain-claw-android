# Host game-data packaging validation — 2026-10-24

Implemented and checked by OpenAI Codex (LLM), under anonymous human direction. This is a computer-tool change; APK 0.4.32 is unchanged. No phone was accessed.

## Change

Previously, packing opened the final ZIP for immediate truncation. The tool now writes a temporary ZIP in the destination directory, closes it, checks all entry CRCs, flushes it, and replaces the final file only after success. Handled failures remove the temporary file. Forced termination may leave a temporary file, but preserves the previous final ZIP. This does not certify power-loss durability on every filesystem or concurrent packing into the shared working directory.

The preparation window checks input before dependency downloads and uses UTF-8 subprocess output. Missing, truncated, empty and structurally invalid input is rejected. Full REZ plus loose Assets is also rejected: reconstruction uses loose files, not a merge with the original archive. Direct full-REZ import remains available. Structural checks do not certify complete campaign data.

## Evidence

Run `python tools/check_pack_assets.py` from the repository root. Eight groups passed:

1. Five-file ZIP publication, exact contents and CRC checks.
2. Injected ENOSPC during the second entry preserved the previous ZIP.
3. Injected CRC failure preserved the previous ZIP.
4. Injected replacement permission failure preserved the previous ZIP.
5. A real owned child process was terminated after writing its first entry; the previous ZIP survived.
6. Synthetic input files remained byte-identical.
7. Missing/truncated/placeholder input was rejected; synthetic loose-data reconstruction passed.
8. A complete synthetic REZ was accepted, then rejected when partial loose overrides were added.

A separate real local packaging run reconstructed 13,184 files into a 107,297,326-byte REZ and produced a CRC-checked ZIP. Five extensionless source files were skipped under the existing packing rule. A before/after content manifest of the source REZ and loose files was identical. Proprietary data and local reports remain ignored and are not distributed.

ENOSPC was simulated; the actual disk was not filled. The real repack used an existing development computer and local dependencies. This is not an interactive preparation-window test, clean-computer installation test, Android import test or campaign test. A new-user clean-computer trial remains required. No game data or original installation was modified.
