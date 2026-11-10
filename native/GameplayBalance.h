#pragma once
#include <cstdint>
// LLM-authored adaptation. Only damage taken and healing pickups vary by difficulty.
namespace PazurBalance {
inline int& Difficulty() { static int value=1; return value; }
constexpr int Damage(int amount,int difficulty) {
    return amount<=0 ? amount : difficulty==0 ? (amount+1)/2 :
        difficulty==2 ? int((int64_t(amount)*3+1)/2) : amount;
}
constexpr int Healing(int amount,int difficulty) {
    return amount<=0 ? amount : difficulty==0 ? int((int64_t(amount)*3+1)/2) :
        difficulty==2 ? (amount+1)/2 : amount;
}
static_assert(Damage(10,0)==5 && Damage(10,1)==10 && Damage(10,2)==15,"damage presets");
static_assert(Healing(10,0)==15 && Healing(10,1)==10 && Healing(10,2)==5,"healing presets");
static_assert(Damage(1,0)==1 && Healing(1,2)==1,"nonzero effects");
}
