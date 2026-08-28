// TRANSFER TEXT AT END NODES (user report 2026-08-26).
//
// Both sentence builders bail before their formatter call when the node DEFINITION has no outgoing
// entry: the node window's refresh 0x13CFB60 tests the outgoing count at 0x13D0426 (`test ecx,ecx;
// je 0x13D0563`, which blanks the `our_from_this` element), and the outliner builder 0x12BEA50
// tests `count > ordinal` at 0x12BED8E..0x12BED90 and returns an empty SSO string. NOPing either gate
// would run `entry = begin + 0` into 0x1BC0B0, which dereferences a NULL begin unconditionally
// (0x1BC0CD). So the sentence is produced AFTER the original returns, from what the engine already
// computed: the node window keeps its own $VAL$ at view+0x170 (0xB5B4B0's result, stored at
// 0x13D038C before the gate), the outliner's value comes from the same 0xB5B4B0(node, &val, handle)
// (end-node safe: it reads node+0xDC/+0xBC and the record only). The destination is the table's.
//
//   node window: both call sites of 0x13CFB60 (0x814F99 per frame, 0x13CD6AE on open) are
//     repointed; after the original, at an END node with the player's record transferring, the
//     text is built with 0x12BEE80(out, "TRANSFER_IN_TRADE", -, &val, -, where) and set on the
//     element found by gui->vt[0x98](gui, "our_from_this") through 0x152AE10(elem, &str, 0).
//   outliner: the three call sites of 0x12BEA50 (0x12B09F3, 0x12B13CF, 0x144250C) are repointed;
//     when the original leaves `out` empty for a merchant at an END node, the wrapper constructs
//     the sentence over `out` with "TRANSFER_IN_TRADE2" (the empty SSO string owns no buffer).
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
#include "transfertext.h"

namespace endtext {

constexpr uintptr_t FORMATTER = 0x12BEE80;
constexpr uintptr_t NODE_REFRESH = 0x13CFB60;
inline const uintptr_t NODE_REFRESH_CALLS[2] = { 0x814F99, 0x13CD6AE };
constexpr uintptr_t OUTLINER_BUILDER = 0x12BEA50;
inline const uintptr_t OUTLINER_CALLS[3] = { 0x12B09F3, 0x12B13CF, 0x144250C };
constexpr uintptr_t KEY_NODE_WINDOW = 0x1D81198;   // "TRANSFER_IN_TRADE"  (the engine's own literal)
constexpr uintptr_t KEY_OUTLINER    = 0x1D72D10;   // "TRANSFER_IN_TRADE2"
constexpr uintptr_t SET_TEXT = 0x152AE10;          // (elem, const std::string*, 0)
constexpr uintptr_t STR_DTOR = 0x95660;            // ~std::string
constexpr uintptr_t TRANSFER_VALUE = 0xB5B4B0;     // int* (node, int* out, handle) -- x1000
constexpr uintptr_t ENVOY_LOCATION = 0x6FFF90;     // (envoy, handle) -> location object (+0xE8 = node)
constexpr int VIEW_NODE = 0xF8, VIEW_GUI = 0xA0, VIEW_VAL = 0x170, GUI_FIND_TEXT = 0x98;
constexpr int ELEM_HIDE = 0x90, ELEM_VISIBLE = 0xC5;   // element vtable Hide (0x13D0B85 pattern); visible byte
inline uint64_t g_label_hidden = 0;

using FnFmt     = uintptr_t (__fastcall*)(uintptr_t, const char*, uintptr_t, const int*, uintptr_t, const void*);
using FnRefresh = void (__fastcall*)(uintptr_t);
using FnBuild   = uintptr_t (__fastcall*)(uintptr_t, uintptr_t);
using FnFind    = uintptr_t (__fastcall*)(uintptr_t, const char*);
using FnSetText = void (__fastcall*)(uintptr_t, const void*, int);
using FnDtor    = void (__fastcall*)(void*);
using FnValue   = int* (__fastcall*)(uintptr_t, int*, uint64_t);
using FnLoc     = uintptr_t (__fastcall*)(uintptr_t, uint64_t);

inline uint64_t g_node_calls = 0, g_node_set = 0, g_out_calls = 0, g_out_set = 0;
inline bool g_installed = false;

inline uint64_t player_handle() {
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + 0x1E60, 16)) return 0;
    uint8_t mode = livetrade::fb(g + 0x1E66), obs = livetrade::fb(g + 0x1E6F);
    return (mode == 7 && obs != 0) ? livetrade::fq(g + 0x1E68) : livetrade::fq(g + 0x1E60);
}

inline bool is_end_node(uintptr_t node) {
    if (!node || !livetrade::validate_region(node + 0xA8, 8)) return false;
    uintptr_t def = livetrade::fq(node + 0xA8);
    if (!def || !livetrade::validate_region(def + 0x98, 16)) return false;
    return livetrade::fq(def + 0xA0) == livetrade::fq(def + 0x98);
}

// the player's record at `node`, only if it is a transferring merchant
inline uintptr_t transferring_record(uintptr_t node, int pidx) {
    if (!node || pidx < 0 || !livetrade::validate_region(node + 0x18, 16)) return 0;
    uintptr_t rb = livetrade::fq(node + 0x18); int rc = livetrade::fi(node + 0x24);
    if (!rb || pidx >= rc) return 0;
    uintptr_t rec = rb + (uintptr_t)pidx * 0xC0;
    if (!livetrade::validate_region(rec, 0xC0)) return 0;
    if ((livetrade::fi(rec + 0x14) & 0xFFFF) != pidx) return 0;
    if (livetrade::fb(rec + 0xAE) == 0 || livetrade::fb(rec + 0xAC) != 1) return 0;
    return rec;
}

// the table target's display name for the player at `node`, as an MSVC-layout string the formatter can copy
inline std::string g_name_storage; inline transfertext::MsvcStr g_name{};
inline std::string g_memo_key; inline uintptr_t g_memo_node = 0;   // node_by_key memo (the refresh runs every frame; reviewed)
inline uintptr_t g_last_node = 0; inline int g_last_val = -1; inline std::string g_last_tgt;   // write-on-change (namespace scope: reset_world_state clears it)
inline const void* target_name(uintptr_t node, int pidx) {
    std::string tkey;
    uintptr_t def = livetrade::fq(node + 0xA8);
    std::string nkey = livetrade::def_key(def);
    if (nkey.empty()) return nullptr;
    auto it = assign::g_table.find({pidx, nkey});
    if (it == assign::g_table.end()) return nullptr;
    if (it->second != g_memo_key || !g_memo_node) { g_memo_key = it->second; g_memo_node = transfertext::node_by_key(it->second); }
    uintptr_t tnode = g_memo_node;
    std::string name;
    if (!tnode || !outtip::display_name(tnode, &name)) { g_memo_node = 0; return nullptr; }
    g_name_storage = name;
    g_name.ptr = g_name_storage.c_str(); g_name.size = name.size(); g_name.cap = name.size() + 16;
    return &g_name;
}

inline void __fastcall node_refresh_wrapper(uintptr_t view) {
    ((FnRefresh)(livetrade::module_base() + NODE_REFRESH))(view);
    g_node_calls++;
    if (!view || !livetrade::validate_region(view + VIEW_VAL, 4) || !livetrade::validate_region(view + VIEW_NODE, 8) ||
        !livetrade::validate_region(view + VIEW_GUI, 8)) return;
    uintptr_t node = livetrade::fq(view + VIEW_NODE);
    int pidx = flagfix::player_index();
    // THE HOME NODE SHOWS NO "SEND MERCHANT" (user rule): with the collect item gone and the transfer
    // item gated off at home (envoybuttons.h) the list is empty, so the label above it is noise.
    // The refresh Shows it every frame (0x13D0B9D); Hide it right after, the same way the engine
    // hides the cancel button (0x13D0B85: element vt[0x90], visible byte +0xC5).
    if (node && pidx >= 0 && livetrade::validate_region(node + 0x18, 16) && livetrade::validate_region(view + VIEW_GUI, 8)) {
        uintptr_t rb = livetrade::fq(node + 0x18); int rc = livetrade::fi(node + 0x24);
        if (rb && pidx < rc && livetrade::validate_region(rb + (uintptr_t)pidx * 0xC0, 0xC0) &&
            (livetrade::fi(rb + (uintptr_t)pidx * 0xC0 + 0x14) & 0xFFFF) == pidx &&
            livetrade::fb(rb + (uintptr_t)pidx * 0xC0 + 0xAD) != 0) {                     // our home node
            uintptr_t gui = livetrade::fq(view + VIEW_GUI);
            uintptr_t gvt = (gui && livetrade::validate_region(gui, 8)) ? livetrade::fq(gui) : 0;
            if (gvt && livetrade::validate_region(gvt + GUI_FIND_TEXT, 8)) {
                uintptr_t label = ((FnFind)livetrade::fq(gvt + GUI_FIND_TEXT))(gui, "send_merchant_label");
                if (label && livetrade::validate_region(label + ELEM_VISIBLE, 1) && livetrade::fb(label + ELEM_VISIBLE) != 0) {
                    uintptr_t lvt = livetrade::fq(label);
                    if (lvt && livetrade::validate_region(lvt + ELEM_HIDE, 8)) { ((void (__fastcall*)(uintptr_t))livetrade::fq(lvt + ELEM_HIDE))(label); g_label_hidden++; }
                }
            }
        }
    }
    if (!is_end_node(node)) return;                                   // the engine handled every other node
    if (!transferring_record(node, pidx)) return;
    int val = livetrade::fi(view + VIEW_VAL);                         // the engine's own $VAL$ (0x13D038C)
    if (val < 0) return;
    const void* where = target_name(node, pidx);
    if (!where) return;
    uintptr_t gui = livetrade::fq(view + VIEW_GUI);
    if (!gui || !livetrade::validate_region(gui, 8)) return;
    uintptr_t gvt = livetrade::fq(gui);
    if (!gvt || !livetrade::validate_region(gvt + GUI_FIND_TEXT, 8)) return;
    uintptr_t elem = ((FnFind)livetrade::fq(gvt + GUI_FIND_TEXT))(gui, "our_from_this");
    if (!elem) return;
    // write on change only: the refresh's value cache (0x13D037F je 0x13D0589) skips both the build
    // AND the blank while the value is unchanged, so the element keeps what we last wrote (reviewed)
    if (node == g_last_node && val == g_last_val && g_name_storage == g_last_tgt) return;
    g_last_node = node; g_last_val = val; g_last_tgt = g_name_storage;
    alignas(16) char tmp[0x20]; memset(tmp, 0, sizeof tmp);
    *(uint64_t*)(tmp + 0x18) = 15;                                    // a default-constructed MSVC std::string
    ((FnFmt)(livetrade::module_base() + FORMATTER))((uintptr_t)tmp, (const char*)(livetrade::module_base() + KEY_NODE_WINDOW), 0, &val, 0, where);
    ((FnSetText)(livetrade::module_base() + SET_TEXT))(elem, tmp, 0);
    ((FnDtor)(livetrade::module_base() + STR_DTOR))(tmp);
    g_node_set++;
}

inline uintptr_t __fastcall outliner_wrapper(uintptr_t out, uintptr_t envoy) {
    uintptr_t ret = ((FnBuild)(livetrade::module_base() + OUTLINER_BUILDER))(out, envoy);
    g_out_calls++;
    if (!out || !livetrade::validate_region(out, 0x20) || *(uint64_t*)(out + 0x10) != 0 || *(uint64_t*)(out + 0x18) >= 16) return ret;   // the engine wrote text, or owns a buffer
    if (!envoy || !livetrade::validate_region(envoy + 0x18, 1) || livetrade::fb(envoy + 0x18) != 2) return ret;
    uint64_t handle = player_handle();
    if (!handle) return ret;
    if (!livetrade::validate_region(envoy + 0x10, 8) || !livetrade::fq(envoy + 0x10)) return ret;   // in transit: the builder's own branch has no fallback either
    int pidx = (int)(int16_t)(handle >> 32);
    uintptr_t loc = ((FnLoc)(livetrade::module_base() + ENVOY_LOCATION))(envoy, handle);
    if (!loc || !livetrade::validate_region(loc + 0xE8, 8)) return ret;
    uintptr_t node = livetrade::fq(loc + 0xE8);
    if (!is_end_node(node)) return ret;
    if (!transferring_record(node, pidx)) return ret;
    const void* where = target_name(node, pidx);
    if (!where) return ret;
    int val = 0;
    ((FnValue)(livetrade::module_base() + TRANSFER_VALUE))(node, &val, handle);
    if (val < 0) return ret;
    ((FnFmt)(livetrade::module_base() + FORMATTER))(out, (const char*)(livetrade::module_base() + KEY_OUTLINER), 0, &val, 0, where);
    g_out_set++;
    return ret;
}

inline uint8_t* thunk_to(uintptr_t site, void* fn) {
    uint8_t* th = detour::alloc_near(site, 32);
    if (!th) return nullptr;
    uint8_t* p = th;
    *p++ = 0x48; *p++ = 0xB8; uint64_t f = (uint64_t)fn; memcpy(p, &f, 8); p += 8;
    *p++ = 0xFF; *p++ = 0xE0;
    return th;
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    int done = 0;
    for (uintptr_t rva : NODE_REFRESH_CALLS) {
        uintptr_t site = livetrade::module_base() + rva;
        uint8_t* th = thunk_to(site, (void*)&node_refresh_wrapper);
        std::string e;
        if (th && detour::repoint_call(site, livetrade::module_base() + NODE_REFRESH, th, &e)) done++;
        else if (err) *err = "node refresh: " + e;
    }
    for (uintptr_t rva : OUTLINER_CALLS) {
        uintptr_t site = livetrade::module_base() + rva;
        uint8_t* th = thunk_to(site, (void*)&outliner_wrapper);
        std::string e;
        if (th && detour::repoint_call(site, livetrade::module_base() + OUTLINER_BUILDER, th, &e)) done++;
        else if (err) *err = "outliner: " + e;
    }
    if (done != 5) { if (err) *err += " (" + std::to_string(done) + " of 5 sites repointed and LEFT IN PLACE)"; return false; }
    g_installed = true;
    return true;
}

} // namespace endtext
