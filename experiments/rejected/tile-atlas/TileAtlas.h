#pragma once
#include <SDL.h>
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <string>
#include <unordered_map>
#include <vector>
#include "Engine/Graphics2D/Image.h"

// OpenAI Codex: opt-in experiment, off by default. Pack immutable tile pixels
// so SDL can batch adjacent copies without changing tile order, coordinates,
// blending, nearest filtering, physics or animation frequency. Original
// textures remain available as a fallback; atlas memory is bounded globally.
namespace PazurTiles {
inline bool& Enabled(){static bool value=false;return value;}
inline unsigned& Generation(){static unsigned value=0;return value;}
inline size_t& HeldBytes(){static size_t value=0;return value;}
inline void Reset(){++Generation();}
struct Entry {SDL_Rect source;SDL_BlendMode blend;unsigned page;};
class Atlas;
inline std::vector<Atlas*>& Registry(){static auto* value=new std::vector<Atlas*>;return *value;}

class Atlas {
    std::vector<SDL_Texture*> pages;
    SDL_Renderer* renderer=nullptr;
    std::unordered_map<SDL_Texture*,Entry> entries;
    std::string name;
    size_t bytes=0;
    unsigned generation=0;
    bool tried=false;
    std::vector<SDL_BlendMode> lastBlends;
    struct TargetScope {
        SDL_Renderer* renderer;Uint8 r,g,b,a;SDL_BlendMode blend;
        explicit TargetScope(SDL_Renderer* value):renderer(value){SDL_GetRenderDrawColor(renderer,&r,&g,&b,&a);SDL_GetRenderDrawBlendMode(renderer,&blend);}
        ~TargetScope(){SDL_SetRenderTarget(renderer,nullptr);SDL_SetRenderDrawColor(renderer,r,g,b,a);SDL_SetRenderDrawBlendMode(renderer,blend);}
    };
    bool CopyRaw(SDL_Texture* source,const SDL_Rect& target) {
        SDL_BlendMode mode;SDL_GetTextureBlendMode(source,&mode);
        if(SDL_SetTextureBlendMode(source,SDL_BLENDMODE_NONE)<0)return false;
        const bool copied=SDL_RenderCopy(renderer,source,nullptr,&target)==0;
        return SDL_SetTextureBlendMode(source,mode)==0&&copied;
    }
    bool ApplyBlend(unsigned page,SDL_BlendMode mode) {
        if(mode==lastBlends[page])return true;
        if(SDL_SetTextureBlendMode(pages[page],mode)<0)return false;
        lastBlends[page]=mode;return true;
    }
public:
    explicit Atlas(const std::string& value):name(value){Registry().push_back(this);}
    ~Atlas(){Clear();auto& list=Registry();list.erase(std::remove(list.begin(),list.end(),this),list.end());}
    void Clear() {
        for(auto texture:pages)SDL_DestroyTexture(texture);
        pages.clear();lastBlends.clear();entries.clear();HeldBytes()-=bytes;bytes=0;tried=false;
    }
    void Prepare(SDL_Renderer* target,const std::vector<Image*>& images) {
        if(generation!=Generation()){Clear();generation=Generation();}
        if(!Enabled()){if(!pages.empty())Clear();return;}
        if(tried)return;tried=true;renderer=target;
        if(SDL_GetRenderTarget(renderer)||!SDL_RenderTargetSupported(renderer))return;
        std::vector<SDL_Texture*> sources;
        int cellWidth=0,cellHeight=0;
        for(auto image:images)if(image&&image->GetTexture()) {
            auto original=image->GetTexture();if(entries.count(original))continue;
            Uint8 r,g,b,a;SDL_GetTextureColorMod(original,&r,&g,&b);SDL_GetTextureAlphaMod(original,&a);
            if(r!=255||g!=255||b!=255||a!=255)continue;
            SDL_ScaleMode scale;SDL_GetTextureScaleMode(original,&scale);if(scale!=SDL_ScaleModeNearest)continue;
            int w,h;SDL_QueryTexture(original,nullptr,nullptr,&w,&h);
            if(w<=0||h<=0||w>512||h>512||(w&(w-1))||(h&(h-1)))continue;
            Entry entry{{0,0,w,h},SDL_BLENDMODE_NONE,0};SDL_GetTextureBlendMode(original,&entry.blend);
            entries.emplace(original,entry);sources.push_back(original);
            // Only nearest-sampled sources are eligible. Align full tile cells
            // without an odd texel gutter; this preserves their sampling grid.
            cellWidth=(std::max)(cellWidth,w);cellHeight=(std::max)(cellHeight,h);
        }
        if(sources.size()<2||sources.size()>1024||cellWidth>32768||cellHeight>32768){entries.clear();return;}
        // Small power-of-two pages avoid loss of nearest-sampling precision on
        // the tested GLES2 path. Larger pages failed the pixel equality gate.
        const int width=512,height=512,columns=width/cellWidth,rows=height/cellHeight;
        const size_t slots=size_t(columns)*rows,pageCount=(sources.size()+slots-1)/slots;
        SDL_RendererInfo info{};SDL_GetRendererInfo(renderer,&info);
        const size_t needed=pageCount*width*height*4;
        if(width>info.max_texture_width||height>info.max_texture_height||needed>8*1024*1024||HeldBytes()+needed>16*1024*1024) {
            SDL_Log("Pazur tile atlas fallback: plane=%s reason=size-budget",name.c_str());entries.clear();return;
        }
        for(size_t i=0;i<pageCount;i++) {
            auto texture=SDL_CreateTexture(renderer,SDL_PIXELFORMAT_RGBA8888,SDL_TEXTUREACCESS_TARGET,width,height);
            if(!texture){Clear();tried=true;return;}
            SDL_SetTextureScaleMode(texture,SDL_ScaleModeNearest);pages.push_back(texture);lastBlends.push_back(SDL_BLENDMODE_INVALID);
        }
        bool good=true;
        {
            TargetScope restore(renderer);
            for(size_t page=0;page<pageCount&&good;page++) {
                good=SDL_SetRenderTarget(renderer,pages[page])==0;
                if(good){SDL_SetRenderDrawColor(renderer,0,0,0,0);good=SDL_RenderClear(renderer)==0;}
                for(size_t slot=0;slot<slots&&page*slots+slot<sources.size()&&good;slot++) {
                    const size_t i=page*slots+slot;auto& entry=entries.at(sources[i]);entry.page=unsigned(page);
                    entry.source.x=int(slot%columns)*cellWidth;entry.source.y=int(slot/columns)*cellHeight;
                    good=CopyRaw(sources[i],entry.source);
                }
            }
        }
        if(!good){Clear();tried=true;return;}
        bytes=needed;HeldBytes()+=bytes;
        SDL_Log("Pazur tile atlas built: plane=%s sources=%u size=%dx%d bytes=%u held=%u pages=%u",name.c_str(),unsigned(sources.size()),width,height,unsigned(bytes),unsigned(HeldBytes()),unsigned(pageCount));
    }
    bool Draw(SDL_Texture* original,const SDL_Rect& destination) {
        if(pages.empty())return false;
        const auto found=entries.find(original);if(found==entries.end()||!ApplyBlend(found->second.page,found->second.blend))return false;
        return SDL_RenderCopy(renderer,pages[found->second.page],&found->second.source,&destination)==0;
    }
    bool Ready() const {return !pages.empty();}
    bool Validate() {
        if(pages.empty())return false;
        // Compare actual GPU output for original vs atlas copies, including
        // blending and 2.25x nearest scaling. Four images per batch bound the
        // temporary readback memory; this runs only on an explicit test command.
        std::vector<std::pair<SDL_Texture*,Entry>> list(entries.begin(),entries.end());
        int cellW=0,cellH=0;
        for(const auto& value:list){cellW=(std::max)(cellW,value.second.source.w+4);cellH=(std::max)(cellH,value.second.source.h+4);}
        size_t compared=0,mismatches=0;
        for(double scale:{1.0,1.5,2.0,2.125,2.25,3.0}) {
            const size_t comparedBefore=compared,mismatchesBefore=mismatches;
            const int w=int(std::ceil(cellW*2*scale)),h=int(std::ceil(cellH*2*scale));
            if(size_t(w)*h>2*1024*1024)return false;
            auto comparison=SDL_CreateTexture(renderer,SDL_PIXELFORMAT_RGBA8888,SDL_TEXTUREACCESS_TARGET,w,h);
            if(!comparison)return false;
            std::vector<std::uint32_t> first(size_t(w)*h),second(first.size());bool good=true;
            {
                TargetScope restore(renderer);
                for(size_t offset=0;offset<list.size()&&good;offset+=4) {
                    for(int pass=0;pass<2&&good;pass++) {
                        good=SDL_SetRenderTarget(renderer,comparison)==0;
                        SDL_SetRenderDrawColor(renderer,18,31,47,255);good=good&&SDL_RenderClear(renderer)==0;
                        for(size_t i=0;i<4&&offset+i<list.size()&&good;i++) {
                            const auto& value=list[offset+i];const auto& entry=value.second;
                            SDL_Rect dest{int((int(i%2)*cellW+1)*scale),int((int(i/2)*cellH+1)*scale),int(entry.source.w*scale),int(entry.source.h*scale)};
                            good=pass==0?SDL_RenderCopy(renderer,value.first,nullptr,&dest)==0:Draw(value.first,dest);
                        }
                        auto& pixels=pass==0?first:second;
                        good=good&&SDL_RenderReadPixels(renderer,nullptr,SDL_PIXELFORMAT_RGBA8888,pixels.data(),w*4)==0;
                    }
                    if(good){compared+=first.size();for(size_t i=0;i<first.size();i++)mismatches+=first[i]!=second[i];}
                }
            }
            SDL_DestroyTexture(comparison);if(!good)return false;
            SDL_Log("Pazur tile atlas scale pixels: plane=%s scale=%.3f compared=%u mismatches=%u",name.c_str(),scale,unsigned(compared-comparedBefore),unsigned(mismatches-mismatchesBefore));
        }
        SDL_Log("Pazur tile atlas pixels: plane=%s compared=%u mismatches=%u",name.c_str(),unsigned(compared),unsigned(mismatches));
        return mismatches==0;
    }
};
inline void SetEnabled(bool value){Enabled()=value;Reset();if(!value)for(auto atlas:Registry())atlas->Clear();SDL_Log("Pazur tile atlas enabled: %d",int(value));}
inline void ValidateAll(){unsigned tested=0,passed=0;for(auto atlas:Registry())if(atlas&&atlas->Ready()){++tested;if(atlas->Validate())++passed;}SDL_Log("Pazur tile atlas validation: tested=%u passed=%u held=%u",tested,passed,unsigned(HeldBytes()));}
}
