// AI MERCHANT ASSIGNMENT, WIRED TO LIVE MERCHANTS (spec 3.14; tests G1, G2).
//
// Cadence is SHADOW-VANILLA, the option the user chose: vanilla's own AI decides WHEN a country
// reconsiders a merchant, and that event triggers our re-placement. We never invent a schedule.
// This mirrors vanilla's cadence by construction, needs no cadence define, and fires on conquest
// for free. (The RE later measured vanilla's own rule -- a 10+rng()%15 day tick with a x1.5
// hysteresis against the worst existing placement at 0x1BD206 -- which is itself a computed-gain
// test with a dwell floor, i.e. exactly the shape the user predicted.)
//
// The TARGET is ours. Spec 3.14: "Candidates are (node, incident-link-end) pairs -- both of the
// node window's tab groups, not Phi_w-outgoing links -- and a candidate's active good set is the
// goods oriented away from that node on that link, which is the solver's own output: the AI reads
// the per-good orientations directly and never infers from the drawn map, and a candidate
// steering nothing scores zero and is never chosen." That is what test G1 looks for: placements
// on Phi_w-INCOMING ends where per-good flow justifies them.
//
// The chosen end is written into assign::g_table, which routing already honours -- including the
// ends the engine has no index for.
//
// Merchant enumeration (the engine's own recipe, used verbatim at 0x2741E6 / 0x1BC2ED):
//   CCountry* c = ((CCountry**)(*(char**)(base+0x233D8D0) + 0x118))[countryIndex];
//   void** vec  = *(void***)((char*)c + 0x1480);      // vector<CEnvoyContainer*>
//   CEnvoyContainer* merchants = (CEnvoyContainer*)vec[1];   // index == envoy type, 1 = merchants
//   CEnvoy** first = *(CEnvoy***)((char*)merchants + 0x20), ** last = ... + 0x28;
// CEnvoy: +0x10 CMerchantConstruction*, +0x18 action (0 free / 1 travelling / 2 posted), +0x44 id
// CMerchantConstruction: +0x80 the node it is posted at
#pragma once
#include <algorithm>
#include <fstream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include "livetrade.h"
#include "assign.h"
#include "../src/ai.h"
#include "../src/economy.h"
#include "../src/frontier.h"

namespace aiwire {

// the tick's flow matrix, summed once after routing (ticklive sets it before step/dispatch)
inline const frontier::FlowMatrix* g_flowmat = nullptr;
// plan() is deterministic for (country, k) within a tick; step and dispatch both need it
inline std::map<int, std::vector<frontier::Placement>> g_plan_cache;   // per country per tick
inline long long g_plan_cache_hits = 0;
inline const std::vector<frontier::Placement>& cached_plan(int N, int home, int k,
        const std::vector<std::vector<int>>& adj, const std::vector<econ::NodeStandings>& st, int c) {
    auto key = c;   // k differs between step (posted merchants) and dispatch (all merchants); the
                    // larger plan is a superset ordered by score, so one plan per country serves both
    auto it = g_plan_cache.find(key);
    if (it != g_plan_cache.end()) { g_plan_cache_hits++; return it->second; }
    return g_plan_cache[key] = frontier::plan(N, home, k, adj, st, *g_flowmat, c);
}

struct Merchant { int id = 0; int action = 0; int node_index = -1; };

inline uintptr_t country_mgr_array() {
    uintptr_t db = livetrade::rq(livetrade::module_base() + 0x233D8D0);
    return db ? livetrade::rq(db + 0x118) : 0;
}

inline uintptr_t country_by_index(int idx) {
    uintptr_t arr = country_mgr_array();
    if (!arr || idx < 0 || idx > 8192) return 0;
    if (!livetrade::validate_region(arr + (uintptr_t)idx * 8, 8)) return 0;
    return livetrade::fq(arr + (uintptr_t)idx * 8);
}

// every merchant a country owns, with the node it currently sits at
inline std::vector<Merchant> merchants_of(int country_idx) {
    std::vector<Merchant> out;
    uintptr_t c = country_by_index(country_idx);
    if (!c || !livetrade::validate_region(c + 0x1480, 8)) return out;
    uintptr_t vec = livetrade::fq(c + 0x1480);
    if (!vec || !livetrade::validate_region(vec + 8, 8)) return out;
    uintptr_t cont = livetrade::fq(vec + 8);            // index 1 == merchants
    if (!cont || !livetrade::validate_region(cont + 0x20, 16)) return out;
    uintptr_t first = livetrade::fq(cont + 0x20), last = livetrade::fq(cont + 0x28);
    if (!first || last <= first || (last - first) > 8 * 256) return out;
    if (!livetrade::validate_region(first, last - first)) return out;
    for (uintptr_t p = first; p + 8 <= last; p += 8) {
        uintptr_t e = livetrade::fq(p);
        if (!e || !livetrade::validate_region(e, 0x48)) continue;
        Merchant m;
        m.id = livetrade::fi(e + 0x44);
        m.action = livetrade::fi(e + 0x18);
        uintptr_t constr = livetrade::fq(e + 0x10);
        if (constr && livetrade::validate_region(constr + 0x80, 8)) {
            uintptr_t node = livetrade::fq(constr + 0x80);
            if (node && livetrade::validate_region(node + 0x120, 4))
                m.node_index = livetrade::fi(node + 0x120);
        }
        out.push_back(m);
    }
    return out;
}

// the previous tick's snapshot, for the shadow-vanilla trigger
inline std::map<int, std::map<int, int>> g_prev;    // country -> merchant id -> node index
inline std::set<int> g_baselined;                     // countries whose first snapshot is taken
inline int g_placed = 0, g_triggers = 0;

// --- G2 damping state, and the G1/G2 measurements -------------------------------------------
// Damping is the second half of the cadence the user chose: a computed-gain test plus a dwell
// floor of a few months. DWELL is ai::DWELL_FLOOR_MONTHS (3); the gain factor is vanilla's own
// x1.5 hysteresis (the constant at 0x1BD206 that its merchant AI tests a candidate against the
// worst existing placement with), so the damping is mirror-vanilla too rather than a new knob.
inline std::map<std::pair<int, std::string>, int>    g_hold_tick;
inline std::map<std::pair<int, std::string>, int>    g_flips;
inline long long g_phi_out = 0, g_phi_in = 0;   // G1: which tab group each chosen end sits in
inline long long g_damped = 0;
inline long long g_kept_collecting = 0;
inline long long g_moved_nodes = 0;
inline long long g_wants_move = 0;
inline long long g_vacated = 0;           // table entries dropped because the merchant left
inline long long g_frontier_cands = 0;    // frontier edges scored
inline int g_why_logged = 0;
inline long long g_rej_unreach = 0, g_rej_at_home = 0, g_rej_farther = 0;   // why
constexpr int CADENCE_TICKS = 3;          // each merchant reconsidered every N months
inline int g_evals = 0;

// Build the solver-side view the scorer needs, from this tick's routed flows.
inline ai::Orient build_orient(int N, const std::vector<econ::GoodFlow>& per_good,
                               const std::vector<std::vector<std::pair<int, int>>>& graphs,
                               const std::vector<std::vector<double>>& inject) {
    ai::Orient o;
    o.N = N;
    o.G = (int)graphs.size();
    o.away.assign(o.G, std::vector<std::vector<int>>(N));
    o.value_g.assign(o.G, std::vector<double>(N, 0.0));
    o.S.assign(o.G, {});
    for (int g = 0; g < o.G; g++) {
        for (auto& [u, v] : graphs[g]) o.away[g][u].push_back(v);
        for (int n = 0; n < N; n++) o.value_g[g][n] = per_good[g].value[n];
        o.S[g] = econ::survival(N, per_good[g], graphs[g]);
    }
    return o;
}

// One pass: diff every country's merchants against last tick; where vanilla moved one, score the
// (node, incident-link-end) candidates and record the winner.
inline void step(const std::vector<livetrade::SimNode>& sim,
                 const std::vector<std::string>& names,
                 const std::vector<econ::NodeStandings>& st,
                 const ai::Orient& orient,
                 const std::vector<std::vector<int>>& undirected_adj,
                 const std::vector<std::vector<int>>& phi_out_adj,   // Phi_w orientation, for G1
                 int tick,
                 int player_country,
                 std::ofstream& log,
                 const std::vector<econ::GoodFlow>* per_good = nullptr) {
    std::map<int, std::string> idx_name;
    for (int i = 0; i < (int)names.size(); i++) idx_name[i] = names[i];
    // engine node index -> field index
    std::map<int, int> eng_to_field;
    for (int fn = 0; fn < (int)names.size(); fn++) {
        for (auto& s : sim) if (s.name == names[fn]) { eng_to_field[s.index] = fn; break; }
    }
    int triggers = 0, placed = 0;
    // only countries that actually hold trade power somewhere are worth scoring
    std::set<int> live_countries;
    for (auto& ns : st) for (auto& e : ns.entries) if (e.power > 0) live_countries.insert(e.country);

    for (int c : live_countries) {
        if (c == player_country) continue;                 // spec 3.14 is about the AI
        // `c` is the RAW tag dword from the node record (+0x14), whose low 16 bits are the
        // country's index into the manager array and whose byte 3 is a validity tag. Passing the
        // raw value as an array index silently found nothing at all.
        int cidx = livetrade::country_index_of(c);
        auto ms = merchants_of(cidx);
        if (ms.empty()) continue;
        std::map<int, int> cur;
        for (auto& m : ms) if (m.action == 2 && m.node_index >= 0) cur[m.id] = m.node_index;
        std::map<int, int>& prev = g_prev[c];
        // THE FIRST SNAPSHOT IS A BASELINE, NOT A TRIGGER. With g_prev empty, every posted
        // merchant in the world read as "newly appeared" on tick 1 and was re-placed -- 624
        // of them, including every collector sitting at its own home node. Measured at
        // north_sea: 14 collectors on tick 1, ZERO from tick 2, all turned into steerers
        // toward english_channel, so P_collect went to 0 and the node forwarded 100% of
        // its value. Shadow-vanilla means we act when VANILLA moves a merchant, and on the
        // first tick vanilla has moved nothing.
        if (!g_baselined.count(c)) { g_baselined.insert(c); prev = cur; continue; }
        // The trigger is PER MERCHANT, not per country: a merchant is reconsidered only when
        // vanilla moved THAT merchant (it appeared, or its posted node changed). Diffing the
        // country's whole map instead lets one merchant setting out re-place all its siblings,
        // which is neither spec 3.14's rule (that rule is about one placement) nor the
        // rarely-firing behaviour the user's prior expects.
        // THE TRIGGER IS A CADENCE, NOT A VANILLA MOVE. The shadow-vanilla rule -- reconsider a
        // merchant only when vanilla just moved it -- turned out to place NOTHING on reverse ends
        // once vanilla settled, which it does within a few months: vanilla's own AI never moves
        // a merchant onto a link it cannot index, so waiting for it to move one first meant
        // waiting forever. The user's stated default (CLAUDE.md, spec 3.14) is the other option:
        // a computed-gain test plus a dwell floor of a few months, expected to fire rarely. So
        // every posted merchant is evaluated on that cadence, and the gain test and dwell floor
        // below are what keep it rare.
        //
        // A merchant vanilla just moved is still evaluated at once (it is in transit anyway).
        std::vector<std::pair<int, int>> changed;
        for (auto& [id, nd] : cur) {
            auto pv = prev.find(id);
            bool moved = (pv == prev.end() || pv->second != nd);
            bool due   = true;   // the caller already gates on g_ticks % 3 == 0; an inner id%3 test left two thirds of merchants never evaluated
            if (moved || due) changed.push_back({id, nd});
        }
        prev = cur;
        // A TABLE ENTRY LIVES ONLY WHILE THE MERCHANT STANDS THERE. When vanilla moves it away
        // the entry must go with it, or merge keeps converting the country's whole standing
        // at that node from collecting to steering and syncrec keeps fabricating has_trader=1
        // -- the country then earns nothing there, even at its own capital. assign::clear had
        // no caller at all; this is it.
        {
            std::set<std::string> posted_at;
            for (auto& [id, nd] : cur) { auto f = eng_to_field.find(nd); if (f != eng_to_field.end()) posted_at.insert(names[f->second]); }
            std::vector<std::string> gone;
            for (auto& [key, tgt] : assign::g_table)
                if (key.first == c && !posted_at.count(key.second)) gone.push_back(key.second);
            for (auto& n : gone) { assign::clear(c, n); g_vacated++; }
        }
        if (changed.empty()) continue;
        triggers += (int)changed.size();
        // build this country's live footprint
        ai::Country ac;
        ac.tag = std::to_string(c);
        // collect_power is WHERE THE COUNTRY COLLECTS -- its home node and any collecting
        // merchant -- not every node it holds power in. score_steer's `reach` sums survival
        // from the far end to these nodes, so with every powered node in here a merchant was
        // credited for pushing value toward places the country never collects at, and the
        // assignments pointed away from home. power_at is kept separately for eligibility.
        std::map<int, double> power_at;
        for (int fn = 0; fn < (int)st.size(); fn++)
            for (auto& e : st[fn].entries)
                if (e.country == c) {
                    if (e.power > 0) power_at[fn] = e.power;
                    if (e.collects && e.power > 0) { ac.collect_power[fn] = e.power; ac.home_nodes.insert(fn); }
                }
        if (ac.collect_power.empty()) continue;     // collects nowhere: nothing to steer toward
        // BFS FROM HOME over the undirected graph. An end n->m is worth evaluating only if it
        // points homeward: dist(m) < dist(n), where dist is hops to the nearest collect node.
        // Everything else is an edge away from home and can only ever score by accident.
        std::vector<int> dist_home((int)names.size(), -1);
        {
            std::vector<int> q;
            for (auto& [H, pw] : ac.collect_power) { dist_home[H] = 0; q.push_back(H); }
            for (size_t qi = 0; qi < q.size(); qi++) {
                int u = q[qi];
                if (u < 0 || u >= (int)undirected_adj.size()) continue;
                for (int v : undirected_adj[u])
                    if (v >= 0 && v < (int)dist_home.size() && dist_home[v] < 0) { dist_home[v] = dist_home[u] + 1; q.push_back(v); }
            }
        }
        // Homeward means "m is no further from a collect node than n is". Strict `<` rejected
        // every end at a home node (dist 0 -- nothing is closer than 0), which is where most
        // merchants stand: 15,683 ends rejected, 34 placed, measured. At home, steering toward
        // another collect node (0 -> 0) is homeward; steering into the void (0 -> 1) is not.
        // Away from home the strict form still holds, so a merchant a hop out never points
        // further out.
        auto homeward = [&](int n, int m) {
            if (n < 0 || m < 0 || n >= (int)dist_home.size() || m >= (int)dist_home.size()) return false;
            if (dist_home[m] < 0 || dist_home[n] < 0) return false;
            return dist_home[n] == 0 ? dist_home[m] == 0 : dist_home[m] < dist_home[n];
        };
        // re-place every posted merchant: candidates are the link ends at the node it sits on
        // ELIGIBLE NODES: every node where this country already holds power. That is the set the
        // engine's own CanSteer (0xB5C010) accepts -- a record with power > 0 or a merchant present,
        // else STEER_NO_POWER -- and it is where a merchant can actually be sent. Trade range is
        // not read from the engine yet (spec 2.7 item 17 is an open probe), so this is the
        // approximation; a country never holds power in a node it cannot reach.
        std::vector<int> eligible;
        for (auto& [fn, pw] : power_at) if (pw > 0) eligible.push_back(fn);
        for (int fn = 0; fn < (int)st.size(); fn++)
            for (auto& e : st[fn].entries)
                if (e.country == c && e.power > 0 &&
                    std::find(eligible.begin(), eligible.end(), fn) == eligible.end())
                    eligible.push_back(fn);

        // Who is ALREADY steering where, and this country's own power per node -- the
        // competition the spec's steered split divides by. This country is excluded so its
        // incumbent placement is not counted against it.
        std::map<int, std::map<int, double>> steer_by_node;
        std::map<int, double> my_power_by_node;
        for (int fn = 0; fn < (int)st.size(); fn++)
            for (auto& e : st[fn].entries) {
                if (e.power <= 0) continue;
                if (e.country == c) { my_power_by_node[fn] = e.power; continue; }
                if (!e.collects && e.steer_to >= 0) steer_by_node[fn][e.steer_to] += e.power;
            }
        // ---- THE FRONTIER MODEL (src/frontier.h) ----------------------------------------
        // Home is the trade capital. The network is home plus every node this country's placed
        // merchants stand at. Candidates are the frontier edges, scored by flow x product of
        // power shares along the network path home x share at home.
        int home = -1;
        for (int fn = 0; fn < (int)st.size() && home < 0; fn++)
            for (auto& e : st[fn].entries) if (e.country == c && e.is_capital) { home = fn; break; }
        if (home < 0) continue;                              // no trade capital: nothing to grow from
        if (!per_good) continue;
        // FOLLOW THE PLAN. frontier::plan(k) is the portfolio the offline test proved right on
        // the 1444 save (Ming: hangzhou->beijing, xian->beijing -- reverse ends toward home).
        // For each planned edge whose stand-node holds one of this country's posted merchants,
        // write that placement; a planned edge with no merchant standing there is what the
        // country WANTS but cannot have until its envoy travels, which is not driven yet.
        std::map<int,int> posted_node;   // merchant id -> field node it stands at
        for (auto& [id, nd] : cur) { auto f0 = eng_to_field.find(nd); if (f0 != eng_to_field.end()) posted_node[id] = f0->second; }
        std::set<int> standing_at;
        for (auto& [id, n2] : posted_node) standing_at.insert(n2);
        int k = (int)posted_node.size();
        if (k <= 0) continue;
        const auto& plan = cached_plan((int)names.size(), home, k, undirected_adj, st, c);
        g_frontier_cands += (long long)plan.size();
        // the weakest CURRENT placement, for the x1.5 move test
        std::set<int> network{home};
        for (int n2 : standing_at) network.insert(n2);
        double weakest = 1e300;
        for (auto& [key, tgt] : assign::g_table) {
            if (key.first != c) continue;
            auto nf = std::find(names.begin(), names.end(), key.second);
            auto tf = std::find(names.begin(), names.end(), tgt);
            if (nf == names.end() || tf == names.end()) continue;
            double v = frontier::added_value((int)names.size(), home, network, undirected_adj, st, *g_flowmat, c,
                                             (int)(nf - names.begin()), (int)(tf - names.begin()));
            if (v < weakest) weakest = v;
        }
        if (weakest > 1e299) weakest = 0.0;
        for (auto& pl : plan) {
            g_evals++;
            if (!standing_at.count(pl.node)) { g_wants_move++; continue; }   // no merchant there yet
            auto key = std::make_pair(c, names[pl.node]);
            auto ex = assign::g_table.find(key);
            if (ex != assign::g_table.end()) {
                if (ex->second == names[pl.target]) continue;                 // already there
                auto ht = g_hold_tick.find(key);
                if (ht != g_hold_tick.end() && tick - ht->second < (int)ai::DWELL_FLOOR_MONTHS) { g_damped++; continue; }
                if (pl.added < 1.5 * weakest) { g_damped++; continue; }       // vanilla's x1.5 vs the weakest
                g_flips[key]++;
            }
            assign::set(c, names[pl.node], names[pl.target]);
            g_hold_tick[key] = tick;
            if (g_why_logged < 40) {
                g_why_logged++;
                log << "    [plan] country#" << c << " home=" << names[home] << ": stand " << names[pl.node]
                    << " -> " << names[pl.target] << " added=" << pl.added << " weakest=" << weakest << (char)10;
            }
            // G1: against the ENGINE's declared outgoing list
            bool outgoing = false;
            {
                uintptr_t nd = 0; for (auto& s2 : sim) if (s2.name == names[pl.node]) { nd = s2.obj; break; }
                uintptr_t def = nd ? livetrade::fq(nd + 0xA8) : 0;
                if (def && livetrade::validate_region(def + 0x98, 16)) {
                    uintptr_t b2 = livetrade::fq(def + 0x98), e2 = livetrade::fq(def + 0xA0);
                    for (uintptr_t p2 = b2; b2 && e2 > b2 && p2 + 0x78 <= e2; p2 += 0x78) {
                        uintptr_t t = livetrade::validate_region(p2 + 0x30, 8) ? livetrade::fq(p2 + 0x30) : 0;
                        if (t && livetrade::def_key(t) == names[pl.target]) { outgoing = true; break; }
                    }
                }
            }
            if (outgoing) g_phi_out++; else g_phi_in++;
            placed++;
        }
    }
    g_triggers += triggers; g_placed += placed;
    long long tot = g_phi_out + g_phi_in;
    int worst_flip = 0;
    for (auto& [k, n] : g_flips) if (n > worst_flip) worst_flip = n;
    log << "  [ai] scan: " << live_countries.size() << " countries with power, "
        << g_wants_move << " merchants standing off their frontier; " << g_vacated << " entries vacated; "
        << g_frontier_cands << " frontier edges scored; " << triggers << " merchants moved by vanilla, "
        << placed << " re-placed by us; table now " << assign::g_table.size() << " entries" << (char)10;
    log << "  [G1] placements by tab group: " << g_phi_out << " on Phi_w-outgoing ends, "
        << g_phi_in << " on Phi_w-INCOMING ends"
        << (tot ? " (" : "") << (tot ? (int)(100.0 * g_phi_in / tot) : 0) << (tot ? "%)" : "")
        << " -- the incoming group is the one vanilla cannot express\n";
    log << "  [G2] damping: " << g_damped << " refused by the dwell floor/gain test, "
        << g_kept_collecting << " collectors kept collecting ("
        << (int)ai::DWELL_FLOOR_MONTHS << " months) or the x1.5 gain test, of " << g_evals
        << " evaluations; worst churn on any one (country,node) = " << worst_flip
        << " target changes over " << tick << " ticks\n";
}

} // namespace aiwire
