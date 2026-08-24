// THE TICK HOOK (spec 2.6): write the model's economy inside the engine's own monthly trade
// update, in the window between the value pass and the collector division.
//
// The monthly driver 0xB4BA90 ends with two loops:
//
//   0xB4BEF8:  for each node in calc order:  call 0xB52160   (the value pass)
//   0xB4BF07   jne -> loop
//   0xB4BF09:  rbx = mgr->nodes; rax = mgr->count           <-- WE HOOK HERE
//   0xB4BF30:  for each node:  call 0xB584F0                 (pass 10: collector division,
//              which computes rec.total = node.current * rec.power_fraction/1000, then
//              rec.money, then CCountry::AddDelayedIncome(country, 2 /*trade*/, &money))
//
// Hooking at 0xB4BF09 means every node's `current` (+0xB0) and every country record's
// `power_fraction` (+0x2C) are final, and nothing recomputes them before pass 10 reads them.
// So writing the model's collectible pool and the model's per-country shares there makes the
// ENGINE'S OWN division pay out the model's income -- into the treasury and the ledger's trade
// category -- with no second income path of our own. That is exactly what spec 2.6 asks for:
// "feeding the engine the collectible pool is sufficient".
//
// The handler must be fast (spec H3: the added tick time must be imperceptible), so it does no
// LP work: the per-good orientations are solved once and cached, and the handler only re-routes
// the live inject over them and writes. Registers at the site: rsi = CTradeManager.
#pragma once
#include <windows.h>
#include <atomic>
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"
#include "install.h"
#include "../src/economy.h"

namespace ticklive {

// what the handler needs, precomputed at attach
struct Plan {
    std::vector<std::vector<std::pair<int, int>>> graphs;  // per live good, field-indexed
    std::vector<int> slots;                                // engine trade_goods_size slot per good
    std::vector<double> prices;                            // current price per good
    std::vector<std::string> names;                        // field index -> node name
    std::vector<std::vector<int>> link_targets;            // node -> outgoing destinations
    std::vector<std::pair<int, int>> phi_w;                // the installed orientation
    std::vector<std::vector<std::vector<char>>> reach;      // per good, precomputed reachability
    int N = 0;
    bool ready = false;
};

inline Plan g_plan;
inline std::string g_log;
inline std::atomic<int> g_ticks{0};
inline std::atomic<bool> g_inside{false};
inline detour::Hook g_hook;

// The whole model write, driven from live memory. Called on the game's own thread inside the
// monthly update. Returns the number of nodes written.
inline int apply(uintptr_t mgr) {
    if (!g_plan.ready) return 0;
    auto sim = livetrade::read_sim_nodes();
    if (sim.empty()) return 0;
    // name the live nodes by engine id (the map was resolved at attach and keyed by stable id)
    for (auto& s : sim) {
        auto it = install::g_id_to_name.find(s.index);
        if (it != install::g_id_to_name.end()) s.name = it->second;
    }
    int gc = 0, matched = 0;
    auto inject = install::gather_inject(sim, g_plan.names, gc, matched);
    std::map<int, std::vector<int>> collect_nodes;
    auto st = install::read_standings_field(sim, g_plan.names, g_plan.link_targets, collect_nodes);

    std::vector<econ::GoodFlow> per_good;
    std::vector<std::vector<double>> inj_field;
    per_good.reserve(g_plan.graphs.size());
    for (size_t k = 0; k < g_plan.graphs.size(); k++) {
        std::vector<double> inj(g_plan.N, 0.0);
        int slot = g_plan.slots[k];
        if (slot < gc)
            for (int n = 0; n < g_plan.N; n++) inj[n] = inject[slot][n] * g_plan.prices[k];
        const std::vector<std::vector<char>>* R =
            k < g_plan.reach.size() ? &g_plan.reach[k] : nullptr;
        per_good.push_back(
            econ::route(g_plan.N, g_plan.graphs[k], inj, st, collect_nodes, 0.05, R));
        inj_field.push_back(std::move(inj));
    }
    auto agg = econ::aggregate(g_plan.N, per_good, inj_field);
    auto gross = econ::gross_link_flows(per_good);

    // links first: install_aggregate derives outgoing from what each node actually holds
    install::install_links(sim, g_plan.names, gross, install::g_id_to_name);
    int wrote = install::install_aggregate(sim, g_plan.names, agg);
    // per-country shares of the pool, so the engine's own pass 10 pays out the model's income.
    // Behind a marker until the engine's own power_fraction semantics are observed (see the
    // standings dump): overwriting it blind could disturb displays that read the same field.
    if (livetrade::marker_present("INCOME"))
        install::install_power_shares(sim, g_plan.names, st);
    return wrote;
}

inline void handler(detour::Regs* r) {
    // never re-enter (the driver can run more than once in a frame at high speed)
    bool expected = false;
    if (!g_inside.compare_exchange_strong(expected, true)) return;
    int wrote = 0;
    uintptr_t mgr = r->rsi;
    // measure the added tick cost -- spec H3 requires it to be imperceptible, and an earlier
    // build (a VirtualQuery per field) stalled the monthly update for ~10 s in the live game.
    LARGE_INTEGER t0{}, t1{}, freq{};
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&t0);
    if (mgr) wrote = apply(mgr);
    QueryPerformanceCounter(&t1);
    double ms = freq.QuadPart ? (double)(t1.QuadPart - t0.QuadPart) * 1000.0 / freq.QuadPart : 0.0;
    int t = ++g_ticks;
    if (t <= 8 || (t % 12) == 0) {
        std::ofstream lg(g_log, std::ios::app);
        lg << "[tick] monthly update " << t << ": wrote " << wrote
           << " nodes inside the engine's value pass (pre-division), " << ms << " ms\n";
    }
    g_inside = false;
}

// Install the inline hook. The expected bytes are the exact 20 bytes at 0xB4BF09 (four whole
// instructions, no RIP-relative operand, no branch), verified offline with capstone:
//   48 8b 5e 18              mov  rbx, [rsi+0x18]
//   48 63 46 24              movsxd rax, [rsi+0x24]
//   48 8b 74 24 60           mov  rsi, [rsp+0x60]
//   48 69 f8 38 01 00 00     imul rdi, rax, 0x138
// A byte mismatch means a different build: refuse (spec 2.5).
inline bool install_hook(std::string* err) {
    uintptr_t base = livetrade::module_base();
    uintptr_t site = base + 0xB4BF09;
    std::vector<uint8_t> expected{
        0x48, 0x8b, 0x5e, 0x18,
        0x48, 0x63, 0x46, 0x24,
        0x48, 0x8b, 0x74, 0x24, 0x60,
        0x48, 0x69, 0xf8, 0x38, 0x01, 0x00, 0x00};
    if (!detour::install(g_hook, site, expected, &handler, "monthly_value_pass")) {
        if (err) *err = g_hook.error;
        return false;
    }
    return true;
}

inline void remove_hook() { detour::remove(g_hook); }

} // namespace ticklive
