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

constexpr uintptr_t REBUILD_CALL = 0xB4BD0A;   // call 0xB4DB00, rcx = manager
constexpr uintptr_t REBUILD_FN   = 0xB4DB00;
constexpr uintptr_t GATE_TREASURE = 0x3E1D30;  // matrix A predicate
constexpr uintptr_t GATE_UPSTREAM = 0xB4E020;  // matrix B predicate (IsNodeUpstreamOfCountry)

inline bool g_active = false;
inline uint64_t g_fills = 0;
inline int g_last_size = 0, g_last_stride = 0;
inline int g_zero_after_fill = -1;    // proof the fill landed: bytes still 0 (must be 0)

using FnRebuild = void(__fastcall*)(uintptr_t);

inline void __fastcall rebuild_wrapper(uintptr_t mgr) {
    ((FnRebuild)(livetrade::module_base() + REBUILD_FN))(mgr);
    if (!g_active || !mgr) return;
    if (!livetrade::validate_region(mgr + 0x24, 0x80)) return;
    int size = *(int32_t*)(mgr + 0xA0);
    g_last_stride = *(int32_t*)(mgr + 0x24);
    g_last_size = size;
    if (size <= 0 || size > (1 << 26)) return;
    int zero = 0;
    for (int k = 0; k < 3; k++) {
        uintptr_t m = *(uintptr_t*)(mgr + 0x88 + 8 * k);
        if (!m || !livetrade::validate_region(m, (size_t)size)) continue;
        memset((void*)m, 1, (size_t)size);
        // A check only ever seen passing is an assertion, not a measurement: count the bytes that
        // are still zero after the fill. This must read 0, and it is a real read of the engine's
        // own table, not of our intent.
        const uint8_t* p = (const uint8_t*)m;
        for (int i = 0; i < size; i += (size > 4096 ? size / 512 : 1)) if (!p[i]) zero++;
    }
    g_zero_after_fill = zero;
    g_fills++;
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
    uintptr_t site = livetrade::module_base() + REBUILD_CALL;
    uint8_t* thunk = detour::alloc_near(site, 32);
    if (!thunk) { if (err) *err = "gate thunk alloc failed"; return false; }
    uint8_t* p = thunk;
    *p++ = 0x48; *p++ = 0xB8;                        // mov rax, imm64
    uint64_t fn = (uint64_t)&rebuild_wrapper;
    memcpy(p, &fn, 8); p += 8;
    *p++ = 0xFF; *p++ = 0xE0;                        // jmp rax
    if (!detour::repoint_call(site, livetrade::module_base() + REBUILD_FN, thunk, err)) return false;
    if (!force_predicates(err)) return false;
    g_installed = true;
    g_active = true;
    return true;
}

inline void report(std::ofstream& lg) {
    lg << "[G4] direction gates: " << g_fills << " rebuilds intercepted, matrices "
       << g_last_size << " bytes (stride " << g_last_stride << "), bytes still zero after fill = "
       << g_zero_after_fill << " (must be 0); both out-of-line predicates patched to return true"
       << "\n";
}

} // namespace gates
