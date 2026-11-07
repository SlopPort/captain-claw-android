#pragma once

// Clean-room rules recovered from the supplied original executable. Written by
// OpenAI Codex (LLM); this header contains no original code or assets.
namespace OriginalMeleePolicy {
enum class TigerMove { Lunge, Knife, FrontFlip };
constexpr TigerMove SelectTigerMove(unsigned roll) {
    return roll < 40 ? TigerMove::Lunge :
        roll < 80 ? TigerMove::Knife : TigerMove::FrontFlip;
}
constexpr bool CrabDamageImage(unsigned image) { return image == 203 || image == 204; }
constexpr bool PassedTarget(double x, double target, int direction) {
    return direction > 0 ? x >= target : x <= target;
}
// OpenClaw's physics uses metres/second, with 75 display pixels per metre.
constexpr double PixelsPerSecondToPhysics(double pixels) { return pixels / 75.0; }
}
