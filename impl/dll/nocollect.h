// MERCHANTS NEVER COLLECT -- for the player too (user decision 2026-08-26).
//
// "Merchants never collect; the only collecting node is the trade capital without a merchant; no
// merchant may be placed at the trade capital; applies to the player too." The AI side is the
// table + syncrec (type is always 1). This is the engine side: every change of a trader record's
// mode goes through ONE function,
//
//   0xB5E290  SetTrader(rec /*rcx*/, bool hasTrader /*dl*/, u8 type /*r8b: 0 collect, 1 steer*/)
//
// -- the sole semantic writer of rec+0xAC (type) and rec+0xAE (has_trader), with one caller
// (0xB599E5) that every path funnels into: the send-merchant command, the node window's
// collect/transfer toggle, PlaceMerchantAtNode, and our own syncrec. So one prologue hook that
// rewrites r8b to 1 whenever hasTrader is set enforces the rule for every path at once, without
// touching the GUI's commands. The GUI's collect button then does nothing visible, and is removed
// from the view separately (interface override) so the player is not offered a dead choice.
//
// The ONE exception is a record at the country's own trade capital (rec+0xAD has_capital): the
// engine's collect-eligibility is `has_trader ? type == 0 : has_capital`, so forcing type=1 on a
// merchant standing at home would switch the capital's own collection OFF. Such a record keeps
// whatever the engine asked for (vanilla: collect). Placing a merchant at the capital is the
// user's other rule; the AI never does it, and the player's case is left to the sweep below.
//
// Prologue (from the PE on disk, build 835bfdf8), 16 relocatable bytes:
//   48 89 5c 24 18   mov [rsp+0x18], rbx
//   55               push rbp
//   56               push rsi
//   57               push rdi
//   48 83 ec 30      sub rsp, 0x30
//   41 0f b6 f0      movzx esi, r8b        <- reads r8b AFTER our handler ran, so the rewrite lands
//
// The tick SWEEP handles what was already collecting before the hook existed (the 1444 save's
// merchants, e.g. Castile's at Bordeaux): any record with has_trader && type == 0 && !has_capital
// is re-set through SetTrader(rec, true, 1) once, and counted.
#pragma once
#include <windows.h>
#include <cstdint>
#include <fstream>
#include <string>
#include <vector>
#include "livetrade.h"
#include "detour.h"

namespace nocollect {

constexpr uintptr_t SET_TRADER = 0xB5E290;
using FnSetTrader = void (__fastcall*)(uintptr_t, bool, uint8_t);
inline detour::Hook g_hook;
inline uint64_t g_calls = 0, g_forced = 0, g_kept_capital = 0, g_swept = 0, g_at_end = 0;
inline bool g_installed = false;

inline void on_set_trader(detour::Regs* r) {
    g_calls++;
    uintptr_t rec = r->rcx;
    bool has_trader = (r->rdx & 0xFF) != 0;
    uint8_t type = (uint8_t)(r->r8 & 0xFF);
    if (!has_trader || type != 0) return;                       // nothing to force
    if (!rec || !livetrade::validate_region(rec + 0xAD, 1)) return;
    if (livetrade::fb(rec + 0xAD) != 0) { g_kept_capital++; return; }   // the capital keeps collecting
    r->r8 = (r->r8 & ~(uint64_t)0xFF) | 1;                        // collect -> transfer
    g_forced++;
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    const std::vector<uint8_t> expected = {0x48, 0x89, 0x5c, 0x24, 0x18, 0x55, 0x56, 0x57,
                                           0x48, 0x83, 0xec, 0x30, 0x41, 0x0f, 0xb6, 0xf0};
    if (!detour::install(g_hook, livetrade::module_base() + SET_TRADER, expected, on_set_trader, "nocollect")) {
        if (err) *err = g_hook.error;
        return false;
    }
    g_installed = true;
    return true;
}

// Once per tick: convert records that were collecting before the hook existed. Returns the count.
inline int sweep(const std::vector<livetrade::SimNode>& sim, std::ofstream* lg) {
    if (!g_installed) return 0;
    auto set_trader = (FnSetTrader)(livetrade::module_base() + SET_TRADER);
    int n = 0, at_end = 0; std::string sample;
    for (auto& s : sim) {
        uintptr_t node = s.obj;
        if (!node || !livetrade::validate_region(node + 0x18, 16)) continue;
        uintptr_t rb = livetrade::fq(node + 0x18); int rc = livetrade::fi(node + 0x24);
        if (!rb || rc <= 0 || rc > 4096 || !livetrade::validate_region(rb, (size_t)rc * 0xC0)) continue;
        // an END node (no outgoing link in the installed graph) has nothing the engine can steer
        // along: SetTrader(rec, true, 1) there is undone by the engine itself (+0xAC must be 0 with
        // zero outgoing links, OFFSETS.md), so the sweep re-converted genua/hangzhou every tick.
        // Those merchants collect in the engine; counted apart, not fought.
        bool is_end = true;
        { uintptr_t def = livetrade::validate_region(node + 0xA8, 8) ? livetrade::fq(node + 0xA8) : 0;
          if (def && livetrade::validate_region(def + 0x98, 16)) is_end = livetrade::fq(def + 0xA0) <= livetrade::fq(def + 0x98); }
        for (int i = 0; i < rc; i++) {
            uintptr_t rec = rb + (uintptr_t)i * 0xC0;
            if (livetrade::fb(rec + 0xAE) == 0) continue;            // no trader
            if (livetrade::fb(rec + 0xAC) != 0) continue;            // already transferring
            if (livetrade::fb(rec + 0xAD) != 0) continue;            // capital: keeps collecting
            if (is_end) { at_end++; continue; }
            set_trader(rec, true, 1);                                 // the hook sees type 1 and lets it through
            n++; g_swept++;
            if (sample.size() < 160) sample += s.name + "#" + std::to_string(livetrade::fi(rec + 0x14) & 0xFFFF) + " ";
        }
    }
    g_at_end = at_end;
    if (lg && (n || at_end)) *lg << "  [nocollect] swept " << n << " collecting merchants to transfer (" << sample << "); " << at_end << " collect at Phi_w END nodes (no outgoing link for the engine to steer along)" << (char)10;
    return n;
}

inline void report(std::ofstream& lg) {
    lg << "  [nocollect] SetTrader calls=" << g_calls << " forced collect->transfer=" << g_forced
       << " kept at capital=" << g_kept_capital << " swept=" << g_swept << (char)10;
}

} // namespace nocollect
