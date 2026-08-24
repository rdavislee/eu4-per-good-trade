// Resolve the engine's node-array order to node NAMES (spec 1.8/2.6 correctness).
//
// The live engine node array is ordered by the engine's internal node id (CTradeNode+0x120,
// which equals the array position); that order is NOT the reference file's declaration order and
// NOT the vanilla save's node order (measured: 0/51 agree). So live index i and solver-field
// index i are different nodes, and any routing keyed on position is wrong.
//
// A node's 33-slot trade_goods_size production vector is a stable, orientation-independent
// fingerprint. We match each live node to a reference-save node by that vector (nearest L1,
// enforced 1-to-1), producing engine-id -> node-name. The match is done ONCE at the start date
// (production == the reference), then the mapping is keyed by the stable engine id, so it does
// not drift as the campaign changes production. The reference save is the same file the solver
// field is built from, so a matched name maps straight to a field index by name.
#pragma once
#include <algorithm>
#include <cmath>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "../src/save.h"

namespace nodemap {

inline double l1(const std::vector<double>& a, const std::vector<double>& b) {
    size_t n = std::max(a.size(), b.size());
    double d = 0;
    for (size_t i = 0; i < n; i++) {
        double x = i < a.size() ? a[i] : 0.0, y = i < b.size() ? b[i] : 0.0;
        d += std::fabs(x - y);
    }
    return d;
}

// live sim node index (== engine id) -> reference node name. Also fills unmatched_live with any
// live index that got no name (e.g. a spurious extra manager slot).
struct Map {
    std::map<int, std::string> id_to_name;   // engine node id -> name
    std::map<std::string, int> name_to_id;   // inverse
    int exact = 0, matched = 0, spurious = 0;
};

inline Map resolve(const std::vector<livetrade::SimNode>& sim,
                   const std::vector<save::NodeEcon>& ref) {
    // live goods vectors (÷1000 to ducats to match the save's units)
    std::vector<std::vector<double>> lv(sim.size());
    for (size_t i = 0; i < sim.size(); i++) {
        lv[i].resize(sim[i].goods.size());
        for (size_t k = 0; k < sim[i].goods.size(); k++) lv[i][k] = sim[i].goods[k] / 1000.0;
    }
    // all (dist, live_i, ref_j) candidate pairs, greedy by ascending distance -> 1-1 matching
    struct P { double d; int i, j; };
    std::vector<P> pairs;
    for (int i = 0; i < (int)sim.size(); i++)
        for (int j = 0; j < (int)ref.size(); j++)
            pairs.push_back({l1(lv[i], ref[j].goods_size), i, j});
    std::sort(pairs.begin(), pairs.end(), [](const P& a, const P& b) { return a.d < b.d; });
    Map m;
    std::vector<char> usedL(sim.size(), 0), usedR(ref.size(), 0);
    for (auto& p : pairs) {
        if (usedL[p.i] || usedR[p.j]) continue;
        usedL[p.i] = usedR[p.j] = 1;
        int id = sim[p.i].index;             // the stable engine node id
        m.id_to_name[id] = ref[p.j].name;
        m.name_to_id[ref[p.j].name] = id;
        m.matched++;
        if (p.d == 0.0) m.exact++;
    }
    for (size_t i = 0; i < sim.size(); i++) if (!usedL[i]) m.spurious++;
    return m;
}

} // namespace nodemap
