#pragma once
#include <cstdio>
#include <string>
#include "tinyxml.h"
#ifdef _WIN32
#include <io.h>
#include <windows.h>
#else
#include <unistd.h>
#endif

// OpenAI Codex (LLM). Write/sync/close a sibling before replacing the live XML.
// Never delete the old target to make replacement succeed. A failed write or
// process death before publication leaves the old save readable. Directory
// metadata durability across sudden power loss is filesystem-dependent.
namespace PazurXml {
enum class Boundary { Written, Flushed, Synced, BeforePublish };
using Checkpoint=bool (*)(Boundary);
inline bool Save(const TiXmlDocument& document,const std::string& target,Checkpoint checkpoint=nullptr) {
    const std::string temporary=target+".tmp";
    FILE* file=std::fopen(temporary.c_str(),"wb");
    if(!file)return false;
    bool good=document.SaveFile(file) && !std::ferror(file);
    if(good&&checkpoint)good=checkpoint(Boundary::Written);
    if(good)good=std::fflush(file)==0;
    if(good&&checkpoint)good=checkpoint(Boundary::Flushed);
#ifdef _WIN32
    if(good)good=::_commit(::_fileno(file))==0;
#else
    if(good)good=::fsync(::fileno(file))==0;
#endif
    if(std::fclose(file)!=0)good=false;
    if(good&&checkpoint)good=checkpoint(Boundary::Synced);
    if(good&&checkpoint)good=checkpoint(Boundary::BeforePublish);
    if(!good)return false;
#ifdef _WIN32
    // Desktop boundary tests exercise the same helper. Production use is
    // Android/POSIX; replacement never falls back to unlinking the old file.
    return MoveFileExA(temporary.c_str(),target.c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH)!=0;
#else
    return std::rename(temporary.c_str(),target.c_str())==0;
#endif
}
}
