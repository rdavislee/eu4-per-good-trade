// OUTGOING TOOLTIP ATTRIBUTION FOR REVERSE-Phi_w DESTINATIONS (spec 1.12; user request 2026-08-26).
//
// The node window's "Outgoing" hover and the ledger's trade page build their per-destination
// lines in 0xB56480(CTradeNode*, std::string* out): one line per entry of the DEFINITION's
// outgoing vector (def+0x98, 0x78 stride; the target node is resolved entry+0x30 -> def+0xDC ->
// province+0xE8), each
//
//     "\xA7W  => " + <target def+0x30 display name> + ": \xA7Y" + value + "\xA4\xA7W\n"
//
// with value = steer_permille[k] (node+0x88) x node+0xC0 / 1000 in ducats x1000, printed as
// integer part "." two digits, TRUNCATED (0xB5653F..0xB565F5; the three constants are at
// 0x1CE8D20 / 0x1C5A8B8 / 0x1CE8C64, read from the binary). A node's outflow along a link the
// definition does not list -- every reverse-Phi_w edge, and ALL of an END node's edges -- is
// inside the header (+0xC0 == +0xBC) but attributed to nothing: "genoa has some ducats outgoing
// but doesn't attribute them to anywhere" (user).
//
// Fix: both call sites (0x13D3E72 node window, 0x11B019D ledger; verified `call 0xB56480`) are
// repointed to a wrapper that runs the original and then appends one line per reverse
// destination in the identical format, through the engine's own std::string::append
// (0x932F0(std::string*, const char*, size_t) -- MSVC layout {buf/ptr@0, size@0x10, cap@0x18}).
// The per-node table is rebuilt every tick by outlinks::install, which now normalises the
// forward permilles over ALL incident away-flows, so forward + reverse lines sum to the header.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <map>
#include <mutex>
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"

namespace outtip {

constexpr uintptr_t BUILDER = 0xB56480;
constexpr uintptr_t APPEND  = 0x932F0;
inline const uintptr_t CALLS[2] = { 0x13D3E72, 0x11B019D };

struct Line { uintptr_t dst_node; int permille; };
inline std::mutex g_mx;
inline std::map<uintptr_t, std::vector<Line>> g_lines;   // node -> reverse destinations (this tick)
inline uint64_t g_calls = 0, g_appended = 0, g_noname = 0;
inline bool g_installed = false;

inline void set_lines(std::map<uintptr_t, std::vector<Line>>& m) {
    std::lock_guard<std::mutex> lk(g_mx);
    g_lines.swap(m);
}

// The engine's own display name for a node: the std::string at def+0x30 (size at +0x40, heap
// pointer when cap at +0x48 >= 16) -- exactly what 0xB5661C..0xB56681 appends.
inline bool display_name(uintptr_t node, std::string* out) {
    if (!node || !livetrade::validate_region(node + 0xA8, 8)) return false;
    uintptr_t def = livetrade::fq(node + 0xA8);
    if (!def || !livetrade::validate_region(def + 0x30, 0x20)) return false;
    uint64_t sz = *(uint64_t*)(def + 0x40), cap = *(uint64_t*)(def + 0x48);
    if (sz == 0 || sz > 200 || cap < sz) return false;
    const char* p = (const char*)(def + 0x30);
    if (cap >= 16) {
        uintptr_t hp = *(uintptr_t*)(def + 0x30);
        if (!hp || !livetrade::validate_region(hp, sz + 1)) return false;
        p = (const char*)hp;
    }
    out->assign(p, (size_t)sz);
    return true;
}

using FnBuild  = uintptr_t (__fastcall*)(uintptr_t, uintptr_t);   // returns `out` (0xB56846: mov rax, rdi)
using FnAppend = void* (__fastcall*)(uintptr_t, const char*, size_t);

// RETURNS WHAT THE ENGINE RETURNS. The builder hands its `out` pointer back in rax and BOTH callers
// use it at once (0x13D3E78 `mov r8, rax`; 0x11B01A2 `mov rdx, rax`) -- a void wrapper left rax
// as whatever the map lookup put there, and the node window died in 0x94910 on the first hover.
inline uintptr_t __fastcall wrapper(uintptr_t node, uintptr_t out) {
    uintptr_t ret = ((FnBuild)(livetrade::module_base() + BUILDER))(node, out);   // the engine's own lines
    g_calls++;
    std::vector<Line> lines;
    {
        std::lock_guard<std::mutex> lk(g_mx);
        auto it = g_lines.find(node);
        if (it != g_lines.end()) lines = it->second;
    }
    if (lines.empty() || !out || !livetrade::validate_region(node + 0xC0, 4)) return ret;
    int64_t c0 = livetrade::fi(node + 0xC0);                          // outgoing, x1000
    auto app = (FnAppend)(livetrade::module_base() + APPEND);
    static const char PFX[7] = { (char)0xA7, 'W', ' ', ' ', '=', '>', ' ' };
    static const char SEP[4] = { ':', ' ', (char)0xA7, 'Y' };
    static const char SFX[4] = { (char)0xA4, (char)0xA7, 'W', (char)10 };
    for (auto& L : lines) {
        std::string name;
        if (!display_name(L.dst_node, &name)) { g_noname++; continue; }
        int64_t v = (int64_t)L.permille * c0 / 1000;                  // ducats x1000 (0xB5655C..0xB5656D)
        if (v < 0) v = 0;
        char num[48];
        snprintf(num, sizeof num, "%lld.%02lld", (long long)(v / 1000), (long long)((v % 1000) / 10));
        std::string s;
        s.append(PFX, 7); s += name; s.append(SEP, 4); s += num; s.append(SFX, 4);
        app(out, s.data(), s.size());
        g_appended++;
    }
    return ret;
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    int done = 0;
    for (uintptr_t rva : CALLS) {
        uintptr_t site = livetrade::module_base() + rva;
        uint8_t* th = detour::alloc_near(site, 32);
        if (!th) { if (err) *err = "no memory within rel32 range of the call site"; continue; }
        uint8_t* p = th;
        *p++ = 0x48; *p++ = 0xB8;                      // mov rax, imm64
        uint64_t fn = (uint64_t)&wrapper;
        memcpy(p, &fn, 8); p += 8;
        *p++ = 0xFF; *p++ = 0xE0;                      // jmp rax  (entered exactly as the callee would be)
        std::string e1;
        if (detour::repoint_call(site, livetrade::module_base() + BUILDER, th, &e1)) done++;
        else if (err) *err = e1;
    }
    if (done != 2) { if (err && err->empty()) *err = "only one call site repointed"; return false; }   // both or neither (reviewed)
    g_installed = true;
    return true;
}

} // namespace outtip
