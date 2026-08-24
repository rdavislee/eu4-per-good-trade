// Solver-track deliverables that ride on the orientations: the mutual-reachability census
// (spec 2.2 item 7), the survival table skeleton (item 6), and the synthetic-shock re-solve
// (item 8). The survival table's live inputs (P_collect / P_transfer / the multi-merchant
// boost) are live-memory quantities; the no-merchant baseline built here -- even outgoing
// split, full collection at sinks -- is the country-independent skeleton the AI scores against,
// and it is the piece computable without the engine (§3.14).
#pragma once
#include <cstdint>
#include <deque>
#include <vector>
#include "drain.h"

namespace analytics {

// per-good directed reachability, OR-projected over live goods: entry[n][m] = a directed path
// n -> ... -> m exists for at least one good (measure6's "ordered pairs connected")
struct Census {
    int N = 0;
    std::vector<std::vector<uint8_t>> any;    // boolean projection
    std::vector<std::vector<int>> count;      // goods count (the DLL deliverable)
    long connected_pairs = 0;                 // ordered pairs with any==1
};

inline void reach_into(int N, const std::vector<std::pair<int, int>>& directed,
                       std::vector<std::vector<uint8_t>>& any,
                       std::vector<std::vector<int>>& count) {
    std::vector<std::vector<int>> adj(N);
    for (auto& [u, v] : directed) adj[u].push_back(v);
    for (int s = 0; s < N; s++) {
        std::vector<uint8_t> seen(N, 0);
        std::deque<int> q{s};
        seen[s] = 1;
        while (!q.empty()) {
            int x = q.front(); q.pop_front();
            for (int y : adj[x]) if (!seen[y]) { seen[y] = 1; q.push_back(y); }
        }
        for (int t = 0; t < N; t++)
            if (t != s && seen[t]) { any[s][t] = 1; count[s][t]++; }
    }
}

inline Census build_census(int N, const std::vector<std::vector<std::pair<int, int>>>& per_good) {
    Census c;
    c.N = N;
    c.any.assign(N, std::vector<uint8_t>(N, 0));
    c.count.assign(N, std::vector<int>(N, 0));
    for (auto& d : per_good) reach_into(N, d, c.any, c.count);
    c.connected_pairs = 0;
    for (int s = 0; s < N; s++)
        for (int t = 0; t < N; t++) c.connected_pairs += c.any[s][t];
    return c;
}

// Survival table skeleton S_g[n][H]: expected fraction of a unit of g at n arriving at H, under
// the NO-MERCHANT regime -- outgoing value splits evenly across g's outgoing links, and a sink
// collects its whole incoming (collected_share = 1), terminating the recursion (spec 1.8, 3.14).
// Backward pass over the good's DAG. Row n sums to 1 by construction (conservation of the unit).
inline std::vector<std::vector<double>> survival_table(
        int N, const std::vector<std::pair<int, int>>& directed) {
    std::vector<std::vector<int>> outs(N);
    std::vector<int> indeg(N, 0), outdeg(N, 0);
    for (auto& [u, v] : directed) { outs[u].push_back(v); indeg[v]++; outdeg[u]++; }
    // topological order (Kahn)
    std::deque<int> q;
    std::vector<int> ind = indeg;
    for (int i = 0; i < N; i++) if (ind[i] == 0) q.push_back(i);
    std::vector<int> topo;
    while (!q.empty()) {
        int x = q.front(); q.pop_front();
        topo.push_back(x);
        for (int y : outs[x]) if (--ind[y] == 0) q.push_back(y);
    }
    // S[n] as a full N-vector; process in reverse topo so successors are done first
    std::vector<std::vector<double>> S(N, std::vector<double>(N, 0.0));
    for (auto it = topo.rbegin(); it != topo.rend(); ++it) {
        int n = *it;
        if (outdeg[n] == 0) {                 // sink for g: collects its whole unit here
            S[n][n] = 1.0;
            continue;
        }
        double w = 1.0 / outdeg[n];           // even split (no merchant steering)
        for (int m : outs[n])
            for (int H = 0; H < N; H++) S[n][H] += w * S[m][H];
    }
    return S;
}

} // namespace analytics
