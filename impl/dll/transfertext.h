// NODE-WINDOW TRANSFER TEXT FOR TABLE-OWNED PLACEMENTS (spec 1.12; user report 2026-08-26).
//
// The node window's "We transfer X to <node>" line (loc key TRANSFER_IN_TRADE) is built INLINE in
// the window refresh 0x13CFB60: it reads the player's record +0xA8 (0x13D04A4), takes
// def->outgoing[ordinal] (0x13D04AE..), resolves entry+0x30 -> target definition -> node ->
// definition+0x30 (the DISPLAY name, 0x13D0517..0x13D0522), and hands that std::string BY POINTER
// as the sixth argument of the formatter
//
//     0x12BEE80(std::string* out, const char* key, <dead>, const int* val, <dead>, const std::string* where)
//
// at the single call site 0x13D0539. A reverse-end placement is +0xA8 = 0 (syncrec.h), so the
// engine names FORWARD link #0: "we transfer 0.01 to Genoa" while the merchant steers to Sevilla
// (user). The table (assign.h) knows the real target, so the call is repointed to a wrapper that
// substitutes the target's display name whenever the player has a table entry at this node.
//
// The refresh caches the transferred VALUE at window+0x170 (0x13D037F..0x13D038C) and skips the
// whole text build while it is unchanged, so a retarget with the same value would keep the stale
// name on screen: frame() writes 0x80000000 into that cache whenever the table's target for the
// displayed node changes; the engine overwrites it with the true value before using it.
// The formatter COPIES the string it is given (0x12BEF13..), so a DLL-owned buffer is safe.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <string>
#include "detour.h"
#include "livetrade.h"
#include "assign.h"
#include "flagfix.h"
#include "outtip.h"
#include "install.h"
#include "alledges.h"

namespace transfertext {

constexpr uintptr_t FORMATTER = 0x12BEE80;
constexpr uintptr_t CALL_SITE = 0x13D0539;   // inside the node-window refresh 0x13CFB60
constexpr int WIN_NODE = 0xF8;               // CTradeNodeView -> CTradeNode*
constexpr int WIN_VALCACHE = 0x170;          // the write-on-change value cache

using FnFmt = uintptr_t (__fastcall*)(uintptr_t, const char*, void*, const int*, void*, const void*);

// MSVC std::string, heap form: {ptr@0, (unused 8), size@0x10, cap@0x18}; cap >= 16 means ptr is live
struct MsvcStr { const char* ptr; char pad[8]; uint64_t size; uint64_t cap; };

inline std::string g_name_storage;
inline MsvcStr g_name{};
inline uintptr_t g_window = 0;          // the node view, captured when the text is built
inline std::string g_last_target;       // what frame() last saw the table say for the displayed node
inline uint64_t g_calls = 0, g_subst = 0, g_nosub = 0, g_pokes = 0, g_viewmismatch = 0;
inline std::string g_memo_key; inline uintptr_t g_memo_node = 0;   // node_by_key memo (the refresh runs every frame)
inline bool g_installed = false;

// the player's table target (node key) at the node the window shows, if any
inline bool target_for(uintptr_t node, std::string* target_key) {
    if (!node || !livetrade::validate_region(node + 0xA8, 8)) return false;
    uintptr_t def = livetrade::fq(node + 0xA8);
    std::string key = livetrade::def_key(def);
    if (key.empty()) return false;
    int pidx = flagfix::player_index();
    if (pidx < 0) return false;
    auto it = assign::g_table.find({pidx, key});
    if (it == assign::g_table.end()) return false;
    *target_key = it->second;
    return true;
}

inline uintptr_t node_by_key(const std::string& key) {
    for (auto& s : livetrade::read_sim_nodes()) {
        auto it = install::g_id_to_name.find(s.index);
        if (it != install::g_id_to_name.end() && it->second == key) return s.obj;
    }
    return 0;
}

inline uintptr_t __fastcall wrapper(uintptr_t out, const char* key, void* d3, const int* val, void* d5, const void* where) {
    g_calls++;
    const void* w = where;
    uintptr_t window = (uintptr_t)val - WIN_VALCACHE;      // r9 is always &window->0x170 at this site
    if (livetrade::validate_region(window + WIN_NODE, 8)) {
        g_window = window;
        uintptr_t node = livetrade::fq(window + WIN_NODE);
        std::string tkey;
        if (window != alledges::view_ptr()) g_viewmismatch++;
        if (node && target_for(node, &tkey)) {
            if (tkey != g_memo_key || !g_memo_node) { g_memo_key = tkey; g_memo_node = node_by_key(tkey); }
            uintptr_t tnode = g_memo_node;
            std::string name;
            if (tnode && outtip::display_name(tnode, &name)) {
                g_name_storage = name;
                g_name.ptr = g_name_storage.c_str();
                g_name.size = name.size();
                g_name.cap = name.size() + 16;                 // heap form: the callee dereferences ptr
                w = &g_name;
                g_last_target = tkey;                          // latched only on success: a miss buys one retry
                g_subst++;
            } else g_nosub++;
        }
    }
    return ((FnFmt)(livetrade::module_base() + FORMATTER))(out, key, d3, val, d5, w);
}

// per frame: force the text to rebuild when the table's target for the displayed node changes
// The view is RE-DERIVED from the engine every frame (G+0x1228, as alledges does) and only touched
// while its window is up (the refresh's own gate: *(view+0xA0)+0xF5 != 0 at 0x814F90) -- a cached
// pointer outlives the in-game state across a menu exit or a load, and validate_region cannot tell
// a freed block from a live one (reviewed).
inline void frame() {
    uintptr_t view = alledges::view_ptr();
    if (!view) { g_last_target.clear(); g_memo_key.clear(); g_memo_node = 0; return; }   // a load reallocates the nodes: forget the memo
    if (!livetrade::validate_region(view + 0xA0, 8) || !livetrade::validate_region(view + WIN_VALCACHE, 4) ||
        !livetrade::validate_region(view + WIN_NODE, 8)) return;
    uintptr_t w = livetrade::fq(view + 0xA0);
    if (!w || !livetrade::validate_region(w + 0xF5, 1) || livetrade::fb(w + 0xF5) == 0) return;   // window not up
    uintptr_t node = livetrade::fq(view + WIN_NODE);
    if (!node || !livetrade::validate_region(node + 0xA8, 8)) return;
    std::string tkey;
    std::string cur = target_for(node, &tkey) ? tkey : std::string();
    if (cur != g_last_target) {
        g_last_target = cur;
        *(int32_t*)(view + WIN_VALCACHE) = (int32_t)0x80000000;
        g_pokes++;
    }
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    uintptr_t site = livetrade::module_base() + CALL_SITE;
    uint8_t* th = detour::alloc_near(site, 32);
    if (!th) { if (err) *err = "no memory within rel32 range of the call site"; return false; }
    uint8_t* p = th;
    *p++ = 0x48; *p++ = 0xB8;                      // mov rax, imm64
    uint64_t fn = (uint64_t)&wrapper;
    memcpy(p, &fn, 8); p += 8;
    *p++ = 0xFF; *p++ = 0xE0;                      // jmp rax
    if (!detour::repoint_call(site, livetrade::module_base() + FORMATTER, th, err)) return false;
    g_installed = true;
    return true;
}

} // namespace transfertext
