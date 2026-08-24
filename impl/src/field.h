// The model field (spec 1.2-1.4, 1.6): per-province wealth -- owner-agnostic, three inputs
// (development, trade good, own condition) -- node sums, per-good supply/demand shares,
// alpha, and the Phase-2 tie-break cost vector (spec 2.3).
//
// Wealth reads the save's own province state: the engine applied on_startup itself, so
// devastation arrives from the save rather than from a hardcoded table. Only owned provinces
// lying in a trade node are counted (2,472 at 1444).
#pragma once
#include <cmath>
#include <map>
#include <string>
#include <vector>
#include "gamedata.h"
#include "save.h"

namespace field {

constexpr double TAX_COEFF = 1.0;       // measured constant, in no shipped file (spec 2.3)
constexpr double A_PHI = 2.0;           // aggregate exponent, hyperparameter (spec 2.3)
constexpr double ALPHA_K = 1.0;         // alpha price exponent k (spec 1.4)
constexpr double ALPHA_MIN = 0.2, ALPHA_MAX = 3.0;
constexpr double P0 = 2.0;              // alpha price anchor (spec 3.5)

struct Row {                             // one counted province
    int pid;
    int node;                            // node index
    std::string good;
    double tax, trade_value;             // annual ducats; wealth = tax + trade_value
};

struct Field {
    int N = 0;                           // nodes
    std::vector<std::string> goods;      // sorted, gold/unknown excluded
    std::map<std::string, int> gidx;
    std::vector<Row> rows;               // ascending pid
    std::vector<double> node_wealth;     // per node, sum of row wealth
    std::vector<std::vector<double>> S, C;   // [good][node] supply/demand shares
    std::vector<char> live;              // world production > 0
    std::vector<double> alpha;           // per good
    std::vector<double> world_gp;        // per good, world goods_produced
    std::vector<double> V;               // price * world_gp (orientation-model value weight)
    double world_wealth = 0;

    // Phase-2 arc costs: for edge list E, cost is symmetric per edge (spec 2.3)
    std::vector<double> tie_cost_edge;   // per undirected edge
};

inline double price_of(const std::string& good,
                       const std::map<std::string, double>& current,
                       const std::map<std::string, double>& base) {
    auto it = current.find(good);
    if (it != current.end()) return it->second;
    auto ib = base.find(good);
    return ib != base.end() ? ib->second : 0.0;
}

inline Field build(const gamedata::TradeNodes& tn, const gamedata::StaticMods& sm,
                   const save::SaveData& sd, const std::map<std::string, double>& base_prices,
                   double tie_eps = 1e-3, double tie_eps2 = 1e-6) {
    Field f;
    f.N = int(tn.order.size());
    for (auto& [g, p] : base_prices)
        if (g != "gold" && g != "unknown") f.goods.push_back(g);   // std::map iterates sorted
    for (int i = 0; i < int(f.goods.size()); i++) f.gidx[f.goods[i]] = i;
    int G = int(f.goods.size());

    // counted rows, ascending pid (save order)
    for (const save::Province& p : sd.provinces) {
        if (!p.has_owner) continue;
        auto nit = tn.pnode.find(p.id);
        if (nit == tn.pnode.end()) continue;
        double price = price_of(p.trade_goods, sd.current_prices, base_prices);
        // the one state modifier with a scaling law: -2 x level/100 (spec 1.3; probe 18)
        double gmod = sm.state_goods_mod.at("devastation") * (p.devastation / 100.0);
        double gp = sm.gp_coeff * p.base_production * (1.0 + gmod);
        if (gp < 0.0) gp = 0.0;
        Row r;
        r.pid = p.id; r.node = nit->second; r.good = p.trade_goods;
        r.tax = TAX_COEFF * p.base_tax;
        r.trade_value = gp * price;
        f.rows.push_back(std::move(r));
    }

    f.node_wealth.assign(f.N, 0.0);
    double wmax = 0.0;
    for (auto& r : f.rows) {
        double w = r.tax + r.trade_value;
        f.node_wealth[r.node] += w;
        f.world_wealth += w;
        if (w > wmax) wmax = w;
    }

    // supply: goods_produced node shares (per-province gp re-derived from the row: gp = tv/price
    // would divide by zero on zero-price goods, so recompute from save data order-faithfully)
    std::vector<std::vector<double>> gp_node(G, std::vector<double>(f.N, 0.0));
    {
        size_t ri = 0;
        for (const save::Province& p : sd.provinces) {
            if (!p.has_owner || !tn.pnode.count(p.id)) continue;
            const Row& r = f.rows[ri++];
            auto git = f.gidx.find(p.trade_goods);
            if (git != f.gidx.end()) {
                double gmod = sm.state_goods_mod.at("devastation") * (p.devastation / 100.0);
                double gp = sm.gp_coeff * p.base_production * (1.0 + gmod);
                if (gp < 0.0) gp = 0.0;
                gp_node[git->second][r.node] += gp;
            }
        }
    }
    f.world_gp.assign(G, 0.0);
    f.live.assign(G, 0);
    f.S.assign(G, std::vector<double>(f.N, 0.0));
    for (int gi = 0; gi < G; gi++) {
        double tot = 0.0;
        for (int n = 0; n < f.N; n++) tot += gp_node[gi][n];
        f.world_gp[gi] = tot;
        if (tot > 0) {
            f.live[gi] = 1;
            for (int n = 0; n < f.N; n++) f.S[gi][n] = gp_node[gi][n] / tot;
        }
    }
    // the routed-value supply construction (measure6's val[]): per-good trade_value node sums.
    // Live goods' S above is the goods_produced share; the reference's per-good runs use
    // trade_value shares (val/val.sum()), which equal gp shares scaled by one price -- identical
    // after normalisation. Keep gp shares; they are the spec's 1.2 statement.

    // demand: c(n,g) = node sums of (w/wmax)^alpha(g), normalised (measure6's construction)
    f.alpha.assign(G, 1.0);
    f.C.assign(G, std::vector<double>(f.N, 0.0));
    f.V.assign(G, 0.0);
    for (int gi = 0; gi < G; gi++) {
        double price = price_of(f.goods[gi], sd.current_prices, base_prices);
        double a = std::pow(price / P0, ALPHA_K);
        f.alpha[gi] = std::max(ALPHA_MIN, std::min(ALPHA_MAX, a));
        f.V[gi] = price * f.world_gp[gi];
    }
    for (int gi = 0; gi < G; gi++) {
        double tot = 0.0;
        std::vector<double>& C = f.C[gi];
        for (auto& r : f.rows) {
            double t = std::pow((r.tax + r.trade_value) / wmax, f.alpha[gi]);
            C[r.node] += t;
            tot += t;
        }
        for (int n = 0; n < f.N; n++) C[n] /= tot;
    }

    // tie-break cost per undirected edge (symmetric in the arc): spec 2.3
    //   1 + TIE_EPS*(w[u]+w[v])/2 + TIE_EPS2*frac(min*max*7919), w = min-max normalised node wealth
    double nwmin = f.node_wealth[0], nwmax = f.node_wealth[0];
    for (double w : f.node_wealth) { nwmin = std::min(nwmin, w); nwmax = std::max(nwmax, w); }
    double span = (nwmax - nwmin) != 0.0 ? (nwmax - nwmin) : 1.0;
    f.tie_cost_edge.assign(tn.edges_und.size(), 1.0);
    for (size_t ei = 0; ei < tn.edges_und.size(); ei++) {
        auto [u, v] = tn.edges_und[ei];
        double a1 = (f.node_wealth[u] - nwmin) / span;
        double a2 = (f.node_wealth[v] - nwmin) / span;
        double ip;
        double gen = std::modf(std::min(a1, a2) * std::max(a1, a2) * 7919.0, &ip);
        f.tie_cost_edge[ei] = 1.0 + tie_eps * (a1 + a2) / 2.0 + tie_eps2 * gen;
    }
    return f;
}

// aggregate-graph balance: b_w = 1/N - c_w with c_w from (w/wmax)^A_PHI node sums (spec 1.6)
inline std::vector<double> b_aggregate(const Field& f) {
    double wmax = 0.0;
    for (auto& r : f.rows) wmax = std::max(wmax, r.tax + r.trade_value);
    std::vector<double> c(f.N, 0.0);
    double tot = 0.0;
    for (auto& r : f.rows) {
        double t = std::pow((r.tax + r.trade_value) / wmax, A_PHI);
        c[r.node] += t; tot += t;
    }
    std::vector<double> b(f.N);
    for (int n = 0; n < f.N; n++) b[n] = 1.0 / f.N - c[n] / tot;
    return b;
}

// per-good balance b_g = s_g - c_g; supply share from trade_value node sums (measure6's val[]),
// which equals the gp share exactly on any single-priced good
inline std::vector<double> b_good(const Field& f, int gi) {
    std::vector<double> b(f.N);
    for (int n = 0; n < f.N; n++) b[n] = f.S[gi][n] - f.C[gi][n];
    return b;
}

} // namespace field
