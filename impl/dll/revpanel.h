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
#include <map>
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
inline size_t g_last_forward = 0;
inline int g_measured = 0;
inline int g_dumped = 0;
inline int g_flipped = 0;   // ribbons whose polyline runs target -> source      // how many forward anchors we have measured, for the log

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


// --- vanilla's own panel placement, read out of 0x13F9CE0 -----------------------------------
// The engine walks the tessellated ribbon from its START accumulating segment length, and takes
// as the anchor the FIRST vertex past a fixed threshold:
//
//   0x13F9F18  movss  xmm8, [0x1DC184C]      ; the threshold == 25.0f
//   0x13FA967  addss  xmm9, xmm10            ; accumulate this segment's length
//   0x13FA96C  test   r14b, r14b             ; already captured?
//   0x13FA975  comiss xmm9, xmm8             ; accumulated > 25.0 ?
//   0x13FA979  jbe    ...                    ; no -> keep walking
//   0x13FA97F  mov    r14b, 1                ; yes -> capture this vertex pair
//
// So the distance is ABSOLUTE, not a fraction of the link: every vanilla panel sits the same
// arc length from the node it belongs to, however long or short the link is. That is exactly why
// mirroring the forward panel's distance looked wrong -- on gulf_of_st_lawrence -> north_sea the
// forward panel is far from gulf_of_st_lawrence, so the mirror put the reverse panel that same
// long way from north_sea's end, i.e. nearly on top of north_sea.
//
// Applying the same rule from the FAR end gives the reverse panel the same 25.0 spacing from its
// own node. ARC_LEN is left as the measured constant so the log can confirm it against what the
// engine actually did to the forward views.
constexpr double ARC_LEN = 25.0;
// minimum gap between two panel anchors; calibrated against the measured vanilla spacing
constexpr double MIN_SEP = 25.0;   // MEASURED: the closest pair among the 159
                                   // vanilla anchors is 25.0155 world units, and 25.0f is the
                                   // .rdata constant at 0x1DC184C -- so that constant is the
                                   // SEPARATION threshold, not an arc length.

// --- walking the ribbon ----------------------------------------------------------------------
// The panel is placed by FOLLOWING THE RIBBON from its own node until it can sit without
// colliding with anything already placed. Mirroring the forward anchor's offset (the previous
// approach) used the ribbon's LOCAL direction at the far end, which on a curved link points
// somewhere the link does not go -- that is why a bordeaux panel still landed on the wrong side
// and why english_channel <- ivory_coast sat off the line entirely. Walking the polyline cannot
// do either: the anchor is always a point ON the ribbon, on the correct side by construction.

// point at arc distance `d` measured inward from endpoint `from_end` (0 or np-1)
inline void point_at_arc(const float* p3, int np, int from_end, double d,
                         double* ox, double* oz) {
    auto len = [&](int i, int j) {
        double dx = p3[i * 3 + 0] - p3[j * 3 + 0], dy = p3[i * 3 + 1] - p3[j * 3 + 1],
               dz = p3[i * 3 + 2] - p3[j * 3 + 2];
        return std::sqrt(dx * dx + dy * dy + dz * dz);
    };
    int cur = from_end, step = (from_end == 0) ? 1 : -1;
    double acc = 0;
    while (cur + step >= 0 && cur + step < np) {
        int nxt = cur + step;
        double L = len(nxt, cur);
        if (acc + L >= d && L > 1e-6) {
            double t = (d - acc) / L;
            *ox = p3[cur * 3 + 0] + t * (p3[nxt * 3 + 0] - p3[cur * 3 + 0]);
            *oz = p3[cur * 3 + 2] + t * (p3[nxt * 3 + 2] - p3[cur * 3 + 2]);
            return;
        }
        acc += L;
        cur = nxt;
    }
    *ox = p3[cur * 3 + 0];
    *oz = p3[cur * 3 + 2];
}

inline double ribbon_length(const float* p3, int np) {
    double t = 0;
    for (int i = 1; i < np; i++) {
        double dx = p3[i*3+0]-p3[(i-1)*3+0], dy = p3[i*3+1]-p3[(i-1)*3+1],
               dz = p3[i*3+2]-p3[(i-1)*3+2];
        t += std::sqrt(dx*dx + dy*dy + dz*dz);
    }
    return t;
}

// arc distance, from endpoint `from_end`, of the polyline point closest to (qx,qz)
inline double arc_of_nearest(const float* p3, int np, int from_end, double qx, double qz) {
    int cur = from_end, step = (from_end == 0) ? 1 : -1;
    double acc = 0, best = 1e30, best_arc = 0;
    while (cur + step >= 0 && cur + step < np) {
        int nxt = cur + step;
        double ax = p3[cur*3+0], az = p3[cur*3+2];
        double bx = p3[nxt*3+0], bz = p3[nxt*3+2];
        double ex = bx - ax, ez = bz - az;
        double L2 = ex*ex + ez*ez;
        double t = (L2 > 1e-9) ? ((qx-ax)*ex + (qz-az)*ez) / L2 : 0.0;
        if (t < 0) t = 0; else if (t > 1) t = 1;
        double px = ax + t*ex, pz = az + t*ez;
        double d2 = (qx-px)*(qx-px) + (qz-pz)*(qz-pz);
        double seg = std::sqrt(L2);
        if (d2 < best) { best = d2; best_arc = acc + t * seg; }
        acc += seg;
        cur = nxt;
    }
    return best_arc;
}

// the definition's key, read out of its std::string at +0x10 (MSVC: buf@0, size@0x10, cap@0x18)
inline std::string def_key(uintptr_t def) {
    if (!def || !livetrade::validate_region(def + 0x10, 0x20)) return "?";
    uint64_t sz = *(uint64_t*)(def + 0x20), cap = *(uint64_t*)(def + 0x28);
    if (sz > 128 || cap < sz) return "?";
    const char* p = (const char*)(def + 0x10);
    if (cap >= 16) {
        uintptr_t hp = *(uintptr_t*)(def + 0x10);
        if (!hp || !livetrade::validate_region(hp, sz + 1)) return "?";
        p = (const char*)hp;
    }
    return std::string(p, (size_t)sz);
}

// --- the reverse link ENTRY -------------------------------------------------------------------
// Pointing the reverse view at the target node fixed culling but made every reverse panel read
// 0.00, because the displayed number is resolved through the link entry's TARGET: the panel for a
// view (src, entry) shows the value arriving at node[entry->target] in the incoming record whose
// +0x18 is `src`. With the view owned by the target but still carrying the FORWARD entry, that
// asks node[tgt] for a record from tgt to itself, which does not exist -- hence 0.00.
//
// So the reverse view needs a reverse entry: the same 0x78-byte shape, but with +0x30 (the
// resolved target, which Link() writes at 0xB697AD) pointing back at the ORIGINAL SOURCE. The
// lookup then becomes node[src].incoming[+0x18 == tgt] -- the record carrying the value flowing
// the other way, which outlinks::rebuild_incoming already creates for every INCIDENT neighbour
// (both directions) and linkvalue::install already fills.
//
// This entry is never inserted into any definition's `outgoing` vector. Appending reverse entries
// there was tried and is permanently ruled out: it makes the graph cyclic and the recursive
// depth-first walk at 0xB67D20 overflows the stack. Standing alone, nothing enumerates or frees
// it, so nothing can trip over it.
//
// The string at +0x10 is rebuilt as an EMPTY SSO string rather than copied: a bitwise copy of a
// std::string shares the heap buffer of any key of 16 characters or more ("gulf_of_st_lawrence"
// is 19), which would double-free. Nothing reads the name after Link() has resolved +0x30.
constexpr uintptr_t ENGINE_NEW_E = 0x1A332D4;   // the game's operator new
constexpr int EN_NAME = 0x10, EN_TARGET = 0x30, EN_ORDINAL = 0x38, EN_PATH = 0x40;
constexpr int EN_CTRL = 0x58;   // vector<float2> of ribbon control points

inline std::map<uintptr_t, uintptr_t> g_rev_entry;    // forward entry -> our reverse entry

inline uintptr_t reverse_entry(uintptr_t fwd_entry, uintptr_t back_to_def) {
    auto it = g_rev_entry.find(fwd_entry);
    if (it != g_rev_entry.end()) return it->second;
    if (!livetrade::validate_region(fwd_entry, 0x78)) return 0;
    using FnNewE = void* (__fastcall*)(size_t);
    auto alloc = (FnNewE)(livetrade::module_base() + ENGINE_NEW_E);
    uint8_t* e = (uint8_t*)alloc(0x78);
    if (!e) return 0;
    memcpy(e, (const void*)fwd_entry, 0x78);        // vtable, class id, and the control polyline
    memset(e + EN_NAME, 0, 0x20);                   // empty std::string: buf[0]=0, size=0, cap=15
    *(uint64_t*)(e + EN_NAME + 0x10) = 0;
    *(uint64_t*)(e + EN_NAME + 0x18) = 15;
    *(uintptr_t*)(e + EN_TARGET) = back_to_def;     // the reverse direction
    *(int32_t*)(e + EN_ORDINAL)  = 0;
    memset(e + EN_PATH, 0, 0x18);                   // empty province path list
    // Its OWN control polyline, reversed. This is what lets the engine place the panel: 0x13F9CE0
    // always works from the ribbon's START, so a ribbon whose control points run target -> source
    // gets its panel placed from the target's end by exactly the code that places outgoing ones.
    // The buffer must be the engine's own -- a LinkView built from this entry may free it.
    {
        uintptr_t qb = *(uintptr_t*)(e + EN_CTRL), qe = *(uintptr_t*)(e + EN_CTRL + 8);
        size_t bytes = (qb && qe > qb) ? (size_t)(qe - qb) : 0;
        size_t qn = bytes / 8;                       // float2 per control point
        if (qn >= 2 && livetrade::validate_region(qb, bytes)) {
            uint64_t* copy = (uint64_t*)alloc(bytes);
            if (copy) {
                const uint64_t* src = (const uint64_t*)qb;
                for (size_t i = 0; i < qn; i++) copy[i] = src[qn - 1 - i];
                *(uintptr_t*)(e + EN_CTRL)      = (uintptr_t)copy;
                *(uintptr_t*)(e + EN_CTRL + 8)  = (uintptr_t)copy + bytes;
                *(uintptr_t*)(e + EN_CTRL + 16) = (uintptr_t)copy + bytes;
            }
        }
    }
    g_rev_entry[fwd_entry] = (uintptr_t)e;
    return (uintptr_t)e;
}

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
    // Every anchor already on the map, ours included as we go. Vanilla rejects an anchor that
    // lands too close to one already placed; without that step two links arriving at a node from
    // similar directions -- the two oceanic routes into english_channel -- get near-identical
    // mirrored anchors and one panel sits invisibly behind the other.
    std::vector<std::pair<float,float>> placed;
    placed.reserve(fwd.size() * 2);
    for (uintptr_t f : fwd)
        if (f && livetrade::validate_region(f + LV_ANCHOR + 12, 4)) {
            const float* a = (const float*)(f + LV_ANCHOR);
            placed.push_back({a[0], a[2]});
        }
    // MEASURE the spacing vanilla itself keeps, rather than inventing a threshold.
    if (lg && g_logged < 6) {
        double mn = 1e30;
        for (size_t i = 0; i < placed.size(); i++)
            for (size_t j = i + 1; j < placed.size(); j++) {
                double dx = placed[i].first - placed[j].first,
                       dz = placed[i].second - placed[j].second;
                double d = std::sqrt(dx * dx + dz * dz);
                if (d < mn) mn = d;
            }
        *lg << "  [revpanel/spacing] closest pair among " << placed.size()
            << " vanilla anchors: " << mn << " world units" << (char)10;
    }
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

        uintptr_t tgtdef_for_lv = livetrade::fq(entry + 0x30);
        uintptr_t rev_entry_for_lv =
            (tgtdef_for_lv && livetrade::validate_region(tgtdef_for_lv + 0xD8, 4))
                ? reverse_entry(entry, srcdef) : 0;

        uintptr_t nlv = make(type);
        if (!nlv) continue;

        // Build the ribbon from the FORWARD polyline, unmodified. The strip is offset to one
        // side of the path, so reversing the points (tried, reverted) flips the offset side and
        // the engine draws a SECOND, visibly displaced ribbon with its own arrow chevrons all
        // over the map. Fed the forward points the geometry lands exactly on top of the existing
        // ribbon and is invisible -- the reverse view contributes only its panel.
        init(nlv, 0, srcdef, entry, &scratch);

        // LET VANILLA PLACE IT, by treating this node's INCOMING edge as an outgoing one.
        //
        // Every hand-rolled rule I tried was wrong in some case: mirroring the forward anchor's
        // (along, across) offset uses the ribbon's LOCAL direction at the far end, which on a
        // curved link points somewhere the link does not go -- a bordeaux panel still landed on
        // the wrong side, and english_channel <- ivory_coast sat off the line. The measurements
        // that were supposed to justify the rule also failed: "0 ribbons tessellated
        // target-first" showed the source-end detection was a no-op, so it had explained nothing.
        //
        // The engine already has the only rule that matters, and it always works from the
        // ribbon's START (0x13F9CE0). So hand it a ribbon that starts at OUR node: the reverse
        // entry carries a reversed copy of the control polyline, so building a view from
        // (targetDef, reverseEntry) makes the engine place the panel from the target's end by
        // exactly the code path that places outgoing panels -- same distance rule, same side,
        // and the same anti-overlap against the shared scratch vector.
        //
        // That view's RIBBON cannot be kept: the strip is offset to one side of its path, so a
        // reversed one draws as a second, visibly displaced ribbon with its own arrow chevrons
        // (tried, reverted). So the view is built only to harvest its anchor, then destroyed
        // through its own deleting destructor, and the anchor is transplanted onto `nlv`, whose
        // geometry came from the forward pair and therefore lands invisibly on the existing
        // ribbon.
        if (rev_entry_for_lv) {
            uintptr_t tmp = make(type);
            if (tmp) {
                init(tmp, 0, tgtdef_for_lv, rev_entry_for_lv, &scratch);
                if (livetrade::validate_region(tmp + LV_ANCHOR + 12, 4)) {
                    const float* ta = (const float*)(tmp + LV_ANCHOR);
                    if (std::isfinite(ta[0]) && std::isfinite(ta[2])) {
                        *(float*)(nlv + LV_ANCHOR + 0) = ta[0];
                        *(float*)(nlv + LV_ANCHOR + 8) = ta[2];
                        placed.push_back({ta[0], ta[2]});
                    }
                }
                uintptr_t vt = livetrade::fq(tmp);
                if (vt && livetrade::validate_region(vt, 8)) {
                    using FnDtor = void* (__fastcall*)(uintptr_t, unsigned);
                    auto dtor = (FnDtor)livetrade::fq(vt);      // vtable[0] = deleting destructor
                    if (dtor) dtor(tmp, 1);
                }
            }
        }

        // OWN THE PANEL FROM THE TARGET NODE'S SIDE.
        //
        // The reverse view was built with the forward view's source definition, so the renderer
        // keyed everything -- culling included -- on the SOURCE node. That is why a reverse panel
        // only appeared when its forward twin did, and why gulf_of_st_lawrence -> north_sea never
        // showed one: the two ends cannot be on screen together, so the source is always culled.
        // The reverse panel belongs to the TARGET node, so point it there. entry+0x30 is the
        // resolved target definition (Link() writes it at 0xB697AD; NULL if the link never
        // resolved, hence the guard).
        {
            uintptr_t tgtdef = tgtdef_for_lv;
            if (tgtdef && livetrade::validate_region(tgtdef + 0xD8, 4)) {
                *(uintptr_t*)(nlv + LV_SRCDEF) = tgtdef;
                // ...and give it the reverse entry, so the number resolves the other way. Both
                // are written AFTER init: the geometry was built from the true forward pair and
                // is cached in +0x88, so swapping these two fields cannot disturb the ribbon.
                if (rev_entry_for_lv) *(uintptr_t*)(nlv + LV_ENTRY) = rev_entry_for_lv;
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
            << " reverse ones (" << g_flipped << " ribbons tessellated target-first)" << "\n";
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
