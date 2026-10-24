# Credits and provenance

All adaptation work in this development session — code changes, documentation, investigation and automated test execution — was performed by **OpenAI Codex, an LLM coding agent**, guided by an anonymous human's requirements, hardware and feedback. This does not claim authorship of the original game, OpenClaw or its dependencies. Their authorship and notices remain intact. See [development notes](docs/DEVELOPMENT-NOTES.md).

## Original work in this adaptation

The two Android credit cards and their small bitmap alphabet are original generated assets by OpenAI Codex, under the adaptation's GPL-3.0 license. They replace missing legacy menu PNGs without copying upstream portraits or commercial game artwork. Their source generator is `tools/credits_png.py`.

The geometric Android application icon (`app/src/main/res/drawable/ic_port.xml`) is original vector artwork by OpenAI Codex (LLM), GPL-3.0. It contains no original Claw artwork or Monolith logo.

## Open-source projects

- **OpenClaw**, pjasicek and contributors: [repository](https://github.com/pjasicek/OpenClaw). This adaptation uses its C++/SDL engine, Box2D/libwap integration, TinyXML, actor models and much of its gameplay. The engine and adaptation use GPL-3.0; see `LICENSE.txt`.
- **Claw Web**, Arthur Boss and contributors: [repository](https://github.com/arthurboss/claw-web), revision `e723d3d48b5ba2cc723751209954cfc46c82d202`, GNU GPL v3. Direct REZ import and save export/import workflows are inspired by that project. The event/preset haptics design is adapted from its HapticFeedback implementation; the SDL/Android backend is new. Narrower startup preloading follows its BaseGameApp approach. Existing Android collision, ladder, touch and level 14 work is documented separately. No original game artwork from Claw Web is bundled by these additions.
- **SDL_GameControllerDB**: [mdqinc/SDL_GameControllerDB](https://github.com/mdqinc/SDL_GameControllerDB), zlib license. Its pinned revision is in `sources.lock.json`; the license text is `app/src/main/assets/licenses/SDL_GameControllerDB-Zlib.txt`.
- **SDL, SDL_image, SDL_mixer and SDL_ttf** come from libsdl-org repositories; **SDL2_gfx** comes from ferzkopp/SDL2_gfx. Exact revisions are in `sources.lock.json`. Notices for these libraries, FreeType, FreePats and TiMidity are retained in `app/src/main/assets/licenses/` and packaged in the APK. Box2D and libwap remain in the pinned OpenClaw tree with their authorship notices.
- **Gradle Wrapper**, Gradle 8.10.2: license and NOTICE files are in `licenses/gradle-wrapper/`. This is a build tool, not part of the running game.

## Commercial game data

Captain Claw / Kapitan Pazur / Claw, its characters, graphics, sounds, music and maps originate in the Monolith Productions game. The source code's GPL license does not grant rights to redistribute these commercial assets. Copyright expiry is not assumed.

Public sources exclude `CLAW.REZ`, the original installation, extracted game resources, movies and generated `game-data.zip`. Players supply their own game data. Local data packages are excluded from publication; making the adaptation open source does not make the commercial game data open source.

## Investigation tools and references

[REA](https://github.com/morluto/rea) assisted investigation of the local installation; it is neither the game engine nor a runtime dependency. Static examination of a local executable is not recovered original Monolith source. See [the scoped REA findings](docs/ORIGINAL-BEHAVIOR-REA.md).

The research lists [awesome-game-decompilations](https://github.com/CharlotteCross1998/awesome-game-decompilations), [open-source-games](https://github.com/bobeff/open-source-games), [awesome-reverse-engineering](https://github.com/morluto/awesome-reverse-engineering) and GitHub topics android-ports/android-reverse were discovery references, not authors of this native port. The adaptation's scope is recorded in [upstream differences](docs/UPSTREAM-DIFF.en.md).
