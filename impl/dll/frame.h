// THE PER-FRAME SEAM (map renderer capture + console while paused).
//
// Two problems share one cause: everything we drive runs off the MONTHLY tick.
//
//  * The arrow layer. BuildTradeRouteLayer(mapRenderer) at 0x10AFA70 is called once at map init,
//    before we inject, so the capture detour there never fired and arrows::rebuild() had no
//    renderer to call -- the node window's tabs reoriented every month while the drawn ribbons
//    never moved.
//  * The console. console::drain() ran from the tick hook, so a PAUSED game could not be told
//    anything -- including "unpause". An event popup pauses EU4 and the whole harness stalls.
//
// The map update at 0x10A6EC0 fixes both. It takes the map renderer as its first argument:
//
//   010A6EC0  mov  [rsp+0x18], r8          <- hook site (20 bytes stolen, through sub rsp)
//   010A6ED4  mov  rdx, [rip -> 0233FE78]  ; the game singleton
//   010A6EDB  mov  rdi, rcx                ; rcx = THE MAP RENDERER
//   ...
//   010A6F38  mov  rcx, rdi
//   010A6F3B  call 0x10AFA70               ; the rebuild, behind two flags and a counter gate
//
// so frame one hands us the renderer whether or not the engine's own rebuild branch is taken,
// and the hook runs while paused because rendering does not stop when the clock does.
#pragma once
#include <windows.h>
#include <atomic>
#include <cstdint>
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"
#include "arrows.h"
#include "console.h"

namespace frame {

// H3 meter: the longest gap between two consecutive frames since last read, in ms. A monthly
// tick that stalls the game shows up here as one long frame; the tick's own ms does not.
inline double g_worst_gap_ms = 0; inline unsigned long long g_last_frame_qpc = 0;
inline void note_frame() {
    LARGE_INTEGER t, f; QueryPerformanceCounter(&t); QueryPerformanceFrequency(&f);
    if (g_last_frame_qpc) { double gap = 1000.0 * (double)((unsigned long long)t.QuadPart - g_last_frame_qpc) / (double)f.QuadPart; if (gap > g_worst_gap_ms) g_worst_gap_ms = gap; }
    g_last_frame_qpc = (unsigned long long)t.QuadPart;
}
inline double take_worst_gap() { double g = g_worst_gap_ms; g_worst_gap_ms = 0; return g; }

constexpr uintptr_t MAP_UPDATE = 0x10A6EC0;
constexpr uint64_t DRAIN_EVERY = 30;      // frames between console polls (~0.5 s at 60 fps)

inline detour::Hook g_hook;
inline std::atomic<uint64_t> g_frames{0};
inline std::atomic<bool> g_busy{false};
inline std::string g_log;
// Registered by ticklive at attach. Runs on the game thread every frame so a view
// change redraws the map at once instead of waiting for the next month boundary.
inline void (*g_view_poll)() = nullptr;

inline bool active() { return g_hook.active; }

inline void handler(detour::Regs* r) {
    note_frame();
    // rcx is the map renderer; take it once and never again
    if (!arrows::g_map_renderer.load()) arrows::g_map_renderer.store((uintptr_t)r->rcx);

    if ((g_frames.fetch_add(1) % DRAIN_EVERY) != 0) return;
    if (g_view_poll) g_view_poll();      // rate-limited: it touches the marker file
    // Commands run the engine's own dispatcher, which can re-enter map code. One at a time.
    if (g_busy.exchange(true)) return;
    console::drain(g_log);
    g_busy.store(false);
}

inline bool install(const std::string& logpath, std::string* err) {
    if (g_hook.active) return true;   // a second campaign re-runs the install: the live hook stays (reviewed)
    g_log = logpath;
    std::vector<uint8_t> expected{
        0x4c, 0x89, 0x44, 0x24, 0x18,               // mov [rsp+0x18], r8
        0x55,                                        // push rbp
        0x53,                                        // push rbx
        0x57,                                        // push rdi
        0x48, 0x8d, 0x6c, 0x24, 0xb0,               // lea rbp, [rsp-0x50]
        0x48, 0x81, 0xec, 0x50, 0x01, 0x00, 0x00};  // sub rsp, 0x150
    if (!detour::install(g_hook, livetrade::module_base() + MAP_UPDATE, expected,
                         &handler, "map_update_frame")) {
        if (err) *err = g_hook.error;
        return false;
    }
    return true;
}

} // namespace frame
