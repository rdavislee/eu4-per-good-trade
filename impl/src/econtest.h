// Economy fixtures (spec 1.8 / 2.8 rows): each rule of the per-good routing, checked on a toy
// graph, PLUS a negative twin for every check so it is seen going red (spec 2.9).
#pragma once
#include <cmath>
#include <cstdio>
#include <string>
#include <vector>
#include "economy.h"

namespace econtest {
// Standing gained fields after these tests were written (own/has_own/merchant_floor/pp/received): build it by name
static inline econ::Standing econtest_standing(int country, double power, bool collects, int steer_to) {
    econ::Standing st{}; st.country = country; st.power = power; st.collects = collects; st.steer_to = steer_to; return st;
}


struct Runner {
    int failed = 0, total = 0;
    void ok(bool pass, const char* name, const std::string& detail = "") {
        total++;
        if (!pass) failed++;
        printf("  [%s] %-56s %s\n", pass ? "OK  " : "FAIL", name, detail.c_str());
    }
};

inline bool near(double a, double b, double tol = 1e-9) { return std::fabs(a - b) <= tol; }

// toy: chain A(0) -> B(1) -> {C(2), D(3)}; C and D sinks. A produces 12/yr.
inline void run_all(Runner& R) {
    const int N = 4;
    std::vector<std::pair<int, int>> dir{{0, 1}, {1, 2}, {1, 3}};
    std::vector<double> inject{12.0, 0.0, 0.0, 0.0};
    const double MOD = 0.05;

    // --- 1. no merchants anywhere, nobody collects: even split, sinks collect fully ---
    {
        std::vector<econ::NodeStandings> st(N);
        auto F = econ::route(N, dir, inject, st, {}, MOD);
        double collected = 0; for (int n = 0; n < N; n++) collected += F.collected[n];
        R.ok(near(collected, 12.0), "conservation: Σ collected == Σ injected (no merchants)",
             "collected=" + std::to_string(collected));
        R.ok(near(F.collected[2], 6.0) && near(F.collected[3], 6.0), "even split at B: C=D=6");
        R.ok(F.collected_share[2] == 1.0 && F.collected_share[3] == 1.0 && F.is_sink[2] && F.is_sink[3],
             "sinks: collected_share == 1");
        R.ok(near(F.collected_share[1], 0.0), "no power at B -> nothing collected there");
        // negative twin: a wrong graph (B not a sink-feeder) must NOT conserve to 12 at C+D
        std::vector<std::pair<int, int>> bad{{0, 1}};
        auto Fb = econ::route(N, bad, inject, st, {}, MOD);
        R.ok(!near(Fb.collected[2] + Fb.collected[3], 12.0), "red twin: truncated graph strands value at B",
             "B collects " + std::to_string(Fb.collected[1]));
    }
    // --- 2. lone steerer takes ALL of the remainder down its link; unsteered link gets nothing ---
    {
        std::vector<econ::NodeStandings> st(N);
        st[1].entries.push_back(econtest_standing(7, 0.5, false, 2));      // tiny power, steering B->C
        st[1].entries.push_back(econtest_standing(8, 40.0, false, -1));    // big power, inert (no collector reachable)
        auto F = econ::route(N, dir, inject, st, {}, MOD);
        R.ok(near(F.flow[1][2], 12.0) && F.flow[1].count(3) == 0, "lone steerer: winner-take-all (0.5 power vs 40 inert)",
             "flow B->C=" + std::to_string(F.flow[1][2]));
        R.ok(near(F.bonus[1][2], 12.0 * MOD), "steering bonus: +5% value added on the steered link");
        R.ok(near(F.p_transfer[1], 0.5), "inert power excluded from P_transfer",
             "P_transfer=" + std::to_string(F.p_transfer[1]));
        // red twin: make country 8 eligible (it collects at D, reachable) -> P_transfer changes
        std::map<int, std::vector<int>> cn{{8, {3}}};
        auto F2 = econ::route(N, dir, inject, st, cn, MOD);
        R.ok(near(F2.p_transfer[1], 40.5), "red twin: reachable collector makes the power count",
             "P_transfer=" + std::to_string(F2.p_transfer[1]));
    }
    // --- 3. collected_share = Pc/(Pc+Pt) with per-good eligibility ---
    {
        std::vector<econ::NodeStandings> st(N);
        st[1].entries.push_back(econtest_standing(1, 10.0, true, -1));     // collector at B, power 10
        st[1].entries.push_back(econtest_standing(2, 30.0, false, 3));     // steerer toward D, power 30
        st[1].entries.push_back(econtest_standing(3, 60.0, false, -1));    // collects at C (reachable) -> eligible
        std::map<int, std::vector<int>> cn{{3, {2}}};
        auto F = econ::route(N, dir, inject, st, cn, MOD);
        R.ok(near(F.collected_share[1], 10.0 / 100.0), "collected_share = 10/(10+30+60)",
             "cs=" + std::to_string(F.collected_share[1]));
        R.ok(near(F.collected[1], 1.2) && near(F.outgoing[1], 10.8), "pool 1.2, remainder 10.8");
        R.ok(near(F.flow[1][3], 10.8) && F.flow[1].count(2) == 0, "remainder follows the only steerer (to D)");
        // red twin: country 3 collecting at an UNREACHABLE node (A) is inert
        std::map<int, std::vector<int>> cn2{{3, {0}}};
        auto F2 = econ::route(N, dir, inject, st, cn2, MOD);
        R.ok(near(F2.collected_share[1], 10.0 / 40.0), "red twin: unreachable collector -> inert -> cs=10/40",
             "cs=" + std::to_string(F2.collected_share[1]));
    }
    // --- 4. two ends of one physical link steer disjoint good sets (spec 1.7 / 2.8 Atlantic) ---
    {
        // good X oriented B->C ; good Y oriented C->B. Merchant of country 5 at B steering toward
        // C, merchant of country 6 at C steering toward B.
        std::vector<std::pair<int, int>> dX{{0, 1}, {1, 2}, {1, 3}};
        std::vector<std::pair<int, int>> dY{{2, 1}, {1, 3}, {0, 1}};   // C->B->D, A->B
        std::vector<econ::NodeStandings> st(N);
        st[1].entries.push_back(econtest_standing(5, 10.0, false, 2));
        st[2].entries.push_back(econtest_standing(6, 10.0, false, 1));
        std::vector<double> injX{12, 0, 0, 0}, injY{0, 0, 12, 0};
        auto FX = econ::route(N, dX, injX, st, {}, MOD);
        auto FY = econ::route(N, dY, injY, st, {}, MOD);
        R.ok(near(FX.flow[1][2], 12.0), "X: B's merchant steers X toward C (active on X)");
        R.ok(FX.p_transfer[2] == 0.0 && FX.is_sink[2], "X: C's merchant inert for X (C is X's sink)");
        R.ok(near(FY.flow[2][1], 12.0), "Y: C's merchant steers Y toward B (active on Y)");
        R.ok(FY.flow[1].count(2) == 0 && near(FY.flow[1][3], 12.0 * 1.05), "Y: B's merchant inert for Y; Y goes on to D");
    }
    // --- 5. survival table: rows sum to 1 (no steering) and to 1+bonus share (steering) ---
    {
        std::vector<econ::NodeStandings> st(N);
        auto F = econ::route(N, dir, inject, st, {}, MOD);
        auto S = econ::survival(N, F, dir);
        double row = 0; for (int H = 0; H < N; H++) row += S[0][H];
        R.ok(near(row, 1.0), "survival row A sums to 1 without steering", "row=" + std::to_string(row));
        R.ok(near(S[0][2], 0.5) && near(S[0][3], 0.5), "A's unit halves to C and D");
        std::vector<econ::NodeStandings> st2(N);
        st2[1].entries.push_back(econtest_standing(7, 1.0, false, 2));
        auto F2 = econ::route(N, dir, inject, st2, {}, MOD);
        auto S2 = econ::survival(N, F2, dir);
        R.ok(near(S2[0][2], 1.05) && near(S2[0][3], 0.0), "steered: A's unit arrives at C with +5%",
             "S[A][C]=" + std::to_string(S2[0][2]));
        R.ok(!near(S2[0][3], 0.5), "red twin: steering changed the table");
    }
    // --- 6. aggregate + net link flows ---
    {
        std::vector<econ::NodeStandings> st(N);
        auto F = econ::route(N, dir, inject, st, {}, MOD);
        std::vector<econ::GoodFlow> pg{F, F};
        std::vector<std::vector<double>> inj{inject, inject};
        auto A = econ::aggregate(N, pg, inj);
        R.ok(near(A[0].local, 24.0) && near(A[0].total, 24.0) && near(A[0].pool, 0.0), "aggregate: local/total/pool sum over goods");
        auto net = econ::net_link_flows(dir, pg);
        R.ok(near(net[{0, 1}], 24.0) && near(net[{1, 2}], 12.0), "net link flows in Phi_w direction");
        std::vector<std::pair<int, int>> rev{{1, 0}};
        auto net2 = econ::net_link_flows(rev, pg);
        R.ok(near(net2[{1, 0}], -24.0), "red twin: opposing Phi_w direction gives a NEGATIVE net (spec 2.6)");
    }
}

} // namespace econtest
