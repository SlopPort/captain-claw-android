#include <SDL.h>
#include <unistd.h>
#include "ClawGameApp.h"
#include "Engine/GameApp/MainLoop.h"

ClawGameApp testApp;
extern "C" int SDL_main(int argc, char** argv) {
    if (argc < 2 || chdir(argv[1]) != 0) {
        SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_ERROR, "Kapitan Pazur", "Nie znaleziono katalogu danych gry.", nullptr);
        return 1;
    }
    SDL_SetHint(SDL_HINT_RENDER_DRIVER, "opengles2");
    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "nearest");
    SDL_SetHint(SDL_HINT_ANDROID_BLOCK_ON_PAUSE, "1");
    SDL_SetMainReady();
    return RunGameEngine(argc, argv);
}
