#include "ComponentProfiler.h"
#include <map>
#include <string>
#include <vector>
#include <algorithm>
namespace PazurProfile {
bool components=false;
static Uint32 end=0;
static std::map<std::string,Uint64> totals;
void Start(){totals.clear();components=true;end=SDL_GetTicks()+5000;}
void Record(const char* name,Uint64 ticks){totals[name]+=ticks;}
void Poll(){
    if(!components || (Sint32)(SDL_GetTicks()-end)<0)return;
    components=false;
    std::vector<std::pair<std::string,Uint64>> rows(totals.begin(),totals.end());
    std::sort(rows.begin(),rows.end(),[](const std::pair<std::string,Uint64>& a,const std::pair<std::string,Uint64>& b){return a.second>b.second;});
    for(size_t i=0;i<rows.size()&&i<10;++i)
        SDL_Log("Pazur component sample: %s total=%.2f ms / 5 seconds (instrumented)",rows[i].first.c_str(),rows[i].second*1000.0/SDL_GetPerformanceFrequency());
}
}
