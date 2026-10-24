# Rejected image-ownership experiment

Baseline source: `9fa0738732c0da611f1c7d497a5e6d75f0dc7a2f` (0.4.17). `RenderBoundsProbe.h`, `integration.patch` and `perf_smoke.py` retain the diagnostic implementation. The patch adds its 0/1 mailbox command and compiles as a separate 0.4.18 diagnostic candidate. It is not applied by the current build.

The cached image already had a strong owner during rectangle calculation. The experiment compared direct borrowing with the inherited weak/shared pointer round trip, without caching geometry or changing draw order. Off/on/off 90-second runs produced post-initial-batch harmonic mean FPS 58.735 / 59.043 / 58.525; render-time difference was about 0.03 ms. No useful gain was established. [Exact APK and method](../../../docs/validation/ATOMIC-PROGRESS-0.4.18.md).

For source review/research only: use a separate copy of the baseline with its locked dependencies/normal patches prepared, copy the header to native/, then review/apply this archival integration patch there. `perf_smoke.py` needs that copy's tools/ on PYTHONPATH and explicit ANDROID_SERIAL. Archival patch application was checked against normalized LF baseline copies; this is not a promise of byte-identical APK output across build paths. Commercial data must be supplied independently.
