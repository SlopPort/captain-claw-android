# Autorzy i pochodzenie

Pracę nad adaptacją w tej sesji — zmiany kodu, dokumentację, rozpoznanie i wykonanie testów — wykonał agent LLM OpenAI Codex według wymagań i uwag człowieka. Nie jest to deklaracja autorstwa oryginalnego silnika, gry ani bibliotek. [Ustalenia i otwarte problemy](docs/DEVELOPMENT-NOTES.md).

All adaptation work in this session was performed by an LLM coding agent (OpenAI Codex), with human requirements, hardware and feedback. Original upstream authorship and notices are preserved.

Claw Web — Arthur Boss and contributors, https://github.com/arthurboss/claw-web, revision e723d3d48b5ba2cc723751209954cfc46c82d202, GNU GPL v3. Direct REZ import and save export/import workflows are inspired by that project. The event/preset haptics design is adapted from its HapticFeedback implementation; the SDL/Android backend is new. Narrower startup preloading follows its BaseGameApp approach. Existing Android collision, ladder, touch and level 14 work is documented separately. No original game artwork from Claw Web is bundled by these additions.

Nie zakładamy wygaśnięcia praw do danych Claw. Otwarcie kodu adaptacji nie pozwala automatycznie publikować plików oryginalnej gry. Lokalne paczki danych są wyłączone z publicznych źródeł.

SDL_GameControllerDB pochodzi z [mdqinc/SDL_GameControllerDB](https://github.com/mdqinc/SDL_GameControllerDB), na licencji zlib. Rewizję zapisano w sources.lock.json; tekst licencji znajduje się w app/src/main/assets/licenses/SDL_GameControllerDB-Zlib.txt.

Projekt jest adaptacją [OpenClaw](https://github.com/pjasicek/OpenClaw) autorstwa pjasicek i współtwórców. Wykorzystuje istniejący silnik, Box2D, libwap, TinyXML, modele aktorów i podstawową rozgrywkę. GPL-3.0 silnika i adaptacji znajduje się w `LICENSE.txt`.

SDL, SDL_image, SDL_mixer i SDL_ttf pochodzą z repozytoriów libsdl-org; SDL2_gfx z ferzkopp/SDL2_gfx. Dokładne rewizje zapisano w `sources.lock.json`. Licencje bibliotek, FreeType, FreePats oraz TiMidity znajdują się również w `app/src/main/assets/licenses/` i są pakowane w APK. Box2D i libwap pozostają w przypiętym drzewie OpenClaw, wraz z ich informacjami o autorach.

Gradle Wrapper pochodzi z Gradle 8.10.2; jego informacje licencyjne i NOTICE są w `licenses/gradle-wrapper/`. Jest narzędziem budowania, nie częścią uruchamianej gry.

Kapitan Pazur / Claw, jego postacie, grafiki, dźwięki, muzyka i mapy pochodzą z gry Monolith Productions. Licencja GPL kodu nie nadaje praw do danych komercyjnej gry. Repozytorium nie zawiera CLAW.REZ, oryginalnej instalacji, filmów ani wygenerowanego `game-data.zip`. Użytkownik dostarcza własne dane gry.

REA (`morluto/rea`) służyło do pomocniczego rozpoznania lokalnej instalacji; nie jest silnikiem gry ani zależnością czasu działania. Zestawienia awesome i tematy GitHub wskazane w opisie prac były źródłami rozpoznania, a nie autorami natywnego portu. Szczegółowy zakres zmian opisuje `docs/UPSTREAM-DIFF.md`.
