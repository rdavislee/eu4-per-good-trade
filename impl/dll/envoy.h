// SENDING A MERCHANT TO THE NODE THE PLAN CHOSE (spec 3.14; the frontier model's last link).
//
// frontier::plan says where a country's k merchants should stand. aiwire can only write a
// placement where a merchant already IS; a planned node with no merchant there was counted as
// g_wants_move and nothing happened -- 1,005 of them on tick 7, against 8 placed. This is the
// mechanic that closes the gap.
//
// THE SEAM, from the send-merchant trace: the engine has a direct placement function, used by its
// own trade-company code (0x3BAB22, 0x3BB173) and by 0x774E05 (which picks a free envoy and calls
// it with mode=0, link=-1, force=0):
//
//   0x3BAD90  PlaceMerchantAtNode(CCountry* country /*rcx*/, CEnvoy* envoy /*rdx*/,
//                                 uint8 mode /*r8b: 0 collect, 1 transfer*/, CTradeNode* node /*r9*/,
//                                 int32 steerLinkIndex /*[rsp+0x20]; -1 = engine's choice*/,
//                                 uint8 force /*[rsp+0x28]; 1 skips the eligibility check*/)
//
// Body: operator new(0xA0) -> CMerchantConstruction ctor 0x25AAF0 -> mc+0x40 = country+0x20 (the
// handle) -> location province of the node -> SetEnvoy(mc, prov, envoy, force*2+1) -> envoy+0x18
// = 2 (posted) -> if steerLinkIndex >= 0, GetTraderRecord(node, handle) and rec+0xA8 = it
// (0x3BAE33). The force*2+1 is load-bearing: SetEnvoy's tail takes r9d in {1,3} as "instant"
// (progress 0x3E8, dates collapsed, 0x25C9C4..0x25C9DC) and tail-jumps into Update, where
// `cmp ecx,3; je` at 0x25B920 skips CanSendMerchantTo entirely and lands on SetTrader at
// 0x25B9A3. So one call places, registers the trade record, and sets the steer index -- with the
// +0xA8 write landing AFTER SetTrader's own link scoring (0xB599AE), so our override wins. No
// command queue, no gate, no travel delay.
//
// Caveat from the trace: SetTrader on that path is guarded by rec+0xAE == 0 (0x25B98E), so at a
// node where the country ALREADY has a trader the envoy is placed but the record's mode is not
// rewritten. We never call it in that state: a planned node with a merchant standing there is
// handled by aiwire (table + syncrec), and dispatch only targets nodes with none.
//
// Merchants never collect (user decision 2026-08-26): mode is always 1. steerLinkIndex is passed
// as -1 and the real target is written by syncrec from the table on the next tick, because a
// reverse end has no link index to pass.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include "livetrade.h"
#include "assign.h"
#include "aiwire.h"
#include "nocollect.h"
#include "../src/frontier.h"

namespace envoy {

constexpr uintptr_t PLACE_MERCHANT = 0x3BAD90;
constexpr int ENVOY_ACTION = 0x18;      // 0 free / 1 travelling / 2 posted
constexpr int ENVOY_ID     = 0x44;

using FnPlace = void (__fastcall*)(uintptr_t country, uintptr_t envoy, uint8_t mode, uintptr_t node,
                                   int32_t steerLinkIndex, uint8_t force);

inline uint64_t g_sent = 0, g_no_free = 0, g_no_node = 0, g_stale_record = 0;
inline std::map<std::pair<int, int>, int> g_sent_tick;   // (country, node) -> tick, dwell
inline std::map<int, int> g_nothing_tick;                  // country -> tick it last placed nothing
inline std::map<int, std::set<int>> g_prev_plan;           // country -> planned node set last time it was planned
inline std::map<std::pair<int, int>, int> g_touched_tick;  // (country, node) -> tick we last SENT TO or RECALLED FROM it (the dwell key)
inline std::set<std::pair<int, int>> g_vacated_on_purpose; // (country, node) we recalled a merchant from -- not a failed placement
struct Landing { uintptr_t envoy; int target_eng; int tick; int cidx; };
inline std::vector<Landing> g_landings;                    // recalls to re-check 1 and 3 ticks later
inline uint64_t g_land_ok1 = 0, g_land_bad1 = 0, g_land_ok3 = 0, g_land_bad3 = 0;
inline uint64_t g_no_free_country = 0;                     // countries with no free merchant this tick (dispatch's own count)
inline uint64_t g_recall_own = 0;                          // recalls whose victim was OUR OWN earlier placement
inline std::string g_log;
inline bool g_installed = false;

// the engine node object for a field index, by name
inline uintptr_t node_obj(const std::vector<livetrade::SimNode>& sim, const std::string& name) {
    for (auto& s : sim) if (s.name == name) return s.obj;
    return 0;
}

// a free envoy (action 0) of this country, or 0
inline uintptr_t free_envoy(int country_idx) {
    uintptr_t c = aiwire::country_by_index(country_idx);
    if (!c || !livetrade::validate_region(c + 0x1480, 8)) return 0;
    uintptr_t vec = livetrade::fq(c + 0x1480);
    if (!vec || !livetrade::validate_region(vec + 8, 8)) return 0;
    uintptr_t cont = livetrade::fq(vec + 8);
    if (!cont || !livetrade::validate_region(cont + 0x20, 16)) return 0;
    uintptr_t first = livetrade::fq(cont + 0x20), last = livetrade::fq(cont + 0x28);
    if (!first || last <= first || (last - first) > 8 * 256) return 0;
    if (!livetrade::validate_region(first, last - first)) return 0;          // C-2: the whole span
    for (uintptr_t p = first; p + 8 <= last; p += 8) {
        uintptr_t e = livetrade::fq(p);
        if (e && livetrade::validate_region(e, 0x48) && livetrade::fb(e + ENVOY_ACTION) == 0) return e;   // C-1: a byte
    }
    return 0;
}

// Place a free merchant of `country_idx` at `node` transferring. Returns false, touching nothing,
// if there is no free merchant or the node is unresolved.
inline std::string g_home_name;   // set by dispatch before send(), for the log line
inline bool send(int country_idx, uintptr_t node, std::ofstream* lg, const std::string& node_name, uintptr_t e = 0) {
    uintptr_t c = aiwire::country_by_index(country_idx);
    if (!c || !node) { g_no_node++; return false; }
    if (!e) e = free_envoy(country_idx);                 // callers that know their free list pass it in
    if (!e || livetrade::fb(e + ENVOY_ACTION) != 0) { g_no_free++; return false; }
    auto place = (FnPlace)(livetrade::module_base() + PLACE_MERCHANT);
    place(c, e, 1, node, -1, 1);
    g_sent++;
    if (lg) *lg << "  [envoy] country#" << country_idx << " merchant#" << livetrade::fi(e + ENVOY_ID)
                << " placed at " << node_name << " (home " << g_home_name << "; transfer; target set by the table next tick)" << (char)10;
    return true;
}

constexpr uintptr_t SET_TRADER = 0xB5E290;    // (rec, bool hasTrader, u8 type) -- syncrec's
using FnSetTrader = void (__fastcall*)(uintptr_t, bool, uint8_t);
inline uint64_t g_recalled = 0, g_recall_stale = 0, g_recall_refused = 0;
inline uint64_t g_plan_at_end = 0;
inline uint64_t g_unreachable = 0;                          // plan entries refused by the engine's CanSendMerchantTo at dispatch                          // plan entries skipped because the engine node has no outgoing link
constexpr int RECALL_CAP_PER_TICK = 60;      // world-wide per tick, observation cap
constexpr int RECALL_BUDGET_PER_COUNTRY = 2; // per country per tick: `continue` after a refusal must not become a stampede      // observation cap while the engine's behaviour on re-placement is being measured

// this country's per-node trade record at `node`, or 0 (index-dense array, slot-checked like syncrec)
inline uintptr_t record_at(uintptr_t node, int cidx) {
    if (!node || !livetrade::validate_region(node + 0x18, 16)) return 0;
    uintptr_t rb = livetrade::fq(node + 0x18); int rc = livetrade::fi(node + 0x24);
    if (!rb || cidx < 0 || cidx >= rc || !livetrade::validate_region(rb + (uintptr_t)cidx * 0xC0, 0xC0)) return 0;
    if ((livetrade::fi(rb + (uintptr_t)cidx * 0xC0 + 0x14) & 0xFFFF) != cidx) return 0;
    return rb + (uintptr_t)cidx * 0xC0;
}

// the name of the node the engine's own steer index on this record points at, or empty
inline std::string engine_steer_target(uintptr_t node, uintptr_t rec) {
    if (!rec || !node) return "";
    int li = livetrade::fi(rec + 0xA8);
    uintptr_t def = livetrade::validate_region(node + 0xA8, 8) ? livetrade::fq(node + 0xA8) : 0;
    if (!def || li < 0 || !livetrade::validate_region(def + 0x98, 16)) return "";
    uintptr_t b2 = livetrade::fq(def + 0x98), e2 = livetrade::fq(def + 0xA0);
    uintptr_t p2 = b2 + (uintptr_t)li * 0x78;
    if (!b2 || e2 <= b2 || p2 + 0x78 > e2 || !livetrade::validate_region(p2 + 0x30, 8)) return "";
    uintptr_t t = livetrade::fq(p2 + 0x30);
    return t ? livetrade::def_key(t) : std::string();
}

// RECALL: move a POSTED merchant to `node`. The engine's own reassignment goes through the same
// PlaceMerchantAtNode; what it does to the OLD node's record is not documented anywhere we
// trust, so the record's has_trader byte is read before and after, and if the engine left it
// set (the 0x775C14 pattern: envoy freed, ClearTrader never called) it is cleared here with
// SetTrader(rec, false, 1) -- otherwise syncrec would keep a phantom merchant there.
inline bool recall_send(int country_idx, uintptr_t envoy, uintptr_t old_node, uintptr_t node,
                        std::ofstream* lg, const std::string& old_name, const std::string& node_name, int tick) {
    uintptr_t c = aiwire::country_by_index(country_idx);
    if (!c || !node || !envoy || !old_node) return false;
    uintptr_t old_rec = record_at(old_node, country_idx);
    int before = old_rec ? livetrade::fb(old_rec + 0xAE) : -1;
    int act0 = livetrade::fb(envoy + ENVOY_ACTION);
    uintptr_t mc0 = livetrade::validate_region(envoy + 0x10, 8) ? livetrade::fq(envoy + 0x10) : 0;   // the construction it owns now
    int target_eng = livetrade::validate_region(node + 0x120, 4) ? livetrade::fi(node + 0x120) : -1;
    auto place = (FnPlace)(livetrade::module_base() + PLACE_MERCHANT);
    place(c, envoy, 1, node, -1, 1);
    int after = old_rec ? livetrade::fb(old_rec + 0xAE) : -1;
    int act1 = livetrade::fb(envoy + ENVOY_ACTION);
    uintptr_t mc1 = livetrade::validate_region(envoy + 0x10, 8) ? livetrade::fq(envoy + 0x10) : 0;
    // does the OLD construction still claim this envoy? (a leaked live alias would re-assert the old post)
    uintptr_t old_back = (mc0 && mc0 != mc1 && livetrade::validate_region(mc0 + 0x48, 8)) ? livetrade::fq(mc0 + 0x48) : 0;
    int newnode = -1;
    { uintptr_t constr = livetrade::validate_region(envoy + 0x10, 8) ? livetrade::fq(envoy + 0x10) : 0;
      if (constr && livetrade::validate_region(constr + 0x80, 8)) { uintptr_t nn = livetrade::fq(constr + 0x80); if (nn && livetrade::validate_region(nn + 0x120, 4)) newnode = livetrade::fi(nn + 0x120); } }
    bool stale = (after == 1);
    if (stale) { ((FnSetTrader)(livetrade::module_base() + SET_TRADER))(old_rec, false, 1); g_recall_stale++; }
    int cleared = old_rec ? livetrade::fb(old_rec + 0xAE) : -1;
    bool landed = (newnode >= 0 && newnode == target_eng);
    if (landed) { g_recalled++; g_landings.push_back({envoy, target_eng, tick, country_idx}); }
    if (lg) *lg << "  [recall] country#" << country_idx << " merchant#" << livetrade::fi(envoy + ENVOY_ID)
                << " " << old_name << " -> " << node_name << ": old has_trader " << before << "->" << after
                << (stale ? " (engine left it set; cleared by SetTrader -> " + std::to_string(cleared) + ")" : "")
                << "; action " << act0 << "->" << act1 << "; construction 0x" << std::hex << mc0 << "->0x" << mc1 << std::dec
                << (mc0 == mc1 ? " (same)" : (old_back == envoy ? " (OLD ONE STILL CLAIMS THE ENVOY)" : " (old one detached)"))
                << "; landed at engine node " << newnode << (landed ? " OK" : " MISMATCH -- not recorded") << (char)10;
    return landed;
}

// One pass per AI tick, after aiwire::step: for each country, for each planned node with no
// merchant standing there, send a free one. Dwell-floored so a merchant is not bounced.
inline int dispatch(const std::vector<livetrade::SimNode>& sim,
                    const std::vector<std::string>& names,
                    const std::vector<econ::NodeStandings>& st,
                    const std::vector<std::vector<int>>& undirected_adj,
                    const std::vector<econ::GoodFlow>& per_good,
                    int tick, std::ofstream* lg) {
    const int player_idx = aiwire::player_country_index();
    if (!g_installed) return 0;
    // DO OUR PLACEMENTS STICK? Every (country,node) we sent to is in g_sent_tick; count how
    // many still have one of that country's merchants standing there this tick.
    { int still = 0, gone = 0;
      std::map<int, std::set<int>> where;   // country -> field nodes with a posted merchant
      std::map<int, int> e2f;
      for (int fn = 0; fn < (int)names.size(); fn++) for (auto& s : sim) if (s.name == names[fn]) { e2f[s.index] = fn; break; }
      int vacated = 0;
      for (auto& [key, t0] : g_sent_tick) {
          if (g_vacated_on_purpose.count(key)) { vacated++; continue; }   // we recalled it ourselves: not a failed placement
          int c = key.first; if (!where.count(c)) { where[c]; for (auto& m : aiwire::merchants_of(livetrade::country_index_of(c))) if (m.action == 2) { auto f = e2f.find(m.node_index); if (f != e2f.end()) where[c].insert(f->second); } }
          if (where[c].count(key.second)) still++; else gone++;
      }
      if (lg && (still || gone)) *lg << "  [envoy] of " << (still + gone + vacated) << " nodes we ever sent a merchant to, " << still << " still hold one, " << gone << " do not, " << vacated << " vacated by our own recall" << (char)10;
      // LANDING VERIFICATION: is each recalled envoy still at its target 1 and 3 ticks later?
      { int ok1 = 0, bad1 = 0, ok3 = 0, bad3 = 0;
        for (auto& L : g_landings) {
            int age = tick - L.tick; if (age != 1 && age != 3) continue;
            int now_at = -1;
            if (livetrade::validate_region(L.envoy, 0x48)) { uintptr_t mc = livetrade::fq(L.envoy + 0x10);
                if (mc && livetrade::validate_region(mc + 0x80, 8)) { uintptr_t nn = livetrade::fq(mc + 0x80); if (nn && livetrade::validate_region(nn + 0x120, 4)) now_at = livetrade::fi(nn + 0x120); } }
            bool ok = (now_at == L.target_eng);
            if (age == 1) { if (ok) ok1++; else bad1++; } else { if (ok) ok3++; else bad3++; }
        }
        g_land_ok1 += ok1; g_land_bad1 += bad1; g_land_ok3 += ok3; g_land_bad3 += bad3;
        if (lg && (ok1 || bad1 || ok3 || bad3)) *lg << "  [recall/verify] +1 tick: " << ok1 << " still at target, " << bad1 << " not; +3 ticks: " << ok3 << " still, " << bad3 << " not (run totals " << g_land_ok1 << "/" << g_land_bad1 << ", " << g_land_ok3 << "/" << g_land_bad3 << ")" << (char)10;
        if (g_landings.size() > 4000) g_landings.erase(g_landings.begin(), g_landings.begin() + 2000);
      }
    }
    int sent = 0, recalls_this_tick = 0, drift_countries = 0, drift_nodes = 0, planned_countries = 0, recall_own_tick = 0;
    std::set<int> countries;
    for (auto& ns : st) for (auto& e : ns.entries) if (e.power > 0) countries.insert(e.country);
    // hoisted: the same for every country, was rebuilt per country (80 x sim.size() string compares)
    std::map<int, int> eng_to_field;
    for (int fn = 0; fn < (int)names.size(); fn++)
        for (auto& s : sim) if (s.name == names[fn]) { eng_to_field[s.index] = fn; break; }
    std::vector<uintptr_t> obj_of(names.size(), 0);   // field index -> engine node object, once (was a string scan per use)
    for (int fn = 0; fn < (int)names.size(); fn++) for (auto& s : sim) if (s.name == names[fn]) { obj_of[fn] = s.obj; break; }
    LARGE_INTEGER cf, ct; QueryPerformanceFrequency(&cf); auto nowms = [&]() { QueryPerformanceCounter(&ct); return 1000.0 * (double)ct.QuadPart / (double)cf.QuadPart; };
    double t_merch = 0, t_plan = 0, t_victim = 0, t_send = 0, t_recall = 0;
    for (int c : countries) {
        int cidx = livetrade::country_index_of(c);
        if (aiwire::g_shard >= 0 && (cidx % 3) != aiwire::g_shard) continue;   // same shard as step
        if (player_idx >= 0 && cidx == player_idx) continue;   // never send the human's merchants
        int home = -1;
        for (int fn = 0; fn < (int)st.size() && home < 0; fn++)
            for (auto& e : st[fn].entries) if (e.country == c && e.is_capital) { home = fn; break; }
        if (home < 0) continue;
        double tm0 = nowms(); const auto& ms = aiwire::merchants_of(cidx); t_merch += nowms() - tm0;
        std::vector<uintptr_t> free_list; for (auto& m : ms) if (m.action == 0 && m.envoy) free_list.push_back(m.envoy);
        if (ms.empty()) continue;
        int k = (int)ms.size();
        // nothing to dispatch if no merchant is free: every plan() call for such a country is
        // wasted (measured: dispatch 190 ms of a 375 ms AI tick, most countries saturated)
        // (the old "no free merchant: skip the country" gate is gone: a country with none free can
        //  still RECALL an off-plan merchant below, and that is most of the world's merchants)
        if (free_list.empty()) g_no_free_country++;
        // a country whose free merchant could not be placed last pass will not place now either
        // (the plan is the same until the standings move); skip it for the dwell floor
        { auto ns = g_nothing_tick.find(c); if (ns != g_nothing_tick.end() && tick - ns->second < (int)ai::DWELL_FLOOR_MONTHS) continue; }
        // a node is OCCUPIED by a merchant that is posted there (action 2) OR still travelling
        // there (action 1): sending a second one to a node the first has not reached yet
        // force-places it instantly, and when the first arrives its record is already claimed
        // (SetTrader is gated on has_trader == 0) -- one merchant stranded (reviewed defect).
        std::set<int> standing;
        for (auto& m : ms) if ((m.action == 2 || m.action == 1) && m.node_index >= 0) { auto f = eng_to_field.find(m.node_index); if (f != eng_to_field.end()) standing.insert(f->second); }
        g_home_name = names[home];
        frontier::Reach reach = [&](int fnode) -> bool {
            if (standing.count(fnode)) return true;
            uintptr_t nobj = (fnode >= 0 && fnode < (int)obj_of.size()) ? obj_of[fnode] : 0;
            return nobj && aiwire::can_send_to(cidx, nobj);
        };
        double tp0 = nowms(); const auto& plan = aiwire::cached_plan((int)names.size(), home, k, undirected_adj, st, c, &reach); t_plan += nowms() - tp0;
        {   // PLAN DRIFT: how many planned nodes changed since this country was last planned
            std::set<int> now; for (auto& q : plan) now.insert(q.node);
            auto pv = g_prev_plan.find(c);
            if (pv != g_prev_plan.end()) {
                int d = 0; for (int n0 : now) if (!pv->second.count(n0)) d++; for (int n0 : pv->second) if (!now.count(n0)) d++;
                if (d) { drift_countries++; drift_nodes += d; }
                planned_countries++;
            }
            g_prev_plan[c] = now;
        }
        int sent_here = 0, recalls_here = 0;
        std::set<uintptr_t> moved_envoys;
        std::set<int> plan_nodes; for (auto& q : plan) plan_nodes.insert(q.node);
        std::set<int> score_net{home}; for (int sn : standing) score_net.insert(sn); for (int pn : plan_nodes) score_net.insert(pn);
        std::map<int, double> victim_value;   // stand node -> value on score_net, memoised for the tick
        for (auto& pl : plan) {
            if (standing.count(pl.node)) continue;               // aiwire handles the ones already there
            if (pl.node == home) continue;                        // never at the capital
            // D-1 (review): the engine's record can say has_trader=1 with no envoy there -- 0x775C14
            // frees an envoy without ClearTrader, and Update then bails forever on +0x58. Placing
            // another merchant on such a record is not caught by the envoy list; read the record.
            {
                uintptr_t nd0 = obj_of[pl.node];
                uintptr_t rb = nd0 ? livetrade::rq(nd0 + 0x18) : 0; int rc = nd0 ? livetrade::ri(nd0 + 0x24) : 0;
                // same slot check syncrec applies: the record at [cidx] must carry this country's
                // index at +0x14, or the array is not index-dense and this is another country's byte
                if (rb && cidx >= 0 && cidx < rc && livetrade::validate_region(rb + (uintptr_t)cidx * 0xC0, 0xC0)
                    && (livetrade::fi(rb + (uintptr_t)cidx * 0xC0 + 0x14) & 0xFFFF) == cidx
                    && livetrade::fb(rb + (uintptr_t)cidx * 0xC0 + 0xAE) != 0) { g_stale_record++; continue; }
            }
            auto key = std::make_pair(c, pl.node);
            auto it = g_touched_tick.find(key);
            if (it != g_touched_tick.end() && tick - it->second < (int)ai::DWELL_FLOOR_MONTHS) continue;
            uintptr_t nd = obj_of[pl.node];
            if (!nd) { g_no_node++; continue; }                      // name did not resolve: not a recall case
            // an END node (no outgoing entry in the engine) cannot hold a steering merchant: the engine
            // would keep it collecting, the model would call it a steerer, and the two would disagree
            // about who is paid. Until relink gives such nodes entries (ALLOUT), the plan skips them.
            if (!nocollect::node_has_outgoing(nd)) g_plan_at_end++;   // D3: an END node is plannable -- the model owns who is paid there (counted only)
            if (!standing.count(pl.node) && !aiwire::can_send_to(cidx, nd)) { g_unreachable++; continue; }   // never force a placement the engine would refuse
            double ts0 = nowms();
            bool placed_here = false;
            if (!free_list.empty()) { placed_here = send(cidx, nd, lg, names[pl.node], free_list.back()); if (placed_here) free_list.pop_back(); }
            t_send += nowms() - ts0;
            bool recalled_here = false;
            if (!placed_here) {
                // NO FREE MERCHANT. The user's rule: move only if this candidate beats the LEAST
                // profitable current merchant by x1.5. Victims are the posted merchants standing OFF
                // the plan, valued by THE SAME METRIC ON THE SAME NETWORK the candidate was scored in
                // -- home + standing + planned nodes, built once per country and never shrunk within
                // the tick. (Scoring victims on the standing network alone made every placement the
                // plan had just created worth -1 as a victim, which won the min and bypassed the
                // x1.5 test: 42 recalls, 9 refusals, self-sustaining -- reviewed.)
                if (recalls_this_tick >= RECALL_CAP_PER_TICK || recalls_here >= RECALL_BUDGET_PER_COUNTRY) continue;
                double tv0 = nowms();
                double weakest = 1e300; const aiwire::Merchant* victim = nullptr; int victim_node = -1; bool any_valid = false;
                for (auto& m : ms) {
                    if (m.action != 2 || m.node_index < 0 || !m.envoy) continue;
                    if (moved_envoys.count(m.envoy)) continue;              // already re-placed this tick (snapshot is stale)
                    auto f = eng_to_field.find(m.node_index); if (f == eng_to_field.end()) continue;
                    int fnode = f->second;
                    if (plan_nodes.count(fnode)) continue;                    // on the plan: not a victim
                    // A MERCHANT STANDING AT ITS OWN CAPITAL is worth nothing under the rule (it can only
                    // collect there, which is forbidden; vanilla parks 573 of them at home at the 1444
                    // start). It is the first victim, at value 0 -- no gain test can keep it there.
                    if (fnode == home) { if (0.0 < weakest) { weakest = 0.0; victim = &m; victim_node = fnode; any_valid = true; } continue; }
                    auto tt = g_touched_tick.find(std::make_pair(c, fnode));
                    if (tt != g_touched_tick.end() && tick - tt->second < (int)ai::DWELL_FLOOR_MONTHS) continue;   // dwell
                    double v;
                    auto memo = victim_value.find(fnode);
                    if (memo != victim_value.end()) v = memo->second;
                    else {
                        int tgt = -1;
                        auto te = assign::g_table.find(std::make_pair(c, names[fnode]));
                        uintptr_t vobj = obj_of[fnode];
                        std::string tname = te != assign::g_table.end() ? te->second : engine_steer_target(vobj, record_at(vobj, cidx));
                        for (int i2 = 0; i2 < (int)names.size(); i2++) if (names[i2] == tname) { tgt = i2; break; }
                        v = tgt >= 0 ? frontier::added_value((int)names.size(), home, score_net, undirected_adj, st, *aiwire::g_flowmat, c, fnode, tgt) : -1.0;
                        victim_value[fnode] = v;
                    }
                    if (v < 0) continue;                                    // not evaluable on this network: never a victim
                    any_valid = true;
                    if (v < weakest) { weakest = v; victim = &m; victim_node = fnode; }
                }
                t_victim += nowms() - tv0;
                if (!victim || !any_valid) continue;                       // nothing recallable for this entry
                if (pl.added < 1.5 * weakest) { g_recall_refused++; continue; }   // NOT break: the greedy plan is not sorted by added
                double tr0 = nowms();
                bool ok_recall = recall_send(cidx, victim->envoy, obj_of[victim_node], nd, lg, names[victim_node], names[pl.node], tick);
                t_recall += nowms() - tr0;
                if (!ok_recall) { g_touched_tick[std::make_pair(c, victim_node)] = tick; continue; }   // do not retry it every tick
                { auto own = g_sent_tick.find(std::make_pair(c, victim_node));
                  if (own != g_sent_tick.end()) { g_recall_own++; recall_own_tick++;
                      if (lg) *lg << "  [recall/own] country#" << cidx << " victim at " << names[victim_node] << " was OUR placement " << (tick - own->second) << " ticks ago, worth " << weakest << " vs candidate " << names[pl.node] << " worth " << pl.added << (char)10; }
                  g_vacated_on_purpose.insert(std::make_pair(c, victim_node)); }
                assign::clear(c, names[victim_node]);
                g_touched_tick[std::make_pair(c, victim_node)] = tick;       // dwell on the node we just emptied too (no ping-pong)
                standing.erase(victim_node);
                moved_envoys.insert(victim->envoy);
                recalls_this_tick++; recalls_here++; recalled_here = true;
            }
            // the table entry is what routing and syncrec read; write it now
            assign::set(c, names[pl.node], names[pl.target]);
            g_sent_tick[key] = tick;
            g_touched_tick[key] = tick;
            g_vacated_on_purpose.erase(key);
            // G1: is this end one the engine can index (declared outgoing) or a reverse end?
            {
                bool outgoing = false;
                uintptr_t def = nd ? livetrade::fq(nd + 0xA8) : 0;
                if (def && livetrade::validate_region(def + 0x98, 16)) {
                    uintptr_t b2 = livetrade::fq(def + 0x98), e2 = livetrade::fq(def + 0xA0);
                    for (uintptr_t p2 = b2; b2 && e2 > b2 && p2 + 0x78 <= e2; p2 += 0x78) {
                        uintptr_t t = livetrade::validate_region(p2 + 0x30, 8) ? livetrade::fq(p2 + 0x30) : 0;
                        if (t && livetrade::def_key(t) == names[pl.target] && livetrade::fq(p2 + 0x58) != 0) { outgoing = true; break; }   // a ribbon-less (appended) entry is a reverse end
                    }
                }
                if (outgoing) aiwire::g_phi_out++; else aiwire::g_phi_in++;
            }
            standing.insert(pl.node);
            if (recalled_here) { /* counted in recalls_here */ } else { sent++; sent_here++; }
        }
        if (sent_here == 0 && recalls_here == 0) g_nothing_tick[c] = tick;
    }
    if (lg) *lg << "  [envoy/cost] merchants_of=" << (int)t_merch << "ms plan=" << (int)t_plan << "ms victims=" << (int)t_victim << "ms send=" << (int)t_send << "ms recall=" << (int)t_recall << "ms" << (char)10;
    if (lg && planned_countries) *lg << "  [plan/drift] " << drift_countries << " of " << planned_countries << " planned countries changed their planned node set since last planned; " << drift_nodes << " node changes in total" << (char)10;
    if (lg && recalls_this_tick) *lg << "  [envoy] recalled " << recalls_this_tick << " (" << recall_own_tick << " of them our own placements; " << g_recall_own << " ever)" << " off-plan merchants this tick (" << g_recalled << " landed in total; " << g_recall_stale << " old records the engine left set; " << g_recall_refused << " refused by the x1.5 test)" << (char)10;
    if (lg && g_plan_at_end) *lg << "  [envoy] plan entries at engine END nodes so far (allowed under D3): " << g_plan_at_end << (char)10;
    if (lg && sent) *lg << "  [envoy] dispatched " << sent << " merchants to planned nodes this tick ("
                        << g_sent << " total; " << g_plan_at_end << " plan entries at END nodes (counted, not skipped); " << g_unreachable << " refused by CanSendMerchantTo; " << g_no_free << " send() calls with no free merchant; " << g_no_free_country << " country-ticks with none free; " << g_stale_record << " skipped: record already has_trader)" << (char)10;
    return sent;
}

inline bool install(const std::string& logpath, std::string* err) {
    g_log = logpath;
    uintptr_t fn = livetrade::module_base() + PLACE_MERCHANT;
    if (!livetrade::validate_region(fn, 16)) { if (err) *err = "0x3BAD90 unreadable"; return false; }
    // the traced prologue, byte-exact; any other build is refused (spec 2.5)
    static const uint8_t expect[20] = {0x48,0x89,0x5C,0x24,0x10, 0x48,0x89,0x6C,0x24,0x18,
                                       0x48,0x89,0x74,0x24,0x20, 0x57, 0x48,0x83,0xEC,0x20};
    if (memcmp((const void*)fn, expect, 20) != 0) { if (err) *err = "0x3BAD90 prologue differs (patched binary?)"; return false; }
    g_installed = true;
    return true;
}

} // namespace envoy
