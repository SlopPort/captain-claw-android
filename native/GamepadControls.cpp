#include "GamepadControls.h"
#include "PlatformInput.h"
#include "CombatProbe.h"
#include "Engine/GameApp/BaseGameApp.h"
#include "Engine/GameApp/BaseGameLogic.h"
#include <array>
#include <map>
#include <set>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <jni.h>

namespace {
// Separate press/release thresholds prevent stick drift near the dead zone
// from rapidly alternating movement. Values are SDL's signed 16-bit axis units.
constexpr int pressThreshold=9830,releaseThreshold=7208;
struct Pad {
    SDL_GameController* controller=nullptr;
    std::array<Sint16,SDL_CONTROLLER_AXIS_MAX> axes{};
    std::array<bool,SDL_CONTROLLER_BUTTON_MAX> buttons{};
    bool left=false,right=false,up=false,down=false,trigger=false;
};
std::map<SDL_JoystickID,Pad> pads;
SDL_JoystickID activePad=-1;
std::set<SDL_Keycode> pressed;
std::map<SDL_Keycode,Uint32> repeatAt;
bool suspended=false,awaitNeutral=true,usingController=false;
int lastContext=-1;
Uint32 jumpUntil=0;
SDL_Joystick* virtualPad=nullptr;
// Android button codes are captured before SDL's device-specific remapping.
// Persist action bindings, not printed Xbox/Switch labels. SDL still owns axes.
constexpr int rawEventCode=0x50414442;
const char* actionNames[]={"jump","attack","fire","weapon","pause","confirm","back"};
const int defaultBindings[]={96,99,97,100,108,96,97};
std::array<int,7> bindings{{96,99,97,100,108,96,97}};
std::set<std::pair<int,int>> rawHeld;
Uint32 bindingPoll=0;
void reloadBindings() {
    const auto now=SDL_GetTicks();
    if (bindingPoll && (Sint32)(now-bindingPoll)<1000) return;
    bindingPoll=now;
    std::array<int,7> next;
    std::copy(std::begin(defaultBindings),std::end(defaultBindings),next.begin());
    std::ifstream file("controller-bindings.txt");
    std::string line;
    while (std::getline(file,line)) {
        const auto split=line.find('=');
        if (split==std::string::npos) continue;
        std::istringstream value(line.substr(split+1));int code;
        if (!(value>>code) || code<0 || code>1001) continue;
        for (int i=0;i<7;++i) if (line.substr(0,split)==actionNames[i]) next[i]=code;
    }
    if (next!=bindings) {
        bindings=next;awaitNeutral=true;
        SDL_Log("Pazur pad bindings reloaded");
    }
}
bool rawAction(int action,const Pad& pad) {
    const int code=bindings[action];
    if (code==1000) return pad.axes[SDL_CONTROLLER_AXIS_TRIGGERLEFT]>16000;
    if (code==1001) return pad.axes[SDL_CONTROLLER_AXIS_TRIGGERRIGHT]>16000;
    for (const auto& key:rawHeld) if (key.second==code) return true;
    return false;
}

int context() {
    if (!g_pApp || !g_pApp->GetGameLogic()) return 0;
    const auto state=g_pApp->GetGameLogic()->GetGameState();
    // ScreenElementMenu pauses with SetRunning(false), without changing GameState.
    // Keep routing input to that menu so Start/B can resume the game.
    if (state==GameState_IngameRunning) return g_pApp->GetGameLogic()->IsRunning()?1:2;
    if (state==GameState_Menu || state==GameState_IngamePaused || state==GameState_ScoreScreen) return 2;
    return 0;
}
void release() {
    PazurInput::Reset(PazurInput::Controller);
    pressed.clear();repeatAt.clear();jumpUntil=0;
}
bool neutral(const Pad& pad) {
    // After focus/context changes, require release before accepting input again;
    // otherwise the pause button or a held jump could trigger in the new screen.
    if (!rawHeld.empty()) return false;
    for (bool down:pad.buttons) if (down) return false;
    return std::abs(int(pad.axes[SDL_CONTROLLER_AXIS_LEFTX]))<releaseThreshold &&
        std::abs(int(pad.axes[SDL_CONTROLLER_AXIS_LEFTY]))<releaseThreshold &&
        pad.axes[SDL_CONTROLLER_AXIS_TRIGGERRIGHT]<releaseThreshold &&
        pad.axes[SDL_CONTROLLER_AXIS_TRIGGERLEFT]<releaseThreshold;
}
void open(int index) {
    if (!SDL_IsGameController(index)) {
        SDL_Log("Pazur pad unsupported: name=%s",SDL_JoystickNameForIndex(index));
        return;
    }
    const auto id=SDL_JoystickGetDeviceInstanceID(index);
    if (pads.count(id)) return;
    auto handle=SDL_GameControllerOpen(index);
    if (!handle) { SDL_Log("Pazur pad open failed: %s",SDL_GetError());return; }
    Pad pad;pad.controller=handle;
    for (int a=0;a<SDL_CONTROLLER_AXIS_MAX;++a) pad.axes[a]=SDL_GameControllerGetAxis(handle,SDL_GameControllerAxis(a));
    for (int b=0;b<SDL_CONTROLLER_BUTTON_MAX;++b) pad.buttons[b]=SDL_GameControllerGetButton(handle,SDL_GameControllerButton(b));
    pads.emplace(id,pad);
    if (activePad<0) {activePad=id;awaitNeutral=true;}
    char guid[33];SDL_JoystickGetGUIDString(SDL_JoystickGetGUID(SDL_GameControllerGetJoystick(handle)),guid,sizeof(guid));
    SDL_Log("Pazur pad connected: name=%s guid=%s id=%d",SDL_GameControllerName(handle),guid,int(id));
}
void reconcile(Uint32 timestamp=0) {
    const int mode=context();
    if (mode!=lastContext) {
        release();awaitNeutral=true;lastContext=mode;
        SDL_Log("Pazur pad context: mode=%d",mode);
    }
    if (suspended || !mode || !pads.count(activePad)) {release();return;}
    auto& pad=pads.at(activePad);
    if (awaitNeutral) {
        release();
        if (neutral(pad)) awaitNeutral=false;
        else return;
    }
    const int x=pad.axes[SDL_CONTROLLER_AXIS_LEFTX],y=pad.axes[SDL_CONTROLLER_AXIS_LEFTY];
    pad.left= -x>(pad.left?releaseThreshold:pressThreshold);
    pad.right=x>(pad.right?releaseThreshold:pressThreshold);
    pad.up= -y>(pad.up?releaseThreshold:pressThreshold);
    pad.down=y>(pad.down?releaseThreshold:pressThreshold);
    pad.trigger=pad.axes[SDL_CONTROLLER_AXIS_TRIGGERRIGHT]>(pad.trigger?10000:16000);
    auto b=[&](SDL_GameControllerButton key){return pad.buttons[key];};
    std::set<SDL_Keycode> next;
    if (pad.left||b(SDL_CONTROLLER_BUTTON_DPAD_LEFT)) next.insert(SDLK_LEFT);
    if (pad.right||b(SDL_CONTROLLER_BUTTON_DPAD_RIGHT)) next.insert(SDLK_RIGHT);
    if (pad.up||b(SDL_CONTROLLER_BUTTON_DPAD_UP)) next.insert(SDLK_UP);
    if (pad.down||b(SDL_CONTROLLER_BUTTON_DPAD_DOWN)) next.insert(SDLK_DOWN);
    const auto now=SDL_GetTicks();
    if (mode==1) {
        if (b(SDL_CONTROLLER_BUTTON_A)||rawAction(0,pad)) {
            if (!pressed.count(SDLK_SPACE)) jumpUntil=now+32;
            next.insert(SDLK_SPACE);
        } else if (pressed.count(SDLK_SPACE) && (Sint32)(now-jumpUntil)<0) next.insert(SDLK_SPACE);
        if (b(SDL_CONTROLLER_BUTTON_X)||rawAction(1,pad)) next.insert(SDLK_LCTRL);
        if (b(SDL_CONTROLLER_BUTTON_B)||rawAction(2,pad)) next.insert(SDLK_LALT);
        if (b(SDL_CONTROLLER_BUTTON_Y)||rawAction(3,pad)) next.insert(SDLK_LSHIFT);
        if (b(SDL_CONTROLLER_BUTTON_START)||b(SDL_CONTROLLER_BUTTON_BACK)||rawAction(4,pad)) next.insert(SDLK_ESCAPE);
    } else {
        if (b(SDL_CONTROLLER_BUTTON_A)||rawAction(5,pad)) next.insert(SDLK_RETURN);
        if (b(SDL_CONTROLLER_BUTTON_B)||b(SDL_CONTROLLER_BUTTON_BACK)||rawAction(6,pad)) next.insert(SDLK_ESCAPE);
        if (rawAction(4,pad)) next.insert(g_pApp->GetGameLogic()->GetGameState()==GameState_Menu?SDLK_RETURN:SDLK_ESCAPE);
        if (b(SDL_CONTROLLER_BUTTON_START)) next.insert(g_pApp->GetGameLogic()->GetGameState()==GameState_Menu?SDLK_RETURN:SDLK_ESCAPE);
    }
    const auto previous=pressed;
    pressed=next;
    for (auto key:previous) if (!next.count(key)) {
        if (key==SDLK_SPACE) PazurCombatProbe::JumpInput(false,timestamp);
        PazurInput::SetKey(PazurInput::Controller,key,false);repeatAt.erase(key);
    }
    for (auto key:next) if (!previous.count(key)) {
        if (key==SDLK_SPACE) PazurCombatProbe::JumpInput(true,timestamp);
        PazurInput::SetKey(PazurInput::Controller,key,true);repeatAt[key]=now+350;
    }
    if (previous!=next) SDL_Log("Pazur pad state: left=%d right=%d jump=%d attack=%d fire=%d up=%d down=%d weapon=%d pause=%d confirm=%d",
        int(next.count(SDLK_LEFT)),int(next.count(SDLK_RIGHT)),int(next.count(SDLK_SPACE)),int(next.count(SDLK_LCTRL)),
        int(next.count(SDLK_LALT)),int(next.count(SDLK_UP)),int(next.count(SDLK_DOWN)),int(next.count(SDLK_LSHIFT)),
        int(next.count(SDLK_ESCAPE)),int(next.count(SDLK_RETURN)));
    if (mode==2) for (auto key:{SDLK_LEFT,SDLK_RIGHT,SDLK_UP,SDLK_DOWN}) {
        if (next.count(key) && (Sint32)(now-repeatAt[key])>=0) {
            PazurInput::Repeat(PazurInput::Controller,key);repeatAt[key]=now+100;
        }
    }
}
}

void PazurGamepad::Initialize() {
    bindingPoll=0;rawHeld.clear();reloadBindings();
    if (SDL_InitSubSystem(SDL_INIT_GAMECONTROLLER)<0) {SDL_Log("Pazur pad init failed: %s",SDL_GetError());return;}
    auto database=SDL_RWFromFile("controllers/gamecontrollerdb.txt","rb");
    SDL_Log("Pazur pad mappings: %d",database?SDL_GameControllerAddMappingsFromRW(database,1):-1);
    for (int i=0;i<SDL_NumJoysticks();++i) open(i);
}
bool PazurGamepad::Handle(const SDL_Event& event) {
    if (event.type==SDL_USEREVENT && event.user.code==rawEventCode) {
        const int device=int(reinterpret_cast<intptr_t>(event.user.data1));
        const int value=int(reinterpret_cast<intptr_t>(event.user.data2));
        const int key=value&0xffff;
        const bool down=(value&0x10000)!=0;
        if (!suspended && down) {rawHeld.insert({device,key});usingController=true;}
        else rawHeld.erase({device,key});
        SDL_Log("Pazur Android pad: key=%d down=%d",key,down);
        reconcile(event.user.timestamp);
        return true;
    }
    if (event.type==SDL_APP_WILLENTERBACKGROUND || (event.type==SDL_WINDOWEVENT && event.window.event==SDL_WINDOWEVENT_FOCUS_LOST)) {
        suspended=true;awaitNeutral=true;rawHeld.clear();release();
    }
    if (event.type==SDL_APP_DIDENTERFOREGROUND || (event.type==SDL_WINDOWEVENT && event.window.event==SDL_WINDOWEVENT_FOCUS_GAINED)) {
        suspended=false;awaitNeutral=true;
    }
    if (event.type==SDL_QUIT || event.type==SDL_APP_TERMINATING) {
        release();for (auto& p:pads) SDL_GameControllerClose(p.second.controller);pads.clear();return false;
    }
    if (event.type==SDL_CONTROLLERDEVICEADDED) {open(event.cdevice.which);return true;}
    if (event.type==SDL_CONTROLLERDEVICEREMOVED) {
        rawHeld.clear();
        auto found=pads.find(event.cdevice.which);
        if (found!=pads.end()) {SDL_GameControllerClose(found->second.controller);pads.erase(found);}
        if (activePad==event.cdevice.which) {release();activePad=pads.empty()?-1:pads.begin()->first;awaitNeutral=true;}
        if (pads.empty()) usingController=false;
        SDL_Log("Pazur pad disconnected: id=%d remaining=%d",int(event.cdevice.which),int(pads.size()));return true;
    }
    if (event.type==SDL_CONTROLLERDEVICEREMAPPED) {
        release();awaitNeutral=true;return true;
    }
    const bool axis=event.type==SDL_CONTROLLERAXISMOTION;
    const bool button=event.type==SDL_CONTROLLERBUTTONDOWN || event.type==SDL_CONTROLLERBUTTONUP;
    if (!axis && !button) return false;
    const auto id=axis?event.caxis.which:event.cbutton.which;
    auto found=pads.find(id);if (found==pads.end()) return true;
    auto& pad=found->second;
    if (axis && event.caxis.axis<SDL_CONTROLLER_AXIS_MAX) pad.axes[event.caxis.axis]=event.caxis.value;
    if (button && event.cbutton.button<SDL_CONTROLLER_BUTTON_MAX) pad.buttons[event.cbutton.button]=event.cbutton.state==SDL_PRESSED;
    const bool meaningful=(button && event.cbutton.state==SDL_PRESSED) ||
        (axis && ((event.caxis.axis==SDL_CONTROLLER_AXIS_LEFTX || event.caxis.axis==SDL_CONTROLLER_AXIS_LEFTY) && std::abs(int(event.caxis.value))>pressThreshold)) ||
        (axis && (event.caxis.axis==SDL_CONTROLLER_AXIS_TRIGGERRIGHT || event.caxis.axis==SDL_CONTROLLER_AXIS_TRIGGERLEFT) && event.caxis.value>16000);
    if (meaningful && !suspended) {
        usingController=true;
        if (activePad!=id) {release();activePad=id;awaitNeutral=false;}
    }
    reconcile(axis?event.caxis.timestamp:event.cbutton.timestamp);
    return true;
}
void PazurGamepad::Update() {reloadBindings();reconcile();}
void PazurGamepad::Shutdown() {
    // SDLActivity can launch native main again in the same Android process.
    // No controller handles or held states may survive that boundary.
    release();
    DebugCommand({"padvirtual","detach"});
    for (auto& pad:pads) SDL_GameControllerClose(pad.second.controller);
    pads.clear();rawHeld.clear();activePad=-1;lastContext=-1;
    suspended=false;awaitNeutral=true;usingController=false;
}
bool PazurGamepad::UsingController() {return usingController&&!pads.empty();}
void PazurGamepad::UseTouch() {usingController=false;}

bool PazurGamepad::DebugCommand(const std::vector<std::string>& args) {
    if (args.empty() || args[0]!="padvirtual") return false;
    if (args.size()==2 && args[1]=="attach") {
        if (virtualPad) return true;
        SDL_VirtualJoystickDesc desc{};desc.version=SDL_VIRTUAL_JOYSTICK_DESC_VERSION;
        desc.type=SDL_JOYSTICK_TYPE_GAMECONTROLLER;desc.naxes=SDL_CONTROLLER_AXIS_MAX;desc.nbuttons=SDL_CONTROLLER_BUTTON_MAX;
        desc.name="Pazur test controller";
        const int index=SDL_JoystickAttachVirtualEx(&desc);
        if (index>=0) {
            virtualPad=SDL_JoystickOpen(index);
            SDL_JoystickSetVirtualAxis(virtualPad,SDL_CONTROLLER_AXIS_TRIGGERLEFT,-32768);
            SDL_JoystickSetVirtualAxis(virtualPad,SDL_CONTROLLER_AXIS_TRIGGERRIGHT,-32768);
            SDL_JoystickUpdate();open(index);
        }
        SDL_Log("Pazur virtual pad: attached=%d",virtualPad!=nullptr);return true;
    }
    if (args.size()==2 && args[1]=="detach") {
        if (virtualPad) {
            const auto id=SDL_JoystickInstanceID(virtualPad);
            for (int i=0;i<SDL_NumJoysticks();++i) if (SDL_JoystickGetDeviceInstanceID(i)==id) {SDL_JoystickDetachVirtual(i);break;}
            SDL_JoystickClose(virtualPad);virtualPad=nullptr;
        }
        return true;
    }
    if (virtualPad && args.size()==4) {
        const int value=std::stoi(args[3]);
        if (args[1]=="raw") {
            SDL_Event event{};event.type=SDL_USEREVENT;event.user.code=rawEventCode;
            event.user.timestamp=SDL_GetTicks();
            event.user.data2=reinterpret_cast<void*>(intptr_t(std::stoi(args[2])|(value?0x10000:0)));
            SDL_PushEvent(&event);
        } else if (args[1]=="button") {
            const auto button=SDL_GameControllerGetButtonFromString(args[2].c_str());
            if (button>=0) SDL_JoystickSetVirtualButton(virtualPad,int(button),value?1:0);
        } else if (args[1]=="axis") {
            const auto axis=SDL_GameControllerGetAxisFromString(args[2].c_str());
            if (axis>=0) SDL_JoystickSetVirtualAxis(virtualPad,int(axis),Sint16((std::max)(-32768,(std::min)(32767,value))));
        }
        SDL_JoystickUpdate();
        return true;
    }
    return true;
}

extern "C" JNIEXPORT void JNICALL Java_pl_pazur_port_GameActivity_nativePadButton(
        JNIEnv*,jclass,jint device,jint key,jboolean down) {
    if (!SDL_WasInit(SDL_INIT_EVENTS)) return;
    SDL_Event event{};event.type=SDL_USEREVENT;event.user.code=rawEventCode;
    event.user.timestamp=SDL_GetTicks();
    event.user.data1=reinterpret_cast<void*>(intptr_t(device));
    event.user.data2=reinterpret_cast<void*>(intptr_t(key|(down?0x10000:0)));
    SDL_PushEvent(&event); // Cross from Java's UI thread to SDL's owning thread.
}
