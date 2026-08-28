// PER-GOOD PROVINCE COLORING (spec 1.12; user 2026-08-27): while the per-good view is active the
// trade mapmode must color the map the way the TRADE-GOODS mapmode does with that good selected --
// provinces producing the good in the good's own color, every other province the engine's gray --
// and the moment the view closes the vanilla trade-node coloring comes back.
//
// Engine seams (static RE 2026-08-27, verified in the session that found them):
//   0x12F0B40  FillProvinceColours(uint32* dst rcx, int fmt edx, int mapmode r8d) -- the ONE
//              provider for every mapmode's primary color plane; per-mode dispatch via an RVA
//              table at 0x12FD6BC indexed by mapmode; `cmp ebx,0x54; ja -> epilogue` means any
//              mode > 0x54 paints NOTHING (the alpha fill for fmt<4 runs before the dispatch).
//              Prologue = 14 relocatable bytes, ideal for detour.h.
//   dst is 4 bytes per province, index = province id, A8R8G8B8: dst[0]=b*255 dst[1]=g*255
//              dst[2]=r*255 (dst[3] set by the engine's own alpha pass).
//   provinces  inline array at *(G+0x1CA8), stride 0x2E10; id at +0x20; good at +0x458.
//   CTradeGood color floats r/g/b at +0x98/+0x9C/+0xA0 (the CColor embedded at +0x88).
//   mode-23 gray for a non-matching province: 0x7f7f7f (0x12FCD60).
//   REPAINT: mode 4 is NOT in the engine's selection-invalidate list (0x9F2E80), so a view change
//              must set IGI+0x34 = 1 (and IGI+0x38 = 0) itself; the map update at 0x818619 then
//              re-runs the provider next frame.
//
// The handler paints the plane itself and routes the engine to its no-op path (r8 = 0x55): fully
// DLL-owned, nothing written into .text, restored by removing the detour.
#pragma once
#include <atomic>
#include <cstdint>
#include <map>
#include <string>
#include "detour.h"
#include "livetrade.h"

namespace colorview {

constexpr uintptr_t FILL_COLORS   = 0x12F0B40;
constexpr uintptr_t PROV_ARRAY    = 0x1CA8;     // G+ -> CProvince[] (inline, stride 0x2E10)
constexpr uintptr_t PROV_STRIDE   = 0x2E10;
constexpr uintptr_t PCOUNT_HOLDER = 0x233FED8;  // *(base+) -> +0x6F0/+0x6F8 bound the array
constexpr int PROV_GOOD = 0x458;
constexpr int GOOD_R = 0x98, GOOD_G = 0x9C, GOOD_B = 0xA0;

inline detour::Hook g_hook;
inline std::atomic<uintptr_t> g_good{0};   // CTradeGood* to paint; 0 = off, vanilla paints
inline uint64_t g_paints = 0, g_passthrough = 0, g_pokes = 0, g_bound_mismatch = 0;
inline int g_last_nprov = 0;

// name -> CTradeGood*, built once from the trade-goods database (liveworld.h's layout)
inline std::map<std::string, uintptr_t> g_by_name;
inline uintptr_t good_by_name(const std::string& want) {
    if (want.empty()) return 0;
    if (g_by_name.empty()) {
        uintptr_t db = livetrade::rq(livetrade::module_base() + 0x242BE70);
        if (!db || !livetrade::validate_region(db + 0x10, 16)) return 0;
        uintptr_t begin = livetrade::fq(db + 0x10), end = livetrade::fq(db + 0x18);
        if (!begin || end <= begin || (end - begin) > 8 * 512) return 0;
        if (!livetrade::validate_region(begin, end - begin)) return 0;
        for (uintptr_t p = begin; p + 8 <= end; p += 8) {
            uintptr_t g = livetrade::fq(p);
            if (!g || !livetrade::validate_region(g + 0x18, 0x20)) continue;
            uint64_t sz = *(uint64_t*)(g + 0x28), cap = *(uint64_t*)(g + 0x30);
            if (sz == 0 || sz > 64 || cap < sz) continue;
            const char* cp = (const char*)(g + 0x18);
            if (cap >= 16) {
                uintptr_t hp = livetrade::fq(g + 0x18);
                if (!hp || !livetrade::validate_region(hp, sz + 1)) continue;
                cp = (const char*)hp;
            }
            g_by_name[std::string(cp, (size_t)sz)] = g;
        }
    }
    if (g_by_name.size() < 20) { g_by_name.clear(); return 0; }   // partial walk: retry next call, never cache it
    auto it = g_by_name.find(want);
    return it == g_by_name.end() ? 0 : it->second;
}

inline int province_count(uintptr_t& arr) {
    // The engine's own mode painters iterate the HOLDER's array (*(holder+0x6F0), stride 0x2E10)
    // and the dst index is the sequential position in it, so index from that array -- no aliasing
    // assumption against G+0x1CA8 needed (reviewed). One whole-span validation replaces ~5000
    // per-province VirtualQuery calls (~45 ms of syscalls per repaint, reviewed).
    uintptr_t h = livetrade::rq(livetrade::module_base() + PCOUNT_HOLDER);
    if (!h || !livetrade::validate_region(h + 0x6F0, 16)) return 0;
    uintptr_t b = livetrade::fq(h + 0x6F0), e = livetrade::fq(h + 0x6F8);
    if (!b || e <= b) return 0;
    size_t span = e - b;
    if (span % PROV_STRIDE != 0) { g_bound_mismatch++; return 0; }
    int n = (int)(span / PROV_STRIDE);
    if (n <= 0 || n > 20000) return 0;      // Anbennar-sized maps exceed vanilla's ~5000
    if (!livetrade::validate_region(b, span)) { g_bound_mismatch++; return 0; }
    arr = b;
    return n;
}

inline void handler(detour::Regs* r) {
    if ((int)(r->r8 & 0xFFFFFFFF) != 4) return;          // only the TRADE mapmode's plane
    uintptr_t good = g_good.load();
    if (!good) { g_passthrough++; return; }              // aggregate view: vanilla paint
    uintptr_t arr = 0;
    int n = province_count(arr);
    if (!n || !r->rcx) { g_passthrough++; return; }
    g_last_nprov = n;
    uint8_t cr = 0x7f, cg = 0x7f, cb = 0x7f;
    if (livetrade::validate_region(good + GOOD_R, 12)) {
        auto f2b = [](float v) { int x = (int)(v * 255.0f); return (uint8_t)(x < 0 ? 0 : x > 255 ? 255 : x); };
        cr = f2b(*(float*)(good + GOOD_R));
        cg = f2b(*(float*)(good + GOOD_G));
        cb = f2b(*(float*)(good + GOOD_B));
    }
    uint8_t* dst = (uint8_t*)r->rcx;
    for (int id = 0; id < n; id++) {
        uintptr_t prov = arr + (uintptr_t)id * PROV_STRIDE;
        uintptr_t pg = *(uintptr_t*)(prov + PROV_GOOD);   // the whole array span was validated above
        if (pg == good) { dst[id * 4 + 0] = cb; dst[id * 4 + 1] = cg; dst[id * 4 + 2] = cr; }
        else            { dst[id * 4 + 0] = 0x7f; dst[id * 4 + 1] = 0x7f; dst[id * 4 + 2] = 0x7f; }
    }
    r->r8 = 0x55;                                        // > 0x54: the engine paints nothing on top
    g_paints++;
}

// ask the engine to re-run the provider next frame (mode 4 never invalidates itself)
inline void poke_repaint() {
    uintptr_t G = livetrade::game_singleton();
    uintptr_t igi = (G && livetrade::validate_region(G + 0x1E00, 8)) ? livetrade::fq(G + 0x1E00) : 0;
    if (!igi || !livetrade::validate_region(igi + 0x34, 16)) return;
    *(volatile uint8_t*)(igi + 0x34) = 1;
    *(volatile int64_t*)(igi + 0x38) = 0;
    g_pokes++;
}

// per frame, after viewmode::poll: keep the painted good in step with the view
inline void sync(const std::string& good_name) {
    uintptr_t want = good_by_name(good_name);
    if (want == g_good.load()) return;
    g_good = want;
    poke_repaint();
}

inline bool install(std::string* err) {
    if (g_hook.active) return true;                      // a second campaign re-runs the install
    uintptr_t site = livetrade::module_base() + FILL_COLORS;
    std::vector<uint8_t> expected{
        0x44, 0x89, 0x44, 0x24, 0x18,                    // mov [rsp+0x18], r8d
        0x89, 0x54, 0x24, 0x10,                          // mov [rsp+0x10], edx
        0x48, 0x89, 0x4c, 0x24, 0x08};                   // mov [rsp+8], rcx
    if (!detour::install(g_hook, site, expected, &handler, "fill_province_colours")) {
        if (err) *err = g_hook.error;
        return false;
    }
    return true;
}

} // namespace colorview
