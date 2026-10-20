#pragma once
#include "Engine/Actor/ActorComponent.h"
#include "Engine/Actor/Components/AnimationComponent.h"

class ActorRenderComponent;
class LavaGeyserComponent : public ActorComponent, public AnimationObserver {
public:
    static const char* g_Name;
    const char* VGetName() const override { return g_Name; }
    bool VInit(TiXmlElement* data) override;
    void VPostInit() override;
    void VUpdate(uint32 ms) override;
    TiXmlElement* VGenerateXml() override { return nullptr; }
    void VOnAnimationLooped(Animation* animation) override;
private:
    AnimationComponent* m_Animation = nullptr;
    ActorRenderComponent* m_Render = nullptr;
    int m_StartDelay = 0, m_Rest = 1000, m_Damage = 10;
    int m_FirstActive = 4, m_LastActive = 18, m_Pulse = 1000, m_Cooldown = 0;
    bool m_WasActive = false;
};

class LavaMouthComponent final : public LavaGeyserComponent {
public:
    static const char* g_Name;
    const char* VGetName() const override { return g_Name; }
};
