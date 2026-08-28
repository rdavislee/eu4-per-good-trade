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
// list node ONLY -- disassembled: 0x1530240 frees the 0x20-byte node via 0xDF1A0 and drops the
// reverse registration via 0x4741B0, and never touches the child itself. So the holder is
// then ours to destroy through its own deleting destructor (vt[0],
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
constexpr int       BOX_APPEND     = 0x260;     // box vtbl: append child (holder), relayout flag
constexpr int       BOX_CLEAR      = 0x278;     // box vtbl: clear all (deletes the children)
constexpr int       BOX_SETTOOLTIP = 0x118;     // box vtbl: SetTooltip(const std::string*) -- stores +0x38 and pushes to the children (0x163DA20)
constexpr uintptr_t STR_MAPICON_TRADEROUTE = 0x232B2E0;   // the engine's static std::string("mapicon_traderoute") (built at 0x1337C2E)
inline uint64_t g_rev_tooltip_set = 0;
constexpr uintptr_t GUI_MANAGER    = 0x23494F0; // *(CGui**)
constexpr uintptr_t HOLDER_CTOR    = 0x152DF80; // (holder, gui, const std::string* windowName)
constexpr uintptr_t SHIELD_SETUP   = 0x10B44B0; // (iface, elem, handle, setFrame, clickable, defTooltip, flagA, flagB)
constexpr uintptr_t TEMPLATE_STR   = 0x232B4C0; // the engine static std::string trade_node_trader
constexpr uintptr_t ENGINE_NEW     = 0x1A332D4;

using FnUpdate  = void (__fastcall*)(uintptr_t);
using FnFindBox = uintptr_t (__fastcall*)(uintptr_t, const char*);
using FnFindIcon= uintptr_t (__fastcall*)(uintptr_t, const char*);
using FnRemove  = void (__fastcall*)(uintptr_t, uintptr_t, int);
using FnRelayout= void (__fastcall*)(uintptr_t);
using FnDtor    = void (__fastcall*)(uintptr_t, unsigned);
using FnAppend  = void (__fastcall*)(uintptr_t, uintptr_t, int);
using FnNew     = void* (__fastcall*)(size_t);
using FnHolderCtor  = uintptr_t (__fastcall*)(uintptr_t, uintptr_t, uintptr_t);
using FnShieldSetup = void (__fastcall*)(uintptr_t, uintptr_t, uint64_t, bool, bool, bool, uint8_t, uint8_t);

inline FnUpdate g_orig = nullptr;
inline bool g_installed = false;
inline uint64_t g_cleared = 0;      // aliased shields removed from forward link-#0 panels
inline uint64_t g_inspected = 0, g_shields = 0;   // forward-#0 panels seen / shields walked
inline uint64_t g_rev_panels = 0, g_rev_with_shields = 0, g_rev_shields = 0;   // reverse panels drawn
inline uint64_t g_rev_removed = 0;   // engine-drawn shields cleared from reverse panels
inline uint64_t g_rev_added = 0;     // shields we drew on reverse panels from the table

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
// THE STEER BUTTON'S STATE (user-reported 2026-08-26). The panel Update (0x13FCD80) derives its own
// link ordinal with the same outgoing-list search the click handler uses (0x13FCE2A..0x13FCE56,
// zero-initialised at 0x13FCDF6, written only on a hit) and lights the button iff rec+0xA8 equals
// it (0x13FD0F5). Our reverse views carry a synthetic entry that is in no outgoing vector, so the
// search misses and the ordinal is 0 -- and a reverse-end assignment IS +0xA8 = 0 (syncrec). Hence
// every reverse panel of the node, plus forward link #0, lit up together. The frame is an int32
// at steer_button+0x64 written through vt[0xA8] SetFrame (0x13A8D80): 1 = steering, 2 = not; the
// tooltip (0x13FBD30) re-reads that field, so correcting it corrects both. The truth is the table.
constexpr int WIN_FIND_BUTTON = 0x68;    // window vtbl: FindButton(const char*)
constexpr int BTN_SETFRAME    = 0xA8;    // button vtbl: SetFrame(int)
constexpr int BTN_FRAME       = 0x64;    // int32 frame: 1 steering here, 2 not
inline std::string g_log;   // set by install(); empty = self_dir()/per-good-trade.log
inline uint64_t g_frames_forced = 0, g_sb_entered = 0, g_sb_nokey = 0, g_sb_want0 = 0, g_sb_nowin = 0, g_sb_nobtn = 0, g_sb_curbad = 0, g_sb_same = 0;
inline int g_sb_curbad_logged = 0;
inline int player_index() {
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + 0x1E60, 16)) return -1;
    uint8_t mode = livetrade::fb(g + 0x1E66), obs = livetrade::fb(g + 0x1E6F);
    uint64_t h = (mode == 7 && obs != 0) ? livetrade::fq(g + 0x1E68) : livetrade::fq(g + 0x1E60);
    return h ? (int)(int16_t)(h >> 32) : -1;
}
inline void fix_steer_button(uintptr_t panel, uintptr_t lv, const revpanel::RevInfo* ri) {
    std::string node_key, far_key;
    if (ri) { node_key = livetrade::def_key(ri->owner_def); far_key = livetrade::def_key(ri->other_def); }
    else {
        if (!livetrade::validate_region(lv + revpanel::LV_SRCDEF, 16)) return;
        uintptr_t src = livetrade::fq(lv + revpanel::LV_SRCDEF), entry = livetrade::fq(lv + revpanel::LV_ENTRY);
        if (!src || !entry || !livetrade::validate_region(entry + 0x30, 8)) return;
        node_key = livetrade::def_key(src); far_key = livetrade::def_key(livetrade::fq(entry + 0x30));
    }
    g_sb_entered++;
    if (node_key.empty() || far_key.empty()) { g_sb_nokey++; return; }
    int pidx = player_index();
    int want = 0;                                   // 0: leave the engine's answer alone
    if (pidx >= 0)
        for (auto& [k, tgt] : assign::g_table)
            if (k.second == node_key && livetrade::country_index_of(k.first) == pidx) { want = (tgt == far_key) ? 1 : 2; break; }
    if (!want && ri) want = 2;                      // no table entry: the 0 == 0 match on a reverse panel means nothing
    if (!want) { g_sb_want0++; return; }
    uintptr_t win = livetrade::validate_region(panel + PANEL_WINDOW, 8) ? livetrade::fq(panel + PANEL_WINDOW) : 0;
    uintptr_t wvt = (win && livetrade::validate_region(win, 8)) ? livetrade::fq(win) : 0;
    if (!wvt || !livetrade::validate_region(wvt + WIN_FIND_BUTTON, 8)) { g_sb_nowin++; return; }
    auto fb = (FnFindBox)livetrade::fq(wvt + WIN_FIND_BUTTON);
    uintptr_t btn = fb ? fb(win, "steer_button") : 0;
    if (!btn || !livetrade::validate_region(btn, 0x70)) { g_sb_nobtn++; return; }
    // ALWAYS SET IT. The engine writes this button's frame every frame (0x13FD1DD: vt[0xA8](1|2),
    // and 0x13A8D80 is `mov [rcx+0x64], edx`), so calling SetFrame with the table's answer is exactly
    // the call the engine just made. The earlier gate that only overwrote a field reading 0/1/2
    // skipped ~25% of panels whose +0x64 read 127/556 (measured: `curbad`), and that is how a
    // merchant moved from a node's forward link to a reverse one stayed 'steering' on BOTH boxes
    // (user, valencia: genua then sevilla). The odd reads are counted, not obeyed.
    int32_t cur = livetrade::fi(btn + BTN_FRAME);
    if (cur != 0 && cur != 1 && cur != 2) {
        g_sb_curbad++;
        if (g_sb_curbad_logged < 12) {
            g_sb_curbad_logged++;
            std::ofstream lg(g_log.empty() ? livetrade::self_dir() + std::string(1, (char)92) + "per-good-trade.log" : g_log, std::ios::app);
            { static uint64_t sb=0; if ((sb++ % 2000) == 0) lg << "  [steerbtn] frame field reads " << cur << " on " << (ri ? "reverse" : "forward") << " panel " << node_key << " -> " << far_key
               << " (want " << want << "); set anyway (1/2000 sampled)" << (char)10; }
        }
    } else if (cur == want) { g_sb_same++; return; }
    uintptr_t bvt = livetrade::fq(btn);
    if (!bvt || !livetrade::validate_region(bvt + BTN_SETFRAME, 8)) return;
    ((void (__fastcall*)(uintptr_t, int))livetrade::fq(bvt + BTN_SETFRAME))(btn, want);
    g_frames_forced++;
}

inline void __fastcall update_hook(uintptr_t panel) {
    if (g_orig) g_orig(panel);                  // the engine builds the row exactly as it wants
    if (!panel || !livetrade::validate_region(panel + PANEL_LINKVIEW, 8)) return;
    uintptr_t lv = livetrade::fq(panel + PANEL_LINKVIEW);
    if (!lv) return;
    fix_steer_button(panel, lv, revpanel::reverse_info(lv));   // before any early return below
    if (const revpanel::RevInfo* ri = revpanel::reverse_info(lv)) {
        // A REVERSE PANEL'S ROW IS BUILT BY US, FROM THE TABLE. The engine cannot build it: every
        // reverse end at a node is +0xA8 = 0 and the engine's ordinal search collapses every
        // reverse panel to 0, so it draws the SAME records on all of them -- and a Phi_w link-#0
        // merchant (vanilla's own, no table entry) is copied onto every non-Phi_w panel at the
        // node. Pruning after the fact cannot tell those copies apart. So: clear everything the
        // engine drew here, then add exactly one shield per table entry whose target is this
        // panel's far node, using the engine's own holder ctor and shield setup (OFFSETS.md).
        g_rev_panels++;
        std::string node_key = livetrade::def_key(ri->owner_def);
        std::string far_key  = livetrade::def_key(ri->other_def);
        uintptr_t w2 = livetrade::fq(panel + PANEL_WINDOW);
        if (node_key.empty() || far_key.empty() || !w2 || !livetrade::validate_region(w2, 8)) return;
        uintptr_t wv2 = livetrade::fq(w2);
        if (!wv2 || !livetrade::validate_region(wv2 + WIN_FIND_BOX, 8)) return;
        auto fb2 = (FnFindBox)livetrade::fq(wv2 + WIN_FIND_BOX);
        uintptr_t bx = fb2 ? fb2(w2, "director_flags") : 0;
        if (!bx || !livetrade::validate_region(bx + BOX_HEAD, 16)) return;
        uintptr_t bvt2 = livetrade::fq(bx);
        if (!bvt2 || !livetrade::validate_region(bvt2 + BOX_CLEAR, 8)) return;
        auto clear2    = (FnRelayout)livetrade::fq(bvt2 + BOX_CLEAR);
        auto append2   = (FnAppend)livetrade::fq(bvt2 + BOX_APPEND);
        auto relayout2 = (FnRelayout)livetrade::fq(bvt2 + BOX_RELAYOUT);
        if (!clear2 || !append2 || !relayout2) return;
        // who belongs here: every country whose table entry at this node targets far_key
        std::vector<int> want;
        for (auto& [key, target] : assign::g_table)
            if (key.second == node_key && target == far_key) want.push_back(livetrade::country_index_of(key.first));
        // the engine's row is wrong by construction; clear it (vt[0x278] deletes the children)
        int had = 0;
        for (uintptr_t nd = livetrade::fq(bx + BOX_HEAD); nd && had < 64 && livetrade::validate_region(nd, 0x20); nd = livetrade::fq(nd + 0x10)) had++;
        if (had) { clear2(bx); g_rev_removed += had; }
        if (want.empty()) return;
        // add ours, from the source node's records (the handle at rec+0x10 is copied, never built)
        uintptr_t node = 0;
        {
            uintptr_t mgr = livetrade::trade_manager();
            int idx = livetrade::validate_region(ri->owner_def + 0xD8, 4) ? livetrade::fi(ri->owner_def + 0xD8) : 0;
            uintptr_t base = mgr ? livetrade::rq(mgr + 0x18) : 0;
            int32_t cnt = 0; if (mgr) livetrade::safe_read(mgr + 0x24, &cnt, 4);
            if (base && idx > 0 && idx < cnt) node = base + (uintptr_t)idx * 0x138;
        }
        if (!node) return;
        uintptr_t rbase = livetrade::rq(node + 0x18); int rcnt = livetrade::ri(node + 0x24);
        if (!rbase || rcnt <= 0 || rcnt > 4096 || !livetrade::validate_region(rbase, (size_t)rcnt * 0xC0)) return;
        uintptr_t gui = livetrade::rq(livetrade::module_base() + GUI_MANAGER);
        uintptr_t g = livetrade::game_singleton();
        uintptr_t iface = 0;
        if (g && livetrade::validate_region(g + 0x1E00, 8)) {
            uintptr_t p1 = livetrade::fq(g + 0x1E00);
            if (p1 && livetrade::validate_region(p1 + 0x58, 8)) iface = livetrade::fq(p1 + 0x58);
        }
        if (!gui || !iface) return;
        auto hnew   = (FnNew)(livetrade::module_base() + ENGINE_NEW);
        auto hctor  = (FnHolderCtor)(livetrade::module_base() + HOLDER_CTOR);
        auto ssetup = (FnShieldSetup)(livetrade::module_base() + SHIELD_SETUP);
        uintptr_t tmpl = livetrade::module_base() + TEMPLATE_STR;
        int prov = livetrade::validate_region(ri->owner_def + 0xDC, 4) ? livetrade::fi(ri->owner_def + 0xDC) : 0;
        int added = 0;
        for (int cidx : want) {
            if (cidx < 0 || cidx >= rcnt) continue;
            uintptr_t rec = rbase + (uintptr_t)cidx * 0xC0;
            if ((livetrade::fi(rec + 0x14) & 0xFFFF) != cidx) continue;
            uint64_t handle = livetrade::fq(rec + 0x10);
            uintptr_t h = (uintptr_t)hnew(0x50);
            if (!h) continue;
            hctor(h, gui, tmpl);
            uintptr_t hw = livetrade::fq(h + HOLDER_WINDOW);
            if (!hw || !livetrade::validate_region(hw, 8)) continue;
            uintptr_t hwvt = livetrade::fq(hw);
            FnFindIcon fi2 = (hwvt && livetrade::validate_region(hwvt + WIN_FIND_ICON, 8)) ? (FnFindIcon)livetrade::fq(hwvt + WIN_FIND_ICON) : nullptr;
            uintptr_t icon = fi2 ? fi2(hw, "trade_node_trader_shield") : 0;
            if (!icon) continue;
            ssetup(iface, icon, handle, true, true, false, 1, 0);
            if (livetrade::validate_region(icon + 0x10, 4)) *(int32_t*)(icon + 0x10) = prov;
            append2(bx, h, 0);
            added++;
        }
        if (added) {
            relayout2(bx); g_rev_added += added;
            // THE HOVER TEXT. The engine's row builder ends with box->vt[0x118]("mapicon_traderoute")
            // (0x13FDE1E -> 0x163DA20), which stores the key at box+0x38 AND pushes it into every child
            // present at that moment (holder vt[0x48] -> window vt[0x118] -> the shield icon's +0x38).
            // AddChild (0x163D9E0) does not propagate it, so shields appended here carried an empty key,
            // the map-icon tooltip dispatcher's compare at 0xB8693D failed, and the panel's tooltip
            // (0x13FBD30, which reads only icon+0x1E8 and the owner node's record) was never entered.
            // Restoring the call is byte-for-byte what the engine does; the string is its own static.
            // the engine string is a lazy magic static (0x1337C28 guard): before its first construction the
            // object is all zeros and SetTooltip would assign an empty key -- guard on its size (reviewed)
            if (livetrade::validate_region(bvt2 + BOX_SETTOOLTIP, 8) &&
                livetrade::validate_region(livetrade::module_base() + STR_MAPICON_TRADEROUTE + 0x10, 8) &&
                *(uint64_t*)(livetrade::module_base() + STR_MAPICON_TRADEROUTE + 0x10) == 18) {
                auto set_tt = (void (__fastcall*)(uintptr_t, const void*))livetrade::fq(bvt2 + BOX_SETTOOLTIP);
                if (set_tt) { set_tt(bx, (const void*)(livetrade::module_base() + STR_MAPICON_TRADEROUTE)); g_rev_tooltip_set++; }
            }
        }
        return;
    }
    // EVERY forward panel, not only ordinal 0. Measured: forward-#0 panels saw 104,066 shields and
    // removed none, while Austria stood on every forward panel out of rheinland. Its table entry
    // (rheinland -> wien) is a FORWARD end, so the old "is this a reverse steerer" test kept it --
    // but the engine had drawn it on every panel whose ordinal search collapsed to its record. The
    // rule is the same as the reverse side's: a shield belongs on a panel only if the country's
    // real target is this panel's far node.
    g_inspected++;
    if (assign::g_table.empty()) return;
    uintptr_t srcdef = livetrade::fq(lv + revpanel::LV_SRCDEF);
    uintptr_t fentry = livetrade::fq(lv + revpanel::LV_ENTRY);
    std::string node_key = livetrade::def_key(srcdef);
    std::string far_key  = (fentry && livetrade::validate_region(fentry + 0x30, 8))
                             ? livetrade::def_key(livetrade::fq(fentry + 0x30)) : std::string();
    if (node_key.empty() || far_key.empty()) return;

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
        // Keep unless the table says this country targets a DIFFERENT far node here. No table
        // entry means an engine-native steerer, kept on whatever panel the engine drew it.
        bool alias = false;
        for (auto& [key, target] : assign::g_table)
            if (key.second == node_key && livetrade::country_index_of(key.first) == cidx) { alias = (target != far_key); break; }
        if (!alias) continue;
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
