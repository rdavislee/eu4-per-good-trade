// AI merchant assignment (spec 3.14), with the cadence the user chose: SHADOW VANILLA.
//
// Cadence (choice A): vanilla's own AI decides WHEN a country reconsiders a merchant. Each tick
// we diff every AI country's merchant assignments against last tick; when vanilla has moved or
// placed one, that event triggers OUR re-placement -- we score the country's candidates with the
// per-good survival table and put the merchant on the best (node, link-end). This mirrors
// vanilla's cadence by construction (it IS vanilla's trigger), needs no cadence define, and fires
// on conquest for free: vanilla reassesses merchants after territorial change, and by then our
// per-good node values are already in the engine's structures, so a freshly-conquered rich node
// (Portugal taking ivory_coast) scores high and the merchant lands there. Value-driven, no
// flip-rate gate -- and merchants survive flips anyway (spec 1.7).
//
// The choice of TARGET is ours: candidates are (node, incident-link-end) pairs, BOTH tab groups
// (spec 3.14), a candidate's active good set is the goods oriented away from the node on that
// link (read from the per-good orientations, never inferred from the drawn map), and a candidate
// steering nothing scores zero and is never chosen.
//
// A secondary gain-test trigger (dwell-floored) for per-good opportunities vanilla's single-graph
// AI cannot see is present but DISABLED by default (SECONDARY_TRIGGER), keeping the cadence
// strictly mirror-vanilla until asked otherwise.
#pragma once
#include <algorithm>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace ai {

constexpr bool SECONDARY_TRIGGER = false;   // strictly mirror-vanilla until enabled
constexpr double DWELL_FLOOR_MONTHS = 3.0;  // travel not spent on transients (spec 3.14)

// ---- orientation view: per-good directed edges as away-sets per node ----
struct Orient {
    int N;
    // away[g][n] = nodes m with edge n->m oriented for good g (goods steerable from n toward m)
    std::vector<std::vector<std::vector<int>>> away;   // [good][node] -> targets
    // per-good value injected at each node (V_g share the node originates); and collected_share
    std::vector<std::vector<double>> value_g;          // [good][node]
    // survival table per good: S[g][n][H] fraction of a unit of g at n arriving at H
    std::vector<std::vector<std::vector<double>>> S;
    int G;
};

// A country's live power footprint, refreshed every evaluation from engine memory. This is what
// makes the placement value-driven: conquest raises collect_power at the new node immediately.
struct Country {
    std::string tag;
    std::map<int, double> collect_power;   // node -> this country's collecting power there (0 = none)
    std::set<int> home_nodes;              // where the home-node steering bonus applies
    double off_home_penalty = 0.5;         // TRADE_NON_CAPITAL_OFFICE magnitude (power modifier)
};

// value a country captures by STEERING good-set at node n down link n->m: the goods oriented
// n->m, each worth its injected value times the fraction that survives to one of C's collect
// nodes (survival table). Single steerer -> winner-take-all share 1.0 (spec 1.8).
inline double score_steer(const Orient& o, const Country& c, int n, int m,
                          std::vector<int>* active_goods = nullptr) {
    double v = 0.0;
    for (int g = 0; g < o.G; g++) {
        // is n->m oriented for g?
        const auto& aw = o.away[g][n];
        if (std::find(aw.begin(), aw.end(), m) == aw.end()) continue;
        if (active_goods) active_goods->push_back(g);
        double reach = 0.0;
        for (auto& [H, pw] : c.collect_power) if (pw > 0) reach += o.S[g][m][H];
        if (reach > 1.0) reach = 1.0;
        v += o.value_g[g][n] * reach;   // lone steerer takes all of g's outgoing value
    }
    return v;
}

// value a country captures by COLLECTING at node n: its share among collectors of the collectible
// pool. Off-home penalty is a POWER modifier (spec 3.14), so it enters powershare, not a haircut.
inline double score_collect(const Orient& o, const Country& c, int n,
                            double collect_pool_n, double total_collector_power_n) {
    auto it = c.collect_power.find(n);
    if (it == c.collect_power.end() || it->second <= 0) return 0.0;
    double p = it->second;
    if (!c.home_nodes.count(n)) p *= (1.0 - c.off_home_penalty);   // off-home power modifier
    double denom = total_collector_power_n;
    if (denom <= 0) return 0.0;
    return collect_pool_n * (p / denom);
}

struct Candidate {
    int node, target;            // link end at `node` toward `target`
    std::vector<int> active;     // goods oriented away from node on this link
    double score;
};

// enumerate (node, incident-link-end) candidates for a country at one node -- BOTH tab groups:
// every physical link incident to `node`, scored by what steering toward the far end delivers.
inline std::vector<Candidate> candidates_at(const Orient& o, const Country& c, int node,
                                            const std::vector<std::vector<int>>& undirected_adj) {
    std::vector<Candidate> out;
    for (int m : undirected_adj[node]) {
        Candidate cand{node, m, {}, 0.0};
        cand.score = score_steer(o, c, node, m, &cand.active);
        if (cand.active.empty()) continue;      // steers nothing -> never chosen (spec 3.14)
        out.push_back(std::move(cand));
    }
    std::sort(out.begin(), out.end(),
              [](const Candidate& a, const Candidate& b) { return a.score > b.score; });
    return out;
}

// ---- shadow-vanilla cadence ----
// merchant assignment snapshot: per country, the merchant's (node,target) placement by merchant id
using Assignments = std::map<std::string, std::map<int, std::pair<int, int>>>;

// countries whose merchant assignments changed since the previous tick (vanilla fired a move)
inline std::vector<std::string> shadow_trigger(const Assignments& prev, const Assignments& cur) {
    std::vector<std::string> moved;
    for (auto& [tag, cur_m] : cur) {
        auto pit = prev.find(tag);
        if (pit == prev.end() || pit->second != cur_m) moved.push_back(tag);
    }
    return moved;
}

// best target for one merchant of a country: highest-scoring candidate over the nodes the country
// may place in (its reachable / powered nodes). Ties broken by (node index, target index) for
// determinism. Returns {-1,-1} if nothing scores > 0 (leave vanilla's placement).
inline std::pair<int, int> best_placement(const Orient& o, const Country& c,
                                          const std::vector<int>& eligible_nodes,
                                          const std::vector<std::vector<int>>& undirected_adj) {
    Candidate best{-1, -1, {}, 0.0};
    for (int n : eligible_nodes) {
        for (auto& cand : candidates_at(o, c, n, undirected_adj)) {
            if (cand.score > best.score ||
                (cand.score == best.score && best.node >= 0 &&
                 (cand.node < best.node || (cand.node == best.node && cand.target < best.target)))) {
                best = cand;
            }
        }
    }
    return best.node < 0 ? std::make_pair(-1, -1) : std::make_pair(best.node, best.target);
}

// the move test for the OPTIONAL secondary trigger only (disabled by default). expected_tenure is
// a durability horizon floored by the dwell minimum -- NOT a flip counter (merchants survive
// flips). It never suppresses a value-justified move; it only damps churn between near-equal
// candidates by charging the travel cost against a minimum residence.
inline bool secondary_move_ok(double v_new, double v_incumbent, double expected_tenure_months,
                              double travel_time_months) {
    if (!SECONDARY_TRIGGER) return false;
    double tenure = std::max(expected_tenure_months, DWELL_FLOOR_MONTHS);
    return (v_new - v_incumbent) * tenure > v_incumbent * travel_time_months;
}

} // namespace ai
