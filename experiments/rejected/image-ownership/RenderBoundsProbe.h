#pragma once
// OpenAI Codex: temporary same-APK experiment. Off by default, changed only by
// the opt-in diagnostic mailbox on the SDL thread. No geometry/result caching.
namespace PazurRenderBounds {
inline bool& Borrow(){static bool enabled=false;return enabled;}
}
