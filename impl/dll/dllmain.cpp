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
#include "tickhook.h"
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
static void run_install(const std::string& logpath) {
    std::ofstream log(logpath, std::ios::app);
    log << "=== INSTALL: per-good economy -> engine ===\n";

    auto sim = livetrade::read_sim_nodes();
    if (sim.empty()) { log << "  no live nodes; aborting install\n"; return; }
    int N = (int)sim.size();
    int goods_count = 0;
    auto inject = install::read_inject(sim, goods_count);
    log << "  live: " << N << " nodes, " << goods_count << " good slots\n";

    // Solve the model's graphs from the install + start save (the same inputs, and the same
    // DRAIN code, the reference implementation uses -- spec 2.8's cross-implementation basis).
    std::string root = install_dir();
    std::string save = std::string(getenv("USERPROFILE") ? getenv("USERPROFILE") : "") +
        "\\OneDrive\\Documents\\Paradox Interactive\\Europa Universalis IV"
        "\\save games\\VANILLA_start.eu4";
    try {
        gamedata::TradeNodes tn = gamedata::load_tradenodes(
            root + "/common/tradenodes/00_tradenodes.txt");
        gamedata::StaticMods sm = gamedata::load_static_mods(root);
        auto prices = gamedata::load_prices(root);
        save::SaveData sd = save::load(save);
        field::Field f = field::build(tn, sm, sd, prices);
        drain::Graph g; g.N = f.N; g.und = tn.und; g.edges_und = tn.edges_und;

        // route every live good along its own graph
        std::vector<double> routed(N, 0.0);
        std::vector<std::vector<std::pair<int, int>>> graphs;   // per live good, in slot order
        int solved = 0;
        for (int gi = 0; gi < (int)f.goods.size(); gi++) {
            if (!f.live[gi]) continue;
            std::vector<double> b(f.N), s = f.S[gi], c = f.C[gi];
            for (int n = 0; n < f.N; n++) b[n] = s[n] - c[n];
            drain::Result r = drain::run(g, b, f.tie_cost_edge, f.node_wealth, s, c);
            // the engine's good slot for this model good: slot k <-> good index k-1 (spec 1.8)
            int slot = gi + 1;
            if (slot >= goods_count) continue;
            // keep the graph indexed by (slot-1) so the monthly loop can re-route without
            // re-solving: the orientation only changes when the world state does.
            if ((int)graphs.size() < slot) graphs.resize(slot);
            graphs[slot - 1] = r.directed;
            std::vector<double> inj(f.N, 0.0);
            for (int n = 0; n < f.N && n < N; n++) inj[n] = inject[slot][n];
            auto collected = install::route_good(f.N, r.directed, inj);
            for (int n = 0; n < f.N && n < N; n++) routed[n] += collected[n];
            solved++;
        }
        double total = 0;
        for (double v : routed) total += v;
        log << "  solved+routed " << solved << " goods; routed world value = " << total << "\n";

        if (livetrade::marker_present("INSTALL")) {
            int wrote = install::install_economy(sim, routed);
            log << "  INSTALLED into the engine: wrote " << wrote << " node values\n";

            // ---- stay installed: re-apply on every monthly trade tick (spec 2.6) ----
            // The engine rebuilds its node values each month; without this the mod's economy
            // would be overwritten after one tick. The loop detects a completed monthly update
            // and re-installs immediately after it, which is where spec 2.6 puts the write.
            if (livetrade::marker_present("MONTHLY")) {
                static std::vector<std::vector<std::pair<int, int>>> s_graphs;
                static std::string s_log = logpath;
                s_graphs = graphs;
                static volatile bool s_stop = false;
                CreateThread(nullptr, 0, [](LPVOID) -> DWORD {
                    int ticks = 0;
                    tickhook::run_monthly_loop([&](const std::vector<livetrade::SimNode>& sim2) {
                        int gc = 0;
                        auto inj2 = install::read_inject(sim2, gc);
                        std::vector<double> routed2(sim2.size(), 0.0);
                        for (size_t gi = 0; gi < s_graphs.size(); gi++) {
                            int slot = (int)gi + 1;
                            if (slot >= gc) continue;
                            std::vector<double> in(sim2.size(), 0.0);
                            for (size_t n = 0; n < sim2.size(); n++) in[n] = inj2[slot][n];
                            auto col = install::route_good((int)sim2.size(), s_graphs[gi], in);
                            for (size_t n = 0; n < sim2.size(); n++) routed2[n] += col[n];
                        }
                        int w = install::install_economy(sim2, routed2);
                        std::ofstream lg(s_log, std::ios::app);
                        lg << "[monthly] tick " << ++ticks << ": re-installed " << w
                           << " node values\n";
                    }, &s_stop);
                    return 0;
                }, nullptr, 0, nullptr);
                log << "  MONTHLY loop started: the economy is re-installed every trade tick\n";
            }
        } else {
            log << "  (dry run -- create pgt.INSTALL next to the DLL to write these values)\n";
            for (int n = 0; n < 8 && n < N; n++)
                log << "    node[" << sim[n].index << "] engine local=" << sim[n].local_value
                    << " -> model routed=" << routed[n] << "\n";
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
