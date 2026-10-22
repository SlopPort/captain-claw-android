#pragma once
#include "UiLanguage.h"
#include <SDL2/SDL_ttf.h>
#include <algorithm>
#include <map>
#include <memory>
#include <set>
#include <string>

// Original menu labels/help by OpenAI Codex (LLM), GPL-3.0. Text is rendered
// locally with a phone font; no commercial English artwork is bundled. Owned
// action rows use consistent centered rectangles, while level grids and volume
// rows keep their layout. Event wiring and enabled feature implementations stay
// inherited; missing destination pages must not masquerade as usable actions.
namespace PazurMenuLabels {
struct FontBatch;
inline FontBatch*& ActiveFontBatch(){static FontBatch* batch=nullptr;return batch;}
// Menu creation runs on the SDL thread. Reuse at most one face per point size
// for this initialization, then close every face before returning. Opening the
// same system font for hundreds of image states delayed cold menu transitions.
struct FontBatch {
    FontBatch* previous;
    std::map<int,TTF_Font*> fonts;
    FontBatch():previous(ActiveFontBatch()){ActiveFontBatch()=this;}
    ~FontBatch(){ActiveFontBatch()=previous;for(auto entry:fonts)if(entry.second)TTF_CloseFont(entry.second);}
    TTF_Font* Get(int size) {
        if(previous)return previous->Get(size);
        auto found=fonts.find(size);if(found!=fonts.end())return found->second;
        TTF_Font* font=nullptr;
        for(const char* file:{"/system/fonts/Roboto-Regular.ttf","/system/fonts/NotoSans-Regular.ttf","/system/fonts/DroidSans.ttf"}) {
            font=TTF_OpenFont(file,size);if(font)break;
        }
        fonts.emplace(size,font);return font;
    }
};
inline bool GridLevel(const std::string& name) {
    static const std::set<std::string> names={"LA_ROCA_BUTTON","BATTLEMENTS_BUTTON","FOOTPATH_BUTTON","DARK_WOODS_BUTTON","TOWNSHIP_BUTTON","PUERTO_LOBOS_BUTTON","DOCKS_BUTTON","SHIPYARDS_BUTTON","PIRATES_COVE_BUTTON","CLIFFS_BUTTON","CAVERNS_BUTTON","UNDERSEA_CAVES_BUTTON","TIGER_ISLAND_BUTTON","TEMPLE_BUTTON"};
    return names.count(name)!=0;
}
inline bool VolumeRow(const std::string& name) {
    return name=="SOUND_ON_BUTTON"||name=="SOUND_OFF_BUTTON"||name=="MUSIC_ON_BUTTON"||name=="MUSIC_OFF_BUTTON";
}
inline bool SharedSoundOption(const std::string& name) {
    return name.compare(0,6,"VOICE_")==0||name.compare(0,8,"AMBIENT_")==0;
}
inline int LayoutWidth(const std::string& name) {
    if(GridLevel(name))return 240;
    if(VolumeRow(name))return 280; // Leave the touch slider track clear to the right.
    if(name=="BACK_BUTTON"||name=="YES_BUTTON"||name=="NO_BUTTON")return 180;
    if(name.size()>=7&&name.compare(name.size()-7,7,"_BUTTON")==0)return 280;
    if(name.size()>=5&&name.compare(name.size()-5,5,"_TEXT")==0&&name!="SAVE_GAME_TEXT")return 400;
    return 0;
}
inline void Position(const std::string& name,Point& point) {
    const int width=LayoutWidth(name);
    if(width&&!GridLevel(name)&&!VolumeRow(name))point.SetX((640-width)/2);
}
inline std::string Label(const std::string& name,const std::string& path) {
    using Pair=std::pair<const char*,const char*>;
    static const std::map<std::string,Pair> labels={
        {"SINGLE_PLAYER_BUTTON",{"Jeden gracz","Single player"}},
        {"SINGLE_PLAYER_TEXT",{"Jeden gracz","Single player"}},
        {"MULTIPLAYER_BUTTON",{"Wielu graczy","Multiplayer"}},
        {"REPLAY_MOVIES_BUTTON",{"Filmy","Replay movies"}},
        {"OPTIONS_BUTTON",{"Opcje","Options"}}, {"OPTIONS_TEXT",{"Opcje","Options"}},
        {"CREDITS_BUTTON",{"Autorzy","Credits"}}, {"HELP_BUTTON",{"Pomoc","Help"}},
        {"QUIT_BUTTON",{"Wyjdź","Quit"}}, {"BACK_BUTTON",{"Wstecz","Back"}},
        {"NEW_GAME_BUTTON",{"Nowa gra","New game"}}, {"NEW_GAME_TEXT",{"Nowa gra","New game"}},
        {"LOAD_GAME_BUTTON",{"Wczytaj grę","Load game"}}, {"LOAD_GAME_TEXT",{"Wczytaj grę","Load game"}},
        {"LOAD_CUSTOM_LEVEL_BUTTON",{"Własny poziom","Custom level"}},
        {"SAVE_GAME_BUTTON",{"Zapisywanie","Saving"}},
        {"UPLOAD_SCORES_BUTTON",{"Wyślij wynik","Upload scores"}},
        {"SAVE_GAME_TEXT",{"Postęp jest zapisywany na punktach kontrolnych i po ukończeniu poziomu. Kopię postępu możesz wyeksportować w ustawieniach aplikacji.","Progress is saved at checkpoints and after completing a level. Export a backup from the app settings."}},
        {"YES_BUTTON",{"Tak","Yes"}}, {"NO_BUTTON",{"Nie","No"}},
        {"QUIT_GAME_TEXT",{"Czy na pewno zakończyć grę?","Are you sure you want to quit?"}},
        {"END_LIFE_TEXT",{"Czy na pewno stracić życie?","Are you sure you want to lose a life?"}},
        {"EDIT_PLAYERS_BUTTON",{"Gracze","Players"}},
        {"DIFFICULTY_BUTTON",{"Poziom trudności","Difficulty"}},
        {"CONTROLS_BUTTON",{"Sterowanie","Controls"}},
        {"AUDIO_BUTTON",{"Dźwięk","Audio"}}, {"AUDIO_TITLE_TEXT",{"Dźwięk","Audio"}},
        {"DISPLAY_BUTTON",{"Obraz","Display"}},
        {"SOUND_ON_BUTTON",{"Efekty: włączone","Sound: on"}},
        {"SOUND_OFF_BUTTON",{"Efekty: wyłączone","Sound: off"}},
        {"VOICE_ON_BUTTON",{"Głosy: opcja Efekty","Voices: Sound option"}},
        {"VOICE_OFF_BUTTON",{"Głosy: opcja Efekty","Voices: Sound option"}},
        {"AMBIENT_ON_BUTTON",{"Otoczenie: opcja Efekty","Ambient: Sound option"}},
        {"AMBIENT_OFF_BUTTON",{"Otoczenie: opcja Efekty","Ambient: Sound option"}},
        {"MUSIC_ON_BUTTON",{"Muzyka: włączona","Music: on"}},
        {"MUSIC_OFF_BUTTON",{"Muzyka: wyłączona","Music: off"}},
        {"RESUME_GAME_BUTTON",{"Wróć do gry","Resume"}},
        {"END_LIFE_BUTTON",{"Zakończ życie","Lose a life"}},
        {"END_GAME_BUTTON",{"Zakończ grę","End game"}},
        {"TOUCHSCREEN_BUTTON",{"Sterowanie dotykiem","Touch controls"}},
        {"CONTROL_IMAGE",{"STEROWANIE DOTYKIEM\nLewa gałka: ruch, góra/dół: drabiny.\nSKOK: dotknij, aby skoczyć; przytrzymaj, aby skoczyć wyżej.\nATAK: szabla. STRZAŁ: wybrana broń.\nBROŃ: zmień broń. PAUZA: menu gry.\nMożesz jednocześnie ruszać się, skakać i atakować.\nUstawienia aplikacji: język i kopie postępu.","TOUCH CONTROLS\nLeft stick: move; up/down: climb ladders.\nJUMP: tap to jump; hold to jump higher.\nATTACK: sword. SHOOT: selected weapon.\nWEAPON: change weapon. PAUSE: game menu.\nMove, jump and attack with multiple fingers.\nApp settings: language and progress backups."}},
    };
    const auto found=labels.find(name);
    if(found!=labels.end())return PazurUi::Text(found->second.first,found->second.second);
    if(name=="CREDITS_IMAGE_PETR")return path.find("credits_ja")!=std::string::npos
        ?PazurUi::Text("PROJEKTY OTWARTE\nOpenClaw: pjasicek i współtwórcy\nClaw Web: Arthur Boss i współtwórcy\n\nSDL, SDL_image, SDL_mixer\nSDL_ttf, SDL_gfx\nBox2D, libwap, TinyXML\nFreeType, FreePats, TiMidity\nSDL GameControllerDB\n\nPełne autorstwo i licencje:\nNOTICE.md i licencje w APK",
            "OPEN-SOURCE PROJECTS\nOpenClaw: pjasicek and contributors\nClaw Web: Arthur Boss and contributors\n\nSDL, SDL_image, SDL_mixer\nSDL_ttf, SDL_gfx\nBox2D, libwap, TinyXML\nFreeType, FreePats, TiMidity\nSDL GameControllerDB\n\nFull attribution and licenses:\nNOTICE.md and licenses in APK")
        :PazurUi::Text("PORT ANDROID\nKod i testy: OpenAI Codex (LLM)\nWymagania i uwagi: człowiek\n\nSilnik i port: GPL 3\nBiblioteki: własne licencje\n\nClaw: Monolith Productions\nDane gry zachowują prawa autorów\nGracz dostarcza własne dane\n\nPlansze autorstwa: Codex",
            "ANDROID PORT\nCode and tests: OpenAI Codex (LLM)\nRequirements and feedback: human\n\nEngine and port: GPL 3\nLibraries retain their licenses\n\nClaw: Monolith Productions\nGame data remains copyrighted\nPlayer supplies their own data\n\nCredit cards: Codex");
    if(name=="MAIN_MENU_TEXT")return path.find("GAMEOVER")!=std::string::npos
        ?PazurUi::Text("Koniec gry\nDotknij, aby wrócić","Game Over\nTap to return")
        :PazurUi::Text("Menu główne","Main menu");
    if(name.find("_LOAD_CHECKPOINT_1_BUTTON")!=std::string::npos)return PazurUi::Text("Punkt kontrolny 1","Checkpoint 1");
    if(name.find("_LOAD_CHECKPOINT_2_BUTTON")!=std::string::npos)return PazurUi::Text("Punkt kontrolny 2","Checkpoint 2");
    if(name.find("_START_BUTTON")!=std::string::npos)return PazurUi::Text("Początek poziomu","Level start");
    static const std::string levels[]={"LA_ROCA","BATTLEMENTS","FOOTPATH","DARK_WOODS","TOWNSHIP","PUERTO_LOBOS","DOCKS","SHIPYARDS","PIRATES_COVE","CLIFFS","CAVERNS","UNDERSEA_CAVES","TIGER_ISLAND","TEMPLE"};
    static const char* levelEnglish[]={"La Roca","Battlements","Thief's Forest","Dark Woods","Town","Puerto De Lobo","Docks","Shipyards","Pirate's Cove","Cliffs","Caverns","Undersea Caves","Tiger Island","Temple"};
    static const char* levelPolish[]={"La Roca","Bastiony","Las złodziei","Mroczny las","Miasteczko","Puerto De Lobo","Doki","Stocznia","Zatoka piratów","Klify","Jaskinie","Podwodne jaskinie","Wyspa tygrysa","Świątynia"};
    // Keep the level number visible as well as a readable name, without copying
    // translated commercial bitmap lettering into the source distribution.
    for(int i=0;i<14;++i)if(name==levels[i]+"_BUTTON"||name=="LOAD_LEVEL"+std::to_string(i+1)+"_TEXT")
        return std::to_string(i+1)+". "+PazurUi::Text(levelPolish[i],levelEnglish[i]);
    return ""; // Nonlinguistic slider artwork remains unchanged.
}

inline std::shared_ptr<Image> Translate(const std::string& name,const std::string& path,
        std::shared_ptr<Image> original,SDL_Renderer* renderer,bool active,bool disabled,bool* changed=nullptr) {
    const auto label=Label(name,path);
    if(label.empty()||!original)return original;
    int width=original->GetWidth(),height=original->GetHeight();
    if(LayoutWidth(name))width=LayoutWidth(name);
    if(GridLevel(name))height=26;
    if(name=="CONTROL_IMAGE"){width=620;height=265;}
    if(name=="TOUCHSCREEN_BUTTON")height=26;
    if(name=="SAVE_GAME_TEXT"){width=552;height=145;}
    if(name=="MAIN_MENU_TEXT"&&path.find("GAMEOVER")!=std::string::npos)height=80;
    if(width<4||height<4)return original;
    int fontSize=(std::max)(10,(std::min)(24,height-4));
    FontBatch batch;
    TTF_Font* font=batch.Get(fontSize);
    // A missing system font leaves the user's original art usable. No null
    // texture replaces a valid menu item on an unusual Android installation.
    if(!font){SDL_Log("Pazur menu label fallback: %s (system font unavailable)",name.c_str());return original;}
    SDL_Color color=disabled&&name!="CONTROL_IMAGE"?SDL_Color{145,150,160,255}:
        active?SDL_Color{255,221,125,255}:SDL_Color{235,238,246,255};
    SDL_Surface* text=TTF_RenderUTF8_Blended_Wrapped(font,label.c_str(),color,(std::max)(1,width-8));
    // Reflow long translated words at the smaller font size instead of merely
    // shrinking an already wrapped two-line image into a single-line button.
    if(text&&text->h>height-4&&fontSize>8) {
        int low=8,high=fontSize-1,best=8;
        const auto resize=[&](int size) {
            font=batch.Get(size);if(!font)return false;
            SDL_FreeSurface(text);fontSize=size;
            text=TTF_RenderUTF8_Blended_Wrapped(font,label.c_str(),color,(std::max)(1,width-8));
            return text!=nullptr;
        };
        bool valid=true;
        while(low<=high&&valid) {
            int candidate=(low+high)/2;valid=resize(candidate);
            if(valid&&text->h<=height-4){best=candidate;low=candidate+1;}else high=candidate-1;
        }
        if(valid&&fontSize!=best)valid=resize(best);
        if(!valid){if(text)SDL_FreeSurface(text);return original;}
    }
    if(!text)return original;
    SDL_Surface* canvas=SDL_CreateRGBSurfaceWithFormat(0,width,height,32,SDL_PIXELFORMAT_RGBA32);
    if(!canvas){SDL_FreeSurface(text);return original;}
    SDL_FillRect(canvas,nullptr,SDL_MapRGBA(canvas->format,16,23,34,225));
    const double scale=(std::min)({1.0,double(width-8)/text->w,double(height-4)/text->h});
    SDL_Rect destination{VolumeRow(name)?4:(width-int(text->w*scale))/2,(height-int(text->h*scale))/2,
        (std::max)(1,int(text->w*scale)),(std::max)(1,int(text->h*scale))};
    SDL_BlitScaled(text,nullptr,canvas,&destination);SDL_FreeSurface(text);
    SDL_Texture* texture=SDL_CreateTextureFromSurface(renderer,canvas);SDL_FreeSurface(canvas);
    if(!texture)return original;
    SDL_SetTextureBlendMode(texture,SDL_BLENDMODE_BLEND);
    auto translated=std::make_shared<Image>(texture);
    if(changed)*changed=true;
    translated->SetOffset(0,0); // Owned text uses the same absolute rectangle as touch hit testing.
    if(g_pApp->GetDebugOptions()->bPreviewIncompleteLevel14)
        SDL_Log("Pazur menu label: language=%s item=%s box=%dx%d text=%dx%d",PazurUi::English()?"en":"pl",name.c_str(),width,height,destination.w,destination.h);
    return translated;
}
}
