// THE ENGINE'S MERCHANT RECORD MUST SAY WHAT OUR TABLE SAYS (spec 1.7; tests C1-C5, G1).
//
// assign::g_table is what the routing honours, so value moves the way the table says. But the
// MAP draws the per-country record (node+0x18[i], stride 0xC0), and nothing wrote the table back
// into it -- so a merchant our AI moved to a reverse end kept a record saying "collecting", or
// "steering along link #k", and was invisible where it actually worked. "No merchants on any
// reverse edges" was that: 134 placements in the table, zero in the records.
//
// What the record CAN express, from the field map:
//   +0xAE has_trader   a merchant is posted here
//   +0xAC type         0 = collect, 1 = steer
//   +0xA8 steer index  a 0-based position in the definition's OUTGOING vector, read UNBOUNDED by
//                      0xB54F8F / 0xB547F9 / 0xB5654D / 0xB556FF / 0x13FC24D -- never a sentinel,
//                      never negative, never >= count.
// So a FORWARD target is written exactly: type=1, +0xA8 = its ordinal. A REVERSE end has no
// ordinal; it is written type=1, +0xA8 = 0 -- a valid slot the engine can read safely -- and the
// routing (which reads the table, not the record) supplies the real target. flagfix.h keeps the
// engine from drawing that merchant on link #0's panel, and the shield on the reverse panel is
// drawn from the table.
//
// The setter is the engine's own: 0xB5E290 SetTrader(rec, bool hasTrader, u8 type) writes +0xAC
// and +0xAE together. +0xA8 is written directly, as the steer command 0x5DA4F0 does at 0x5DA5C4.
//
// Only records the engine already holds are touched. A country with no record at the node has no
// standing to steer with; the table entry stays and takes effect the month the record appears.
#pragma once
#include <windows.h>
#include <cstdint>
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "assign.h"

namespace syncrec {

constexpr uintptr_t SET_TRADER = 0xB5E290;    // (rec, bool hasTrader, u8 type)
using FnSetTrader = void (__fastcall*)(uintptr_t, bool, uint8_t);

inline int g_forward = 0, g_reverse = 0, g_missing = 0, g_unchanged = 0;

// ordinal of `target_def` in `def`'s outgoing vector, or -1 (a reverse end)
inline int forward_ordinal(uintptr_t def, uintptr_t target_def) {
    if (!def || !livetrade::validate_region(def + 0x98, 16)) return -1;
    uintptr_t b = livetrade::fq(def + 0x98), e = livetrade::fq(def + 0xA0);
    if (!b || e <= b || (e - b) > 0x78 * 64) return -1;
    int i = 0;
    for (uintptr_t p = b; p + 0x78 <= e; p += 0x78, i++)
        if (livetrade::validate_region(p + 0x30, 8) && livetrade::fq(p + 0x30) == target_def) return i;
    return -1;
}

inline void apply(const std::vector<livetrade::SimNode>& sim, std::ofstream* lg) {
    if (assign::g_table.empty()) return;
    std::map<std::string, uintptr_t> node_by_key, def_by_key;
    for (auto& s : sim) {
        std::string k = livetrade::node_key(s.obj);
        if (k.empty()) continue;
        node_by_key[k] = s.obj;
        def_by_key[k]  = livetrade::fq(s.obj + 0xA8);
    }
    auto set_trader = (FnSetTrader)(livetrade::module_base() + SET_TRADER);
    int fwd = 0, rev = 0, missing = 0, same = 0;
    for (auto& [key, target] : assign::g_table) {
        int country = key.first;
        auto nit = node_by_key.find(key.second);
        auto tit = def_by_key.find(target);
        if (nit == node_by_key.end() || tit == def_by_key.end()) { missing++; continue; }
        uintptr_t node = nit->second;
        uintptr_t base = livetrade::rq(node + 0x18);
        int cnt = livetrade::ri(node + 0x24);
        if (!base || cnt <= 0 || cnt > 4096 || !livetrade::validate_region(base, (size_t)cnt * 0xC0)) {
            missing++; continue;
        }
        // the record is indexed by country index (field map: allocated countryCount * 0xC0)
        int cidx = livetrade::country_index_of(country);
        if (cidx < 0 || cidx >= cnt) { missing++; continue; }
        uintptr_t rec = base + (uintptr_t)cidx * 0xC0;
        if ((livetrade::fi(rec + 0x14) & 0xFFFF) != cidx) { missing++; continue; }   // slot mismatch
        int ord = forward_ordinal(livetrade::fq(node + 0xA8), tit->second);
        int32_t want_idx = ord >= 0 ? ord : 0;
        bool already = livetrade::fb(rec + 0xAE) != 0 && livetrade::fb(rec + 0xAC) == 1 &&
                       livetrade::fi(rec + 0xA8) == want_idx;
        if (already) { same++; continue; }
        DWORD old = 0;
        if (!VirtualProtect((void*)(rec + 0xA8), 8, PAGE_READWRITE, &old)) { missing++; continue; }
        *(int32_t*)(rec + 0xA8) = want_idx;
        VirtualProtect((void*)(rec + 0xA8), 8, old, &old);
        set_trader(rec, true, 1);
        if (ord >= 0) fwd++; else rev++;
    }
    g_forward = fwd; g_reverse = rev; g_missing = missing; g_unchanged = same;
    if (lg && (fwd || rev))
        *lg << "  [syncrec] engine records aligned to the table: " << fwd << " forward steers, "
            << rev << " reverse ends (index 0, target from the table), " << same
            << " already right, " << missing << " with no record yet" << (char)10;
}

} // namespace syncrec
