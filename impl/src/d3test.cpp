// D3 v2 test (offline, no game): the split rule of impl/DEPARTURES.md D3 on synthetic standings.
//   split(m -> n) = sum over goods g with n in U_g(m) of (price_g / |U_g(m)|) / sum over goods with U_g(m) != {} of price_g
//   received_c(n) = sum over m of [pp_c(m) >= 2] * pp_c(m)/5 * split(m -> n)
// Checks: the split's values and its unit sum, conservation of every distributed fifth, the
// threshold, no chaining (received power never re-sends: the source is provincial power only), the
// receipt carried on the standing (Standing.received, what rec+0x40 displays), and the standing
// added for a country that had none.
#include <cstdio>
#include <cmath>
#include <vector>
#include "economy.h"

static int g_bad = 0;
static void check(bool ok, const char* what, double got, double want) {
    printf("%-58s got %.6f want %.6f %s\n", what, got, want, ok ? "OK" : "MISMATCH");
    if (!ok) g_bad++;
}
static void near(const char* what, double got, double want) { check(std::fabs(got - want) < 1e-9, what, got, want); }

int main() {
    const int N = 4;
    // good A (price 2): 0->1, 3->1, 1->2        upstream of 1 = {0, 3}
    // good B (price 1): 3->1, 1->2, 1->0        upstream of 1 = {3}, upstream of 0 = {1}
    std::vector<std::vector<std::pair<int, int>>> graphs = { {{0,1},{3,1},{1,2}}, {{3,1},{1,2},{1,0}} };
    std::vector<double> prices = {2.0, 1.0};
    auto split = econ::propagation_split(N, graphs, prices);
    // node 1: A gives 0 and 3 weight 2/2 = 1 each; B gives 3 weight 1; denominator 2 + 1 = 3
    near("split(1 -> 0) = (2/2) / 3", split[1][0], 1.0 / 3.0);
    near("split(1 -> 3) = (2/2 + 1) / 3", split[1][3], 2.0 / 3.0);
    { double s = 0; for (auto& [n, v] : split[1]) s += v; near("split(1 -> *) sums to 1", s, 1.0); }
    near("split(0 -> 1) = 1 (only B has an upstream edge at 0)", split[0][1], 1.0);
    near("split(2 -> 1) = 1", split[2][1], 1.0);
    check(split[3].empty(), "split(3 -> *) is empty (no upstream edge at 3)", (double)split[3].size(), 0.0);

    // country 7: provincial power 30 at node 0, 10 at node 1, 1 at node 2 (below the threshold), none at node 3
    std::vector<econ::NodeStandings> st(N);
    auto add = [&](int n, int c, double pp) { econ::Standing s{}; s.country = c; s.pp = pp; s.power = pp; s.own = pp; s.has_own = true; s.collects = false; s.steer_to = -1; st[n].entries.push_back(s); };
    add(0, 7, 30.0); add(1, 7, 10.0); add(2, 7, 1.0);
    auto pp_at = econ::pp_index(N, st);
    auto recv = econ::propagation_received(N, pp_at, split);
    near("received at 0 = fifth of node 1 (2) x 1/3", recv[0][7], 2.0 / 3.0);
    near("received at 3 = fifth of node 1 (2) x 2/3", recv[3][7], 4.0 / 3.0);
    near("received at 1 = fifth of node 0 (6) x 1", recv[1][7], 6.0);
    check(recv[2].count(7) == 0, "node 2 receives nothing (node 1 sends only upstream)", 0.0, 0.0);
    {   // conservation: every distributed fifth lands somewhere; node 2's pp 1 is below the threshold and sends nothing
        double tot = 0; for (int n = 0; n < N; n++) for (auto& [c, r] : recv[n]) tot += r;
        near("sum of receipts = 30/5 + 10/5", tot, 8.0);
    }
    int added = econ::apply_split_propagation(N, st, recv);
    near("power at node 1 = own 10 + received 6", st[1].entries[0].power, 16.0);
    near("Standing.received at node 1 (the rec+0x40 line)", st[1].entries[0].received, 6.0);
    near("power at node 0 = own 30 + 2/3", st[0].entries[0].power, 30.0 + 2.0 / 3.0);
    check(added == 1, "one standing added (country 7 at node 3, where it had none)", (double)added, 1.0);
    near("the added standing's power = its receipt", st[3].entries.empty() ? -1.0 : st[3].entries[0].power, 4.0 / 3.0);
    near("the added standing's receipt", st[3].entries.empty() ? -1.0 : st[3].entries[0].received, 4.0 / 3.0);
    // NO CHAINING: recompute the receipts from the post-apply standings' PROVINCIAL power -- node 3's
    // received 4/3 has pp 0 and must send nothing; node 1's receipt of 6 must not raise its fifth
    auto pp_after = econ::pp_index(N, st);
    auto recv2 = econ::propagation_received(N, pp_after, split);
    near("no chaining: receipts unchanged after apply (node 0)", recv2[0][7], recv[0][7]);
    near("no chaining: receipts unchanged after apply (node 3)", recv2[3][7], recv[3][7]);
    check(recv2[1][7] == recv[1][7] && recv2[2].count(7) == 0, "no chaining: node 1 and node 2 unchanged", recv2[1][7], recv[1][7]);

    printf(g_bad ? "D3 v2 split rule: FAIL (%d)\n" : "D3 v2 split rule: PASS\n", g_bad);
    return g_bad ? 1 : 0;
}
