#include <SDL.h>
#include <unistd.h>
#include <cstring>
#include "ClawGameApp.h"
#include "Engine/GameApp/MainLoop.h"

ClawGameApp testApp;
extern "C" int SDL_main(int argc, char** argv) {
    // Java has already presented a localized recovery screen. Return without
    // initializing SDL/game data when its off-UI-thread preparation failed.
    if(argc==2 && std::strcmp(argv[1],"--startup-aborted")==0)return 0;
    if (argc < 2 || chdir(argv[1]) != 0) {
        SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_ERROR, "Kapitan Pazur", "Nie znaleziono katalogu danych gry.", nullptr);
        return 1;
    }
    SDL_SetHint(SDL_HINT_RENDER_DRIVER, "opengles2");
    // SDL disables its draw queue when a renderer is chosen explicitly. We use
    // only SDL rendering APIs, so batching can keep draw order/state intact while
    // avoiding a driver submission for each individual tile/sprite. The local
    // opt-out file exists for device A/B measurements and driver fallback.
    const bool batching=access("render-batching-off",F_OK)!=0;
    SDL_SetHint(SDL_HINT_RENDER_BATCHING,batching?"1":"0");
    SDL_Log("Pazur renderer batching: %d",batching);
    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "nearest");
    SDL_SetHint(SDL_HINT_ANDROID_BLOCK_ON_PAUSE, "1");
    SDL_SetMainReady();
    return RunGameEngine(argc, argv);
}
