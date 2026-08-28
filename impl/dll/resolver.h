// THE MONTHLY RE-SOLVE (spec 2.6 "recomputed on a fixed monthly tick"; tests F1/F3/F4/F5).
//
// The orientation is a function of the WORLD, so it has to be recomputed as the world changes:
// development grows, war brings devastation, prices move, colonies appear. Until the field came
// from live memory the graphs could never move; now they can, and this is what moves them.
//
// Cost discipline (spec H3): the full 30-graph solve is ~0.1-0.3 s, which is far too long to sit
// on the game thread inside the monthly update. So the solve runs on a BACKGROUND thread against
// a snapshot of the live world, and publishes its result atomically. The tick hook keeps using
// the currently published orientation -- it never blocks, and never waits for a solve.
//
// Determinism is unaffected (spec 2.1/2.8): the solve is the same deterministic DRAIN over the
// same inputs; only WHEN it runs is off-thread. The published orientation is swapped under a
// lock so a tick either sees the whole old orientation or the whole new one, never a mix.
#pragma once
#include <windows.h>
#include <atomic>
#include <fstream>
#include <algorithm>
#include <mutex>
#include <string>
#include <vector>
#include "liveworld.h"
#include "livetrade.h"
#include "../src/economy.h"
#include "../src/field.h"
#include "../src/drain.h"
#include "../src/gamedata.h"

namespace resolver {

struct Orientation {
    std::vector<std::vector<std::pair<int, int>>> graphs;   // per live good
    std::vector<int> slots;                                  // engine tgs slot per good
    std::vector<double> prices;                              // price per good
    std::vector<std::string> good_names;                     // the good each graph belongs to
    std::vector<std::vector<std::vector<char>>> reach;       // per good reachability
    std::vector<std::pair<int, int>> phi_w;                  // the aggregate orientation
    double world_wealth = 0;
    int counted_provinces = 0;
    int generation = 0;
};

inline std::mutex g_mtx;
inline Orientation g_current;
inline std::atomic<bool> g_stop{false};
inline std::atomic<int> g_generation{0};
inline std::string g_log;
inline std::atomic<bool> g_solve_now{false};

// static inputs, loaded once
struct Statics {
    gamedata::TradeNodes tn;
    gamedata::StaticMods sm;
    std::map<std::string, double> base_prices;
    std::map<std::string, int> good_slot;
    drain::Graph graph;
    bool ready = false;
};
inline Statics g_st;

// count how many undirected edges are oriented differently between two orientations
inline int count_flips(const std::vector<std::pair<int, int>>& a,
                       const std::vector<std::pair<int, int>>& b) {
    std::set<std::pair<int, int>> sa(a.begin(), a.end());
    int flips = 0;
    for (auto& [u, v] : b) if (!sa.count({u, v}) && sa.count({v, u})) flips++;
    return flips;
}

// One full re-solve from the LIVE world. Returns false if the world could not be read.
inline bool solve_once(Orientation& out, std::string* why = nullptr) {
    if (!g_st.ready) { if (why) *why = "statics not loaded"; return false; }
    liveworld::WorldRead w = liveworld::read_world();
    if (!w.ok) { if (why) *why = "live world read failed"; return false; }
    {   // H1/INPUTS: the fingerprint of what the solve CONSUMED (spec 2.8 named this the next
        // instrument). H1 compares orientations across a save/reload; the solver itself is
        // deterministic (30/30 offline), so if two runs at the same date disagree, either the
        // inputs differ -- which this hash proves -- or the model is at fault. Order-independent
        // per province so vector order can never matter.
        uint64_t h = 1469598103934665603ull;
        auto mix = [&h](uint64_t v) { h ^= v; h *= 1099511628211ull; };
        std::vector<uint64_t> per;
        per.reserve(w.sd.provinces.size());
        for (auto& pr : w.sd.provinces) {
            uint64_t g2 = 1469598103934665603ull;
            auto m2 = [&g2](uint64_t v) { g2 ^= v; g2 *= 1099511628211ull; };
            m2((uint64_t)pr.id);
            m2((uint64_t)llround(pr.base_tax * 1000.0));
            m2((uint64_t)llround(pr.base_production * 1000.0));
            m2((uint64_t)llround(pr.devastation * 1000.0));
            for (unsigned char c : pr.trade_goods) m2(c);
            per.push_back(g2);
        }
        std::sort(per.begin(), per.end());
        for (uint64_t v : per) mix(v);
        for (auto& [gname, price] : w.sd.current_prices) {
            for (unsigned char c : gname) mix(c);
            mix((uint64_t)llround(price * 1000.0));
        }
        std::ofstream lh(g_log, std::ios::app);
        lh << "[H1/inputs] date=" << (livetrade::game_singleton() && livetrade::validate_region(livetrade::game_singleton() + 0x1DF0, 4) ? livetrade::fi(livetrade::game_singleton() + 0x1DF0) : -1) << " provinces=" << w.sd.provinces.size() << " prices=" << w.sd.current_prices.size()
           << " hash=" << std::hex << h << std::dec << (char)10;
    }
    field::Field f = field::build(g_st.tn, g_st.sm, w.sd, g_st.base_prices);
    out.graphs.clear(); out.slots.clear(); out.prices.clear(); out.reach.clear();
    out.good_names.clear();
    out.world_wealth = f.world_wealth;
    out.counted_provinces = (int)f.rows.size();

    // Phi_w -- the installed/drawn orientation (spec 1.6)
    {
        std::vector<double> b = field::b_aggregate(f);
        std::vector<double> s(f.N, 1.0 / f.N), c(f.N);
        for (int n = 0; n < f.N; n++) c[n] = s[n] - b[n];
        drain::Result r = drain::run(g_st.graph, b, f.tie_cost_edge, f.node_wealth, s, c);
        out.phi_w = r.directed;
    }
    // every live good
    for (int gi = 0; gi < (int)f.goods.size(); gi++) {
        if (!f.live[gi]) continue;
        std::vector<double> b(f.N), s = f.S[gi], c = f.C[gi];
        for (int n = 0; n < f.N; n++) b[n] = s[n] - c[n];
        drain::Result r = drain::run(g_st.graph, b, f.tie_cost_edge, f.node_wealth, s, c);
        auto slotit = g_st.good_slot.find(f.goods[gi]);
        out.slots.push_back(slotit != g_st.good_slot.end() ? slotit->second : gi + 1);
        out.prices.push_back(field::price_of(f.goods[gi], w.sd.current_prices, g_st.base_prices));
        out.graphs.push_back(r.directed);
        out.good_names.push_back(f.goods[gi]);
        std::vector<std::vector<int>> outs(f.N);
        for (auto& e : r.directed) outs[e.first].push_back(e.second);
        out.reach.push_back(econ::reach_sets(f.N, outs));
    }
    out.generation = ++g_generation;
    return true;
}

// publish a freshly solved orientation for the tick hook to use
inline void publish(const Orientation& o) {
    std::lock_guard<std::mutex> lk(g_mtx);
    g_current = o;
}

inline Orientation snapshot() {
    std::lock_guard<std::mutex> lk(g_mtx);
    return g_current;
}

// The background solver: re-solve whenever the tick hook asks, never on the game thread.
inline void solver_thread() {
    while (!g_stop) {
        if (g_solve_now.exchange(false)) {
            Orientation next;
            std::string why;
            LARGE_INTEGER t0{}, t1{}, freq{};
            QueryPerformanceFrequency(&freq);
            QueryPerformanceCounter(&t0);
            bool ok = solve_once(next, &why);
            QueryPerformanceCounter(&t1);
            double ms = freq.QuadPart
                ? (double)(t1.QuadPart - t0.QuadPart) * 1000.0 / freq.QuadPart : 0.0;
            if (ok) {
                Orientation prev = snapshot();
                int flips = prev.phi_w.empty() ? 0 : count_flips(prev.phi_w, next.phi_w);
                int good_flips = 0;
                if (prev.graphs.size() == next.graphs.size())
                    for (size_t k = 0; k < next.graphs.size(); k++)
                        good_flips += count_flips(prev.graphs[k], next.graphs[k]);
                publish(next);
                std::ofstream lg(g_log, std::ios::app);
                lg << "[resolve] gen " << next.generation << ": " << next.counted_provinces
                   << " provinces, world wealth " << next.world_wealth << ", " << ms << " ms"
                   << " -- Phi_w flips vs previous: " << flips
                   << ", per-good flips: " << good_flips << "\n";
            } else {
                std::ofstream lg(g_log, std::ios::app);
                lg << "[resolve] FAILED: " << why << "\n";
            }
        }
        Sleep(150);
    }
}

inline bool g_started = false;
inline void start(const std::string& logpath) {
    if (g_started) return;            // one solver thread per process (reviewed)
    g_started = true;
    g_log = logpath;
    CreateThread(nullptr, 0, [](LPVOID) -> DWORD { solver_thread(); return 0; }, nullptr, 0, nullptr);
}

// ask for a re-solve (called from the tick hook; never blocks)
inline void request() { g_solve_now = true; }

} // namespace resolver
