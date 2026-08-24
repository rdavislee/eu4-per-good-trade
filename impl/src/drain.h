// DRAIN (spec 1.1): peel -> HHI-adaptive sink selection -> min-cost b-flow -> gated
// deterministic drainage sweep -> un-peel. Semantics replicate the reference drain.py
// exactly, including Python's banker's rounding for k, the stable top-k cluster sort,
// FIFO Kahn topo order, list-order double summation for DEF, and the lazy priority heap
// keyed (DEF asc, beta asc, index).
//
// Per-tick checks (spec 2.8): acyclicity and 2-core sink containment in
// {selected} u {promoted} u {fallbacks} are ASSERTIONS (throw); the sink-set equality
// {selected & flow-terminal} u {promoted} is a MONITOR (reported, never thrown -- T1/T2/T3
// are its legitimate failures); conservation (unserved == stranded) and reachability are
// assertions computed by the same constructions as the reference (final.py, props6.py).
#pragma once
#include <algorithm>
#include <cfenv>
#include <cmath>
#include <deque>
#include <map>
#include <queue>
#include <set>
#include <stdexcept>
#include <vector>
#include "netsimplex.h"

namespace drain {

constexpr double ZERO_TOL = 1e-11;       // net flow below this counts as zero (flowop.py)

struct Graph {                            // the map: adjacency + edges, index space 0..N-1
    int N = 0;
    std::vector<std::vector<int>> und;                // neighbor lists, reference order
    std::vector<std::pair<int, int>> edges_und;       // sorted unique pairs
};

struct Checks {
    bool acyclic = false;
    bool containment = false;             // core sinks subset of S0 u promotions u fallbacks
    bool equality = false;                // MONITOR: sinks == {S0 & flow-terminal} u promotions
    std::vector<int> equality_diff;       // symmetric difference when the monitor trips
    double unserved = 0, stranded = 0;    // greedy DEF-weighted push (final.py evaluator)
    bool conservation = false;            // |unserved - stranded| < 1e-9
    double reach_pct = 0;                 // demand mass reachable from supply, percent
    int orphan_sinks = 0;
    double lp_margin = 0;                 // smallest positive reduced cost off the basis
    int lp_ties_blocked = 0, lp_ties_open = 0;
};

struct Result {
    std::vector<std::pair<int, int>> directed;        // all oriented edges
    std::set<int> S0;                                 // Phase-1 selection
    std::set<int> Sset;                               // S0 + promotions + fallbacks
    std::vector<int> promotions, fallbacks;           // in firing order
    std::map<int, int> order;                         // marking order (core nodes)
    std::vector<int> core;
    std::vector<std::pair<int, std::pair<int, int>>> flow_arc;  // (edge idx, (u,v)) in edge order
    std::vector<int> free_edges;                      // edge indices
    std::vector<double> net;                          // per edge
    std::vector<double> beta;                         // post-peel balance
    double cost = 0;
    double hhi = 0; int k = 0, nclusters = 0;
    Checks checks;
};

inline double py_round_half_even(double x) {
    // Python round() on a double: correctly-rounded half-to-even
    int save = std::fegetround();
    std::fesetround(FE_TONEAREST);
    double r = std::nearbyint(x);
    std::fesetround(save);
    return r;
}

// ---------------------------------------------------------------- phase 0 ----
struct Peel { int v, u; double bv; };     // pendant v folded into u carrying balance bv

inline void phase0(const Graph& g, const std::vector<double>& b,
                   std::vector<int>& core, std::vector<double>& beta, std::vector<Peel>& plog) {
    int N = g.N;
    beta = b;
    std::vector<char> alive(N, 1);
    std::vector<int> deg(N);
    for (int i = 0; i < N; i++) deg[i] = int(g.und[i].size());
    bool changed = true;
    while (changed) {
        changed = false;
        for (int v = 0; v < N; v++) {
            if (alive[v] && deg[v] == 1) {
                int u = -1;
                for (int x : g.und[v]) if (alive[x]) { u = x; break; }
                if (u < 0) continue;                  // isolated leftover
                plog.push_back({v, u, beta[v]});
                beta[u] += beta[v];
                alive[v] = 0; deg[u]--; deg[v] = 0;
                changed = true;
            }
        }
    }
    core.clear();
    for (int v = 0; v < N; v++) if (alive[v]) core.push_back(v);
}

// ---------------------------------------------------------------- phase 1 ----
inline std::set<int> phase1(const Graph& g, const std::vector<int>& core,
                            const std::vector<double>& beta,
                            double& hhi, int& k_out, int& nclusters) {
    std::set<int> coreset(core.begin(), core.end());
    std::vector<int> Dset;
    for (int v : core) if (beta[v] < 0) Dset.push_back(v);
    hhi = std::numeric_limits<double>::quiet_NaN(); k_out = 0; nclusters = 0;
    if (Dset.empty()) return {};
    double D = 0;
    for (int v : Dset) D += -beta[v];
    std::set<int> ds(Dset.begin(), Dset.end());
    // connected components of the demander-induced subgraph, discovered in Dset order
    std::vector<std::vector<int>> comps;
    std::set<int> seen;
    for (int v : Dset) {
        if (seen.count(v)) continue;
        std::vector<int> comp{v}, stack{v};
        std::set<int> incomp{v};
        seen.insert(v);
        while (!stack.empty()) {
            int x = stack.back(); stack.pop_back();
            for (int y : g.und[x]) {
                if (ds.count(y) && !incomp.count(y)) {
                    incomp.insert(y); seen.insert(y); comp.push_back(y); stack.push_back(y);
                }
            }
        }
        std::sort(comp.begin(), comp.end());
        comps.push_back(std::move(comp));
    }
    nclusters = int(comps.size());
    std::vector<double> M(comps.size(), 0.0);
    for (size_t j = 0; j < comps.size(); j++)
        for (int v : comps[j]) M[j] += -beta[v];
    double H = 0;
    for (double m : M) { double q = m / D; H += q * q; }
    hhi = H;
    int k = int(py_round_half_even(1.0 / H));
    k = std::max(1, std::min(k, nclusters));
    k_out = k;
    // stable top-k by mass descending (Python sorted(key=-M) is stable)
    std::vector<int> idx(comps.size());
    for (size_t j = 0; j < idx.size(); j++) idx[j] = int(j);
    std::stable_sort(idx.begin(), idx.end(), [&](int a, int b) { return M[a] > M[b]; });
    std::set<int> S;
    for (int t = 0; t < k; t++) {
        const std::vector<int>& comp = comps[idx[t]];
        int best = comp[0];
        for (int v : comp)
            if (beta[v] < beta[best] || (beta[v] == beta[best] && v < best)) best = v;
        S.insert(best);
    }
    return S;
}

// ---------------------------------------------------------------- phase 2 ----
inline void phase2(const Graph& g, const std::vector<int>& core, const std::vector<double>& beta,
                   const std::vector<double>& tie_cost_edge, Result& r) {
    std::set<int> coreset(core.begin(), core.end());
    std::vector<double> b(g.N, 0.0);
    for (int v : core) b[v] = beta[v];
    netsimplex::Result lp = netsimplex::Solver::solve(g.N, g.edges_und, tie_cost_edge, b);
    r.net = lp.net;
    r.cost = lp.cost;
    r.checks.lp_margin = lp.smallest_positive_rc;
    r.checks.lp_ties_blocked = lp.ties_blocked;
    r.checks.lp_ties_open = lp.ties_open;
    for (size_t ei = 0; ei < g.edges_und.size(); ei++) {
        auto [u, v] = g.edges_und[ei];
        if (!coreset.count(u) || !coreset.count(v)) continue;
        double phi = lp.net[ei];
        if (phi > ZERO_TOL) r.flow_arc.push_back({int(ei), {u, v}});
        else if (phi < -ZERO_TOL) r.flow_arc.push_back({int(ei), {v, u}});
        else r.free_edges.push_back(int(ei));
    }
}

// ------------------------------------------------- phase 3: adjacency prep ---
struct SweepAdj {
    std::map<int, std::vector<int>> outs, ins, freeadj;
    std::map<int, double> inflow;
};

inline SweepAdj phase3(const Graph& g, const Result& r) {
    SweepAdj a;
    for (auto& [ei, arc] : r.flow_arc) {
        a.outs[arc.first].push_back(arc.second);
        a.ins[arc.second].push_back(arc.first);
        a.inflow[arc.second] += std::fabs(r.net[ei]);
    }
    for (int ei : r.free_edges) {
        auto [u, v] = g.edges_und[ei];
        a.freeadj[u].push_back(v);
        a.freeadj[v].push_back(u);
    }
    return a;
}

// DEF: downstream demand on the flow-arc subgraph (drain.py flow_def, summation replicated)
inline std::map<int, double> flow_def(const std::vector<int>& core,
                                      const std::vector<double>& beta, const SweepAdj& a) {
    std::map<int, int> ind;
    for (auto& [v, lst] : a.ins) ind[v] = int(lst.size());
    std::deque<int> q;
    for (int v : core) if (ind.count(v) == 0 || ind[v] == 0) q.push_back(v);
    std::vector<int> topo;
    std::map<int, int> ind2 = ind;
    while (!q.empty()) {
        int x = q.front(); q.pop_front();
        topo.push_back(x);
        auto it = a.outs.find(x);
        if (it != a.outs.end())
            for (int y : it->second) {
                ind2[y]--;
                if (ind2[y] == 0) q.push_back(y);
            }
    }
    std::map<int, double> DEF;
    for (auto it = topo.rbegin(); it != topo.rend(); ++it) {
        int v = *it;
        double s = 0;
        auto ot = a.outs.find(v);
        if (ot != a.outs.end()) for (int u : ot->second) s += DEF[u];
        DEF[v] = std::max(0.0, -beta[v]) + s;
    }
    for (int v : core)
        if (!DEF.count(v)) DEF[v] = std::max(0.0, -beta[v]);
    return DEF;
}

// ------------------------------------------ phase 3: deterministic sweep -----
// priority ready-queue keyed (DEF ascending, beta ascending, index) -- drain.py's
// sweep_priority with key_mode "defasc_beta", lazy heap entries revalidated on pop
inline void sweep_priority(const Graph& g, const std::vector<int>& core,
                           const std::vector<double>& beta, const std::set<int>& S,
                           const std::vector<double>& node_wealth, const SweepAdj& a,
                           Result& r) {
    struct Key {
        double def_, beta_; int pid, u;
        bool operator>(const Key& o) const {
            if (def_ != o.def_) return def_ > o.def_;
            if (beta_ != o.beta_) return beta_ > o.beta_;
            if (pid != o.pid) return pid > o.pid;
            return u > o.u;
        }
    };
    std::map<int, double> DEF = flow_def(core, beta, a);
    std::map<int, int> cnt;
    for (int u : core) {
        auto it = a.outs.find(u);
        cnt[u] = it == a.outs.end() ? 0 : int(it->second.size());
    }
    std::set<int> marked;
    std::set<int> Sset(S.begin(), S.end());
    auto ready = [&](int u) {
        if (marked.count(u) || cnt[u] != 0) return false;
        if (Sset.count(u)) return true;
        auto ot = a.outs.find(u);
        if (ot != a.outs.end() && !ot->second.empty()) return true;
        auto ft = a.freeadj.find(u);
        if (ft != a.freeadj.end())
            for (int w : ft->second) if (marked.count(w)) return true;
        return false;
    };
    std::priority_queue<Key, std::vector<Key>, std::greater<Key>> heap;
    auto push = [&](int u) { heap.push({DEF[u], beta[u], u, u}); };
    for (int u : core) if (ready(u)) push(u);
    int t = 0;
    while (int(marked.size()) < int(core.size())) {
        int found = -1;
        while (!heap.empty()) {
            Key k = heap.top(); heap.pop();
            if (ready(k.u)) { found = k.u; break; }
        }
        if (found < 0) {
            // STALL: promote among gated candidates (unmarked, all flow out-neighbours marked)
            std::vector<int> gated;
            for (int u : core) if (!marked.count(u) && cnt[u] == 0) gated.push_back(u);
            std::vector<int> terminals;
            for (int u : gated) {
                auto ot = a.outs.find(u);
                bool noouts = ot == a.outs.end() || ot->second.empty();
                auto ift = a.inflow.find(u);
                if (noouts && ift != a.inflow.end() && ift->second > ZERO_TOL)
                    terminals.push_back(u);
            }
            int s_star;
            if (!terminals.empty()) {
                s_star = terminals[0];
                for (int v : terminals)
                    if (beta[v] < beta[s_star] || (beta[v] == beta[s_star] && v < s_star))
                        s_star = v;
                r.promotions.push_back(s_star);
            } else {
                if (gated.empty())
                    throw std::runtime_error("drain: no gated unmarked node - flow support cycle");
                s_star = gated[0];   // fallback: highest wealth, ties lowest index
                for (int v : gated)
                    if (node_wealth[v] > node_wealth[s_star] ||
                        (node_wealth[v] == node_wealth[s_star] && v < s_star))
                        s_star = v;
                r.fallbacks.push_back(s_star);
            }
            Sset.insert(s_star);
            if (ready(s_star)) push(s_star);
            continue;
        }
        marked.insert(found);
        r.order[found] = t++;
        auto it = a.ins.find(found);
        if (it != a.ins.end())
            for (int x : it->second) {
                cnt[x]--;
                if (ready(x)) push(x);
            }
        auto ft = a.freeadj.find(found);
        if (ft != a.freeadj.end())
            for (int w : ft->second) if (ready(w)) push(w);
    }
    r.Sset = Sset;
}

// ---------------------------------------------------------------- phase 4 ----
inline void compile_dirs(const Graph& g, const std::vector<Peel>& plog, Result& r) {
    for (auto& [ei, arc] : r.flow_arc) r.directed.push_back(arc);
    for (int ei : r.free_edges) {
        auto [u, v] = g.edges_und[ei];
        r.directed.push_back(r.order.at(u) > r.order.at(v) ? std::make_pair(u, v)
                                                           : std::make_pair(v, u));
    }
    for (auto it = plog.rbegin(); it != plog.rend(); ++it)
        r.directed.push_back(it->bv >= 0 ? std::make_pair(it->v, it->u)
                                         : std::make_pair(it->u, it->v));
}

// --------------------------------------------------------------- checks ------
inline bool has_cycle(int N, const std::vector<std::pair<int, int>>& directed) {
    std::vector<std::vector<int>> adj(N);
    for (auto& [u, v] : directed) adj[u].push_back(v);
    std::vector<int> col(N, 0);
    std::vector<std::pair<int, int>> stack;      // (node, next child index)
    for (int s = 0; s < N; s++) {
        if (col[s] != 0) continue;
        stack.push_back({s, 0});
        col[s] = 1;
        while (!stack.empty()) {
            auto& [u, ci] = stack.back();
            if (ci < int(adj[u].size())) {
                int w = adj[u][ci++];
                if (col[w] == 1) return true;
                if (col[w] == 0) { col[w] = 1; stack.push_back({w, 0}); }
            } else {
                col[u] = 2;
                stack.pop_back();
            }
        }
    }
    return false;
}

// greedy DEF-weighted push (final.py eval_phase4_full): conservation check
inline void eval_conservation(int N, const std::vector<std::pair<int, int>>& directed,
                              const std::vector<double>& b, Checks& c) {
    std::vector<std::vector<int>> outs(N);
    std::vector<int> ind(N, 0);
    for (auto& [u, v] : directed) { outs[u].push_back(v); ind[v]++; }
    std::deque<int> q;
    for (int i = 0; i < N; i++) if (ind[i] == 0) q.push_back(i);
    std::vector<int> topo;
    while (!q.empty()) {
        int x = q.front(); q.pop_front();
        topo.push_back(x);
        for (int y : outs[x]) if (--ind[y] == 0) q.push_back(y);
    }
    if (int(topo.size()) != N) { c.conservation = false; return; }   // cyclic: caught elsewhere
    std::vector<double> dfc(N, 0.0);
    for (auto it = topo.rbegin(); it != topo.rend(); ++it) {
        int v = *it;
        double s = 0;
        for (int u : outs[v]) s += dfc[u];
        dfc[v] = std::max(0.0, -b[v]) + s;
    }
    std::vector<double> inflow(N, 0.0);
    double uns = 0, stranded = 0;
    for (int v : topo) {
        double out;
        if (b[v] > 0) out = inflow[v] + b[v];
        else {
            double srv = std::min(inflow[v], -b[v]);
            uns += (-b[v]) - srv;
            out = inflow[v] - srv;
        }
        if (!outs[v].empty()) {
            double ws = 0;
            for (int t2 : outs[v]) ws += dfc[t2];
            for (int t2 : outs[v])
                inflow[t2] += out * (ws > 0 ? dfc[t2] / ws : 1.0 / outs[v].size());
        } else {
            stranded += out;
        }
    }
    c.unserved = uns; c.stranded = stranded;
    c.conservation = std::fabs(uns - stranded) < 1e-9;
}

// demand reachability from supply over the directed graph (props6.py construction)
inline void eval_reachability(int N, const std::vector<std::pair<int, int>>& directed,
                              const std::vector<double>& s, const std::vector<double>& cdem,
                              const std::vector<int>& sinks, Checks& c) {
    std::vector<std::vector<int>> adj(N);
    for (auto& [u, v] : directed) adj[u].push_back(v);
    std::vector<char> seen(N, 0);
    std::vector<int> st;
    for (int i = 0; i < N; i++) if (s[i] > 0 && !seen[i]) { st.push_back(i); }
    while (!st.empty()) {
        int x = st.back(); st.pop_back();
        if (seen[x]) continue;
        seen[x] = 1;
        for (int y : adj[x]) st.push_back(y);
    }
    double tot = 0, got = 0;
    for (int i = 0; i < N; i++) { tot += cdem[i]; if (seen[i]) got += cdem[i]; }
    c.reach_pct = tot > 0 ? 100.0 * got / tot : 100.0;
    c.orphan_sinks = 0;
    for (int i : sinks) if (!seen[i]) c.orphan_sinks++;
}

// ------------------------------------------------------------------ driver ---
// s/cdem: the raw supply/demand share vectors (for reachability); b must equal s - cdem.
inline Result run(const Graph& g, const std::vector<double>& b,
                  const std::vector<double>& tie_cost_edge,
                  const std::vector<double>& node_wealth,
                  const std::vector<double>& s, const std::vector<double>& cdem) {
    Result r;
    std::vector<Peel> plog;
    phase0(g, b, r.core, r.beta, plog);
    if (int(r.core.size()) <= 1) {
        for (auto it = plog.rbegin(); it != plog.rend(); ++it)
            r.directed.push_back(it->bv >= 0 ? std::make_pair(it->v, it->u)
                                             : std::make_pair(it->u, it->v));
        r.checks.acyclic = !has_cycle(g.N, r.directed);
        r.checks.containment = true;
        return r;
    }
    r.S0 = phase1(g, r.core, r.beta, r.hhi, r.k, r.nclusters);
    phase2(g, r.core, r.beta, tie_cost_edge, r);
    SweepAdj a = phase3(g, r);
    sweep_priority(g, r.core, r.beta, r.S0, node_wealth, a, r);
    compile_dirs(g, plog, r);

    // ----- per-tick checks (spec 2.8) -----
    r.checks.acyclic = !has_cycle(g.N, r.directed);
    std::vector<int> sinks;
    {
        std::vector<int> od(g.N, 0);
        for (auto& [u, v] : r.directed) od[u]++;
        for (int i = 0; i < g.N; i++) if (od[i] == 0) sinks.push_back(i);
    }
    std::set<int> coreset(r.core.begin(), r.core.end());
    r.checks.containment = true;
    for (int sk : sinks)
        if (coreset.count(sk) && !r.Sset.count(sk)) r.checks.containment = false;
    // equality monitor: {S0 & flow-terminal} u promotions vs core sinks
    std::set<int> formula;
    {
        std::set<int> has_out;
        for (auto& [ei, arc] : r.flow_arc) has_out.insert(arc.first);
        for (int v : r.S0) if (!has_out.count(v)) formula.insert(v);
        for (int v : r.promotions) formula.insert(v);
        std::set<int> sinkset(sinks.begin(), sinks.end());
        // compare over the whole graph as props6 does (pendant sinks break it -> T1, reported)
        r.checks.equality = (formula == sinkset);
        if (!r.checks.equality) {
            std::set_symmetric_difference(formula.begin(), formula.end(),
                                          sinkset.begin(), sinkset.end(),
                                          std::back_inserter(r.checks.equality_diff));
        }
    }
    eval_conservation(g.N, r.directed, b, r.checks);
    eval_reachability(g.N, r.directed, s, cdem, sinks, r.checks);
    return r;
}

} // namespace drain
