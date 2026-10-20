# Development notes / Uwagi o pracy

## Transparency / Transparentność

All adaptation work in this development session — code changes, documentation, investigation and execution of automated tests — was performed by an LLM coding agent (OpenAI Codex). The human supplied the goal, requirements, original game installation, hardware and feedback. This does not make the LLM the author of upstream OpenClaw or its dependencies. Their original attribution remains intact. Human device feedback is distinguished from automated measurements. LLM-generated code and explanations can contain mistakes.

Całą pracę nad adaptacją w tej sesji — zmiany kodu, dokumentację, rozpoznanie problemów i uruchamianie testów automatycznych — wykonał agent LLM (OpenAI Codex). Człowiek dostarczył cel, wymagania, instalację gry, sprzęt i uwagi. Silnik OpenClaw i biblioteki pochodzą od ich dotychczasowych autorów. Nie przypisujemy ich pracy LLM. Wyniki automatyczne nie zastępują pełnego przejścia gry przez człowieka. Kod i opisy wygenerowane przez LLM mogą zawierać błędy.

## Findings / Ustalenia

- Touch events previously entered a second event queue; direct dispatch reduced measured native event-to-movement delay. This is not a measurement of complete physical screen latency.
- Sliding a finger off jump previously released jump and activated another action. Action ownership now lasts until that finger lifts or is cancelled.
- Brief jump taps used to produce very small jumps. Touch holds are now at least 110 ms; holding longer still increases height. Exact equivalence with the original Windows game has not been established.
- Drawing larger touch controls every frame reduced performance. Cached button textures restored the earlier performance range; level 13 remains slower than level 1.
- Touch and controller keys need separate ownership: releasing one source must not release a key still held by the other. See `native/PlatformInput.cpp`.
- Controller support uses SDL and a pinned Android subset of SDL_GameControllerDB. Bluetooth and USB share this input path; implementing both does not prove that both were tested on hardware.

## Open checks / Otwarte sprawdzenia

- Finish real GameSir Nova 2 Lite button, axis, pause, disconnect and reconnect checks. Android identifies the paired device as Wireless Controller. A connected device is not yet a passed gameplay test.
- Complete a natural playthrough of all levels. Existing controlled enemy and collision scenarios are documented in `validation/COMBAT-AUDIT.md`; they do not establish that every encounter is correct.
- Revisit the intermittent level 7 projectile assertion if it returns. A guard was added; the original root cause is not conclusively established.
- Test installation instructions from a clean phone and a clean computer. Current import requires a prepared ZIP; this is a known usability limitation.
- English installation documentation is provided; in-game text and all historical developer documents are not yet fully translated.
- Keep comments focused on reasons, invariants, lifetime and failure handling. Do not label inherited code as LLM-authored or add a comment to every obvious statement. Document remaining gaps instead of claiming that every source line has been reviewed.

## Huawei P9 Lite, 2 GB RAM, LineageOS Android 10

Planned device test, not yet performed. Record the exact model/build and actual CPU architecture from the device rather than assuming it from the product name. Use the same APK and data for comparisons. Preserve saves and normal settings before diagnostics.

Initial connection on 2026-10-20: device reports VNS-L21, Android 10, ARM64 and ARMv7 support, MemTotal 1,821,440 kB. Version 0.4.4-dev installed successfully. The prepared data ZIP was copied into Downloads for the normal file-picker import test. Import, gameplay and performance results remain pending; installation alone is not a successful gameplay test.

Measure cold launch/import, level load time, warmed gameplay on levels 1 and 13, frame-time spikes, process memory, 20–30 minutes of play, background/resume and Bluetooth input. Record temperature or throttling where available. Check whether other apps are being killed and whether the game survives returning from the background. A short average FPS sample is insufficient for a 2 GB phone.

If performance is poor, profile first. Candidates include rendering resolution, visible sprite work, texture memory, asset loading, audio and expensive AI/physics updates. Change one factor at a time; compare the same scene and preserve readable graphics, correct collisions and game speed. No optimization gains on this device are claimed before measurement.

Planowany test, jeszcze niewykonany. Najpierw sprawdzamy model, system i architekturę, następnie czas uruchamiania, ładowanie poziomów, płynność poziomów 1 i 13, zużycie pamięci, dłuższą grę, powrót z tła i pada. Optymalizacje dobieramy do wyników, bez obietnicy konkretnej liczby FPS.
