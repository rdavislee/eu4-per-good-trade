// CARAVAN POWER NEEDS ACTUAL STEERING (spec 1.7, 3.11; test C5).
//
// Spec 1.7 adds one condition to vanilla: "Caravan power requires the merchant to be steering at
// least one good on that link; assignment alone does not qualify." Vanilla grants it on the
// merchant_present_inland / merchant_steering_to_inland flags alone, which under a per-good model
// would pay a merchant that happens to sit on a link carrying none of its goods.
//
// The grant site (sim, not UI):
//   0xB53C92  mov  rcx, [r14+0xA8]     ; r14 = CTradeNode, +0xA8 = its definition
//   0xB53C99  call 0xB6A090            ; the inland test
//   0xB53CA0  je   0xB541B9            ; not inland -> no grant
//   0xB53CC1  mov  rcx, [rdi+rax]      ; the country (rdi = tagIndex*8)
//   0xB53CC5  call 0x3EDB90            ; ComputeCaravanPower(country, &out) -> returns &out
//   0xB53CCA  mov  esi, [rax]
//   0xB53CD0  je   0xB541B9            ; zero -> no grant
//
// So the call site already holds both halves of the condition -- the node in r14 and the country
// in rdi -- and the engine ALREADY skips the grant when the computed power is zero. That makes
// the clean intervention a call-site redirect: point the 5-byte rel32 at our own wrapper, let the
// original compute the value, then zero it when the model says this country steers nothing at
// this node. No instruction relocation, no new branch, and vanilla's own "zero means no grant"
// path does the rest.
#pragma once
#include <windows.h>
#include <cstdint>
#include <map>
#include <set>
#include <string>
#include "livetrade.h"

namespace caravan {

constexpr uintptr_t CALL_SITE = 0xB53CC5;    // call 0x3EDB90 inside the grant
constexpr uintptr_t COMPUTE   = 0x3EDB90;    // ComputeCaravanPower(country, int* out) -> out

// (country tag index, node index) pairs that DO steer at least one good this tick. Rebuilt by the
// tick hook from the routing model; a pair absent from here gets no caravan power.
inline std::set<std::pair<int, int>> g_steering;
inline bool g_active = false;
inline uint64_t g_granted = 0, g_denied = 0;

using FnCompute = int* (__fastcall*)(void*, int*);

// The wrapper. r8 and r9 are supplied by the thunk below: the node and tagIndex*8 that the call
// site happens to be holding.
inline int* __fastcall wrapper(void* country, int* out, void* node, uintptr_t tagidx8) {
    FnCompute orig = (FnCompute)(livetrade::module_base() + COMPUTE);
    int* r = orig(country, out);
    if (!g_active || !r) return r;
    int node_idx = -1;
    if (node && livetrade::validate_region((uintptr_t)node + 0x120, 4))
        node_idx = livetrade::fi((uintptr_t)node + 0x120);
    int tag = (int)(tagidx8 / 8);
    if (node_idx >= 0 && !g_steering.count({tag, node_idx})) {
        *r = 0;                 // spec 1.7: assignment alone does not qualify
        g_denied++;
    } else {
        g_granted++;
    }
    return r;
}

// thunk: forward the two extra registers the call site is holding, then tail-jump to the wrapper
inline uint8_t* g_thunk = nullptr;
inline bool g_installed = false;

inline bool install(std::string* err) {
    if (g_installed) return true;
    uintptr_t site = livetrade::module_base() + CALL_SITE;
    // verify the original bytes: e8 <rel32> reaching COMPUTE (spec 2.5 -- a patch is a new binary)
    if (!livetrade::validate_region(site, 5)) { if (err) *err = "call site unreadable"; return false; }
    if (*(uint8_t*)site != 0xE8) { if (err) *err = "not a rel32 call"; return false; }
    int32_t rel = *(int32_t*)(site + 1);
    uintptr_t target = site + 5 + rel;
    if (target != livetrade::module_base() + COMPUTE) {
        if (err) *err = "call does not reach ComputeCaravanPower (patched binary?)";
        return false;
    }
    g_thunk = (uint8_t*)VirtualAlloc(nullptr, 64, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!g_thunk) { if (err) *err = "thunk alloc failed"; return false; }
    uint8_t* p = g_thunk;
    *p++ = 0x4D; *p++ = 0x89; *p++ = 0xF0;              // mov r8, r14      (the node)
    *p++ = 0x49; *p++ = 0x89; *p++ = 0xF9;              // mov r9, rdi      (tagIndex*8)
    *p++ = 0x48; *p++ = 0xB8;                            // mov rax, imm64
    uint64_t fn = (uint64_t)&wrapper;
    memcpy(p, &fn, 8); p += 8;
    *p++ = 0xFF; *p++ = 0xE0;                            // jmp rax
    // repoint the call
    int32_t newrel = (int32_t)((intptr_t)g_thunk - (intptr_t)(site + 5));
    DWORD old = 0;
    if (!VirtualProtect((void*)site, 5, PAGE_EXECUTE_READWRITE, &old)) {
        if (err) *err = "VirtualProtect failed"; return false;
    }
    *(int32_t*)(site + 1) = newrel;
    VirtualProtect((void*)site, 5, old, &old);
    FlushInstructionCache(GetCurrentProcess(), (void*)site, 5);
    g_installed = true;
    g_active = true;
    return true;
}

} // namespace caravan
