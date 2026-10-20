#pragma once
#include "Engine/Actor/ActorComponent.h"
#include "Engine/Actor/Components/AnimationComponent.h"
#include "Engine/Actor/Components/ControllerComponents/HealthComponent.h"
#include "OmarBattle.h"
#include <array>

class ActorRenderComponent;
class OmarEncounterComponent final : public ActorComponent, public HealthObserver {
public:
    static const char* g_Name;
    const char* VGetName() const override { return g_Name; }
    OmarEncounterComponent();
    ~OmarEncounterComponent();
    bool VInit(TiXmlElement*) override { return true; }
    void VPostInit() override;
    void VUpdate(uint32 ms) override;
    TiXmlElement* VGenerateXml() override { return nullptr; }
    bool VCanResistDamage(DamageType type, Point impact) override;
    void VOnResistDamage(DamageType type, Point impact) override;
    static void Draw(SDL_Renderer* renderer);
    static bool IsEnding();
private:
    void Started(IEventDataPtr event);
    void Ended(IEventDataPtr event);
    void Entered(IEventDataPtr event);
    void Reset();
    void PublishHealth();
    void Move(const Point& position);
    void ClearEffects();
    void UpdateRing(uint32 ms);
    void UpdateBolts(uint32 ms);
    void Shoot();
    void Supplies(uint32 ms);
    void BeginDefeat();
    StrongActorPtr Sprite(const char* image);
    struct Bolt { StrongActorPtr actor; Point speed; int life = 0; };
    std::array<Bolt, 12> m_Bolts;
    std::array<StrongActorPtr, 8> m_Ring;
    OmarBattle m_Battle;
    HealthComponent* m_Health = nullptr;
    AnimationComponent* m_Animation = nullptr;
    ActorRenderComponent* m_Render = nullptr;
    Point m_Home, m_PendingPosition;
    bool m_TeleportPending = false, m_SuppliesFound = false;
    struct Supply { int id = -1; Point position; int wait = 0; bool present = false; };
    std::array<Supply, 2> m_Supplies;
    bool m_Started = false, m_SwitchShield = true, m_Dead = false, m_Left = false;
    int m_Time = 0, m_AttackTimer = 1700, m_HitCooldown = 0, m_PlayerCooldown = 0;
    int m_Recovery = 0, m_DeathTime = 0, m_Opening = 0;
};

class ChameleonFadeComponent final : public ActorComponent {
public:
    static const char* g_Name;
    const char* VGetName() const override { return g_Name; }
    bool VInit(TiXmlElement*) override { return true; }
    void VPostInit() override;
    void VUpdate(uint32 ms) override;
    TiXmlElement* VGenerateXml() override { return nullptr; }
private:
    int m_Time = 0, m_LastAlpha = -1;
    ActorRenderComponent* m_Render = nullptr;
    HealthComponent* m_Health = nullptr;
    AnimationComponent* m_Animation = nullptr;
};
