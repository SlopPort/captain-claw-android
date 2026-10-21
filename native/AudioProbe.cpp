#include "AudioProbe.h"
#include <SDL.h>
#include <SDL_mixer.h>
#include <atomic>
#include <algorithm>
#include <cstdlib>

namespace {
std::atomic<bool> enabled{false};
std::string label;
std::atomic<unsigned> buffers{0},audible{0},samples{0},peak{0};
void mixed(void*,Uint8* stream,int length) {
    const auto pcm=reinterpret_cast<const Sint16*>(stream);
    unsigned count=0,maximum=0;
    for(int i=0;i<length/2;++i) {
        const auto value=unsigned(std::abs(int(pcm[i])));
        if(value)++count;
        maximum=std::max(maximum,value);
    }
    buffers.fetch_add(1,std::memory_order_relaxed);
    samples.fetch_add(count,std::memory_order_relaxed);
    if(count)audible.fetch_add(1,std::memory_order_relaxed);
    auto previous=peak.load(std::memory_order_relaxed);
    while(maximum>previous && !peak.compare_exchange_weak(previous,maximum,std::memory_order_relaxed)) { }
}
}
void PazurAudioProbe::Enable(bool value) {
    int frequency,channels;Uint16 format;
    enabled=value && Mix_QuerySpec(&frequency,&format,&channels) && format==AUDIO_S16SYS;
    SDL_Log("Pazur audio trace: enabled=%d",int(enabled.load()));
}
void PazurAudioProbe::Mixed(unsigned char* stream,int bytes) {
    if(enabled.load(std::memory_order_relaxed))mixed(nullptr,stream,bytes);
}
void PazurAudioProbe::Begin(const std::string& value) {
    label=value;buffers=0;audible=0;samples=0;peak=0;
    SDL_Log("Pazur audio measurement: label=%s",label.c_str());
}
void PazurAudioProbe::Report() {
    SDL_Log("Pazur audio mix: label=%s buffers=%u audible=%u nonzero=%u peak=%u",
        label.c_str(),buffers.load(),audible.load(),samples.load(),peak.load());
}
void PazurAudioProbe::Sound(const std::string& path,bool played) {
    if(enabled)SDL_Log("Pazur audio sound: label=%s accepted=%d path=%s",label.c_str(),played,path.c_str());
}
