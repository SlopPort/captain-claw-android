#pragma once
#include "Engine/Actor/ActorComponent.h"
#include "Engine/Actor/Components/AnimationComponent.h"
#include "Engine/Actor/Components/ControllerComponents/HealthComponent.h"

// Original arena objects retain their WWD positions. These additions were
// written by OpenAI Codex; the engine, artwork and animations retain their authors.
TiXmlElement* AquatisArenaObject(const std::string& logic, const Point& position);
void AquatisDynamiteExploded(const Point& position, int source);
bool AquatisDynamiteReachedCrack(const Point& position,int source,Point& destination);

class AquatisTentacleComponent final : public ActorComponent, public HealthObserver, public AnimationObserver {
public:
    static const char* g_Name;
    const char* VGetName() const override { return g_Name; }
    bool VInit(TiXmlElement*) override { return true; }
    TiXmlElement* VGenerateXml() override { return nullptr; }
    void VPostInit() override;
    void VUpdate(uint32 ms) override;
    void VOnHealthChanged(int32 before,int32 after,DamageType,Point,int) override;
    bool VCanResistDamage(DamageType,Point) override;
    void VOnAnimationFrameChanged(Animation*,AnimationFrame*,AnimationFrame*) override;
    void VOnAnimationLooped(Animation*) override;
    void Reset(bool enabled);
    bool Down() const;
private:
    HealthComponent* health=nullptr;
    AnimationComponent* animation=nullptr;
    bool active=false, disabled=false, swinging=false, struck=false;
    uint32 cooldown=700, sinking=0;
};

class AquatisArenaComponent final : public ActorComponent, public HealthObserver {
public:
    static const char* g_Name;
    AquatisArenaComponent();
    ~AquatisArenaComponent();
    const char* VGetName() const override { return g_Name; }
    bool VInit(TiXmlElement*) override { return true; }
    TiXmlElement* VGenerateXml() override { return nullptr; }
    void VPostInit() override;
    void VUpdate(uint32 ms) override;
    bool VCanResistDamage(DamageType,Point) override { return !rockDamage; }
    void Explosion(const Point& position,int source);
    bool CaptureTarget(const Point& position,int source,Point& destination);
private:
    void Started(IEventDataPtr);
    void Ended(IEventDataPtr);
    void Loaded(IEventDataPtr);
    void ResetParts(bool enabled);
    void Discover();
    HealthComponent* health=nullptr;
    std::vector<WeakActorPtr> tentacles, rocks;
    std::vector<Point> rockHomes;
    WeakActorPtr supply;
    Point crack, supplyHome;
    SDL_Rect crackBounds{};
    bool ready=false, started=false, pending=false, rockDamage=false;
    unsigned used=0;
    uint32 falling=0, supplyTimer=0;
    int thrower=0;
};
