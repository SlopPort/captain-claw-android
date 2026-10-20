#pragma once
#include <SDL.h>

namespace PazurInput {
enum Source { Touch, Controller };
void SetKey(Source source,SDL_Keycode key,bool down);
void Reset(Source source);
void Repeat(Source source,SDL_Keycode key);
}
