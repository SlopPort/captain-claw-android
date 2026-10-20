#include <libwap.h>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <string>

int main(int argc, char** argv) {
    if (argc != 3) return 2;
    auto archive = WAP_LoadRezArchive(argv[1]);
    if (!archive) return 3;
    std::ifstream requests(argv[2]);
    std::string path;
    while (std::getline(requests, path)) {
        if (!path.empty() && path.back() == '\r') path.pop_back();
        auto ani = WAP_AniLoadFromRezArchive(archive, path.c_str());
        if (!ani) { std::printf("MISSING|%s\n", path.c_str()); continue; }
        std::printf("ANI|%s|%u", path.c_str(), ani->animationFramesCount);
        for (unsigned i=0; i<ani->animationFramesCount; ++i) {
            const auto& frame = ani->animationFrames[i];
            std::printf("|%u,%u,%u", frame.imageFileId, frame.duration, frame.triggeredEventFlag);
        }
        std::printf("\n");
        WAP_AniDestroy(ani);
    }
    for (int level=1; level<=14; ++level) {
        char file[80];
        std::snprintf(file,sizeof(file),"/LEVEL%d/WORLDS/WORLD.WWD",level);
        auto world = WAP_WwdLoadFromRezArchive(archive,file);
        if (!world) return 4;
        for (unsigned p=0; p<world->planesCount; ++p) for (unsigned i=0; i<world->planes[p].objectsCount; ++i) {
            const auto& o=world->planes[p].objects[i];
            // Preserve the complete logic inventory, including unknown or unsupported enemy names.
            std::printf("OBJ|%d|%s|%s|%d|%d|%d|%d|%d,%d,%d,%d|%d,%d,%d,%d\n",level,o.logic,o.imageSet,o.x,o.y,o.health,o.damage,
                o.hitRect.left,o.hitRect.top,o.hitRect.right,o.hitRect.bottom,
                o.attackRect.left,o.attackRect.top,o.attackRect.right,o.attackRect.bottom);
        }
        WAP_WwdDestroy(world);
    }
    WAP_DestroyRezArchive(archive);
}
