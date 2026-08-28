// DIRECTION GATES (spec 1.10; test G4, first half).
//
// Spec 1.10, verbatim: "Any mechanism gated on one nation being upstream or downstream of another
// evaluates TRUE." The engine expresses every such gate through three uint8 reachability matrices
// that the trade-node manager rebuilds once per monthly update:
//
//   mgr = the trade-node manager (== G+0x2198)
//     mgr+0x24  int32  stride == node count
//     mgr+0x88  u8*    matrix A -- BFS from the country's trade capital        (0xB4D0D0)
//     mgr+0x90  u8*    matrix B -- as A, plus every node holding a merchant    (0xB4D0D0)
//     mgr+0x98  u8*    matrix C -- gated BFS                                    (0xB4D530)
//     mgr+0xA0  int32  total size of each matrix
//   index = countryIdx * stride + node->[0x120]
//
// and rebuilds them at
//   0xB4BD07  mov rcx, rsi          ; rsi = the manager
//   0xB4BD0A  call 0xB4DB00         ; the rebuild
//
// So the whole of 1.10 is one call-site redirect: let the engine rebuild, then fill all three
// matrices with 1. Every inline gate site reads the matrix directly and now sees TRUE; the two
// out-of-line predicates are leaf functions returning al, so they are patched to `mov al,1; ret`
// rather than made to walk a table that now says the same thing 25 million times:
//
//   0x3E1D30  the treasure-fleet gate            (matrix A, 3 callers)
//   0xB4E020  IsNodeUpstreamOfCountry            (matrix B, 2 callers)
//
// Two things this deliberately does NOT do. It does not touch the trade-conflict casus belli at
// 0x38D8C0, which performs no direction test at all -- it is a pure power-share threshold, exactly
// as 1.10 describes, so "never refuses on upstream/downstream grounds" is already true there and
// patching it would be patching nothing. And it does not make the treasure-fleet ROUTER work by
// filling matrix A: a router whose every hop test says yes just takes the first outgoing link and
// dead-ends. Routing is spec 1.11 and is treasure.h's job.
#pragma once
#include <windows.h>
#include <cstdint>
#include <fstream>
#include <string>
#include "detour.h"
#include "livetrade.h"

namespace gates {

// EVERY call site, not just the monthly one. Enumerated from the 1.37.5 binary by scanning .text
// for E8 rel32 calls whose target resolves to 0xB4DB00 -- exactly these six, which matches the
// count recorded during RE. Hooking only 0xB4BD0A left the other five free to refill B with the
// engine's own BFS behind our back: measured on the 1635 world, matrix B held engine content at
// ~40% of half-second samples, i.e. spec 1.10's 21 INLINED gate sites were reading vanilla's
// directions a large fraction of the time. The frame-poll refill could not fix that (it mops up
// after the fact); owning the call sites puts the refill immediately after every rebuild.
constexpr uintptr_t REBUILD_CALLS[] = { 0x482DFA, 0x766F78, 0x774B57, 0x775EEC, 0x7769D1, 0xB4BD0A };
constexpr int REBUILD_CALL_N = 6;
inline int g_sites_hooked = 0;
inline std::string g_site_report;      // which sites refused, and why
constexpr uintptr_t REBUILD_CALL = 0xB4BD0A;   // call 0xB4DB00, rcx = manager (the monthly one)
constexpr uintptr_t REBUILD_FN   = 0xB4DB00;
constexpr uintptr_t GATE_TREASURE = 0x3E1D30;  // matrix A predicate
constexpr uintptr_t GATE_UPSTREAM = 0xB4E020;  // matrix B predicate (IsNodeUpstreamOfCountry)

inline bool g_active = false;
inline uint64_t g_fills = 0;
inline int g_last_size = 0, g_last_stride = 0;

// WHERE A FILL CAME FROM -- the distinction IS the instrument. Straight after the engine's own
// rebuild, B legitimately holds the engine's BFS and we are about to correct it, so zeros there are
// expected and mean nothing. Zeros found at a FRAME poll mean an UNOWNED 0xB4DB00 call site ran and
// spec 1.10 was genuinely off for up to one poll interval. That is the lapse worth counting, and
// unlike the pre-rebuild sample it CANNOT be satisfied by our own memset.
enum FillSite { FILL_REBUILD = 0, FILL_FRAME = 1, FILL_TICK = 2 };
inline long long g_fills_frame = 0, g_fills_rebuild = 0;
inline long long g_lapses = 0;            // frame polls that found engine content in B
inline int  g_lapse_worst = 0;            // worst zero-count sampled at such a poll (of 512 probes)
inline int  g_size_growth = 0;            // mgr+0xA0 grew while the block pointer stayed put
inline int  g_first_size = 0;
inline uintptr_t g_first_b = 0;
inline bool g_no_frame_fill = false;      // pgt.NOGATEFILL: sample but do not refill, to make the above go red
inline int g_zero_before_rebuild = -1;   // B as the ENGINE left it, sampled before each rebuild: 0 == the gate held all month

// The growth guard that used to live here is REMOVED (2026-08-27, reviewed): its country-count
// reader vcalled the wrong global and returned garbage in vanilla (-1157598207) while looking
// plausible under a total conversion; four of the six 0xB4DB00 call sites are outside our
// control and advance mgr+0xA0 without reallocating, so it could not observe growth anyway;
// and it never fired in 201 years of play or in either conversion. Protection that reads as
// protection but cannot work is worse than none.

using FnRebuild = void(__fastcall*)(uintptr_t);

// Fill matrix B (the upstream/downstream table). Callable, because the mod ALSO rebuilds the
// matrices directly (ticklive: after an orientation install and after merchant landings) and the
// engine's rebuild restores B to its own BFS -- without re-filling there, spec 1.10 held only for
// the microseconds between the engine's monthly rebuild and our next one (reviewed).
inline void fill_b(uintptr_t mgr, int site = FILL_FRAME) {
    if (!g_active || !mgr) return;
    if (!livetrade::validate_region(mgr + 0x24, 0x80)) return;
    int size = *(int32_t*)(mgr + 0xA0);
    g_last_stride = *(int32_t*)(mgr + 0x24);
    g_last_size = size;
    if (size <= 0 || size > (1 << 26)) return;
    uintptr_t m2 = *(uintptr_t*)(mgr + 0x90);          // B only: A is the treasure router's BFS, C is the model's
    if (!m2 || !livetrade::validate_region(m2, (size_t)size)) return;

    // GROWTH DETECTOR, replacing the guard removed above. The engine memsets mgr+0xA0 bytes over this
    // same block on EVERY rebuild, so writing that many bytes is exactly as safe as the engine's own
    // write -- but only while the count has not grown since the block was allocated. validate_region
    // cannot see a heap-block boundary (VirtualQuery reports the whole page region), so watch the
    // count itself: if it grows while the pointer stays put, clamp to the allocated size and say so.
    if (g_first_b != m2) { g_first_b = m2; g_first_size = size; }
    else if (size > g_first_size) { g_size_growth++; size = g_first_size; }

    if (site != FILL_REBUILD) {
        // Sample BEFORE our write. Only the ENGINE writes zeros into B, so a nonzero count here is a
        // real lapse of spec 1.10: an unowned 0xB4DB00 call site ran since our last fill.
        const uint8_t* p = (const uint8_t*)m2;
        int zero = 0, step = size > 4096 ? size / 512 : 1;
        for (int i = 0; i < size; i += step) if (!p[i]) zero++;
        if (zero > 0) { g_lapses++; if (zero > g_lapse_worst) g_lapse_worst = zero; }
    }
    if (site == FILL_FRAME && g_no_frame_fill) return;   // red-test mode: measure, deliberately do not fix
    memset((void*)m2, 1, (size_t)size);
    g_fills++;
    if (site == FILL_FRAME) g_fills_frame++; else g_fills_rebuild++;
}

inline void __fastcall rebuild_wrapper(uintptr_t mgr) {
    // BEFORE the engine rebuilds, read the table as it stands: that is the only moment the fill can
    // be observed to have survived (or not) a month of engine and mod activity. Reading straight
    // after our own memset, as this used to, could never fail -- it measured memset, not the gate.
    if (g_active && mgr && livetrade::validate_region(mgr + 0x24, 0x80)) {
        int sz = *(int32_t*)(mgr + 0xA0);
        uintptr_t b = *(uintptr_t*)(mgr + 0x90);
        if (sz > 0 && sz <= (1 << 26) && b && livetrade::validate_region(b, (size_t)sz)) {
            const uint8_t* p = (const uint8_t*)b;
            int zero = 0, step = sz > 4096 ? sz / 512 : 1;
            for (int i = 0; i < sz; i += step) if (!p[i]) zero++;
            g_zero_before_rebuild = zero;              // 0 == B still all-1 from last month
        }
    }
    ((FnRebuild)(livetrade::module_base() + REBUILD_FN))(mgr);
    fill_b(mgr, FILL_REBUILD);
}

// Force the two out-of-line predicates true. Both are leaf functions that return their answer in
// al, so three bytes replace each of them outright.
inline bool force_predicates(std::string* err) {
    struct { uintptr_t rva; const char* name; } fns[] = {
        {GATE_TREASURE, "treasure-fleet gate"},
        {GATE_UPSTREAM, "IsNodeUpstreamOfCountry"},
    };
    for (auto& f : fns) {
        uintptr_t at = livetrade::module_base() + f.rva;
        if (!livetrade::validate_region(at, 8)) { if (err) *err = std::string(f.name) + ": unreadable"; return false; }
        // both begin by loading from their argument; refuse anything else (spec 2.5)
        uint8_t b0 = *(uint8_t*)at;
        if (b0 != 0x48 && b0 != 0x49) { if (err) *err = std::string(f.name) + ": unexpected prologue"; return false; }
        DWORD old = 0;
        if (!VirtualProtect((void*)at, 3, PAGE_EXECUTE_READWRITE, &old)) {
            if (err) *err = std::string(f.name) + ": VirtualProtect failed"; return false;
        }
        uint8_t patch[3] = {0xB0, 0x01, 0xC3};      // mov al, 1 ; ret
        memcpy((void*)at, patch, 3);
        VirtualProtect((void*)at, 3, old, &old);
        FlushInstructionCache(GetCurrentProcess(), (void*)at, 3);
    }
    return true;
}

inline bool g_installed = false;

inline bool install(std::string* err) {
    if (g_installed) return true;
    uintptr_t base = livetrade::module_base();
    // One thunk serves all six: they span ~7 MB of .text, far inside rel32 reach of each other.
    uint8_t* thunk = detour::alloc_near(base + REBUILD_CALLS[0], 32);
    if (!thunk) { if (err) *err = "gate thunk alloc failed"; return false; }
    uint8_t* p = thunk;
    *p++ = 0x48; *p++ = 0xB8;                        // mov rax, imm64
    uint64_t fn = (uint64_t)&rebuild_wrapper;
    memcpy(p, &fn, 8); p += 8;
    *p++ = 0xFF; *p++ = 0xE0;                        // jmp rax
    // repoint_call verifies each site really is an E8 reaching 0xB4DB00 before writing, so a wrong
    // address fails that site rather than corrupting code. Report the tally; a short count means a
    // site moved and the gate is only partly owned, which the lapse counter will then show.
    std::string one;
    for (int i = 0; i < REBUILD_CALL_N; i++) {
        char sb[96];
        if (detour::repoint_call(base + REBUILD_CALLS[i], base + REBUILD_FN, thunk, &one)) {
            g_sites_hooked++;
        } else {
            // Name the site AND the reason: a silent 5-of-6 is how the gate stayed half-owned.
            // Also record what is actually at the site, since "not a rel32 call" usually means one
            // of our own hooks patched it first and the order of installs decides the winner.
            const uint8_t* q = (const uint8_t*)(base + REBUILD_CALLS[i]);
            snprintf(sb, sizeof sb, "%s0x%llX(%s; bytes %02X %02X %02X %02X %02X)",
                     g_site_report.empty() ? "" : ", ",
                     (unsigned long long)REBUILD_CALLS[i], one.c_str(),
                     q[0], q[1], q[2], q[3], q[4]);
            g_site_report += sb;
        }
    }
    if (g_sites_hooked == 0) { if (err) *err = "no rebuild call site could be hooked: " + one; return false; }
    if (g_sites_hooked < REBUILD_CALL_N && err)
        *err = "only " + std::to_string(g_sites_hooked) + " of 6 rebuild call sites hooked (" + one + ")";
    if (!force_predicates(err)) return false;
    g_installed = true;
    g_active = true;
    return true;
}

inline void report(std::ofstream& lg) {
    lg << "[G4] direction gates: " << g_fills_rebuild << " rebuilds intercepted, " << g_fills_frame
       << " frame refills, matrices " << g_last_size << " bytes (stride " << g_last_stride << "); "
       << "LAPSES (engine content found in B at a frame poll, sampled before our write) = " << g_lapses
       << ", worst " << g_lapse_worst << "/512 probes; size-growth events = " << g_size_growth
       << "; both out-of-line predicates patched to return true"
       << " [pre-rebuild sample = " << g_zero_before_rebuild
       << " -- NO LONGER EVIDENCE: the frame poll refills B within ~0.5 s, so this is now read"
       << " just after our own memset. The LAPSES counter is the one that can fail.]"
       << "\n";
}

} // namespace gates
