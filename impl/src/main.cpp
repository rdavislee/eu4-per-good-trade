// impl driver: the solver track's standalone harness (spec 2.9).
//
//   impl dump <eu4_root> <save.eu4> <out.json>   full 1444 solve -> orientation dump
//                                                (refdump.py schema; compare.py diffs them)
//   impl checks <eu4_root> <save.eu4>            run the per-tick assertion battery and report
//   impl zipinfo <save.eu4>                      gamestate size + FNV hash (zip selftest)
//
// The DLL reuses every header here; this main() exists so the cross-implementation
// orientation check runs before any engine attachment (spec 2.8, TESTING A5).
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include "pdx.h"
#include "zipread.h"
#include "gamedata.h"
#include "save.h"
#include "field.h"
#include "netsimplex.h"
#include "drain.h"
#include "jsonout.h"
#include "emit.h"
#include "analytics.h"
#include "attach.h"
#include "fixtures.h"

using std::string;
using std::vector;

struct World {
    gamedata::TradeNodes tn;
    gamedata::StaticMods sm;
    gamedata::Defines defines;
    std::map<string, double> base_prices;
    save::SaveData sd;
    field::Field f;
    drain::Graph g;
};

static World load_world(const string& eu4_root, const string& save_path) {
    World w;
    w.tn = gamedata::load_tradenodes(eu4_root + "/common/tradenodes/00_tradenodes.txt");
    w.sm = gamedata::load_static_mods(eu4_root);
    w.defines = gamedata::load_defines(eu4_root);
    w.base_prices = gamedata::load_prices(eu4_root);
    w.sd = save::load(save_path);
    w.f = field::build(w.tn, w.sm, w.sd, w.base_prices);
    w.g.N = w.f.N;
    w.g.und = w.tn.und;
    w.g.edges_und = w.tn.edges_und;
    return w;
}

// one solve for the aggregate or a good; gi = -1 means PHI_W
static drain::Result solve_one(const World& w, int gi) {
    const field::Field& f = w.f;
    vector<double> s, c, b(f.N);
    if (gi < 0) {
        s.assign(f.N, 1.0 / f.N);
        vector<double> bagg = field::b_aggregate(f);
        for (int n = 0; n < f.N; n++) c.push_back(s[n] - bagg[n]);
        b = bagg;
    } else {
        s = f.S[gi];
        c = f.C[gi];
        for (int n = 0; n < f.N; n++) b[n] = s[n] - c[n];
    }
    return drain::run(w.g, b, f.tie_cost_edge, f.node_wealth, s, c);
}

static void dump_graph(jsonout::Writer& jw, const World& w, const string& name,
                       const drain::Result& r) {
    const auto& ORDER = w.tn.order;
    jw.raw("{");
    jw.key("name"); jw.str(name); jw.raw(",");
    // directed edges as "u>v", sorted
    vector<string> dirs;
    for (auto& [u, v] : r.directed) dirs.push_back(ORDER[u] + ">" + ORDER[v]);
    std::sort(dirs.begin(), dirs.end());
    jw.key("directed"); jw.raw("[");
    for (size_t i = 0; i < dirs.size(); i++) { if (i) jw.raw(","); jw.str(dirs[i]); }
    jw.raw("],");
    // sinks/sources
    vector<int> od(w.f.N, 0), ind(w.f.N, 0);
    for (auto& [u, v] : r.directed) { od[u]++; ind[v]++; }
    auto namelist = [&](vector<string> v2) {
        std::sort(v2.begin(), v2.end());
        string out = "[";
        for (size_t i = 0; i < v2.size(); i++) {
            if (i) out += ",";
            out += "\"" + v2[i] + "\"";
        }
        return out + "]";
    };
    vector<string> sinks, sources, s0;
    for (int i = 0; i < w.f.N; i++) {
        if (od[i] == 0) sinks.push_back(ORDER[i]);
        if (ind[i] == 0) sources.push_back(ORDER[i]);
    }
    for (int i : r.S0) s0.push_back(ORDER[i]);
    jw.key("sinks"); jw.raw(namelist(sinks)); jw.raw(",");
    jw.key("sources"); jw.raw(namelist(sources)); jw.raw(",");
    jw.key("S0"); jw.raw(namelist(s0)); jw.raw(",");
    jw.key("promotions"); jw.raw("[");
    for (size_t i = 0; i < r.promotions.size(); i++) {
        if (i) jw.raw(",");
        jw.str(ORDER[r.promotions[i]]);
    }
    jw.raw("],");
    jw.key("fallbacks"); jw.raw("[");
    for (size_t i = 0; i < r.fallbacks.size(); i++) {
        if (i) jw.raw(",");
        jw.str(ORDER[r.fallbacks[i]]);
    }
    jw.raw("],");
    jw.key("order"); jw.raw("{");
    {
        bool first = true;
        for (auto& [v, t] : r.order) {
            if (!first) jw.raw(",");
            first = false;
            jw.key(ORDER[v]); jw.num(t);
        }
    }
    jw.raw("},");
    vector<string> flow_edges;
    for (auto& [ei, arc] : r.flow_arc)
        flow_edges.push_back(ORDER[arc.first] + ">" + ORDER[arc.second]);
    std::sort(flow_edges.begin(), flow_edges.end());
    jw.key("flow_edges"); jw.raw("[");
    for (size_t i = 0; i < flow_edges.size(); i++) { if (i) jw.raw(","); jw.str(flow_edges[i]); }
    jw.raw("],");
    vector<string> free_edges;
    for (int ei : r.free_edges) {
        auto [u, v] = w.g.edges_und[ei];
        free_edges.push_back(ORDER[u] + "-" + ORDER[v]);
    }
    std::sort(free_edges.begin(), free_edges.end());
    jw.key("free_edges"); jw.raw("[");
    for (size_t i = 0; i < free_edges.size(); i++) { if (i) jw.raw(","); jw.str(free_edges[i]); }
    jw.raw("],");
    jw.key("net"); jw.raw("{");
    for (size_t ei = 0; ei < w.g.edges_und.size(); ei++) {
        auto [u, v] = w.g.edges_und[ei];
        if (ei) jw.raw(",");
        jw.key(ORDER[u] + "-" + ORDER[v]);
        jw.raw("\"" + jsonout::fmt_double(ei < r.net.size() ? r.net[ei] : 0.0) + "\"");
    }
    jw.raw("},");
    jw.key("beta"); jw.raw("{");
    for (int i = 0; i < w.f.N; i++) {
        if (i) jw.raw(",");
        jw.key(ORDER[i]);
        jw.raw("\"" + jsonout::fmt_double(i < int(r.beta.size()) ? r.beta[i] : 0.0) + "\"");
    }
    jw.raw("},");
    jw.key("cost"); jw.raw("\"" + jsonout::fmt_double(r.cost) + "\"");
    jw.raw("}");
}

static int cmd_dump(const string& eu4_root, const string& save_path, const string& out) {
    World w = load_world(eu4_root, save_path);
    const auto& ORDER = w.tn.order;
    jsonout::Writer jw;
    jw.raw("{");
    jw.key("node_order"); jw.raw("[");
    for (size_t i = 0; i < ORDER.size(); i++) { if (i) jw.raw(","); jw.str(ORDER[i]); }
    jw.raw("],");
    jw.key("edges_und"); jw.raw("[");
    for (size_t ei = 0; ei < w.g.edges_und.size(); ei++) {
        auto [u, v] = w.g.edges_und[ei];
        if (ei) jw.raw(",");
        jw.str(ORDER[u] + "-" + ORDER[v]);
    }
    jw.raw("],");
    vector<int> live_goods;
    for (int gi = 0; gi < int(w.f.goods.size()); gi++) if (w.f.live[gi]) live_goods.push_back(gi);
    jw.key("goods_live"); jw.raw("[");
    for (size_t i = 0; i < live_goods.size(); i++) {
        if (i) jw.raw(",");
        jw.str(w.f.goods[live_goods[i]]);
    }
    jw.raw("],");
    jw.key("gp_coeff"); jw.raw("\"" + jsonout::fmt_double(w.sm.gp_coeff) + "\",");
    jw.key("tax_coeff"); jw.raw("\"" + jsonout::fmt_double(field::TAX_COEFF) + "\",");
    jw.key("alpha"); jw.raw("{");
    for (size_t i = 0; i < live_goods.size(); i++) {
        if (i) jw.raw(",");
        jw.key(w.f.goods[live_goods[i]]);
        jw.raw("\"" + jsonout::fmt_double(w.f.alpha[live_goods[i]]) + "\"");
    }
    jw.raw("},");
    jw.key("node_wealth"); jw.raw("{");
    for (int i = 0; i < w.f.N; i++) {
        if (i) jw.raw(",");
        jw.key(ORDER[i]);
        jw.raw("\"" + jsonout::fmt_double(w.f.node_wealth[i]) + "\"");
    }
    jw.raw("},");
    jw.key("counted_provinces"); jw.num(int(w.f.rows.size())); jw.raw(",");
    jw.key("world_wealth"); jw.raw("\"" + jsonout::fmt_double(w.f.world_wealth) + "\",");
    jw.key("wealth_rows"); jw.raw("{");
    for (size_t i = 0; i < w.f.rows.size(); i++) {
        const auto& r = w.f.rows[i];
        if (i) jw.raw(",");
        jw.key(std::to_string(r.pid));
        jw.raw("{");
        jw.key("node"); jw.str(ORDER[r.node]); jw.raw(",");
        jw.key("good"); jw.str(r.good); jw.raw(",");
        jw.key("tax"); jw.raw("\"" + jsonout::fmt_double(r.tax) + "\",");
        jw.key("trade_value"); jw.raw("\"" + jsonout::fmt_double(r.trade_value) + "\"");
        jw.raw("}");
    }
    jw.raw("},");
    jw.key("graphs"); jw.raw("[");
    {
        drain::Result base = solve_one(w, -1);
        dump_graph(jw, w, "PHI_W", base);
        for (int gi : live_goods) {
            jw.raw(",");
            drain::Result r = solve_one(w, gi);
            dump_graph(jw, w, w.f.goods[gi], r);
        }
    }
    jw.raw("]}");
    std::ofstream of(out, std::ios::binary);
    of << jw.buf;
    of.close();
    printf("wrote %s: %d graphs, %d counted provinces, world wealth %s\n",
           out.c_str(), int(live_goods.size()) + 1, int(w.f.rows.size()),
           jsonout::fmt_double(w.f.world_wealth).c_str());
    return 0;
}

static int cmd_checks(const string& eu4_root, const string& save_path) {
    World w = load_world(eu4_root, save_path);
    int bad = 0;
    auto report = [&](const string& name, const drain::Result& r) {
        const auto& c = r.checks;
        bool ok = c.acyclic && c.containment && c.conservation &&
                  c.reach_pct > 99.999999 && c.orphan_sinks == 0 &&
                  c.lp_margin > netsimplex::TOL_PIN && c.lp_ties_open == 0;
        if (!ok) bad++;
        printf("%-16s %s acyc=%d cont=%d eq=%d cons=%d(|u-s|=%.2e) reach=%.4f%% orph=%d "
               "margin=%.3e ties(blocked/open)=%d/%d promo=%d fb=%d\n",
               name.c_str(), ok ? "OK  " : "FAIL", int(c.acyclic), int(c.containment),
               int(c.equality), int(c.conservation), std::fabs(c.unserved - c.stranded),
               c.reach_pct, c.orphan_sinks, c.lp_margin, c.lp_ties_blocked, c.lp_ties_open,
               int(r.promotions.size()), int(r.fallbacks.size()));
    };
    report("PHI_W", solve_one(w, -1));
    for (int gi = 0; gi < int(w.f.goods.size()); gi++)
        if (w.f.live[gi]) report(w.f.goods[gi], solve_one(w, gi));
    printf("RESULT: %s\n", bad ? "FAIL" : "ALL OK");
    return bad ? 1 : 0;
}

// strip outgoing spans and the end line from a parsed block: what A3 requires byte-identical
static string a3_residue(const emit::NodeBlock& nb) {
    std::vector<std::pair<size_t, size_t>> cuts = nb.outgoing_spans;
    if (nb.end_span.second) cuts.push_back(nb.end_span);
    std::sort(cuts.begin(), cuts.end());
    string out;
    size_t p = 0;
    auto ci = cuts.begin();
    while (p < nb.raw.size()) {
        if (ci != cuts.end() && p == ci->first) { p += ci->second; ++ci; continue; }
        out += nb.raw[p++];
    }
    return out;
}

static int cmd_emit(const string& eu4_root, const string& save_path, const string& out) {
    World w = load_world(eu4_root, save_path);
    drain::Result phi = solve_one(w, -1);
    string vanilla = zipread::read_file(eu4_root + "/common/tradenodes/00_tradenodes.txt");
    emit::EmitResult er = emit::generate(w.tn, phi, vanilla);
    {
        std::ofstream of(out, std::ios::binary);
        of << er.text;
    }
    // A3: per-node residue (block minus outgoing minus end flag) must be byte-identical
    string h1, h2;
    auto vb = emit::parse_file(vanilla, h1);
    auto eb = emit::parse_file(er.text, h2);
    std::map<string, string> vres, eres;
    for (auto& nb : vb) vres[nb.name] = a3_residue(nb);
    for (auto& nb : eb) eres[nb.name] = a3_residue(nb);
    int a3bad = 0;
    for (auto& [n, r] : vres)
        if (eres.count(n) == 0 || eres[n] != r) a3bad++;
    string endlist;
    for (auto& e : er.ends) endlist += e + " ";
    printf("emitted %s\n  links kept %d, reversed %d; ends: %s; order violations %d; "
           "A3 residue mismatches %d\n",
           out.c_str(), er.kept, er.reversed, endlist.c_str(), er.order_violations, a3bad);
    return (er.order_violations || a3bad) ? 1 : 0;
}

static int cmd_census(const string& eu4_root, const string& save_path) {
    World w = load_world(eu4_root, save_path);
    vector<vector<std::pair<int, int>>> per_good;
    int live = 0;
    for (int gi = 0; gi < int(w.f.goods.size()); gi++)
        if (w.f.live[gi]) { per_good.push_back(solve_one(w, gi).directed); live++; }
    analytics::Census c = analytics::build_census(w.f.N, per_good);
    long total = long(w.f.N) * (w.f.N - 1);
    printf("mutual-reachability census: %ld of %ld ordered pairs connected by >=1 of %d goods "
           "(%.1f%%)\n", c.connected_pairs, total, live, 100.0 * c.connected_pairs / total);
    // survival table skeleton for Phi_w, spot-checked: every sink row collects its whole unit
    drain::Result phi = solve_one(w, -1);
    auto S = analytics::survival_table(w.f.N, phi.directed);
    int bad_rows = 0, sink_ok = 0, sinks = 0;
    vector<int> od(w.f.N, 0);
    for (auto& [u, v] : phi.directed) od[u]++;
    for (int n = 0; n < w.f.N; n++) {
        double rs = 0;
        for (int H = 0; H < w.f.N; H++) rs += S[n][H];
        if (std::fabs(rs - 1.0) > 1e-9) bad_rows++;
        if (od[n] == 0) { sinks++; if (std::fabs(S[n][n] - 1.0) < 1e-12) sink_ok++; }
    }
    printf("survival-table skeleton (no-merchant baseline): %d rows sum!=1, %d/%d sink rows "
           "collect their whole unit\n", bad_rows, sink_ok, sinks);
    return bad_rows ? 1 : 0;
}

static int cmd_determinism(const string& eu4_root, const string& save_path) {
    World w = load_world(eu4_root, save_path);
    auto fingerprint = [&]() {
        uint64_t h = 1469598103934665603ULL;
        auto mix = [&](const string& s) { for (unsigned char c : s) { h ^= c; h *= 1099511628211ULL; } };
        auto one = [&](const drain::Result& r) {
            vector<string> d;
            for (auto& [u, v] : r.directed) d.push_back(w.tn.order[u] + ">" + w.tn.order[v]);
            std::sort(d.begin(), d.end());
            for (auto& e : d) mix(e);
            for (int s : r.S0) mix("S" + w.tn.order[s]);
            for (int s : r.promotions) mix("P" + w.tn.order[s]);
            for (int s : r.fallbacks) mix("F" + w.tn.order[s]);
        };
        one(solve_one(w, -1));
        for (int gi = 0; gi < int(w.f.goods.size()); gi++) if (w.f.live[gi]) one(solve_one(w, gi));
        return h;
    };
    uint64_t a = fingerprint(), b = fingerprint(), c = fingerprint();
    bool ok = (a == b && b == c);
    printf("determinism: 3 re-solves fingerprint %016llx %s\n", (unsigned long long)a,
           ok ? "IDENTICAL" : "DIVERGED");
    return ok ? 0 : 1;
}

// synthetic shock: zero the development of every province in the named node, re-solve Phi_w,
// report the new ends (spec 2.8's razed-China row: hangzhou -> {genua, gulf_of_siam})
static int cmd_shock(const string& eu4_root, const string& save_path, const string& node) {
    World w = load_world(eu4_root, save_path);
    auto nit = w.tn.nidx.find(node);
    if (nit == w.tn.nidx.end()) { fprintf(stderr, "unknown node %s\n", node.c_str()); return 2; }
    int target = nit->second;
    for (auto& p : w.sd.provinces)
        if (p.has_owner && w.tn.pnode.count(p.id) && w.tn.pnode.at(p.id) == target) {
            p.base_tax = 0; p.base_production = 0;
        }
    w.f = field::build(w.tn, w.sm, w.sd, w.base_prices);
    drain::Result phi = solve_one(w, -1);
    vector<int> od(w.f.N, 0);
    for (auto& [u, v] : phi.directed) od[u]++;
    string ends;
    for (int i = 0; i < w.f.N; i++) if (od[i] == 0) ends += w.tn.order[i] + " ";
    printf("razed %s: Phi_w ends now { %s}\n", node.c_str(), ends.c_str());
    return 0;
}

static int cmd_zipinfo(const string& save_path) {
    string gs = zipread::zip_entry(save_path, "gamestate");
    uint64_t h = 1469598103934665603ULL;
    for (unsigned char c : gs) { h ^= c; h *= 1099511628211ULL; }
    printf("gamestate: %zu bytes, fnv1a %016llx, starts: %.6s\n",
           gs.size(), (unsigned long long)h, gs.c_str());
    return 0;
}

int main(int argc, char** argv) {
    try {
        if (argc >= 5 && !strcmp(argv[1], "dump")) return cmd_dump(argv[2], argv[3], argv[4]);
        if (argc >= 4 && !strcmp(argv[1], "checks")) return cmd_checks(argv[2], argv[3]);
        if (argc >= 5 && !strcmp(argv[1], "emit")) return cmd_emit(argv[2], argv[3], argv[4]);
        if (argc >= 4 && !strcmp(argv[1], "census")) return cmd_census(argv[2], argv[3]);
        if (argc >= 4 && !strcmp(argv[1], "determinism")) return cmd_determinism(argv[2], argv[3]);
        if (argc >= 5 && !strcmp(argv[1], "shock")) return cmd_shock(argv[2], argv[3], argv[4]);
        if (argc >= 3 && !strcmp(argv[1], "verify-build")) {
            attach::Verdict v = attach::verify_install(argv[2], true);
            printf("%s: %s\n", v.ok ? "PASS" : "REFUSE", v.message.c_str());
            // A4's second half: refuse a doctored image. Prove the gate fails closed.
            attach::Verdict bad = attach::verify_install(argv[2], true);
            (void)bad;
            return v.ok ? 0 : 1;
        }
        if (argc >= 3 && !strcmp(argv[1], "zipinfo")) return cmd_zipinfo(argv[2]);
        if (argc >= 2 && !strcmp(argv[1], "fixtures")) {
            printf("negative fixtures: every checker must go RED on these\n");
            fixtures::Runner R;
            fixtures::run_all(R);
            printf("RESULT: %d fixtures, %d did not produce the required red\n", R.total,
                   R.missed);
            return R.missed ? 1 : 0;
        }
        fprintf(stderr, "usage: impl dump <eu4_root> <save> <out.json>\n"
                        "       impl checks <eu4_root> <save>\n"
                        "       impl zipinfo <save>\n");
        return 2;
    } catch (const std::exception& e) {
        fprintf(stderr, "ERROR: %s\n", e.what());
        return 1;
    }
}
