# Rejected tile-atlas experiment

Baseline source: `2973d95` (0.4.19). The last diagnostic iteration is preserved as `TileAtlas.h`, `integration.patch` and `pixel_smoke.py`. New code is by OpenAI Codex (LLM), GPL-3.0; baseline OpenClaw/SDL authorship remains unchanged. This archive is **not compiled into the game**.

The experiment packed immutable nearest-sampled tile textures into bounded render targets to reduce texture switches without reordering tiles or changing physics/AI. It retained original textures for fallback, preserved blend modes, invalidated targets after renderer resets and capped allocations at 8 MiB per plane / 16 MiB globally. The registry uses process-lifetime storage to avoid global-destruction ordering problems; scene-owned textures are explicitly released.

GPU readback on the API-21 software-rendered emulator rejected it:

- Non-power-of-two layouts differed from original output at 2.25x scaling.
- Power-of-two alignment reduced differences; the level-one case passed at 1x/2.25x, but level nine still differed.
- The last 512x512 page variant matched the level-one sample at 1x, 2x, 2.125x, 2.25x and 3x, but differed at **1.5x**: 937 background, 687 action and 119 foreground pixels. It failed the unchanged zero-difference gate.

Last rejected APK SHA-256 `4d4f8ea595a275eb17150eb390c5da978c5c4493c14b44b71f6099354d5229a6`. Local reports `tile-atlas-api21-0.4.20-r6` retain results. No FPS improvement is claimed, and it was never installed on the physical phone. These test samples are not a proof over every fractional destination phase or GPU; that is another reason not to promote the code.

For isolated research only: prepare a separate baseline copy and locked dependencies, copy this header to native/, review/apply the archival integration patch, and build the x86_64 diagnostic APK. The pixel script needs the copy's tools/ on PYTHONPATH and explicit ANDROID_SERIAL. The failed pixel gate is expected on the tested configuration. Patch application was checked against LF-normalized baseline copies, not against arbitrary newer sources; no byte-reproducible APK claim is made. No commercial assets are provided.

Po polsku: pomysł ograniczał przełączanie tekstur, ale zmieniał część pikseli przy wybranych skalach. Został odrzucony i usunięty z gry przed testem telefonu. Kod zostaje otwarty jako dokumentacja próby, a nie gotowa optymalizacja.
