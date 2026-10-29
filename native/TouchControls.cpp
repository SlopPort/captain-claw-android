#include "TouchControls.h"
#include "CombatProbe.h"
#include "GamepadControls.h"
#include "PlatformInput.h"
#include "OmarEncounterComponent.h"
#include "UiLanguage.h"
#include "GameplayBalance.h"
#include <algorithm>
#include <array>
#include <SDL2/SDL2_gfxPrimitives.h>
#include <map>
#include <set>
#include <cmath>
#include <jni.h>
#include "Engine/GameApp/BaseGameApp.h"
#include "Engine/GameApp/BaseGameLogic.h"

namespace {
void updateSettingsPosition(bool menu) {
    static int previous=-1;
    if(previous==int(menu))return;
    auto env=static_cast<JNIEnv*>(SDL_AndroidGetJNIEnv());
    auto activity=static_cast<jobject>(SDL_AndroidGetActivity());
    if(!env||!activity)return;
    auto type=env->GetObjectClass(activity);
    auto method=env->GetMethodID(type,"setMenuOverlay","(Z)V");
    if(method)env->CallVoidMethod(activity,method,jboolean(menu));
    if(env->ExceptionCheck()){env->ExceptionDescribe();env->ExceptionClear();}
    else if(method)previous=int(menu);
    env->DeleteLocalRef(type);env->DeleteLocalRef(activity);
}
struct Button { SDL_Rect rect; SDL_Keycode key; const char* polish; bool round; const char* english; };
const char* label(const Button& button) { return PazurUi::Text(button.polish,button.english); }
const Button buttons[] = {
    {{506, 346, 120, 120}, SDLK_SPACE, "SKOK", true, "JUMP"},
    {{378, 358, 104, 104}, SDLK_LCTRL, "ATAK", true, "ATTACK"},
    {{447, 228, 96, 96}, SDLK_LALT, "STRZAL", true, "SHOOT"},
    {{562, 110, 62, 34}, SDLK_LSHIFT, "BRON", false, "WEAPON"},
    {{16, 80, 66, 34}, SDLK_ESCAPE, "PAUZA", false, "PAUSE"},
};
std::map<SDL_FingerID, SDL_Keycode> fingers;
std::set<SDL_Keycode> pressed;
std::set<SDL_FingerID> directionFingers;
bool stickHeld = false;
SDL_FingerID stickFinger = 0;
float stickX = 0, stickY = 0;
int width();
int controlLayout=0;
int movement=0,deadzone=14;
std::array<int,15> buttonOptions{{100,0,0,100,0,0,100,0,0,100,0,0,100,0,0}};
float floatingX=100,floatingY=394;
float stickCenterX() { return movement==1&&stickHeld ? floatingX : controlLayout==3 ? width()-100 : 100; }
float stickCenterY() { return movement==1&&stickHeld ? floatingY : 394; }
const float stickTravel = 48;
Uint32 touchTimestamp=0;
Uint32 jumpPressedAt=0;
bool jumpMinimumPending=false;
// Touch taps should produce a useful low jump; holding still controls the full height.
constexpr Uint32 minimumJumpPressMs=110;

int width() { return static_cast<int>(g_pApp->GetWindowSizeScaled().x); }
SDL_Rect rect(const Button& button) {
    auto r = button.rect;
    if (button.key != SDLK_ESCAPE) {
        if(controlLayout==1 && button.round) {
            if(button.key==SDLK_SPACE) r={496,336,132,132};
            if(button.key==SDLK_LCTRL) r={352,348,120,120};
            if(button.key==SDLK_LALT) r={420,212,110,110};
        }
        if(controlLayout==2) {
            if(button.key==SDLK_SPACE) r=buttons[1].rect;
            if(button.key==SDLK_LCTRL) r=buttons[0].rect;
        }
        r.x += width() - 640;
        if(controlLayout==3)r.x=width()-r.x-r.w;
    }
    const int index=int(&button-buttons)*3;
    const int size=buttonOptions[index];
    const int newWidth=r.w*size/100,newHeight=r.h*size/100;
    r.x+=(r.w-newWidth)/2+buttonOptions[index+1];
    r.y+=(r.h-newHeight)/2+buttonOptions[index+2];
    r.w=newWidth;r.h=newHeight;
    r.x=(std::max)(0,(std::min)(width()-r.w,r.x));
    r.y=(std::max)(0,(std::min)(480-r.h,r.y));
    return r;
}

SDL_Rect directionRect(int i) {
    const int cx=controlLayout==3 ? width()-100 : 100;
    const SDL_Rect positions[]={{cx-88,368,56,56},{cx+32,368,56,56},{cx-28,308,56,56},{cx-28,428,56,50}};
    return positions[i];
}
SDL_Keycode directionHit(float x,float y) {
    const SDL_Keycode keys[]={SDLK_LEFT,SDLK_RIGHT,SDLK_UP,SDLK_DOWN};
    for(int i=0;i<4;i++){auto r=directionRect(i);if(x>=r.x&&x<r.x+r.w&&y>=r.y&&y<r.y+r.h)return keys[i];}
    return SDLK_UNKNOWN;
}

bool active() {
    return g_pApp && g_pApp->GetGameLogic()
        && g_pApp->GetGameLogic()->GetGameState() == GameState_IngameRunning
        && g_pApp->GetGameLogic()->IsRunning();
}

SDL_Keycode hit(float x, float y) {
    for (const auto& button : buttons) {
        const auto r = rect(button);
        if (button.round) {
            const float dx=x-r.x-r.w/2, dy=y-r.y-r.h/2;
            const float radius=r.w/2+6;
            if (dx*dx+dy*dy<=radius*radius) return button.key;
            continue;
        }
        if (x >= r.x && x < r.x+r.w && y >= r.y && y < r.y+r.h) return button.key;
    }
    return SDLK_UNKNOWN;
}

void sendKey(SDL_Keycode key, bool down) {
    if (key==SDLK_SPACE) PazurCombatProbe::JumpInput(down,touchTimestamp);
    PazurInput::SetKey(PazurInput::Touch,key,down);
}

void reconcile() {
    std::set<SDL_Keycode> next;
    for (const auto& finger : fingers) if (finger.second != SDLK_UNKNOWN) next.insert(finger.second);
    const auto now=SDL_GetTicks();
    if (next.count(SDLK_SPACE)) {
        if (!pressed.count(SDLK_SPACE)) { jumpPressedAt=now; jumpMinimumPending=true; }
    } else if (jumpMinimumPending && now-jumpPressedAt<minimumJumpPressMs) {
        next.insert(SDLK_SPACE);
    } else jumpMinimumPending=false;
    // Ignore small thumb drift. Eight directions allow climbing while moving sideways.
    const float magnitude = std::sqrt(stickX*stickX + stickY*stickY);
    if (stickHeld && magnitude >= deadzone) {
        const float threshold = magnitude * 0.45f;
        if (stickX < -threshold) next.insert(SDLK_LEFT);
        if (stickX > threshold) next.insert(SDLK_RIGHT);
        if (stickY < -threshold) next.insert(SDLK_UP);
        if (stickY > threshold) next.insert(SDLK_DOWN);
    }
    for (auto key : pressed) if (!next.count(key)) sendKey(key, false);
    for (auto key : next) if (!pressed.count(key)) sendKey(key, true);
    if (pressed != next) {
        SDL_Log("Pazur controls: left=%d right=%d jump=%d attack=%d fire=%d up=%d down=%d",
            next.count(SDLK_LEFT) != 0, next.count(SDLK_RIGHT) != 0,
            next.count(SDLK_SPACE) != 0, next.count(SDLK_LCTRL) != 0, next.count(SDLK_LALT) != 0,
            next.count(SDLK_UP) != 0, next.count(SDLK_DOWN) != 0);
    }
    pressed = next;
}

SDL_Renderer* cacheRenderer=nullptr;
SDL_Texture* buttonTextures[5][2]={};
SDL_Texture* stickTextures[3]={}; // Base, idle thumb, held thumb; about 115 KiB total.
bool targetCacheFailed=false;

void clearButtonCache() {
    for (auto& texture:stickTextures) {if(texture)SDL_DestroyTexture(texture);texture=nullptr;}
    for (auto& states : buttonTextures) for (auto& texture : states) {
        if (texture) SDL_DestroyTexture(texture);
        texture=nullptr;
    }
    cacheRenderer=nullptr;
    targetCacheFailed=false;
}

void prepareCacheRenderer(SDL_Renderer* renderer) {
    if (cacheRenderer==renderer) return;
    // SDL destroys textures together with their renderer; never reuse those handles.
    for (auto& states:buttonTextures) for (auto& texture:states) texture=nullptr;
    for (auto& texture:stickTextures) texture=nullptr;
    cacheRenderer=renderer;targetCacheFailed=!SDL_RenderTargetSupported(renderer);
}

void drawStickPart(SDL_Renderer* renderer,int cx,int cy,int state) {
    if (state==0) {
        filledCircleRGBA(renderer,cx,cy,74,12,18,28,100);
        aacircleRGBA(renderer,cx,cy,74,235,218,170,150);
        aacircleRGBA(renderer,cx,cy,48,235,218,170,55);
    } else {
        const bool held=state==2;
        filledCircleRGBA(renderer,cx,cy,26,held?140:55,held?105:61,held?35:71,195);
        aacircleRGBA(renderer,cx,cy,26,255,242,206,210);
    }
}

bool drawCachedStick(SDL_Renderer* renderer) {
    prepareCacheRenderer(renderer);
    if (targetCacheFailed || SDL_GetRenderTarget(renderer)) return false;
    const auto premultiplied=SDL_ComposeCustomBlendMode(SDL_BLENDFACTOR_ONE,
        SDL_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,SDL_BLENDOPERATION_ADD,
        SDL_BLENDFACTOR_ONE,SDL_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,SDL_BLENDOPERATION_ADD);
    for(int i=0;i<3;i++) if(!stickTextures[i]) {
        const int size=i==0?152:56;
        auto texture=SDL_CreateTexture(renderer,SDL_PIXELFORMAT_RGBA8888,SDL_TEXTUREACCESS_TARGET,size,size);
        if(!texture || SDL_SetTextureBlendMode(texture,premultiplied)<0) {
            if(texture)SDL_DestroyTexture(texture);targetCacheFailed=true;return false;
        }
        Uint8 r,g,b,a;SDL_BlendMode blend;
        SDL_GetRenderDrawColor(renderer,&r,&g,&b,&a);SDL_GetRenderDrawBlendMode(renderer,&blend);
        if(SDL_SetRenderTarget(renderer,texture)<0) {
            SDL_SetRenderTarget(renderer,nullptr);SDL_DestroyTexture(texture);targetCacheFailed=true;return false;
        }
        SDL_SetRenderDrawColor(renderer,0,0,0,0);SDL_RenderClear(renderer);
        drawStickPart(renderer,size/2,size/2,i);
        SDL_SetRenderTarget(renderer,nullptr);
        SDL_SetRenderDrawColor(renderer,r,g,b,a);SDL_SetRenderDrawBlendMode(renderer,blend);
        stickTextures[i]=texture;
    }
    const SDL_Rect base{int(stickCenterX())-76,int(stickCenterY())-76,152,152};
    const SDL_Rect thumb{int(stickCenterX()+stickX)-28,int(stickCenterY()+stickY)-28,56,56};
    SDL_RenderCopy(renderer,stickTextures[0],nullptr,&base);
    SDL_RenderCopy(renderer,stickTextures[stickHeld?2:1],nullptr,&thumb);
    return true;
}

void drawRoundButton(SDL_Renderer* renderer,const Button& button,const SDL_Rect& r,bool held) {
            const int cx=r.x+r.w/2, cy=r.y+r.h/2, radius=r.w/2;
            filledCircleRGBA(renderer,cx,cy,radius,held?140:12,held?105:18,held?35:28,held?195:105);
            aacircleRGBA(renderer,cx,cy,radius,235,218,170,195);
            aacircleRGBA(renderer,cx,cy,radius-3,235,218,170,55);
            if (button.key==SDLK_SPACE) {
                thickLineRGBA(renderer,cx,cy+9,cx,cy-22,4,255,242,206,235);
                thickLineRGBA(renderer,cx-12,cy-10,cx,cy-22,4,255,242,206,235);
                thickLineRGBA(renderer,cx+12,cy-10,cx,cy-22,4,255,242,206,235);
            } else if (button.key==SDLK_LCTRL) {
                thickLineRGBA(renderer,cx-15,cy+10,cx+15,cy-20,5,255,242,206,235);
                thickLineRGBA(renderer,cx-19,cy-2,cx-3,cy+14,4,235,218,170,235);
                thickLineRGBA(renderer,cx-21,cy+16,cx-13,cy+8,4,235,218,170,235);
            } else {
                roundedRectangleRGBA(renderer,cx-22,cy-12,cx+9,cy+3,4,255,242,206,235);
                filledTrigonRGBA(renderer,cx+10,cy-12,cx+23,cy-4,cx+10,cy+3,255,242,206,235);
                vlineRGBA(renderer,cx-15,cy-12,cy+3,235,218,170,235);
            }
            const int textWidth=SDL_strlen(label(button))*8;
            stringRGBA(renderer,cx-textWidth/2,cy+24,label(button),255,242,206,235);
}

bool drawCachedButton(SDL_Renderer* renderer,const Button& button,const SDL_Rect& r,bool held) {
    prepareCacheRenderer(renderer);
    if (targetCacheFailed || SDL_GetRenderTarget(renderer)) return false;
    const int index=&button-buttons;
    const auto premultiplied=SDL_ComposeCustomBlendMode(SDL_BLENDFACTOR_ONE,
        SDL_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,SDL_BLENDOPERATION_ADD,
        SDL_BLENDFACTOR_ONE,SDL_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,SDL_BLENDOPERATION_ADD);
    for (int state=0;state<2;++state) if (!buttonTextures[index][state]) {
        auto texture=SDL_CreateTexture(renderer,SDL_PIXELFORMAT_RGBA8888,SDL_TEXTUREACCESS_TARGET,r.w+4,r.h+4);
        if (!texture || SDL_SetTextureBlendMode(texture,premultiplied)<0) {
            if (texture) SDL_DestroyTexture(texture);
            targetCacheFailed=true;
            return false;
        }
        Uint8 red,green,blue,alpha;
        SDL_BlendMode blend;
        SDL_GetRenderDrawColor(renderer,&red,&green,&blue,&alpha);
        SDL_GetRenderDrawBlendMode(renderer,&blend);
        if (SDL_SetRenderTarget(renderer,texture)<0) {
            SDL_SetRenderTarget(renderer,nullptr);
            SDL_DestroyTexture(texture);
            targetCacheFailed=true;
            return false;
        }
        SDL_SetRenderDrawColor(renderer,0,0,0,0);
        SDL_RenderClear(renderer);
        const SDL_Rect local{2,2,r.w,r.h};
        drawRoundButton(renderer,button,local,state!=0);
        SDL_SetRenderTarget(renderer,nullptr);
        SDL_SetRenderDrawColor(renderer,red,green,blue,alpha);
        SDL_SetRenderDrawBlendMode(renderer,blend);
        buttonTextures[index][state]=texture;
    }
    const SDL_Rect destination{r.x-2,r.y-2,r.w+4,r.h+4};
    SDL_RenderCopy(renderer,buttonTextures[index][held?1:0],nullptr,&destination);
    return true;
}
}

void PazurTouch::Shutdown() {
    Reset();
    clearButtonCache();
}

void PazurTouch::Reset() {
    PazurCombatProbe::ResetKeys();
    fingers.clear();
    directionFingers.clear();
    jumpMinimumPending=false;
    stickHeld = false;
    stickX = stickY = 0;
    reconcile();
}

void PazurTouch::OpenSettings(bool difficulty) {
    Reset();
    auto env=static_cast<JNIEnv*>(SDL_AndroidGetJNIEnv());
    auto activity=static_cast<jobject>(SDL_AndroidGetActivity());
    if(!env||!activity)return;
    auto type=env->GetObjectClass(activity);
    auto method=env->GetMethodID(type,difficulty?"openDifficultySettings":"openControlSettings","()V");
    if(method)env->CallVoidMethod(activity,method);
    if(env->ExceptionCheck()){env->ExceptionDescribe();env->ExceptionClear();}
    env->DeleteLocalRef(type);env->DeleteLocalRef(activity);
}

void PazurTouch::Update() {
    static Uint32 lastPoll=0;
    const auto now=SDL_GetTicks();
    if(!lastPoll || now-lastPoll>=1000) {
        lastPoll=now;
        auto env=static_cast<JNIEnv*>(SDL_AndroidGetJNIEnv());
        auto activity=static_cast<jobject>(SDL_AndroidGetActivity());
        if(env&&activity) {
            auto type=env->GetObjectClass(activity);
            auto method=env->GetMethodID(type,"getTouchLayout","()I");
            int next=method?env->CallIntMethod(activity,method):0;
            if(env->ExceptionCheck()){env->ExceptionClear();next=0;}
            auto optionsMethod=env->GetMethodID(type,"getControlOptions","()[I");
            auto options=optionsMethod?static_cast<jintArray>(env->CallObjectMethod(activity,optionsMethod)):nullptr;
            if(env->ExceptionCheck()){env->ExceptionClear();options=nullptr;}
            if(options && env->GetArrayLength(options)==18) {
                jint values[18];env->GetIntArrayRegion(options,0,18,values);
                const int nextMovement=(std::max)(0,(std::min)(2,int(values[0])));
                const int nextDeadzone=(std::max)(8,(std::min)(28,int(values[1])));
                std::array<int,15> nextButtons;
                for(int i=0;i<15;i++)nextButtons[i]=(std::max)(i%3==0?60:-100,(std::min)(i%3==0?130:100,int(values[3+i])));
                if(nextMovement!=movement||nextDeadzone!=deadzone||nextButtons!=buttonOptions) {
                    Reset();clearButtonCache();movement=nextMovement;deadzone=nextDeadzone;buttonOptions=nextButtons;
                }
                PazurBalance::Difficulty()=(std::max)(0,(std::min)(2,int(values[2])));
            }
            if(options)env->DeleteLocalRef(options);
            env->DeleteLocalRef(type);env->DeleteLocalRef(activity);
            if(next<0||next>3)next=0;
            if(next!=controlLayout){Reset();clearButtonCache();controlLayout=next;SDL_Log("Pazur touch layout: %d",next);}
        }
    }
    if (!active()) { Reset(); return; }
    reconcile();
}

bool PazurTouch::Handle(const SDL_Event& event) {
    if (event.type==SDL_FINGERDOWN) PazurGamepad::UseTouch();
    if (event.type==SDL_RENDER_TARGETS_RESET || event.type==SDL_RENDER_DEVICE_RESET) clearButtonCache();
    if (event.type == SDL_APP_WILLENTERBACKGROUND ||
        (event.type == SDL_WINDOWEVENT && event.window.event == SDL_WINDOWEVENT_FOCUS_LOST)) {
        Reset();
    }
    if (!active()) return false;
    // Synthetic mouse clicks must not trigger a second action in the game.
    if ((event.type == SDL_MOUSEBUTTONDOWN || event.type == SDL_MOUSEBUTTONUP) &&
        event.button.which == SDL_TOUCH_MOUSEID) return true;
    if (event.type == SDL_MOUSEMOTION && event.motion.which == SDL_TOUCH_MOUSEID) return true;
    if (event.type != SDL_FINGERDOWN && event.type != SDL_FINGERMOTION && event.type != SDL_FINGERUP) return false;
    const auto& touch = event.tfinger;
    touchTimestamp=touch.timestamp;
    const float x = touch.x * width(), y = touch.y * 480.0f;
    if (event.type == SDL_FINGERUP) {
        fingers.erase(touch.fingerId);
        directionFingers.erase(touch.fingerId);
        if (stickHeld && touch.fingerId == stickFinger) {
            stickHeld = false;
            stickX = stickY = 0;
        }
    } else {
        const bool movementSide=controlLayout==3 ? x>width()-200 : x<200;
        const bool floatingStart=movement==1&&movementSide&&y>220&&hit(x,y)==SDLK_UNKNOWN;
        if(event.type==SDL_FINGERDOWN&&!stickHeld&&floatingStart){floatingX=x;floatingY=y;}
        const float dx = x-(floatingStart&&!stickHeld?floatingX:stickCenterX()), dy = y-(floatingStart&&!stickHeld?floatingY:stickCenterY());
        if (movement!=2 && event.type == SDL_FINGERDOWN && !stickHeld && (floatingStart || dx*dx+dy*dy <= 86*86)) {
            stickHeld = true;
            stickFinger = touch.fingerId;
        }
        if (stickHeld && touch.fingerId == stickFinger) {
            const float distance = std::sqrt(dx*dx+dy*dy);
            const float scale = distance > stickTravel ? stickTravel/distance : 1.0f;
            stickX = dx*scale;
            stickY = dy*scale;
            fingers.erase(touch.fingerId);
        } else if (movement==2 && (event.type==SDL_FINGERDOWN ||
                directionFingers.count(touch.fingerId))) {
            auto action=hit(x,y);
            fingers[touch.fingerId]=event.type==SDL_FINGERDOWN&&action!=SDLK_UNKNOWN?action:directionHit(x,y);
            if(event.type==SDL_FINGERDOWN&&action==SDLK_UNKNOWN&&movementSide&&y>220)directionFingers.insert(touch.fingerId);
        } else if (event.type==SDL_FINGERDOWN) {
            // The button owns its finger until release/cancel, even if the thumb drifts.
            fingers[touch.fingerId] = hit(x, y);
        }
    }
    reconcile();
    return true;
}

void PazurTouch::Draw(SDL_Renderer* renderer) {
    PazurCombatProbe::Poll();
    updateSettingsPosition(!active()||OmarEncounterComponent::IsEnding());
    OmarEncounterComponent::Draw(renderer);
    if (OmarEncounterComponent::IsEnding()) { Reset(); return; }
    if (!active()) { Reset(); return; }
    if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14) {
        boxRGBA(renderer, 140, 100, 500, 125, 90, 20, 10, 220);
        stringRGBA(renderer, 160, 109, PazurUi::Text("TRYB TESTOWY","TEST MODE"), 255, 235, 180, 255);
    }
    if (PazurGamepad::UsingController()) return;
    if(movement==2) {
        const char* labels[]={"<",">","^","v"};
        for(int i=0;i<4;i++){auto r=directionRect(i);
            roundedBoxRGBA(renderer,r.x,r.y,r.x+r.w-1,r.y+r.h-1,8,20,30,45,180);
            stringRGBA(renderer,r.x+r.w/2-4,r.y+r.h/2-4,labels[i],255,242,206,255);
        }
    } else if(!drawCachedStick(renderer)) {
        drawStickPart(renderer,stickCenterX(),stickCenterY(),0);
        drawStickPart(renderer,stickCenterX()+stickX,stickCenterY()+stickY,stickHeld?2:1);
    }
    for (const auto& button : buttons) {
        const auto r = rect(button);
        const bool held = pressed.count(button.key) != 0;
        if (button.round) {
            if (!drawCachedButton(renderer,button,r,held)) drawRoundButton(renderer,button,r,held);
            continue;
        }
        roundedBoxRGBA(renderer, r.x, r.y, r.x+r.w-1, r.y+r.h-1, 8,
            held ? 140 : 12, held ? 105 : 18, held ? 35 : 28, held ? 190 : 115);
        roundedRectangleRGBA(renderer, r.x, r.y, r.x+r.w-1, r.y+r.h-1, 8, 235, 218, 170, 170);
        const int textWidth = SDL_strlen(label(button))*8;
        stringRGBA(renderer, r.x+(r.w-textWidth)/2, r.y+(r.h-8)/2, label(button), 255, 242, 206, 235);
    }
}

// Debug fixture only: exercise shared geometry and actual finger routing, then restore.
bool PazurTouch::CheckInputOptions() {
    if(!active())return false;
    const int oldLayout=controlLayout,oldMovement=movement,oldDeadzone=deadzone;
    auto oldButtons=buttonOptions;
    Reset();bool passed=true;
    for(int i=0;i<5;i++){buttonOptions[i*3]=100;buttonOptions[i*3+1]=0;buttonOptions[i*3+2]=0;}
    auto finger=[&](Uint32 type,float x,float y) {
        SDL_Event event{};event.type=type;event.tfinger.type=type;event.tfinger.fingerId=987654;
        event.tfinger.x=x/width();event.tfinger.y=y/480;Handle(event);
    };
    for(int layout=0;layout<4;layout++) {
        controlLayout=layout;
        for(int mode=0;mode<3;mode++) {
            movement=mode;deadzone=14;
            for(const auto& button:buttons) {
                auto r=rect(button);
                passed=passed&&r.x>=0&&r.y>=0&&r.x+r.w<=width()&&r.y+r.h<=480&&hit(r.x+r.w/2,r.y+r.h/2)==button.key;
            }
            const float x=layout==3?width()-100:100;
            if(mode==2) {
                auto r=directionRect(0);finger(SDL_FINGERDOWN,r.x+r.w/2,r.y+r.h/2);
                passed=passed&&pressed.count(SDLK_LEFT);
                finger(SDL_FINGERMOTION,x,250);passed=passed&&!pressed.count(SDLK_LEFT);
                finger(SDL_FINGERMOTION,r.x+r.w/2,r.y+r.h/2);passed=passed&&pressed.count(SDLK_LEFT);
            } else {
                finger(SDL_FINGERDOWN,x,394);finger(SDL_FINGERMOTION,x+40,394);
                passed=passed&&pressed.count(SDLK_RIGHT);
            }
            finger(SDL_FINGERUP,x,394);passed=passed&&pressed.empty();Reset();
        }
    }
    // Out-of-range positions remain on-screen at supported custom sizes.
    for(int i=0;i<5;i++){buttonOptions[i*3]=130;buttonOptions[i*3+1]=100;buttonOptions[i*3+2]=100;}
    for(const auto& button:buttons){auto r=rect(button);passed=passed&&r.x>=0&&r.y>=0&&r.x+r.w<=width()&&r.y+r.h<=480;}
    Reset();controlLayout=oldLayout;movement=oldMovement;deadzone=oldDeadzone;buttonOptions=oldButtons;clearButtonCache();
    SDL_Log("Pazur input options fixture: passed=%d layouts=4 movement=3",passed);
    return passed;
}
