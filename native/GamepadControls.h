#pragma once
#include <SDL.h>
#include <string>
#include <vector>

namespace PazurGamepad {
void Initialize();
bool Handle(const SDL_Event& event);
void Update();
bool UsingController();
void UseTouch();
bool DebugCommand(const std::vector<std::string>& args);
}
