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
#include <fstream>
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
#include "assign.h"
#include "syncrec.h"
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
inline int g_installed_gen = -1;   // generation whose orientation is installed
inline int g_installed_view = -2;  // viewmode::g_selected it was installed for
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
inline void verify_income(const std::vector<livetrade::SimNode>& sim, std::ofstream& lg) {
    if (g_predicted.empty()) return;
    std::map<int, double> actual;
    for (auto& s : sim)
        for (auto& rec : livetrade::read_standings(s.obj)) {
            if (rec.total == 0) continue;
            actual[livetrade::country_index_of(rec.tag_index)] += rec.total;
        }
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
    bool rebuilt = flipped > 0 ? arrows::rebuild() : true;
    if (flipped > 0) arrows::mark_dirty();
    g_installed_gen  = g_plan.generation;
    g_installed_view = viewmode::g_selected;
    std::ofstream lg2(g_log, std::ios::app);
    lg2 << "[arrows] view=" << (viewmode::per_good() ? viewmode::g_selected_name
                                                    : std::string("AGGREGATE"))
        << " edges=" << active.size() << " re-oriented " << flipped
        << " drawn routes, layer rebuild "
        << (rebuilt ? "OK" : "SKIPPED (map renderer not captured yet)") << "\n";
}
}

// Per-frame: pick up a view change and re-install the orientation immediately. Spec 1.12's
// province click has to feel instant; waiting for the monthly tick would make the map lag a
// month behind the selection.
inline void frame_view_poll() {
    if (!g_plan.ready) return;
    // POLL ONLY. Installing the orientation from here rewrites the definition graph and rebuilds
    // the route layer in the middle of a frame, while the trade pass may be walking the very
    // lists being resized -- that raced and crashed the game. The install stays in the monthly
    // tick hook, which sits at a known-safe point between passes (0xB4BF09); at speed 5 a month
    // is about a second, so a view change still lands promptly.
    viewmode::poll(g_plan.good_names);

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
    if (!g_plan.ready) return 0;
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
    auto st = install::read_standings_field(sim, g_plan.names, g_plan.link_targets, collect_nodes);
    // spec 1.7: merchants assigned to a link END the engine has no index for (a link drawn INTO
    // this node) live in our own table and are merged on top of the engine's own assignments.
    assign::poll(g_log);
    int assigned = assign::merge(st, g_plan.names);
    // ...and the engine records are made to say the same, so the map draws what is routed
    { std::ofstream lsr(g_log, std::ios::app); syncrec::apply(sim, &lsr); }
    if (assigned && (g_ticks.load() % 12) == 0) {
        std::ofstream la(g_log, std::ios::app);
        la << "  [assign] " << assigned << " DLL-owned merchant assignments active\n";
    }

    std::vector<econ::GoodFlow> per_good;
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
    if (g_split_ticks < 6) {
        g_split_ticks++;
        std::ofstream lgs(g_log, std::ios::app);
        int ns = -1;
        for (int i = 0; i < (int)g_plan.names.size(); i++)
            if (g_plan.names[i] == "north_sea") { ns = i; break; }
        if (ns >= 0 && ns < (int)st.size()) {
            lgs << "  [split] tick " << g_split_ticks
                << " north_sea standings (power, collects, steer_to):" << (char)10;
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
    // SWAP-ON-VIEW (spec 1.12): in a per-good view the SAME fields carry that good's numbers
    // alone, so the aggregate is taken over just the selected good.
    viewmode::poll(g_plan.good_names);

    install_active_orientation();

    std::vector<econ::GoodFlow> shown = per_good;
    std::vector<std::vector<double>> shown_inj = inj_field;
    if (viewmode::per_good() && viewmode::g_selected < (int)per_good.size()) {
        shown.assign(1, per_good[viewmode::g_selected]);
        shown_inj.assign(1, inj_field[viewmode::g_selected]);
    }
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
    if (livetrade::marker_present("AI") && (g_ticks.load() % 3) == 0) {
        std::vector<std::vector<int>> und(g_plan.N), phi_out(g_plan.N);
        for (int u = 0; u < g_plan.N && u < (int)g_plan.link_targets.size(); u++)
            for (int v : g_plan.link_targets[u])
                if (v >= 0) { und[u].push_back(v); und[v].push_back(u); phi_out[u].push_back(v); }
        ai::Orient orient = aiwire::build_orient(g_plan.N, per_good, g_plan.graphs, inj_field);
        std::ofstream la(g_log, std::ios::app);
        aiwire::step(sim, g_plan.names, st, orient, und, phi_out, (int)g_ticks.load(), -1, la, &per_good);
    }
    auto agg = econ::aggregate(g_plan.N, shown, shown_inj);
    auto gross = econ::gross_link_flows(shown);                  // WITH steering bonus
    auto away  = econ::directed_flows_no_bonus(shown);           // NO bonus

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
    // 2. one canonical value per physical link, written into BOTH endpoints' records
    linkvalue::install(sim, g_plan.names, gross, install::g_id_to_name);
    // 2. now derive the node figures from those final records
    int wrote = install::install_aggregate(sim, g_plan.names, agg, viewmode::per_good());
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
        predict_income(sim, g_plan.names, pool_monthly);
        money::sample_before(sim);      // E2: accumulator before the collector division
        money::g_pass10_total = (int)sim.size();   // so the wrapper knows when the pass ends
        g_verify_pending = true;      // the verifier samples rec.total after pass 10 finishes
    }
    // per-country shares of the pool, so the engine's own pass 10 pays out the model's income.
    // Behind a marker until the engine's own power_fraction semantics are observed (see the
    // standings dump): overwriting it blind could disturb displays that read the same field.
    if (livetrade::marker_present("INCOME"))
        install::install_power_shares(sim, g_plan.names, st);
    return wrote;
}

inline void handler(detour::Regs* r) {
    // never re-enter (the driver can run more than once in a frame at high speed)
    bool expected = false;
    if (!g_inside.compare_exchange_strong(expected, true)) return;
    int wrote = 0;
    uintptr_t mgr = r->rsi;
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
            Sleep(400);                        // let pass 10 finish
            auto sim = livetrade::read_sim_nodes();
            if (!sim.empty()) {
                std::ofstream lg(g_log, std::ios::app);
                verify_income(sim, lg);                 // E1
                money::check_e4(sim, lg, g_ticks.load()); // E4
            }
        }
        Sleep(120);
    }
}

inline void start_verifier() {
    CreateThread(nullptr, 0, [](LPVOID) -> DWORD { verify_worker(); return 0; }, nullptr, 0, nullptr);
}

} // namespace ticklive
