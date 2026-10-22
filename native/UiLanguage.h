#pragma once
#include <fstream>
#include <string>

// ASCII labels for SDL_gfx's built-in font. Chosen once per engine process;
// Android writes this preference atomically before creating SDLActivity.
// OpenAI Codex (LLM); original menu art and recordings remain user-owned data.
namespace PazurUi {
inline bool English() {
    static const bool english=[]() {
        std::ifstream input("ui-language.txt");std::string code;input>>code;
        return code=="en";
    }();
    return english;
}
inline const char* Text(const char* polish,const char* english) {
    return English()?english:polish;
}
}
