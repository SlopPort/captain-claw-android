#include "AquatisArena.h"
#include "Engine/Actor/Actor.h"
#include "Engine/Actor/ActorTemplates.h"
#include "Engine/Actor/Components/PositionComponent.h"
#include "Engine/Actor/Components/RenderComponent.h"
#include "Engine/Actor/Components/ControllerComponents/AmmoComponent.h"
#include "Engine/GameApp/BaseGameApp.h"
#include "Engine/GameApp/BaseGameLogic.h"
#include "Engine/Events/EventMgr.h"
#include "Engine/Events/Events.h"
#include <algorithm>
#include <cmath>

namespace {
WeakActorPtr arenaOwner;
void text(TiXmlElement* parent,const char* name,const char* value) {
    auto element=new TiXmlElement(name);element->LinkEndChild(new TiXmlText(value));parent->LinkEndChild(element);
}
void visible(Actor* actor,bool show) { actor->GetRawComponent<ActorRenderComponent>(true)->SetVisible(show); }
void move(Actor* actor,Point p) {
    IEventMgr::Get()->VTriggerEvent(IEventDataPtr(new EventData_Move_Actor(actor->GetGUID(),p)));
}
}

TiXmlElement* AquatisArenaObject(const std::string& logic,const Point& position) {
    if(logic=="AquatisDynamite") {
        auto xml=ActorTemplates::CreateXmlData_PickupActor(PickupType_Ammo_Dynamite,position,true);
        xml->SetAttribute("Type","Level12_AquatisSupply");return xml;
    }
    const bool tentacle=logic=="Tentacle", rock=logic=="AquatisStalactite";
    const char* image=tentacle?"/LEVEL12/IMAGES/AQUATISTENTACLE/*.PID":
        rock?"/LEVEL12/IMAGES/PROJECTILES/STALACTITE/*.PID":"/LEVEL12/IMAGES/AQUATISWALLCRACK/*.PID";
    auto xml=ActorTemplates::CreateXmlData_StaticImage(ActorPrototype_StaticImage,position,image,AnimationDef());
    xml->SetAttribute("Type",tentacle?"Level12_AquatisTentacle":rock?"Level12_AquatisRock":"Level12_AquatisCrack");
    if(tentacle) {
        auto animation=new TiXmlElement("AnimationComponent");
        text(animation,"AnimationPath","/LEVEL12/ANIS/AQUATISTENTACLE/*.ANI");xml->LinkEndChild(animation);
        // Fifty HP means three standard pistol hits or one magic claw.
        auto hp=new TiXmlElement("HealthComponent");text(hp,"Health","50");text(hp,"MaxHealth","50");xml->LinkEndChild(hp);
        ActorBodyDef body;body.bodyType=b2_staticBody;body.makeSensor=true;
        body.fixtureType=FixtureType_EnemyAI;body.position=position;body.size=Point(55,95);body.gravityScale=0;
        body.collisionFlag=CollisionFlag_DynamicActor;
        body.collisionMask=CollisionFlag_Bullet|CollisionFlag_Magic|CollisionFlag_Explosion|CollisionFlag_ClawAttack;
        xml->LinkEndChild(ActorTemplates::CreatePhysicsComponent(&body));
        xml->LinkEndChild(new TiXmlElement(AquatisTentacleComponent::g_Name));
    }
    return xml;
}

const char* AquatisTentacleComponent::g_Name="AquatisTentacleComponent";
void AquatisTentacleComponent::VPostInit() {
    health=m_pOwner->GetRawComponent<HealthComponent>(true);health->AddObserver(this);
    animation=m_pOwner->GetRawComponent<AnimationComponent>(true);animation->AddObserver(this);
    animation->SetAnimation("idle");
}
bool AquatisTentacleComponent::Down() const { return health->GetHealth()<=0; }
bool AquatisTentacleComponent::VCanResistDamage(DamageType,Point) { return !active; }
void AquatisTentacleComponent::Reset(bool enabled) {
    active=enabled;disabled=false;swinging=struck=false;sinking=0;cooldown=700;
    health->SetMaxHealth();visible(m_pOwner.get(),enabled);
    auto physics=g_pApp->GetGameLogic()->VGetGamePhysics();
    if(enabled)physics->VActivate(m_pOwner->GetGUID());else physics->VDeactivate(m_pOwner->GetGUID());
    animation->SetAnimation(enabled?"respawn":"idle");
}
void AquatisTentacleComponent::VOnHealthChanged(int32 before,int32 after,DamageType,Point,int) {
    if(after>=before || !active)return;
    swinging=false;
    animation->SetAnimation(after<=0?"killfall":"hit");
    if(after<=0) { sinking=600;SDL_Log("Pazur Aquatis tentacle down: %u",m_pOwner->GetGUID()); }
    // Deactivation is deferred until update: damage can arrive inside Box2D.
}
void AquatisTentacleComponent::VOnAnimationLooped(Animation*) {
    if(active && !Down()) {swinging=false;animation->SetAnimation("idle");}
}
void AquatisTentacleComponent::VOnAnimationFrameChanged(Animation* anim,AnimationFrame*,AnimationFrame* frame) {
    if(!active || Down() || !swinging || struck || anim->GetName()!="strike1" || frame->idx<2)return;
    struck=true;
    const auto p=m_pOwner->GetPositionComponent()->GetPosition();
    ActorTemplates::CreateAreaDamage(Point(p.x-35,p.y-10),Point(115,75),10,
        CollisionFlag_EnemyAIAttack,"Rectangle",DamageType_MeleeAttack,Direction_Left,m_pOwner->GetGUID());
}
void AquatisTentacleComponent::VUpdate(uint32 ms) {
    if(!active)return;
    if(Down()) {
        if(!disabled) {g_pApp->GetGameLogic()->VGetGamePhysics()->VDeactivate(m_pOwner->GetGUID());disabled=true;}
        sinking=ms>=sinking?0:sinking-ms;if(!sinking)visible(m_pOwner.get(),false);return;
    }
    cooldown=ms>=cooldown?0:cooldown-ms;
    const auto claw=g_pApp->GetGameLogic()->GetClawActor();if(!claw || cooldown || swinging)return;
    const auto p=m_pOwner->GetPositionComponent()->GetPosition(), c=claw->GetPositionComponent()->GetPosition();
    if(std::abs(c.x-p.x)<115 && std::abs(c.y-p.y)<90) {
        swinging=true;struck=false;cooldown=1300;animation->SetAnimation("strike1");
    }
}

const char* AquatisArenaComponent::g_Name="AquatisArenaComponent";
AquatisArenaComponent::AquatisArenaComponent() {
    IEventMgr::Get()->VAddListener(MakeDelegate(this,&AquatisArenaComponent::Loaded),EventData_World_Finished_Loading::sk_EventType);
    IEventMgr::Get()->VAddListener(MakeDelegate(this,&AquatisArenaComponent::Started),EventData_Boss_Fight_Started::sk_EventType);
    IEventMgr::Get()->VAddListener(MakeDelegate(this,&AquatisArenaComponent::Ended),EventData_Boss_Fight_Ended::sk_EventType);
}
AquatisArenaComponent::~AquatisArenaComponent() {
    if(arenaOwner.lock()==m_pOwner)arenaOwner.reset();
    IEventMgr::Get()->VRemoveListener(MakeDelegate(this,&AquatisArenaComponent::Loaded),EventData_World_Finished_Loading::sk_EventType);
    IEventMgr::Get()->VRemoveListener(MakeDelegate(this,&AquatisArenaComponent::Started),EventData_Boss_Fight_Started::sk_EventType);
    IEventMgr::Get()->VRemoveListener(MakeDelegate(this,&AquatisArenaComponent::Ended),EventData_Boss_Fight_Ended::sk_EventType);
}
void AquatisArenaComponent::VPostInit() {
    health=m_pOwner->GetRawComponent<HealthComponent>(true);health->AddObserver(this);arenaOwner=m_pOwner;
}
void AquatisArenaComponent::Loaded(IEventDataPtr) {Discover();}
void AquatisArenaComponent::Discover() {
    if(ready)return;
    auto logic=g_pApp->GetGameLogic();
    tentacles.clear();rocks.clear();rockHomes.clear();
    for(auto actor:logic->FindActorByName("Level12_AquatisTentacle"))tentacles.push_back(logic->VGetActor(actor->GetGUID()));
    for(auto actor:logic->FindActorByName("Level12_AquatisRock")) {rocks.push_back(logic->VGetActor(actor->GetGUID()));rockHomes.push_back(actor->GetPositionComponent()->GetPosition());}
    auto hole=logic->FindActorByName("Level12_AquatisCrack",true);
    auto ammo=logic->FindActorByName("Level12_AquatisSupply",true);
    if(!hole || !ammo || tentacles.size()!=3 || rocks.size()!=5) {
        LOG_ERROR("Aquatis arena is incomplete; expected 3 tentacles, 5 stalactites, crack and supply");return;
    }
    crack=hole->GetPositionComponent()->GetPosition();
    crackBounds=hole->GetRawComponent<ActorRenderComponent>(true)->VGetPositionRect();
    supply=ammo;supplyHome=ammo->GetPositionComponent()->GetPosition();ready=true;
    SDL_Log("Pazur Aquatis arena ready: tentacles=3 rocks=5 crack=%.0f,%.0f",crack.x,crack.y);
}
void AquatisArenaComponent::ResetParts(bool enabled) {
    for(auto weak:tentacles)if(auto part=weak.lock())part->GetRawComponent<AquatisTentacleComponent>(true)->Reset(enabled);
}
void AquatisArenaComponent::Started(IEventDataPtr) {
    Discover();started=ready;used=falling=0;pending=false;ResetParts(started);
    if(started)SDL_Log("Pazur Aquatis fight started");
}
void AquatisArenaComponent::Ended(IEventDataPtr event) {
    started=false;pending=false;falling=0;ResetParts(false);
    if(!static_pointer_cast<EventData_Boss_Fight_Ended>(event)->GetIsBossDead()) {
        used=0;
        for(unsigned i=0;i<rocks.size();++i)if(auto rock=rocks[i].lock()) {move(rock.get(),rockHomes[i]);visible(rock.get(),true);}
    }
}
void AquatisArenaComponent::Explosion(const Point& p,int source) {
    if(g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14)
        SDL_Log("Pazur Aquatis explosion candidate: x=%.1f y=%.1f source=%d",p.x,p.y,source);
    if(!started || pending || used>=rocks.size())return;
    const auto claw=g_pApp->GetGameLogic()->GetClawActor();
    if(!claw || source!=(int)claw->GetGUID() || std::abs(p.x-crack.x)>38 || std::abs(p.y-crack.y)>65)return;
    for(auto weak:tentacles) {auto part=weak.lock();if(!part || !part->GetRawComponent<AquatisTentacleComponent>(true)->Down())return;}
    pending=true;falling=0;thrower=source;
    SDL_Log("Pazur Aquatis crack explosion: accepted rock=%u",used+1);
}
bool AquatisArenaComponent::CaptureTarget(const Point& p,int source,Point& destination) {
    if(!started || pending || used>=rocks.size())return false;
    const auto claw=g_pApp->GetGameLogic()->GetClawActor();
    // Use the imported crack sprite's actual aperture extent (60x128 in the
    // standard map), rather than an arbitrarily smaller vertical hitbox.
    if(!claw || source!=(int)claw->GetGUID() || p.x<crackBounds.x || p.x>=crackBounds.x+crackBounds.w ||
        p.y<crackBounds.y || p.y>=crackBounds.y+crackBounds.h)return false;
    for(auto weak:tentacles) {auto part=weak.lock();if(!part || !part->GetRawComponent<AquatisTentacleComponent>(true)->Down())return false;}
    destination=crack;
    if(g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14)
        SDL_Log("Pazur Aquatis crack captured dynamite: x=%.1f y=%.1f",p.x,p.y);
    return true;
}
void AquatisArenaComponent::VUpdate(uint32 ms) {
    if(!started)return;
    // A single actor owns resupply. Keeping only a weak reference allows pickup
    // destruction; replacements never accumulate while an old pickup exists.
    if(supply.expired()) {
        supplyTimer+=ms;
        if(supplyTimer>=2500) {supply=ActorTemplates::CreateActorPickup(PickupType_Ammo_Dynamite,supplyHome,true);supplyTimer=0;}
    } else supplyTimer=0;
    if(!pending)return;
    falling+=ms;
    auto rock=rocks[used].lock();
    if(!rock) {pending=false;LOG_ERROR("Aquatis stalactite disappeared");return;}
    const auto home=rockHomes[used];
    const double destination=m_pOwner->GetPositionComponent()->GetY()-35;
    const double y=std::min(destination,home.y+falling*.36);
    move(rock.get(),Point(home.x,y));
    if(y<destination)return;
    visible(rock.get(),false);++used;pending=false;
    rockDamage=true;
    health->AddHealth(-20,DamageType_Explosion,m_pOwner->GetPositionComponent()->GetPosition(),thrower);
    rockDamage=false;
    SDL_Log("Pazur Aquatis stalactite hit: health=%d remaining=%u",health->GetHealth(),unsigned(rocks.size()-used));
    if(health->GetHealth()>0)ResetParts(true);
}
void AquatisDynamiteExploded(const Point& p,int source) {
    auto boss=arenaOwner.lock();
    if(boss)if(auto arena=boss->GetRawComponent<AquatisArenaComponent>(false))arena->Explosion(p,source);
}
bool AquatisDynamiteReachedCrack(const Point& p,int source,Point& destination) {
    auto boss=arenaOwner.lock();
    if(boss)if(auto arena=boss->GetRawComponent<AquatisArenaComponent>(false))return arena->CaptureTarget(p,source,destination);
    return false;
}
