// SYNTHETIC SHOCK (spec 2.2 item 8; tests F1/F2/F3/F4). Change the world and watch the
// orientation follow.
//
// TESTING.md words these as console scenarios ("nudge development via console until it flips"),
// but EU4 ignores synthetic keyboard input on this machine -- it reads raw input, so no injected
// keystroke reaches the console. Writing the province's development field directly is the same
// state change the console's `develop` command makes, applied to the same memory the engine
// reads, so the stimulus is equivalent and the observation is unchanged: the next monthly
// re-solve reads the live province table (liveworld.h), re-solves, and the map must follow.
//
// Province fields (build 835bfdf8): array at G+0x1CA8, stride 0x2E10, subscript == province id;
// base_tax +0x3E4, base_production +0x3E8 (int32 x1000), owning trade node +0xE8.
#pragma once
#include <windows.h>
#include <fstream>
#include <string>
#include <vector>
#include "livetrade.h"
#include "liveworld.h"

namespace shock {

inline bool g_applied = false;

// Multiply base_production (and base_tax) of every province belonging to `node_obj`.
// Returns how many provinces were changed.
inline int pump_node(uintptr_t node_obj, double factor, std::ofstream& log) {
    uintptr_t g = livetrade::game_singleton();
    if (!g) return 0;
    uintptr_t base = livetrade::rq(g + 0x1CA8), endp = livetrade::rq(g + 0x1CB0);
    if (!base || endp <= base) return 0;
    size_t span = endp - base;
    int count = (int)(span / liveworld::PROV_STRIDE);
    if (count <= 0 || count > 20000 || !livetrade::validate_region(base, span)) return 0;
    int changed = 0;
    for (int i = 0; i < count; i++) {
        uintptr_t p = base + (uintptr_t)i * liveworld::PROV_STRIDE;
        if (livetrade::fq(p + liveworld::PROV_NODE) != node_obj) continue;
        int32_t bp = livetrade::fi(p + liveworld::PROV_BASE_PROD);
        int32_t bt = livetrade::fi(p + liveworld::PROV_BASE_TAX);
        int32_t nbp = (int32_t)(bp * factor), nbt = (int32_t)(bt * factor);
        DWORD old = 0;
        if (VirtualProtect((void*)(p + liveworld::PROV_BASE_PROD), 8, PAGE_READWRITE, &old)) {
            *(int32_t*)(p + liveworld::PROV_BASE_PROD) = nbp;
            VirtualProtect((void*)(p + liveworld::PROV_BASE_PROD), 8, old, &old);
        }
        if (VirtualProtect((void*)(p + liveworld::PROV_BASE_TAX), 8, PAGE_READWRITE, &old)) {
            *(int32_t*)(p + liveworld::PROV_BASE_TAX) = nbt;
            VirtualProtect((void*)(p + liveworld::PROV_BASE_TAX), 8, old, &old);
        }
        changed++;
        if (changed <= 5)
            log << "     prov#" << livetrade::fi(p + liveworld::PROV_ID)
                << " base_prod " << bp / 1000.0 << " -> " << nbp / 1000.0
                << ", base_tax " << bt / 1000.0 << " -> " << nbt / 1000.0 << "\n";
    }
    return changed;
}

// Apply the shock named by a marker file's content, once. The marker `pgt.SHOCK` holds a node
// name; the node is resolved through the authoritative id->name map.
inline void maybe_apply(const std::string& logpath,
                        const std::vector<livetrade::SimNode>& sim,
                        const std::map<int, std::string>& id_to_name) {
    // Removing the marker re-arms the shock, so a test can fire several in one session
    // (shock A, observe, remove marker, shock B, observe) without restarting the game.
    if (!livetrade::marker_present("SHOCK")) { g_applied = false; return; }
    if (g_applied) return;
    std::string path = livetrade::self_dir() + "\\pgt.SHOCK";
    std::ifstream f(path);
    std::string want;
    std::getline(f, want);
    while (!want.empty() && (want.back() == '\r' || want.back() == '\n' || want.back() == ' '))
        want.pop_back();
    if (want.empty()) return;
    std::ofstream log(logpath, std::ios::app);
    log << "--- SHOCK: pumping node '" << want << "' ---\n";
    for (auto& s : sim) {
        auto it = id_to_name.find(s.index);
        if (it == id_to_name.end() || it->second != want) continue;
        int n = pump_node(s.obj, 20.0, log);
        log << "   pumped " << n << " provinces in '" << want << "' by 20x\n";
        g_applied = true;
        return;
    }
    log << "   node '" << want << "' not found\n";
    g_applied = true;      // don't retry forever
}

} // namespace shock
