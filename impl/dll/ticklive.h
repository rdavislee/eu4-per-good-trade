// THE TICK HOOK (spec 2.6): write the model's economy inside the engine's own monthly trade
// update, in the window between the value pass and the collector division.
//
// The monthly driver 0xB4BA90 ends with two loops:
//
//   0xB4BEF8:  for each node in calc order:  call 0xB52160   (the value pass)
//   0xB4BF07   jne -> loop
//   0xB4BF09:  rbx = mgr->nodes; rax = mgr->count           <-- WE HOOK HERE
//   0xB4BF30:  for each node:  call 0xB584F0                 (pass 10: collector division,
//              which computes rec.total = node.current * rec.power_fraction/1000, then
//              rec.money, then CCountry::AddDelayedIncome(country, 2 /*trade*/, &money))
//
// Hooking at 0xB4BF09 means every node's `current` (+0xB0) and every country record's
// `power_fraction` (+0x2C) are final, and nothing recomputes them before pass 10 reads them.
// So writing the model's collectible pool and the model's per-country shares there makes the
// ENGINE'S OWN division pay out the model's income -- into the treasury and the ledger's trade
// category -- with no second income path of our own. That is exactly what spec 2.6 asks for:
// "feeding the engine the collectible pool is sufficient".
//
// The handler must be fast (spec H3: the added tick time must be imperceptible), so it does no
// LP work: the per-good orientations are solved once and cached, and the handler only re-routes
// the live inject over them and writes. Registers at the site: rsi = CTradeManager.
#pragma once
#include <windows.h>
#include <atomic>
#include <cstdio>
#include <algorithm>
#include <fstream>
#include <mutex>
#include <map>
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"
#include "install.h"
#include "resolver.h"
#include "arrows.h"
#include "shock.h"
#include "relink.h"
#include "viewmode.h"
#include "selprov.h"
#include "gates.h"
#include "treasure.h"
#include "colorview.h"
#include "assign.h"
#include "syncrec.h"
#include "flagfix.h"
#include "transfertext.h"
#include "outlinertext.h"
#include "endtext.h"
#include "lightship.h"
#include "clickfix.h"
#include "envoy.h"
#include "nocollect.h"
#include "igiprobe.h"
#include "aiguard.h"
#include "propprobe.h"
#include "caravan.h"
#include "money.h"
#include "aiwire.h"
#include "console.h"
#include "outlinks.h"
#include "flowwrite.h"
#include "linkvalue.h"
#include "revpanel.h"
#include "frame.h"
#include "../src/economy.h"

namespace savegame { std::string loaded_save_name(); }   // defined in savegame.h (included after this header)

namespace ticklive {

inline std::atomic<bool> g_verify_pending;

// what the handler needs, precomputed at attach
struct Plan {
    std::vector<std::vector<std::pair<int, int>>> graphs;  // per live good, field-indexed
    std::vector<int> slots;                                // engine trade_goods_size slot per good
    std::vector<double> prices;                            // current price per good
    std::vector<std::string> names;                        // field index -> node name
    std::vector<std::string> good_names;                   // parallel to graphs: the good's name
    std::vector<std::vector<int>> link_targets;            // node -> outgoing destinations
    std::vector<std::pair<int, int>> phi_w;                // the installed orientation
    std::vector<std::pair<int, int>> phi_w_prev;           // previous, to name the flips
    std::vector<std::vector<std::vector<char>>> reach;      // per good, precomputed reachability
    int N = 0;
    int generation = 0;
    bool ready = false;
};

inline Plan g_plan;
inline std::string g_log;
inline std::atomic<int> g_ticks{0};
inline int g_reach_rebuilt = 0;   // engine reachability rebuilds after our graph rewrites
// MATRIX C IS THE MODEL REACH (user, 2026-08-27). The engine rebuild makes the byte permissive
// under our merchant cones, which neuters the two consumers that need a REAL distinction: the
// light-ship scorer reach gate and the +10%/merchant home bonus counter. The model notion: node n
// counts for country c iff SOME good graph carries value from n to the country home (or n IS the
// home). Computed each tick from g_plan.reach, applied after every engine rebuild (the engine own
// monthly rebuild runs before our hook; the landing rebuild re-applies).
inline std::map<int, std::vector<uint8_t>> g_matc;   // country index -> byte per ENGINE node index
inline int g_matc_written = 0, g_matc_countries = 0;
inline void apply_matrix_c() {
    if (g_matc.empty() || livetrade::marker_present("NOREACHC")) return;
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + 0x21BC, 4) || !livetrade::validate_region(g + 0x2230, 8) || !livetrade::validate_region(g + 0x2238, 4)) return;
    int Neng = livetrade::fi(g + 0x21BC);
    uintptr_t C = livetrade::fq(g + 0x2230);
    int total = livetrade::fi(g + 0x2238);
    if (!C || Neng <= 0 || total <= 0 || !livetrade::validate_region(C, (size_t)total)) return;
    for (auto& [cidx, bytes] : g_matc) {
        if ((int)bytes.size() != Neng) continue;
        long long off = (long long)cidx * Neng;
        if (off < 0 || off + Neng > total) continue;
        memcpy((void*)(C + off), bytes.data(), (size_t)Neng);
        g_matc_written++;
    }
}
inline void compute_matrix_c() {
    g_matc.clear();
    if (!homeward::g_ready || g_plan.reach.empty() || livetrade::marker_present("NOREACHC")) return;
    uintptr_t g = livetrade::game_singleton();
    int Neng = (g && livetrade::validate_region(g + 0x21BC, 4)) ? livetrade::fi(g + 0x21BC) : 0;
    if (Neng <= 0) return;
    // engine node index by field: install::g_id_to_name is engine id -> name; the id is the array index
    std::map<std::string, int> eng_of_name;
    for (auto& [id, nm] : install::g_id_to_name) eng_of_name[nm] = id;
    std::vector<int> eng_of_field(g_plan.N, -1);
    for (int fn = 0; fn < g_plan.N && fn < (int)g_plan.names.size(); fn++) {
        auto it = eng_of_name.find(g_plan.names[fn]);
        if (it != eng_of_name.end() && it->second >= 0 && it->second < Neng) eng_of_field[fn] = it->second;
    }
    // reach_any[n][h]: h reachable from n in SOME good graph (185k char ORs: trivial)
    std::vector<std::vector<char>> reach_any(g_plan.N, std::vector<char>(g_plan.N, 0));
    for (auto& R : g_plan.reach)
        for (int n = 0; n < g_plan.N && n < (int)R.size(); n++)
            for (int h = 0; h < g_plan.N && h < (int)R[n].size(); h++)
                if (R[n][h]) reach_any[n][h] = 1;
    for (auto& [cidx, home] : homeward::g_home_of) {
        if (home < 0 || home >= g_plan.N) continue;
        std::vector<uint8_t> bytes((size_t)Neng, 0);
        for (int fn = 0; fn < g_plan.N; fn++) {
            int ei = eng_of_field[fn];
            if (ei < 0) continue;
            bytes[ei] = (fn == home || reach_any[fn][home]) ? 1 : 0;
        }
        g_matc[cidx] = std::move(bytes);
    }
    g_matc_countries = (int)g_matc.size();
    apply_matrix_c();
}
inline int g_reach_rebuilt_frame = 0;   // ...of which from the frame poll after merchant landings
inline int g_installed_gen = -1;   // generation whose orientation is installed
inline int g_installed_view = -2;  // viewmode::g_selected it was installed for
// INSTANT VIEW SWITCH (user, 2026-08-27; reviewed): a province click must swap the arrows, panels
// and values THE MOMENT it happens, paused included. The click may NEVER run the model tick -- a
// second apply() in the same engine month double-subtracts the D3 propagation (the power ratchet),
// races the tick thread through relink/arrows (both directions drawn at once), and pays pass 10
// on a single good's pool. So the tick caches its model outputs and the frame poll re-renders the
// DISPLAY alone from that cache: orientation install + link/node value writes, no standings write,
// no pool write, no AI, no dispatch, under the same g_inside exclusion the tick uses.
inline std::mutex g_render_mx;
inline bool g_render_valid = false;                       // set by the first real tick
inline std::vector<econ::GoodFlow> g_r_per_good;          // last tick's routed flows, all goods
inline std::vector<std::vector<double>> g_r_inj;          // and their injections
inline std::map<std::string, double> g_r_engine_local;    // the ENGINE's own +0xB4 at that tick (monthly)
inline std::atomic<int> g_rendered_view{-999};            // viewmode::g_selected the display currently shows
// IN-SESSION RELOADS THAT BYPASS THE InitSaveGame SITE (user, 2026-08-27: exit to menu -> load a
// save reverted the mod to vanilla). 0x5D00BC is the binary's ONLY direct caller of InitSaveGame
// (E8/E9 scan of the whole .text), yet an in-game load runs neither it nor the inner 0x775EEC site
// -- a different loader entirely. Detection is therefore generic: the trade manager the plan was
// set up for. A reload allocates a new world, so a tick or frame that sees a DIFFERENT manager is
// a world this plan and every pointer cache must not touch: the tick skips, the frame poll runs
// the save setup (reset + sidecar restore + suppressed driver + solve) exactly as the loading path
// would have.
inline std::atomic<uintptr_t> g_world_mgr{0};             // the manager finish_setup armed the plan for
inline void (*g_resetup_inline)(uintptr_t) = nullptr;     // earlyload's in-session save setup
inline void (*g_resetup_in_tick)(uintptr_t) = nullptr;    // the same, safe inside the monthly driver
// THE MANAGER POINTER IS A CONSTANT (2026-08-27): trade_manager() returns g+0x2198, a fixed
// sub-object of the process-lifetime game singleton, so it is identical across every campaign and
// reload -- comparing it can NEVER detect a load (that was the ET/Ironman "quit to menu -> reopen
// -> vanilla" bug). The world's IDENTITY is its node array instead: mgr+0x18 (begin ptr) and
// mgr+0x24 (count), which the engine CLEARS on quit-to-menu and repopulates on load. A reload is
// any transition of that pair after the plan was armed -- including the count going to 0 at the
// menu and back. g_world_nb/g_world_cnt are the armed-for identity; g_saw_no_world latches the
// menu gap so even a same-address, same-count reload is caught.
inline std::atomic<uintptr_t> g_world_nb{0};
inline std::atomic<int> g_world_cnt{0};
inline std::atomic<uint64_t> g_world_fp{0};
inline std::atomic<bool> g_saw_no_world{false};
// THE GAME DATE IS THE CAMPAIGN-CHANGE SIGNAL THAT SURVIVES THE MENU GAP (2026-08-27).
// The frame hook rides the MAP UPDATE, so no frames run at the menu or during a load: every
// transient signal (node count going to 0, game.log truncation) happens inside that blind window
// and is gone by the time polling resumes -- and ET reuses ONE node set at every date, so the
// node array and key fingerprint are byte-identical across 1241 -> 1776. The date is not
// transient: it is simply different afterwards. G+0x1DF0 holds days with 365-day years (found by
// scanning G for date-range ints: exactly one candidate, 648424 == 1776.7.4 = 1776*365+185).
// A campaign change moves it by years; normal play advances it a few days between polls.
constexpr uintptr_t GAME_DATE_OFF = 0x1DF0;
constexpr int DATE_JUMP_FWD = 730;                 // a NEW campaign is a bookmark years away; normal play advances <= a month between polls
constexpr int DATE_BACK_TOL = 30;                  // a backward move past this is a load (never happens in normal play)
// g_world_date is a ROLLING LAST-SEEN date, refreshed every poll/tick, NOT the setup date --
// comparing against the setup date fired a bogus resetup ~3 months into EVERY campaign (measured:
// the 1444 spectator run re-solved every 90 days). Only a real jump (backward, or years forward in
// one step) means the campaign changed.
inline int engine_date() {
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + GAME_DATE_OFF, 4)) return -1;
    int d = livetrade::fi(g + GAME_DATE_OFF);
    return (d > 100000 && d < 1200000) ? d : -1;   // plausible EU4 date, else "unknown"
}
inline std::atomic<int> g_world_date{-1};
inline std::string g_world_save;                   // frame-poll thread only (the loaded save's name)
// THE ENGINE TRUNCATES logs/game.log ON EVERY CAMPAIGN LAUNCH (measured: after Mongolia -> USA
// in one process, the file held only USA's session). That is the one campaign-change signal that
// fires for EVERY path -- menu new game, menu load, in-game load, Ironman -- regardless of which
// internal loader ran, and regardless of the node set (ET reuses the same 80 nodes at every date,
// which is why the key fingerprint alone missed a menu -> new-date switch). A size DECREASE
// latches g_saw_no_world; the first frame poll after that runs only once the new world's map
// renders, so the resetup always sees the completed world.
inline std::string g_gamelog_path;                 // set at attach (dllmain; needs savegame::userdir_root)
inline long long g_gamelog_last = -1;              // frame-poll thread only
// A world's IDENTITY that survives everything: the FNV hash of its node count and every node's
// definition key. Two campaigns with the same node count at the same reused array address (an ET
// in-session new game after a load -- 1241 Mongolia has ~80 nodes too) still differ here, because
// their node KEYS differ. This is what nb/cnt alone missed. Cheap: node_key reads under a
// TickCacheScope collapse ~130 VirtualQuery calls to one.
inline uint64_t world_fingerprint(uintptr_t mgr) {
    if (!mgr || !livetrade::validate_region(mgr + 0x18, 16)) return 0;
    uintptr_t base = livetrade::fq(mgr + 0x18);
    int cnt = livetrade::validate_region(mgr + 0x24, 4) ? livetrade::fi(mgr + 0x24) : 0;
    if (!base || cnt <= 0 || cnt > 4096 || !livetrade::validate_region(base, (size_t)cnt * 0x138)) return 0;
    livetrade::TickCacheScope cache;
    uint64_t h = 1469598103934665603ull;
    h ^= (uint64_t)(unsigned)cnt; h *= 1099511628211ull;
    for (int i = 0; i < cnt; i++) {
        std::string k = livetrade::node_key(base + (uintptr_t)i * 0x138);
        for (unsigned char c : k) { h ^= c; h *= 1099511628211ull; }
        h ^= 0x9E; h *= 1099511628211ull;             // key separator
    }
    return h;
}
inline void arm_world_identity(uintptr_t mgr) {
    g_world_mgr = mgr;
    if (mgr && livetrade::validate_region(mgr + 0x24, 4) && livetrade::validate_region(mgr + 0x18, 8)) {
        g_world_nb  = livetrade::fq(mgr + 0x18);
        g_world_cnt = livetrade::fi(mgr + 0x24);
    }
    g_world_fp = world_fingerprint(mgr);
    g_world_date = engine_date();
    g_world_save = savegame::loaded_save_name();
    g_saw_no_world = false;
}
inline std::atomic<bool> g_inside{false};
inline detour::Hook g_hook;

// ---------------------------------------------------------------------------------------
// TEST E1 (spec 2.6 / 3.10): "ledger trade income = powershare_C(n) . collect_pool(n) summed
// over the country's collecting nodes, to the ducat".
//
// We write collect_pool(n) into node+0xB0 and leave the engine's own powershare (rec+0x2C)
// alone, so the engine's pass 10 computes rec.total = pool x powershare for every collector.
// The check is therefore: predict Sigma_n pool(n) x pf(C,n) at tick N (right after our write,
// before pass 10 runs), then at tick N+1 read what pass 10 actually stored in rec.total and
// compare. Agreement to the milli-ducat proves the engine is dividing the MODEL's economy.
inline std::map<int, double> g_predicted;     // country index -> predicted Sigma total
inline int g_predict_tick = -1;

inline void predict_income(const std::vector<livetrade::SimNode>& sim,
                           const std::vector<std::string>& names,
                           const std::vector<double>& pool_written_monthly) {
    g_predicted.clear();
    auto byname = install::live_by_name(sim);
    for (int fn = 0; fn < (int)names.size() && fn < (int)pool_written_monthly.size(); fn++) {
        auto it = byname.find(names[fn]);
        if (it == byname.end()) continue;
        double pool = pool_written_monthly[fn];
        for (auto& rec : livetrade::read_standings(sim[it->second].obj)) {
            if (rec.power_fraction <= 0) continue;          // engine pays only its collectors
            g_predicted[livetrade::country_index_of(rec.tag_index)] += pool * rec.power_fraction;
        }
    }
}

// read back what pass 10 actually stored, and report the reconciliation
inline void predict_income_from_model(const std::vector<double>& pool_written_monthly) {
    g_predicted.clear();
    for (int fn = 0; fn < (int)install::g_share_by_node.size() && fn < (int)pool_written_monthly.size(); fn++)
        for (auto& [cidx, sh] : install::g_share_by_node[fn]) g_predicted[cidx] += pool_written_monthly[fn] * sh;
}

inline void verify_income(const std::vector<livetrade::SimNode>& sim, std::ofstream& lg) {
    // The engine's OWN paid trade income, read before anything else -- this is what E3 compares
    // between a modded run and an unmodded null run, so it must be measured even when the model
    // predicted nothing (pgt.NOWRITE: the mod observes, the engine's vanilla division stands).
    std::map<int, double> actual;
    for (auto& s : sim)
        for (auto& rec : livetrade::read_standings(s.obj)) {
            if (rec.total == 0) continue;
            actual[livetrade::country_index_of(rec.tag_index)] += rec.total;
        }
    {   // E3: world total + the biggest earners, comparable across runs at the same date. Spec 2.8
        // makes the DISTRIBUTION across the great powers the gating metric, not the world total.
        std::vector<std::pair<double, int>> top;
        for (auto& [c, v] : actual) top.push_back({v, c});
        std::sort(top.begin(), top.end(), [](auto& a, auto& b) { return a.first > b.first; });
        double world = 0; for (auto& [v, c] : top) world += v;
        lg << "[E3/top] countries=" << top.size() << " world=" << world << " top:";
        for (size_t i = 0; i < top.size() && i < 8; i++) lg << " #" << top[i].second << "=" << top[i].first;
        lg << (char)10;
    }
    if (g_predicted.empty()) return;
    int checked = 0, agree = 0;
    double worst = 0; int worst_c = -1;
    for (auto& [c, pred] : g_predicted) {
        auto a = actual.find(c);
        double got = (a == actual.end()) ? 0.0 : a->second;
        double d = std::fabs(got - pred);
        checked++;
        if (d <= 0.002 + 0.001 * checked) agree++;       // milli-ducat grid, per-node rounding
        if (d > worst) { worst = d; worst_c = c; }
    }
    lg << "[E1] engine-divided income vs model prediction: " << agree << "/" << checked
       << " countries agree; worst |diff| = " << worst << " ducats (country #" << worst_c << ")\n";
    // a few named samples
    int shown = 0;
    for (auto& [c, pred] : g_predicted) {
        auto a = actual.find(c);
        double got = (a == actual.end()) ? 0.0 : a->second;
        if (pred < 0.5) continue;
        lg << "     country#" << c << " predicted=" << pred << " engine=" << got
           << " diff=" << (got - pred) << "\n";
        if (++shown >= 6) break;
    }
}

// The whole model write, driven from live memory. Called on the game's own thread inside the
// monthly update. Returns the number of nodes written.
// The active orientation (Phi_w, or the selected good's graph) installed into the engine.
// Extracted so BOTH the monthly tick and the per-frame hook can call it: selecting a good
// must redraw the map immediately, not on the next month boundary. The generation/view
// guard inside makes it idempotent, so calling it every frame costs one comparison.
inline void install_active_orientation() {
// ---- INSTALL THE ACTIVE ORIENTATION (spec 1.12) -----------------------------------------
// The drawn graph is Phi_w in the aggregate view and THE SELECTED GOOD'S GRAPH in a per-good
// view -- 1.12 "redirects the arrow layer to that good's graph". It therefore has to be
// re-installed when the VIEW changes and not only when the solver publishes a new generation,
// because selecting a good does not advance the generation. This also has to run after
// viewmode::poll, which is why it no longer lives in the adopt block above.
if (livetrade::marker_present("ARROWS") &&
    (g_plan.generation != g_installed_gen || viewmode::g_selected != g_installed_view)) {
    const std::vector<std::pair<int, int>>& active =
        (viewmode::per_good() && viewmode::g_selected < (int)g_plan.graphs.size())
            ? g_plan.graphs[viewmode::g_selected] : g_plan.phi_w;
    std::map<std::string, int> name_to_id;
    for (auto& [id, nm] : install::g_id_to_name) name_to_id[nm] = id;
    std::set<std::pair<int, int>> desired;
    for (auto& [u, v] : active) {
        if (u >= (int)g_plan.names.size() || v >= (int)g_plan.names.size()) continue;
        auto a = name_to_id.find(g_plan.names[u]);
        auto b = name_to_id.find(g_plan.names[v]);
        if (a == name_to_id.end() || b == name_to_id.end()) continue;
        desired.insert({a->second, b->second});
    }
    {   // name the links whose drawn direction changed (F1 wants it findable by eye)
        std::set<std::pair<int, int>> prev;
        for (auto& [u, v] : g_plan.phi_w_prev) prev.insert({u, v});
        std::ofstream lg3(g_log, std::ios::app);
        for (auto& [u, v] : active)
            if (prev.count({v, u}))
                lg3 << "[flip] " << g_plan.names[v] << " -> " << g_plan.names[u]
                    << "  became  " << g_plan.names[u] << " -> " << g_plan.names[v] << "\n";
    }
    // REORIENT THE DEFINITION GRAPH -- what drives the node window's tabs AND the arrows.
    int relinked = -1;
    if (livetrade::marker_present("RELINK")) {
        std::ofstream lgr(g_log, std::ios::app);
        auto sim_now = livetrade::read_sim_nodes();      // needed for the steer clamp
        std::set<std::pair<std::string, std::string>> want;
        for (auto& [u, v] : active)
            if (u < (int)g_plan.names.size() && v < (int)g_plan.names.size())
                want.insert({g_plan.names[u], g_plan.names[v]});
        if (relink::capture(lgr)) {
            relinked = relink::apply(want, lgr, sim_now);
            if (livetrade::marker_present("LISTDUMP"))
                relink::dump_lists(g_log, {"baltic_sea", "novgorod", "lubeck"});
        }
    }
    int flipped = livetrade::marker_present("RELINK") ? relinked
                                                      : arrows::set_directions(desired);
    // REBUILD THE LAYER ON EVERY INSTALL, not only when `flipped > 0`: relink returns links
    // reversed vs the FILE declaration, not vs the previous install, so leaving a per-good view
    // for the aggregate is "0 reversed" while every one of those polylines just changed back.
    // Gating on it left the old view's ribbons on screen -- both directions at ivory_coast/cape,
    // artifacts at mexico/california -- surviving ticks, because an unchanged view skips this
    // whole block (user, 2026-08-27).
    bool rebuilt = arrows::rebuild();
    arrows::mark_dirty();
    // THE ENGINE'S REACHABILITY MATRICES FOLLOW THE GRAPH. CTradeManager+0x88/+0x90/+0x98 are three
    // per-country x per-node byte tables (upstream-of-home, plus merchant cones, plus the powered
    // variant) rebuilt ONLY by 0xB4DB00, which the monthly driver calls at 0xB4BD0A -- BEFORE our
    // hook rewrites the definitions. Stale tables made every steer button read STEER_LATER ("You
    // cannot direct trade after it has passed your home") for the rest of the month (user), and
    // 0xB596E0 SetTrader / the steer command's CanExecute (0x5DA4F0) gate on the same bytes. The
    // rebuild is idempotent (memset + BFS over the definitions' incoming vectors), writes only
    // those four fields, and is the engine's own call on load/new game/tag change (reviewed).
    {   // same reasoning as the layer rebuild above: the definitions changed whenever this block
        // ran at all, and `flipped` does not measure that. The rebuild is idempotent and cheap.
        uintptr_t mgr = livetrade::trade_manager();
        // the engine's rebuild restores its own BFS into A/B/C: re-apply BOTH overlays (spec 1.10's
        // matrix B, and the model's matrix C) or they hold only until the next rebuild (reviewed)
        // FILL_REBUILD, not the default: B legitimately holds the engine's BFS the instant after a
        // rebuild, so sampling it here counted our own correction as a gate lapse and inflated the
        // rate (this alone accounted for most of a measured "27% of polls").
        if (mgr) { ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + 0xB4DB00))(mgr); g_reach_rebuilt++; gates::fill_b(mgr, gates::FILL_REBUILD); apply_matrix_c(); }
    }
    homeward::g_reach_dirty = true;   // the dispatch that follows lands merchants: the frame poll rebuilds once more after the tick
    g_installed_gen  = g_plan.generation;
    g_installed_view = viewmode::g_selected;
    std::ofstream lg2(g_log, std::ios::app);
    lg2 << "[arrows] view=" << (viewmode::per_good() ? viewmode::g_selected_name
                                                    : std::string("AGGREGATE"))
        << " edges=" << active.size() << " re-oriented " << flipped
        << " drawn routes, layer rebuild "
        << (rebuilt ? "OK" : "SKIPPED (map renderer not captured yet)") << "\n";
    {   // THE INSTALLED ORIENTATION'S END NODES, every time the orientation changes (F1/F2/F5).
        // A sink is a node the active graph gives no outgoing edge. F2 ("raze China moves the
        // end") and F5 ("a price crash spreads a market") are stated as claims about THIS set,
        // and F1 wants the flip visible end-to-end; the [flip] lines above name the links, this
        // names the resulting poles. Cheap: one pass over the edge list per orientation install.
        std::vector<char> has_out(g_plan.N, 0);
        for (auto& [u, v] : active) if (u >= 0 && u < g_plan.N) has_out[u] = 1;
        std::string ends; int n_ends = 0;
        for (int n = 0; n < g_plan.N; n++)
            if (!has_out[n]) { n_ends++; if (n < (int)g_plan.names.size()) ends += g_plan.names[n] + " "; }
        lg2 << "[ends] " << (viewmode::per_good() ? viewmode::g_selected_name : std::string("Phi_w"))
            << " sinks=" << n_ends << " { " << ends << "}" << (char)10;
    }
}
}

// Per-frame: pick up a view change and re-install the orientation immediately. Spec 1.12's
// province click has to feel instant; waiting for the monthly tick would make the map lag a
// month behind the selection.
// D3 probe read-back: (record, label) of the probe node's top receivers, read again at the START of the
// next tick before any write -- tells whether the engine rewrites rec+0x40 between our ticks
inline std::vector<std::pair<uintptr_t, std::string>> g_probe_recs;
inline std::map<uintptr_t, std::pair<int32_t, int32_t>> g_probe_last;   // rec -> (+0x48, +0x40) last seen by the frame hook
inline uint64_t g_probe_frames = 0;                                        // frames since the last tick's write
inline void probe_frame(std::ofstream* lg) {
    if (g_probe_recs.empty() || !lg) return;
    g_probe_frames++;
    for (auto& [rec, who] : g_probe_recs) {
        if (!livetrade::validate_region(rec, 0xC0)) continue;
        int32_t v48 = livetrade::fi(rec + 0x48), v40 = livetrade::fi(rec + 0x40);
        auto it = g_probe_last.find(rec);
        if (it == g_probe_last.end()) { g_probe_last[rec] = {v48, v40}; continue; }
        if (it->second.first != v48 || it->second.second != v40) {
            *lg << "  [d3/probe] frame-change " << who << ": +0x48 " << it->second.first << " -> " << v48 << "  +0x40 " << it->second.second << " -> " << v40
                << "  (frame " << g_probe_frames << " after the tick's write; +0xAE=" << (int)livetrade::fb(rec + 0xAE) << " +0xA8=" << livetrade::fi(rec + 0xA8) << ")" << (char)10;
            it->second = {v48, v40};
        }
    }
}

// THE FIRST TICK RUNS AT ATTACH (user rule, 2026-08-26): the model acts on the monthly trade
// driver, so a new campaign spent its first month in vanilla's state (merchants collecting) and
// its second with the opening re-placements settling. The engine's own game-setup path (0x773B20,
// from 0x81AC47) calls that same driver 0xB4BA90(manager) once after loading everything, so
// calling it here -- as soon as the solver has published an orientation, before the player has
// unpaused -- is the engine's own init pattern: our hook inside it runs the whole tick 1 (the
// orientation install, the startup re-placement, every write) at 11 November 1444.
constexpr uintptr_t MONTHLY_TRADE_DRIVER = 0xB4BA90;
inline int  g_treasure_gen = -1;                          // ladder's last built generation; cleared per world
inline bool g_first_tick_done = false;
inline bool g_first_solve_requested = false;
inline std::atomic<bool> g_attach_done{false};   // every hook is in (dllmain): only then may the attach-time tick run
inline void first_tick_at_attach() {
    if (g_first_tick_done || g_ticks.load() > 0 || livetrade::marker_present("NOFIRSTTICK")) { if (g_ticks.load() > 0 || livetrade::marker_present("NOFIRSTTICK")) console::set_hold(false); return; }   // never release mid-setup (reviewed)
    if (!g_attach_done.load() || !g_hook.active || !nocollect::g_installed) return;   // the tick hook itself must be in (reviewed)
    // the solver reads the live world itself and solves on request; only the tick used to ask
    if (!g_first_solve_requested) { g_first_solve_requested = true; resolver::request();
        std::ofstream lg(g_log, std::ios::app); lg << "[firsttick] solve requested at attach" << (char)10; return; }
    resolver::Orientation o = resolver::snapshot();
    if (o.graphs.empty()) return;                       // the solver has not published yet
    uintptr_t mgr = livetrade::trade_manager();
    if (!mgr) return;
    g_first_tick_done = true;
    { std::ofstream lg(g_log, std::ios::app); lg << "[firsttick] orientation gen " << o.generation << " published: running the monthly trade driver at attach" << (char)10; }
    money::g_suppress_pay = true;                      // a setup run: the engine's pass 10 must not pay a month's income (reviewed)
    ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + MONTHLY_TRADE_DRIVER))(mgr);
    money::g_suppress_pay = false;
    { std::ofstream lg(g_log, std::ios::app); lg << "[firsttick] done: tick counter now " << g_ticks.load() << (char)10; }
    console::set_hold(false);                         // now the run's commands may move the world
}

// EVERYTHING WORLD-KEYED, FORGOTTEN: a second campaign in the same process (new game -> menu -> load)
// reallocates the nodes and re-numbers the countries; the plan's naming half is rebuilt by the
// loading path, and these caches would otherwise carry campaign 1 into campaign 2 (reviewed).
inline void reset_world_state();
}
namespace earlyload { extern std::atomic<int> g_hits; extern std::atomic<int> g_opening_placements_skipped; }
namespace savegame { extern int g_written, g_restored, g_restore_missing, g_cleared; }

namespace ticklive {

// The display overlay: the view's numbers into the link records and node fields. `shown` is the
// selected good alone in a per-good view, all goods in the aggregate. Never writes the pool
// (+0xB0), never touches standings: pure display, safe to run any number of times per month.
inline int render_overlay(std::vector<livetrade::SimNode>& sim,
                          const std::vector<econ::GoodFlow>& per_good,
                          const std::vector<std::vector<double>>& inj_field,
                          bool tick_owns_pool) {
    std::vector<econ::GoodFlow> shown = per_good;
    std::vector<std::vector<double>> shown_inj = inj_field;
    // ONE load of the selection. viewmode::poll runs on the frame thread OUTSIDE this path's
    // exclusion and clears g_selected to -1 when the window closes, so re-reading it after the bounds
    // check let per_good[-1] through -- a GoodFlow read from before the vector, then copy-constructed
    // (reviewed). Both containers are bounds-checked: they are parallel by construction, but the
    // check belongs on the one being subscripted.
    const int sel = viewmode::g_selected;
    bool pg = viewmode::per_good() && sel >= 0
              && sel < (int)per_good.size() && sel < (int)inj_field.size();
    if (pg) {
        shown.assign(1, per_good[sel]);
        shown_inj.assign(1, inj_field[sel]);
    }
    auto agg   = econ::aggregate(g_plan.N, shown, shown_inj);
    auto gross = econ::gross_link_flows(shown);                  // WITH steering bonus
    auto away  = econ::directed_flows_no_bonus(shown);           // per-mille shares (see apply)
    outlinks::install_incoming(sim, g_plan.names, gross, install::g_id_to_name);
    outlinks::install(sim, g_plan.names, away, install::g_id_to_name);
    linkvalue::install(sim, g_plan.names, gross, install::g_id_to_name);
    int wrote = install::install_aggregate(sim, g_plan.names, agg, pg, /*write_pool=*/tick_owns_pool);
    // D3 (TESTING.md): the good's sinks and their collected_share, checkable without a click
    if (pg && !shown.empty()) {
        const econ::GoodFlow& gf = shown[0];
        std::ofstream ld(g_log, std::ios::app);
        int sinks = 0, full = 0;
        std::string list;
        for (int n = 0; n < g_plan.N && n < (int)gf.is_sink.size(); n++) {
            if (!gf.is_sink[n]) continue;
            sinks++;
            double cs = n < (int)gf.collected_share.size() ? gf.collected_share[n] : 0.0;
            if (cs >= 0.999999) full++;
            char b[160]; snprintf(b, sizeof b, " %s(in=%.3f cs=%.3f)", g_plan.names[n].c_str(),
                     n < (int)gf.incoming.size() ? gf.incoming[n] / 12.0 : 0.0, cs);
            list += b;
        }
        ld << "[D3] view=" << viewmode::g_selected_name << " sinks=" << sinks << " with collected_share==1: "
           << full << " |" << list << (char)10;
    }
    return wrote;
}

// The frame-poll render: everything a view switch changes, nothing a month changes. Runs under
// the g_inside exclusion (the caller holds it), so it can never overlap the tick's apply().
inline void render_view() {
    if (!g_plan.ready) return;
    std::vector<econ::GoodFlow> per_good;
    std::vector<std::vector<double>> inj_field;
    std::map<std::string, double> eng_local;
    {
        std::lock_guard<std::mutex> lk(g_render_mx);
        if (!g_render_valid) return;                  // no tick yet: retried next poll
        per_good = g_r_per_good; inj_field = g_r_inj; eng_local = g_r_engine_local;
    }
    livetrade::TickCacheScope tick_cache;
    LARGE_INTEGER f, t0, t1; QueryPerformanceFrequency(&f); QueryPerformanceCounter(&t0);
    auto sim = livetrade::read_sim_nodes();
    if (sim.empty()) return;
    for (auto& s2 : sim) {
        auto it = install::g_id_to_name.find(s2.index);
        if (it != install::g_id_to_name.end()) s2.name = it->second;
    }
    // the ENGINE's own local is the baseline every render starts from: a per-good pass overwrote
    // +0xB4, put it back before anything derives held/outgoing from it (review defect: the stale
    // per-good local collapsed held/outgoing/pool for the rest of the month)
    for (auto& s2 : sim) {
        auto it = eng_local.find(s2.name);
        if (it == eng_local.end()) continue;
        s2.local_value = it->second;
        livetrade::write_local_value(s2.obj, it->second);
    }
    install_active_orientation();                     // relink + arrows for the new view
    int wrote = render_overlay(sim, per_good, inj_field, /*tick_owns_pool=*/false);
    g_rendered_view = viewmode::g_selected;
    QueryPerformanceCounter(&t1);
    double ms = f.QuadPart ? (double)(t1.QuadPart - t0.QuadPart) * 1000.0 / f.QuadPart : 0.0;
    std::ofstream lv(g_log, std::ios::app);
    lv << "[view] rendered " << (viewmode::per_good() ? viewmode::g_selected_name : std::string("AGGREGATE"))
       << " from the frame: " << wrote << " nodes, " << (int)ms << " ms (display only)" << (char)10;
}

// IS THERE ACTUALLY A WORLD? The trade manager is G+0x2198, a process-lifetime sub-object, so a
// non-null manager says nothing: at the menu and mid-load its node array is dangling while the
// pointer still reads back. Anything that writes engine memory from the frame poll must ask this
// first (reviewed).
inline bool world_alive(uintptr_t mgr) {
    if (!mgr) return false;
    if (!livetrade::validate_region(mgr + 0x18, 8) || !livetrade::fq(mgr + 0x18)) return false;
    if (!livetrade::validate_region(mgr + 0x24, 4) || livetrade::fi(mgr + 0x24) <= 0) return false;
    return true;
}

inline void frame_view_poll() {
    if (!g_plan.ready) return;
    if (g_inside.load()) return;                        // the loading-time tick runs on another thread: never overlap apply()
    first_tick_at_attach();
    // The render path below MAY install the orientation from here -- but only under the g_inside
    // exclusion the tick handler itself takes, and only via render_view() (display writes alone).
    // An UNGUARDED install from the frame raced the loading-thread tick through relink/arrows and
    // crashed; a full apply() from here double-ran the D3 propagation (the i37 power ratchet).
    {   // an in-session campaign change -- primary signal: the engine truncated logs/game.log
        // (fires on EVERY campaign start); secondary: node-array identity (see arm_world_identity)
        if (!g_gamelog_path.empty()) {
            WIN32_FILE_ATTRIBUTE_DATA fad{};
            long long sz = GetFileAttributesExA(g_gamelog_path.c_str(), GetFileExInfoStandard, &fad)
                ? (((long long)fad.nFileSizeHigh << 32) | fad.nFileSizeLow) : -1;
            if (g_gamelog_last >= 0 && sz >= 0 && sz < g_gamelog_last && !g_saw_no_world.load()) {
                std::ofstream lg(g_log, std::ios::app);
                lg << "[world] game.log truncated (" << g_gamelog_last << " -> " << sz
                   << " bytes): a campaign launch happened; resetup at the next live-world poll" << (char)10;
                g_saw_no_world = true;
            }
            g_gamelog_last = sz;
        }
        uintptr_t now_mgr = livetrade::trade_manager();
        if (now_mgr && g_resetup_inline && g_world_cnt.load() > 0) {   // only once a plan is armed
            uintptr_t cur_nb = livetrade::validate_region(now_mgr + 0x18, 8) ? livetrade::fq(now_mgr + 0x18) : 0;
            int cur_cnt = livetrade::validate_region(now_mgr + 0x24, 4) ? livetrade::fi(now_mgr + 0x24) : 0;
            if (cur_nb == 0 || cur_cnt <= 0) {
                g_saw_no_world = true;                  // at the menu / world torn down: remember the gap
            } else {
                // the node KEYS are the identity that survives pointer/count reuse (see world_fingerprint).
                // Only computed when the cheap checks did not already decide -- and it is what catches an
                // in-session NEW GAME whose world happens to share the old shape.
                uint64_t cur_fp = world_fingerprint(now_mgr);
                int cur_date = engine_date(); int last_date = g_world_date.load();
                bool date_jump = (cur_date > 0 && last_date > 0 &&
                                  (cur_date < last_date - DATE_BACK_TOL || cur_date - last_date > DATE_JUMP_FWD));
                bool changed = g_saw_no_world.load() || date_jump
                            || cur_nb != g_world_nb.load() || cur_cnt != g_world_cnt.load()
                            || (cur_fp != 0 && cur_fp != g_world_fp.load());
                if (changed) {
                    bool expected = false;
                    if (g_inside.compare_exchange_strong(expected, true)) {
                        { std::ofstream lg(g_log, std::ios::app);
                          lg << "[world] identity changed under a ready plan (date " << last_date << "->" << cur_date
                             << " nb " << std::hex << g_world_nb.load() << "->" << cur_nb
                             << " fp " << g_world_fp.load() << "->" << cur_fp << std::dec << " cnt " << g_world_cnt.load() << "->" << cur_cnt
                             << " saw_no_world=" << g_saw_no_world.load() << "): campaign change, rerunning setup" << (char)10; }
                        g_resetup_inline(now_mgr);      // finish_setup: reset_world_state + full re-derive + re-arm
                        g_inside = false;
                    }
                    return;                             // nothing below may touch the new world yet
                }
                if (cur_date > 0) g_world_date = cur_date;   // roll the last-seen date forward (normal play)
            }
        }
    }
    {   // spec 1.10 must hold after ANY rebuild, including the engine's own call sites (a save
        // load goes through several we do not control): refill matrix B here too.
        // A TORN-DOWN WORLD leaves the manager live but its node array dangling: mgr is G+0x2198, a
        // process-lifetime sub-object, so a non-null manager is NOT evidence that a world exists
        // (reviewed -- the branch above latches g_saw_no_world and falls through to here). And the
        // tick can be inside the engine's non-reentrant rebuild on another thread, so this takes the
        // same exclusion the render path below does.
        uintptr_t mgr_b = livetrade::trade_manager();
        if (world_alive(mgr_b)) {
            bool expected = false;
            if (g_inside.compare_exchange_strong(expected, true)) {
                gates::fill_b(mgr_b, gates::FILL_FRAME);
                g_inside = false;
            }
        }
    }
    selprov::frame();                                   // the province click -> its good's view (selprov.h)
    {   // INSTANT VIEW SWITCH: the click (or the pgt.VIEW marker) changed the selection; render the
        // display from the last tick's cache NOW, paused included, under the tick's own exclusion.
        viewmode::poll(g_plan.good_names);
        if (viewmode::g_selected != g_rendered_view.load()) {
            bool expected = false;
            if (g_inside.compare_exchange_strong(expected, true)) {   // never while a tick runs; retried next poll
                render_view();
                g_inside = false;
            }
        }
    }
    viewmode::poll(g_plan.good_names);
    colorview::sync(viewmode::per_good() ? viewmode::g_selected_name : std::string());   // per-good producers colored, rest gray; vanilla back on close
    { std::ofstream ip(g_log, std::ios::app); igiprobe::frame(&ip); }   // D1 probe, two-phase (igiprobe.h); inert without its markers
    if (!g_probe_recs.empty()) { std::ofstream pf(g_log, std::ios::app); probe_frame(&pf); }   // D3 probe: who rewrites the record between our ticks
    if (transfertext::g_installed) transfertext::frame();               // node window: rebuild the transfer text when the table's target changes
    // MERCHANT LANDINGS REFRESH THE ENGINE'S REACHABILITY TABLES. 0xB4DB00 skips a merchant in transit
    // (envoy+0x10 == 0), so every merchant that lands after the monthly rebuild -- all of the opening
    // re-placements -- read STEER_LATER on its panels until the next month (user). Coalesced: one call
    // per frame at most, on the game thread, never inside the tick (the tick rebuilds itself).
    if (homeward::g_reach_dirty && g_ticks.load() > 0) {
        uintptr_t mgr = livetrade::trade_manager();
        if (world_alive(mgr)) {
            bool expected = false;
            if (g_inside.compare_exchange_strong(expected, true)) {   // 0xB4DB00 is NOT reentrant and the
                homeward::g_reach_dirty = false;                      // tick calls it too; clear the request
                ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + 0xB4DB00))(mgr);
                g_reach_rebuilt++; g_reach_rebuilt_frame++;
                gates::fill_b(mgr, gates::FILL_REBUILD);              // engine content here is expected, not a lapse
                apply_matrix_c();
                g_inside = false;
            }
        }
    }

    // Reverse-direction map panels, driven from the frame hook (render thread, inside the frame).
    if (livetrade::marker_present("REVPANEL")) {
        std::ofstream rp(g_log, std::ios::app);
        revpanel::frame_tick(&rp);
    }

    // (reverse map panels install as a hook on the layer rebuild -- see revpanel.h;
    //  calling them from here ran before the rebuild and off its render phase)

    // pgt.OPENNODE holding a node name opens that node's window from here. It lives on the FRAME
    // hook, not the monthly tick: the game is usually PAUSED while inspecting a node window, and
    // a paused game never ticks -- the same trap that made console commands unreachable.
    if (livetrade::marker_present("OPENNODE")) {
        std::string path = livetrade::self_dir() + "\\" + "pgt.OPENNODE";
        std::string want;
        { std::ifstream f(path); std::getline(f, want); }
        while (!want.empty() && (want.back()=='\r' || want.back()=='\n' || want.back()==' '))
            want.pop_back();
        DeleteFileA(path.c_str());
        if (!want.empty()) {
            uintptr_t target = 0;
            for (auto& s2 : livetrade::read_sim_nodes()) {
                auto it = install::g_id_to_name.find(s2.index);
                if (it != install::g_id_to_name.end() && it->second == want) { target = s2.obj; break; }
            }
            std::string oe; bool ok = alledges::open_node(target, &oe);
            std::ofstream lg(g_log, std::ios::app);
            lg << "  [opennode] " << want << " -> " << (ok ? "opened" : ("FAILED: " + oe)) << "\n";;
        }
    }
}

inline int apply(uintptr_t mgr) {
    // PHASE PROFILE (H3): where the monthly cost goes. Marks are cumulative ms since apply() began.
    livetrade::TickCacheScope tick_cache;   // fast validate_region for the duration of apply() only
    LARGE_INTEGER ph_f, ph_t0, ph_t; QueryPerformanceFrequency(&ph_f); QueryPerformanceCounter(&ph_t0);
    std::string ph_line;
    auto PH = [&](const char* name) { QueryPerformanceCounter(&ph_t); ph_line += std::string(" ") + name + "=" + std::to_string((int)(1000.0 * (double)(ph_t.QuadPart - ph_t0.QuadPart) / (double)ph_f.QuadPart)); };
    if (!g_plan.ready) return 0;
    if (!g_probe_recs.empty()) {
        std::ofstream lp0(g_log, std::ios::app);
        for (auto& [rec, who] : g_probe_recs)
            if (livetrade::validate_region(rec, 0xC0))
                lp0 << "  [d3/probe] tick-start read-back " << who << ": key=" << std::hex << (unsigned)livetrade::fi(rec + 0x14) << std::dec << " +0x40=" << livetrade::fi(rec + 0x40)
                    << " +0x48=" << livetrade::fi(rec + 0x48) << " +0x28=" << livetrade::fi(rec + 0x28) << " +0xAE=" << (int)livetrade::fb(rec + 0xAE) << (char)10;
    }
    // Adopt a newly published orientation, if the background solver produced one since the last
    // tick. The swap is whole-orientation: a tick never mixes old and new graphs.
    {
        resolver::Orientation o = resolver::snapshot();
        if (!o.graphs.empty() && o.generation != g_plan.generation) {
            g_plan.graphs = o.graphs;
            g_plan.slots  = o.slots;
            g_plan.prices = o.prices;
            g_plan.good_names = o.good_names;
            g_plan.reach  = o.reach;
            g_plan.phi_w_prev = g_plan.phi_w;
            g_plan.phi_w  = o.phi_w;
            g_plan.generation = o.generation;
            std::ofstream lg(g_log, std::ios::app);
            lg << "[tick] adopted orientation gen " << o.generation << "\n";
        }
    }
    // ask the background solver to recompute for next month (never blocks the game thread)
    resolver::request();
    auto sim = livetrade::read_sim_nodes();
    if (sim.empty()) return 0;
    // name the live nodes by engine id (the map was resolved at attach and keyed by stable id)
    for (auto& s : sim) {
        auto it = install::g_id_to_name.find(s.index);
        if (it != install::g_id_to_name.end()) s.name = it->second;
    }
    // Console commands queued by the harness, run on the GAME THREAD before anything reads the
    // world, so this tick's solve already sees whatever the command changed.
    if (!frame::active()) console::drain(g_log);   // frame hook owns this when installed
    shock::maybe_apply(g_log, sim, install::g_id_to_name);
    int gc = 0, matched = 0;
    auto inject = install::gather_inject(sim, g_plan.names, gc, matched);
    std::map<int, std::vector<int>> collect_nodes;
    PH("standings");
    {   // H1 fingerprint: an order-independent hash of the installed Phi_w, by node NAME, so a
        // save/reload at the same date can be compared bit-for-bit across processes.
        std::vector<std::string> es;
        for (auto& [u, v] : g_plan.phi_w) if (u < (int)g_plan.names.size() && v < (int)g_plan.names.size()) es.push_back(g_plan.names[u] + ">" + g_plan.names[v]);
        std::sort(es.begin(), es.end());
        uint64_t h = 1469598103934665603ull;
        for (auto& e0 : es) for (unsigned char ch : e0) { h ^= ch; h *= 1099511628211ull; }
        std::ofstream lh(g_log, std::ios::app);
        lh << "[H1] date=" << engine_date() << " gen " << g_plan.generation << ": Phi_w edges=" << es.size() << " hash=" << std::hex << h << std::dec << (char)10;
    }
    {   // the ENGINE's live outgoing lists, this tick -- the graph it propagated along and the array
        // its steer ordinals index (reviewed: the attach-time list was stale after every relink)
        int links_seen = 0;
        auto lt = install::live_link_targets(g_plan.names, install::g_id_to_name, links_seen);
        if (links_seen > 0) g_plan.link_targets = lt;
    }
    auto st = install::read_standings_field(sim, g_plan.names, g_plan.link_targets, collect_nodes);
    // spec 1.7: merchants assigned to a link END the engine has no index for (a link drawn INTO
    // this node) live in our own table and are merged on top of the engine's own assignments.
    assign::poll(g_log);
    int assigned = assign::merge(st, g_plan.names);
    // ...and the engine records are made to say the same, so the map draws what is routed
    { std::ofstream lsr(g_log, std::ios::app); syncrec::apply(sim, &lsr); }
    // The table's contents, by node pair, so a claim like "rheinland-saxony carries merchants on
    // both ends" is read off the log rather than inferred from counters. Once a year.
    if (g_ticks.load() >= 4 && g_ticks.load() <= 8) {
        std::ofstream lt(g_log, std::ios::app);
        std::map<std::pair<std::string, std::string>, int> by_edge;
        for (auto& [key, target] : assign::g_table) by_edge[{key.second, target}]++;
        lt << "  [table] " << assign::g_table.size() << " placements on " << by_edge.size()
           << " directed ends; merge applied=" << assign::g_merge_applied
           << " noname=" << assign::g_merge_noname << " (e.g. " << assign::g_merge_noname_example << ")"
           << " kept_collector="
           << assign::g_merge_kept_collector << " added_new=" << assign::g_merge_added
           << "; flagfix: forward-#0 panels inspected=" << flagfix::g_inspected << " shields seen=" << flagfix::g_shields << " removed=" << flagfix::g_cleared << " | reverse panels updated=" << flagfix::g_rev_panels << " with shields=" << flagfix::g_rev_with_shields << " total shields=" << flagfix::g_rev_shields << " removed-off-panel=" << flagfix::g_rev_removed << " added-from-table=" << flagfix::g_rev_added << " tooltip-keyed=" << flagfix::g_rev_tooltip_set << " | steer_button clicks seen=" << clickfix::g_clicks << " reverse=" << clickfix::g_reverse_clicks
           << (char)10;
        for (auto& [e, n] : by_edge)
            lt << "     " << e.first << " -> " << e.second << " : " << n << " merchant(s)" << (char)10;
    }
    if (assigned && (g_ticks.load() % 12) == 0) {
        std::ofstream la(g_log, std::ios::app);
        la << "  [assign] " << assigned << " DLL-owned merchant assignments active\n";
    }

    std::vector<econ::GoodFlow> per_good;

    auto pp_at = econ::pp_index(g_plan.N, st);                     // D3: provincial power by node and country
    {   // DEPARTURE D3: remove what the ENGINE propagated along the graph it is running -- the installed
        // orientation (Phi_w, or the selected good's graph in a per-good view), NOT the attach-time link
        // list (reviewed: relink moves entries between definitions on every flip). Signed: a deficit
        // (subject transfers) is carried into the per-good power and clamped there.
        // the engine propagated along ITS outgoing lists (refreshed above); subtract along the same
    const std::vector<std::vector<int>>& downs = g_plan.link_targets;
    for (int fn = 0; fn < g_plan.N && fn < (int)st.size(); fn++)
            for (auto& e : st[fn].entries) { e.own = e.power - econ::prop_from(pp_at, downs[fn], e.country); e.has_own = true; }
}
{   // D3 v2: the fifth split among each node's neighbours by price-weighted goods, along each good's graph
    auto split = econ::propagation_split(g_plan.N, g_plan.graphs, g_plan.prices);
    auto recv  = econ::propagation_received(g_plan.N, pp_at, split);
    double s_val = 0, s_own = 0, s_pp = 0, s_recv = 0;
    for (int fn = 0; fn < g_plan.N && fn < (int)st.size(); fn++) { for (auto& e : st[fn].entries) { s_val += e.power; s_own += e.own; s_pp += e.pp; } if (fn < (int)recv.size()) for (auto& [c, r] : recv[fn]) s_recv += r; }
    int added  = econ::apply_split_propagation(g_plan.N, st, recv);
    double s_after = 0; for (int fn = 0; fn < g_plan.N && fn < (int)st.size(); fn++) for (auto& e : st[fn].entries) s_after += e.power;
    int wrote_p = livetrade::marker_present("NOWRITE") ? 0 : install::write_power_to_records(sim, g_plan.names, st);
    std::ofstream lp(g_log, std::ios::app);
    lp << "  [d3] split propagation: " << added << " standings added where a country receives power it had none of; " << wrote_p << " record powers written" << (char)10;
    lp << "  [d3/sum] Sval(engine)=" << s_val << " Sown=" << s_own << " Srecv=" << s_recv << " Spp=" << s_pp << " Sval(model)=" << s_after << "   (a ratchet would show Sval(engine) rising by ~Srecv tick over tick with Spp flat)" << (char)10;
    // PROBE (pgt.D3PROBE = node name): who receives what there
    if (livetrade::marker_present("D3PROBE")) {
        std::string want; { std::ifstream f(livetrade::self_dir() + std::string(1, (char)92) + "pgt.D3PROBE"); std::getline(f, want); }
        while (!want.empty() && (want.back() == (char)13 || want.back() == (char)10 || want.back() == (char)32)) want.pop_back();
        for (int fn = 0; fn < g_plan.N; fn++) if (g_plan.names[fn] == want) {
            lp << "  [d3/probe] " << want << ": neighbours receiving from here ";
            for (auto& [n2, sh] : split[fn]) lp << g_plan.names[n2] << "=" << sh << " ";
            lp << (char)10 << "  [d3/probe] " << want << ": received power by country: ";
            {   // the largest receivers, then every country whose trade capital is at a NEIGHBOUR (the user's test: Tunis at Genoa)
                std::vector<std::pair<double, int>> top; for (auto& [c, r] : recv[fn]) top.push_back({r, c});
                std::sort(top.begin(), top.end(), [](auto& a, auto& b) { return a.first > b.first; });
                for (size_t i = 0; i < top.size() && i < 12; i++) lp << "#" << livetrade::country_index_of(top[i].second) << "=" << top[i].first << " ";
                {   // what the engine's record holds right after our write (rec+0x40 is the tooltip's line)
                    g_probe_recs.clear();
                    auto byn = install::live_by_name(sim);
                    auto bit = byn.find(want);
                    uintptr_t nobj = bit == byn.end() ? 0 : sim[bit->second].obj;
                    uintptr_t rb = (nobj && livetrade::validate_region(nobj + 0x18, 16)) ? livetrade::fq(nobj + 0x18) : 0;
                    int rc = rb ? livetrade::fi(nobj + 0x24) : 0;
                    lp << (char)10 << "  [d3/probe] " << want << ": record read-back after the write: ";
                    for (size_t i = 0; i < top.size() && i < 4; i++) {
                        int idx = livetrade::country_index_of(top[i].second);
                        if (!rb || idx < 0 || idx >= rc) continue;
                        uintptr_t rec = rb + (uintptr_t)idx * 0xC0;
                        if (!livetrade::validate_region(rec, 0xC0)) continue;
                        { char kb[24]; snprintf(kb, sizeof kb, "%08x", (unsigned)livetrade::fi(rec + 0x14));
                          lp << "#" << idx << " key=" << kb << " +0x40=" << livetrade::fi(rec + 0x40) << " +0x48=" << livetrade::fi(rec + 0x48) << " +0xAE=" << (int)livetrade::fb(rec + 0xAE) << " standings:[";
                          for (auto& e : st[fn].entries) if ((e.country & 0xFFFF) == idx) { char eb[24]; snprintf(eb, sizeof eb, "%08x", (unsigned)e.country);
                              lp << " " << eb << " power=" << e.power << " own=" << e.own << " recv=" << e.received << " pp=" << e.pp << (e.merchant_floor ? " floor" : ""); }
                          lp << " ] recv-key:"; for (auto& [c, r] : recv[fn]) if ((c & 0xFFFF) == idx) { char rb2[24]; snprintf(rb2, sizeof rb2, "%08x", (unsigned)c); lp << " " << rb2 << "=" << r; }
                          lp << " | "; }
                        g_probe_recs.push_back({rec, want + " #" + std::to_string(idx)});
                        g_probe_last[rec] = {livetrade::fi(rec + 0x48), livetrade::fi(rec + 0x40)}; g_probe_frames = 0;
                    }
                }
                lp << (char)10 << "  [d3/probe] " << want << ": by trade capital of the neighbour countries: ";
                for (auto& [n2, sh] : split[fn]) for (auto& e : st[n2].entries) if (e.is_capital) {
                    auto rit = recv[fn].find(e.country); double r = rit == recv[fn].end() ? 0.0 : rit->second;
                    double now = 0; for (auto& e2 : st[fn].entries) if (e2.country == e.country) { now = e2.power; break; }
                    lp << g_plan.names[n2] << ":#" << livetrade::country_index_of(e.country) << " receives " << r << " (power here now " << now << ") ";
                }
            }
            lp << (char)10;
        }
    }
    }

    
    std::vector<std::vector<double>> inj_field;
    per_good.reserve(g_plan.graphs.size());
    for (size_t k = 0; k < g_plan.graphs.size(); k++) {
        std::vector<double> inj(g_plan.N, 0.0);
        int slot = g_plan.slots[k];
        if (slot < gc)
            for (int n = 0; n < g_plan.N; n++) inj[n] = inject[slot][n] * g_plan.prices[k];
        const std::vector<std::vector<char>>* R =
            k < g_plan.reach.size() ? &g_plan.reach[k] : nullptr;

        per_good.push_back(
            econ::route(g_plan.N, g_plan.graphs[k], inj, st, collect_nodes, 0.05, R));
        inj_field.push_back(std::move(inj));
    }

    // ONE-OFF DIAGNOSTIC: the collect/transfer split at north_sea, per good.
    //
    // Spec 1.8 says a country's power counts toward P_transfer(g) ONLY if it steers g here or
    // collects at a node reachable from here in g's graph; anything else is INERT for that good
    // and is excluded from BOTH sums. For livestock the whole reachable set from north_sea is
    // empty New World nodes, so every European standing should be inert, P_transfer should be 0,
    // and collected_share should be 1 -- Scotland (whose trade capital is north_sea) collects all
    // of it and nothing crosses the Atlantic. Print the actual numbers instead of reasoning about
    // them, including which countries land in which bucket.
    static int g_split_ticks = 0;
    if (g_split_ticks < 40) {
        g_split_ticks++;
        std::ofstream lgs(g_log, std::ios::app);
        // Which node to dissect comes from a marker (pgt.SPLIT holding a node key), re-read
        // every tick so a new suspect needs no rebuild. Defaults to north_sea.
        std::string want_node = "north_sea";
        if (livetrade::marker_present("SPLIT")) {
            std::ifstream mf(livetrade::self_dir() + "\\pgt.SPLIT");
            std::string ln;
            if (std::getline(mf, ln)) {
                while (!ln.empty() && (ln.back() == '\r' || ln.back() == '\n' || ln.back() == ' ')) ln.pop_back();
                if (!ln.empty()) want_node = ln;
            }
        }
        int ns = -1;
        for (int i = 0; i < (int)g_plan.names.size(); i++)
            if (g_plan.names[i] == want_node) { ns = i; break; }
        if (ns >= 0 && ns < (int)st.size()) {
            lgs << "  [split] tick " << g_split_ticks
                << " " << want_node << " standings (power, collects, steer_to):" << (char)10;
            for (auto& e : st[ns].entries) {
                if (e.power <= 0) continue;
                std::string tgt = "-";
                if (e.steer_to >= 0 && e.steer_to < (int)g_plan.names.size())
                    tgt = g_plan.names[e.steer_to];
                lgs << "     country#" << e.country << " power=" << e.power
                      << " collects=" << (e.collects ? "YES" : "no")
                    << " steers_to=" << tgt << (char)10;
            }
            for (size_t k = 0; k < per_good.size() && k < g_plan.graphs.size(); k++) {
                const auto& F = per_good[k];
                if (ns >= (int)F.p_collect.size()) continue;
                double v = F.value[ns], pc = F.p_collect[ns], pt = F.p_transfer[ns];
                if (v <= 0 && pc <= 0 && pt <= 0) continue;
                std::string gname = k < g_plan.good_names.size() ? g_plan.good_names[k] : "?";
                lgs << "     [" << gname << "] value=" << v
                      << " P_collect=" << pc << " P_transfer=" << pt
                      << " collected_share=" << F.collected_share[ns]
                      << " outgoing=" << F.outgoing[ns];
                // WHO is transfer-eligible here, and why. Replicates econ::route's own test so
                // the answer comes from the same inputs the router used.
                if (F.outgoing[ns] > 0.01 && k < g_plan.reach.size()) {
                    const auto& R = g_plan.reach[k];
                    std::vector<int> outs_here;
                    for (auto& e : g_plan.graphs[k]) if (e.first == ns) outs_here.push_back(e.second);
                    std::string arcs;
                    for (int m : outs_here)
                        arcs += (m < (int)g_plan.names.size() ? g_plan.names[m] : "?") + " ";
                    lgs << "        out-arcs: " << arcs << (char)10;
                    for (auto& e : st[ns].entries) {
                        if (e.power <= 0 || e.collects) continue;
                        bool steers = false;
                        for (int m : outs_here) if (m == e.steer_to) { steers = true; break; }
                        std::string why;
                        if (steers) why = "steers";
                        else {
                            auto cit = collect_nodes.find(e.country);
                            if (cit != collect_nodes.end())
                                for (int H : cit->second)
                                    if (H >= 0 && H < (int)R.size() && ns < (int)R.size() && R[ns][H]) {
                                        why = "collects at " +
                                              (H < (int)g_plan.names.size() ? g_plan.names[H] : "?");
                                        break;
                                    }
                        }
                        if (!why.empty())
                            lgs << "        ELIGIBLE country#" << e.country
                                << " power=" << e.power << " (" << why << ")" << (char)10;
                    }
                }
                auto it = F.flow[ns].begin();
                for (; it != F.flow[ns].end(); ++it)
                    if (it->second > 0 && it->first < (int)g_plan.names.size())
                        lgs << "  -> " << g_plan.names[it->first] << "=" << it->second;
                lgs << (char)10;
            }
        }
    }
    {   // spec 1.11: the treasure fleet's next-hop ladder, precomputed here so the engine-side
        // hook is a pure integer lookup inside the money path (treasure.h)
        // NOT a function-local static: a new campaign restarts generation numbering, so a stale
        // latch could skip the rebuild for the new world entirely (reviewed).
        if (treasure::g_installed && g_plan.generation != g_treasure_gen) {
            g_treasure_gen = g_plan.generation;
            treasure::rebuild(g_plan.N, g_plan.phi_w, g_plan.graphs, g_plan.link_targets,
                              install::g_id_to_name, g_plan.names);
        }
    }
    {   // J10: WHERE DO THE AI'S LIGHT SHIPS ACTUALLY SIT? A light ship protecting trade shows up as
        // ship_power on the node's own per-country record (rec+0x1C), so this needs no navy RE.
        // Classify every placement against the model: the country's HOME node, a node where it steers,
        // and -- the claim J10 makes -- a Phi_w-INCOMING (reverse) end. Vanilla's scorer is kept
        // deliberately (the user's call); it consumes the model's node values, shares and reach
        // (matrix C), so this measures whether the model's network moves the ships. Once a year.
        if ((g_ticks.load() % 12) == 1) {
            std::set<std::pair<int,int>> phi_in;            // (node, from): an arrow drawn INTO node
            for (auto& [u, v] : g_plan.phi_w) phi_in.insert({v, u});
            std::map<int,int> home_of;                      // country -> its home node
            std::map<std::pair<int,int>,int> steer_at;      // (country, NODE) -> the node steered to FROM there
            for (int fn = 0; fn < g_plan.N && fn < (int)st.size(); fn++)
                for (auto& e : st[fn].entries) {
                    // KEY BY THE BARE INDEX: standings carry the raw tag dword, the ship records
                    // carry the index. Mixing them made every placement fall through to "unsteered"
                    // (measured: home=0 on a world where ships are visibly at home nodes).
                    int ci = livetrade::country_index_of(e.country);
                    if (e.is_capital) home_of[ci] = fn;
                    // KEYED BY (country, node). Keying by country alone kept whichever node came last
                    // and then asked "is there an arrow into THIS node from the target it steers to
                    // somewhere ELSE" -- misclassifying every country with more than one merchant,
                    // i.e. every major power (reviewed).
                    if (e.steer_to >= 0) steer_at[{ci, fn}] = e.steer_to;
                }
            auto byname = install::live_by_name(sim);
            double tot = 0, at_home = 0, at_reverse = 0, at_steer = 0, elsewhere = 0;
            int placements = 0;
            for (int fn = 0; fn < g_plan.N && fn < (int)g_plan.names.size(); fn++) {
                auto it = byname.find(g_plan.names[fn]);
                if (it == byname.end()) continue;
                for (auto& r : livetrade::read_standings(sim[it->second].obj)) {
                    if (r.ship_power <= 0.0) continue;
                    int c = livetrade::country_index_of(r.tag_index);
                    tot += r.ship_power; placements++;
                    auto h = home_of.find(c);
                    if (h != home_of.end() && h->second == fn) { at_home += r.ship_power; continue; }
                    // Does this country steer FROM THIS node? The old test asked only whether it
                    // steered anywhere at all, and ANDed a record field (rec+0xA8) that syncrec writes
                    // as 0 on a reverse end and is 0 on ordinary records -- so ">= 0" was true almost
                    // always and nothing ever reached "elsewhere" (reviewed).
                    auto sv = steer_at.find({c, fn});
                    if (sv == steer_at.end()) { elsewhere += r.ship_power; continue; }
                    // A REVERSE END: the merchant here pushes fn -> sv->second while Phi_w draws that
                    // link sv->second -> fn, i.e. against the arrow.
                    if (phi_in.count({fn, sv->second})) at_reverse += r.ship_power;
                    else at_steer += r.ship_power;
                }
            }
            std::ofstream lj(g_log, std::ios::app);
            lj << "  [J10/ships] placements=" << placements << " power=" << tot
               << " home=" << at_home << " reverse-end=" << at_reverse
               << " other-steered=" << at_steer << " unsteered=" << elsewhere << (char)10;
        }
    }

    PH("routed");
    {   // F5 (a price crash spreads a market): one named good's SINKS and its alpha, every tick.
        // pgt.GOODSINKS holds a good name (default grain). A crash must widen this set toward the
        // populous regions rather than leave it concentrated -- the claim is about this list.
        std::string want = "grain";
        if (livetrade::marker_present("GOODSINKS")) {
            std::ifstream f(livetrade::self_dir() + std::string(1, (char)92) + "pgt.GOODSINKS");
            std::string ln;
            if (std::getline(f, ln)) {
                while (!ln.empty() && (ln.back() == (char)13 || ln.back() == (char)10 || ln.back() == (char)32)) ln.pop_back();
                if (!ln.empty()) want = ln;
            }
            for (size_t k = 0; k < g_plan.graphs.size() && k < g_plan.good_names.size(); k++) {
                if (g_plan.good_names[k] != want) continue;
                std::vector<char> has_out(g_plan.N, 0);
                for (auto& [u, v] : g_plan.graphs[k]) if (u >= 0 && u < g_plan.N) has_out[u] = 1;
                std::string list; int cnt = 0;
                for (int n = 0; n < g_plan.N; n++)
                    if (!has_out[n]) { cnt++; if (n < (int)g_plan.names.size()) list += g_plan.names[n] + " "; }
                std::ofstream lgs2(g_log, std::ios::app);
                lgs2 << "  [goodsinks] " << want << " price=" << (k < g_plan.prices.size() ? g_plan.prices[k] : 0.0)
                     << " sinks=" << cnt << " { " << list << "}" << (char)10;
                break;
            }
        }
    }
    // SWAP-ON-VIEW (spec 1.12): in a per-good view the SAME fields carry that good's numbers
    // alone, so the aggregate is taken over just the selected good.
    viewmode::poll(g_plan.good_names);

    PH("pre-orient");
    install_active_orientation();
    PH("orient");

    // The tick's own writes are ALWAYS the full aggregate economy -- pools, shares and pass 10 must
    // never see a single good's numbers because a window happened to be open at the month boundary
    // (reviewed). The active view is applied as a display overlay AFTER the canonical writes.
    std::vector<econ::GoodFlow> shown = per_good;
    std::vector<std::vector<double>> shown_inj = inj_field;
    // spec 1.7 / C5: caravan power only where a merchant actually steers a good on its link.
    // A country is "steering" at a node if any live good's graph orients an edge from that node
    // toward the link end the merchant sits on.
    {
        std::set<std::pair<int, int>> steering;
        std::map<std::string, int> nid;
        for (auto& [id, nm] : install::g_id_to_name) nid[nm] = id;
        for (int fn = 0; fn < g_plan.N && fn < (int)st.size(); fn++) {
            auto ni = nid.find(g_plan.names[fn]);
            if (ni == nid.end()) continue;
            for (auto& e : st[fn].entries) {
                if (e.steer_to < 0) continue;
                bool carries = false;
                for (auto& F : per_good) {
                    auto it = F.flow[fn].find(e.steer_to);
                    if (it != F.flow[fn].end() && it->second > 0) { carries = true; break; }
                }
                if (carries) steering.insert({e.country, ni->second});
            }
        }
        caravan::g_steering.swap(steering);
    }
    // spec 3.14 / G1: shadow-vanilla AI merchant re-placement over BOTH tab groups.
    std::vector<std::vector<int>> und(g_plan.N), phi_out(g_plan.N);
    for (int u = 0; u < g_plan.N && u < (int)g_plan.link_targets.size(); u++)
        for (int v : g_plan.link_targets[u])
            if (v >= 0) { und[u].push_back(v); und[v].push_back(u); phi_out[u].push_back(v); }
    auto away  = econ::directed_flows_no_bonus(shown);           // NO bonus (used again below for the per-mille shares)
    homeward::publish(g_plan.names, und, collect_nodes, sim, &away);   // the SetTrader hook homeward default: a user rule, not an AI feature (reviewed)
    compute_matrix_c();                                           // the model reach into the engine byte (light ships, +10%/merchant bonus)
if (livetrade::marker_present("AI")) {   // every month, a third of the countries (aiwire::g_shard)
        ai::Orient orient = aiwire::build_orient(g_plan.N, per_good, g_plan.graphs, inj_field);
        std::ofstream la(g_log, std::ios::app);
        PH("pre-flowmat");
        frontier::FlowMatrix flowmat = frontier::flow_matrix(g_plan.N, per_good);   // once per tick
        PH("flowmat");
        aiwire::g_flowmat = &flowmat;
        aiwire::g_shard = (int)(g_ticks.load() % 3);
        frontier::g_calls_candidates = 0; frontier::g_calls_plan = 0; aiwire::g_plan_cache.clear(); aiwire::g_plan_cache_hits = 0; aiwire::merchants_memo_reset(); aiwire::reach_cache_reset();
        { int pidx = aiwire::player_country_index();
          bool live = false; for (auto& ns0 : st) for (auto& e0 : ns0.entries) if (e0.power > 0 && livetrade::country_index_of(e0.country) == pidx) live = true;
          la << "  [ai] player country index=" << pidx << (pidx < 0 ? " (observer: every country is AI)" : (live ? " -- a LIVE trading country, excluded from the AI" : " -- holds no trade power anywhere (excluding it changes nothing)")) << (char)10;
          aiwire::step(sim, g_plan.names, st, orient, und, phi_out, (int)g_ticks.load(), pidx, la, &per_good); }
        PH("ai-step");
        envoy::dispatch(sim, g_plan.names, st, und, per_good, (int)g_ticks.load(), &la);   // send free merchants to planned nodes
        PH("dispatch");
        { std::ofstream lc(g_log, std::ios::app); lc << "  [ai/reach] CanSendMerchantTo calls this tick=" << aiwire::g_reach_calls << " refused=" << aiwire::g_reach_refused << (char)10; lc << "  [ai/cost] validate_region calls this tick=" << livetrade::g_validate_calls << " syscalls=" << livetrade::g_validate_syscalls << "; plan() calls=" << frontier::g_calls_plan << " candidates() calls=" << frontier::g_calls_candidates << " cache hits=" << aiwire::g_plan_cache_hits << (char)10; }
        aiwire::g_flowmat = nullptr;
    }
    auto agg = econ::aggregate(g_plan.N, shown, shown_inj);
    auto gross = econ::gross_link_flows(shown);                  // WITH steering bonus

    // ORDER MATTERS. The whole non-negativity guarantee is that `outgoing` is a FUNCTION of what
    // the node holds: install_aggregate computes held = local + Sigma incoming(+0x10) and writes
    // out = held x forwarded_fraction clamped into [0, held], so the UI's
    // total = local + Sigma incoming - outgoing can never go below zero. That only holds if the
    // incoming records are FINAL first. Writing them afterwards changes Sigma incoming out from
    // under an `outgoing` already derived from the old value -- which is exactly how negative
    // totals kept reappearing (krakow, north_sea).
    //
    // 1. one directed value per physical link, written at BOTH ends so the two node views agree
    // 1. the per-outgoing-link panel array (node+0x88). Also RESIZES it: the engine reads
    //    one past its end (0x13FC24D) and stock data is short on 24 of 80 nodes.
    // 0. give EVERY incident link a record at BOTH ends. The engine's own vectors are
    //    one-directional, so a link had a record at only one end and the two node windows
    //    read different arrays for it -- north_sea showing 2 where english_channel showed 10.
    // Give EVERY incident link a record. An edge carries two disjoint figures and both
    // belong at both ends; without a record for links drawn OUT of this node, the value
    // arriving along them has nowhere to live and is omitted from incoming entirely.
    outlinks::g_log_inc = g_log;
    // NO-COLLECT ENFORCEMENT runs every tick, AI marker or not: a save loaded mid-session brings
    // its collecting merchants back through the deserializer, which the hook never sees.
    { std::ofstream lnc(g_log, std::ios::app); nocollect::sweep(sim, &lnc); nocollect::report(lnc); }
    if (livetrade::marker_present("ALLOUT")) { std::ofstream lag(g_log, std::ios::app); aiguard::null_record_nodes(sim, &lag); }
    if (livetrade::marker_present("PROPPROBE")) { std::ofstream lpp(g_log, std::ios::app); propprobe::run(sim, lpp); }
    PH("ai+dispatch");
    if (livetrade::marker_present("NOWRITE")) {   // the E3 NULL RUN: the model observes, the engine keeps
        // its own vanilla division -- so still arm the pass-10 sampler, which is what [E3/top]
        // reads. Without the node count the wrapper never recognises its last node and E3 would
        // measure nothing in the control run.
        { int valid = 0; for (auto& s2 : sim) { std::string k2 = livetrade::node_key(s2.obj); if (!k2.empty() && k2 != "Null") valid++; }
          money::g_pass10_total = valid; money::g_pass10_seen = 0; }
        g_verify_pending = true;
        PH("nowrite"); std::ofstream lg0(g_log, std::ios::app); lg0 << "[tick/phases]" << ph_line << " (NOWRITE: engine writes skipped)" << (char)10; return 0; }
    outlinks::install_incoming(sim, g_plan.names, gross, install::g_id_to_name);
    // `away` (NO steering bonus), not `gross`. These become per-mille SHARES of the node's
    // outflow, and the tooltip turns them into ducats by multiplying by node+0xC0 == the
    // outgoing figure -- which itself excludes the bonus (route(): outgoing = value -
    // collected, while incoming adds f + b). Sharing out `gross` against a bonus-free total
    // would inflate every per-link line.
    //
    // NOTE on semantics: vanilla's steer_power is a share of MERCHANT POWER, and a merchant
    // there biases every good. Ours is the share of outflow our PER-GOOD routing actually
    // sends down each link -- spec 1.7: a merchant steers only the goods oriented away from
    // this node on that link, and is inert for the rest. The model has already applied that
    // rule per good; this field only carries the resulting aggregate split.
    outlinks::install(sim, g_plan.names, away, install::g_id_to_name);
    { std::ofstream lot(g_log, std::ios::app); lot << "  [outtip] reverse destinations listed: " << outlinks::g_rev_dest
          << "; tooltip builds so far=" << outtip::g_calls << " lines appended=" << outtip::g_appended << " unnamed=" << outtip::g_noname << (char)10;
      lot << "  [transfertext] builds=" << transfertext::g_calls << " substituted=" << transfertext::g_subst << " no-name=" << transfertext::g_nosub
          << " outliner builds=" << outlinertext::g_calls << " substituted=" << outlinertext::g_subst << " no-name=" << outlinertext::g_nosub<< " endtext node-window set=" << endtext::g_node_set << "/" << endtext::g_node_calls << " outliner set=" << endtext::g_out_set << "/" << endtext::g_out_calls<< " reach-rebuilt=" << g_reach_rebuilt << " (after landings: " << g_reach_rebuilt_frame << ") " << " treasure hops=" << treasure::g_calls << " supplied=" << treasure::g_supplied << " declined=" << treasure::g_declined << " norow=" << treasure::g_norow << " gatefills=" << gates::g_fills << " (frame " << gates::g_fills_frame << ", rebuild " << gates::g_fills_rebuild << ")" << " gateLAPSES=" << gates::g_lapses << " worst=" << gates::g_lapse_worst << "/512" << " gate-size-growth=" << gates::g_size_growth << " matC countries=" << g_matc_countries << " writes=" << g_matc_written << " homeward set=" << homeward::g_set << " had=" << homeward::g_had << " nohome=" << homeward::g_nohome << " nopath=" << homeward::g_nopath<< " athome=" << homeward::g_athome << " unknown-node=" << homeward::g_unknown_node << " multihome=" << homeward::g_multihome << " multicollect=" << homeward::g_multicollect << " capital-recalled=" << envoy::g_capital_recalled << " cache-pokes=" << transfertext::g_pokes << " view-mismatch=" << transfertext::g_viewmismatch << "; merge added with a bare index=" << assign::g_merge_bareidx
          << "; recall victims valued 0 for an off-network target=" << envoy::g_victim_offnet << (char)10;
      lot << "  [opening] loading-path hits=" << earlyload::g_hits.load() << " vanilla opening placements skipped=" << earlyload::g_opening_placements_skipped.load()
<< " colors: paints=" << colorview::g_paints << " passthrough=" << colorview::g_passthrough << " pokes=" << colorview::g_pokes << " bound-mismatch=" << colorview::g_bound_mismatch
<< " ships: allocator calls=" << lightship::g_calls << " rewritten=" << lightship::g_rewritten << " no-scores=" << lightship::g_nocountry << " bad-args=" << lightship::g_badargs << " sidecars written=" << savegame::g_written << " restored=" << savegame::g_restored << " missing=" << savegame::g_restore_missing << " new-game clears=" << savegame::g_cleared << (char)10; }
    // 2. one canonical value per physical link, written into BOTH endpoints' records
    PH("incoming");
    linkvalue::install(sim, g_plan.names, gross, install::g_id_to_name);
    // 2. now derive the node figures from those final records
    PH("linkvalue");
    int wrote = install::install_aggregate(sim, g_plan.names, agg, /*write_local=*/false);   // canonical: the overlay below shows the view
    // 3. the outgoing figure = the sum of this node's own outgoing rows, so the per-link
    //    amounts add up to it. Safe now that every link has a record at both ends.
    // NOT install_outgoing_sums: it summed node+0x88, which is the steer-share array, not
    // ducats. `outgoing` stays install_aggregate's clamped value, which is a function of
    // local + Sigma incoming and therefore cannot drive the displayed total negative.
    // ALWAYS, not behind a marker. node+0x88 is the per-outgoing-link value array the map panels
    // and the breakdown builder index BY LINK ORDINAL WITH NO BOUNDS CHECK, and in stock data it
    // is SHORTER than the outgoing list on 24 of 80 nodes -- a latent access violation that fires
    // whenever one of those nodes is looked at (0xB5654D, and 0x13FC24D in the panel module).
    // resize() is what makes it safe; turning this off to chase an unrelated bug re-exposed the
    // crash. It also writes the per-edge figures, scaled to sum to the node's own `outgoing`.
    // (moved above: outlinks must run BEFORE anything derives outgoing from the records)
    if ((g_ticks.load() % 4) == 0) {
        std::ofstream lf(g_log, std::ios::app);
        lf << "  [flow] wrote " << wrote << " nodes; " << flowwrite::g_bad_nodes
           << " fail local+incoming-outgoing==collected; worst " << flowwrite::g_worst_residual
           << " at " << flowwrite::g_worst_node << "\n";;
    }
    if ((g_ticks.load() % 4) == 0) outlinks::audit(g_log, sim);
    {   // both ends of every physical link must carry the same number
        std::ofstream la(g_log, std::ios::app);
        linkvalue::assert_flows(sim, g_plan.names, gross, install::g_id_to_name, la);
    }

    // predict this month's per-country division: pool (what we just wrote) x the engine's own
    // powershare. Recompute the monthly pool exactly as install_aggregate did.
    {
        auto byname = install::live_by_name(sim);
        std::vector<double> pool_monthly(g_plan.N, 0.0);
        for (int fn = 0; fn < g_plan.N; fn++) {
            auto it = byname.find(g_plan.names[fn]);
            if (it == byname.end()) continue;
            pool_monthly[fn] = livetrade::fi(sim[it->second].obj + 0xB0) / 1000.0;
        }
        // DEPARTURE D3: the model owns the division. Shares are written FIRST, then the prediction
        // is made from the model's own shares (not a read-back), so E1 tests write + pass 10 + pool.
        if (!livetrade::marker_present("NOSHARE")) {
            int wrote_sh = install::install_power_shares(sim, g_plan.names, st);
            std::ofstream lsh(g_log, std::ios::app); lsh << "  [share] wrote " << wrote_sh << " power fractions; pools with no paid collector so far=" << install::g_unpaid_pools << "; power writes skipped (slot)=" << install::g_power_write_skipped << (char)10;
            predict_income_from_model(pool_monthly);
        } else predict_income(sim, g_plan.names, pool_monthly);
        // E2's 'before' is now sampled inside pass 10 itself (money.h pass10_wrapper)
        // Pass 10 runs once per node with a VALID definition (0xB4BF3A tests def->vtbl[0x40]), so
        // the Null sentinel at slot 0 is skipped: 80 calls, not sim.size() == 81. Counting 81
        // meant the wrapper's 'last node' never fired and check_e2 saw 0/0.
        { int valid = 0; for (auto& s2 : sim) { std::string k2 = livetrade::node_key(s2.obj); if (!k2.empty() && k2 != "Null") valid++; }   // the sentinel has key "Null" and is skipped by pass 10: 80, measured
          money::g_pass10_total = valid; money::g_pass10_seen = 0; }
        { std::ofstream lp(g_log, std::ios::app); lp << "  [E2/wrap] exact=" << money::g_exact << " pass10 calls so far=" << money::g_pass10_calls_total << " total expected/month=" << money::g_pass10_total << (char)10; }
        g_verify_pending = true;      // the verifier samples rec.total after pass 10 finishes
    }
    // per-country shares of the pool, so the engine's own pass 10 pays out the model's income.
    // Behind a marker until the engine's own power_fraction semantics are observed (see the
    // standings dump): overwriting it blind could disturb displays that read the same field.
    // DEPARTURE D3: the model owns the collector division. power_fraction is written for every
    // record before the engine divides the pool; E1 then tests that the engine pays what was written.

    {   // the frame render path (instant view switch) reuses this tick's model outputs
        std::lock_guard<std::mutex> lk(g_render_mx);
        g_r_per_good = per_good;
        g_r_inj = inj_field;
        g_r_engine_local.clear();
        for (auto& s2 : sim) if (!s2.name.empty()) g_r_engine_local[s2.name] = s2.local_value;   // read before any overlay write
        g_render_valid = true;
    }
    // a view open across the month boundary: overlay its numbers on the canonical writes above
    if (viewmode::per_good()) render_overlay(sim, per_good, inj_field, /*tick_owns_pool=*/false);
    g_rendered_view = viewmode::g_selected;
    PH("aggregate+shares");
    { std::ofstream lgp(g_log, std::ios::app); lgp << "[tick/phases]" << ph_line << (char)10; }
    { std::ofstream ls(g_log, std::ios::app); ls << "  [steerbtn] entered=" << flagfix::g_sb_entered << " nokey=" << flagfix::g_sb_nokey << " want0=" << flagfix::g_sb_want0 << " nowin=" << flagfix::g_sb_nowin << " nobtn=" << flagfix::g_sb_nobtn << " curbad=" << flagfix::g_sb_curbad << " same=" << flagfix::g_sb_same << " forced=" << flagfix::g_frames_forced << (char)10; }
    return wrote;
}

inline void handler(detour::Regs* r) {
    // never re-enter (the driver can run more than once in a frame at high speed)
    bool expected = false;
    if (!g_inside.compare_exchange_strong(expected, true)) return;
    int wrote = 0;
    uintptr_t mgr = r->rsi;
    {   // a tick on a reloaded world this plan was not armed for: re-set up here (the frame poll
        // rides the map update and may never resume in a new campaign).
        // NEVER WHILE THE ENGINE IS BUILDING A WORLD (reviewed): InitNewGame runs a full
        // monthly driver at 0x774C2F -> 0x75D690 -> 0xB4BA90 BEFORE the mod's setup site at
        // 0x774C3B, and our hook lives inside that driver. enter_setup() disarms the plan for
        // exactly that window; without this guard the tick would re-set up on a half-built
        // world and then the wrapper would do it all again a few instructions later.
        // Keyed on the node array (mgr+0x18/+0x24), never the constant manager pointer.
        int armed = assign::g_in_loading.load() ? 0 : g_world_cnt.load();
        if (mgr && armed > 0 && livetrade::validate_region(mgr + 0x24, 4) && livetrade::validate_region(mgr + 0x18, 8)) {
            uintptr_t cur_nb = livetrade::fq(mgr + 0x18); int cur_cnt = livetrade::fi(mgr + 0x24);
            uint64_t cur_fp = world_fingerprint(mgr);
            int cd = engine_date(), ld = g_world_date.load();
            bool djump = (cd > 0 && ld > 0 && (cd < ld - DATE_BACK_TOL || cd - ld > DATE_JUMP_FWD));
            if (cd > 0) g_world_date = cd;   // roll the last-seen date (the tick observes it too)
            if (djump || cur_nb == 0 || cur_cnt <= 0 || cur_nb != g_world_nb.load() || cur_cnt != armed
                || (cur_fp != 0 && cur_fp != g_world_fp.load())) {
                {   std::ofstream lg(g_log, std::ios::app);
                    lg << "[world] tick sees a different campaign (date " << ld << "->" << cd
                       << " cnt " << armed << "->" << cur_cnt << "): re-setting up from inside the monthly update" << (char)10; }
                // DO THE RESETUP HERE. Holding the tick and waiting for the frame poll deadlocked:
                // the poll rides the map update and never resumed in a second campaign, so the mod
                // stayed silent and the game showed vanilla trade (ET 1241 -> menu -> 1776).
                if (g_resetup_in_tick) {
                    g_resetup_in_tick(mgr);                 // no nested driver run: we are inside it
                    if (!g_plan.ready) { g_inside = false; return; }   // setup failed: stay out of this world
                    // armed for the new world now; fall through and apply THIS tick's values
                } else { g_inside = false; return; }
            }
        }
    }
    // measure the added tick cost -- spec H3 requires it to be imperceptible, and an earlier
    // build (a VirtualQuery per field) stalled the monthly update for ~10 s in the live game.
    LARGE_INTEGER t0{}, t1{}, freq{};
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&t0);
    if (mgr) wrote = apply(mgr);
    QueryPerformanceCounter(&t1);
    double ms = freq.QuadPart ? (double)(t1.QuadPart - t0.QuadPart) * 1000.0 / freq.QuadPart : 0.0;
    int t = ++g_ticks;
    if (t <= 8 || (t % 12) == 0) {
        std::ofstream lg(g_log, std::ios::app);
        lg << "[H3] worst frame gap since last tick: " << frame::take_worst_gap() << " ms" << (char)10;
        lg << "[tick] monthly update " << t << ": wrote " << wrote
           << " nodes inside the engine's value pass (pre-division), " << ms << " ms\n";
    }
    g_inside = false;
}

// Install the inline hook. The expected bytes are the exact 20 bytes at 0xB4BF09 (four whole
// instructions, no RIP-relative operand, no branch), verified offline with capstone:
//   48 8b 5e 18              mov  rbx, [rsi+0x18]
//   48 63 46 24              movsxd rax, [rsi+0x24]
//   48 8b 74 24 60           mov  rsi, [rsp+0x60]
//   48 69 f8 38 01 00 00     imul rdi, rax, 0x138
// A byte mismatch means a different build: refuse (spec 2.5).
inline bool install_hook(std::string* err) {
    if (g_hook.active) return true;   // a second campaign re-runs the install: the live hook stays (reviewed)
    uintptr_t base = livetrade::module_base();
    uintptr_t site = base + 0xB4BF09;
    std::vector<uint8_t> expected{
        0x48, 0x8b, 0x5e, 0x18,
        0x48, 0x63, 0x46, 0x24,
        0x48, 0x8b, 0x74, 0x24, 0x60,
        0x48, 0x69, 0xf8, 0x38, 0x01, 0x00, 0x00};
    if (!detour::install(g_hook, site, expected, &handler, "monthly_value_pass")) {
        if (err) *err = g_hook.error;
        return false;
    }
    return true;
}

inline void remove_hook() { detour::remove(g_hook); }

// E1 VERIFIER THREAD. The handler runs BEFORE pass 10, so reading rec.total there samples
// records the engine has already reset for the new month -- which is why an in-handler read
// reported zeros. The division we want to check happens microseconds after the handler returns,
// so a worker samples shortly after each tick instead, off the game thread (spec H3).
inline std::atomic<bool> g_verify_stop{false};

inline void verify_worker() {
    while (!g_verify_stop) {
        if (g_verify_pending.exchange(false)) {
            // E1 and E4 now run from money::pass10_wrapper's last node (g_after_pass10),
            // inside the pass; the 400 ms sleep here raced it and read half-paid records.
            (void)0;
        }
        Sleep(120);
    }
}

inline void after_pass10(const std::vector<livetrade::SimNode>& sim, std::ofstream& lg) {
    verify_income(sim, lg);                       // E1
    money::check_e4(sim, lg, g_ticks.load());     // E4
}

inline bool g_verifier_started = false;
inline void start_verifier() {
    if (g_verifier_started) return;   // a second install must not spawn a second verifier thread (reviewed)
    g_verifier_started = true;
    money::g_after_pass10 = &after_pass10;
    CreateThread(nullptr, 0, [](LPVOID) -> DWORD { verify_worker(); return 0; }, nullptr, 0, nullptr);
}


inline void reset_world_state() {
    g_ticks = 0;                                        // the opening rule fires again for the new world
    g_first_tick_done = false; g_first_solve_requested = false;
    g_probe_recs.clear(); g_probe_last.clear();
    envoy::g_sent_tick.clear(); envoy::g_nothing_tick.clear(); envoy::g_prev_plan.clear();
    envoy::g_touched_tick.clear(); envoy::g_vacated_on_purpose.clear(); envoy::g_landings.clear();
    envoy::g_capital_recalled_envoys.clear();
    aiwire::g_prev.clear(); aiwire::g_baselined.clear(); aiwire::g_plan_cache.clear();
    aiwire::g_hold_tick.clear(); aiwire::g_flips.clear();      // tick-valued: campaign 1's ticks would read as the future (reviewed)
    arrows::g_defs_cache.clear();                               // definition pointers: one re-scan buys certainty
    arrows::g_reversed.clear();
    arrows::g_map_renderer = 0;                                 // the reloaded world rebuilds its own layer object
    relink::reset();                                            // captured defs are freed memory now: recapture
    colorview::g_by_name.clear(); colorview::g_good = 0;        // CTradeGood pointers are per-world
    g_treasure_gen = -1;
    treasure::reset();                                          // the next-hop ladder is the OLD topology; node id == index
                                                                // in any world, so pick_hop's fail-closed check cannot
                                                                // catch it (reviewed). Inert unless pgt.TREASURE.
    {   std::lock_guard<std::mutex> lk(g_render_mx);
        g_render_valid = false;
        g_r_per_good.clear(); g_r_inj.clear(); g_r_engine_local.clear();
    }
    g_rendered_view = -999;
    assign::g_skip_startup_once = false;
    lightship::clear_all();
    g_matc.clear();
    revpanel::g_rev_entry.clear(); revpanel::g_rev_views.clear(); revpanel::g_last_forward = 0;
    homeward::g_ready = false; homeward::g_field_of_node.clear();
    transfertext::g_memo_key.clear(); transfertext::g_memo_node = 0; transfertext::g_last_target.clear();
    endtext::g_memo_key.clear(); endtext::g_memo_node = 0; endtext::g_last_node = 0; endtext::g_last_val = -1; endtext::g_last_tgt.clear();
    g_installed_gen = -1;                               // the orientation must be installed afresh
    std::ofstream lg(g_log, std::ios::app); lg << "[world] state reset for a new campaign in this process" << (char)10;
}
} // namespace ticklive
