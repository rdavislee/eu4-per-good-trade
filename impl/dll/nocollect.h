// MERCHANTS NEVER COLLECT -- for the player too (user decision 2026-08-26).
//
// "Merchants never collect; the only collecting node is the trade capital without a merchant; no
// merchant may be placed at the trade capital; applies to the player too." The AI side is the
// table + syncrec (type is always 1). This is the engine side.
//
// THE SEAM (reviewed against the PE, build 835bfdf8). Two functions:
//
//   0xB596E0  SetTrader(CTradeNode* node /*rcx*/, u64 handle /*rdx*/, u8 type /*r8b*/)
//             -- the OUTER one: GetTraderRecord arithmetic (rec = *(node+0x18) + 0xC0 * idx),
//             then, ONLY IF type == 1 (0xB59767), scores the node's outgoing links and writes the
//             chosen ordinal to rec+0xA8 (0xB599AE), then calls
//   0xB5E290  SetTraderFlags(rec, bool hasTrader, u8 type)
//             -- writes rec+0xAC (type) and rec+0xAE (has_trader). Nothing else.
//
// The first version hooked the INNER function. That rewrote the type after the outer one had
// already branched away from its link scoring on the original type 0, so every converted merchant
// carried a steer ordinal nobody chose (Bordeaux "to Champagne" was link #0) -- and it had no
// end-node guard, so it could manufacture the one record state this code base has already
// crashed on (type 1 at a node with an empty outgoing vector, 0xB5654D). Both reviewed.
//
// So the hook is on the OUTER function, where rcx = node and rdx = handle are live:
//   - type != 0            -> nothing to do
//   - node has NO outgoing -> leave type 0 (the engine cannot steer there; counted as at_end)
//   - record has_capital   -> leave type 0 (forcing it would switch the capital's own collection
//                             off; a MERCHANT standing there is the other rule -- counted)
//   - otherwise            -> r8b = 1, and the engine's own link scoring then runs and writes a
//                             real rec+0xA8.
// All four callers of the outer function (0x25AE22 arrival, 0x25B9A3 instant placement,
// 0x27424A send_merchant command, 0x305C6C trade-capital move) pass through this prologue.
//
// Prologue of 0xB596E0, 15 relocatable bytes (no RIP-relative operand, no branch into them,
// checked against .text and .pdata by the reviewer):
//   48 89 5c 24 08   mov [rsp+0x08], rbx
//   48 89 54 24 10   mov [rsp+0x10], rdx
//   55 56 57         push rbp / rsi / rdi
//   41 54            push r12
//
// The SWEEP converts records that were collecting before the hook existed (the save's merchants)
// by calling the OUTER function with type 1, so they get a scored ordinal too, and it checks that
// each conversion landed (+0xAC == 1, +0xA8 in range) -- the test that can go red. It runs every
// tick regardless of the AI marker: it is the enforcement, not an AI feature. Records at end nodes
// and merchants standing at their own capital are counted by name, not fought here.
#pragma once
#include <windows.h>
#include <cstdint>
#include <fstream>
#include <string>
#include <vector>
#include "livetrade.h"
#include "detour.h"

namespace nocollect {

constexpr uintptr_t SET_TRADER_OUTER = 0xB596E0;   // (node, handle, type)
using FnSetTraderOuter = void (__fastcall*)(uintptr_t node, uint64_t handle, uint8_t type);
inline detour::Hook g_hook;
inline uint64_t g_calls = 0, g_type0 = 0, g_forced = 0, g_kept_capital = 0, g_kept_end = 0, g_no_record_oob = 0, g_no_record_unreadable = 0, g_swept = 0, g_red = 0;
inline uint64_t g_scored = 0, g_unscored = 0;   // sweep poison experiment: did the engine choose the ordinal?
inline uint64_t g_at_end = 0, g_at_capital = 0;
inline std::string g_end_names, g_capital_names;
inline bool g_installed = false;

inline bool node_has_outgoing(uintptr_t node) {
    uintptr_t def = livetrade::validate_region(node + 0xA8, 8) ? livetrade::fq(node + 0xA8) : 0;
    if (!def || !livetrade::validate_region(def + 0x98, 16)) return false;   // unreadable: treat as none (never force)
    return livetrade::fq(def + 0xA0) > livetrade::fq(def + 0x98);
}

// the record the outer function will address for (node, handle), slot-checked, or 0
inline uintptr_t record_for(uintptr_t node, uint64_t handle) {
    if (!node || !livetrade::validate_region(node + 0x18, 16)) return 0;
    uintptr_t rb = livetrade::fq(node + 0x18); int rc = livetrade::fi(node + 0x24);
    int idx = (int)(int16_t)(handle >> 32);
    if (!rb || idx < 0 || idx >= rc) { g_no_record_oob++; return 0; }
    if (!livetrade::validate_region(rb + (uintptr_t)idx * 0xC0, 0xC0)) { g_no_record_unreadable++; return 0; }
    // NO slot-equality check here: the engine stamps rec+0x10/+0x14 at 0xB599EF, AFTER the flags
    // call, so on first contact the record is still all-zero and a slot test fails closed -- the
    // merchant would quietly keep collecting (reviewed). The array is index-dense by construction:
    // every engine site addresses rb + 0xC0*idx with no search, so this IS the record it will read.
    return rb + (uintptr_t)idx * 0xC0;
}

inline void on_set_trader(detour::Regs* r) {
    g_calls++;
    if ((r->r8 & 0xFF) != 0) return;                           // already transfer
    g_type0++;
    uintptr_t node = r->rcx; uint64_t handle = r->rdx;
    if (!node_has_outgoing(node)) g_kept_end++;                // counted; type 1 at an END node is safe (relink.h, syncrec.h notes)
    uintptr_t rec = record_for(node, handle);
    if (!rec) return;                                          // cannot see the record: leave the engine alone
    if (livetrade::fb(rec + 0xAD) != 0) { g_kept_capital++; return; }
    r->r8 = (r->r8 & ~(uint64_t)0xFF) | 1;                     // collect -> transfer; the engine scores the link
    g_forced++;
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    const std::vector<uint8_t> expected = {0x48, 0x89, 0x5c, 0x24, 0x08, 0x48, 0x89, 0x54, 0x24, 0x10,
                                           0x55, 0x56, 0x57, 0x41, 0x54};
    if (!detour::install(g_hook, livetrade::module_base() + SET_TRADER_OUTER, expected, on_set_trader, "nocollect")) {
        if (err) *err = g_hook.error;
        return false;
    }
    g_installed = true;
    return true;
}

// Once per tick. Converts records that were collecting before the hook existed; verifies each
// conversion landed; counts (by name) the two classes the rule cannot reach through the engine.
inline int sweep(const std::vector<livetrade::SimNode>& sim, std::ofstream* lg) {
    if (!g_installed) return 0;
    if (livetrade::marker_present("NOWRITE")) return 0;        // a vanilla-control arm must not have its records mutated
    auto set_trader = (FnSetTraderOuter)(livetrade::module_base() + SET_TRADER_OUTER);
    int n = 0, red = 0; uint64_t at_end = 0, at_capital = 0;
    std::string sample, end_names, cap_names;
    for (auto& s : sim) {
        uintptr_t node = s.obj;
        if (!node || !livetrade::validate_region(node + 0x18, 16)) continue;
        uintptr_t rb = livetrade::fq(node + 0x18); int rc = livetrade::fi(node + 0x24);
        if (!rb || rc <= 0 || rc > 4096 || !livetrade::validate_region(rb, (size_t)rc * 0xC0)) continue;
        bool has_out = node_has_outgoing(node);
        int end_here = 0, cap_here = 0;
        for (int i = 0; i < rc; i++) {
            uintptr_t rec = rb + (uintptr_t)i * 0xC0;
            if ((livetrade::fi(rec + 0x14) & 0xFFFF) != i) continue;   // slot check (syncrec's)
            if (livetrade::fb(rec + 0xAE) == 0) continue;               // no trader
            if (livetrade::fb(rec + 0xAD) != 0) { cap_here++; continue; }   // a merchant at its own capital
            if (livetrade::fb(rec + 0xAC) != 0) continue;               // already transferring
            if (!has_out) end_here++;                                   // counted; converted like any other record
            uint64_t handle = livetrade::fq(rec + 0x10);
            int outc = 0;
            { uintptr_t def = livetrade::fq(node + 0xA8); outc = (int)((livetrade::fq(def + 0xA0) - livetrade::fq(def + 0x98)) / 0x78); }
            // POISON EXPERIMENT (reviewed): the outer function scores links only when a [country x node]
            // presence gate passes; otherwise it jumps to the flags call and +0xA8 keeps whatever was
            // there. Writing a legal sentinel first and reading it back tells the two apart per record.
            int poison = outc >= 2 ? outc - 1 : -1;
            if (poison >= 0) *(int32_t*)(rec + 0xA8) = poison;
            set_trader(node, handle, 1);                                // the outer function
            int type_after = livetrade::fb(rec + 0xAC), ord = livetrade::fi(rec + 0xA8);
            if (poison >= 0) { if (ord != poison) g_scored++; else g_unscored++; }
            if (type_after != 1 || ord < 0 || ord >= outc) { red++; if (lg) *lg << "  [nocollect] RED: conversion did not land at " << s.name << "#" << i << " type=" << type_after << " ord=" << ord << "/" << outc << (char)10; }
            n++; g_swept++;
            if (sample.size() < 200) sample += s.name + "#" + std::to_string(i) + "->" + std::to_string(ord) + "/" + std::to_string(outc) + (poison >= 0 ? (ord != poison ? "s " : "u ") : " ");
        }
        if (end_here) { at_end += end_here; if (end_names.size() < 120) end_names += s.name + "(" + std::to_string(end_here) + ") "; }
        if (cap_here) { at_capital += cap_here; if (cap_names.size() < 120) cap_names += s.name + "(" + std::to_string(cap_here) + ") "; }
    }
    g_red += red; g_at_end = at_end; g_at_capital = at_capital; g_end_names = end_names; g_capital_names = cap_names;
    if (lg && (n || at_end || at_capital))
        *lg << "  [nocollect] swept " << n << " collecting merchants to transfer (" << sample << "); " << red << " did not land; "
            << at_end << " collect at END nodes [" << end_names << "]; " << at_capital << " merchants stand at their own capital [" << cap_names << "]" << (char)10;
    return n;
}

inline void report(std::ofstream& lg) {
    lg << "  [nocollect] SetTrader(outer) calls=" << g_calls << " of which type0=" << g_type0
       << ": forced=" << g_forced << " kept_end=" << g_kept_end << " kept_capital=" << g_kept_capital
       << " no_record(oob=" << g_no_record_oob << " unreadable=" << g_no_record_unreadable << ")"
       << "; swept=" << g_swept << " red=" << g_red << " (engine scored the ordinal: " << g_scored << ", gate skipped: " << g_unscored << ")"
       << "; this tick: at END nodes=" << g_at_end << " [" << g_end_names << "] at own capital=" << g_at_capital << " [" << g_capital_names << "]" << (char)10;
}

} // namespace nocollect
