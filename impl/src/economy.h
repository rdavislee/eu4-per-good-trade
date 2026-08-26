// The per-good economy (spec 1.8, 2.6, 3.14): what the network ROUTES, given the orientation.
//
// For one good g over its DRAIN graph, with the engine's own inject_g(n) as origination and the
// engine's per-node per-country modified trade power + merchant intent as the power inputs:
//
//   collected_share(n,g) = 1                                 if n is a sink for g
//                        = P_collect / (P_collect + P_transfer(g))   otherwise
//   P_transfer(g) counts a country's power only if it steers g at n, or collects at some node
//   reachable from n in g's graph (per-good eligibility, spec 1.8 / 3.7); inert otherwise.
//   Remainder: if anyone steers g at n, split across outgoing links in proportion to the power
//   steering TOWARD each link (unsteered links get nothing; a lone steerer takes all); else an
//   even split across g's outgoing links. At a sink there is no remainder.
//   Steering adds value: TRADE_ADDED_VALUE_MODIFER per steering merchant on the link (the
//   engine's own "value_added_outgoing"); the boost lands on the downstream node's incoming.
//
// Everything is in the document's ANNUAL basis; the engine-write boundary divides by 12
// (spec 2.6). Orientation is an input here and is never touched -- this file moves money, not
// arrows (spec 1.8: "a manufactory moves inject and with it the money; it does not move the
// arrows").
#pragma once
#include <algorithm>
#include <cmath>
#include <deque>
#include <map>
#include <vector>

namespace econ {

// One country's standing at one node, as the engine holds it (node-wide, good-independent).
struct Standing {
    int country;        // engine country index
    double power;       // modified trade power at this node (merchant bonuses etc. included)
    // DEPARTURE D3 (impl/DEPARTURES.md): power split into what is local to this node and what
    // vanilla propagated here along Phi_w, so the propagation can be redone per good.
    double own = 0;     // power minus the vanilla fifths received along the INSTALLED graph (signed: a deficit is carried, not clamped)
    bool has_own = false;      // own computed (else per-good power falls back to power)
    bool merchant_floor = false;   // a table-owned merchant stands here: final per-good power >= 2
    double pp = 0;      // provincial power here (rec+0x28), the source of propagation
    bool collects;      // collecting here: home node, or a merchant collecting
    int steer_to;       // link end this country's merchant steers toward (node index), or -1
    bool is_capital = false;   // this node is the country's trade capital (home)
};

struct NodeStandings { std::vector<Standing> entries; };

// DEPARTURE D3: per-good trade power. The vanilla rule (spec 1.9, measured on the engine's records
// 2026-08-26: FULL fifth, threshold 2) sends a fifth of a country's PROVINCIAL power at m to every
// node immediately upstream of m along Phi_w. Here the same fifth travels along GOOD g's graph:
//     P_c(n, g) = own_c(n) + sum over m with n -> m in g's graph of [pp_c(m) >= 2] * pp_c(m) / 5
// pp_at[m] maps country -> provincial power at m (built once per tick by pp_index).
constexpr double PROP_THRESHOLD = 2.0;
constexpr double PROP_DIVIDER   = 5.0;
inline std::vector<std::map<int, double>> pp_index(int N, const std::vector<NodeStandings>& st) {
    std::vector<std::map<int, double>> pp_at(N);
    for (int n = 0; n < N && n < (int)st.size(); n++) for (auto& e : st[n].entries) if (e.pp > 0) pp_at[n][e.country] = e.pp;
    return pp_at;
}
inline double prop_from(const std::vector<std::map<int, double>>& pp_at, const std::vector<int>& downs, int country) {
    double p = 0;
    for (int m : downs) { if (m < 0 || m >= (int)pp_at.size()) continue; auto it = pp_at[m].find(country); if (it != pp_at[m].end() && it->second >= PROP_THRESHOLD) p += it->second / PROP_DIVIDER; }
    return p;
}
// DEPARTURE D3 v2 (user, 2026-08-26): trade power stays ONE number per node. What becomes
// good-aware is how a node's fifth is DIVIDED among its neighbours: the fifth is split among the
// goods by price, and each good's portion goes to the neighbours upstream of m in THAT good's
// graph (equally among them if several). Goods with no upstream neighbour at m take no share, so
// the fifth is fully distributed whenever anything flows into m.
//   split[m][n] = sum over goods g with n in U_g(m) of  (w_g / |U_g(m)|)  /  sum over goods g with U_g(m) != {} of w_g
//   received_c(n) = sum over m of [pp_c(m) >= 2] * pp_c(m)/5 * split[m][n]
//   P_c(n) = own_c(n) + received_c(n)      (own = the engine's aggregate minus vanilla's full fifths)
inline std::vector<std::map<int, double>> propagation_split(int N,
        const std::vector<std::vector<std::pair<int, int>>>& graphs, const std::vector<double>& prices) {
    std::vector<std::map<int, double>> split(N);      // m -> (n -> share of m's fifth)
    std::vector<double> denom(N, 0.0);
    std::vector<std::vector<std::vector<int>>> up(graphs.size());   // [g][m] = upstream neighbours of m in g
    for (size_t g = 0; g < graphs.size(); g++) {
        up[g].assign(N, {});
        for (auto& [u, v] : graphs[g]) if (u >= 0 && u < N && v >= 0 && v < N) up[g][v].push_back(u);
        double w = g < prices.size() ? prices[g] : 1.0; if (w <= 0) w = 1.0;
        for (int m = 0; m < N; m++) if (!up[g][m].empty()) denom[m] += w;
    }
    for (size_t g = 0; g < graphs.size(); g++) {
        double w = g < prices.size() ? prices[g] : 1.0; if (w <= 0) w = 1.0;
        for (int m = 0; m < N; m++) {
            if (up[g][m].empty() || denom[m] <= 0) continue;
            double per = (w / (double)up[g][m].size()) / denom[m];
            for (int n : up[g][m]) split[m][n] += per;
        }
    }
    return split;
}
// received power by (node, country) under the split rule
inline std::vector<std::map<int, double>> propagation_received(int N, const std::vector<std::map<int, double>>& pp_at,
                                                                const std::vector<std::map<int, double>>& split) {
    std::vector<std::map<int, double>> recv(N);
    for (int m = 0; m < N && m < (int)pp_at.size(); m++)
        for (auto& [c, pp] : pp_at[m]) {
            if (pp < PROP_THRESHOLD) continue;
            double F = pp / PROP_DIVIDER;
            for (auto& [n, sh] : split[m]) if (n >= 0 && n < N) recv[n][c] += F * sh;
        }
    return recv;
}
// apply: every standing's power becomes own + received (clamped at 0, merchant floor kept), and a
// country that receives power at a node where it had no standing gets one (the engine has a
// record slot for every country at every node, so it can be written there too)
inline int apply_split_propagation(int N, std::vector<NodeStandings>& st, const std::vector<std::map<int, double>>& recv) {
    int added = 0;
    for (int n = 0; n < N && n < (int)st.size(); n++) {
        std::map<int, double> left = n < (int)recv.size() ? recv[n] : std::map<int, double>{};
        for (auto& e : st[n].entries) {
            double base = e.has_own ? e.own : e.power;
            double r = 0; auto it = left.find(e.country); if (it != left.end()) { r = it->second; left.erase(it); }
            double v = base + r; if (v < 0) v = 0;
            if (e.merchant_floor && v < 2.0) v = 2.0;
            e.power = v;
        }
        for (auto& [c, r] : left) {
            if (r <= 0) continue;
            Standing s{}; s.country = c; s.power = r; s.own = 0; s.has_own = true; s.pp = 0; s.collects = false; s.steer_to = -1;
            st[n].entries.push_back(s); added++;
        }
    }
    return added;
}

inline std::vector<std::vector<double>> per_good_power(int N, const std::vector<std::pair<int, int>>& directed,
                                                       const std::vector<NodeStandings>& st,
                                                       const std::vector<std::map<int, double>>& pp_at) {
    std::vector<std::vector<int>> outs(N);
    for (auto& [u, v] : directed) if (u >= 0 && u < N) outs[u].push_back(v);
    std::vector<std::vector<double>> P(N);
    for (int n = 0; n < N && n < (int)st.size(); n++) {
        P[n].resize(st[n].entries.size());
        for (size_t i = 0; i < st[n].entries.size(); i++) {
            const Standing& e = st[n].entries[i];
            double base = e.has_own ? e.own : e.power;
            double v = base + prop_from(pp_at, outs[n], e.country);
            if (v < 0) v = 0;                                   // clamp the FINAL power, never the deficit (reviewed)
            if (e.merchant_floor && v < 2.0) v = 2.0;           // the merchant-present bonus, on the final power
            P[n][i] = v;
        }
    }
    return P;
}

// Result of routing one good.
struct GoodFlow {
    std::vector<double> value;            // value_g(n) = inject + incoming (annual)
    std::vector<double> incoming;         // Σ realized inflow incl. steering bonus
    std::vector<double> collected_share;  // spec 1.8
    std::vector<double> collected;        // value * collected_share  (the collectible pool, per good)
    std::vector<double> outgoing;         // value * (1 - collected_share)
    std::vector<double> p_collect, p_transfer;   // the two power sums used
    std::vector<std::map<int, double>> flow;     // flow[n][m] = realized value leaving n toward m (pre-bonus)
    std::vector<std::map<int, double>> bonus;    // bonus[n][m] = steering value added on that link
    std::vector<std::map<int, int>> steerers;    // steerers[n][m] = number of merchants steering n->m
    std::vector<bool> is_sink;
    std::vector<int> topo;                       // the order used
};

// steering value bonus for k merchants on one link: the first adds the full modifier, each
// further merchant half of the previous (the engine's diminishing "value added" -- the exact
// engine schedule is a flow-pass fact the live comparison pins; the modifier itself is the
// define TRADE_ADDED_VALUE_MODIFER = 0.05).
inline double steer_bonus(int k, double modifier) {
    double b = 0, step = modifier;
    for (int i = 0; i < k; i++) { b += step; step *= 0.5; }
    return b;
}

// reachability: reach[n] = set of nodes reachable from n (including n) over `directed`
inline std::vector<std::vector<char>> reach_sets(int N, const std::vector<std::vector<int>>& outs) {
    std::vector<std::vector<char>> R(N, std::vector<char>(N, 0));
    for (int s = 0; s < N; s++) {
        std::vector<int> st{s};
        R[s][s] = 1;
        while (!st.empty()) {
            int x = st.back(); st.pop_back();
            for (int y : outs[x]) if (!R[s][y]) { R[s][y] = 1; st.push_back(y); }
        }
    }
    return R;
}

inline std::vector<int> topo_order(int N, const std::vector<std::vector<int>>& outs) {
    std::vector<int> indeg(N, 0);
    for (int u = 0; u < N; u++) for (int v : outs[u]) indeg[v]++;
    std::deque<int> q;
    for (int i = 0; i < N; i++) if (indeg[i] == 0) q.push_back(i);
    std::vector<int> order;
    while (!q.empty()) {
        int x = q.front(); q.pop_front();
        order.push_back(x);
        for (int y : outs[x]) if (--indeg[y] == 0) q.push_back(y);
    }
    return order;
}

// Route one good. `directed` is g's orientation; `inject[n]` the engine's produced value of g at
// n (annual); `standings[n]` the engine's per-country power/intent at n; `collect_nodes[c]` the
// nodes where country c collects (for the reachability leg of eligibility).
//
// `precomputed_reach` (optional) is this good's reachability matrix. It depends only on the
// orientation, so when the orientation is cached across ticks the matrix can be too -- which is
// what keeps the tick hook's cost off the game thread (spec H3).
inline GoodFlow route(int N, const std::vector<std::pair<int, int>>& directed,
                      const std::vector<double>& inject,
                      const std::vector<NodeStandings>& standings,
                      const std::map<int, std::vector<int>>& collect_nodes,
                      double added_value_modifier,
                      const std::vector<std::vector<char>>* precomputed_reach = nullptr,
                      const std::vector<std::vector<double>>* power_g = nullptr) {   // D3: per-good power, else s.power
    std::vector<std::vector<int>> outs(N);
    for (auto& [u, v] : directed) outs[u].push_back(v);
    for (auto& o : outs) std::sort(o.begin(), o.end());
    std::vector<std::vector<char>> R_local;
    if (!precomputed_reach) R_local = reach_sets(N, outs);
    const std::vector<std::vector<char>>& R = precomputed_reach ? *precomputed_reach : R_local;
    GoodFlow F;
    F.value.assign(N, 0.0); F.incoming.assign(N, 0.0); F.collected_share.assign(N, 0.0);
    F.collected.assign(N, 0.0); F.outgoing.assign(N, 0.0);
    F.p_collect.assign(N, 0.0); F.p_transfer.assign(N, 0.0);
    F.flow.assign(N, {}); F.bonus.assign(N, {}); F.steerers.assign(N, {});
    F.is_sink.assign(N, false);
    F.topo = topo_order(N, outs);
    std::vector<double> carried(N, 0.0);
    for (int n = 0; n < N; n++) carried[n] = inject[n];

    for (int n : F.topo) {
        F.value[n] = carried[n];
        const auto& S = standings[n].entries;
        auto PW = [&](size_t i) -> double { return (power_g && n < (int)power_g->size() && i < (*power_g)[n].size()) ? (*power_g)[n][i] : S[i].power; };
        if (outs[n].empty()) {                       // sink for g: no remainder
            F.is_sink[n] = true;
            F.collected_share[n] = 1.0;
            F.collected[n] = F.value[n];
            for (size_t i = 0; i < S.size(); i++) if (S[i].collects) F.p_collect[n] += PW(i);
            continue;
        }
        // power sums, per-good eligibility
        double pc = 0, pt = 0;
        std::map<int, double> steer_power;       // link end -> power steering toward it
        std::map<int, int> steer_count;
        for (size_t si = 0; si < S.size(); si++) {
            const Standing& s = S[si];
            const double spower = PW(si);
            if (spower <= 0) continue;
            if (s.collects) { pc += spower; continue; }
            bool steers_g = false;
            if (s.steer_to >= 0 &&
                std::find(outs[n].begin(), outs[n].end(), s.steer_to) != outs[n].end()) {
                steers_g = true;
                steer_power[s.steer_to] += spower;
                steer_count[s.steer_to] += 1;
            }
            bool reaches_collector = false;
            if (!steers_g) {
                auto it = collect_nodes.find(s.country);
                if (it != collect_nodes.end())
                    for (int H : it->second) {
                        // H == n is NOT downstream. reach_sets marks every node reachable from
                        // itself (R[s][s] = 1), so without this guard a country that collects AT n
                        // counts as transferring value AWAY from n -- the very node it collects at.
                        // Spec 1.8 means a node reachable from n in g's graph, somewhere the value
                        // would actually arrive; collecting here is what P_collect is for, and the
                        // `s.collects` branch above has already taken that case.
                        //
                        // Measured cost of the missing guard, at north_sea on a 1444 start: every
                        // one of the thirteen contributors to P_transfer qualified as "collects at
                        // north_sea", putting P_transfer at 0.33 against a P_collect of 0.017. The
                        // collected share fell to 0.049 and 46.9 of 49.4 livestock left the node --
                        // all of it to st_lawrence, the only out-arc and an empty node in 1444.
                        if (H == n) continue;
                        if (H >= 0 && H < N && R[n][H]) { reaches_collector = true; break; }
                    }
            }
            if (steers_g || reaches_collector) pt += spower;   // else inert for g
        }
        F.p_collect[n] = pc; F.p_transfer[n] = pt;
        // The engine's own branch, at the tail of 0xB593F0:
        //     0xB5961C  movsxd rcx,[r13]     ; pull
        //     0xB59620  test   ecx,ecx
        //     0xB59624  mov    edi,0x3E8     ; pull == 0 -> retention = 1000, keep everything
        // It tests pull ALONE, never reading retain. In model terms: P_transfer == 0 means
        // collected_share == 1, regardless of P_collect. The old 0/0 -> 0.0 was inverted
        // against that: an uninhabited node (every New World node in 1444 has NO standings
        // at all) forwarded 100% of whatever reached it. Identical to the old value wherever
        // pc > 0; differs only at pc == pt == 0, where the engine keeps.
        double cs = (pt > 0) ? pc / (pc + pt) : 1.0;
        F.collected_share[n] = cs;
        F.collected[n] = F.value[n] * cs;
        F.outgoing[n] = F.value[n] - F.collected[n];
        // split the remainder
        if (!steer_power.empty()) {
            double tot = 0; for (auto& [m, p] : steer_power) tot += p;
            for (auto& [m, p] : steer_power) {
                double f = F.outgoing[n] * (p / tot);
                int k = steer_count[m];
                double b = f * steer_bonus(k, added_value_modifier);
                F.flow[n][m] = f; F.bonus[n][m] = b; F.steerers[n][m] = k;
                carried[m] += f + b;
                F.incoming[m] += f + b;
            }
            // unsteered links receive nothing (spec 1.8, load-bearing)
        } else {
            double share = F.outgoing[n] / (double)outs[n].size();
            for (int m : outs[n]) {
                F.flow[n][m] = share; F.bonus[n][m] = 0.0;
                carried[m] += share;
                F.incoming[m] += share;
            }
        }
    }
    return F;
}

// Survival table S[n][H] for one good under the CURRENT merchant field (spec 3.14): the fraction
// of a unit of g at n that is collected at H, multiplying through collected_share, the steering
// shares and the per-link bonus. Row sums exceed 1 only by the steering bonus (value is added).
inline std::vector<std::vector<double>> survival(int N, const GoodFlow& F,
                                                 const std::vector<std::pair<int, int>>& directed) {
    std::vector<std::vector<int>> outs(N);
    for (auto& [u, v] : directed) outs[u].push_back(v);
    std::vector<std::vector<double>> S(N, std::vector<double>(N, 0.0));
    for (auto it = F.topo.rbegin(); it != F.topo.rend(); ++it) {
        int n = *it;
        S[n][n] += F.collected_share[n];
        if (F.is_sink[n]) continue;
        double rem = 1.0 - F.collected_share[n];
        if (rem <= 0) continue;
        // link shares as realized (steered proportions, or even split)
        double out_total = F.outgoing[n];
        for (int m : outs[n]) {
            double share;
            auto fi = F.flow[n].find(m);
            if (out_total > 0 && fi != F.flow[n].end()) share = fi->second / out_total;
            else if (F.flow[n].empty()) share = 1.0 / outs[n].size();
            else share = (fi == F.flow[n].end()) ? 0.0 : (1.0 / outs[n].size());
            if (share <= 0) continue;
            int k = 0; auto ki = F.steerers[n].find(m); if (ki != F.steerers[n].end()) k = ki->second;
            double mult = 1.0 + (k > 0 ? steer_bonus(k, 0.05) : 0.0);
            for (int H = 0; H < N; H++) S[n][H] += rem * share * mult * S[m][H];
        }
    }
    return S;
}

// The engine-facing aggregate of all goods at a node (spec 2.6's table), annual.
struct NodeAggregate {
    double total = 0;        // Σ_g value_g(n)
    double pool = 0;         // Σ_g value_g(n) * collected_share(n,g)
    double local = 0;        // Σ_g inject_g(n)   (must equal the engine's own local, spec B4)
    double incoming = 0;     // Σ_g incoming_g(n)
    double outgoing = 0;     // Σ_g outgoing_g(n)
};

// DIRECTED gross realized flow on every ordered pair actually carrying value:
// gross[(u,v)] = Σ_g (flow_g(u->v) + bonus_g(u->v)) >= 0.
// This -- not the signed net -- is what the engine's incoming-link record for v must hold: the
// value that actually ARRIVES at v along that link. Both directions of a physical link can carry
// value at once (different goods, spec 1.12), and each is reported as its own non-negative figure,
// which is also what keeps a negative from ever reaching the UI (spec 1.12/3.9).
inline std::map<std::pair<int, int>, double> gross_link_flows(
        const std::vector<GoodFlow>& per_good) {
    std::map<std::pair<int, int>, double> gross;
    for (auto& F : per_good)
        for (int u = 0; u < (int)F.flow.size(); u++)
            for (auto& [v, val] : F.flow[u]) {
                double b = 0;
                auto bi = F.bonus[u].find(v);
                if (bi != F.bonus[u].end()) b = bi->second;
                gross[{u, v}] += val + b;
            }
    return gross;
}

// per-link net realized flow in the installed Phi_w direction (u->v): Σ_g flow(u->v) - flow(v->u)
inline std::map<std::pair<int, int>, double> net_link_flows(
        const std::vector<std::pair<int, int>>& phi_w, const std::vector<GoodFlow>& per_good) {
    std::map<std::pair<int, int>, double> net;
    for (auto& [u, v] : phi_w) {
        double f = 0;
        for (auto& F : per_good) {
            auto a = F.flow[u].find(v); if (a != F.flow[u].end()) f += a->second + F.bonus[u].at(v);
            auto b = F.flow[v].find(u); if (b != F.flow[v].end()) f -= b->second + F.bonus[v].at(u);
        }
        net[{u, v}] = f;
    }
    return net;
}

// DIRECTED flow WITHOUT the steering bonus.
//
// route() is deliberately asymmetric: `F.outgoing[n] = value - collected` excludes the steering
// bonus, while `F.incoming[m] += f + b` includes it -- the bonus is value the steerer pulls in at
// the receiving end, not value the sender parted with. So the two ends of one directed edge carry
// slightly different figures, and the write-back must use the matching one at each end or the
// node identity stops closing:
//   Sigma_over_edges away(n->m)      == agg.outgoing   (use THIS, no bonus)
//   Sigma_over_edges toward(m->n)+b  == agg.incoming   (use gross_link_flows, with bonus)
// Mixing them is what put "11" on a map panel beside "3" in the node window.
inline std::map<std::pair<int, int>, double> directed_flows_no_bonus(
        const std::vector<GoodFlow>& per_good) {
    std::map<std::pair<int, int>, double> out;
    for (auto& F : per_good)
        for (int u = 0; u < (int)F.flow.size(); u++)
            for (auto& [v, val] : F.flow[u]) out[{u, v}] += val;
    return out;
}

inline std::vector<NodeAggregate> aggregate(int N, const std::vector<GoodFlow>& per_good,
                                            const std::vector<std::vector<double>>& inject) {
    std::vector<NodeAggregate> A(N);
    for (size_t g = 0; g < per_good.size(); g++) {
        const auto& F = per_good[g];
        for (int n = 0; n < N; n++) {
            A[n].total += F.value[n];
            A[n].pool += F.collected[n];
            A[n].local += inject[g][n];
            A[n].incoming += F.incoming[n];
            A[n].outgoing += F.outgoing[n];
        }
    }
    return A;
}

} // namespace econ
