// FINDING THE SELECTED PROVINCE (spec 1.12's per-good trigger; test D1).
//
// "Clicking a province switches province colouring to the vanilla trade-goods rendering for that
// good and redirects the arrow layer to that good's graph." Nothing in the binary is named
// `selected_province`, and the province window is opened by GUI name rather than by a call that
// carries the province, so the pointer is found empirically instead: the province array is a flat
// stride-0x2E10 table at G+0x1CA8, so ANY qword in the game singleton that lands exactly on an
// element boundary of that table is a candidate "current province" pointer. Scan, click, scan
// again -- the offset whose province index tracks the click is the one.
#pragma once
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "liveworld.h"

namespace selprov {

// offset in the game singleton -> province index it currently points at
inline std::map<int, int> g_last;
inline int g_offset = -1;          // the confirmed offset, once identified

struct Cand { int off; int prov; };

inline std::vector<Cand> scan(int span = 0xA000) {
    std::vector<Cand> out;
    uintptr_t g = livetrade::game_singleton();
    if (!g) return out;
    uintptr_t base = livetrade::rq(g + 0x1CA8), endp = livetrade::rq(g + 0x1CB0);
    if (!base || endp <= base) return out;
    uint64_t span_bytes = endp - base;
    int count = (int)(span_bytes / liveworld::PROV_STRIDE);
    if (count <= 0 || count > 20000) return out;
    for (int off = 0; off + 8 <= span; off += 8) {
        if (!livetrade::validate_region(g + off, 8)) continue;
        uintptr_t p = livetrade::fq(g + off);
        if (p < base || p >= endp) continue;
        uint64_t delta = p - base;
        if (delta % liveworld::PROV_STRIDE) continue;         // must be an element boundary
        out.push_back({off, (int)(delta / liveworld::PROV_STRIDE)});
    }
    return out;
}

// Log every candidate, and mark the ones whose value CHANGED since the last scan -- those are the
// ones tracking the click.
inline void report(const std::string& logpath) {
    auto c = scan();
    std::ofstream lg(logpath, std::ios::app);
    lg << "--- selected-province candidates: " << c.size() << " qwords in G point at a province ---" << "\n";
    int changed = 0;
    for (auto& e : c) {
        auto it = g_last.find(e.off);
        bool moved = (it != g_last.end() && it->second != e.prov);
        if (moved) changed++;
        lg << "   G+0x" << std::hex << e.off << std::dec << "  -> province index " << e.prov
           << (moved ? "   <== CHANGED" : "") << "\n";
        g_last[e.off] = e.prov;
    }
    lg << "   (" << changed << " changed since the previous scan)" << "\n";
}

// Once g_offset is known, this is the live read: the trade good of the selected province.
inline int selected_good_slot() {
    if (g_offset < 0) return -1;
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + g_offset, 8)) return -1;
    uintptr_t p = livetrade::fq(g + g_offset);
    if (!p || !livetrade::validate_region(p + liveworld::PROV_GOOD, 8)) return -1;
    uintptr_t good = livetrade::fq(p + liveworld::PROV_GOOD);
    if (!good) return -1;
    return liveworld::good_slot_of(good);
}

} // namespace selprov
