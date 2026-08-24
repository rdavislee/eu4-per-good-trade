// Uncapacitated min-cost b-flow by network simplex (spec 2.2 item 5: simplex family required --
// the spanning-tree-basis property needs a basic optimum; interior-point without crossover is
// excluded). Single-threaded scalar code, no runtime CPU dispatch (spec 2.1 build discipline).
//
// Anti-cycling: Bland's rule (lowest-index eligible entering arc; lowest-index blocking leaving
// arc), which terminates finitely under degeneracy. The optimum is unique by the tie-break cost
// with margin >= 3.8e-8 (spec 2.3), four orders above the entering threshold here, so any
// correct simplex returns the same vertex -- the cross-implementation check rides on that.
//
// After termination the basic flows are RECOMPUTED exactly from b by peeling the tree, so net
// flows are pure sums of input balances (no accumulated pivot arithmetic), and the reduced-cost
// classification of spec 2.8's solver-tolerance row runs on the final basis.
#pragma once
#include <algorithm>
#include <cmath>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace netsimplex {

constexpr double ENTER_EPS = 1e-12;      // entering threshold, far below the tie-break margin
constexpr double TOL_PIN = 1e-10;        // the pinned optimality tolerance (flowop.LP_OPTS)
constexpr double RC_ZERO = 1e-11;        // |rc| below this counts as an exact tie (paper's state)
// Artificial arc cost. Must exceed any real path cost (<= 81 arcs x ~1.002 on the 1444 field)
// and stay SMALL: potentials inherit this scale, and reduced costs near zero are computed by
// cancellation against it, so its ULP bounds the rc precision. 256 (a power of two) puts that
// noise at ~1e-13, below ENTER_EPS; the original 1e6 put it at ~2e-10, which swallowed
// sub-tolerance margins whole (caught by the "LP margin red" fixture).
constexpr double ART_COST = 256.0;

struct Result {
    // net flow per undirected edge: positive = flow u->v for edge (u,v)
    std::vector<double> net;
    double cost = 0.0;                   // objective value
    // spec 2.8 solver-tolerance row classification over off-basis real arcs:
    double smallest_positive_rc = 0.0;   // the uniqueness margin (0 if none positive)
    int ties_blocked = 0;                // rc ~ 0, cannot carry flow in any optimum ("report")
    int ties_open = 0;                   // rc ~ 0, CAN carry flow -> alternative optimum ("halt")
    int iterations = 0;
};

class Solver {
public:
    // edges: undirected (u,v) pairs over n nodes; cost per edge (symmetric); b: node balance,
    // b[i] > 0 net supply. Solves min sum cost*f, outflow - inflow = b, f >= 0 on both arcs.
    static Result solve(int n, const std::vector<std::pair<int, int>>& edges,
                        const std::vector<double>& edge_cost, const std::vector<double>& b) {
        Solver s(n, edges, edge_cost, b);
        return s.run();
    }

private:
    int n_, root_, nn_;                          // real nodes, root index, total nodes
    const std::vector<std::pair<int, int>>& edges_;
    struct Arc { int u, v, edge; double cost; }; // edge = undirected edge index, -1 artificial
    std::vector<Arc> arcs_;
    std::vector<double> b_;
    std::vector<double> flow_;
    std::vector<char> in_tree_;
    // tree structure, rebuilt per pivot (n is tiny; clarity over pointer surgery)
    std::vector<int> parent_, parent_arc_, depth_;
    std::vector<double> pi_;

    Solver(int n, const std::vector<std::pair<int, int>>& edges,
           const std::vector<double>& edge_cost, const std::vector<double>& b)
        : n_(n), root_(n), nn_(n + 1), edges_(edges), b_(b) {
        for (size_t ei = 0; ei < edges.size(); ei++) {
            auto [u, v] = edges[ei];
            arcs_.push_back({u, v, int(ei), edge_cost[ei]});
            arcs_.push_back({v, u, int(ei), edge_cost[ei]});
        }
        for (int i = 0; i < n_; i++) {
            if (b[i] >= 0) arcs_.push_back({i, root_, -1, ART_COST});
            else arcs_.push_back({root_, i, -1, ART_COST});
        }
        flow_.assign(arcs_.size(), 0.0);
        in_tree_.assign(arcs_.size(), 0);
        for (int i = 0; i < n_; i++) {
            size_t ai = edges.size() * 2 + i;
            in_tree_[ai] = 1;
            flow_[ai] = std::fabs(b[i]);
        }
    }

    void rebuild_tree() {
        parent_.assign(nn_, -1); parent_arc_.assign(nn_, -1); depth_.assign(nn_, 0);
        pi_.assign(nn_, 0.0);
        std::vector<std::vector<std::pair<int, int>>> adj(nn_);   // (other node, arc index)
        for (size_t ai = 0; ai < arcs_.size(); ai++) {
            if (!in_tree_[ai]) continue;
            adj[arcs_[ai].u].push_back({arcs_[ai].v, int(ai)});
            adj[arcs_[ai].v].push_back({arcs_[ai].u, int(ai)});
        }
        std::vector<int> stack{root_};
        std::vector<char> seen(nn_, 0); seen[root_] = 1;
        parent_[root_] = root_;
        while (!stack.empty()) {
            int x = stack.back(); stack.pop_back();
            for (auto [y, ai] : adj[x]) {
                if (seen[y]) continue;
                seen[y] = 1;
                parent_[y] = x; parent_arc_[y] = ai; depth_[y] = depth_[x] + 1;
                const Arc& a = arcs_[ai];
                // convention: rc(u->v) = cost - pi[u] + pi[v]; tree arcs have rc = 0
                if (a.u == y) pi_[y] = a.cost + pi_[x];      // arc y->x
                else pi_[y] = pi_[x] - a.cost;               // arc x->y
                stack.push_back(y);
            }
        }
        for (int i = 0; i < nn_; i++)
            if (!seen[i]) throw std::runtime_error("netsimplex: tree does not span");
    }

    double rc(size_t ai) const {
        const Arc& a = arcs_[ai];
        return a.cost - pi_[a.u] + pi_[a.v];
    }

    int lca(int u, int v) const {
        while (u != v) {
            if (depth_[u] >= depth_[v]) u = parent_[u];
            else v = parent_[v];
        }
        return u;
    }

    // cycle arcs for entering arc u->v: tree path v..lca (cycle runs along the walk) and
    // u..lca (cycle runs against the walk). sign +1 = arc gains theta, -1 = loses.
    void cycle_arcs(int u, int v, std::vector<std::pair<int, int>>& out) const {
        out.clear();
        int l = lca(u, v);
        for (int x = u; x != l; x = parent_[x]) {
            int a = parent_arc_[x];
            // cycle direction on this side is parent->x (downward toward u)
            out.push_back({a, arcs_[a].u == parent_[x] ? +1 : -1});
        }
        for (int y = v; y != l; y = parent_[y]) {
            int a = parent_arc_[y];
            // cycle direction on this side is y->parent (upward from v)
            out.push_back({a, arcs_[a].u == y ? +1 : -1});
        }
    }

    void pivot(size_t enter) {
        std::vector<std::pair<int, int>> cyc;
        cycle_arcs(arcs_[enter].u, arcs_[enter].v, cyc);
        double theta = std::numeric_limits<double>::infinity();
        int leave = -1;
        for (auto [a, s] : cyc) {
            if (s >= 0) continue;
            if (flow_[a] < theta) { theta = flow_[a]; leave = a; }
            else if (flow_[a] == theta && a < leave) leave = a;   // Bland tie-break
        }
        if (leave < 0) throw std::runtime_error("netsimplex: unbounded (no leaving arc)");
        flow_[enter] += theta;
        for (auto [a, s] : cyc) flow_[a] += s * theta;
        in_tree_[enter] = 1;
        in_tree_[leave] = 0;
        flow_[leave] = 0.0;
    }

    Result run() {
        rebuild_tree();
        int iters = 0;
        const int MAX_ITERS = 2000000;
        for (;; iters++) {
            if (iters > MAX_ITERS) throw std::runtime_error("netsimplex: iteration cap");
            int enter = -1;                     // Bland: lowest-index negative-rc arc
            for (size_t ai = 0; ai < arcs_.size(); ai++) {
                if (in_tree_[ai]) continue;
                if (rc(ai) < -ENTER_EPS) { enter = int(ai); break; }
            }
            if (enter < 0) break;
            pivot(size_t(enter));
            rebuild_tree();
        }
        recompute_tree_flows();
        return finish(iters);
    }

    void recompute_tree_flows() {
        // zero all, then peel leaf-first: each node's residual balance rides its parent arc
        for (size_t ai = 0; ai < arcs_.size(); ai++) flow_[ai] = 0.0;
        std::vector<double> resid(nn_, 0.0);
        for (int i = 0; i < n_; i++) resid[i] = b_[i];
        std::vector<int> byd(nn_);
        for (int i = 0; i < nn_; i++) byd[i] = i;
        std::sort(byd.begin(), byd.end(), [&](int a, int c) { return depth_[a] > depth_[c]; });
        for (int x : byd) {
            if (x == root_) continue;
            int a = parent_arc_[x];
            double f = (arcs_[a].u == x) ? resid[x] : -resid[x];
            if (f < 0) {
                if (f < -1e-7)
                    throw std::runtime_error("netsimplex: negative basic flow " + std::to_string(f));
                f = 0.0;
            }
            flow_[a] = f;
            resid[parent_[x]] += resid[x];
        }
    }

    // potentials over REAL tree arcs only, per real-tree component rooted at its lowest node:
    // removes the artificial-arc scale from every rc the classification computes
    std::vector<double> clean_potentials() const {
        std::vector<double> pi2(n_, 0.0);
        std::vector<char> assigned(n_, 0);
        std::vector<std::vector<std::pair<int, int>>> adj(n_);
        for (size_t ai = 0; ai < edges_.size() * 2; ai++) {
            if (!in_tree_[ai]) continue;
            adj[arcs_[ai].u].push_back({arcs_[ai].v, int(ai)});
            adj[arcs_[ai].v].push_back({arcs_[ai].u, int(ai)});
        }
        for (int s = 0; s < n_; s++) {
            if (assigned[s]) continue;
            assigned[s] = 1; pi2[s] = 0.0;
            std::vector<int> stack{s};
            while (!stack.empty()) {
                int x = stack.back(); stack.pop_back();
                for (auto [y, ai] : adj[x]) {
                    if (assigned[y]) continue;
                    assigned[y] = 1;
                    const Arc& a = arcs_[ai];
                    if (a.u == y) pi2[y] = a.cost + pi2[x];
                    else pi2[y] = pi2[x] - a.cost;
                    stack.push_back(y);
                }
            }
        }
        return pi2;
    }

    Result finish(int iters) {
        Result r;
        r.iterations = iters;
        for (size_t ai = edges_.size() * 2; ai < arcs_.size(); ai++)
            if (flow_[ai] > 1e-7)
                throw std::runtime_error("netsimplex: infeasible (artificial arc carries flow; "
                                         "disconnected component with imbalance?)");
        r.net.assign(edges_.size(), 0.0);
        r.cost = 0.0;
        for (size_t ei = 0; ei < edges_.size(); ei++) {
            double f_fwd = flow_[ei * 2], f_bwd = flow_[ei * 2 + 1];
            r.net[ei] = f_fwd - f_bwd;
            r.cost += arcs_[ei * 2].cost * f_fwd + arcs_[ei * 2 + 1].cost * f_bwd;
        }
        // reduced-cost classification, spec 2.8's three branches, over OFF-SUPPORT arcs:
        // nonbasic arcs by their reduced cost (computed against clean real-rooted potentials,
        // so no artificial-arc scale contaminates the small values), plus degenerate basic
        // arcs (zero flow, rc = 0 by construction) -- the latter is how a genuine tie appears
        // when this solver's basis includes the tied arc (paper's state on 1444: a 78-arc
        // support on an 80-node tree)
        std::vector<double> pi2 = clean_potentials();
        for (size_t ai = 0; ai < edges_.size() * 2; ai++) {
            if (in_tree_[ai]) {
                if (flow_[ai] <= RC_ZERO) r.ties_blocked++;
                continue;
            }
            const Arc& a = arcs_[ai];
            double c = a.cost - pi2[a.u] + pi2[a.v];
            if (std::fabs(c) <= RC_ZERO) {
                if (can_carry(ai)) r.ties_open++;
                else r.ties_blocked++;
            } else {
                double m = std::fabs(c);   // |c|: a tiny negative residue is still a margin
                if (r.smallest_positive_rc == 0.0 || m < r.smallest_positive_rc)
                    r.smallest_positive_rc = m;
            }
        }
        return r;
    }

    // can a zero-reduced-cost non-basic arc carry flow in an optimum? Adding it closes a tree
    // cycle; it can iff a strictly positive theta fits around that cycle.
    bool can_carry(size_t enter) {
        std::vector<std::pair<int, int>> cyc;
        cycle_arcs(arcs_[enter].u, arcs_[enter].v, cyc);
        double theta = std::numeric_limits<double>::infinity();
        for (auto [a, s] : cyc)
            if (s < 0) theta = std::min(theta, flow_[a]);
        return theta > 1e-12;   // infinity (no bound) counts as carry-capable
    }
};

} // namespace netsimplex
