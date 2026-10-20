#include "LavaGeyserComponent.h"
#include "Engine/Actor/Actor.h"
#include "Engine/Actor/Components/PositionComponent.h"
#include "Engine/Actor/Components/RenderComponent.h"
#include "Engine/Actor/Components/ControllerComponents/HealthComponent.h"
#include "Engine/GameApp/BaseGameApp.h"
#include "Engine/GameApp/BaseGameLogic.h"
#include "Engine/Graphics2D/Image.h"
#include "Engine/Events/EventMgr.h"
#include "Engine/Events/Events.h"
#include <algorithm>
#include <cmath>

const char* LavaGeyserComponent::g_Name = "LavaGeyserComponent";
const char* LavaMouthComponent::g_Name = "LavaMouthComponent";

bool LavaGeyserComponent::VInit(TiXmlElement* data) {
    ParseValueFromXmlElem(&m_StartDelay, data->FirstChildElement("StartDelay"));
    ParseValueFromXmlElem(&m_Rest, data->FirstChildElement("RestMs"));
    ParseValueFromXmlElem(&m_Damage, data->FirstChildElement("Damage"));
    ParseValueFromXmlElem(&m_FirstActive, data->FirstChildElement("FirstActiveFrame"));
    ParseValueFromXmlElem(&m_LastActive, data->FirstChildElement("LastActiveFrame"));
    ParseValueFromXmlElem(&m_Pulse, data->FirstChildElement("PulseMs"));
    return m_StartDelay >= 0 && m_Rest >= 0 && m_Damage > 0 && m_Pulse > 0
        && m_FirstActive >= 0 && m_LastActive >= m_FirstActive;
}

void LavaGeyserComponent::VPostInit() {
    m_Animation = m_pOwner->GetRawComponent<AnimationComponent>(true);
    m_Render = m_pOwner->GetRawComponent<ActorRenderComponent>(true);
    assert(m_Animation->GetCurrentAnimation());
    assert(m_LastActive < (int)m_Animation->GetCurrentAnimation()->GetAnimFramesSize());
    m_Animation->SetDelay(m_StartDelay);
    m_Animation->AddObserver(this);
}

void LavaGeyserComponent::VOnAnimationLooped(Animation*) {
    m_Animation->SetDelay(m_Rest);
}

void LavaGeyserComponent::VUpdate(uint32 ms) {
    m_Cooldown = m_Cooldown > (int)ms ? m_Cooldown - (int)ms : 0;
    const auto animation = m_Animation->GetCurrentAnimation();
    const auto frame = animation->GetCurrentAnimationFrame();
    const bool active = !animation->IsPaused() && (int)frame->idx >= m_FirstActive && (int)frame->idx <= m_LastActive;
    if (active != m_WasActive) {
        const bool mouth = SDL_strcmp(VGetName(), LavaMouthComponent::g_Name) == 0;
        static int traces[2][2] = {{0, 0}, {0, 0}};
        if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 && traces[mouth][active]++ < 4)
            SDL_Log("Pazur %s: damage=%d frame=%u", mouth ? "lava mouth" : "geyser", active, frame->idx);
        if (mouth && active) {
            SoundInfo sound("/LEVEL14/SOUNDS/LAVAMOUTH1.WAV");
            sound.setPositionEffect = true;
            sound.setDistanceEffect = true;
            sound.soundSourcePosition = m_pOwner->GetPositionComponent()->GetPosition();
            IEventMgr::Get()->VTriggerEvent(IEventDataPtr(new EventData_Request_Play_Sound(sound)));
        }
        m_WasActive = active;
    }
    if (!active || m_Cooldown) return;
    const auto claw = g_pApp->GetGameLogic()->GetClawActor();
    if (!claw) return;
    const Point origin = m_pOwner->GetPositionComponent()->GetPosition();
    if (std::fabs(claw->GetPositionComponent()->GetX() - origin.x) > 256) return;
    const auto image = m_Render->GetImage(frame->imageName).lock();
    if (!image) return;
    const SDL_Rect hazard = image->GetPositonRect((int)origin.x, (int)origin.y);
    const SDL_Rect target = g_pApp->GetGameLogic()->VGetGamePhysics()->VGetAABB(claw->GetGUID(), true);
    if (!SDL_HasIntersection(&hazard, &target)) return;
    const auto health = claw->GetRawComponent<HealthComponent>(true);
    if (health->GetHealth() <= 0) return;
    const int before = health->GetHealth();
    health->AddHealth(-m_Damage, DamageType_EnemyAura, origin, m_pOwner->GetGUID());
    m_Cooldown = m_Pulse;
    const bool mouth = SDL_strcmp(VGetName(), LavaMouthComponent::g_Name) == 0;
    static int traces[2] = {0, 0};
    if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 && traces[mouth]++ < 8)
        SDL_Log("Pazur %s hit: health=%d->%d frame=%u", mouth ? "lava mouth" : "geyser", before, health->GetHealth(), frame->idx);
}
