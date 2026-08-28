// OUTLINER / ENVOY-LIST TRANSFER TEXT FOR TABLE-OWNED PLACEMENTS (user report 2026-08-26).
//
// The right-hand outliner's merchant row ("outliner_merchant_entry", 0x12B0630), the unit entry
// (0x12B1260) and the generic envoy list entry (0x1441CE0) all set their sentence through ONE
// builder, 0x12BEA50(std::string* out, Envoy* envoy), which resolves the destination exactly as
// the node window does (record +0xA8 -> def->outgoing[ordinal] -> target def -> node -> def+0x30)
// and calls the formatter at the single site
//
//     0x12BEDFA  call 0x12BEE80(out, "TRANSFER_IN_TRADE2", <dead r8>, &val, <dead [rsp+0x20]>, where)
//
// At that call r13 = the SOURCE CTradeNode* (envoy+0x10 -> +0x38 -> +0xE8, or the country's
// +0x14B0 -> +0xE8), rbx = the PLAYER country handle (the same global the node window reads), and
// both are nonvolatile and untouched since before the branch (verified). The two dead argument
// slots carry them: a thunk moves r13 into r8 and rbx into the fifth slot, then tail-jumps to the
// wrapper, which substitutes the table target's display name for the player at that node. No
// value cache on this path: the entries are rebuilt unconditionally, nothing to invalidate.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <string>
#include "detour.h"
#include "livetrade.h"
#include "assign.h"
#include "outtip.h"
#include "transfertext.h"

namespace outlinertext {

constexpr uintptr_t FORMATTER = 0x12BEE80;
constexpr uintptr_t CALL_SITE = 0x12BEDFA;   // inside 0x12BEA50

using FnFmt = uintptr_t (__fastcall*)(uintptr_t, const char*, uintptr_t, const int*, uint64_t, const void*);

inline std::string g_name_storage;
inline transfertext::MsvcStr g_name{};
inline uint64_t g_calls = 0, g_subst = 0, g_nosub = 0;
inline bool g_installed = false;

inline uintptr_t __fastcall wrapper(uintptr_t out, const char* key, uintptr_t node, const int* val, uint64_t handle, const void* where) {
    g_calls++;
    const void* w = where;
    int country = (int)(int16_t)(handle >> 32);
    if (node && country >= 0 && livetrade::validate_region(node + 0xA8, 8)) {
        uintptr_t def = livetrade::fq(node + 0xA8);
        std::string nkey = livetrade::def_key(def);
        auto it = nkey.empty() ? assign::g_table.end() : assign::g_table.find({country, nkey});
        if (it != assign::g_table.end()) {
            uintptr_t tnode = transfertext::node_by_key(it->second);
            std::string name;
            if (tnode && outtip::display_name(tnode, &name)) {
                g_name_storage = name;
                g_name.ptr = g_name_storage.c_str();
                g_name.size = name.size();
                g_name.cap = name.size() + 16;
                w = &g_name;
                g_subst++;
            } else g_nosub++;
        }
    }
    return ((FnFmt)(livetrade::module_base() + FORMATTER))(out, key, node, val, handle, w);
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    uintptr_t site = livetrade::module_base() + CALL_SITE;
    uint8_t* th = detour::alloc_near(site, 48);
    if (!th) { if (err) *err = "no memory within rel32 range of the call site"; return false; }
    uint8_t* p = th;
    // mov r8, r13                      4D 89 E8          (arg3 <- source node)
    *p++ = 0x4D; *p++ = 0x89; *p++ = 0xE8;
    // mov [rsp+0x28], rbx              48 89 5C 24 28    (arg5 slot: [rsp+0x20] before the call, +8 for the return address)
    *p++ = 0x48; *p++ = 0x89; *p++ = 0x5C; *p++ = 0x24; *p++ = 0x28;
    // mov rax, imm64; jmp rax          (tail-jump: the frame stays byte-identical to a direct call)
    *p++ = 0x48; *p++ = 0xB8;
    uint64_t fn = (uint64_t)&wrapper;
    memcpy(p, &fn, 8); p += 8;
    *p++ = 0xFF; *p++ = 0xE0;
    if (!detour::repoint_call(site, livetrade::module_base() + FORMATTER, th, err)) return false;
    g_installed = true;
    return true;
}

} // namespace outlinertext
