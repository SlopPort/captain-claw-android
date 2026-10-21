#pragma once
#include <string>

// Opt-in test diagnostics only. Counts mixed nonzero samples, never records
// microphone input or stores game audio. Written by OpenAI Codex.
namespace PazurAudioProbe {
    void Enable(bool enabled);
    void Begin(const std::string& label);
    void Report();
    void Sound(const std::string& path,bool played);
    void Mixed(unsigned char* stream,int bytes);
}
