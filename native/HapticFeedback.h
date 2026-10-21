#pragma once
// Event/preset design adapted from arthurboss/claw-web, e723d3d, GPLv3.
// Arthur Boss and contributors; Android/SDL backend by OpenAI Codex (LLM).
namespace PazurHaptics {
enum Preset { Light, Jump, Attack, Damage, Explosion, Landing };
void Trigger(Preset preset);
}
