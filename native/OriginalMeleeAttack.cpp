#include "OriginalMeleeAttack.h"
#include "Engine/Actor/Actor.h"
#include "Engine/Actor/Components/PositionComponent.h"
#include "Engine/Actor/Components/RenderComponent.h"
#include "Engine/Actor/Components/PhysicsComponent.h"
#include "Engine/Actor/Components/Animation.h"
#include "Engine/Actor/Components/EnemyAI/EnemyAIComponent.h"
#include "Engine/GameApp/BaseGameApp.h"
#include "Engine/GameApp/BaseGameLogic.h"
#include "Engine/Physics/ClawPhysics.h"
#include "Engine/Util/Util.h"
#include <tinyxml.h>

bool OriginalMeleeAttackAIStateComponent::VDelegateInit(TiXmlElement* data) {
    if (!MeleeAttackAIStateComponent::VDelegateInit(data)) return false;
    std::string name;
    ParseValueFromXmlElem(&name, data->FirstChildElement("OriginalAttackPolicy"));
    if (name == "HermitCrabWindow") policy = Policy::Crab;
    else if (name == "FishLunge") policy = Policy::Fish;
    else if (name == "TigerMoves") policy = Policy::Tiger;
    else if (!name.empty()) return false;
    return true;
}

bool OriginalMeleeAttackAIStateComponent::VCanEnter() {
    if (finishing) return false;
    // A committed move continues if its target leaves the sensor. Entry still
    // requires the normal hostile sensor and an unobstructed line of sight.
    if (m_IsActive && (policy == Policy::Tiger || policy == Policy::Fish)) return true;
    if (policy == Policy::Tiger && clock < nextEntry) return false;
    return MeleeAttackAIStateComponent::VCanEnter();
}

void OriginalMeleeAttackAIStateComponent::VOnStateEnter(BaseEnemyAIStateComponent* previous) {
    finishing = false;
    committedTargets.clear();
    if (policy != Policy::Upstream)
        for (auto* target : m_EnemyAgroList)
            if (target) committedTargets.insert(target->GetGUID());
    if (policy == Policy::Tiger || policy == Policy::Fish) {
        m_IsActive = true;
        const auto offset = FindClosestHostileActorOffset();
        direction = offset.x >= 0 ? 1 : -1;
        m_pRenderComponent->SetMirrored(direction > 0);
        targetX = m_pPositionComponent->GetPosition().x + offset.x;
        if (policy == Policy::Tiger) {
            // Original 0x4988e0: modulo 751 + 1250, then modulo 101 with
            // thresholds 40 and 80. This is an entry gate, not a frame delay.
            nextEntry = clock + Util::GetRandomNumber(1250, 2000);
            entryWakePending = true;
            tigerMove = OriginalMeleePolicy::SelectTigerMove(Util::GetRandomNumber(0, 100));
            repeats = tigerMove == OriginalMeleePolicy::TigerMove::Knife ?
                Util::GetRandomNumber(2, 4) : 1;
        }
        BeginCustomMove();
        return;
    }
    MeleeAttackAIStateComponent::VOnStateEnter(previous);
}

void OriginalMeleeAttackAIStateComponent::VOnStateLeave(BaseEnemyAIStateComponent* next) {
    SetWindow(false, Point(), Point(), 0);
    committedTargets.clear();
    if (policy == Policy::Tiger || policy == Policy::Fish) {
        // Cancel horizontal attack travel on damage, death or any other state
        // transition. Keep gravity/falling velocity under the engine's control.
        auto velocity = m_pPhysicsComponent->GetVelocity();
        velocity.x = 0;
        m_pPhysicsComponent->SetVelocity(velocity);
    }
    MeleeAttackAIStateComponent::VOnStateLeave(next);
}

void OriginalMeleeAttackAIStateComponent::VExecuteAttack() {
    MeleeAttackAIStateComponent::VExecuteAttack();
    if (policy == Policy::Crab)
        SetWindow(false, Point(), Point(), 0);
}

void OriginalMeleeAttackAIStateComponent::VOnAttackFrame(
    std::shared_ptr<EnemyAttackAction> attack, Direction dir, const Point& offset) {
    if (policy != Policy::Crab) {
        MeleeAttackAIStateComponent::VOnAttackFrame(attack, dir, offset);
        return;
    }
    // The original crab exposes one moving rectangle during images 203/204.
    // Do not spawn the upstream 50 ms stationary damage actor as well.
    direction = dir == Direction_Right ? 1 : -1;
    SetWindow(true, offset, attack->attackAreaSize, attack->damage);
    Util::PlayRandomSoundFromList(m_pEnemyAIComponent->GetMeleeAttackSounds());
}

bool OriginalMeleeAttackAIStateComponent::IsCurrentAnimation(Animation* animation) const {
    return m_IsActive && animation == m_pAnimationComponent->GetCurrentAnimation().get();
}

void OriginalMeleeAttackAIStateComponent::BeginCustomMove() {
    moveStarted = clock;
    startX = m_pPositionComponent->GetPosition().x;
    soundPlayed = false;
    SetWindow(false, Point(), Point(), 0);
    auto velocity = m_pPhysicsComponent->GetVelocity();
    velocity.x = 0;
    if (policy == Policy::Fish) {
        // Strike entry 0x4440c0 exposes the damage rectangle immediately and
        // travels horizontally at 180 px/s until crossing the captured target X.
        customAnimation = "strike1";
        velocity.x = direction * OriginalMeleePolicy::PixelsPerSecondToPhysics(180);
        auto attack = m_AttackActions.front();
        Point offset = attack->attackSpawnPositionOffset;
        if (direction > 0) offset.x *= -1;
        SetWindow(true, offset, attack->attackAreaSize, attack->damage);
    } else if (tigerMove == OriginalMeleePolicy::TigerMove::Knife) {
        customAnimation = "strike1";
    } else if (tigerMove == OriginalMeleePolicy::TigerMove::Lunge) {
        customAnimation = "strike3";
        // Original 0x498b70 holds still on initial image 800 (500 ms).
        // Travel begins on image 400, not at entry into the wind-up.
        velocity.x = 0;
    } else {
        // Original front-flip is sprite-animated horizontal travel, not the
        // previous generic roll with a new physical jump impulse.
        customAnimation = "frontflip";
        targetX = startX + direction * 100;
        velocity.x = direction * OriginalMeleePolicy::PixelsPerSecondToPhysics(250);
    }
    m_pAnimationComponent->SetAnimation(customAnimation);
    m_pAnimationComponent->ResetAnimation();
    m_pAnimationComponent->SetDelay(0);
    m_pPhysicsComponent->SetVelocity(velocity);
    static int logs = 0;
    if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 && logs++ < 1000)
        SDL_Log("Pazur original melee: actor=%s animation=%s repeats=%d next_entry=%llu clock=%llu direction=%d",
            m_pOwner->GetName().c_str(), customAnimation.c_str(), repeats,
            (unsigned long long)nextEntry, (unsigned long long)clock, direction);
}

void OriginalMeleeAttackAIStateComponent::FinishCustomMove() {
    static int logs = 0;
    if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 && logs++ < 1000)
        SDL_Log("Pazur original finish: actor=%s animation=%s x=%.3f start=%.3f target=%.3f elapsed=%llu direction=%d",
            m_pOwner->GetName().c_str(), customAnimation.c_str(),
            m_pPositionComponent->GetPosition().x, startX, targetX,
            (unsigned long long)(clock-moveStarted), direction);
    finishing = true;
    SetWindow(false, Point(), Point(), 0);
    m_pEnemyAIComponent->EnterBestState(true);
    // Only exclude this state while selecting its successor. Keeping this flag
    // set after leaving would permanently disable the next attack entry.
    finishing = false;
}

void OriginalMeleeAttackAIStateComponent::SetWindow(
    bool enabled, const Point& offset, const Point& size, unsigned damage) {
    if (enabled != damageWindow) {
        hitActors.clear();
        static int logs = 0;
        if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 && logs++ < 2000)
            SDL_Log("Pazur original window: actor=%s enabled=%d image=%u tick=%u",
                m_pOwner->GetName().c_str(), enabled,
                m_pAnimationComponent->GetCurrentAnimation()->GetCurrentAnimationFrame()->imageId,
                SDL_GetTicks());
    }
    damageWindow = enabled;
    windowOffset = offset;
    windowSize = size;
    windowDamage = damage;
}

void OriginalMeleeAttackAIStateComponent::TestDamageWindow() {
    if (!damageWindow || !m_IsActive) return;
    const auto center = m_pPositionComponent->GetPosition() + windowOffset;
    SDL_Rect area{(int)(center.x - windowSize.x / 2), (int)(center.y - windowSize.y / 2),
        (int)windowSize.x, (int)windowSize.y};
    // Entry sensors determine eligibility, not the extent of an already active
    // attack. Retain committed IDs after sensor exit and resolve each through
    // the live actor registry. Snapshot IDs before AddHealth can remove actors.
    auto targetIds = committedTargets;
    for (auto* target : m_EnemyAgroList)
        if (target) targetIds.insert(target->GetGUID());
    auto logic = g_pApp->GetGameLogic();
    auto physics = logic->VGetGamePhysics();
    auto boxPhysics = dynamic_cast<ClawPhysics*>(physics.get());
    for (int id : targetIds) {
        auto target = MakeStrongPtr(logic->VGetActor(id));
        if (!target || hitActors.count(id)) continue;
        auto health = MakeStrongPtr(target->GetComponent<HealthComponent>());
        if (!health || health->GetHealth() <= 0 || !boxPhysics ||
            !boxPhysics->HasActorBody(id)) continue;
        auto body = physics->VGetAABB(id, true);
        SDL_Rect intersection;
        if (!SDL_IntersectRect(&area, &body, &intersection)) continue;
        hitActors.insert(target->GetGUID());
        static int logs = 0;
        if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 && logs++ < 1000)
            SDL_Log("Pazur original contact: actor=%s target=%s damage=%u image=%u tick=%u",
                m_pOwner->GetName().c_str(), target->GetName().c_str(), windowDamage,
                m_pAnimationComponent->GetCurrentAnimation()->GetCurrentAnimationFrame()->imageId, SDL_GetTicks());
        Point impact(direction > 0 ? intersection.x : intersection.x + intersection.w,
            intersection.y + intersection.h / 2);
        health->AddHealth(-(int)windowDamage, DamageType_MeleeAttack, impact, m_pOwner->GetGUID());
        if (!m_IsActive) return;
    }
}

void OriginalMeleeAttackAIStateComponent::VOnAnimationFrameChanged(
    Animation* animation, AnimationFrame* last, AnimationFrame* frame) {
    if (policy == Policy::Upstream || policy == Policy::Crab) {
        MeleeAttackAIStateComponent::VOnAnimationFrameChanged(animation, last, frame);
        if (policy == Policy::Crab && IsCurrentAnimation(animation) &&
            animation->GetName() == m_AttackActions.front()->animation &&
            !OriginalMeleePolicy::CrabDamageImage(frame->imageId))
            SetWindow(false, Point(), Point(), 0);
        return;
    }
    if (!IsCurrentAnimation(animation) || animation->GetName() != customAnimation) return;
    if (policy == Policy::Fish) {
        // Image 202 is the original chomp sound cue, not the damage trigger.
        if (frame->imageId == 202 && !soundPlayed) {
            soundPlayed = true;
            Util::PlayRandomSoundFromList(m_pEnemyAIComponent->GetMeleeAttackSounds());
        }
        return;
    }
    if (tigerMove == OriginalMeleePolicy::TigerMove::Knife && frame->imageId == 202) {
        // Original 0x498ca0/0x498de0: rectangle [-63,-58,0,-1], base damage 15.
        SetWindow(true, Point(direction * 31.5, -29.5), Point(63,57), 15);
    } else if (tigerMove == OriginalMeleePolicy::TigerMove::Lunge) {
        auto velocity = m_pPhysicsComponent->GetVelocity();
        velocity.x = frame->imageId == 800 ? 0 :
            direction * OriginalMeleePolicy::PixelsPerSecondToPhysics(300);
        m_pPhysicsComponent->SetVelocity(velocity);
        if (frame->imageId == 402)
            SetWindow(true, Point(direction * 37.5, -12), Point(73,54), 20);
    }
}

void OriginalMeleeAttackAIStateComponent::VOnAnimationLooped(Animation* animation) {
    if (policy == Policy::Upstream || policy == Policy::Crab) {
        MeleeAttackAIStateComponent::VOnAnimationLooped(animation);
        return;
    }
    if (!IsCurrentAnimation(animation) || animation->GetName() != customAnimation) return;
    if (policy == Policy::Tiger) {
        if (tigerMove == OriginalMeleePolicy::TigerMove::Knife && --repeats > 0)
            BeginCustomMove();
        else FinishCustomMove();
    }
    // Fish travel ends at its captured target X, independently of ANI looping.
}

void OriginalMeleeAttackAIStateComponent::VUpdate(uint32 ms) {
    clock += ms;
    if (policy == Policy::Upstream || policy == Policy::Crab) {
        MeleeAttackAIStateComponent::VUpdate(ms);
        if (policy == Policy::Crab) {
            const auto animation = m_pAnimationComponent->GetCurrentAnimation();
            if (!m_IsActive || animation->GetName() != m_AttackActions.front()->animation ||
                !OriginalMeleePolicy::CrabDamageImage(animation->GetCurrentAnimationFrame()->imageId))
                SetWindow(false, Point(), Point(), 0);
            TestDamageWindow();
        }
        return;
    }
    if (!m_IsActive) {
        const auto current = m_pEnemyAIComponent->GetCurrentState();
        if (policy == Policy::Tiger && entryWakePending && clock >= nextEntry &&
            current && current->VGetStateType() == EnemyAIState_Patrolling) {
            entryWakePending = false;
            // Wake once on expiry; normal sensor and patrol transitions handle
            // later arrivals. Do not interrupt a hurt or parry animation.
            m_pEnemyAIComponent->EnterBestState(true);
        }
        return;
    }
    TestDamageWindow();
    if (!m_IsActive) return;
    const double x = m_pPositionComponent->GetPosition().x;
    if (policy == Policy::Fish || tigerMove != OriginalMeleePolicy::TigerMove::Knife) {
        const bool crossed = OriginalMeleePolicy::PassedTarget(x, targetX, direction);
        // The original also exits on patrol limits. Keep the existing map-aware
        // borders; the timeout prevents a solid wall trapping an active state.
        auto patrol = MakeStrongPtr(m_pOwner->GetComponent<PatrolEnemyAIStateComponent>());
        const bool outside = patrol && patrol->GetLeftPatrolBorder() < patrol->GetRightPatrolBorder() &&
            (x <= patrol->GetLeftPatrolBorder() || x >= patrol->GetRightPatrolBorder());
        const uint64_t maxTravel = policy == Policy::Tiger &&
            tigerMove == OriginalMeleePolicy::TigerMove::FrontFlip ? 1000 : 2000;
        if (crossed || outside || clock - moveStarted >= maxTravel)
            FinishCustomMove();
    }
}
