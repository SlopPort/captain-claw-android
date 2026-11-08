#pragma once
#include "Engine/Actor/Components/EnemyAI/EnemyAIStateComponent.h"
#include "OriginalMeleePolicy.h"
#include <set>

// Registered under the existing MeleeAttack component ID, so the engine's
// contact listener and diagnostics continue to find the same state. Ordinary
// enemies retain the upstream implementation unless their XML opts in.
class OriginalMeleeAttackAIStateComponent final : public MeleeAttackAIStateComponent {
public:
    bool VDelegateInit(TiXmlElement*) override;
    bool VCanEnter() override;
    void VUpdate(uint32 ms) override;
    void VOnStateEnter(BaseEnemyAIStateComponent*) override;
    void VOnStateLeave(BaseEnemyAIStateComponent*) override;
    void VExecuteAttack() override;
    void VOnAttackFrame(std::shared_ptr<EnemyAttackAction>, Direction, const Point&) override;
    void VOnAnimationFrameChanged(Animation*, AnimationFrame*, AnimationFrame*) override;
    void VOnAnimationLooped(Animation*) override;
private:
    enum class Policy { Upstream, Crab, Fish, Tiger };
    Policy policy = Policy::Upstream;
    OriginalMeleePolicy::TigerMove tigerMove = OriginalMeleePolicy::TigerMove::Knife;
    uint64_t clock = 0, nextEntry = 0, moveStarted = 0;
    int repeats = 0, direction = -1;
    bool finishing = false, damageWindow = false, soundPlayed = false;
    bool entryWakePending = false;
    double targetX = 0, startX = 0;
    std::string customAnimation;
    std::set<int> hitActors;
    std::set<int> committedTargets;
    Point windowSize, windowOffset;
    unsigned windowDamage = 0;
    void BeginCustomMove(const char* reason);
    void FinishCustomMove();
    void SetWindow(bool enabled, const Point& offset, const Point& size, unsigned damage);
    void TestDamageWindow();
    bool IsCurrentAnimation(Animation*) const;
};
