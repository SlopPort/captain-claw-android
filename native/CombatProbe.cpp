#include "CombatProbe.h"
#include "CombatPrototypes.h"
#include "ComponentProfiler.h"
#include "GamepadControls.h"
#include "AudioProbe.h"
#include "Engine/GameApp/BaseGameApp.h"
#include "Engine/Audio/Audio.h"
#include "Engine/Actor/ActorTemplates.h"
#include "Engine/Actor/Components/PositionComponent.h"
#include "Engine/Actor/Components/PhysicsComponent.h"
#include "Engine/Actor/Components/AnimationComponent.h"
#include "Engine/Actor/Components/ControllableComponent.h"
#include "Engine/Actor/Components/ControllerComponents/HealthComponent.h"
#include "Engine/Actor/Components/ControllerComponents/LifeComponent.h"
#include "Engine/Actor/Components/ControllerComponents/AmmoComponent.h"
#include "Engine/Actor/Components/ControllerComponents/PowerupComponent.h"
#include "Engine/Actor/Components/AIComponents/TogglePegAIComponent.h"
#include "Engine/Actor/Components/PickupComponents/PickupComponent.h"
#include "Engine/Actor/Components/CheckpointComponent.h"
#include "Engine/Actor/Components/EnemyAI/EnemyAIComponent.h"
#include "Engine/Actor/Components/AIComponents/ProjectileAIComponent.h"
#include "Engine/Actor/Components/AreaDamageComponent.h"
#include "Engine/UserInterface/HumanView.h"
#include "Engine/Scene/SceneNodes.h"
#include "Engine/Events/EventMgr.h"
#include "Engine/Events/Events.h"
#include <fstream>
#include <cstdio>
#include <libwap.h>

namespace {
WeakActorPtr fixtureClaw, target;
bool floorCreated = false;
const Point arena(200000, 1045);
std::map<SDL_Keycode, Uint32> heldKeys;
// Test-only scheduling avoids USB round-trip latency between two ordinary
// button presses. It never calls attack/damage logic directly.
Uint32 scheduledSwordAt=0;
struct JumpTrace {
    bool armed=false, airborne=false, received=false;
    std::string label;
    double baseY=0, rise=0;
    Uint32 inputTime=0, queueMs=0, releaseMs=0;
    int takeoffMs=-1, jumps=0;
} jumpTrace;

// Observe existing level platforms without changing their animation or collision.
// Launch inputs are scheduled on the game thread, avoiding USB round-trip jitter.
struct PegTrial {
    WeakActorPtr source, destination;
    Uint32 started=0, launched=0, positionedAt=0;
    bool active=false, positioned=false;
    SDL_Rect targetBox{}, sourceBox{};
    double baseY=0, rise=0;
} pegTrial;

struct LadderTrace {
    Uint32 end=0, nextSample=0;
    std::string label, previousState;
} ladderTrace;

void keyEvent(SDL_Keycode key, bool down) {
    if (key==SDLK_SPACE) PazurCombatProbe::JumpInput(down,0);
    SDL_Event event{};
    event.type = down ? SDL_KEYDOWN : SDL_KEYUP;
    event.key.state = down ? SDL_PRESSED : SDL_RELEASED;
    event.key.keysym.sym = key;
    event.key.keysym.scancode = SDL_GetScancodeFromKey(key);
    SDL_PushEvent(&event);
}

void status() {
    auto logic = g_pApp->GetGameLogic();
    auto claw = logic->GetClawActor();
    auto enemy = target.lock();
    const auto box = logic->VGetGamePhysics()->VGetAABB(claw->GetGUID(), true);
    const auto position = claw->GetPositionComponent()->GetPosition();
    auto hp = claw->GetRawComponent<HealthComponent>(true);
    auto enemyHp = enemy ? enemy->GetRawComponent<HealthComponent>(false) : nullptr;
    auto ammo=claw->GetRawComponent<AmmoComponent>(true);
    SDL_Log("Pazur probe action: ammo=%d remaining=%u animation=%s",
        int(ammo->GetActiveAmmoType()),ammo->GetRemainingActiveAmmo(),
        claw->GetRawComponent<AnimationComponent>(true)->GetCurrentAnimationName().c_str());
    SDL_Log("Pazur probe status: claw=%d duck=%d x=%.1f y=%.1f box=%d,%d,%d,%d target=%s target_id=%u target_hp=%d target_max=%d",
        hp->GetHealth(), claw->GetRawComponent<ClawControllableComponent>(true)->IsDucking(),
        position.x, position.y, box.x, box.y, box.w, box.h,
        enemy ? enemy->GetName().c_str() : "none", enemy ? enemy->GetGUID() : 0,
        enemyHp ? enemyHp->GetHealth() : -999, enemyHp ? enemyHp->GetMaxHealth() : -999);
}
}

bool PazurCombatProbe::Handle(const std::vector<std::string>& args, const ActorMap& actors) {
    if (args.empty()) return false;
    auto logic = g_pApp->GetGameLogic();
    // Virtual input must remain releasable in menus where no hero exists.
    if (PazurGamepad::DebugCommand(args)) return true;
    if(args[0]=="componentprofile") {PazurProfile::Start();return true;}
    if(args[0]=="audiotrace" && args.size()==2) {PazurAudioProbe::Enable(args[1]=="1");return true;}
    if(args[0]=="audiomeasure" && args.size()==2) {PazurAudioProbe::Begin(args[1]);return true;}
    if(args[0]=="audioreport") {PazurAudioProbe::Report();return true;}
    if(args[0]=="audioquiet") {g_pApp->GetAudio()->StopAllSounds();return true;}
    // This probe is reachable only through the explicitly enabled test mailbox.
    if (args[0]=="audiooptions") {
        auto audio=g_pApp->GetAudio();
        if (args.size()==5) {
            audio->SetSoundActive(args[1]=="1");
            audio->SetMusicActive(args[2]=="1");
            audio->SetSoundVolume(std::stoi(args[3]));
            audio->SetMusicVolume(std::stoi(args[4]));
        }
        SDL_Log("Pazur audio options: sound=%d music=%d soundVolume=%d musicVolume=%d",
            audio->IsSoundActive(),audio->IsMusicActive(),audio->GetSoundVolume(),audio->GetMusicVolume());
        return true;
    }
    auto claw = logic->GetClawActor();
    if (!claw) return false;
    auto physics = logic->VGetGamePhysics();
    if(args[0]=="campaignposition" && (args.size()==3 || args.size()==4)) {
        // Explicit setup fixture: ordinary console teleport retains terminal
        // fall velocity, making subsequent button-contact tests USB dependent.
        const Point position(std::stod(args[1]),std::stod(args[2]));
        auto body=claw->GetRawComponent<PhysicsComponent>(true);
        body->SetFallHeight(0);body->SetHeightInAir(0);
        physics->VSetLinearSpeed(claw->GetGUID(),Point(0,0));
        physics->VSetPosition(claw->GetGUID(),position);
        claw->GetPositionComponent()->SetPosition(position);
        IEventMgr::Get()->VTriggerEvent(IEventDataPtr(new EventData_Move_Actor(claw->GetGUID(),position)));
        if(args.size()==4 && args[3]=="sword") {
            // Same ordinary input event as combatkey, without a USB round trip
            // that would let the falling player pass a hanging target first.
            keyEvent(SDLK_LCTRL,true);heldKeys[SDLK_LCTRL]=SDL_GetTicks()+100;
        }
        return true;
    }
    if(args[0]=="campaignshot" && args.size()==4) {
        // Explicit projectile fixture: actual physics, collision and fuse apply.
        // No direct damage callback or boss health modification is permitted.
        const AmmoType ammo=args[1]=="dynamite"?AmmoType_Dynamite:AmmoType_Pistol;
        ActorTemplates::CreateClawProjectile(ammo,Direction_Right,
            Point(std::stod(args[2]),std::stod(args[3])),claw->GetGUID(),Point(0,0));
        return true;
    }
    if(args[0]=="campaignmap" || args[0]=="campaignfinish") {
        const int level=logic->GetCurrentLevelData()->GetLevelNumber();
        int endings=0;
        for(const auto& pair:actors) {
            const auto actor=pair.second;
            const auto position=actor->GetPositionComponent();
            if(!position)continue;
            const bool ending=actor->GetRawComponent<EndLevelPickupComponent>(false)!=nullptr;
            const bool checkpoint=actor->GetRawComponent<CheckpointComponent>(false)!=nullptr;
            const auto name=actor->GetName();
            bool boss=false;
            for(const std::string suffix:{"_LaRaux","_Katherine","_Wolvington","_Gabriel","_Marrow","_Aquatis","_RedTail","_Omar"})
                if(name.size()>=suffix.size() && name.compare(name.size()-suffix.size(),suffix.size(),suffix)==0)boss=true;
            if(ending || checkpoint || boss || name.find("Level12_Aquatis")==0 || name.find("Level10_Marrow")==0 || name.find("Level8_Gabriel")==0) {
                auto hp=actor->GetRawComponent<HealthComponent>(false);
                SDL_Log("Pazur campaign object: level=%d kind=%s id=%u name=%s x=%.1f y=%.1f hp=%d",
                    level,ending?"exit":checkpoint?"checkpoint":boss?"boss":"arena",actor->GetGUID(),name.c_str(),
                    position->GetX(),position->GetY(),hp?hp->GetHealth():-1);
            }
            if(ending) {
                ++endings;
                if(args[0]=="campaignfinish") {
                    // Explicit technical fixture: reach the EXISTING end item.
                    // Normal physics must collect it; never synthesize completion.
                    Handle({"combatkey","release","0"},actors);
                    const auto p=position->GetPosition();
                    physics->VSetLinearSpeed(claw->GetGUID(),Point(0,0));
                    physics->VSetPosition(claw->GetGUID(),p);
                    claw->GetPositionComponent()->SetPosition(p.x,p.y);
                    SDL_Log("Pazur campaign fixture: teleport-to-existing-exit level=%d",level);
                    break;
                }
            }
        }
        SDL_Log("Pazur campaign state: level=%d exits=%d health=%d lives=%d",
            level,endings,claw->GetRawComponent<HealthComponent>(true)->GetHealth(),
            claw->GetRawComponent<LifeComponent>(true)->GetLives());
        return true;
    }
    if(args[0]=="laddertrace" && args.size()==3) {
        ladderTrace=LadderTrace{};
        ladderTrace.label=args[1];
        ladderTrace.end=SDL_GetTicks()+(std::max)(100,(std::min)(10000,std::stoi(args[2])));
        return true;
    }
    if(args[0]=="pegtrial" && args.size()==5) {
        ResetKeys();
        pegTrial=PegTrial{};
        const Point from(std::stod(args[1]),std::stod(args[2]));
        const Point to(std::stod(args[3]),std::stod(args[4]));
        for(const auto& pair:actors) {
            auto actor=pair.second;
            if(!actor->GetRawComponent<TogglePegAIComponent>(false))continue;
            const auto p=actor->GetPositionComponent()->GetPosition();
            if(std::abs(p.x-from.x)<5 && std::abs(p.y-from.y)<5)pegTrial.source=actor;
            if(std::abs(p.x-to.x)<5 && std::abs(p.y-to.y)<5)pegTrial.destination=actor;
        }
        auto source=pegTrial.source.lock();
        if(!source || pegTrial.destination.expired()) {
            SDL_Log("Pazur peg trial: rejected=platform-not-found");return true;
        }
        pegTrial.active=true;pegTrial.started=SDL_GetTicks();
        SDL_Log("Pazur peg trial: started source=%.0f,%.0f target=%.0f,%.0f catnip=%d",
            from.x,from.y,to.x,to.y,
            claw->GetRawComponent<PowerupComponent>(true)->HasPowerup(PowerupType_Catnip));
        return true;
    }
    if(args[0]=="combatlastlife") {
        // Enter the normal last-life death/animation/menu path, not a fake UI.
        claw->GetRawComponent<LifeComponent>(true)->SetCurrentLives(0);
        claw->GetRawComponent<HealthComponent>(true)->SetCurrentHealth(0);
        return true;
    }
    if(args[0]=="combatstairs" && args.size()==4) {
        const int rise=std::stoi(args[3]);
        const double distance=std::stod(args[2]);
        if(rise<1 || rise>128 || std::abs(distance)<60 || std::abs(distance)>160)return true;
        Handle({"combatstage",args[1],args[2],std::to_string(5-rise)},actors);
        // One raised step per fresh process; real offensive AI and normal player
        // health remain enabled. Never accumulate different steps in one arena.
        physics->VAddStaticGeometry(Point(distance>0?200040:199700,1100-rise),
            Point(260,rise+64),CollisionType_Solid,FixtureType_Solid);
        SDL_Log("Pazur stairs fixture: rise=%d side=%d",rise,distance>0?1:-1);
        return true;
    }
    if (args[0]=="laddermap") {
        const int level=logic->GetCurrentLevelData()->GetLevelNumber();
        auto archive=WAP_LoadRezArchive("CLAW.REZ");
        if (!archive) return true;
        const auto path="/LEVEL"+std::to_string(level)+"/WORLDS/WORLD.WWD";
        auto world=WAP_WwdLoadFromRezArchive(archive,path.c_str());
        auto metadata=g_pApp->GetLevelMetadata(level);
        if (world) {
            for (unsigned p=0;p<world->planesCount;++p) {
                const auto& plane=world->planes[p];
                if (!(plane.properties.flags&WAP_PLANE_FLAG_MAIN_PLANE)) continue;
                for (unsigned y=0;y<plane.properties.tilesOnAxisY;++y)
                    for (unsigned x=0;x<plane.properties.tilesOnAxisX;++x) {
                        const int tile=plane.tiles[y*plane.properties.tilesOnAxisX+x];
                        const auto end=metadata->tileIdToTopLadderEndMap.find(tile);
                        if (end!=metadata->tileIdToTopLadderEndMap.end())
                            SDL_Log("Pazur ladder map: level=%d x=%d top=%d tile=%d",level,
                                int(x*64+end->second.x),int(y*64+end->second.y),tile);
                    }
            }
            WAP_WwdDestroy(world);
        }
        WAP_DestroyRezArchive(archive);
        return true;
    }
    if (args[0]=="ladderstage") {
        // Isolated static ladder and its one-way cap, using the production fixtures.
        Handle({"combatstage","-1","80","0"},actors);
        static WeakActorPtr ladderClaw;
        if (ladderClaw.lock()!=claw) {
            physics->VAddStaticGeometry(Point(199968,768),Point(64,320),CollisionType_Climb,FixtureType_Climb);
            physics->VAddStaticGeometry(Point(199968,768),Point(64,10),CollisionType_Ground,FixtureType_TopLadderGround);
            ladderClaw=claw;
        }
        SDL_Log("Pazur ladder fixture: x=200000 top=768 bottom=1088");
        return true;
    }
    if (args[0]=="edgestage") {
        Handle({"combatstage","-1","80","0"},actors);
        static WeakActorPtr edgeClaw;
        if(edgeClaw.lock()!=claw) {
            // Upper ledge and lower catch floor, using ordinary production ground.
            physics->VAddStaticGeometry(Point(205872,768),Point(256,20),CollisionType_Ground,FixtureType_Solid);
            physics->VAddStaticGeometry(Point(205200,2368),Point(1600,20),CollisionType_Ground,FixtureType_Solid);
            edgeClaw=claw;
        }
        SDL_Log("Pazur edge fixture: left=205872 right=206128 top=768 catch=2368");
        return true;
    }
    if (args[0]=="ladderstatus") {
        auto pc=claw->GetPhysicsComponent();
        auto anim=claw->GetRawComponent<AnimationComponent>(true);
        const auto box=physics->VGetAABB(claw->GetGUID(),true);
        const auto position=claw->GetPositionComponent()->GetPosition();
        const auto velocity=pc->GetVelocity();
        SDL_Log("Pazur ladder status: x=%.1f y=%.1f bottom=%d climb=%d ladder=%d ground=%d vy=%.2f animation=%s paused=%d",
            position.x,position.y,box.y+box.h,pc->IsClimbing(),pc->IsOnLadder(),pc->IsOnGround(),velocity.y,
            anim->GetCurrentAnimationName().c_str(),anim->GetCurrentAnimation()->IsPaused());
        return true;
    }
    if (args[0] == "combatmap") {
        int count=0;
        for (const auto& pair : actors) {
            auto actor=pair.second;
            bool regular=false;
            for (const auto name : combatTypeNames) if (actor->GetName()==name) { regular=true; break; }
            if (!regular || !actor->GetRawComponent<EnemyAIComponent>(false)) continue;
            auto hp=actor->GetRawComponent<HealthComponent>(true);
            auto position=actor->GetPositionComponent()->GetPosition();
            const auto box=physics->VGetAABB(actor->GetGUID(),true);
            SDL_Log("Pazur map enemy: actor=%s id=%u hp=%d max=%d x=%.0f y=%.0f box=%d,%d,%d,%d",
                actor->GetName().c_str(),actor->GetGUID(),hp->GetHealth(),hp->GetMaxHealth(),
                position.x,position.y,box.x,box.y,box.w,box.h);
            ++count;
        }
        SDL_Log("Pazur map enemy count: %d",count);
        return true;
    }
    if (args[0] == "combatjumpattack" && (args.size() == 3 || args.size() == 4)) {
        ResetKeys();
        const auto now=SDL_GetTicks();
        keyEvent(SDLK_SPACE,true);
        heldKeys[SDLK_SPACE]=now+(std::max)(20,(std::min)(1000,std::stoi(args[1])));
        scheduledSwordAt=now+(std::max)(20,(std::min)(1000,std::stoi(args[2])));
        if(args.size()==4 && (args[3]=="left" || args[3]=="right")) {
            const auto direction=args[3]=="left"?SDLK_LEFT:SDLK_RIGHT;
            keyEvent(direction,true);heldKeys[direction]=now+250;
        }
        return true;
    }
    if (args[0] == "combatkey" && args.size() == 3) {
        if (args[1] == "release") { ResetKeys(); return true; }
        const std::map<std::string,SDL_Keycode> keys{{"left",SDLK_LEFT},{"right",SDLK_RIGHT},
            {"down",SDLK_DOWN},{"up",SDLK_UP},{"sword",SDLK_LCTRL},{"pistol",SDLK_LALT},{"jump",SDLK_SPACE}};
        auto found=keys.find(args[1]);
        if (found == keys.end()) return true;
        if (heldKeys.count(found->second)) keyEvent(found->second,false);
        keyEvent(found->second,true);
        heldKeys[found->second]=SDL_GetTicks()+(std::max)(20,(std::min)(6000,std::stoi(args[2])));
        return true;
    }
    if (args[0] == "combatstatus") { status(); return true; }
    if (args[0] == "combatjumpmeasure" && args.size()==2) {
        jumpTrace=JumpTrace{};
        jumpTrace.armed=true;
        jumpTrace.label=args[1];
        jumpTrace.baseY=claw->GetPositionComponent()->GetY();
        return true;
    }
    if ((args[0] == "combatstage" || args[0] == "combatdummy") && args.size() == 4) {
        if (claw->GetRawComponent<ClawControllableComponent>(true)->IsDying()) {
            SDL_Log("Pazur probe rejected: player is dying; start a fresh process");
            return true;
        }
        ResetKeys();
        const int index = std::stoi(args[1]);
        if (index < -1 || index >= int(sizeof(combatPrototypes)/sizeof(combatPrototypes[0]))) return true;
        const double distance = std::stod(args[2]), dy = std::stod(args[3]);
        if (fixtureClaw.lock() != claw) { floorCreated = false; fixtureClaw = claw; }
        // Only the temporary process is changed; no level or save is written.
        std::vector<uint32> remove;
        for (const auto& pair : actors) {
            auto actor = pair.second;
            auto position = actor->GetPositionComponent();
            const bool inArena = position && position->GetX()>199000 && position->GetX()<201000;
            if (actor != claw && (actor->GetRawComponent<EnemyAIComponent>(false) ||
                actor->GetRawComponent<ProjectileAIComponent>(false) || actor->GetRawComponent<AreaDamageComponent>(false) || inArena))
                remove.push_back(pair.first);
        }
        // Notify the scene as well as the actor map; direct deletion would leave render nodes dangling.
        for (auto id : remove) IEventMgr::Get()->VTriggerEvent(IEventDataPtr(new EventData_Destroy_Actor(id)));
        target.reset();
        if (!floorCreated) {
            physics->VAddStaticGeometry(Point(199000,1100), Point(2000,64), CollisionType_Solid, FixtureType_Solid);
            floorCreated = true;
        }
        auto control = claw->GetRawComponent<ClawControllableComponent>(true);
        auto health = claw->GetRawComponent<HealthComponent>(true);
        health->SetCurrentHealth(100);
        health->SetInvulnerable(false);
        control->SetFrozen(false);
        control->SetFrozenTime(0);
        control->OnStand();
        auto pc = claw->GetPhysicsComponent();
        pc->SetCurrentSpeed(Point(0,0));
        pc->SetFallHeight(0);
        pc->SetHeightInAir(0);
        pc->RestoreGravityScale();
        physics->VSetLinearSpeed(claw->GetGUID(),Point(0,0));
        physics->VScaleActor(claw->GetGUID(),2.0);
        physics->VSetPosition(claw->GetGUID(),arena);
        claw->GetPositionComponent()->SetPosition(arena.x,arena.y);
        claw->GetRawComponent<AmmoComponent>(true)->SetActiveAmmo(AmmoType_Pistol);
        claw->GetRawComponent<AmmoComponent>(true)->SetAmmo(AmmoType_Pistol,99);
        g_pApp->GetHumanView()->GetCamera()->VSetPosition(arena-Point(g_pApp->GetWindowSizeScaled().x/2,240));
        if (index >= 0) {
            auto xml = g_pApp->GetActorPrototypeElem(combatPrototypes[index]);
            auto pos = xml->FirstChildElement("PositionComponent")->FirstChildElement("Position");
            pos->SetAttribute("x", int(arena.x+distance));
            pos->SetAttribute("y", int(arena.y+dy));
            if (auto mirrored=xml->FirstChildElement("ActorRenderComponent")->FirstChildElement("Mirrored"))
                mirrored->FirstChild()->SetValue((xml->FirstChildElement("PunkRatAIStateComponent") ? distance>0 : distance<0) ? "true" : "false");
            auto body = xml->FirstChildElement("PhysicsComponent");
            if (auto clamp = body->FirstChildElement("ClampToGround")) clamp->FirstChild()->SetValue("false");
            if (auto patrol = xml->FirstChildElement("PatrolEnemyAIStateComponent")) {
                for (const auto& value : {std::make_pair("LeftPatrolBorder",199200), std::make_pair("RightPatrolBorder",200800)})
                    if (auto e=patrol->FirstChildElement(value.first)) e->FirstChild()->SetValue(std::to_string(value.second));
                if (args[0]=="combatdummy") {
                    if (auto e=patrol->FirstChildElement("IsAlwaysIdle")) e->FirstChild()->SetValue("true");
                    if (auto e=patrol->FirstChildElement("PatrolSpeed")) e->FirstChild()->SetValue("0");
                }
            }
            if (args[0]=="combatdummy") {
                for (auto e=xml->FirstChildElement(); e;) {
                    auto next=e->NextSiblingElement();
                    const std::string name=e->Value();
                    if (name.find("AttackAIStateComponent")!=std::string::npos ||
                        name=="PunkRatAIStateComponent" || name=="RollEnemyAIStateComponent") xml->RemoveChild(e);
                    e=next;
                }
            }
            target = logic->VCreateActor(xml,nullptr);
            delete xml;
        }
        SDL_Log("Pazur probe stage: index=%d distance=%.0f dy=%.0f",index,distance,dy);
        status();
        return true;
    }
    if (args[0] == "combatshot" && args.size() == 3) {
        const double height = std::stod(args[1]);
        const bool right = std::stoi(args[2]) > 0;
        const auto position = claw->GetPositionComponent()->GetPosition();
        // Ignore scenery in this isolated fixture, so a shot below the feet can reach the foot sensor.
        ActorTemplates::CreateProjectile("/LEVEL1/IMAGES/MUSKETBALL/*",10,DamageType_Bullet,
            right ? Direction_Right : Direction_Left,
            position+Point(right ? -180 : 180,height), CollisionFlag_EnemyAIProjectile,
            CollisionFlag_Controller|CollisionFlag_InvisibleController,INVALID_ACTOR_ID);
        SDL_Log("Pazur probe shot: height=%.0f right=%d",height,right);
        return true;
    }
    if (args[0] == "combatduplicate") {
        auto enemy = target.lock();
        if (!enemy) return true;
        auto hp = enemy->GetRawComponent<HealthComponent>(true);
        auto shot = ActorTemplates::CreateProjectile("/LEVEL1/IMAGES/MUSKETBALL/*",1,DamageType_Bullet,
            Direction_Right,enemy->GetPositionComponent()->GetPosition(),CollisionFlag_Bullet,0,claw->GetGUID());
        auto projectile = shot->GetRawComponent<ProjectileAIComponent>(true);
        const int before = hp->GetHealth();
        projectile->OnCollidedWithActor(enemy.get());
        const int first = hp->GetHealth();
        projectile->OnCollidedWithActor(enemy.get());
        SDL_Log("Pazur probe duplicate: before=%d first=%d second=%d",before,first,hp->GetHealth());
        return true;
    }
    return false;
}

void PazurCombatProbe::ResetKeys() {
    scheduledSwordAt=0;
    for (const auto& key : heldKeys) keyEvent(key.first,false);
    heldKeys.clear();
}

void PazurCombatProbe::JumpInput(bool down, Uint32 eventTime) {
    if (!jumpTrace.armed) return;
    const auto now=SDL_GetTicks();
    if (down && !jumpTrace.received) {
        jumpTrace.received=true;
        jumpTrace.inputTime=now;
        jumpTrace.queueMs=eventTime && (Sint32)(now-eventTime)>=0 ? now-eventTime : 0;
    } else if (!down && jumpTrace.received && !jumpTrace.releaseMs) {
        jumpTrace.releaseMs=now-jumpTrace.inputTime;
    }
}

void PazurCombatProbe::Poll() {
    const auto now=SDL_GetTicks();
    for (auto it=heldKeys.begin(); it!=heldKeys.end();) {
        if ((Sint32)(now-it->second)>=0) { keyEvent(it->first,false); it=heldKeys.erase(it); }
        else ++it;
    }
    if (!g_pApp || !g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14 ||
        !g_pApp->GetGameLogic()) return;
    const bool playing=g_pApp->GetGameLogic()->IsRunning() &&
        g_pApp->GetGameLogic()->GetGameState()==GameState_IngameRunning;
    if(scheduledSwordAt) {
        if(!playing)scheduledSwordAt=0;
        else if((Sint32)(now-scheduledSwordAt)>=0) {
            scheduledSwordAt=0;
            keyEvent(SDLK_LCTRL,true);
            heldKeys[SDLK_LCTRL]=now+100;
        }
    }
    if(ladderTrace.end) {
        if(!playing || (Sint32)(now-ladderTrace.end)>=0) {
            SDL_Log("Pazur ladder trace end: label=%s",ladderTrace.label.c_str());
            ladderTrace.end=0;
        } else {
            auto claw=g_pApp->GetGameLogic()->GetClawActor();
            auto pc=claw->GetPhysicsComponent();
            const auto animation=claw->GetRawComponent<AnimationComponent>(true)->GetCurrentAnimationName();
            const auto state=std::to_string(pc->IsOnGround())+std::to_string(pc->IsOnLadder())+
                std::to_string(pc->IsClimbing())+animation;
            // Sample every transition, including one-frame contact changes;
            // unchanged states need only ten samples per second.
            if(state!=ladderTrace.previousState || (Sint32)(now-ladderTrace.nextSample)>=0) {
                const auto p=claw->GetPositionComponent()->GetPosition();
                const auto v=pc->GetVelocity();
                SDL_Log("Pazur ladder trace: label=%s tick=%u x=%.2f y=%.2f ground=%d ladder=%d climb=%d vx=%.9f vy=%.9f animation=%s falling=%d jumping=%d",
                    ladderTrace.label.c_str(),now,p.x,p.y,pc->IsOnGround(),pc->IsOnLadder(),pc->IsClimbing(),
                    v.x,v.y,animation.c_str(),pc->IsFalling(),pc->IsJumping());
                ladderTrace.previousState=state;ladderTrace.nextSample=now+100;
            }
        }
    }
    if(pegTrial.active) {
        auto source=pegTrial.source.lock(), destination=pegTrial.destination.lock();
        auto logic=g_pApp->GetGameLogic();
        auto claw=logic->GetClawActor();
        if(!playing || !source || !destination || !claw) {
            pegTrial.active=false;ResetKeys();
        } else {
            auto physics=logic->VGetGamePhysics();
            auto pc=claw->GetPhysicsComponent();
            const int frame=destination->GetRawComponent<AnimationComponent>(true)
                ->GetCurrentAnimation()->GetCurrentAnimationFrame()->idx;
            const int sourceFrame=source->GetRawComponent<AnimationComponent>(true)
                ->GetCurrentAnimation()->GetCurrentAnimationFrame()->idx;
            // Inactive Box2D fixtures have no broad-phase proxies. Query their
            // AABB only while solid; retain the target bounds during off phases.
            if(frame<2)pegTrial.targetBox=physics->VGetAABB(destination->GetGUID(),true);
            if(!pegTrial.positioned && sourceFrame<2) {
                const auto sourceBox=physics->VGetAABB(source->GetGUID(),true);
                pegTrial.sourceBox=sourceBox;
                const Point start(source->GetPositionComponent()->GetX(),sourceBox.y-70);
                pc->SetFallHeight(0);pc->SetHeightInAir(0);pc->SetCurrentSpeed(Point(0,0));
                claw->GetRawComponent<ClawControllableComponent>(true)->OnStand();
                physics->VSetLinearSpeed(claw->GetGUID(),Point(0,0));
                physics->VSetPosition(claw->GetGUID(),start);
                claw->GetPositionComponent()->SetPosition(start.x,start.y);
                pegTrial.positioned=true;pegTrial.positionedAt=now;
            }
            const auto p=claw->GetPositionComponent()->GetPosition();
            const auto targetBox=pegTrial.targetBox;
            const auto box=physics->VGetAABB(claw->GetGUID(),true);
            if(pegTrial.positioned && now-pegTrial.positionedAt>200 && !pegTrial.launched && pc->IsOnGround() &&
                std::abs(box.y+box.h-pegTrial.sourceBox.y)<5 && frame<2) {
                pegTrial.launched=now;pegTrial.baseY=p.y;
                keyEvent(SDLK_SPACE,true);heldKeys[SDLK_SPACE]=now+600;
                const double dx=destination->GetPositionComponent()->GetX()-p.x;
                const auto key=dx<0?SDLK_LEFT:SDLK_RIGHT;
                keyEvent(key,true);heldKeys[key]=now+Uint32(std::abs(dx)/350.0*1000);
                SDL_Log("Pazur peg launch: x=%.1f y=%.1f target_top=%d frame=%d",p.x,p.y,targetBox.y,frame);
            }
            if(pegTrial.launched)pegTrial.rise=(std::max)(pegTrial.rise,pegTrial.baseY-p.y);
            const bool landed=pegTrial.launched && now-pegTrial.launched>200 && pc->IsOnGround() &&
                std::abs(box.y+box.h-targetBox.y)<5 && p.x>=targetBox.x && p.x<=targetBox.x+targetBox.w;
            if(landed || now-pegTrial.started>8000 || (pegTrial.launched && p.y>pegTrial.baseY+200)) {
                SDL_Log("Pazur peg result: landed=%d rise=%.1f x=%.1f y=%.1f bottom=%d target_top=%d frame=%d",
                    landed,pegTrial.rise,p.x,p.y,box.y+box.h,targetBox.y,frame);
                pegTrial.active=false;ResetKeys();
            }
        }
    }
    if (playing && jumpTrace.armed && jumpTrace.received) {
        auto claw=g_pApp->GetGameLogic()->GetClawActor();
        const double rise=jumpTrace.baseY-claw->GetPositionComponent()->GetY();
        jumpTrace.rise=(std::max)(jumpTrace.rise,rise);
        if (rise>2 && !jumpTrace.airborne) {
            jumpTrace.airborne=true;
            ++jumpTrace.jumps;
            if (jumpTrace.takeoffMs<0) jumpTrace.takeoffMs=now-jumpTrace.inputTime;
        } else if (rise<1) jumpTrace.airborne=false;
        if (now-jumpTrace.inputTime>=2200) {
            SDL_Log("Pazur jump trace: label=%s queue_ms=%u takeoff_ms=%d rise=%.1f hold_ms=%u jumps=%d",
                jumpTrace.label.c_str(),jumpTrace.queueMs,jumpTrace.takeoffMs,jumpTrace.rise,
                jumpTrace.releaseMs,jumpTrace.jumps);
            jumpTrace.armed=false;
        }
    }
    static Uint32 lastPoll=0;
    if (now-lastPoll<100) return;
    lastPoll=now;
    std::ifstream input("combat-command.txt");
    std::string line;
    if (!std::getline(input,line)) return;
    input.close();
    std::remove("combat-command.txt");
    const auto separator=line.find('|');
    if (separator==std::string::npos) return;
    const auto ticket=line.substr(0,separator);
    auto command=line.substr(separator+1);
    if (!command.empty() && command.back()=='\r') command.pop_back();
    // Combat fixtures require live physics. Virtual button releases must work while paused.
    const bool allowed=playing || command.compare(0,11,"padvirtual ")==0;
    if (allowed) CommandHandler::HandleCommand(command.c_str(),g_pApp->GetHumanView()->GetConsole().get());
    std::ofstream response("combat-response.txt");
    response<<ticket<<(allowed ? "|done\n" : "|rejected: game not running\n");
}
