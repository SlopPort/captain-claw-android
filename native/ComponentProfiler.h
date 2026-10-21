#pragma once
#include <SDL.h>
namespace PazurProfile {
extern bool components;
void Start();
void Record(const char* name,Uint64 ticks);
void Poll();
}
