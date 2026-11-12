// OpenAI Codex (LLM): synthetic data, no original game assets or decompiled code.
// tile_source.inc contains the current OpenClaw routine extracted at audit time;
// its upstream GPL authorship remains separate from this comparison harness.
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

struct SDL_Rect { int x, y, w, h; };
enum CollisionType { CollisionType_None=0, CollisionType_Solid=1,
    CollisionType_Ground=2, CollisionType_Climb=3, CollisionType_Death=4 };
enum { WAP_TILE_TYPE_SINGLE=1, WAP_TILE_TYPE_DOUBLE=2, WAP_TILE_ATTRIBUTE_CLEAR=0 };
struct TileRect { int left, top, right, bottom; };
struct TileDescription { int tileId, type, width, height, insideAttrib, outsideAttrib; TileRect rect; };
struct TileCollisionRectangle { CollisionType collisionType; SDL_Rect collisionRect; };
struct TileCollisionPrototype { int id; unsigned width, height; std::vector<TileCollisionRectangle> collisionRectangles; };
#define LOG_ERROR(value) ((void)0)
void PrintRect(SDL_Rect, const std::string&) {}
#include "tile_source.inc"

// Independent predicate from REA's inclusive double-tile comparisons. This
// checks integer pixel cells, not Box2D skin/contact behavior or a played route.
int reference(const TileDescription& desc, int x, int y) {
    if(desc.type==WAP_TILE_TYPE_SINGLE) return desc.insideAttrib;
    return desc.rect.left<=x && x<=desc.rect.right &&
        desc.rect.top<=y && y<=desc.rect.bottom ? desc.insideAttrib : desc.outsideAttrib;
}

int main() {
    struct Case { const char* name; int type; TileRect rect; };
    const Case cases[] = {
        {"single",1,{0,0,63,63}}, {"top-half",2,{0,0,63,31}},
        {"right-half",2,{32,0,63,63}}, {"bottom-half",2,{0,32,63,63}},
        {"left-half",2,{0,0,31,63}}, {"middle-band",2,{0,16,63,47}},
        {"middle-stripe",2,{16,0,47,63}}
    };
    bool equal=true;
    std::cout << "{\"cases\":[";
    for(unsigned i=0;i<sizeof(cases)/sizeof(cases[0]);++i) {
        TileDescription desc{1,cases[i].type,64,64,1,0,cases[i].rect};
        TileCollisionPrototype output{};
        ParseCollisionRectanglesFromTile(&output,&desc);
        int mismatches=0, outOfTile=0, firstX=-1, firstY=-1;
        for(const auto& piece:output.collisionRectangles) {
            const auto& r=piece.collisionRect;
            if(r.x<0 || r.y<0 || r.x+r.w>64 || r.y+r.h>64) ++outOfTile;
        }
        for(int y=0;y<64;++y) for(int x=0;x<64;++x) {
            // A solid fixture covers the pixel cell's center using its exact
            // emitted origin/size. Clear pieces create no solid geometry.
            bool portSolid=false;
            for(const auto& piece:output.collisionRectangles) {
                const auto& r=piece.collisionRect;
                if(piece.collisionType==CollisionType_Solid && r.x<=x+.5 && x+.5<r.x+r.w &&
                    r.y<=y+.5 && y+.5<r.y+r.h) portSolid=true;
            }
            if(portSolid!=(reference(desc,x,y)==1)) {
                ++mismatches;
                if(firstX<0) { firstX=x; firstY=y; }
            }
        }
        if(mismatches || outOfTile) equal=false;
        if(i) std::cout << ',';
        std::cout << "{\"name\":\"" << cases[i].name << "\",\"mismatched_cells\":" << mismatches
            << ",\"out_of_tile_pieces\":" << outOfTile << ",\"first_mismatch\":[" << firstX << ',' << firstY << "]}";
    }
    std::cout << "],\"equivalent_for_selected_cases\":" << (equal?"true":"false") << "}\n";
    return equal?0:1;
}
