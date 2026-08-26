// A NULL CHECK THE ENGINE FORGOT (found by the crash logger, 2026-08-26).
//
// With relink's ALLOUT step -- every incident link appended to every node's outgoing list so a
// reverse end (and an END node like genua) has a steer ordinal -- the game died on the first AI
// tick at eu4.exe+0x1BAEA1 reading 0xFC4C. That is inside 0x1BA150, the AI light-ship /
// trade-fleet allocator in ai_financial.cpp ("Evaluating trade fleets for:"), the sibling of the
// merchant AI aisilence.h NOPs; its only caller is 0x1B8325, five bytes after the NOPed call.
//
// It makes two passes over node indices 0..N-1. Pass 1 builds a byte mask A[i] ("we own a member
// province here AND have a trader or capital here"). Pass 2, for every masked node, reads OUR
// per-country record: entries = *(node+0x18); rec = entries + 0xC0*idx; rec+0x4C ... with NO null
// check on `entries`. The only node whose record array can be null is the NULL-node singleton
// (0x2462D80, built with an empty country DB) that index 0 / out-of-range resolve to, and once the
// appended entries exist the mask admits it: 0 + 0xC0*336 + 0x4C = 0xFC4C. (Why the mask flips is
// an open residual -- see the two diagnostics below.)
//
// The fix keeps the light-ship AI alive (G3 wants it) and guards the one read. The site
//   0x1BAE71  48 8b 45 68         mov  rax, [rbp+0x68]     ; A
//   0x1BAE75  42 80 3c 30 00      cmp  byte [rax+r14], 0   ; A[i]
//   0x1BAE7A  0f 84 00 10 00 00   je   0x1BBE80            ; skip this node
//   0x1BAE80  49 8b 7d 18         mov  rdi, [r13+0x18]     ; entries (unguarded)
// is 15 bytes ending on an instruction boundary; rax is dead at both targets (0x1BAE80 reloads
// it before use at 0x1BAEA5, 0x1BBE80 overwrites it first thing), r13 = the node is live. The
// site becomes `jmp [rip+0]; dq stub; nop` and the stub is:
//   mov rax,[rbp+0x68] ; cmp byte [rax+r14],0 ; je skip
//   mov rax,[r13+0x18] ; test rax,rax ; je skip
//   jmp [rip+0] -> 0x1BAE80
//   skip: jmp [rip+0] -> 0x1BBE80
// -- the original test plus the missing one, no other behaviour change. Not installed unless
// ALLOUT is on: without appended entries the walk never reaches a null array (measured: weeks).
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>
#include "livetrade.h"
#include "detour.h"

namespace aiguard {

constexpr uintptr_t SITE      = 0x1BAE71;
constexpr uintptr_t CONTINUE  = 0x1BAE80;
constexpr uintptr_t SKIP      = 0x1BBE80;
constexpr uintptr_t NULL_NODE = 0x2462D80;   // CTradeNode singleton returned by 0xB60B80
constexpr uintptr_t NULL_DEF  = 0x2462C90;   // its definition (0xB60A80)
inline bool g_installed = false;
inline uint8_t* g_stub = nullptr;

inline bool install(std::string* err, std::ofstream* lg) {
    if (g_installed) return true;
    uintptr_t base = livetrade::module_base();
    uintptr_t site = base + SITE;
    const uint8_t expected[15] = {0x48, 0x8b, 0x45, 0x68, 0x42, 0x80, 0x3c, 0x30, 0x00, 0x0f, 0x84, 0x00, 0x10, 0x00, 0x00};
    if (!livetrade::validate_region(site, 16) || memcmp((void*)site, expected, 15) != 0) { if (err) *err = "site bytes differ at 0x1BAE71"; return false; }
    // the stub
    std::vector<uint8_t> st = {
        0x48, 0x8b, 0x45, 0x68,                    // mov rax,[rbp+0x68]
        0x42, 0x80, 0x3c, 0x30, 0x00,              // cmp byte [rax+r14],0
        0x74, 0x17,                                // je skip (+23)
        0x49, 0x8b, 0x45, 0x18,                    // mov rax,[r13+0x18]
        0x48, 0x85, 0xc0,                          // test rax,rax
        0x74, 0x0e,                                // je skip (+14)
        0xff, 0x25, 0x00, 0x00, 0x00, 0x00,        // jmp [rip+0]
        0, 0, 0, 0, 0, 0, 0, 0,                    // -> CONTINUE
        0xff, 0x25, 0x00, 0x00, 0x00, 0x00,        // skip: jmp [rip+0]
        0, 0, 0, 0, 0, 0, 0, 0                     // -> SKIP
    };
    uint64_t cont = base + CONTINUE, skip = base + SKIP;
    memcpy(&st[26], &cont, 8);
    memcpy(&st[40], &skip, 8);
    g_stub = detour::alloc_exec(st.size());
    if (!g_stub) { if (err) *err = "stub alloc failed"; return false; }
    memcpy(g_stub, st.data(), st.size());
    // the patch: jmp [rip+0]; dq stub; nop
    uint8_t patch[15] = {0xff, 0x25, 0x00, 0x00, 0x00, 0x00, 0, 0, 0, 0, 0, 0, 0, 0, 0x90};
    uint64_t stub_addr = (uint64_t)g_stub;
    memcpy(&patch[6], &stub_addr, 8);
    detour::Freeze fz(site, site + 15);            // no thread inside the 15 bytes while they change
    if (!fz.ok) { if (err) *err = "freeze failed: " + fz.why; return false; }
    DWORD old = 0;
    if (!VirtualProtect((void*)site, 15, PAGE_EXECUTE_READWRITE, &old)) { if (err) *err = "VirtualProtect failed"; return false; }
    memcpy((void*)site, patch, 15);
    VirtualProtect((void*)site, 15, old, &old);
    FlushInstructionCache(GetCurrentProcess(), (void*)site, 15);
    g_installed = true;
    if (lg) {
        uintptr_t nn = base + NULL_NODE, nd = base + NULL_DEF;
        *lg << "  [aiguard] light-ship AI null-record guard installed at 0x1BAE71 (stub 0x" << std::hex << (uint64_t)g_stub << std::dec << ")"
            << "; NULL node +0x18=0x" << std::hex << (livetrade::validate_region(nn + 0x18, 8) ? livetrade::fq(nn + 0x18) : (uintptr_t)0xEEEE)
            << " +0xA8=0x" << (livetrade::validate_region(nn + 0xA8, 8) ? livetrade::fq(nn + 0xA8) : (uintptr_t)0xEEEE)
            << " NULL def +0xE6=" << std::dec << (livetrade::validate_region(nd + 0xE6, 1) ? (int)livetrade::fb(nd + 0xE6) : -1) << (char)10;
    }
    return true;
}

// diagnostic for the residual: which live nodes carry a null record array?
inline int null_record_nodes(const std::vector<livetrade::SimNode>& sim, std::ofstream* lg) {
    int n = 0; std::string names;
    for (auto& s : sim)
        if (s.obj && livetrade::validate_region(s.obj + 0x18, 8) && livetrade::fq(s.obj + 0x18) == 0) { n++; if (names.size() < 200) names += s.name + " "; }
    if (lg && n) *lg << "  [aiguard] " << n << " live nodes with a NULL record array: " << names << (char)10;
    return n;
}

} // namespace aiguard
