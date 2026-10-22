// Read-only route inventory using upstream libwap. Written by OpenAI Codex (LLM).
// Build against the locked libwap sources with -iquote, not -I: on Windows,
// libwap/IO.h otherwise shadows the toolchain's unrelated system <io.h>.
// Supply a locally owned WORLD.WWD. Never redistribute the resulting map dump.
#include "libwap.h"
#include <cstdio>

int main(int argc, char** argv)
{
    if (argc != 2) return 2;
    auto world = WAP_WwdLoadFromFile(argv[1]);
    if (!world) return 3;
    std::printf("START %d %d\n", world->properties.startX, world->properties.startY);
    for (unsigned p = 0; p < world->planesCount; ++p) {
        const auto& plane = world->planes[p];
        if (!(plane.properties.flags & WAP_PLANE_FLAG_MAIN_PLANE)) continue;
        for (unsigned n = 0; n < plane.objectsCount; ++n) {
            const auto& object = plane.objects[n];
            std::printf("OBJ %d %d %d %s %s speed=%d,%d range=%d,%d,%d,%d\n",
                object.id, object.x, object.y, object.logic, object.imageSet,
                object.speedX, object.speedY, object.minX, object.minY,
                object.maxX, object.maxY);
        }
        const auto width = plane.properties.tilesOnAxisX;
        const auto height = plane.properties.tilesOnAxisY;
        std::printf("GRID %u %u\n", width, height);
        for (unsigned y = 0; y < height; ++y) {
            for (unsigned x = 0; x < width; ++x)
                std::printf("%d ", plane.tiles[y * width + x]);
            std::puts("");
        }
    }
    for (unsigned n = 0; n < world->tileDescriptionsCount; ++n) {
        const auto& tile = world->tileDescriptions[n];
        std::printf("TILE %u %u %u %u %u %u %d %d %d %d\n", n, tile.type,
            tile.width, tile.height, tile.insideAttrib, tile.outsideAttrib,
            tile.rect.left, tile.rect.top, tile.rect.right, tile.rect.bottom);
    }
    WAP_WwdDestroy(world);
    return 0;
}
