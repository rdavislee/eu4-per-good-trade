// OFFLINE TEST OF THE AI MERCHANT CHOOSER (spec 3.14; the user's frontier model).
//
// No game. The scorer is pure C++ over the routing's flows and the per-node standings, so it
// is driven here from the vanilla 1444 save exactly as the DLL drives it in-process:
//   - field::build gives per-good supply by node; inject[g][n] is the annual trade_value of
//     the counted provinces of good g in node n, the same figure the DLL feeds econ::route
//   - standings come from the save's own per-node country sub-blocks (val, has_capital),
//     extracted to standings1444.json; power = val, the engine's own per-country figure
//   - every good is routed with econ::route on its solved orientation, then frontier::plan
//     chooses k merchants for a country
// Output: for each named country, the chosen edges with the three factors separated -- flow,
// the product of path shares, and the share at home -- so a wrong number is visible as a wrong
// FACTOR, not just a wrong total.
//
//   aitest <eu4_root> <save> <standings.json> TAG[,k] [TAG[,k] ...]
#include <cstdio>
#include <fstream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>
#include "gamedata.h"
#include "save.h"
#include "field.h"
#include "drain.h"
#include "economy.h"
#include "frontier.h"

using namespace std;

// minimal JSON reader for the standings file: [{"name":..,"countries":{"TAG":{"val":..,"has_capital":true,..},..}},..]
struct CS { double val = 0; bool has_capital = false; };
static map<string, map<string, CS>> read_standings(const string& path) {
    ifstream f(path); stringstream ss; ss << f.rdbuf(); string s = ss.str();
    map<string, map<string, CS>> out;
    size_t p = 0;
    while ((p = s.find("\"name\": \"", p)) != string::npos || (p = s.find("\"name\":\"", p)) != string::npos) {
        p = s.find('"', p + 7); size_t q = s.find('"', p + 1);
        string node = s.substr(p + 1, q - p - 1);
        size_t cend = s.find("\"name\"", q);
        if (cend == string::npos) cend = s.size();
        size_t c = q;
        while (true) {
            size_t t = s.find("\"val\"", c);
            if (t == string::npos || t > cend) break;
            // tag is the last quoted key before this "val" that is 3 uppercase letters
            size_t k = s.rfind("\": {", t); size_t k0 = s.rfind('"', k - 1);
            string tag = s.substr(k0 + 1, k - k0 - 1);
            size_t v = s.find(':', t) + 1; double val = atof(s.c_str() + v);
            size_t hc = s.find("\"has_capital\"", t); bool cap = hc != string::npos && hc < s.find('}', t) && s.compare(s.find(':', hc) + 1, 5, " true") == 0;
            if (!cap && hc != string::npos && hc < s.find('}', t)) cap = s.compare(s.find(':', hc) + 1, 4, "true") == 0;
            out[node][tag] = CS{val, cap};
            c = s.find('}', t) + 1;
        }
        p = q;
    }
    return out;
}

int main(int argc, char** argv) {
    if (argc < 5) { fprintf(stderr, "usage: aitest <eu4_root> <save> <standings.json> TAG[,k] ...\n"); return 2; }
    string root = argv[1], savep = argv[2], stp = argv[3];
    auto tn = gamedata::load_tradenodes(root + "/common/tradenodes/00_tradenodes.txt");
    auto sm = gamedata::load_static_mods(root);
    auto base_prices = gamedata::load_prices(root);
    auto sd = save::load(savep);
    field::Field f = field::build(tn, sm, sd, base_prices);
    int N = f.N;
    auto standings_raw = read_standings(stp);

    // node name -> index, from the field's node order
    map<string, int> nidx;
    for (int n = 0; n < N; n++) nidx[tn.order[n]] = n;
    // undirected adjacency: the field's own, in declaration order
    const vector<vector<int>>& adj = tn.und;
    // tag -> a stable integer id
    map<string, int> tagid; int next_id = 1;
    auto id_of = [&](const string& t) { auto it = tagid.find(t); if (it != tagid.end()) return it->second; tagid[t] = next_id; return next_id++; };
    // standings per node: power = val (the engine's own per-country figure), collects = has_capital
    vector<econ::NodeStandings> st(N);
    map<int, vector<int>> collect_nodes;
    map<int, int> home_of;
    for (auto& [node, cm] : standings_raw) {
        auto it = nidx.find(node); if (it == nidx.end()) continue;
        for (auto& [tag, cs] : cm) {
            if (cs.val <= 0 && !cs.has_capital) continue;
            econ::Standing s{}; s.country = id_of(tag); s.power = cs.val; s.collects = cs.has_capital; s.steer_to = -1; s.is_capital = cs.has_capital;
            st[it->second].entries.push_back(s);
            if (cs.has_capital) { collect_nodes[s.country].push_back(it->second); home_of[s.country] = it->second; }
        }
    }
    // inject[g][n]: annual trade_value of counted provinces of good g in node n
    vector<vector<double>> inject(f.goods.size(), vector<double>(N, 0.0));
    for (auto& r : f.rows) { auto g = f.gidx.find(r.good); if (g != f.gidx.end() && r.node >= 0 && r.node < N) inject[g->second][r.node] += r.trade_value; }
    // route every live good on its solved orientation
    drain::Graph g; g.N = f.N; g.und = tn.und; g.edges_und = tn.edges_und;   // as main.cpp builds it
    vector<econ::GoodFlow> per_good;
    for (int gi = 0; gi < (int)f.goods.size(); gi++) {
        if (!f.live[gi]) continue;
        vector<double> b(N); for (int n = 0; n < N; n++) b[n] = f.S[gi][n] - f.C[gi][n];
        drain::Result r = drain::run(g, b, f.tie_cost_edge, f.node_wealth, f.S[gi], f.C[gi]);
        per_good.push_back(econ::route(N, r.directed, inject[gi], st, collect_nodes, 0.05));
    }
    frontier::FlowMatrix FM = frontier::flow_matrix(N, per_good);
    printf("routed %zu goods over %d nodes; %zu countries with a trade capital\n\n", per_good.size(), N, home_of.size());

    for (int a = 4; a < argc; a++) {
        string arg = argv[a]; int k = 3; size_t comma = arg.find(',');
        string tag = comma == string::npos ? arg : arg.substr(0, comma);
        if (comma != string::npos) k = atoi(arg.c_str() + comma + 1);
        auto tid = tagid.find(tag);
        if (tid == tagid.end() || !home_of.count(tid->second)) { printf("%s: no trade capital found\n\n", tag.c_str()); continue; }
        int c = tid->second, home = home_of[c];
        printf("== %s  home=%s  share_at_home=%.3f  k=%d ==\n", tag.c_str(), tn.order[home].c_str(), frontier::share_at(st, home, c), k);
        // show the first frontier fully, then the plan
        set<int> net{home};
        auto first = frontier::candidates(N, home, net, adj, st, FM, c);
        printf("  frontier from home (%zu edges), top 6:\n", first.size());
        for (size_t i = 0; i < first.size() && i < 6; i++) {
            auto& p = first[i];
            double fl = frontier::flow_toward(per_good, p.node, p.target);
            double so = frontier::share_at(st, p.node, c, frontier::MERCHANT_PRESENT_POWER);
            printf("    %-18s -> %-18s flow=%8.3f  share@stand=%.3f  x path=%.3f  = %8.4f\n", tn.order[p.node].c_str(), tn.order[p.target].c_str(), fl, so, p.added / (fl * so > 0 ? fl * so : 1), p.added);
        }
        auto plan = frontier::plan(N, home, k, adj, st, FM, c);
        printf("  plan(%d):\n", k);
        for (auto& p : plan) printf("    stand at %-18s steer -> %-18s added=%8.4f\n", tn.order[p.node].c_str(), tn.order[p.target].c_str(), p.added);
        printf("\n");
    }
    return 0;
}
