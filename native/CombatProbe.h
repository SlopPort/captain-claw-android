#pragma once
#include "Engine/GameApp/BaseGameLogic.h"

namespace PazurCombatProbe {
// Diagnostic commands are enabled only by the explicit preview/debug option.
bool Handle(const std::vector<std::string>& args, const ActorMap& actors);
void Poll();
void ResetKeys();
void JumpInput(bool down, Uint32 eventTime);
}
