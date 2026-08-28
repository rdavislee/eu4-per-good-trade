// THE PROVINCE WINDOW IS THE PER-GOOD VIEW'S LIFETIME (spec 1.12 / test D1; user 2026-08-27):
// while the province window is OPEN, the whole trade view shows that province's good -- its graph
// as the arrows, its values on the panels, only outgoing panels; the moment it CLOSES, everything
// returns to the aggregate: all panels (reverse included), the trade-node coloring, full trade
// values, Phi_w arrows.
//
// Engine seams (static RE 2026-08-27): the selection holder is IGI+0x1220 (+0x00 selected
// CProvince*, written only at 0x139C870 -- NEVER cleared on window close, so the selection alone
// cannot be the lifetime); +0x10 is the CProvinceInterface*, whose SHOWN province is view+0x958
// and whose visible test (0x1348370) is window(view+0xA0)+0xF5, else the embedded small view
// view+0x2F0 -> window(+0x558) -> +0xF5. CProvince+0x458 = CTradeGood* (0xA14020); good+0x18 = the
// name std::string (the key 00_tradegoods.txt declares). A good the model does not route (gold) or
// a windowless frame maps to the aggregate view. In TRADE map mode the engine routes clicks to the
// node window, so opening the province window from there is the follow-up (Holder::OpenFor).
#pragma once
#include <cstdint>
#include <string>
#include "livetrade.h"
#include "viewmode.h"

namespace selprov {

constexpr int IGI_HOLDER   = 0x1220;   // IGI -> the province-view holder
constexpr int HOLDER_VIEW  = 0x10;     // holder -> CProvinceInterface*
constexpr int VIEW_GUI     = 0xA0;     // view -> CGuiWindow (visible byte +0xF5)
constexpr int VIEW_SMALL   = 0x2F0;    // view -> the embedded small view
constexpr int SMALL_GUI    = 0x558;    // small view -> its window (visible byte +0xF5)
constexpr int WIN_VISIBLE  = 0xF5;
constexpr int VIEW_PROV    = 0x958;    // view -> the CProvince it shows
constexpr int PROV_ID      = 0x20;
constexpr int PROV_GOOD    = 0x458;    // CProvince -> CTradeGood*
constexpr int GOOD_NAME    = 0x18;     // CTradeGood -> std::string name

inline uint64_t g_opens = 0, g_closes = 0, g_nogood = 0;
inline bool g_was_active = false;

inline std::string good_name_of(uintptr_t prov) {
    if (!livetrade::validate_region(prov + PROV_GOOD, 8)) return std::string();
    uintptr_t good = livetrade::fq(prov + PROV_GOOD);
    if (!good || !livetrade::validate_region(good + GOOD_NAME, 0x20)) return std::string();
    uint64_t sz = *(uint64_t*)(good + GOOD_NAME + 0x10), cap = *(uint64_t*)(good + GOOD_NAME + 0x18);
    if (sz == 0 || sz > 64 || cap < sz) return std::string();
    const char* p = (const char*)(good + GOOD_NAME);
    if (cap >= 16) {
        uintptr_t hp = *(uintptr_t*)(good + GOOD_NAME);
        if (!hp || !livetrade::validate_region(hp, sz + 1)) return std::string();
        p = (const char*)hp;
    }
    return std::string(p, (size_t)sz);
}

// the province view, when it exists (IGI -> holder -> +0x10)
inline uintptr_t province_view() {
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + 0x1E00, 8)) return 0;
    uintptr_t igi = livetrade::fq(g + 0x1E00);
    if (!igi || !livetrade::validate_region(igi + IGI_HOLDER, 8)) return 0;
    uintptr_t holder = livetrade::fq(igi + IGI_HOLDER);
    if (!holder || !livetrade::validate_region(holder + HOLDER_VIEW, 8)) return 0;
    return livetrade::fq(holder + HOLDER_VIEW);
}

// the engine's own visibility rule (0x1348370)
inline bool view_visible(uintptr_t view) {
    if (!view) return false;
    if (livetrade::validate_region(view + VIEW_GUI, 8)) {
        uintptr_t w = livetrade::fq(view + VIEW_GUI);
        if (w && livetrade::validate_region(w + WIN_VISIBLE, 1) && livetrade::fb(w + WIN_VISIBLE)) return true;
    }
    if (livetrade::validate_region(view + VIEW_SMALL, 8)) {
        uintptr_t sv = livetrade::fq(view + VIEW_SMALL);
        if (sv && livetrade::validate_region(sv + SMALL_GUI, 8)) {
            uintptr_t sw = livetrade::fq(sv + SMALL_GUI);
            if (sw && livetrade::validate_region(sw + WIN_VISIBLE, 1) && livetrade::fb(sw + WIN_VISIBLE)) return true;
        }
    }
    return false;
}

// per frame, BEFORE viewmode::poll (game thread; every field is written on it)
inline void frame() {
    uintptr_t view = province_view();
    bool active = view_visible(view);
    if (!active) {
        if (g_was_active) { g_closes++; g_was_active = false; }
        viewmode::g_click_want.clear();              // window closed: the aggregate view, everything back
        return;
    }
    uintptr_t prov = livetrade::validate_region(view + VIEW_PROV, 8) ? livetrade::fq(view + VIEW_PROV) : 0;
    std::string good;
    if (prov && livetrade::validate_region(prov + PROV_ID, 4) && livetrade::fi(prov + PROV_ID) > 0)
        good = good_name_of(prov);
    if (good.empty()) { viewmode::g_click_want.clear(); g_nogood++; return; }   // wasteland/sea/no good
    if (!g_was_active) { g_opens++; g_was_active = true; }
    viewmode::g_click_want = good;                   // viewmode maps it to a live good or aggregate
}

} // namespace selprov
