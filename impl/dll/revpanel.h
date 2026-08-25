// REVERSE-DIRECTION MAP PANELS (spec 1.7, 1.12; tests B3, C1-C5).
//
// On the map, each trade arrow carries a small panel at its start: the ducats moving along that
// link, and a `steer_button` to put a merchant on it. Those panels exist ONLY for a node's
// Phi_w-OUTGOING links, because the builder makes one "LinkView" per entry of def+0x98:
//
//   0x10AFA70  BuildTradeRouteLayer(controller)
//     0x10AF9E0                      clear: destroy every element, end = begin
//     0x10AFB20..0x10AFD1E           for each trade-node DEFINITION
//       0x10AFBE0..0x10AFCF0           for each entry of def+0x98 (0x78 stride)
//         0x10AFC05                      skip entries whose ribbon polyline (+0x58/+0x60) is empty
//         0x10AFC68  type->vtbl[0x50] -> 0x13FFBE0   allocate a LinkView (operator new 0xF8)
//         0x10AFCA7  0x13F6220(lv, mapmodeFlag, srcDef, &outEntry, &scratch)  initialise
//         0x10AFCC4                      push_back into controller+0x4B8
//
// LinkView fields that matter: +0x78 = SOURCE definition, +0x80 = the outgoing ENTRY itself
// (its +0x30 is the target definition), +0x88 = vector<float3> world polyline, +0xC8/+0xCC/+0xD0 =
// the world anchor the panel is drawn at (+0xCC is forced to 19.0f), +0xC0 = pooled panel slot.
//
// So a "reverse" panel is NOT a LinkView with source and target swapped -- that would make the
// tooltip's search at 0x13FC236 (which looks for the source's outgoing entry to the target) fall
// through and read one past the end of node+0x88, and would make the value lookup at 0x1337A0B
// miss and display 0.000. Instead we build a SECOND LinkView over the SAME link, initialised
// identically, and only move its ANCHOR to the far end of the ribbon. Every dereference and both
// searches stay on the path they already take for the forward panel, so the number shown is the
// real flow for that link -- displayed at the node the arrow points INTO, which is where a player
// needs it to steer against Phi_w.
#pragma once
#include <windows.h>
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"
#include "console.h"

namespace revpanel {

constexpr uintptr_t GAME_SINGLETON = 0x233FE78;
constexpr uintptr_t INIT_LINKVIEW  = 0x13F6220;   // (lv, mapmodeFlag, srcDef, &entry, &scratch)
constexpr uintptr_t TYPE_LOOKUP    = 0x14DB870;   // (registry, &std::string name) -> type object
constexpr int VEC_BEGIN = 0x4B8, VEC_END = 0x4C0, VEC_CAP = 0x4C8;
constexpr int CTL_REGISTRY = 0x18;
constexpr int LV_SRCDEF = 0x78, LV_ENTRY = 0x80, LV_POLY = 0x88, LV_ANCHOR = 0xC8;

inline bool g_active = false;
inline uint64_t g_added = 0;
inline int g_logged = 0;
inline std::string g_log;
inline size_t g_last_forward = 0;   // forward count at our last injection

using FnInit  = void*  (__fastcall*)(uintptr_t, int, uintptr_t, uintptr_t, void*);
using FnLookup= uintptr_t (__fastcall*)(uintptr_t, void*);
using FnMake  = uintptr_t (__fastcall*)(uintptr_t);

inline uintptr_t controller() {
    uintptr_t g = livetrade::rq(livetrade::module_base() + GAME_SINGLETON);
    if (!g || !livetrade::validate_region(g + 0x1E00, 8)) return 0;
    uintptr_t map = livetrade::fq(g + 0x1E00);
    if (!map || !livetrade::validate_region(map + 0x330, 8)) return 0;
    uintptr_t a = livetrade::fq(map + 0x330);
    if (!a || !livetrade::validate_region(a + 0x360, 8)) return 0;
    uintptr_t ctl = livetrade::fq(a + 0x360);
    return (ctl && livetrade::validate_region(ctl + VEC_CAP, 8)) ? ctl : 0;
}

// the "traderoute" object type, whose vtbl[0x50] allocates a LinkView
inline uintptr_t linkview_type(uintptr_t ctl) {
    console::Str nm; nm.init(); nm.assign("traderoute");
    auto fn = (FnLookup)(livetrade::module_base() + TYPE_LOOKUP);
    // DEREFERENCE. The engine does `mov rcx, [rdi+0x18]` at 0x10AFC56 -- the registry is the
    // POINTER stored at ctl+0x18, not that address. Passing the address crashed inside the
    // hash lookup, which the breadcrumb pinned to this exact call.
    uintptr_t reg = livetrade::fq(ctl + CTL_REGISTRY);
    if (!reg) { nm.tidy(); return 0; }
    uintptr_t t = fn(reg, nm.raw);
    nm.tidy();
    return t;
}

// Append one extra LinkView per existing one, anchored at the FAR end of its ribbon.
//
// Constraints, all of them load-bearing (each corresponds to a way this crashed):
//  * RENDER THREAD, SAME PHASE. 0x13F6220 tail-calls 0x13F9CE0, which creates a GPU vertex buffer
//    through the renderer singleton at 0x23494B8. Calling it from a tick hook or another thread
//    dies inside the vendor D3D driver with no crash dump.
//  * NEVER replace the vector's buffer. It is a stock MSVC vector and the engine reallocates it
//    with its own deallocator (0xC9CD0 -> 0xC9D60), which for buffers >= 0x1000 reads an alignment
//    header at [_Myfirst - 8]. DLL-owned storage has no such header. Append through the engine's
//    own grow helper instead.
//  * Skip links whose ribbon polyline is empty -- the engine's builder guards this at 0x10AFC16
//    and 0x13F6220 does not validate it.
//  * Build ONLY through the factory: the vector's clear (0x10AF9E0) calls vtbl[0](deleting) on
//    every element, so a hand-rolled object corrupts the heap.
constexpr uintptr_t VEC_GROW = 0xCC220;      // push_back slow path (vec, _Mylast, &value)
constexpr uintptr_t ENGINE_FREE = 0x17394F0; // operator delete(p, n)

using FnGrow = void (__fastcall*)(void*, void*, void**);
using FnFree = void (__fastcall*)(void*, size_t);

inline int add_reverse(std::ofstream* lg) {
    uintptr_t ctl = controller();
    if (!ctl) return -1;
    uintptr_t b = livetrade::fq(ctl + VEC_BEGIN), e = livetrade::fq(ctl + VEC_END);
    if (!b || e < b) return -1;
    size_t n = (size_t)((e - b) / 8);
    if (n == 0 || n > 4096) return 0;
    if (n == g_last_forward * 2) return 0;              // already augmented this rebuild

    uintptr_t type = linkview_type(ctl);
    if (!type || !livetrade::validate_region(type, 8)) return -1;
    uintptr_t tvt = livetrade::fq(type);
    if (!tvt || !livetrade::validate_region(tvt + 0x50, 8)) return -1;
    auto make = (FnMake)livetrade::fq(tvt + 0x50);
    auto init = (FnInit)(livetrade::module_base() + INIT_LINKVIEW);
    auto grow = (FnGrow)(livetrade::module_base() + VEC_GROW);
    auto efree = (FnFree)(livetrade::module_base() + ENGINE_FREE);

    // snapshot the forward views first: the vector moves as we append to it
    std::vector<uintptr_t> fwd((const uintptr_t*)b, (const uintptr_t*)e);
    int added = 0;
    // shared across the pass: the engine appends each accepted anchor and rejects near-duplicates
    struct { void* first; void* last; void* end; } scratch{nullptr, nullptr, nullptr};
    for (uintptr_t lv : fwd) {
        if (!lv || !livetrade::validate_region(lv + LV_ANCHOR + 12, 4)) continue;
        uintptr_t srcdef = livetrade::fq(lv + LV_SRCDEF);
        uintptr_t entry  = livetrade::fq(lv + LV_ENTRY);
        if (!srcdef || !entry || !livetrade::validate_region(entry + 0x60, 8)) continue;
        // the builder's own guard (0x10AFC16): an empty ribbon makes a degenerate LinkView
        uintptr_t p0 = livetrade::fq(entry + 0x58), p1 = livetrade::fq(entry + 0x60);
        if (!p0 || p1 < p0 || (p1 - p0) < 8) continue;

        uintptr_t nlv = make(type);
        if (!nlv) continue;

        // Let VANILLA place it. 0x13F9CE0 walks the ribbon a FIXED arc length from its START,
        // applies a side offset, and REJECTS an anchor that lands too close to one already in the
        // scratch vector (0x13FAB80..0x13FACED). Computing a position ourselves -- mirroring the
        // forward panel's distance -- looks wrong on short or lopsided links (gulf_of_st_lawrence
        // -> north_sea ended up nearly on top of north_sea). So instead REVERSE the ribbon, run the
        // engine's own placement, then put the ribbon back: the anchor is then chosen from the far
        // end by exactly the algorithm that placed the forward panels.
        //
        // The scratch vector is shared across the whole pass so our anchors also de-duplicate
        // against each other, the way vanilla's do within one rebuild.
        {
            uintptr_t qb = livetrade::fq(entry + 0x58), qe = livetrade::fq(entry + 0x60);
            size_t qn = (qb && qe > qb) ? (size_t)((qe - qb) / 8) : 0;
            if (qn >= 2 && livetrade::validate_region(qb, qe - qb)) {
                uint64_t* q = (uint64_t*)qb;                    // float2 points, 8 bytes each
                for (size_t i = 0, j = qn - 1; i < j; i++, j--) std::swap(q[i], q[j]);
                init(nlv, 0, srcdef, entry, &scratch);
                for (size_t i = 0, j = qn - 1; i < j; i++, j--) std::swap(q[i], q[j]);   // restore
            } else {
                init(nlv, 0, srcdef, entry, &scratch);
            }
        }

        // append through the ENGINE's own vector, never by repointing it
        uintptr_t vb = livetrade::fq(ctl + VEC_BEGIN);
        uintptr_t ve = livetrade::fq(ctl + VEC_END);
        uintptr_t vc = livetrade::fq(ctl + VEC_CAP);
        void* val = (void*)nlv;
        if (ve < vc) { *(uintptr_t*)ve = nlv; *(uintptr_t*)(ctl + VEC_END) = ve + 8; }
        else         { grow((void*)(ctl + VEC_BEGIN), (void*)ve, (void**)&val); }
        added++;
    }
    if (scratch.first)
        efree(scratch.first, (size_t)((char*)scratch.end - (char*)scratch.first));
    g_last_forward = fwd.size();
    g_added += added;
    if (lg && g_logged < 6) {
        g_logged++;
        *lg << "  [revpanel] " << fwd.size() << " forward panels, added " << added
            << " reverse ones (anchored at the far end of each ribbon)" << "\n";
    }
    return added;
}


// --- install: run immediately AFTER the engine rebuilds the LinkView vector -------------------
//
// 0x13F6220 tail-calls 0x13F9CE0, which creates a GPU vertex buffer through the renderer singleton
// (0x23494B8) and the controller's device at [ctl+0x18]+0x88. That is safe only on the render
// thread, in the same phase as the engine's own rebuild. The rebuild is 0x10AFA70; calling from
// anywhere else -- a tick hook, a timer, or even the PROLOGUE of the frame function before the
// rebuild has run -- dies inside the vendor D3D code with no crash dump, which is exactly what
// happened. So redirect the rebuild's call sites and append on the way out.
constexpr uintptr_t BUILD_LAYER = 0x10AFA70;
inline const uintptr_t BUILD_CALLS[3] = { 0x10A6F3B, 0x12595E1, 0x12596EE };
inline bool g_installed = false;

using FnBuild = void (__fastcall*)(uintptr_t);

inline void __fastcall build_wrapper(uintptr_t ctl) {
    ((FnBuild)(livetrade::module_base() + BUILD_LAYER))(ctl);      // the engine's own rebuild
    if (!g_active) return;
    std::ofstream lg(g_log, std::ios::app);
    add_reverse(g_log.empty() ? nullptr : &lg);
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    int done = 0;
    for (uintptr_t rva : BUILD_CALLS) {
        uintptr_t site = livetrade::module_base() + rva;
        uint8_t* th = detour::alloc_near(site, 32);
        if (!th) continue;
        uint8_t* p = th;
        *p++ = 0x48; *p++ = 0xB8;                      // mov rax, imm64
        uint64_t fn = (uint64_t)&build_wrapper;
        memcpy(p, &fn, 8); p += 8;
        *p++ = 0xFF; *p++ = 0xE0;                      // jmp rax
        std::string e1;
        if (detour::repoint_call(site, livetrade::module_base() + BUILD_LAYER, th, &e1)) done++;
        else if (err) *err = e1;
    }
    // The TAIL JUMP at 0x125ACA1 (`e9 <rel32>  jmp 0x10AFA70`, after `add rsp,0x20; pop rbx`).
    // It is a jmp, not a call, so the call-site helper skips it -- and switching INTO the trade map
    // mode goes through exactly this path, which is why the wrapper never fired. Redirect it to a
    // thunk that calls the wrapper and returns: a tail jump leaves the ORIGINAL caller's return
    // address at [rsp], so `ret` lands in the right place.
    {
        uintptr_t site = livetrade::module_base() + 0x125ACA1;
        if (livetrade::validate_region(site, 5) && *(uint8_t*)site == 0xE9) {
            int32_t rel = *(int32_t*)(site + 1);
            if (site + 5 + rel == livetrade::module_base() + BUILD_LAYER) {
                uint8_t* th = detour::alloc_near(site, 32);
                if (th) {
                    uint8_t* p = th;
                    *p++ = 0x48; *p++ = 0x83; *p++ = 0xEC; *p++ = 0x28;   // sub rsp,0x28 (align+shadow)
                    *p++ = 0x48; *p++ = 0xB8;                             // mov rax, imm64
                    uint64_t fn = (uint64_t)&build_wrapper;
                    memcpy(p, &fn, 8); p += 8;
                    *p++ = 0xFF; *p++ = 0xD0;                             // call rax
                    *p++ = 0x48; *p++ = 0x83; *p++ = 0xC4; *p++ = 0x28;   // add rsp,0x28
                    *p++ = 0xC3;                                          // ret
                    int64_t disp = (int64_t)((intptr_t)th - (intptr_t)(site + 5));
                    if (disp >= INT32_MIN && disp <= INT32_MAX) {
                        DWORD old = 0;
                        if (VirtualProtect((void*)site, 5, PAGE_EXECUTE_READWRITE, &old)) {
                            *(int32_t*)(site + 1) = (int32_t)disp;
                            VirtualProtect((void*)site, 5, old, &old);
                            FlushInstructionCache(GetCurrentProcess(), (void*)site, 5);
                            done++;
                        }
                    }
                }
            }
        }
    }
    if (!done) { if (err && err->empty()) *err = "no rebuild call site could be redirected"; return false; }
    g_active = true;
    g_installed = true;
    return true;
}


// Is the game currently in the TRADE map mode? The LinkView vector only exists in that mode, and
// every rebuild trigger is guarded by it: *(int*)(*(GS+0x1E00) + 0x2C) == 4 at 0x10AFBF3, and
// mapObj+0x2158 == 4 at the explicit rebuild sites.
inline bool in_trade_mapmode() {
    uintptr_t g = livetrade::rq(livetrade::module_base() + GAME_SINGLETON);
    if (!g || !livetrade::validate_region(g + 0x1E00, 8)) return false;
    uintptr_t map = livetrade::fq(g + 0x1E00);
    if (!map || !livetrade::validate_region(map + 0x2C, 4)) return false;
    return livetrade::fi(map + 0x2C) == 4;
}

// Called from the per-frame hook. The engine rebuilds the vector only when it is EMPTY or on an
// explicit mode/selection refresh, so on a map that was built before we attached the wrapper never
// fires and the extras never appear. Doing it here still satisfies the real constraint -- the frame
// hook is on the render thread, inside the frame, which is where 0x13F9CE0's vertex-buffer work
// must happen. The idempotence guard keeps it to one pass per rebuild.
constexpr uintptr_t CLEAR_LAYER = 0x10AF9E0;   // destroys every LinkView, sets end = begin
using FnClear = void (__fastcall*)(uintptr_t);

inline bool g_asked = false;

inline void frame_tick(std::ofstream* lg) {
    if (!g_active || !in_trade_mapmode()) return;
    uintptr_t ctl = controller();
    if (!ctl) return;
    uintptr_t b = livetrade::fq(ctl + VEC_BEGIN), e = livetrade::fq(ctl + VEC_END);
    if (!b || e < b) return;
    size_t n = (size_t)((e - b) / 8);

    // DO NOT construct LinkViews here. 0x13F6220 tail-calls 0x13F9CE0, which creates a GPU vertex
    // buffer; doing that outside the engine's own rebuild phase kills the process instantly with no
    // crash dump (observed twice). Instead INVALIDATE the layer and let the engine rebuild it: the
    // lazy trigger at 0x10A6F3B fires when the vector is empty, and that call site is already
    // redirected to build_wrapper -- so the append happens inside the engine's rebuild, in exactly
    // the phase it is safe in.
    // Already augmented? nothing to do. Otherwise the engine has rebuilt (zooming, a map-mode or
    // selection refresh all discard our extras), so append again. Calling add_reverse from here is
    // safe -- the earlier crashes were the registry dereference bug, not the render phase.
    if (n > 0 && n != g_last_forward * 2) { add_reverse(lg); return; }
    if (false) {
        ((FnClear)(livetrade::module_base() + CLEAR_LAYER))(ctl);
        g_asked = true;
        if (lg) *lg << "  [revpanel] cleared the layer (" << n
                    << " views); the engine will rebuild and we append on its own path" << "\n";
    }
}

} // namespace revpanel
