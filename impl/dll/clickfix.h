// CLICKING A REVERSE PANEL'S STEER BUTTON ASSIGNS THE MERCHANT TO THAT END (spec 1.7; tests C1, C2).
//
// The panel's steer_button handler is 0x13FD5F0. Traced: it derives the link ordinal by searching
// [LinkView+0x78]->outgoing for [LinkView+0x80]->+0x30 (0x13FD612..0x13FD666), leaving the result
// at its zero init on a miss (0x13FD664), then posts steer_command {country@0x50, linkIndex@0x58,
// nodeIndex@0x5C} which 0x5DA4F0 writes verbatim into rec+0xA8 at 0x5DA5C4. On a REVERSE view the
// search misses by construction, so the engine would steer link #0 -- the wrong link.
//
// The fix does not fight the engine's command. It records the player's real intent in
// assign::g_table BEFORE the handler runs, and lets the handler post its +0xA8=0 command as usual:
// +0xA8=0 with a table entry is exactly the representation syncrec.h already writes for a reverse
// end, the router reads the table (not the record) for the target, and the engine's own flag row
// then draws the merchant on this panel. The only new thing is the table write.
//
// Hooked at the prologue via detour.h. The first 14 bytes are position-independent:
//   48 89 5c 24 10   mov [rsp+0x10], rbx
//   48 89 6c 24 18   mov [rsp+0x18], rbp
//   56               push rsi
//   57               push rdi
//   41 56            push r14
// so the trampoline replays them and jumps back. At entry rcx = panel, [rcx+0x38] = LinkView.
// The handler is bound as a delegate (no call rel32 site exists), so a call-site redirect is not
// available and the prologue is the seam.
//
// The country is the one the handler itself would use (0x13FD6B1..0x13FD6E1): [G+0x1E68] when
// [G+0x1E66]==7 && [G+0x1E6F]!=0 (observer), else [G+0x1E60]. Both are 8-byte handles whose
// bytes 4..5 are the country index; the table is keyed by the raw tag dword whose low 16 bits are
// that index (livetrade::country_index_of), so the key is rebuilt from the index alone.
#pragma once
#include <windows.h>
#include <cstdint>
#include <fstream>
#include <string>
#include "livetrade.h"
#include "detour.h"
#include "revpanel.h"
#include "assign.h"

namespace clickfix {

constexpr uintptr_t CLICK_HANDLER = 0x13FD5F0;
constexpr int PANEL_LINKVIEW = 0x38;

inline detour::Hook g_hook;
inline uint64_t g_clicks = 0, g_reverse_clicks = 0;
inline std::string g_log;

inline uint64_t player_handle() {
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + 0x1E60, 16)) return 0;
    uint8_t mode = *(uint8_t*)(g + 0x1E66);
    uint8_t obs  = *(uint8_t*)(g + 0x1E6F);
    return (mode == 7 && obs != 0) ? livetrade::fq(g + 0x1E68) : livetrade::fq(g + 0x1E60);
}

inline void on_click(detour::Regs* r) {
    g_clicks++;
    uintptr_t panel = r->rcx;
    // log EVERY click so the seam is provably live before the reverse case is judged
    if (!g_log.empty()) {
        std::ofstream lg(g_log, std::ios::app);
        uintptr_t lv0 = (panel && livetrade::validate_region(panel + PANEL_LINKVIEW, 8)) ? livetrade::fq(panel + PANEL_LINKVIEW) : 0;
        lg << "  [click] steer_button #" << g_clicks << " panel=0x" << std::hex << panel << " lv=0x" << lv0 << std::dec
           << (lv0 && revpanel::is_reverse(lv0) ? " (REVERSE view)" : " (forward view)") << (char)10;
    }
    if (!panel || !livetrade::validate_region(panel + PANEL_LINKVIEW, 8)) return;
    uintptr_t lv = livetrade::fq(panel + PANEL_LINKVIEW);
    if (!lv) return;
    const revpanel::RevInfo* ri = revpanel::reverse_info(lv);
    uint64_t h = player_handle();
    if (!h) return;
    int cidx = (int)(int16_t)(h >> 32);
    if (cidx < 0) return;
    // BOTH kinds of panel write the table. The table is the source of truth for the model, for
    // syncrec and for the steer button, so a FORWARD click that only posted the engine command left
    // a stale reverse entry behind: the player could move a merchant onto a reverse end but never
    // back onto Champagne (user-reported 2026-08-26). A forward click writes (node -> far node);
    // syncrec then writes the matching real ordinal, agreeing with what the engine just posted.
    uintptr_t owner_def = 0, other_def = 0;
    if (ri) { owner_def = ri->owner_def; other_def = ri->other_def; }
    else {
        if (!livetrade::validate_region(lv + revpanel::LV_SRCDEF, 16)) return;
        owner_def = livetrade::fq(lv + revpanel::LV_SRCDEF);
        uintptr_t entry = livetrade::fq(lv + revpanel::LV_ENTRY);
        if (!entry || !livetrade::validate_region(entry + 0x30, 8)) return;
        other_def = livetrade::fq(entry + 0x30);
    }
    std::string node  = livetrade::def_key(owner_def);
    std::string other = livetrade::def_key(other_def);
    if (node.empty() || other.empty()) return;
    // the table key is the raw tag dword; its low 16 bits are the index, which is all the
    // routing and syncrec ever extract from it
    {   // no merchant assignment at the player's OWN trade capital (user rule); the engine record
        // of this country at this node carries has_capital at +0xAD
        uintptr_t nobj = 0;
        for (auto& s0 : livetrade::read_sim_nodes()) if (s0.obj && livetrade::validate_region(s0.obj + 0xA8, 8) && livetrade::fq(s0.obj + 0xA8) == owner_def) { nobj = s0.obj; break; }
        if (nobj && livetrade::validate_region(nobj + 0x18, 16)) {
            uintptr_t rb = livetrade::fq(nobj + 0x18); int rc = livetrade::fi(nobj + 0x24);
            int idx = cidx & 0xFFFF;
            if (rb && idx >= 0 && idx < rc && livetrade::validate_region(rb + (uintptr_t)idx * 0xC0, 0xC0) && livetrade::fb(rb + (uintptr_t)idx * 0xC0 + 0xAD) != 0) {
                std::ofstream lg(g_log, std::ios::app);
                lg << "  [click] REFUSED: " << node << " is this country's trade capital -- no merchant may be assigned there" << (char)10;
                return;
            }
        }
    }
    assign::set(cidx, node, other);
    g_reverse_clicks++;
    if (!g_log.empty()) {
        std::ofstream lg(g_log, std::ios::app);
        lg << "  [click] player country#" << cidx << " assigned a merchant at " << node << (ri ? "" : " (FORWARD panel)")
           << " to steer the REVERSE end toward " << other << " (table entry written; the engine's"
           << " own command posts +0xA8=0, which is this end's representation)" << (char)10;
    }
}

inline bool install(const std::string& logpath, std::string* err) {
    g_log = logpath;
    uintptr_t target = livetrade::module_base() + CLICK_HANDLER;
    std::vector<uint8_t> expected = {0x48,0x89,0x5C,0x24,0x10, 0x48,0x89,0x6C,0x24,0x18,
                                     0x56, 0x57, 0x41,0x56};
    if (!detour::install(g_hook, target, expected, &on_click, "steer_button click")) {
        if (err) *err = g_hook.error;
        return false;
    }
    return true;
}

} // namespace clickfix
