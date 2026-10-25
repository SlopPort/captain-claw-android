#pragma once
#include <SDL.h>
class b2Body;
class PhysicsComponent;
namespace PazurRecorder {
void Input(const SDL_Event& event);
void Sample(b2Body* body, PhysicsComponent* physics, int level, Uint32 stepMs);
}
