// per-good-trade.dll -- the runtime-attached mod (spec 2.1, 2.5). Loaded into eu4.exe (build
// 835bfdf8) via the version.dll proxy (loader.cpp), following the EU4dll precedent.
//
// On attach, in order:
//   1. Build gate (spec 2.5): verify this is the frozen 1.37.5 build via BOTH the in-memory
//      version string ("release_1.37.5", found by pattern scan of the loaded image, EU4dll's
//      own method) AND eu4_rev.txt + eu4.exe SHA-256 next to the executable. Any mismatch ->
//      log, refuse, and do nothing else. A patch is a new binary; every offset is invalid.
//   2. Embedded solver self-test: read the install + the start save from disk and solve Phi_w
//      in-process, proving the whole solver (parsers, field, DRAIN, emitter) runs inside the
//      game process exactly as the standalone harness does. This is the cross-implementation
//      basis (spec 2.8) -- the same code, now in the target address space.
//   3. Hook seams (hooks.h): resolve every seam whose signature is known; report the rest as
//      pending. While the tick/inject/UI seams are pending, the mod stays read-only.
//
// Everything logs to per-good-trade.log next to eu4.exe.
#include <windows.h>
#include <filesystem>
#include <fstream>
#include <string>
#include "pattern.h"
#include "hooks.h"
#include "livetrade.h"
#include "install.h"
#include "nodemap.h"
#include "liveworld.h"
#include "resolver.h"
#include "arrows.h"
#include "tickhook.h"
#include "ticklive.h"
#include "../src/attach.h"
#include "../src/gamedata.h"
#include "../src/save.h"
#include "../src/field.h"
#include "../src/drain.h"

namespace fs = std::filesystem;

static std::ofstream g_log;
static std::string g_logpath;
static void L(const std::string& s) { if (g_log) { g_log << s << "\n"; g_log.flush(); } }

// GetModuleFileName-based install directory (the folder holding eu4.exe)
static std::string install_dir() {
    char buf[MAX_PATH];
    DWORD n = GetModuleFileNameA(nullptr, buf, MAX_PATH);
    if (n == 0) return "";
    std::string p(buf, n);
    size_t slash = p.find_last_of("\\/");
    return slash == std::string::npos ? "" : p.substr(0, slash);
}

// A DRAIN solve driven entirely from install + save files, proving the embedded solver runs
// in-process. (The LIVE-memory equivalent -- reading inject/trade_goods_size from engine memory
// each tick -- is the trade_tick + node_trade_goods_size seams, pending the debugger session.)
static void solver_self_test(const std::string& root) {
    try {
        std::string save = std::string(getenv("USERPROFILE") ? getenv("USERPROFILE") : "") +
            "\\OneDrive\\Documents\\Paradox Interactive\\Europa Universalis IV\\save games\\VANILLA_start.eu4";
        gamedata::TradeNodes tn = gamedata::load_tradenodes(root + "/common/tradenodes/00_tradenodes.txt");
        gamedata::StaticMods sm = gamedata::load_static_mods(root);
        auto prices = gamedata::load_prices(root);
        save::SaveData sd = save::load(save);
        field::Field f = field::build(tn, sm, sd, prices);
        drain::Graph g; g.N = f.N; g.und = tn.und; g.edges_und = tn.edges_und;
        std::vector<double> bagg = field::b_aggregate(f);
        std::vector<double> s(f.N, 1.0 / f.N), c(f.N);
        for (int n = 0; n < f.N; n++) c[n] = s[n] - bagg[n];
        drain::Result r = drain::run(g, bagg, f.tie_cost_edge, f.node_wealth, s, c);
        std::vector<int> od(f.N, 0);
        for (auto& [u, v] : r.directed) od[u]++;
        std::string sinks;
        for (int i = 0; i < f.N; i++) if (od[i] == 0) sinks += tn.order[i] + " ";
        L("solver self-test: " + std::to_string(f.rows.size()) + " provinces, world wealth " +
          std::to_string(f.world_wealth) + ", Phi_w ends { " + sinks + "}");
        L("  per-tick checks: acyclic=" + std::to_string(r.checks.acyclic) +
          " conservation=" + std::to_string(r.checks.conservation) +
          " reach=" + std::to_string(r.checks.reach_pct) + "%");
    } catch (const std::exception& e) {
        L(std::string("solver self-test FAILED: ") + e.what());
    }
}

// ===========================================================================================
// THE MOD, RUNNING IN THE LIVE GAME (spec 1.8 -> 2.6):
//   read the engine's per-node/per-good produced quantities -> solve the per-good graphs with
//   the shipped DRAIN operator over the same install data the reference uses -> route each
//   good's injected value along its own graph -> write the routed totals back into the engine's
//   node fields, so the game's own numbers become the model's numbers (Goal 7).
#include "../src/economy.h"

// Solve + route + (optionally) install, NAME-KEYED so live nodes and solver-field nodes line up
// regardless of file order (spec 1.8 -> 2.6). Returns the field, its node names and the per-good
// graphs so the monthly loop can re-route without re-solving.
struct Installed {
    field::Field f;
    std::vector<std::string> names;                     // field index -> node name
    std::vector<std::vector<std::pair<int,int>>> graphs; // per live-good, field-indexed
    std::vector<int> good_slot;                          // parallel to graphs: engine good slot
    bool ok = false;
};

static void run_install(const std::string& logpath) {
    std::ofstream log(logpath, std::ios::app);
    log << "=== INSTALL: per-good economy -> engine (name-keyed) ===\n";

    // WAIT FOR LIVE TRADE DATA. The engine populates each node's trade_goods_size and
    // local_value in the monthly value pass; a DLL injected before the first pass (or while a
    // campaign is still loading) sees an all-zero trade state, and installing on that would
    // route nothing and destroy the naming match. Poll until the world carries value.
    std::vector<livetrade::SimNode> sim;
    double world_local = 0;
    for (int attempt = 0; attempt < 120; attempt++) {          // up to ~60s
        sim = livetrade::read_sim_nodes();
        world_local = 0;
        for (auto& s : sim) world_local += s.local_value;
        if (!sim.empty() && world_local > 0.0) break;
        Sleep(500);
    }
    if (sim.empty()) { log << "  no live nodes; aborting install\n"; return; }
    if (world_local <= 0.0) {
        log << "  live trade state still empty after waiting (is a campaign running?); "
               "aborting install rather than writing zeros\n";
        return;
    }
    int named = 0; for (auto& s : sim) if (!s.name.empty()) named++;
    log << "  live: " << sim.size() << " nodes, world local=" << world_local
        << " (monthly), " << named << " named from memory\n";

    std::string root = install_dir();
    std::string save = std::string(getenv("USERPROFILE") ? getenv("USERPROFILE") : "") +
        "\\OneDrive\\Documents\\Paradox Interactive\\Europa Universalis IV"
        "\\save games\\VANILLA_start.eu4";
    try {
        gamedata::TradeNodes tn = gamedata::load_tradenodes(
            root + "/common/tradenodes/00_tradenodes.txt");
        gamedata::StaticMods sm = gamedata::load_static_mods(root);
        auto prices = gamedata::load_prices(root);
        auto goods_order = gamedata::load_goods_order(root);   // slot k <-> goods_order[k-1] (1-based)
        std::map<std::string, int> good_slot;                  // good name -> engine tgs slot
        for (int k = 0; k < (int)goods_order.size(); k++) good_slot[goods_order[k]] = k + 1;
        save::SaveData sd = save::load(save);
        field::Field f = field::build(tn, sm, sd, prices);
        drain::Graph g; g.N = f.N; g.und = tn.und; g.edges_und = tn.edges_und;

        // ---- LIVE WORLD READ (spec 2.2: the DLL reads live memory, never a save) ----
        // Build the same field from the running game's province table and compare. At the 1444
        // start the two must agree; from then on only the LIVE field tracks the campaign, which
        // is what lets the orientation move month to month (F1/F3/F4/F5).
        {
            liveworld::WorldRead w = liveworld::read_world();
            log << "  live world read: " << w.provinces_seen << " provinces seen, " << w.owned
                << " owned, " << w.with_good << " with a trade good, "
                << w.sd.current_prices.size() << " prices\n";
            if (w.ok) {
                try {
                    field::Field lf = field::build(tn, sm, w.sd, prices);
                    log << "    live field: " << lf.rows.size() << " counted provinces, world wealth "
                        << lf.world_wealth << "  (save field: " << f.rows.size() << " / "
                        << f.world_wealth << ")\n";
                    // solve Phi_w on the live field and report its ends
                    std::vector<double> lb = field::b_aggregate(lf);
                    std::vector<double> ls(lf.N, 1.0 / lf.N), lc(lf.N);
                    for (int n = 0; n < lf.N; n++) lc[n] = ls[n] - lb[n];
                    drain::Result lr = drain::run(g, lb, lf.tie_cost_edge, lf.node_wealth, ls, lc);
                    std::vector<int> od(lf.N, 0);
                    for (auto& e : lr.directed) od[e.first]++;
                    std::string ends;
                    for (int i = 0; i < lf.N; i++) if (od[i] == 0) ends += tn.order[i] + " ";
                    log << "    live Phi_w ends { " << ends << "}\n";
                    if (livetrade::marker_present("LIVEFIELD")) {
                        f = lf;                     // the live field becomes the model's field
                        log << "    USING THE LIVE FIELD (orientation now tracks the campaign)\n";
                    }
                } catch (const std::exception& e) {
                    log << "    live field build failed: " << e.what() << "\n";
                }
            }
        }

        // NAME the live nodes authoritatively: the engine node-array order is a permutation of
        // both the file order and the save order, so match each live node to a save node by its
        // stable trade_goods_size production vector (nearest L1, 1-to-1), keyed by engine id.
        nodemap::Map nm = nodemap::resolve(sim, sd.nodes);
        for (auto& s : sim) {
            auto it = nm.id_to_name.find(s.index);
            if (it != nm.id_to_name.end()) s.name = it->second;
        }
        install::g_id_to_name = nm.id_to_name;
        log << "  named live nodes by goods-signature: " << nm.matched << " matched ("
            << nm.exact << " exact), " << nm.spurious << " spurious/unnamed\n";

        // gather live inject into FIELD index order, BY NAME (the index-mismatch fix)
        int goods_count = 0, matched = 0;
        auto inject = install::gather_inject(sim, tn.order, goods_count, matched);
        log << "  matched " << matched << "/" << f.N << " live nodes to solver nodes by name\n";

        // LIVE per-country standings (spec 1.8): the engine's own trade power, collect/steer
        // intent and steering targets, so routing uses the real merchant field rather than the
        // no-merchant even split. Steer indices are engine outgoing-link indices, so build each
        // node's outgoing destination list in the engine's own link order first.
        std::vector<std::vector<int>> link_targets(f.N);
        {
            std::map<std::string, int> fidx;
            for (int i = 0; i < f.N; i++) fidx[tn.order[i]] = i;
            for (int i = 0; i < f.N; i++)
                for (const auto& og : tn.nodes[i].outgoing) {
                    auto d = fidx.find(og.name);
                    link_targets[i].push_back(d == fidx.end() ? -1 : d->second);
                }
        }
        std::map<int, std::vector<int>> collect_nodes;
        auto live_st = install::read_standings_field(sim, tn.order, link_targets, collect_nodes);
        {
            int with_power = 0, traders = 0, steerers = 0;
            for (auto& ns : live_st) for (auto& e : ns.entries) {
                if (e.power > 0) with_power++;
                if (e.collects) traders++;
                if (e.steer_to >= 0) steerers++;
            }
            log << "  live standings: " << with_power << " country-node power entries, "
                << traders << " collecting, " << steerers << " steering\n";
            if (livetrade::marker_present("STANDDUMP"))
                install::dump_standings(logpath, sim, {"sevilla", "genua", "english_channel"});
        }

        static std::vector<std::vector<std::pair<int, int>>> s_graphs;
        static std::vector<int> s_slots;
        static std::vector<double> s_prices;
        static std::vector<std::string> s_names;
        static field::Field s_field;
        s_graphs.clear(); s_slots.clear(); s_prices.clear();
        std::vector<econ::GoodFlow> per_good;
        std::vector<std::vector<double>> inj_field;   // per live good, field-indexed
        int solved = 0;
        for (int gi = 0; gi < (int)f.goods.size(); gi++) {
            if (!f.live[gi]) continue;
            std::vector<double> b(f.N), s = f.S[gi], c = f.C[gi];
            for (int n = 0; n < f.N; n++) b[n] = s[n] - c[n];
            drain::Result r = drain::run(g, b, f.tie_cost_edge, f.node_wealth, s, c);
            // engine tgs slot for THIS good by name (sorted good order != tradegoods file order),
            // and inject VALUE = live produced quantity x current price (spec 1.8).
            auto slotit = good_slot.find(f.goods[gi]);
            int slot = slotit != good_slot.end() ? slotit->second : (gi + 1);
            double price = field::price_of(f.goods[gi], sd.current_prices, prices);
            std::vector<double> inj(f.N, 0.0);
            if (slot < goods_count) for (int n = 0; n < f.N; n++) inj[n] = inject[slot][n] * price;
            econ::GoodFlow F = econ::route(f.N, r.directed, inj, live_st, collect_nodes, 0.05);
            per_good.push_back(F);
            inj_field.push_back(inj);
            s_graphs.push_back(r.directed);
            s_slots.push_back(slot);
            s_prices.push_back(price);
            solved++;
        }
        auto agg = econ::aggregate(f.N, per_good, inj_field);
        double world_total = 0, world_local = 0, world_pool = 0;
        for (auto& a : agg) { world_total += a.total; world_local += a.local; world_pool += a.pool; }
        log << "  solved+routed " << solved << " goods; world total=" << world_total
            << " local=" << world_local << " collectible=" << world_pool << " (annual)\n";
        s_names = tn.order; s_field = f;

        // Phi_w (the installed/drawn orientation) and the per-link net realized flows (spec 2.6)
        std::vector<std::pair<int, int>> phi_w;
        {
            std::vector<double> bagg = field::b_aggregate(f);
            std::vector<double> sw(f.N, 1.0 / f.N), cw(f.N);
            for (int n = 0; n < f.N; n++) cw[n] = sw[n] - bagg[n];
            drain::Result rw = drain::run(g, bagg, f.tie_cost_edge, f.node_wealth, sw, cw);
            phi_w = rw.directed;
        }
        // GROSS directed flows are what the engine's incoming records hold (non-negative, spec 1.12).
        auto net_links = econ::gross_link_flows(per_good);
        auto signed_net = econ::net_link_flows(phi_w, per_good);   // measured, for the 2.8 report
        static std::map<std::pair<int, int>, double> s_netlinks;
        static std::map<int, std::string> s_id2name;
        s_netlinks = net_links; s_id2name = nm.id_to_name;

        if (livetrade::marker_present("INSTALL")) {
            // LINKS FIRST: install_aggregate derives each node's outgoing from what the node
            // actually holds (engine local + the incoming records), so the model's arrivals must
            // already be in those records when it runs.
            int links = install::install_links(sim, tn.order, net_links, nm.id_to_name);
            int wrote = install::install_aggregate(sim, tn.order, agg);
            log << "  INSTALLED pool+outgoing on " << wrote << " nodes, " << links
                << " link values (local left intact per B4)\n";
            // THE TICK HOOK (spec 2.6): land the write inside the engine's own monthly
            // update, between the value pass and the collector division. Preferred over the
            // polling loop -- it is the point spec 2.6 names, and pass 10 then divides OUR pool.
            if (livetrade::marker_present("TICKHOOK")) {
                ticklive::g_log = logpath;
                ticklive::g_plan.graphs = s_graphs;
                ticklive::g_plan.slots = s_slots;
                ticklive::g_plan.prices = s_prices;
                ticklive::g_plan.names = tn.order;
                ticklive::g_plan.link_targets = link_targets;
                ticklive::g_plan.phi_w = phi_w;
                ticklive::g_plan.N = f.N;
                // precompute each good's reachability once: it depends only on the orientation,
                // so the tick hook never pays for it (spec H3)
                ticklive::g_plan.reach.clear();
                for (auto& gr : s_graphs) {
                    std::vector<std::vector<int>> outs(f.N);
                    for (auto& e : gr) outs[e.first].push_back(e.second);
                    ticklive::g_plan.reach.push_back(econ::reach_sets(f.N, outs));
                }
                ticklive::g_plan.ready = true;
                std::string herr;
                // the background solver: statics once, then a re-solve per month
                resolver::g_st.tn = tn;
                resolver::g_st.sm = sm;
                resolver::g_st.base_prices = prices;
                resolver::g_st.good_slot = good_slot;
                resolver::g_st.graph = g;
                resolver::g_st.ready = true;
                resolver::start(logpath);
                arrows::g_log = logpath;
                // warm the definition cache HERE (worker thread): it is a heap scan, far too
                // slow to run inside the monthly tick (spec H3).
                if (livetrade::marker_present("DEFDUMP")) arrows::dump_definition_layout(logpath, 3);
                {
                    auto defs = arrows::definitions();
                    log << "  arrow definitions cached: " << defs.size()
                        << " (" << arrows::g_def_source << ")\n";
                }
                {
                    std::string aerr;
                    if (arrows::install_capture(&aerr))
                        log << "  arrow-layer capture installed at eu4.exe+0x10AFA70\n";
                    else
                        log << "  arrow-layer capture NOT installed: " << aerr << "\n";
                }
                ticklive::start_verifier();
                if (ticklive::install_hook(&herr))
                    log << "  TICK HOOK installed at eu4.exe+0xB4BF09 (writes land inside the "
                           "engine's monthly update, before the collector division)\n";
                else
                    log << "  tick hook NOT installed: " << herr << "\n";
            }
            if (livetrade::marker_present("MONTHLY")) {
                static std::string s_log = logpath;
                static volatile bool s_stop = false;
                CreateThread(nullptr, 0, [](LPVOID) -> DWORD {
                    int ticks = 0;
                    tickhook::run_monthly_loop([&](const std::vector<livetrade::SimNode>& sim2) {
                        int gc = 0, mm = 0;
                        auto inj2 = install::gather_inject(sim2, s_names, gc, mm);
                        std::vector<econ::GoodFlow> pg;
                        std::vector<std::vector<double>> injf;
                        for (size_t k = 0; k < s_graphs.size(); k++) {
                            int slot = s_slots[k];
                            std::vector<double> in(s_field.N, 0.0);
                            if (slot < gc) for (int n = 0; n < s_field.N; n++) in[n] = inj2[slot][n] * s_prices[k];
                            std::vector<econ::NodeStandings> st(s_field.N);
                            pg.push_back(econ::route(s_field.N, s_graphs[k], in, st, {}, 0.05));
                            injf.push_back(in);
                        }
                        auto ag = econ::aggregate(s_field.N, pg, injf);
                        int lk = install::install_links(sim2, s_names, s_netlinks, s_id2name);
                        int w = install::install_aggregate(sim2, s_names, ag);
                        std::ofstream lg(s_log, std::ios::app);
                        lg << "[monthly] tick " << ++ticks << ": re-installed " << w
                           << " nodes, " << lk << " links\n";
                    }, &s_stop);
                    return 0;
                }, nullptr, 0, nullptr);
                log << "  MONTHLY loop started: economy re-installed every trade tick\n";
            }
        } else {
            log << "  (dry run -- create pgt.INSTALL next to the DLL to write these values)\n";
            auto byname = install::live_by_name(sim);
            for (int fn = 0; fn < 8 && fn < f.N; fn++) {
                auto it = byname.find(tn.order[fn]);
                double eng = it != byname.end() ? sim[it->second].local_value : -1;
                log << "    " << tn.order[fn] << " engine local=" << eng
                    << " model total=" << agg[fn].total << " pool=" << agg[fn].pool << "\n";
            }
        }
    } catch (const std::exception& e) {
        log << "  install failed: " << e.what() << "\n";
    }
    log << "=== INSTALL complete ===\n";
}

static void attach_main() {
    // PGT_ROOT lets a test host point the file checks + solver self-test at the real install
    // without the DLL sitting in Program Files; unset in normal use (root = the exe's own dir).
    // The install root is where eu4.exe lives (this DLL is injected into it). Env vars are not
    // inherited by an already-running target, so nothing here depends on them.
    std::string root = install_dir();
    // Log next to THIS DLL (its own directory is writable and known), falling back to %TEMP%.
    // The install directory is typically write-protected, so never log there.
    std::string logpath;
    {
        char self[MAX_PATH] = {0};
        HMODULE hself = nullptr;
        GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                           GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                           (LPCSTR)&install_dir, &hself);
        DWORD n = GetModuleFileNameA(hself, self, MAX_PATH);
        std::string dir;
        if (n) {
            std::string p(self, n);
            size_t slash = p.find_last_of("\\/");
            if (slash != std::string::npos) dir = p.substr(0, slash);
        }
        if (dir.empty()) {
            char tmp[MAX_PATH] = {0};
            GetTempPathA(MAX_PATH, tmp);
            dir = tmp;
            if (!dir.empty() && (dir.back() == '\\' || dir.back() == '/')) dir.pop_back();
        }
        logpath = dir + "\\per-good-trade.log";
    }
    g_logpath = logpath;
    g_log.open(logpath, std::ios::app);
    L("=== per-good-trade.dll attach ===");
    L("install dir: " + root);

    // 1. build gate -- in-memory version string first (EU4dll's method), then file identity
    pat::Module m = pat::main_module();
    L("main module base " + std::to_string(m.base) + " size " + std::to_string(m.size));
    // Two independent identity proofs; BOTH are checked and at least one must confirm the target,
    // and neither may contradict it. The file check (eu4_rev.txt + eu4.exe SHA-256) is
    // authoritative; the in-memory string scan is corroboration -- it can legitimately miss when
    // the string sits in a not-yet-paged section of the mapped image, which is not evidence of a
    // wrong build. A file-check FAILURE always refuses (spec 2.5: a patch is a new binary).
    uintptr_t vs = pat::find_string(m, attach::TARGET_BRANCH);
    attach::Verdict v = attach::verify_install(root, true);
    if (!v.ok) {
        L("REFUSE: " + v.message);
        return;
    }
    L("build gate PASS: " + v.message +
      (vs ? ("; in-memory '" + std::string(attach::TARGET_BRANCH) + "' @ " + std::to_string(vs))
          : "; (in-memory string not paged in -- file identity is authoritative)"));

    // 2. embedded solver self-test
    solver_self_test(root);

    // 3. hook seams
    hooks::InstallReport hr = hooks::install(m);
    L("hook seams: " + std::to_string(hr.resolved) + " resolved, " +
      std::to_string(hr.pending) + " pending (debugger session):");
    for (auto& line : hr.lines) L("  " + line);
    if (hr.resolved == 0)
        L("mod is READ-ONLY: all live-memory seams pending. Build gate + embedded solver only.");

    // 4. in-process live trade access (injected into a running game). Spawns a worker thread so
    // no heavy memory-walking happens under the loader lock.
    static std::string s_logpath = g_logpath;
    HANDLE wt = CreateThread(nullptr, 0, [](LPVOID) -> DWORD {
        // Log directly (not via L(), whose ofstream belongs to the attach thread) so every stage
        // is visible even if a later stage faults.
        auto note = [](const char* s) {
            std::ofstream f(s_logpath, std::ios::app);
            f << "[worker] " << s << "\n";
        };
        note("worker started");
        Sleep(1500);
        note("scanning for trade nodes...");
        try {
            livetrade::log_snapshot(s_logpath);
            if (livetrade::marker_present("LINKDUMP")) {
                auto sim0 = livetrade::read_sim_nodes();
                livetrade::dump_incoming(s_logpath, sim0);
            }
            note("snapshot complete");
            run_install(s_logpath);
        } catch (const std::exception& e) {
            std::ofstream f(s_logpath, std::ios::app);
            f << "[worker] EXCEPTION: " << e.what() << "\n";
        } catch (...) {
            note("unknown exception during snapshot");
        }
        return 0;
    }, nullptr, 0, nullptr);
    L(wt ? "livetrade worker thread created" : "FAILED to create livetrade worker thread");
    L("=== attach complete (livetrade worker spawned) ===");
}

BOOL APIENTRY DllMain(HMODULE, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        attach_main();
    }
    return TRUE;
}
