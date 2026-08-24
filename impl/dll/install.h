// Installing the per-good economy into the engine (spec 1.8, 2.6).
//
// This is what the mod actually DOES at runtime, in-process:
//   1. read the engine's own produced quantities -- per node, per good -- from each CTradeNode's
//      trade_goods_size vector (+0x108), which is exactly spec 1.8's `inject_g(n)` basis;
//   2. run the shipped DRAIN solver over the model's own orientation inputs to get the per-good
//      graphs and Phi_w (the same code the reference implementation runs -- spec 2.8 requires
//      them to agree on orientation exactly);
//   3. route each good's injected value along its own graph and sum per node;
//   4. write the routed totals back into the engine's node fields (local/outgoing), so the
//      game's own displays, ledger and AI read the model's numbers (Goal 7).
//
// Step 4 uses the write path proven in livetrade.h. The ROUTING here is the per-good flow of
// spec 1.8: at a sink the good is fully collected; elsewhere it splits across the good's
// outgoing links (evenly in the no-merchant baseline -- merchant steering is the AI layer).
#pragma once
#include <cmath>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"

namespace install {

struct GoodRoute {
    // per-good directed graph over node indices, from the solver
    std::vector<std::pair<int, int>> directed;
    std::vector<int> sinks;
};

// Route one good's injected values along its graph. inject[n] is the engine's produced value at
// node n for this good; returns the value arriving/collected at each node (spec 1.8's realized
// flow under the no-merchant even split).
inline std::vector<double> route_good(int N, const std::vector<std::pair<int, int>>& directed,
                                      const std::vector<double>& inject) {
    std::vector<std::vector<int>> outs(N);
    std::vector<int> indeg(N, 0);
    for (auto& [u, v] : directed) { outs[u].push_back(v); indeg[v]++; }
    // topological order (the graph is acyclic by construction -- spec 1.1)
    std::vector<int> order;
    std::vector<int> ind = indeg;
    std::vector<int> q;
    for (int i = 0; i < N; i++) if (ind[i] == 0) q.push_back(i);
    while (!q.empty()) {
        int x = q.back(); q.pop_back();
        order.push_back(x);
        for (int y : outs[x]) if (--ind[y] == 0) q.push_back(y);
    }
    std::vector<double> carried(N, 0.0), collected(N, 0.0);
    for (int n = 0; n < N; n++) carried[n] = inject[n];
    for (int n : order) {
        if (outs[n].empty()) {                 // sink for this good: fully collected here
            collected[n] += carried[n];
            continue;
        }
        double share = carried[n] / outs[n].size();
        for (int m : outs[n]) carried[m] += share;
    }
    return collected;
}

// Read the engine's per-node, per-good produced values (spec 1.8's inject).
inline std::vector<std::vector<double>> read_inject(const std::vector<livetrade::SimNode>& sim,
                                                    int& goods_count) {
    goods_count = 0;
    for (auto& s : sim) goods_count = std::max<int>(goods_count, (int)s.goods.size());
    std::vector<std::vector<double>> inject(goods_count, std::vector<double>(sim.size(), 0.0));
    for (size_t n = 0; n < sim.size(); n++)
        for (size_t k = 0; k < sim[n].goods.size(); k++)
            inject[k][n] = sim[n].goods[k] / 1000.0;
    return inject;
}

// Install: write each node's routed total into the engine's local_value field.
// Returns the number of nodes written.
inline int install_economy(const std::vector<livetrade::SimNode>& sim,
                           const std::vector<double>& routed_total) {
    int wrote = 0;
    for (size_t n = 0; n < sim.size() && n < routed_total.size(); n++)
        if (livetrade::write_local_value(sim[n].obj, routed_total[n])) wrote++;
    return wrote;
}

} // namespace install
