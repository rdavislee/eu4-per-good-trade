// SWAP-ON-VIEW (spec 1.12; tests D2, D3, D4).
//
// "Clicking a province switches province colouring to the vanilla trade-goods rendering for that
// good and redirects the arrow layer to that good's graph -- and the SAME WIDGETS REPOPULATE WITH
// THAT GOOD'S NUMBERS: the node box the good's value at the node, the window all six fields for
// the good alone." Spec 1.12 explicitly chooses swap-on-view precisely so the engine never needs
// thirty fields per node: only the selected good's numbers are displayed at a time.
//
// That is the whole trick here. The node window, the map-mode box and the tooltips do not store a
// total -- each recomputes local + Sigma incoming - outgoing from the sim node every time it
// draws (see OFFSETS.md). So displaying one good's economy needs NO UI hook at all: install that
// good's per-good values into the same sim fields the aggregate normally writes, and every
// consumer follows. A sink for the selected good then shows collected_share == 1 by construction
// (it forwards nothing), which is what test D3 looks for.
//
// The arrow layer is the half that still needs the definition graph to be re-orientable; the
// numbers do not. The selected good is DLL-owned state, because the engine has none: no
// "selected trade good" string or field exists anywhere in the binary (UI RE, negative result).
#pragma once
#include <fstream>
#include <string>
#include <vector>
#include "livetrade.h"

namespace viewmode {

// -1 = aggregate view (Sigma over all goods, the default). Otherwise an index into the solver's
// live-good list, meaning "show only this good".
inline int g_selected = -1;
inline std::string g_selected_name;
// THE PROVINCE CLICK (spec 1.12 / test D1; user 2026-08-27): clicking a province selects its trade
// good's view; closing the window (or clicking water) returns to the aggregate. clickview.h writes
// this each frame from the engine's own province view; the pgt.VIEW marker (the test harness)
// still takes precedence when present.
inline std::string g_click_want;

// Read the requested view from a marker file next to the DLL. `pgt.VIEW` holding a good name
// selects that good; no marker (or an empty one) means the aggregate view. This is the test
// harness for the view; the player-facing trigger is the province click, which needs the
// arrow-layer work to be meaningful anyway.
inline void poll(const std::vector<std::string>& good_names, std::ofstream* log = nullptr) {
    std::string want;
    if (livetrade::marker_present("VIEW")) {
        std::ifstream f(livetrade::self_dir() + "\\pgt.VIEW");
        std::getline(f, want);
        while (!want.empty() && (want.back() == '\r' || want.back() == '\n' || want.back() == ' '))
            want.pop_back();
    }
    if (want.empty()) want = g_click_want;
    int next = -1;
    if (!want.empty())
        for (int i = 0; i < (int)good_names.size(); i++)
            if (good_names[i] == want) { next = i; break; }
    if (next != g_selected) {
        g_selected = next;
        g_selected_name = (next < 0) ? "" : good_names[next];
        if (log)
            *log << "  [view] " << (next < 0 ? std::string("AGGREGATE (all goods)")
                                             : ("PER-GOOD: " + g_selected_name)) << "\n";
    }
}

inline bool per_good() { return g_selected >= 0; }

} // namespace viewmode
