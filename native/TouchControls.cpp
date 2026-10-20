#include "TouchControls.h"
#include "CombatProbe.h"
#include "GamepadControls.h"
#include "PlatformInput.h"
#include "OmarEncounterComponent.h"
#include <SDL2/SDL2_gfxPrimitives.h>
#include <map>
#include <set>
#include <cmath>
#include "Engine/GameApp/BaseGameApp.h"
#include "Engine/GameApp/BaseGameLogic.h"

namespace {
struct Button { SDL_Rect rect; SDL_Keycode key; const char* label; bool round; };
const Button buttons[] = {
    {{506, 346, 120, 120}, SDLK_SPACE, "SKOK", true},
    {{378, 358, 104, 104}, SDLK_LCTRL, "ATAK", true},
    {{447, 228, 96, 96}, SDLK_LALT, "STRZAL", true},
    {{562, 110, 62, 34}, SDLK_LSHIFT, "BRON", false},
    {{16, 80, 66, 34}, SDLK_ESCAPE, "PAUZA", false},
};
std::map<SDL_FingerID, SDL_Keycode> fingers;
std::set<SDL_Keycode> pressed;
bool stickHeld = false;
SDL_FingerID stickFinger = 0;
float stickX = 0, stickY = 0;
const float stickCenterX = 100, stickCenterY = 394, stickTravel = 48;
Uint32 touchTimestamp=0;
Uint32 jumpPressedAt=0;
bool jumpMinimumPending=false;
// Touch taps should produce a useful low jump; holding still controls the full height.
constexpr Uint32 minimumJumpPressMs=110;

int width() { return static_cast<int>(g_pApp->GetWindowSizeScaled().x); }
SDL_Rect rect(const Button& button) {
    auto r = button.rect;
    if (button.key != SDLK_ESCAPE) r.x += width() - 640;
    return r;
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
    if (stickHeld && magnitude >= 14) {
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
bool targetCacheFailed=false;

void clearButtonCache() {
    for (auto& states : buttonTextures) for (auto& texture : states) {
        if (texture) SDL_DestroyTexture(texture);
        texture=nullptr;
    }
    cacheRenderer=nullptr;
    targetCacheFailed=false;
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
            const int textWidth=SDL_strlen(button.label)*8;
            stringRGBA(renderer,cx-textWidth/2,cy+24,button.label,255,242,206,235);
}

bool drawCachedButton(SDL_Renderer* renderer,const Button& button,const SDL_Rect& r,bool held) {
    if (cacheRenderer!=renderer) {
        // SDL owns textures when their renderer is destroyed.
        for (auto& states : buttonTextures) for (auto& texture : states) texture=nullptr;
        cacheRenderer=renderer;
        targetCacheFailed=!SDL_RenderTargetSupported(renderer);
    }
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

void PazurTouch::Reset() {
    PazurCombatProbe::ResetKeys();
    fingers.clear();
    jumpMinimumPending=false;
    stickHeld = false;
    stickX = stickY = 0;
    reconcile();
}

void PazurTouch::Update() {
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
        if (stickHeld && touch.fingerId == stickFinger) {
            stickHeld = false;
            stickX = stickY = 0;
        }
    } else {
        const float dx = x-stickCenterX, dy = y-stickCenterY;
        if (event.type == SDL_FINGERDOWN && !stickHeld && dx*dx+dy*dy <= 86*86) {
            stickHeld = true;
            stickFinger = touch.fingerId;
        }
        if (stickHeld && touch.fingerId == stickFinger) {
            const float distance = std::sqrt(dx*dx+dy*dy);
            const float scale = distance > stickTravel ? stickTravel/distance : 1.0f;
            stickX = dx*scale;
            stickY = dy*scale;
            fingers.erase(touch.fingerId);
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
    OmarEncounterComponent::Draw(renderer);
    if (OmarEncounterComponent::IsEnding()) { Reset(); return; }
    if (!active()) { Reset(); return; }
    if (g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14) {
        boxRGBA(renderer, 140, 100, 500, 125, 90, 20, 10, 220);
        stringRGBA(renderer, 160, 109, "TRYB TESTOWY - POZIOM 14", 255, 235, 180, 255);
    }
    if (PazurGamepad::UsingController()) return;
    filledCircleRGBA(renderer, stickCenterX, stickCenterY, 74, 12, 18, 28, 100);
    aacircleRGBA(renderer, stickCenterX, stickCenterY, 74, 235, 218, 170, 150);
    aacircleRGBA(renderer, stickCenterX, stickCenterY, 48, 235, 218, 170, 55);
    filledCircleRGBA(renderer, stickCenterX+stickX, stickCenterY+stickY, 26,
        stickHeld ? 140 : 55, stickHeld ? 105 : 61, stickHeld ? 35 : 71, 195);
    aacircleRGBA(renderer, stickCenterX+stickX, stickCenterY+stickY, 26, 255, 242, 206, 210);
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
        const int textWidth = SDL_strlen(button.label)*8;
        stringRGBA(renderer, r.x+(r.w-textWidth)/2, r.y+(r.h-8)/2, button.label, 255, 242, 206, 235);
    }
}
