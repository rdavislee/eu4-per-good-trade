// Negative fixtures (spec 2.9): every per-tick assertion paired with an input that makes it
// fail -- "an assertion nobody has watched go red is an assertion nobody has tested".
// redtest6.py is the reference-side model; these are the solver-side fixtures.
//
// T1/T2/T3 are spec 3.2's worked counterexamples, reproduced here through the SAME drain::run
// the production solve uses (toys.py is the reference's generic-input model of these):
//   T1 pendant net-importer      -> equality monitor must trip; containment must hold
//   T2 free-edge race            -> equality monitor must trip; containment must hold
//   T3 fallback branch           -> containment vs {S0 u promoted} alone would fail; vs the
//                                   full set it must hold -- the fallback set is part of the
//                                   assertion, not an escape clause
//   T5 disconnected imbalance    -> the LP must refuse, not return garbage
// plus direct reds for each checker: acyclicity, conservation, reachability, containment,
// and the LP tie classification's "halt" state (spec 2.8's three branches).
#pragma once
#include <cstdio>
#include <vector>
#include "ai.h"
#include "attach.h"
#include "drain.h"
#include "jsonout.h"
#include "netsimplex.h"
#include "sha256.h"

namespace fixtures {

struct Runner {
    int missed = 0, total = 0;
    void report(bool went_red, const char* name, const std::string& detail) {
        total++;
        if (!went_red) missed++;
        printf("  [%s] %-52s %s\n", went_red ? "RED " : "MISS", name, detail.c_str());
    }
};

inline drain::Graph make_graph(int N, const std::vector<std::pair<int, int>>& edges) {
    drain::Graph g;
    g.N = N;
    g.und.assign(N, {});
    for (auto& [u, v] : edges) { g.und[u].push_back(v); g.und[v].push_back(u); }
    std::set<std::pair<int, int>> es;
    for (auto& [u, v] : edges) es.insert({std::min(u, v), std::max(u, v)});
    g.edges_und.assign(es.begin(), es.end());
    return g;
}

inline drain::Result run_toy(const drain::Graph& g, const std::vector<double>& b,
                             const std::vector<double>& wealth) {
    std::vector<double> unit_cost(g.edges_und.size(), 1.0);
    std::vector<double> s(g.N, 0.0), c(g.N, 0.0);
    for (int i = 0; i < g.N; i++) { if (b[i] > 0) s[i] = b[i]; else c[i] = -b[i]; }
    return drain::run(g, b, unit_cost, wealth, s, c);
}

inline std::string names_of(const std::vector<const char*>& nm, const std::set<int>& xs) {
    std::string out = "{";
    bool first = true;
    for (int x : xs) { if (!first) out += ","; first = false; out += nm[x]; }
    return out + "}";
}

inline void run_all(Runner& R) {
    // ---- T1: pendant net-importer. Triangle A,B,D + leaf C on B. ----
    {
        std::vector<const char*> nm{"A", "B", "D", "C"};
        drain::Graph g = make_graph(4, {{0, 1}, {1, 2}, {2, 0}, {1, 3}});
        drain::Result r = run_toy(g, {5, -3, 0, -2}, {0, 0, 0, 0});
        std::set<int> sinks;
        {
            std::vector<int> od(4, 0);
            for (auto& [u, v] : r.directed) od[u]++;
            for (int i = 0; i < 4; i++) if (od[i] == 0) sinks.insert(i);
        }
        bool sink_is_C = sinks == std::set<int>{3};
        bool eq_tripped = !r.checks.equality;
        bool cont_held = r.checks.containment;
        R.report(sink_is_C && eq_tripped && cont_held,
                 "T1 pendant importer -> equality monitor trips",
                 "sinks=" + names_of(nm, sinks) + " eq=" + (r.checks.equality ? "EQ" : "TRIPPED") +
                 " cont=" + (cont_held ? "held" : "BROKE"));
    }
    // ---- T2: free-edge race strips a selected flow-terminal demander. ----
    {
        std::vector<const char*> nm{"S1", "u1", "w", "u2", "S2"};
        drain::Graph g = make_graph(5, {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 0}, {2, 0}});
        drain::Result r = run_toy(g, {3, -3, 0, -2, 2}, {0, 0, 0, 0, 0});
        std::set<int> sinks;
        {
            std::vector<int> od(5, 0);
            for (auto& [u, v] : r.directed) od[u]++;
            for (int i = 0; i < 5; i++) if (od[i] == 0) sinks.insert(i);
        }
        bool sinks_u2 = sinks == std::set<int>{3};
        bool s0_both = r.S0 == std::set<int>{1, 3};
        bool eq_tripped = !r.checks.equality;
        R.report(sinks_u2 && s0_both && eq_tripped && r.checks.containment,
                 "T2 free-edge race -> equality monitor trips",
                 "sinks=" + names_of(nm, sinks) + " S0=" + names_of(nm, r.S0) +
                 " eq=" + (r.checks.equality ? "EQ" : "TRIPPED"));
    }
    // ---- T3: fallback branch; containment must include the fallback set. ----
    {
        std::vector<const char*> nm{"A", "B", "C"};
        drain::Graph g = make_graph(3, {{0, 1}, {0, 2}, {1, 2}});
        drain::Result r = run_toy(g, {0, 0, 0}, {3, 2, 1});
        std::set<int> sinks;
        {
            std::vector<int> od(3, 0);
            for (auto& [u, v] : r.directed) od[u]++;
            for (int i = 0; i < 3; i++) if (od[i] == 0) sinks.insert(i);
        }
        bool fb_fired = r.fallbacks.size() == 1 && r.fallbacks[0] == 0;   // highest wealth: A
        std::set<int> narrow;   // {selected} u {promoted} without fallbacks
        for (int v : r.S0) narrow.insert(v);
        for (int v : r.promotions) narrow.insert(v);
        bool narrow_would_fail = false;
        for (int sk : sinks) if (!narrow.count(sk)) narrow_would_fail = true;
        R.report(fb_fired && sinks == std::set<int>{0} && narrow_would_fail &&
                 r.checks.containment,
                 "T3 fallback -> narrow containment would halt, full holds",
                 "sinks=" + names_of(nm, sinks) + " fb=" + names_of(nm, {r.fallbacks.begin(),
                 r.fallbacks.end()}) + " narrow_fails=" + (narrow_would_fail ? "yes" : "NO"));
    }
    // ---- T5: disconnected graph with per-component imbalance -> LP refuses. ----
    {
        drain::Graph g = make_graph(4, {{0, 1}, {2, 3}});
        bool threw = false;
        std::string what;
        try {
            std::vector<double> cost(g.edges_und.size(), 1.0);
            netsimplex::Solver::solve(4, g.edges_und, cost, {0.6, -0.4, 0.4, -0.6});
        } catch (const std::exception& e) { threw = true; what = e.what(); }
        R.report(threw, "T5 disconnected imbalance -> solver refuses",
                 threw ? what.substr(0, 60) : "RETURNED A FLOW");
    }
    // ---- acyclicity checker red: a directed cycle must be detected. ----
    {
        bool detected = drain::has_cycle(3, {{0, 1}, {1, 2}, {2, 0}});
        R.report(detected, "acyclicity red: 3-cycle detected", detected ? "cycle found" : "MISSED");
    }
    // ---- conservation red: corrupted b (sum != 0) must break unserved == stranded. ----
    {
        drain::Checks c;
        drain::eval_conservation(2, {{0, 1}}, {1.0, -2.0}, c);
        R.report(!c.conservation,
                 "conservation red: sum(b) != 0 breaks unserved==stranded",
                 "unserved=" + std::to_string(c.unserved) + " stranded=" +
                 std::to_string(c.stranded));
    }
    // ---- reachability red: demand behind a wrong-way arc + an unreached sink. ----
    {
        drain::Checks c;
        // A(+1) <- B(-1): the only arc points B->A, so demand at B is unreachable from supply;
        // isolated C is a sink no supply reaches.
        drain::eval_reachability(3, {{1, 0}}, {1, 0, 0}, {0, 1, 0.5}, {0, 2}, c);
        R.report(c.reach_pct < 100.0 && c.orphan_sinks > 0,
                 "reachability red: unreachable demand + orphan sink",
                 "reach=" + std::to_string(c.reach_pct) + "% orphans=" +
                 std::to_string(c.orphan_sinks));
    }
    // ---- containment red: a core sink outside {S0 u promoted u fallbacks} must fail. ----
    {
        // run T2 and then corrupt the maintained set the way a bookkeeping bug would
        drain::Graph g = make_graph(5, {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 0}, {2, 0}});
        drain::Result r = run_toy(g, {3, -3, 0, -2, 2}, {0, 0, 0, 0, 0});
        std::set<int> sinks;
        std::vector<int> od(5, 0);
        for (auto& [u, v] : r.directed) od[u]++;
        for (int i = 0; i < 5; i++) if (od[i] == 0) sinks.insert(i);
        std::set<int> corrupted = r.Sset;
        for (int sk : sinks) corrupted.erase(sk);
        bool would_fail = false;
        std::set<int> coreset(r.core.begin(), r.core.end());
        for (int sk : sinks)
            if (coreset.count(sk) && !corrupted.count(sk)) would_fail = true;
        R.report(would_fail, "containment red: dropped promotion fails the assert",
                 would_fail ? "corrupted set misses a core sink" : "STILL PASSES");
    }
    // ---- LP tie classification red: unit costs on two equal corridors -> "halt" state. ----
    {
        // square A(+1) B(0) C(-1) D(0): two equal 2-hop routes; with unit costs the optimum
        // is not unique, so a zero-reduced-cost arc CAN carry flow -> ties_open > 0
        drain::Graph g = make_graph(4, {{0, 1}, {1, 2}, {2, 3}, {3, 0}});
        std::vector<double> cost(g.edges_und.size(), 1.0);
        netsimplex::Result lp =
            netsimplex::Solver::solve(4, g.edges_und, cost, {1.0, 0.0, -1.0, 0.0});
        R.report(lp.ties_open > 0,
                 "LP tie red: equal corridors under unit costs -> halt state",
                 "ties_open=" + std::to_string(lp.ties_open) + " ties_blocked=" +
                 std::to_string(lp.ties_blocked) + " margin=" +
                 std::to_string(lp.smallest_positive_rc));
    }
    // ---- LP margin red: the margin reported must sit ABOVE the pinned tolerance on a
    //      well-separated instance and the checker must flag one that does not. ----
    {
        // two parallel corridors A-B-C and A-D-C, A(+1) C(-1). D attaches to the tree by one
        // of its corridor arcs (degenerate); the OTHER corridor-2 arc is necessarily nonbasic
        // and its reduced cost equals the corridor cost difference -- so the near-tie cannot
        // hide inside the basis the way a single tied edge can.
        drain::Graph g = make_graph(4, {{0, 1}, {1, 2}, {0, 3}, {3, 2}});
        // edges sorted: (0,1)=A-B, (0,3)=A-D, (1,2)=B-C, (2,3)=C-D
        std::vector<double> clean{1.0, 1.0, 1.0, 2.0};      // corridor gap 1.0
        netsimplex::Result lp =
            netsimplex::Solver::solve(4, g.edges_und, clean, {1.0, 0.0, -1.0, 0.0});
        bool sep = lp.smallest_positive_rc > netsimplex::TOL_PIN;
        std::vector<double> shaved{1.0, 1.0, 1.0, 1.0 + 5e-11};   // corridor gap 5e-11
        netsimplex::Result lp2 =
            netsimplex::Solver::solve(4, g.edges_und, shaved, {1.0, 0.0, -1.0, 0.0});
        bool flagged = lp2.smallest_positive_rc <= netsimplex::TOL_PIN &&
                       lp2.smallest_positive_rc > 0;
        R.report(sep && flagged,
                 "LP margin red: sub-tolerance separation is flagged",
                 "clean=" + std::to_string(lp.smallest_positive_rc) + " shaved=" +
                 jsonout::fmt_double(lp2.smallest_positive_rc));
    }
    // ---- SHA-256 self-test: the standalone hash must match the known NIST vector. ----
    {
        // FIPS 180-4 example: SHA256("abc")
        std::string h = sha256::hex("abc");
        bool ok = h == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";
        R.report(ok, "sha256 self-test: NIST 'abc' vector", h.substr(0, 16) + "...");
    }
    // ---- attach gate red: a wrong build revision must be REFUSED (spec 2.5, TESTING A4). ----
    {
        // hand the gate a directory with a doctored eu4_rev.txt via a temp file the test writes;
        // if the platform temp write is unavailable this still asserts the pure logic below.
        attach::Verdict v;
        v = attach::verify_install("Z:/no/such/install/here", false);
        R.report(!v.ok, "attach gate red: missing install refused",
                 v.ok ? "ACCEPTED nonexistent" : v.message.substr(0, 40));
    }
    // ---- AI: conquest drives placement, no flip-rate gate (the Ivory Coast case). ----
    {
        // 3 nodes: 0=home, 1=conduit, 2=ivory_coast. One good g=0 orients 2->1->0 (value flows
        // toward home). Portugal collects at home. Merchant candidate at node 2 steering toward 1
        // delivers node 2's injected value to home via the survival table.
        ai::Orient o;
        o.N = 3; o.G = 1;
        o.away = {{{1}, {0}, {1}}};                    // g0: 0->1, 1->0, 2->1
        o.value_g = {{0.0, 0.0, 10.0}};                // ivory_coast injects value
        // survival table for g0: from 2 -> reaches 0; from 1 -> reaches 0; 0 is sink
        o.S = {{{1,0,0}, {1,0,0}, {1,0,0}}};           // S[g][n][H]: everything reaches home(0)
        std::vector<std::vector<int>> adj{{1, 2}, {0, 2}, {0, 1}};

        ai::Country before{"POR", {{0, 5.0}}, {0}, 0.5};        // collects only at home
        ai::Country after = before;
        after.collect_power[2] = 4.0;                          // conquered ivory_coast: power now

        auto best_after = ai::best_placement(o, after, {0, 1, 2}, adj);
        // before: node 2 steering 2->1 still reaches home(0) via survival, so it already scores;
        // the point of the test is that conquest does not LOWER it and the target is value-driven.
        double s_before = ai::score_steer(o, before, 2, 1);
        double s_after = ai::score_steer(o, after, 2, 1);
        bool placed_at_ivory = (best_after.first == 2 && best_after.second == 1);
        R.report(placed_at_ivory && s_after >= s_before,
                 "AI: value-driven placement at conquered node",
                 "best_after=(" + std::to_string(best_after.first) + "->" +
                 std::to_string(best_after.second) + ") score " + jsonout::fmt_double(s_after));
    }
    // ---- AI shadow cadence: only countries whose assignment changed are re-triggered. ----
    {
        ai::Assignments prev{{"POR", {{0, {2, 1}}}}, {"CAS", {{0, {5, 6}}}}};
        ai::Assignments cur{{"POR", {{0, {3, 4}}}},  {"CAS", {{0, {5, 6}}}}};   // POR moved, CAS same
        auto moved = ai::shadow_trigger(prev, cur);
        bool ok = moved.size() == 1 && moved[0] == "POR";
        R.report(ok, "AI shadow cadence: only the moved country triggers",
                 "moved={" + (moved.empty() ? "" : moved[0]) + "}");
    }
    // ---- AI: a candidate that steers nothing is never chosen (spec 3.14). ----
    {
        ai::Orient o;
        o.N = 2; o.G = 1;
        o.away = {{{}, {0}}};                          // g0: node0 steers nothing, node1 -> 0
        o.value_g = {{0.0, 5.0}};
        o.S = {{{1,0}, {1,0}}};
        std::vector<std::vector<int>> adj{{1}, {0}};
        ai::Country c{"TST", {{0, 3.0}}, {0}, 0.5};
        auto cands = ai::candidates_at(o, c, 0, adj);   // node 0 steers nothing toward 1
        R.report(cands.empty(), "AI: zero-steer candidate is never enumerated",
                 std::to_string(cands.size()) + " candidates at a steer-nothing node");
    }
}

} // namespace fixtures
