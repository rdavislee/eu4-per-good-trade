// D3 identity test (offline, no game): when every good's graph is Phi_w, the per-good power must
// equal the aggregate standing power for every (node, country). Uses synthetic standings.
#include <cstdio>
#include <cmath>
#include <vector>
#include <map>
#include "economy.h"
int main() {
    int N = 4;
    // Phi_w: 0->1, 1->2, 3->1  (1 has two upstream nodes 0 and 3)
    std::vector<std::pair<int,int>> phi = {{0,1},{1,2},{3,1}};
    std::vector<econ::NodeStandings> st(N);
    auto add = [&](int n, int c, double pp, double extra) { econ::Standing s{}; s.country = c; s.pp = pp; s.power = pp + extra; s.collects = false; s.steer_to = -1; st[n].entries.push_back(s); };
    // country 7: provincial 10 at node 1 (>=2), 1 at node 2 (<2), 30 at node 0
    add(0, 7, 30.0, 10.0/5.0);            // node 0 receives a fifth of node 1's 10 (its downstream)
    add(1, 7, 10.0, 0.0);                 // node 1 receives from node 2: pp 1 < 2 -> nothing
    add(2, 7, 1.0, 0.0);
    add(3, 7, 0.0, 10.0/5.0);             // node 3 is also upstream of node 1: full fifth (FULL rule)
    // downstream lists along Phi_w (link_targets)
    std::vector<std::vector<int>> down(N); for (auto& [u,v] : phi) down[u].push_back(v);
    auto pp_at = econ::pp_index(N, st);
    for (int n = 0; n < N; n++) for (auto& e : st[n].entries) { double v = e.power - econ::prop_from(pp_at, down[n], e.country); e.own = v > 0 ? v : 0; }
    auto P = econ::per_good_power(N, phi, st, pp_at);
    int bad = 0;
    for (int n = 0; n < N; n++) for (size_t i = 0; i < st[n].entries.size(); i++) {
        double d = std::fabs(P[n][i] - st[n].entries[i].power);
        printf("node %d country %d: aggregate=%.4f own=%.4f per-good(Phi_w)=%.4f %s\n", n, st[n].entries[i].country, st[n].entries[i].power, st[n].entries[i].own, P[n][i], d < 1e-9 ? "OK" : "MISMATCH");
        if (d >= 1e-9) bad++;
    }
    // a different graph for good g: 1->0 (reversed), 1->2, 3->1: node 0 now DOWNSTREAM of 1
    std::vector<std::pair<int,int>> g = {{1,0},{1,2},{3,1}};
    auto Pg = econ::per_good_power(N, g, st, pp_at);
    printf("good g (1->0): node 0 country 7 power=%.4f (own %.4f, no fifth from 1 any more), node 1 = %.4f (own %.4f + fifth of node 0's 30 = 6)\n", Pg[0][0], st[0].entries[0].own, Pg[1][0], st[1].entries[0].own);
    if (std::fabs(Pg[0][0] - st[0].entries[0].own) > 1e-9 || std::fabs(Pg[1][0] - (st[1].entries[0].own + 6.0)) > 1e-9) bad++;
    printf(bad ? "D3 identity: FAIL (%d)\n" : "D3 identity: PASS\n", bad);
    return bad ? 1 : 0;
}
