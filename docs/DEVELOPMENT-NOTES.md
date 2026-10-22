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

User feedback after 0.4.5: configurable controller input works well. The next reported bug was repeated climbing at the top of level 1's first ladder, plus PAD obscuring health. Version 0.4.6 fixes the ladder attachment/exit condition and moves PAD to bottom centre. Actual-map and isolated checks passed; exact original Windows behavior remains unverified. A separate held-direction menu repeat defect was found and fixed. Detailed evidence and intermediate failed fixtures: [LADDERS.md](validation/LADDERS.md).

- Finish real GameSir Nova 2 Lite gameplay button, axis, pause, disconnect and reconnect checks. Redmi identified Wireless Controller; Huawei paired in red Switch mode as Pro Controller, and the user confirmed menu navigation. A connected device is not yet a passed gameplay test.
- A Huawei menu-exit test exposed a crash from Android process-wide exit inside the event callback. The Android path now unwinds the loop and releases controller/touch state. Three automated exit/relaunch cycles passed; other shutdown scenarios still need coverage.
- The user also found that the controller stopped responding after opening pause on level 1. Rendering continued: the input context missed the engine's SetRunning(false) pause flag while GameState remained IngameRunning. That flag combination now selects menu input. Three automated pause/menu-direction/resume cycles passed; physical confirmation after the fix is pending. The test checks actual direction events, not just mailbox acknowledgements.
- Complete a natural playthrough of all levels. Existing controlled enemy and collision scenarios are documented in `validation/COMBAT-AUDIT.md`; they do not establish that every encounter is correct.
- Revisit the intermittent level 7 projectile assertion if it returns. A guard was added; the original root cause is not conclusively established.
- Test installation instructions from a clean computer. The user confirmed the prepared ZIP import on Huawei. Version 0.4.8 also accepts a complete REZ; automated runtime checks passed, but manual picker validation of this new route remains pending.
- English installation documentation is provided; in-game text and all historical developer documents are not yet fully translated.
- Keep comments focused on reasons, invariants, lifetime and failure handling. Do not label inherited code as LLM-authored or add a comment to every obvious statement. Document remaining gaps instead of claiming that every source line has been reviewed.

## Huawei P9 Lite, 2 GB RAM, LineageOS Android 10

Update 0.4.8: the user confirmed ZIP installation and configurable controller gameplay. Automated map-start, collision, ladder and performance checks have now run on this phone; results and remaining limits are in [PORT-0.4.8.md](validation/PORT-0.4.8.md). Long natural play and stable 60 FPS throughout every map remain unverified. The paragraphs below retain the original test plan as historical context, not the current test status.

Planned device test, not yet performed. Record the exact model/build and actual CPU architecture from the device rather than assuming it from the product name. Use the same APK and data for comparisons. Preserve saves and normal settings before diagnostics.

Initial connection on 2026-10-20: device reports VNS-L21, Android 10, ARM64 and ARMv7 support, MemTotal 1,821,440 kB. Version 0.4.4-dev installed successfully. The prepared data ZIP was copied into Downloads for the normal file-picker import test. Import, gameplay and performance results remain pending; installation alone is not a successful gameplay test.

Measure cold launch/import, level load time, warmed gameplay on levels 1 and 13, frame-time spikes, process memory, 20–30 minutes of play, background/resume and Bluetooth input. Record temperature or throttling where available. Check whether other apps are being killed and whether the game survives returning from the background. A short average FPS sample is insufficient for a 2 GB phone.

If performance is poor, profile first. Candidates include rendering resolution, visible sprite work, texture memory, asset loading, audio and expensive AI/physics updates. Change one factor at a time; compare the same scene and preserve readable graphics, correct collisions and game speed. No optimization gains on this device are claimed before measurement.

Planowany test, jeszcze niewykonany. Najpierw sprawdzamy model, system i architekturę, następnie czas uruchamiania, ładowanie poziomów, płynność poziomów 1 i 13, zużycie pamięci, dłuższą grę, powrót z tła i pada. Optymalizacje dobieramy do wyników, bez obietnicy konkretnej liczby FPS.


## 2026-10-22: remaining rendering hypothesis / Dalszy kierunek renderowania

Source inspection only, no implementation or speedup claim: `Image::GetTextureFromPid` builds an RGBA surface for every decoded PID; `Util::CreateRGBSurface` supplies an alpha mask; pinned SDL enables surface blending for that mask and copies the blend mode into the texture. A fully opaque tile can therefore still use blending. The next candidate is to classify actual decoded tile pixels once during loading and test blend-NONE only for images proven entirely opaque, keeping original textures, UVs, draw order and uniform scaling. Actor opacity/color changes must retain their original behavior. Actual eligible-tile counts, exact image comparisons on real drivers and same-APK A/B/A timing are required before promotion. This is distinct from the rejected atlas and has no measured benefit yet.

Po przeglądzie kodu kolejnym kandydatem do pomiaru jest pominięcie mieszania przezroczystości wyłącznie dla kafelków, których wszystkie piksele są potwierdzone jako nieprzezroczyste. Nie wdrożono tego i nie przypisano żadnego zysku FPS. Wymagane są rzeczywiste porównania obrazu i wydajności; zachowanie przezroczystych kafelków i postaci pozostaje warunkiem.
