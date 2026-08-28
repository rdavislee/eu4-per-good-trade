// Offline timing of the tick's routing term (TESTING.md H3, the launch-free half): builds the 1444
// field, solves every live good's graph, precomputes reach exactly as the DLL does (g_plan.reach),
// and times econ::route over all goods -- once with the precomputed reach (the live tick's path) and
// once letting route() recompute reach_sets per good (the reference path), so the design choice is
// measured, not assumed. Usage: routetime <eu4_root> <save> [iterations]
#include <cstdio>
#include <chrono>
#include <map>
#include <string>
#include <vector>
#include "gamedata.h"
#include "save.h"
#include "field.h"
#include "drain.h"
#include "economy.h"
using namespace std;
using clk = chrono::high_resolution_clock;

int main(int argc, char** argv) {
    if (argc < 3) { fprintf(stderr, "usage: routetime <eu4_root> <save> [iters]\n"); return 2; }
    string root = argv[1], savep = argv[2];
    int iters = argc >= 4 ? atoi(argv[3]) : 50;
    auto tn = gamedata::load_tradenodes(root + "/common/tradenodes/00_tradenodes.txt");
    auto sm = gamedata::load_static_mods(root);
    auto base_prices = gamedata::load_prices(root);
    auto sd = save::load(savep);
    field::Field f = field::build(tn, sm, sd, base_prices);
    int N = f.N;

    // synthetic standings: one collector + a couple of steerers per node, so the per-node inner
    // loops (power sums, steer split, reach lookups) run at a realistic width without the game
    vector<econ::NodeStandings> st(N);
    map<int, vector<int>> collect_nodes;
    drain::Graph g; g.N = f.N; g.und = tn.und; g.edges_und = tn.edges_und;
    for (int n = 0; n < N; n++) {
        econ::Standing c{}; c.country = 1 + n; c.power = 5.0; c.collects = true; c.steer_to = -1; c.is_capital = true;
        st[n].entries.push_back(c); collect_nodes[c.country].push_back(n);
        for (int j = 0; j < (int)tn.und[n].size() && j < 3; j++) {
            econ::Standing s{}; s.country = 1000 + n * 8 + j; s.power = 2.0 + j; s.collects = false; s.steer_to = tn.und[n][j];
            st[n].entries.push_back(s);
        }
    }

    // every live good's graph + its reach (what the DLL precomputes into g_plan.reach)
    vector<vector<pair<int, int>>> graphs;
    vector<vector<double>> inject;
    vector<vector<vector<char>>> reach;
    for (int gi = 0; gi < (int)f.goods.size(); gi++) {
        if (!f.live[gi]) continue;
        vector<double> b(N); for (int n = 0; n < N; n++) b[n] = f.S[gi][n] - f.C[gi][n];
        drain::Result r = drain::run(g, b, f.tie_cost_edge, f.node_wealth, f.S[gi], f.C[gi]);
        graphs.push_back(r.directed);
        vector<double> inj(N, 0.0);
        for (auto& row : f.rows) if (f.gidx.count(row.good) && f.gidx[row.good] == gi && row.node >= 0 && row.node < N) inj[row.node] += row.trade_value;
        inject.push_back(inj);
        vector<vector<int>> outs(N); for (auto& [u, v] : r.directed) outs[u].push_back(v);
        reach.push_back(econ::reach_sets(N, outs));
    }
    int G = (int)graphs.size();
    printf("field: %d nodes, %d live goods; timing %d iterations of the full route sweep\n", N, G, iters);

    auto sweep = [&](bool precomp) {
        double us = 1e30;
        for (int it = 0; it < iters; it++) {
            auto t0 = clk::now();
            for (int k = 0; k < G; k++)
                econ::route(N, graphs[k], inject[k], st, collect_nodes, 0.05, precomp ? &reach[k] : nullptr);
            double ms = chrono::duration<double, milli>(clk::now() - t0).count();
            if (ms < us) us = ms;
        }
        return us;
    };
    double with = sweep(true), without = sweep(false);
    printf("  route sweep, reach PRECOMPUTED (the live tick's path):   %.2f ms  (best of %d)\n", with, iters);
    printf("  route sweep, reach recomputed per good (reference path): %.2f ms\n", without);
    printf("  reach precompute saves %.2f ms/tick (%.0f%%)\n", without - with, 100.0 * (without - with) / without);
    return 0;
}
