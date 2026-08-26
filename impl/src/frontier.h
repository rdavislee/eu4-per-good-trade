// AI MERCHANT PLACEMENT: THE FRONTIER MODEL (spec 3.14; tests G1, G2).
//
// The user's model, verbatim in structure:
//
//   1. HOME is the trade-capital node. The NETWORK is home plus the far node of every merchant
//      the country has placed. It grows one node per placement.
//   2. CANDIDATES are the frontier: every edge (either direction) with one end in the network and
//      the other outside. The merchant stands at the outside end and steers inward. Candidates
//      therefore always connect back to home THROUGH the network -- that is the BFS.
//   3. SCORE of a candidate = the value that actually flows along the edge toward the network
//      (our own routing's number), multiplied by the country's share of ALL trade power at every
//      node on the shortest network path home, and then by its share at home. Value walks the
//      graph home and at each node you keep only your fraction of it -- the trade mechanic itself,
//      walked backward.
//   4. MOVE only if a candidate beats the country's LEAST profitable current merchant by x1.5, or
//      the country has a merchant to spare. Vanilla's own rule (0x1BD206), over all edge ends.
//
// One choice not the user's: when two network paths lead home, the score follows the BFS-shortest
// one. It is what walking the graph gives for free; a best-path variant is a later refinement.
#pragma once
#include <map>
#include <set>
#include <vector>
#include "economy.h"

namespace frontier {

struct Placement { int node; int target; double added; };   // stand at `node`, steer toward `target`

// share of ALL trade power at n held by `country`; 0 if none
inline double share_at(const std::vector<econ::NodeStandings>& st, int n, int country) {
    if (n < 0 || n >= (int)st.size()) return 0.0;
    double mine = 0, tot = 0;
    for (auto& e : st[n].entries) { if (e.power > 0) { tot += e.power; if (e.country == country) mine += e.power; } }
    return tot > 0 ? mine / tot : 0.0;
}

// total (over goods) realized flow leaving n toward m, this tick
inline double flow_toward(const std::vector<econ::GoodFlow>& per_good, int n, int m) {
    double f = 0;
    for (auto& F : per_good) {
        if (n < 0 || n >= (int)F.flow.size()) continue;
        auto it = F.flow[n].find(m);
        if (it != F.flow[n].end()) f += it->second;
    }
    return f;
}

// BFS from home over the NETWORK only; parent[] gives the shortest path home for each member
inline std::vector<int> network_parents(int N, int home, const std::set<int>& network,
                                        const std::vector<std::vector<int>>& adj) {
    std::vector<int> parent(N, -1);
    if (home < 0 || home >= N) return parent;
    std::vector<int> q{home}; parent[home] = home;
    for (size_t i = 0; i < q.size(); i++) {
        int u = q[i];
        if (u < 0 || u >= (int)adj.size()) continue;
        for (int v : adj[u])
            if (v >= 0 && v < N && parent[v] < 0 && network.count(v)) { parent[v] = u; q.push_back(v); }
    }
    return parent;
}

// the product of shares along the path from `entry` (a network node) home, INCLUDING home
inline double path_share(const std::vector<econ::NodeStandings>& st, const std::vector<int>& parent,
                         int entry, int home, int country) {
    double p = 1.0; int cur = entry; int guard = 0;
    while (cur >= 0 && guard++ < 256) {
        p *= share_at(st, cur, country);
        if (cur == home) return p;
        cur = parent[cur];
    }
    return 0.0;    // entry not connected to home through the network
}

// score every frontier edge; `network` must contain home
inline std::vector<Placement> candidates(int N, int home, const std::set<int>& network,
                                         const std::vector<std::vector<int>>& adj,
                                         const std::vector<econ::NodeStandings>& st,
                                         const std::vector<econ::GoodFlow>& per_good,
                                         int country) {
    std::vector<Placement> out;
    if (home < 0 || home >= N) return out;
    std::vector<int> parent = network_parents(N, home, network, adj);
    for (int inside : network) {
        if (parent[inside] < 0) continue;                 // network island not connected to home
        double ps = path_share(st, parent, inside, home, country);
        if (ps <= 0) continue;
        if (inside < 0 || inside >= (int)adj.size()) continue;
        for (int outside : adj[inside]) {
            if (network.count(outside)) continue;         // not a frontier edge
            double f = flow_toward(per_good, outside, inside);
            if (f <= 0) continue;                         // nothing moves inward here
            out.push_back({outside, inside, f * ps});
        }
    }
    std::sort(out.begin(), out.end(), [](const Placement& a, const Placement& b) { return a.added > b.added; });
    return out;
}

// the added value of an EXISTING placement (stand at node, steer toward target), same walk
inline double added_value(int N, int home, const std::set<int>& network,
                          const std::vector<std::vector<int>>& adj,
                          const std::vector<econ::NodeStandings>& st,
                          const std::vector<econ::GoodFlow>& per_good,
                          int country, int node, int target) {
    std::vector<int> parent = network_parents(N, home, network, adj);
    if (target < 0 || target >= N || parent[target] < 0) return 0.0;
    return flow_toward(per_good, node, target) * path_share(st, parent, target, home, country);
}

} // namespace frontier
