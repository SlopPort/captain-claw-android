#pragma once
#include <SDL.h>

namespace PazurTouch {
bool Handle(const SDL_Event& event);
void Draw(SDL_Renderer* renderer);
void Reset();
void Shutdown();
void Update();
}
