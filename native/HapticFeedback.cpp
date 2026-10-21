#include "HapticFeedback.h"
#include "GamepadControls.h"
#include <SDL.h>
#include <jni.h>
#include <fstream>

// Inspired by Claw Web's HapticFeedback.Trigger and named event presets.
// This backend uses SDL rumble or the current Android activity, never web APIs.
void PazurHaptics::Trigger(Preset preset) {
    static Uint32 poll=0,last=0;static bool enabled=false;
    const auto now=SDL_GetTicks();
    if(!poll || now-poll>1000) {poll=now;enabled=std::ifstream("haptics-enabled").good();}
    if(!enabled || (last && now-last<45))return;
    last=now;
    const int duration=preset==Explosion?120:preset==Damage?80:preset==Landing?45:25;
    if(PazurGamepad::UsingController()) {
        PazurGamepad::Rumble(duration);return;
    }
    auto env=static_cast<JNIEnv*>(SDL_AndroidGetJNIEnv());
    auto activity=static_cast<jobject>(SDL_AndroidGetActivity());
    if(!env||!activity)return;
    auto type=env->GetObjectClass(activity);
    auto method=env->GetMethodID(type,"pulseHaptic","(I)V");
    if(method)env->CallVoidMethod(activity,method,duration);
    if(env->ExceptionCheck()) {env->ExceptionDescribe();env->ExceptionClear();}
    env->DeleteLocalRef(type);env->DeleteLocalRef(activity);
}
