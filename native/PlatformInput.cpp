#include "PlatformInput.h"
#include "Engine/GameApp/BaseGameApp.h"
#include <set>

namespace {
// Accessed only on the SDL game thread. Each source owns its own held keys.
// Dispatch immediately: re-queueing events here adds another frame of input delay.
std::set<SDL_Keycode> keys[2];
void dispatch(SDL_Keycode key,bool down,bool repeat=false) {
    SDL_Event event{};
    event.type=down?SDL_KEYDOWN:SDL_KEYUP;
    event.key.state=down?SDL_PRESSED:SDL_RELEASED;
    event.key.repeat=repeat;
    event.key.timestamp=SDL_GetTicks();
    event.key.keysym.sym=key;
    event.key.keysym.scancode=SDL_GetScancodeFromKey(key);
    g_pApp->OnEvent(event);
}
}
void PazurInput::SetKey(Source source,SDL_Keycode key,bool down) {
    // The game sees the union: lifting a touch must not cancel a held pad button.
    const bool before=keys[0].count(key)||keys[1].count(key);
    if (down) keys[source].insert(key); else keys[source].erase(key);
    const bool after=keys[0].count(key)||keys[1].count(key);
    if (before!=after) dispatch(key,after);
}
void PazurInput::Reset(Source source) {
    // Copy before releasing because SetKey mutates the original set.
    const auto previous=keys[source];
    for (auto key:previous) SetKey(source,key,false);
}
void PazurInput::Repeat(Source source,SDL_Keycode key) {
    if (keys[source].count(key)) dispatch(key,true,true);
}
