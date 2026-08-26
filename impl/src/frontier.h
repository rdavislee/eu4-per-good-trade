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
#include <functional>
#include <set>
#include <vector>
#include "economy.h"

namespace frontier {

struct Placement { int node; int target; double added; };   // stand at `node`, steer toward `target`
inline long long g_calls_candidates = 0, g_calls_plan = 0;   // per-tick cost counters

// A merchant present at a node holds MERCHANT_MAX_POWER_BONUS (+2) of trade power there, whatever
// else it holds (spec 1.7). This is what keeps a REVERSE end from scoring zero: the engine
// propagates power upstream only along Phi_w links (spec 1.9), so at a node downstream of the
// country in Phi_w it has no propagated power at all -- its share read off the standings is
// exactly 0 and the whole product is 0. Every reverse candidate was dying here, silently, long
// before the x1.5 test. The merchant's own presence is the floor.
constexpr double MERCHANT_PRESENT_POWER = 2.0;

// share of ALL trade power at n held by `country`; `floor_mine` lifts the country's own power
// to at least that much (the merchant-present bonus at a node it would stand on)
inline double share_at(const std::vector<econ::NodeStandings>& st, int n, int country,
                       double floor_mine = 0.0) {
    if (n < 0 || n >= (int)st.size()) return 0.0;
    double mine = 0, tot = 0;
    for (auto& e : st[n].entries) { if (e.power > 0) { tot += e.power; if (e.country == country) mine += e.power; } }
    if (mine < floor_mine) { tot += floor_mine - mine; mine = floor_mine; }
    return tot > 0 ? mine / tot : 0.0;
}

// The per-tick flow matrix: F[n][m] = total over goods of realized flow leaving n toward m.
// Summed ONCE per tick. flow_toward() below re-summed 29 goods for every (edge, candidate) of
// every country -- measured at 450 ms on an AI tick against 22 ms otherwise.
// A flat N x N array, not a vector of maps: the map form allocated per node per tick and cost
// ~100 ms a month on its own (measured as the whole of what had been attributed to planning).
struct FlowMatrix { int N = 0; std::vector<double> v; double at(int n, int m) const { return (n < 0 || m < 0 || n >= N || m >= N) ? 0.0 : v[(size_t)n * N + m]; } };
inline FlowMatrix flow_matrix(int N, const std::vector<econ::GoodFlow>& per_good) {
    FlowMatrix F; F.N = N; F.v.assign((size_t)N * N, 0.0);
    for (auto& G : per_good)
        for (int n = 0; n < N && n < (int)G.flow.size(); n++)
            for (auto& [m, val] : G.flow[n]) if (m >= 0 && m < N) F.v[(size_t)n * N + m] += val;
    return F;
}
inline double flow_of(const FlowMatrix& F, int n, int m) { return F.at(n, m); }

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

// the product of shares along the path from `entry` (a network node) home, INCLUDING home.
// Every node on the path except home is a network node -- one where this country has (or is
// planning) a merchant -- so the merchant-present floor applies at each of them, not only at
// the node being scored. Without it the network cannot grow past one hop into territory where
// the country has no propagated power: the second hop's path share read 0 (reviewed defect).
inline double path_share(const std::vector<econ::NodeStandings>& st, const std::vector<int>& parent,
                         int entry, int home, int country) {
    double p = 1.0; int cur = entry; int guard = 0;
    while (cur >= 0 && guard++ < 256) {
        p *= share_at(st, cur, country, cur == home ? 0.0 : MERCHANT_PRESENT_POWER);
        if (cur == home) return p;
        cur = parent[cur];
    }
    return 0.0;    // entry not connected to home through the network
}

// score every frontier edge; `network` must contain home
// REACH. A candidate stand node must be one the country can actually send a merchant to. The
// model does not know the engine's range rule (trade range from owned provinces, discovery),
// so the caller passes it in: nullptr means every node is reachable (the offline test); the DLL
// passes the engine's own CanSendMerchantTo, OR-ed with nodes the country already occupies.
// Without it a New World tribe could plan -- and be force-placed -- at Sevilla (observed 1444).
using Reach = std::function<bool(int)>;
inline std::vector<Placement> candidates(int N, int home, const std::set<int>& network,
                                         const std::vector<std::vector<int>>& adj,
                                         const std::vector<econ::NodeStandings>& st,
                                         const FlowMatrix& F,
                                         int country, const Reach* reach = nullptr) {
    std::vector<Placement> out;
    g_calls_candidates++;
    if (home < 0 || home >= N) return out;
    std::vector<int> parent = network_parents(N, home, network, adj);
    for (int inside : network) {
        if (parent[inside] < 0) continue;                 // network island not connected to home
        double ps = path_share(st, parent, inside, home, country);
        if (ps <= 0) continue;
        if (inside < 0 || inside >= (int)adj.size()) continue;
        for (int outside : adj[inside]) {
            if (network.count(outside)) continue;         // not a frontier edge
            if (reach && *reach && !(*reach)(outside)) continue;   // out of the country's reach
            double f = flow_of(F, outside, inside);
            if (f <= 0) continue;                         // nothing moves inward here
            // the merchant would stand at `outside`: its own presence is +2 there, so its
            // share at the entry node is never zero even where nothing propagates
            double s_out = share_at(st, outside, country, MERCHANT_PRESENT_POWER);
            out.push_back({outside, inside, f * s_out * ps});
        }
    }
    std::sort(out.begin(), out.end(), [](const Placement& a, const Placement& b) { return a.added > b.added; });
    return out;
}

// what a merchant earns COLLECTING at n: the node's collectible pool (sum over goods of
// value x collected_share) times the country's share of all power there. This is the
// alternative every steer candidate must beat: Ming at hangzhou (a Phi_w sink) collects
// a share of everything pooled there, which is why it does not push north to beijing.
// Collecting anywhere but the trade capital halves the country's power there:
// TRADE_NON_CAPITAL_OFFICE = -0.50 (defines.lua:1200; spec 3.14 treats it as a POWER modifier,
// so it enters the share, not the payout). This is what stops "collect at every node you
// hold power in" from ever scoring: off home you keep half the share, and the +2 merchant
// presence is halved with it.
constexpr double OFF_HOME_POWER_MULT = 0.5;

inline double collect_value(const std::vector<econ::NodeStandings>& st,
                            const std::vector<econ::GoodFlow>& per_good, int n, int country, int home) {
    double pool = 0;
    for (auto& F : per_good) if (n >= 0 && n < (int)F.collected.size()) pool += F.collected[n];
    if (n < 0 || n >= (int)st.size()) return 0.0;
    double mine = 0, tot = 0;
    for (auto& e : st[n].entries) { if (e.power > 0) { tot += e.power; if (e.country == country) mine += e.power; } }
    if (mine < MERCHANT_PRESENT_POWER) { tot += MERCHANT_PRESENT_POWER - mine; mine = MERCHANT_PRESENT_POWER; }
    if (n != home) { tot -= mine * (1.0 - OFF_HOME_POWER_MULT); mine *= OFF_HOME_POWER_MULT; }
    return tot > 0 ? pool * (mine / tot) : 0.0;
}

// THE PORTFOLIO: where a country's k merchants should stand. Greedy, exactly as the user
// described the network growing: start from home, take the best frontier edge, add its outside
// node to the network (the merchant now stands there and it is a place value can be funnelled
// through), re-score the new frontier, repeat k times. Later merchants can therefore reach nodes
// two or more hops out -- but only through a path of earlier merchants, which is the BFS.
inline std::vector<Placement> plan(int N, int home, int k,
                                   const std::vector<std::vector<int>>& adj,
                                   const std::vector<econ::NodeStandings>& st,
                                   const FlowMatrix& F,
                                   int country, const Reach* reach = nullptr) {
    std::vector<Placement> chosen;
    g_calls_plan++;
    if (home < 0 || home >= N || k <= 0) return chosen;
    std::set<int> network{home};
    for (int i = 0; i < k; i++) {
        auto cands = candidates(N, home, network, adj, st, F, country, reach);
        if (cands.empty() || cands.front().added <= 0) break;   // nothing left worth a merchant
        chosen.push_back(cands.front());
        network.insert(cands.front().node);
    }
    return chosen;
}

// the added value of an EXISTING placement (stand at node, steer toward target): the SAME
// metric candidates() scores -- flow x the merchant's own share at its stand node (floored,
// it is standing there) x the path product home -- so the x1.5 comparison is like against like.
// Returns -1 when the target is not connected to home through the network: the placement is
// worth nothing AND must not be folded into a min as a 0, which would disable the gain test.
inline double added_value(int N, int home, const std::set<int>& network,
                          const std::vector<std::vector<int>>& adj,
                          const std::vector<econ::NodeStandings>& st,
                          const FlowMatrix& F,
                          int country, int node, int target) {
    std::vector<int> parent = network_parents(N, home, network, adj);
    if (target < 0 || target >= N || parent[target] < 0) return -1.0;
    double s_node = share_at(st, node, country, MERCHANT_PRESENT_POWER);
    return flow_of(F, node, target) * s_node * path_share(st, parent, target, home, country);
}

} // namespace frontier
