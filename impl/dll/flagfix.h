// A MERCHANT STEERING A REVERSE END MUST NOT ALSO APPEAR ON FORWARD LINK #0 (spec 1.7, 1.12).
//
// The engine's flag row (0x13FD7B0) admits a record iff, among other gates, rec+0xA8 equals the
// panel's link ordinal -- and it derives that ordinal by searching the source node's outgoing
// vector, leaving it at its zero init on a miss (0x13FD894). syncrec.h writes a merchant steering a
// REVERSE end as type=1, +0xA8 = 0, because +0xA8 is read unbounded by five consumers and can hold
// no sentinel. Two consequences follow, one wanted and one not:
//
//   WANTED: on the reverse panel the ordinal search misses, collapses to 0, and the record with
//   +0xA8 == 0 is selected -- the engine draws the reverse merchant on the reverse panel by itself,
//   with a working tooltip (0x13FCCA3 reads only icon+0x1E8). The shield-creation trace found
//   this is the only STABLE way to get a shield: anything we add ourselves trips the count gate
//   at 0x13FD57B and is wiped by the next frame's full rebuild.
//
//   NOT WANTED: on the source node's FORWARD panel for link #0 the same record is selected too,
//   so the merchant shows up on a link it does not steer. The earlier version of this file
//   cleared the whole row on REVERSE panels -- backwards: it hid the shields that were right and
//   left the aliased ones in place.
//
// So: forward panels with ordinal 0 get the aliased shields removed; reverse panels are left to
// the engine. Removal is box->vt[0x270](box, holder, 0) = 0x163D8B0, which unlinks the holder's
// list node; the holder is then ours to destroy through its own deleting destructor (vt[0],
// 0xFC6D40 -> 0x152E030 frees the held window, then operator delete). Done after g_orig each
// frame, because the engine rebuilds the row whenever its count gate fails -- which, with our
// removals, is every frame; that is the per-frame cost the trace priced and accepted.
//
// Child list of the box (CGuiOverlappingElementsBox, vtable 0x1DA4910): {head,tail,count} at
// box+0x100/+0x108/+0x110, nodes are 0x20 bytes {payload@0, prev@8, next@0x10}. The holder's
// window is at holder+0x40; the shield icon is window->vt[0xC8](window,"trade_node_trader_shield")
// and carries the 8-byte country handle at icon+0x1E8, whose bytes 4..5 are the country index.
#pragma once
#include <windows.h>
#include <cstdint>
#include <string>
#include <vector>
#include "livetrade.h"
#include "revpanel.h"
#include "assign.h"

namespace flagfix {

constexpr uintptr_t PANEL_VTABLE   = 0x1D823C0;
constexpr int       VT_UPDATE      = 0x10;      // per-frame Update
constexpr uintptr_t PANEL_UPDATE   = 0x13FCD80;
constexpr int       PANEL_WINDOW   = 0x08;      // GUI window, written by the ctor at 0x13FB8A5
constexpr int       PANEL_LINKVIEW = 0x38;      // zeroed by the ctor at 0x13FB97B
constexpr int       WIN_FIND_BOX   = 0xE8;      // window vtbl: FindOverlappingElementsBox(const char*)
constexpr int       WIN_FIND_ICON  = 0xC8;      // window vtbl: FindIcon(const char*)
constexpr int       BOX_REMOVE     = 0x270;     // box vtbl: remove one child (holder), relayout flag
constexpr int       BOX_RELAYOUT   = 0x2C0;
constexpr int       BOX_HEAD       = 0x100;
constexpr int       HOLDER_WINDOW  = 0x40;
constexpr int       ICON_HANDLE    = 0x1E8;

using FnUpdate  = void (__fastcall*)(uintptr_t);
using FnFindBox = uintptr_t (__fastcall*)(uintptr_t, const char*);
using FnFindIcon= uintptr_t (__fastcall*)(uintptr_t, const char*);
using FnRemove  = void (__fastcall*)(uintptr_t, uintptr_t, int);
using FnRelayout= void (__fastcall*)(uintptr_t);
using FnDtor    = void (__fastcall*)(uintptr_t, unsigned);

inline FnUpdate g_orig = nullptr;
inline bool g_installed = false;
inline uint64_t g_cleared = 0;      // aliased shields removed from forward link-#0 panels
inline uint64_t g_inspected = 0, g_shields = 0;   // forward-#0 panels seen / shields walked
inline uint64_t g_rev_panels = 0, g_rev_with_shields = 0, g_rev_shields = 0;   // reverse panels drawn

// the ordinal a FORWARD panel represents: its entry's target within its source's outgoing vector
inline int panel_ordinal(uintptr_t lv) {
    uintptr_t srcdef = livetrade::fq(lv + revpanel::LV_SRCDEF);
    uintptr_t entry  = livetrade::fq(lv + revpanel::LV_ENTRY);
    if (!srcdef || !entry || !livetrade::validate_region(entry + 0x30, 8)) return -1;
    uintptr_t tgt = livetrade::fq(entry + 0x30);
    if (!livetrade::validate_region(srcdef + 0x98, 16)) return -1;
    uintptr_t b = livetrade::fq(srcdef + 0x98), e = livetrade::fq(srcdef + 0xA0);
    if (!b || e <= b || (e - b) > 0x78 * 64) return -1;
    int i = 0;
    for (uintptr_t p = b; p + 0x78 <= e; p += 0x78, i++)
        if (livetrade::validate_region(p + 0x30, 8) && livetrade::fq(p + 0x30) == tgt) return i;
    return -1;
}

// does our table say this country steers a REVERSE end at `node_key`?
inline bool steers_reverse_here(int country_index, const std::string& node_key, uintptr_t srcdef) {
    for (auto& [key, target] : assign::g_table) {
        if (key.second != node_key) continue;
        if (livetrade::country_index_of(key.first) != country_index) continue;
        // reverse iff the target is NOT in the source's outgoing vector
        uintptr_t b = livetrade::fq(srcdef + 0x98), e = livetrade::fq(srcdef + 0xA0);
        for (uintptr_t p = b; b && e > b && p + 0x78 <= e; p += 0x78) {
            uintptr_t t = livetrade::validate_region(p + 0x30, 8) ? livetrade::fq(p + 0x30) : 0;
            if (t && livetrade::def_key(t) == target) return false;   // a forward end
        }
        return true;
    }
    return false;
}

// MEASURED, 10932 forward-#0 panels over five ticks: the box's child list is EMPTY after g_orig
// (box+0x100 head == 0, +0x108 tail == 0). The engine does not draw the +0xA8=0 records on
// forward link #0 after all -- so there is nothing to remove, and this hook is a guard that
// costs one list-head read per panel per frame. Kept so a future engine path that does draw
// them is corrected rather than silently shown.
inline void __fastcall update_hook(uintptr_t panel) {
    if (g_orig) g_orig(panel);                  // the engine builds the row exactly as it wants
    if (!panel || !livetrade::validate_region(panel + PANEL_LINKVIEW, 8)) return;
    uintptr_t lv = livetrade::fq(panel + PANEL_LINKVIEW);
    if (!lv) return;
    if (revpanel::is_reverse(lv)) {
        // MEASURE, do not touch: how many shields did the engine put on this reverse panel?
        g_rev_panels++;
        uintptr_t w2 = livetrade::fq(panel + PANEL_WINDOW);
        if (w2 && livetrade::validate_region(w2, 8)) {
            uintptr_t wv2 = livetrade::fq(w2);
            if (wv2 && livetrade::validate_region(wv2 + WIN_FIND_BOX, 8)) {
                auto fb2 = (FnFindBox)livetrade::fq(wv2 + WIN_FIND_BOX);
                uintptr_t bx = fb2 ? fb2(w2, "director_flags") : 0;
                if (bx && livetrade::validate_region(bx + BOX_HEAD, 16)) {
                    int n = 0;
                    for (uintptr_t nd = livetrade::fq(bx + BOX_HEAD); nd && n < 64 && livetrade::validate_region(nd, 0x20); nd = livetrade::fq(nd + 0x10)) n++;
                    if (n) { g_rev_with_shields++; g_rev_shields += n; }
                }
            }
        }
        return;
    }
    if (panel_ordinal(lv) != 0) return;                  // only link #0 collects the aliases
    g_inspected++;
    if (assign::g_table.empty()) return;
    uintptr_t srcdef = livetrade::fq(lv + revpanel::LV_SRCDEF);
    std::string node_key = livetrade::def_key(srcdef);
    if (node_key.empty()) return;

    uintptr_t win = livetrade::fq(panel + PANEL_WINDOW);
    if (!win || !livetrade::validate_region(win, 8)) return;
    uintptr_t wvt = livetrade::fq(win);
    if (!wvt || !livetrade::validate_region(wvt + WIN_FIND_BOX, 8)) return;
    auto find_box = (FnFindBox)livetrade::fq(wvt + WIN_FIND_BOX);
    if (!find_box) return;
    uintptr_t box = find_box(win, "director_flags");
    if (!box || !livetrade::validate_region(box + BOX_HEAD, 24)) return;
    uintptr_t bvt = livetrade::fq(box);
    if (!bvt || !livetrade::validate_region(bvt + BOX_RELAYOUT, 8)) return;
    auto remove   = (FnRemove)livetrade::fq(bvt + BOX_REMOVE);
    auto relayout = (FnRelayout)livetrade::fq(bvt + BOX_RELAYOUT);
    if (!remove || !relayout) return;

    // snapshot the holders first: removal unlinks nodes under us
    std::vector<uintptr_t> holders;
    for (uintptr_t nd = livetrade::fq(box + BOX_HEAD); nd && livetrade::validate_region(nd, 0x20);
         nd = livetrade::fq(nd + 0x10)) {
        uintptr_t h = livetrade::fq(nd);
        if (h) holders.push_back(h);
        if (holders.size() > 64) break;
    }
    int removed = 0;
    for (uintptr_t h : holders) {
        if (!livetrade::validate_region(h + HOLDER_WINDOW, 8)) continue;
        uintptr_t hw = livetrade::fq(h + HOLDER_WINDOW);
        if (!hw || !livetrade::validate_region(hw, 8)) continue;
        uintptr_t hwvt = livetrade::fq(hw);
        if (!hwvt || !livetrade::validate_region(hwvt + WIN_FIND_ICON, 8)) continue;
        auto find_icon = (FnFindIcon)livetrade::fq(hwvt + WIN_FIND_ICON);
        if (!find_icon) continue;
        uintptr_t icon = find_icon(hw, "trade_node_trader_shield");
        if (!icon || !livetrade::validate_region(icon + ICON_HANDLE, 8)) continue;
        uint64_t handle = livetrade::fq(icon + ICON_HANDLE);
        g_shields++;
        int cidx = (int)(int16_t)(handle >> 32);
        if (!steers_reverse_here(cidx, node_key, srcdef)) continue;
        remove(box, h, 0);
        uintptr_t hvt = livetrade::fq(h);
        if (hvt && livetrade::validate_region(hvt, 8)) {
            auto dtor = (FnDtor)livetrade::fq(hvt);
            if (dtor) dtor(h, 1);                        // frees the held window, then the holder
        }
        removed++;
    }
    if (removed) { relayout(box); g_cleared += removed; }
}

// Swap the vtable slot. Verified against the expected original first: on any other build the slot
// holds something else and we refuse rather than corrupt a vtable (spec 2.5).
inline bool install(std::string* err) {
    if (g_installed) return true;
    uintptr_t slot = livetrade::module_base() + PANEL_VTABLE + VT_UPDATE;
    if (!livetrade::validate_region(slot, 8)) { if (err) *err = "panel vtable unreadable"; return false; }
    uintptr_t cur = livetrade::fq(slot);
    if (cur != livetrade::module_base() + PANEL_UPDATE) {
        if (err) *err = "panel vtable slot +0x10 is not 0x13FCD80 (patched binary?)";
        return false;
    }
    g_orig = (FnUpdate)cur;
    DWORD old = 0;
    if (!VirtualProtect((void*)slot, 8, PAGE_READWRITE, &old)) {
        if (err) *err = "VirtualProtect on the panel vtable failed"; return false;
    }
    *(uintptr_t*)slot = (uintptr_t)&update_hook;
    VirtualProtect((void*)slot, 8, old, &old);
    FlushInstructionCache(GetCurrentProcess(), (void*)slot, 8);
    g_installed = true;
    return true;
}

} // namespace flagfix
