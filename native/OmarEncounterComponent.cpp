#include "OmarEncounterComponent.h"
#include "Engine/Actor/Actor.h"
#include "Engine/Actor/ActorTemplates.h"
#include "Engine/Actor/Components/PositionComponent.h"
#include "Engine/Actor/Components/RenderComponent.h"
#include "Engine/Actor/Components/ControllableComponent.h"
#include "Engine/GameApp/BaseGameApp.h"
#include "Engine/GameApp/BaseGameLogic.h"
#include "Engine/Events/EventMgr.h"
#include "Engine/Events/Events.h"
#include <SDL2/SDL2_gfxPrimitives.h>
#include "Engine/Resource/Loaders/PidLoader.h"
#include "Engine/Graphics2D/Image.h"
#include "Engine/Actor/Components/ControllerComponents/AmmoComponent.h"
#include "Engine/Actor/Components/ControllerComponents/PowerupComponent.h"
#include <algorithm>
#include <cmath>

namespace {
int endingMs = 0;
shared_ptr<Image> amuletImage, gemImage, adoraImage;
bool encounterVisible = false;
const char* hint = "";
void sound(const char* path) {
    IEventMgr::Get()->VTriggerEvent(IEventDataPtr(new EventData_Request_Play_Sound(SoundInfo(path))));
}
void destroy(StrongActorPtr& actor) {
    if (actor) IEventMgr::Get()->VQueueEvent(IEventDataPtr(new EventData_Destroy_Actor(actor->GetGUID())));
    actor.reset();
}
void position(StrongActorPtr actor, Point p) {
    if (actor) IEventMgr::Get()->VTriggerEvent(IEventDataPtr(new EventData_Move_Actor(actor->GetGUID(), p)));
}
}

const char* OmarEncounterComponent::g_Name = "OmarEncounterComponent";
const char* ChameleonFadeComponent::g_Name = "ChameleonFadeComponent";

OmarEncounterComponent::OmarEncounterComponent() {
    IEventMgr::Get()->VAddListener(MakeDelegate(this, &OmarEncounterComponent::Started), EventData_Boss_Fight_Started::sk_EventType);
    IEventMgr::Get()->VAddListener(MakeDelegate(this, &OmarEncounterComponent::Ended), EventData_Boss_Fight_Ended::sk_EventType);
    IEventMgr::Get()->VAddListener(MakeDelegate(this, &OmarEncounterComponent::Entered), EventData_Entered_Boss_Area::sk_EventType);
}
OmarEncounterComponent::~OmarEncounterComponent() {
    IEventMgr::Get()->VRemoveListener(MakeDelegate(this, &OmarEncounterComponent::Started), EventData_Boss_Fight_Started::sk_EventType);
    IEventMgr::Get()->VRemoveListener(MakeDelegate(this, &OmarEncounterComponent::Ended), EventData_Boss_Fight_Ended::sk_EventType);
    IEventMgr::Get()->VRemoveListener(MakeDelegate(this, &OmarEncounterComponent::Entered), EventData_Entered_Boss_Area::sk_EventType);
    // Level unloading owns destruction of the actors; never enqueue into a dying map.
    endingMs = 0;
    amuletImage.reset(); gemImage.reset(); adoraImage.reset();
    encounterVisible = false;
}
void OmarEncounterComponent::VPostInit() {
    m_Health = m_pOwner->GetRawComponent<HealthComponent>(true);
    m_Animation = m_pOwner->GetRawComponent<AnimationComponent>(true);
    m_Render = m_pOwner->GetRawComponent<ActorRenderComponent>(true);
    m_Health->AddObserver(this);
    m_Home = m_pOwner->GetPositionComponent()->GetPosition();
    m_Animation->SetAnimation("idle");
    SDL_Log("Pazur Omar ready: %.0f,%.0f", m_Home.x, m_Home.y);
}
void OmarEncounterComponent::PublishHealth() {
    m_Health->SetCurrentHealth(m_Battle.health);
    IEventMgr::Get()->VTriggerEvent(IEventDataPtr(new EventData_Boss_Health_Changed(m_Battle.health / 2, m_Battle.health)));
}
void OmarEncounterComponent::Move(const Point& p) {
    // Contact callbacks run while Box2D is locked. Apply transforms in VUpdate.
    m_PendingPosition = p;
    m_TeleportPending = true;
}
void OmarEncounterComponent::ClearEffects() {
    for (auto& actor : m_Ring) destroy(actor);
    for (auto& bolt : m_Bolts) { destroy(bolt.actor); bolt.life = 0; }
}
void OmarEncounterComponent::Reset() {
    ClearEffects();
    m_Battle.reset();
    m_Started = false; m_Dead = false; m_Left = false;
    m_Time = m_DeathTime = m_Recovery = m_HitCooldown = m_PlayerCooldown = m_Opening = 0;
    m_AttackTimer = 1700; m_SwitchShield = true;
    endingMs = 0; encounterVisible = false;
    Move(m_Home);
    m_Render->SetAlpha(255);
    m_Animation->SetAnimation("idle");
    PublishHealth();
    SDL_Log("Pazur Omar reset");
}
void OmarEncounterComponent::Entered(IEventDataPtr) {
    const auto claw = g_pApp->GetGameLogic()->GetClawActor();
    if (claw) IEventMgr::Get()->VTriggerEvent(IEventDataPtr(new EventData_Checkpoint_Reached(claw->GetGUID(), Point(42100, 1968), false, 0)));
    encounterVisible = true;
    PublishHealth();
    SDL_Log("Pazur Omar staging");
}
void OmarEncounterComponent::Started(IEventDataPtr) {
    m_Started = true;
    encounterVisible = true;
    m_SwitchShield = true;
    PublishHealth();
    SDL_Log("Pazur Omar fight started");
}
void OmarEncounterComponent::Ended(IEventDataPtr event) {
    if (!static_pointer_cast<EventData_Boss_Fight_Ended>(event)->GetIsBossDead()) Reset();
}
StrongActorPtr OmarEncounterComponent::Sprite(const char* image) {
    AnimationDef animation;
    animation.hasAnimation = animation.isCycleAnimation = true;
    animation.cycleAnimationDuration = 70;
    return ActorTemplates::CreateActor_StaticImage(ActorPrototype_StaticAnimatedImage,
        m_pOwner->GetPositionComponent()->GetPosition(), image, animation);
}
bool OmarEncounterComponent::VCanResistDamage(DamageType, Point) { return true; }
void OmarEncounterComponent::VOnResistDamage(DamageType type, Point impact) {
    if (!m_Started || m_Dead || m_HitCooldown || m_Recovery) return;
    const auto claw = g_pApp->GetGameLogic()->GetClawActor();
    if (!claw) return;
    OmarBattle::Hit hit = OmarBattle::Other;
    if (type == DamageType_FireSword) hit = OmarBattle::Fire;
    if (type == DamageType_FrostSword) hit = OmarBattle::Ice;
    if (type == DamageType_Bullet) hit = OmarBattle::Bullet;
    if (type == DamageType_MeleeAttack && claw->GetRawComponent<ClawControllableComponent>(true)->IsDucking()) hit = OmarBattle::DuckSword;
    if (!m_Battle.secondPhase()) {
        // The two empty places in the rotating ring form a real opening.
        const Point center = m_pOwner->GetPositionComponent()->GetPosition();
        const Point cp = claw->GetPositionComponent()->GetPosition();
        double angle = std::atan2(cp.y - center.y, cp.x - center.x);
        double gap = m_Time * 0.00065 + 5.340707511;
        if (std::fabs(std::remainder(angle - gap, 6.283185307)) > 0.8) return;
    }
    const bool wasSecond = m_Battle.secondPhase();
    const int before = m_Battle.health;
    const bool hurt = m_Battle.strike(hit);
    PublishHealth();
    SDL_Log("Pazur Omar contact: type=%d health=%d->%d bullets=%d", (int)type, before, m_Battle.health, m_Battle.bullets);
    if (hit == OmarBattle::Bullet && wasSecond) {
        m_HitCooldown = 180;
        m_Animation->SetAnimation(m_Battle.bullets == 3 ? "hithigh" : "block");
        m_Recovery = 300;
        if (m_Battle.bullets == 3) m_Opening = 3500;
    }
    if (!hurt) {
        if (!(wasSecond && hit == OmarBattle::Bullet)) {
            m_HitCooldown = 250;
            m_Recovery = 300;
            m_Animation->SetAnimation("block");
        }
        return;
    }
    m_HitCooldown = 900;
    m_Recovery = 650;
    m_Animation->SetAnimation("hithigh");
    if (!wasSecond) {
        m_SwitchShield = true;
        if (m_Battle.secondPhase()) {
            ClearEffects();
            Move(Point(42390, 1970));
            const auto ammo = claw->GetRawComponent<AmmoComponent>(true);
            if (ammo->GetRemainingAmmo(AmmoType_Pistol) < 24) ammo->SetAmmo(AmmoType_Pistol, 24);
            SDL_Log("Pazur Omar phase two");
        }
    } else if (!m_Battle.defeated()) {
        m_Left = !m_Left;
        Move(Point(m_Left ? 42020 : 42390, 1970));
        m_Opening = 0;
        SDL_Log("Pazur Omar teleport");
    }
    if (m_Battle.defeated()) BeginDefeat();
}
void OmarEncounterComponent::BeginDefeat() {
    m_Dead = true;
    m_DeathTime = 0;
    ClearEffects();
    m_Animation->SetAnimation("killfall");
    const auto claw = g_pApp->GetGameLogic()->GetClawActor();
    if (claw) {
        claw->GetRawComponent<ClawControllableComponent>(true)->SetFrozen(true);
        claw->GetRawComponent<HealthComponent>(true)->SetInvulnerable(true);
    }
    IEventMgr::Get()->VQueueEvent(IEventDataPtr(new EventData_Boss_Fight_Ended(true)));
    SDL_Log("Pazur Omar defeated: surrender sequence");
}
void OmarEncounterComponent::UpdateRing(uint32) {
    if (m_SwitchShield) {
        for (auto& actor : m_Ring) destroy(actor);
        for (auto& actor : m_Ring) actor = Sprite(m_Battle.fireShield ? "/LEVEL14/IMAGES/FIRESHIELD/*" : "/LEVEL14/IMAGES/ICESHIELD/*");
        m_SwitchShield = false;
    }
    const Point center = m_pOwner->GetPositionComponent()->GetPosition();
    const auto claw = g_pApp->GetGameLogic()->GetClawActor();
    if (!claw) return;
    const SDL_Rect target = g_pApp->GetGameLogic()->VGetGamePhysics()->VGetAABB(claw->GetGUID(), true);
    for (size_t i = 0; i < m_Ring.size(); ++i) {
        double angle = m_Time * 0.00065 + i * 0.628318531;
        Point p = center + Point(std::cos(angle)*105, std::sin(angle)*105);
        position(m_Ring[i], p);
        SDL_Rect hazard{(int)p.x-12, (int)p.y-12, 24, 24};
        if (!m_PlayerCooldown && SDL_HasIntersection(&hazard, &target)) {
            claw->GetRawComponent<HealthComponent>(true)->AddHealth(-20, DamageType_EnemyAura, p, m_pOwner->GetGUID());
            m_PlayerCooldown = 900;
        }
    }
}
void OmarEncounterComponent::Shoot() {
    const auto claw = g_pApp->GetGameLogic()->GetClawActor();
    if (!claw) return;
    for (auto& bolt : m_Bolts) if (!bolt.actor) {
        const Point p = m_pOwner->GetPositionComponent()->GetPosition() + Point(0, -20);
        Point delta = claw->GetPositionComponent()->GetPosition() - p;
        double length = (std::max)(1.0, std::sqrt(delta.x*delta.x + delta.y*delta.y));
        bolt.speed = Point(delta.x/length*230, delta.y/length*230);
        bolt.actor = Sprite("/LEVEL14/IMAGES/OMARPROJECTILE/*");
        position(bolt.actor, p);
        bolt.life = 4500;
        sound("/LEVEL14/SOUNDS/OMAR/ENERGYBALL.WAV");
        SDL_Log("Pazur Omar projectile");
        return;
    }
}
void OmarEncounterComponent::UpdateBolts(uint32 ms) {
    const auto claw = g_pApp->GetGameLogic()->GetClawActor();
    if (!claw) return;
    const SDL_Rect target = g_pApp->GetGameLogic()->VGetGamePhysics()->VGetAABB(claw->GetGUID(), true);
    for (auto& bolt : m_Bolts) if (bolt.actor) {
        bolt.life -= ms;
        Point p = bolt.actor->GetPositionComponent()->GetPosition() + Point(bolt.speed.x * ms/1000., bolt.speed.y * ms/1000.);
        SDL_Rect hazard{(int)p.x-12, (int)p.y-12, 24, 24};
        bool hit = SDL_HasIntersection(&hazard, &target);
        if (hit && !m_PlayerCooldown) {
            claw->GetRawComponent<HealthComponent>(true)->AddHealth(-20, DamageType_EnemyAura, p, m_pOwner->GetGUID());
            m_PlayerCooldown = 900;
        }
        if (bolt.life <= 0 || hit) destroy(bolt.actor);
        else position(bolt.actor, p);
    }
}
void OmarEncounterComponent::VUpdate(uint32 ms) {
    if (m_TeleportPending) {
        g_pApp->GetGameLogic()->VGetGamePhysics()->VSetPosition(m_pOwner->GetGUID(), m_PendingPosition);
        position(m_pOwner, m_PendingPosition);
        m_TeleportPending = false;
    }
    Supplies(ms);
    if (!m_Started) return;
    if (m_Dead) {
        const int old = m_DeathTime;
        m_DeathTime += ms;
        if (old < 700 && m_DeathTime >= 700) {
            m_Animation->SetAnimation("killfall2");
            sound("/LEVEL14/SOUNDS/OMAR/THENFALL.WAV");
        }
        if (old < 2400 && m_DeathTime >= 2400) m_Animation->SetAnimation("killfall3");
        if (m_DeathTime > 3600) {
            auto animation = m_Animation->GetCurrentAnimation();
            animation->SetAnimationFrame(animation->GetAnimFramesSize()-1);
            m_Render->SetImage(animation->GetCurrentAnimationFrame()->imageName);
            m_Animation->PauseAnimation();
            endingMs = m_DeathTime-3600;
        }
        if (old < 3600 && m_DeathTime >= 3600) {
            sound("/STATES/BOOTY/SOUNDS/AMULET.WAV");
            amuletImage = PidResourceLoader::LoadAndReturnImage("/LEVEL14/IMAGES/AMULET/AMULET.PID", g_pApp->GetCurrentPalette());
            gemImage = PidResourceLoader::LoadAndReturnImage("/LEVEL14/IMAGES/GEM/CENTERGEM1.PID", g_pApp->GetCurrentPalette());
            adoraImage = PidResourceLoader::LoadAndReturnImage("/LEVEL14/IMAGES/SIAMESE/SIAMESE.PID", g_pApp->GetCurrentPalette());
            SDL_Log("Pazur finale: ninth gem and amulet");
        }
        if (old < 18000 && m_DeathTime >= 18000) {
            SDL_Log("Pazur finale complete");
            IEventMgr::Get()->VQueueEvent(IEventDataPtr(new EventData_Finished_Level()));
        }
        return;
    }
    m_Time += ms;
    if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 && m_Time < 60000 && m_Time/2000 != (m_Time-(int)ms)/2000) {
        const auto claw = g_pApp->GetGameLogic()->GetClawActor();
        if (claw) SDL_Log("Pazur arena position: boss=%.0f,%.0f claw=%.0f,%.0f frozen=%d anim=%s", m_pOwner->GetPositionComponent()->GetX(), m_pOwner->GetPositionComponent()->GetY(), claw->GetPositionComponent()->GetX(), claw->GetPositionComponent()->GetY(), claw->GetRawComponent<ClawControllableComponent>(true)->IsActorFrozen(), claw->GetRawComponent<AnimationComponent>(true)->GetCurrentAnimationName().c_str());
    }
    m_HitCooldown = (std::max)(0, m_HitCooldown-(int)ms);
    m_PlayerCooldown = (std::max)(0, m_PlayerCooldown-(int)ms);
    if (m_Opening > 0 && (m_Opening -= ms) <= 0) { m_Opening = 0; m_Battle.bullets = 0; SDL_Log("Pazur Omar opening closed"); }
    if (m_Recovery > 0 && (m_Recovery -= ms) <= 0) { m_Recovery = 0; m_Animation->SetAnimation("idle"); }
    if (!m_Battle.secondPhase()) {
        hint = m_Battle.fireShield ? "OGIEN: uzyj lodowego miecza przez luke" : "LOD: uzyj ognistego miecza przez luke";
        UpdateRing(ms);
    } else hint = m_Battle.bullets == 3 ? "TERAZ: podejdz i zaatakuj kucajac" : "OMAR: trzy strzaly otwieraja obrone";
    if (const auto claw = g_pApp->GetGameLogic()->GetClawActor()) m_Render->SetMirrored(claw->GetPositionComponent()->GetX() > m_pOwner->GetPositionComponent()->GetX());
    UpdateBolts(ms);
    m_AttackTimer -= ms;
    if (m_AttackTimer <= 0 && !m_Recovery && !m_Opening) {
        m_Animation->SetAnimation("strike3");
        m_Recovery = 650;
        Shoot();
        m_AttackTimer = m_Battle.secondPhase() ? 1200 : 2100;
    }
}
void OmarEncounterComponent::Supplies(uint32 ms) {
    auto logic = g_pApp->GetGameLogic();
    if (!m_SuppliesFound) {
        const char* names[] = {"GAME_POWERUPS_FIRESWORD", "GAME_POWERUPS_ICESWORD"};
        for (int i=0; i<2; ++i) for (Actor* actor : logic->FindActorByName(names[i])) {
            if (actor->GetPositionComponent()->GetX() > 39000) {
                m_Supplies[i].id = actor->GetGUID();
                m_Supplies[i].position = actor->GetPositionComponent()->GetPosition();
                m_Supplies[i].present = true;
                SDL_Log("Pazur Omar supply: %s %.0f,%.0f", names[i], m_Supplies[i].position.x, m_Supplies[i].position.y);
            }
        }
        m_SuppliesFound = true;
    }
    if (m_Dead) return;
    for (int i=0; i<2; ++i) {
        auto& supply = m_Supplies[i];
        if (!supply.present || !logic->VGetActor(supply.id).expired()) continue;
        supply.wait += ms;
        if (supply.wait >= 6000) {
            const auto actor = ActorTemplates::CreateActorPickup(i==0 ? PickupType_Powerup_FireSword : PickupType_Powerup_FrostSword, supply.position, true);
            if (actor) supply.id = actor->GetGUID();
            supply.wait = 0;
            SDL_Log("Pazur Omar sword replenished: %d", i);
        }
    }
}
bool OmarEncounterComponent::IsEnding() { return endingMs > 0; }
void OmarEncounterComponent::Draw(SDL_Renderer* renderer) {
    if (!encounterVisible) return;
    const int extra = (int)g_pApp->GetWindowSizeScaled().x - 640;
    const int centerOffset = extra/2;
    if (endingMs) {
        boxRGBA(renderer, 0, 0, 639+extra, 479, 8, 6, 18, 230);
        stringRGBA(renderer, 248+centerOffset, 110, "OMAR POKONANY", 255, 213, 110, 255);
        const auto image = endingMs < 3500 ? gemImage : (endingMs < 7000 ? adoraImage : amuletImage);
        if (image) {
            const double scale = (std::min)(2.0, (std::min)(180.0/image->GetHeight(), 220.0/image->GetWidth()));
            const int w = image->GetWidth()*scale, h = image->GetHeight()*scale;
            SDL_Rect r{320+centerOffset-w/2, 220-h/2, w, h};
            SDL_SetTextureAlphaMod(image->GetTexture(), 255);
            SDL_SetTextureColorMod(image->GetTexture(), 255, 255, 255);
            SDL_RenderCopy(renderer, image->GetTexture(), nullptr, &r);
        }
        stringRGBA(renderer, 204+centerOffset, 327, "AMULET DZIEWIECIU ZYC", 255, 229, 170, 255);
        stringRGBA(renderer, 164+centerOffset, 354, "Zdobyles ostatni klejnot i amulet.", 235, 230, 245, 255);
        stringRGBA(renderer, 172+centerOffset, 376, "Adora powierza ci ich ochrone.", 235, 230, 245, 255);
    } else {
        boxRGBA(renderer, 112+centerOffset, 65, 535+centerOffset, 88, 15, 10, 25, 195);
        stringRGBA(renderer, 120+centerOffset, 73, hint, 255, 232, 190, 255);
    }
}
void ChameleonFadeComponent::VPostInit() {
    m_Render = m_pOwner->GetRawComponent<ActorRenderComponent>(true);
    m_Health = m_pOwner->GetRawComponent<HealthComponent>(true);
    m_Animation = m_pOwner->GetRawComponent<AnimationComponent>(true);
    m_Time = (m_pOwner->GetGUID() * 337) % 6000;
}
void ChameleonFadeComponent::VUpdate(uint32 ms) {
    if (m_Health->GetHealth() <= 0) { m_Render->SetAlpha(255); return; }
    m_Time = (m_Time + ms) % 6000;
    int alpha = 255;
    if (m_Time >= 1500 && m_Time < 2500) alpha = 255-(m_Time-1500)*223/1000;
    else if (m_Time >= 2500 && m_Time < 4500) alpha = 32;
    else if (m_Time >= 4500 && m_Time < 5500) alpha = 32+(m_Time-4500)*223/1000;
    const auto name = m_Animation->GetCurrentAnimationName();
    // Telegraph the tongue and make damage feedback visible.
    if (name.find("strike") != std::string::npos || name == "hit") alpha = 255;
    m_Render->SetAlpha(alpha);
    const int phase = alpha == 32 ? 0 : alpha == 255 ? 2 : 1;
    if (phase != m_LastAlpha) {
        const auto claw = g_pApp->GetGameLogic()->GetClawActor();
        static int traces = 0;
        if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 && claw && std::fabs(claw->GetPositionComponent()->GetX()-m_pOwner->GetPositionComponent()->GetX()) < 250 && traces++ < 16)
            SDL_Log("Pazur chameleon fade: alpha=%d", alpha);
        m_LastAlpha = phase;
    }
}
