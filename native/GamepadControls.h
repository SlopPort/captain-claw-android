#pragma once
#include <SDL.h>
#include <string>
#include <vector>

namespace PazurGamepad {
void Initialize();
void Shutdown();
bool Handle(const SDL_Event& event);
void Update();
bool UsingController();
void UseTouch();
void Rumble(int durationMs);
bool DebugCommand(const std::vector<std::string>& args);
}
