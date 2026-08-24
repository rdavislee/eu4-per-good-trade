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
#include "resolver.h"
#include "arrows.h"
#include "shock.h"
#include "relink.h"
#include "viewmode.h"
#include "assign.h"
#include "caravan.h"
#include "../src/economy.h"

namespace ticklive {

inline std::atomic<bool> g_verify_pending;

// what the handler needs, precomputed at attach
struct Plan {
    std::vector<std::vector<std::pair<int, int>>> graphs;  // per live good, field-indexed
    std::vector<int> slots;                                // engine trade_goods_size slot per good
    std::vector<double> prices;                            // current price per good
    std::vector<std::string> names;                        // field index -> node name
    std::vector<std::string> good_names;                   // parallel to graphs: the good's name
    std::vector<std::vector<int>> link_targets;            // node -> outgoing destinations
    std::vector<std::pair<int, int>> phi_w;                // the installed orientation
    std::vector<std::pair<int, int>> phi_w_prev;           // previous, to name the flips
    std::vector<std::vector<std::vector<char>>> reach;      // per good, precomputed reachability
    int N = 0;
    int generation = 0;
    bool ready = false;
};

inline Plan g_plan;
inline std::string g_log;
inline std::atomic<int> g_ticks{0};
inline std::atomic<bool> g_inside{false};
inline detour::Hook g_hook;

// ---------------------------------------------------------------------------------------
// TEST E1 (spec 2.6 / 3.10): "ledger trade income = powershare_C(n) . collect_pool(n) summed
// over the country's collecting nodes, to the ducat".
//
// We write collect_pool(n) into node+0xB0 and leave the engine's own powershare (rec+0x2C)
// alone, so the engine's pass 10 computes rec.total = pool x powershare for every collector.
// The check is therefore: predict Sigma_n pool(n) x pf(C,n) at tick N (right after our write,
// before pass 10 runs), then at tick N+1 read what pass 10 actually stored in rec.total and
// compare. Agreement to the milli-ducat proves the engine is dividing the MODEL's economy.
inline std::map<int, double> g_predicted;     // country index -> predicted Sigma total
inline int g_predict_tick = -1;

inline void predict_income(const std::vector<livetrade::SimNode>& sim,
                           const std::vector<std::string>& names,
                           const std::vector<double>& pool_written_monthly) {
    g_predicted.clear();
    auto byname = install::live_by_name(sim);
    for (int fn = 0; fn < (int)names.size() && fn < (int)pool_written_monthly.size(); fn++) {
        auto it = byname.find(names[fn]);
        if (it == byname.end()) continue;
        double pool = pool_written_monthly[fn];
        for (auto& rec : livetrade::read_standings(sim[it->second].obj)) {
            if (rec.power_fraction <= 0) continue;          // engine pays only its collectors
            g_predicted[livetrade::country_index_of(rec.tag_index)] += pool * rec.power_fraction;
        }
    }
}

// read back what pass 10 actually stored, and report the reconciliation
inline void verify_income(const std::vector<livetrade::SimNode>& sim, std::ofstream& lg) {
    if (g_predicted.empty()) return;
    std::map<int, double> actual;
    for (auto& s : sim)
        for (auto& rec : livetrade::read_standings(s.obj)) {
            if (rec.total == 0) continue;
            actual[livetrade::country_index_of(rec.tag_index)] += rec.total;
        }
    int checked = 0, agree = 0;
    double worst = 0; int worst_c = -1;
    for (auto& [c, pred] : g_predicted) {
        auto a = actual.find(c);
        double got = (a == actual.end()) ? 0.0 : a->second;
        double d = std::fabs(got - pred);
        checked++;
        if (d <= 0.002 + 0.001 * checked) agree++;       // milli-ducat grid, per-node rounding
        if (d > worst) { worst = d; worst_c = c; }
    }
    lg << "[E1] engine-divided income vs model prediction: " << agree << "/" << checked
       << " countries agree; worst |diff| = " << worst << " ducats (country #" << worst_c << ")\n";
    // a few named samples
    int shown = 0;
    for (auto& [c, pred] : g_predicted) {
        auto a = actual.find(c);
        double got = (a == actual.end()) ? 0.0 : a->second;
        if (pred < 0.5) continue;
        lg << "     country#" << c << " predicted=" << pred << " engine=" << got
           << " diff=" << (got - pred) << "\n";
        if (++shown >= 6) break;
    }
}

// The whole model write, driven from live memory. Called on the game's own thread inside the
// monthly update. Returns the number of nodes written.
inline int apply(uintptr_t mgr) {
    if (!g_plan.ready) return 0;
    // Adopt a newly published orientation, if the background solver produced one since the last
    // tick. The swap is whole-orientation: a tick never mixes old and new graphs.
    {
        resolver::Orientation o = resolver::snapshot();
        if (!o.graphs.empty() && o.generation != g_plan.generation) {
            g_plan.graphs = o.graphs;
            g_plan.slots  = o.slots;
            g_plan.prices = o.prices;
            g_plan.good_names = o.good_names;
            g_plan.reach  = o.reach;
            g_plan.phi_w_prev = g_plan.phi_w;
            g_plan.phi_w  = o.phi_w;
            g_plan.generation = o.generation;
            // Redraw the map arrows to the new Phi_w (spec 1.12: Phi_w is the drawn direction).
            // Runs here because the layer rebuild touches render objects and must be on the
            // game thread. Field indices -> engine node ids via the authoritative name map.
            if (livetrade::marker_present("ARROWS")) {
                std::map<std::string, int> name_to_id;
                for (auto& [id, nm] : install::g_id_to_name) name_to_id[nm] = id;
                std::set<std::pair<int, int>> desired;
                for (auto& [u, v] : o.phi_w) {
                    if (u >= (int)g_plan.names.size() || v >= (int)g_plan.names.size()) continue;
                    auto a = name_to_id.find(g_plan.names[u]);
                    auto b = name_to_id.find(g_plan.names[v]);
                    if (a == name_to_id.end() || b == name_to_id.end()) continue;
                    desired.insert({a->second, b->second});
                }
                // name the links whose drawn direction changed, so the flip can be found on
                // the map (test F1 wants it confirmed by eye, not by log line)
                {
                    std::set<std::pair<int,int>> prev;
                    for (auto& [u, v] : g_plan.phi_w_prev) prev.insert({u, v});
                    std::ofstream lg3(g_log, std::ios::app);
                    for (auto& [u, v] : o.phi_w)
                        if (prev.count({v, u}))
                            lg3 << "[flip] " << g_plan.names[v] << " -> " << g_plan.names[u]
                                << "  became  " << g_plan.names[u] << " -> " << g_plan.names[v] << "\n";
                }
                // REORIENT THE DEFINITION GRAPH -- what actually drives the node window's
                // incoming/outgoing tabs AND the arrow layer. Reversing render geometry alone
                // changed neither (observed in the running game).
                int relinked = -1;
                if (livetrade::marker_present("RELINK")) {
                    std::ofstream lgr(g_log, std::ios::app);
                    auto sim_now = livetrade::read_sim_nodes();   // needed for the steer clamp
                    // by NAME: the solver's field indices map straight to node names, so the
                    // engine's two index spaces never enter the picture.
                    std::set<std::pair<std::string, std::string>> want;
                    for (auto& [u, v] : o.phi_w)
                        if (u < (int)g_plan.names.size() && v < (int)g_plan.names.size())
                            want.insert({g_plan.names[u], g_plan.names[v]});
                    if (relink::capture(lgr)) {
                        relinked = relink::apply(want, lgr, sim_now);
                        if (livetrade::marker_present("LISTDUMP"))
                            relink::dump_lists(g_log, {"baltic_sea", "novgorod", "lubeck"});
                    }
                }
                int flipped = livetrade::marker_present("RELINK") ? relinked
                                                                  : arrows::set_directions(desired);
                bool rebuilt = flipped > 0 ? arrows::rebuild() : true;
                std::ofstream lg2(g_log, std::ios::app);
                lg2 << "[arrows] re-oriented " << flipped << " drawn routes, layer rebuild "
                    << (rebuilt ? "OK" : "SKIPPED (map renderer not captured yet)")
                    << " | desired=" << desired.size() << " defs=" << arrows::g_defs_seen
                    << " entries=" << arrows::g_entries_seen
                    << " fwd=" << arrows::g_matched_fwd << " rev=" << arrows::g_matched_rev
                    << " unmatched=" << arrows::g_unmatched
                    << " src=" << arrows::g_def_source << "\n";
            }
            std::ofstream lg(g_log, std::ios::app);
            lg << "[tick] adopted orientation gen " << o.generation << "\n";
        }
    }
    // ask the background solver to recompute for next month (never blocks the game thread)
    resolver::request();
    auto sim = livetrade::read_sim_nodes();
    if (sim.empty()) return 0;
    // name the live nodes by engine id (the map was resolved at attach and keyed by stable id)
    for (auto& s : sim) {
        auto it = install::g_id_to_name.find(s.index);
        if (it != install::g_id_to_name.end()) s.name = it->second;
    }
    shock::maybe_apply(g_log, sim, install::g_id_to_name);
    int gc = 0, matched = 0;
    auto inject = install::gather_inject(sim, g_plan.names, gc, matched);
    std::map<int, std::vector<int>> collect_nodes;
    auto st = install::read_standings_field(sim, g_plan.names, g_plan.link_targets, collect_nodes);
    // spec 1.7: merchants assigned to a link END the engine has no index for (a link drawn INTO
    // this node) live in our own table and are merged on top of the engine's own assignments.
    assign::poll(g_log);
    int assigned = assign::merge(st, g_plan.names);
    if (assigned && (g_ticks.load() % 12) == 0) {
        std::ofstream la(g_log, std::ios::app);
        la << "  [assign] " << assigned << " DLL-owned merchant assignments active\n";
    }

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
    // SWAP-ON-VIEW (spec 1.12): in a per-good view the SAME fields carry that good's numbers
    // alone, so the aggregate is taken over just the selected good.
    viewmode::poll(g_plan.good_names);
    std::vector<econ::GoodFlow> shown = per_good;
    std::vector<std::vector<double>> shown_inj = inj_field;
    if (viewmode::per_good() && viewmode::g_selected < (int)per_good.size()) {
        shown.assign(1, per_good[viewmode::g_selected]);
        shown_inj.assign(1, inj_field[viewmode::g_selected]);
    }
    // spec 1.7 / C5: caravan power only where a merchant actually steers a good on its link.
    // A country is "steering" at a node if any live good's graph orients an edge from that node
    // toward the link end the merchant sits on.
    {
        std::set<std::pair<int, int>> steering;
        std::map<std::string, int> nid;
        for (auto& [id, nm] : install::g_id_to_name) nid[nm] = id;
        for (int fn = 0; fn < g_plan.N && fn < (int)st.size(); fn++) {
            auto ni = nid.find(g_plan.names[fn]);
            if (ni == nid.end()) continue;
            for (auto& e : st[fn].entries) {
                if (e.steer_to < 0) continue;
                bool carries = false;
                for (auto& F : per_good) {
                    auto it = F.flow[fn].find(e.steer_to);
                    if (it != F.flow[fn].end() && it->second > 0) { carries = true; break; }
                }
                if (carries) steering.insert({e.country, ni->second});
            }
        }
        caravan::g_steering.swap(steering);
    }
    auto agg = econ::aggregate(g_plan.N, shown, shown_inj);
    auto gross = econ::gross_link_flows(shown);

    // links first: install_aggregate derives outgoing from what each node actually holds
    install::install_links(sim, g_plan.names, gross, install::g_id_to_name);
    int wrote = install::install_aggregate(sim, g_plan.names, agg, viewmode::per_good());

    // predict this month's per-country division: pool (what we just wrote) x the engine's own
    // powershare. Recompute the monthly pool exactly as install_aggregate did.
    {
        auto byname = install::live_by_name(sim);
        std::vector<double> pool_monthly(g_plan.N, 0.0);
        for (int fn = 0; fn < g_plan.N; fn++) {
            auto it = byname.find(g_plan.names[fn]);
            if (it == byname.end()) continue;
            pool_monthly[fn] = livetrade::fi(sim[it->second].obj + 0xB0) / 1000.0;
        }
        predict_income(sim, g_plan.names, pool_monthly);
        g_verify_pending = true;      // the verifier samples rec.total after pass 10 finishes
    }
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

// E1 VERIFIER THREAD. The handler runs BEFORE pass 10, so reading rec.total there samples
// records the engine has already reset for the new month -- which is why an in-handler read
// reported zeros. The division we want to check happens microseconds after the handler returns,
// so a worker samples shortly after each tick instead, off the game thread (spec H3).
inline std::atomic<bool> g_verify_stop{false};

inline void verify_worker() {
    while (!g_verify_stop) {
        if (g_verify_pending.exchange(false)) {
            Sleep(400);                        // let pass 10 finish
            auto sim = livetrade::read_sim_nodes();
            if (!sim.empty()) {
                std::ofstream lg(g_log, std::ios::app);
                verify_income(sim, lg);
            }
        }
        Sleep(120);
    }
}

inline void start_verifier() {
    CreateThread(nullptr, 0, [](LPVOID) -> DWORD { verify_worker(); return 0; }, nullptr, 0, nullptr);
}

} // namespace ticklive
