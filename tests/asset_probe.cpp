#include <libwap.h>
#include <cstdio>
#include <cstring>
#include <map>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    RezArchive* archive = WAP_LoadRezArchive(argv[1]);
    if (!archive) return 3;
    for (int level = 1; level <= 14; ++level) {
        char path[80];
        std::snprintf(path, sizeof(path), "/LEVEL%d/WORLDS/WORLD.WWD", level);
        WapWwd* world = WAP_WwdLoadFromRezArchive(archive, path);
        if (!world || !world->planesCount) return 4;
        unsigned objects = 0;
        std::map<std::string, unsigned> logics;
        if (level == 14) std::printf("L14 spawn: %d,%d\n", world->properties.startX, world->properties.startY);
        for (unsigned p = 0; p < world->planesCount; ++p) {
            auto& plane = world->planes[p];
            objects += plane.objectsCount;
            if (level == 14 && (plane.properties.flags & WAP_PLANE_FLAG_MAIN_PLANE)) {
                for (int row = 28; row <= 43; ++row) {
                    std::printf("L14 arena terrain y=%d:", row * 64);
                    for (int col = 650; col <= 682; ++col) {
                        int id = plane.tiles[row * plane.properties.tilesOnAxisX + col];
                        char mark = '.';
                        if (id >= 0 && (unsigned)id < world->tileDescriptionsCount) {
                            const auto& t = world->tileDescriptions[id];
                            mark = t.type == WAP_TILE_TYPE_DOUBLE ? '?' : t.insideAttrib == WAP_TILE_ATTRIBUTE_SOLID ? '#' : t.insideAttrib == WAP_TILE_ATTRIBUTE_GROUND ? '=' : t.insideAttrib == WAP_TILE_ATTRIBUTE_DEATH ? '!' : '.';
                        }
                        std::printf(" %c", mark);
                    }
                    std::printf("\n");
                }
            }
            if (level == 14 && (plane.properties.flags & WAP_PLANE_FLAG_MAIN_PLANE)) {
                for (int row : {30,31,32,37,38,39,40,41,42}) for (int col=658;col<=663;++col) {
                    int id=plane.tiles[row*plane.properties.tilesOnAxisX+col];
                    if(id>=0 && (unsigned)id<world->tileDescriptionsCount) {
                        const auto& t=world->tileDescriptions[id];
                        std::printf("L14 tile: x=%d y=%d id=%d type=%u in=%u out=%u rect=%d,%d,%d,%d\n",col*64,row*64,id,t.type,t.insideAttrib,t.outsideAttrib,t.rect.left,t.rect.top,t.rect.right,t.rect.bottom);
                    }
                }
            }
            if (level == 14) for (unsigned i = 0; i < plane.objectsCount; ++i) {
                const auto& object = plane.objects[i];
                ++logics[object.logic];
                if (std::strncmp(object.logic, "Lava", 4) == 0)
                    std::printf("L14 lava: logic=%s images=%s x=%d y=%d speed=%d sx=%d sy=%d damage=%d flags=%u\n", object.logic, object.imageSet, object.x, object.y, object.speed, object.speedX, object.speedY, object.damage, object.drawFlags);
                if (std::strcmp(object.logic, "TigerGuard") == 0 || std::strcmp(object.logic, "Chameleon") == 0)
                    std::printf("L14 enemy: logic=%s images=%s x=%d y=%d patrol=%d,%d health=%d damage=%d\n", object.logic, object.imageSet, object.x, object.y, object.minX, object.maxX, object.health, object.damage);
                if (std::strcmp(object.logic, "TProjectile") == 0)
                    std::printf("L14 shooter: images=%s x=%d y=%d area=%d,%d,%d,%d speed=%d damage=%d\n", object.imageSet, object.x, object.y, object.minX, object.minY, object.maxX, object.maxY, object.speed, object.damage);
                if ((std::strcmp(object.logic, "CrumblingPeg") == 0 || std::strcmp(object.logic, "TogglePeg") == 0 || std::strcmp(object.logic, "FloorSpike") == 0) && logics[object.logic] == 1)
                    std::printf("L14 fixture: logic=%s images=%s x=%d y=%d\n", object.logic, object.imageSet, object.x, object.y);
                if (std::strstr(object.logic, "Checkpoint") || std::strstr(object.logic, "Omar") || std::strstr(object.imageSet, "FIRESWORD") || std::strcmp(object.logic, "BossStager") == 0 || object.x > 39000 && (std::strstr(object.logic, "Powerup") || std::strstr(object.logic, "DoNothing")))
                    std::printf("L14 object: logic=%s images=%s x=%d y=%d\n", object.logic, object.imageSet, object.x, object.y);
            }
            if (level == 1) for (unsigned i = 0; i < plane.objectsCount; ++i) {
                const auto& object = plane.objects[i];
                if (std::strstr(object.imageSet, "CANDELABRA") || std::strstr(object.logic, "SuperCheckpoint"))
                    std::printf("L1 decoration: logic=%s images=%s frame=%d x=%d y=%d\n",
                        object.logic, object.imageSet, object.i, object.x, object.y);
            }
        }
        std::printf("PASS decode level %d: planes=%u objects=%u\n", level, world->planesCount, objects);
        for (const auto& entry : logics) std::printf("L14 logic: %s count=%u\n", entry.first.c_str(), entry.second);
        WAP_WwdDestroy(world);
    }
    for (const char* name : {"LAUNCHLEFT", "LAUNCHRIGHT"}) {
        char path[100];
        std::snprintf(path, sizeof(path), "/LEVEL14/ANIS/SHOOTERS/%s.ANI", name);
        WapAni* ani = WAP_AniLoadFromRezArchive(archive, path);
        if (!ani) return 5;
        std::printf("L14 animation: %s images=%s frames=%u\n", name, ani->imageSetPath, ani->animationFramesCount);
        for (unsigned i = 0; i < ani->animationFramesCount; ++i) {
            const auto& f = ani->animationFrames[i];
            std::printf("  frame=%u image=%u ms=%u event=%u sound=%s\n", i, f.imageFileId, f.duration, f.triggeredEventFlag, f.eventFilePath ? f.eventFilePath : "");
        }
        WAP_AniDestroy(ani);
    }
    for (const char* name : {"TIGER/STRIKE1", "TIGER/STRIKE2", "TIGER/STRIKE3", "TIGERWHITE/STRIKE1", "CHAMELEON/STRIKE1"}) {
        char path[100];
        std::snprintf(path, sizeof(path), "/LEVEL14/ANIS/%s.ANI", name);
        WapAni* ani = WAP_AniLoadFromRezArchive(archive, path);
        if (!ani) return 6;
        std::printf("L14 enemy animation: %s frames=%u\n", name, ani->animationFramesCount);
        for (unsigned i = 0; i < ani->animationFramesCount; ++i) {
            const auto& f = ani->animationFrames[i];
            std::printf("  frame=%u image=%u ms=%u sound=%s\n", i, f.imageFileId, f.duration, f.eventFilePath ? f.eventFilePath : "");
        }
        WAP_AniDestroy(ani);
    }
    for (const char* name : {"LAVAGEYSER", "LAVAHAND", "LAVAHANDPROJECTILE"}) {
        char path[100];
        std::snprintf(path, sizeof(path), "/LEVEL14/ANIS/%s.ANI", name);
        WapAni* ani = WAP_AniLoadFromRezArchive(archive, path);
        if (!ani) return 7;
        std::printf("L14 lava animation: %s frames=%u\n", name, ani->animationFramesCount);
        for (unsigned i = 0; i < ani->animationFramesCount; ++i) {
            const auto& f = ani->animationFrames[i];
            std::printf("  frame=%u image=%u ms=%u sound=%s\n", i, f.imageFileId, f.duration, f.eventFilePath ? f.eventFilePath : "");
        }
        WAP_AniDestroy(ani);
    }
    WAP_DestroyRezArchive(archive);
    return 0;
}
