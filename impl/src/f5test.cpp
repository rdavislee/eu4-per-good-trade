// F5 (TESTING.md): "A price crash spreads a market." EU4 1.37.5 has NO console verb that sets a
// trade good's price (change_price / set_price / price / add_price all answer "Unknown command" --
// measured 2026-08-27), so the claim is tested where spec 2.8's own rows were measured: offline,
// on the same install + start save the DLL's self-test uses, by crashing grain's price in the
// field inputs and re-solving that good's graph.
//
// The mechanism under test (spec 1.4): alpha(g) = (price/P0)^k, and demand weight per province is
// (wealth/wmax)^alpha. alpha > 1 concentrates demand on the richest nodes; alpha < 1 flattens the
// curve so populous-but-poorer regions carry relatively more demand. PASS = the crash lowers alpha
// below 1 AND the good's sinks de-concentrate (they move off / beyond the richest cluster).
#include <cstdio>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include "gamedata.h"
#include "save.h"
#include "field.h"
#include "drain.h"

static std::vector<std::string> sinks_of(const drain::Result& r, const gamedata::TradeNodes& tn, int N) {
    std::vector<char> has_out(N, 0);
    for (auto& e : r.directed) if (e.first >= 0 && e.first < N) has_out[e.first] = 1;
    std::vector<std::string> out;
    for (int n = 0; n < N; n++) if (!has_out[n]) out.push_back(n < (int)tn.order.size() ? tn.order[n] : "?");
    return out;
}

int main(int argc, char** argv) {
    std::string root = argc > 1 ? argv[1]
        : "C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis IV";
    std::string save = argc > 2 ? argv[2]
        : std::string(getenv("USERPROFILE") ? getenv("USERPROFILE") : "") +
          "\\OneDrive\\Documents\\Paradox Interactive\\Europa Universalis IV\\save games\\VANILLA_start.eu4";
    const std::string GOOD = "grain";
    const double CRASH = 0.625;          // the spec's reachable floor for grain

    gamedata::TradeNodes tn = gamedata::load_tradenodes(root + "/common/tradenodes/00_tradenodes.txt");
    gamedata::StaticMods sm = gamedata::load_static_mods(root);
    auto base_prices = gamedata::load_prices(root);
    save::SaveData sd = save::load(save);

    drain::Graph g;
    int bad = 0;
    std::vector<std::string> before, after;
    double a_before = 0, a_after = 0, p_before = 0;

    for (int pass = 0; pass < 2; pass++) {
        save::SaveData s2 = sd;
        if (pass == 1) s2.current_prices[GOOD] = CRASH;
        field::Field f = field::build(tn, sm, s2, base_prices);
        g.N = f.N; g.und = tn.und; g.edges_und = tn.edges_und;
        int gi = -1;
        for (int i = 0; i < (int)f.goods.size(); i++) if (f.goods[i] == GOOD) { gi = i; break; }
        if (gi < 0) { printf("FAIL: good '%s' not in the field\n", GOOD.c_str()); return 1; }
        std::vector<double> b(f.N), S = f.S[gi], C = f.C[gi];
        for (int n = 0; n < f.N; n++) b[n] = S[n] - C[n];
        drain::Result r = drain::run(g, b, f.tie_cost_edge, f.node_wealth, S, C);
        auto sk = sinks_of(r, tn, f.N);
        if (pass == 0) { before = sk; a_before = f.alpha[gi]; p_before = field::price_of(GOOD, s2.current_prices, base_prices); }
        else           { after  = sk; a_after  = f.alpha[gi]; }
        printf("%-8s price=%.3f alpha=%.4f sinks=%d :", pass ? "CRASH" : "BASE",
               pass ? CRASH : p_before, pass ? a_after : a_before, (int)sk.size());
        for (auto& s3 : sk) printf(" %s", s3.c_str());
        printf("\n");
    }

    std::set<std::string> B(before.begin(), before.end()), A(after.begin(), after.end());
    std::vector<std::string> gained, lost;
    for (auto& x : A) if (!B.count(x)) gained.push_back(x);
    for (auto& x : B) if (!A.count(x)) lost.push_back(x);
    printf("\nalpha %.4f -> %.4f  (must fall below 1)\n", a_before, a_after);
    printf("sinks %d -> %d;  gained:", (int)before.size(), (int)after.size());
    for (auto& x : gained) printf(" %s", x.c_str());
    printf("   lost:");
    for (auto& x : lost) printf(" %s", x.c_str());
    printf("\n");

    if (!(a_after < 1.0 && a_after < a_before)) { printf("FAIL: alpha did not drop below 1\n"); bad++; }
    if (gained.empty() && lost.empty()) { printf("FAIL: the sink set did not move at all\n"); bad++; }
    printf(bad ? "\nF5 FAIL (%d)\n" : "\nF5 PASS: the crash lowers alpha below 1 and moves the market's ends\n", bad);
    return bad ? 1 : 0;
}
