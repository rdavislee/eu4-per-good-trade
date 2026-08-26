// Installing the per-good economy into the engine (spec 1.8, 2.6), NAME-KEYED.
//
// The critical correctness point: the live engine's node array is in the engine's own node order
// (which follows the MOD's reordered 00_tradenodes.txt), while the solver's field is indexed by
// the reference file's node order. Those orders differ, so live node i and field node i are NOT
// the same place. Everything here maps between them BY NODE NAME, read from engine memory
// (livetrade::SimNode::name), so routing lands on the right nodes no matter how a file is ordered.
//
//   1. read each live node's produced quantities (trade_goods_size) -> inject, gathered into
//      FIELD index order by name;
//   2. run the shipped DRAIN solver over the field to get each good's graph and Phi_w;
//   3. route each good's injected value along its own graph (econ::route -- per-good eligibility,
//      steering, sink collection); aggregate to the spec 2.6 node fields;
//   4. write the aggregate back into the engine's node TOTAL field (local is left untouched so
//      spec test B4 -- "local equals the engine's own" -- still holds), by name.
#pragma once
#include <cmath>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "assign.h"
#include "../src/economy.h"
#include "arrows.h"

namespace install {

// The authoritative engine-node-id -> node-name map, resolved once at attach (nodemap::resolve)
// and keyed by the STABLE engine id, so every later read can name its nodes without rematching.
inline std::map<int, std::string> g_id_to_name;

// name -> live SimNode index (engine array position). Built once per read.
inline std::map<std::string, int> live_by_name(const std::vector<livetrade::SimNode>& sim) {
    std::map<std::string, int> m;
    for (int i = 0; i < (int)sim.size(); i++) if (!sim[i].name.empty()) m[sim[i].name] = i;
    return m;
}

// Gather live inject into FIELD index order, by name. field_names[fn] is the node name at field
// index fn (the reference file's order). Returns inject[good_slot][field_index] in annual ducats.
// good slot k <-> model good index k-1 (spec 1.8); slot 0 is unused/gold.
inline std::vector<std::vector<double>> gather_inject(
        const std::vector<livetrade::SimNode>& sim,
        const std::vector<std::string>& field_names, int& goods_count,
        int& matched) {
    auto byname = live_by_name(sim);
    goods_count = 0;
    for (auto& s : sim) goods_count = std::max<int>(goods_count, (int)s.goods.size());
    int N = (int)field_names.size();
    std::vector<std::vector<double>> inject(goods_count, std::vector<double>(N, 0.0));
    matched = 0;
    for (int fn = 0; fn < N; fn++) {
        auto it = byname.find(field_names[fn]);
        if (it == byname.end()) continue;
        matched++;
        const auto& g = sim[it->second].goods;
        for (int k = 0; k < (int)g.size() && k < goods_count; k++) inject[k][fn] = g[k] / 1000.0;
    }
    return inject;
}

// Route one good (no-merchant baseline; econ::route with empty standings). Kept for callers that
// only need collected-at-node totals.
inline std::vector<double> route_good(int N, const std::vector<std::pair<int, int>>& directed,
                                      const std::vector<double>& inject) {
    std::vector<econ::NodeStandings> st(N);
    auto F = econ::route(N, directed, inject, st, {}, 0.05);
    return F.collected;
}

// Write the aggregate node economy back into the engine, BY NAME. Writes the node TOTAL
// (+0xCC accum) and the UI total cache; leaves local untouched (spec B4). Returns nodes written.
inline int install_aggregate(const std::vector<livetrade::SimNode>& sim,
                             const std::vector<std::string>& field_names,
                             const std::vector<econ::NodeAggregate>& agg,
                             bool write_local = false) {
    auto byname = live_by_name(sim);
    int wrote = 0;
    for (int fn = 0; fn < (int)field_names.size() && fn < (int)agg.size(); fn++) {
        auto it = byname.find(field_names[fn]);
        if (it == byname.end()) continue;
        uintptr_t node = sim[it->second].obj;
        // annual -> monthly twelfth at the engine-write boundary (spec 2.6).
        //   pool  -> +0xB0 `current`  (pass 10 divides THIS among collectors: the money)
        //   outgoing -> +0xBC
        // local (+0xB4) is left as the engine's own (spec B4). The UI recomputes
        // total = local + Σ incoming − outgoing, so no total field needs writing.
        // The engine (and every UI consumer) recomputes total = local + Σ incoming − outgoing.
        // `local` stays the ENGINE's own (spec B4) while the model's local is its own annual
        // inject; the two differ by the recorded reference-side gap (spec 2.8, ~3.4%). So the
        // model's absolute outgoing cannot be written raw -- it would exceed local+incoming and
        // drive `total` negative, which spec 1.12 forbids ever displaying.
        //
        // What is invariant is the SPLIT: the fraction of everything a node holds that it
        // forwards, outgoing/value, which is exactly 1 - collected_share aggregated over goods.
        // Applying that fraction to what the node actually holds here reproduces the model's
        // economy in the engine's own units and keeps the identity non-negative by construction.
        // The SPLIT the node applies to everything it holds: the fraction forwarded, which is
        // 1 - collected_share aggregated over goods. Using a fraction rather than the model's
        // absolute outgoing keeps the identity in the ENGINE's units, where `local` is the
        // engine's own and differs from the model's inject by the recorded reference-side gap
        // (spec 2.8). Applying the split to what the node actually holds reproduces the model's
        // economy without importing that gap, and keeps total >= 0 by construction.
        double model_value = agg[fn].total;                       // annual, model units
        double fwd = model_value > 0 ? agg[fn].outgoing / model_value : 0.0;
        if (fwd < 0) fwd = 0; if (fwd > 1) fwd = 1;
        // In a PER-GOOD view `local` is REPLACED below by the selected good's inject, so `held`
        // must be sized against the value that will actually be there when the UI recomputes
        // total = local + Sigma incoming - outgoing. Sizing it against the engine's all-goods
        // local and then writing a much smaller per-good local drove `total` negative -- which
        // is exactly what showed up on baltic_sea and novgorod in the wool view, and what spec
        // 1.12 forbids ever displaying.
        double engine_local = write_local ? (agg[fn].local / 12.0)
                                          : sim[it->second].local_value;   // monthly
        double engine_in = 0;
        for (auto& l : livetrade::read_incoming(sim[it->second].obj)) engine_in += l.value_raw / 1000.0;
        double held = engine_local + engine_in;                   // monthly
        double out = held * fwd;
        if (out < 0) out = 0;
        if (out > held) out = held;                               // total >= 0 always (spec 1.12)
        livetrade::write_outgoing(node, out);
        // value_added_outgoing. The outgoing TOOLTIP computes each destination's ducats as
        //     steer_permille[k] * node+0xC0 / 1e6
        // so leaving +0xC0 at the engine's value made the per-destination lines sum to the
        // ENGINE's outgoing while the header showed ours. The engine's own invariant is
        // +0xC0 == +0xBC; keep it.
        livetrade::write_fixed(node, 0xC0, out);
        // the collectible pool is what is NOT forwarded (spec 2.6): pass 10 divides this
        bool a = livetrade::write_pool(node, held - out);
        // In the AGGREGATE view local is never written: test B4 requires it to stay the engine's
        // own origination. In a PER-GOOD view spec 1.12 asks for all six fields to show the
        // selected good alone, so local becomes that good's inject.
        if (write_local) livetrade::write_local_value(node, agg[fn].local / 12.0);
        if (a) wrote++;
    }
    return wrote;
}


// Build `link_targets` from LIVE MEMORY -- the engine's own per-definition outgoing lists -- and
// NEVER from a tradenodes file.
//
// This was a real defect. The DLL was reading the vanilla
// `common/tradenodes/00_tradenodes.txt` while the running game had loaded the MOD's emitted file.
// Both declare the same 159 undirected edges (test A3 guarantees that), but the emitter reorders
// declarations and reverses directions: measured, 69 of 80 nodes have a DIFFERENT outgoing list
// and 77 links are declared the opposite way round. Since a merchant's steer target is stored as
// an INDEX into the engine's own outgoing list (rec+0xA8), resolving that index through the
// vanilla file pointed most steering at the wrong destination -- silently, with no error.
//
// Reading the engine's own lists removes the whole class of bug: the index is resolved against
// exactly the array it indexes.
inline std::vector<std::vector<int>> live_link_targets(
        const std::vector<std::string>& field_names,
        const std::map<int, std::string>& id_to_name,
        int& links_seen) {
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)field_names.size(); i++) fidx[field_names[i]] = i;
    std::vector<std::vector<int>> lt(field_names.size());
    links_seen = 0;
    for (uintptr_t def : arrows::definitions()) {
        int src_id = livetrade::fi(def + 0xD8);
        auto sn = id_to_name.find(src_id);
        if (sn == id_to_name.end()) continue;
        auto sf = fidx.find(sn->second);
        if (sf == fidx.end()) continue;
        uintptr_t ob = livetrade::fq(def + 0x98), oe = livetrade::fq(def + 0xA0);
        if (!ob || oe <= ob) continue;
        for (uintptr_t e = ob; e + 0x78 <= oe; e += 0x78) {
            uintptr_t tdef = livetrade::fq(e + 0x30);
            int dst_f = -1;
            if (tdef && livetrade::validate_region(tdef + 0xD8, 4)) {
                auto dn = id_to_name.find(livetrade::fi(tdef + 0xD8));
                if (dn != id_to_name.end()) {
                    auto df = fidx.find(dn->second);
                    if (df != fidx.end()) dst_f = df->second;
                }
            }
            lt[sf->second].push_back(dst_f);
            links_seen++;
        }
    }
    return lt;
}

// Read the engine's live per-node per-country standings into the routing model's form
// (spec 1.8: P_collect / P_transfer(g), steering targets, per-good eligibility).
//
//   power        = min(val, max(0, max_pow*max_demand/1000)) + t_in - t_out   [the engine's own]
//   collects     = has_trader ? (type==0) : has_capital
//   steer target = the outgoing-link index at +0xA8, resolved to a destination FIELD index
//
// `link_targets[node_field]` must list that node's outgoing link destinations in the engine's
// own link order, so a steer index can be turned into a destination node.
inline std::vector<econ::NodeStandings> read_standings_field(
        const std::vector<livetrade::SimNode>& sim,
        const std::vector<std::string>& field_names,
        const std::vector<std::vector<int>>& link_targets,
        std::map<int, std::vector<int>>& collect_nodes_out) {
    auto byname = live_by_name(sim);
    int N = (int)field_names.size();
    std::map<std::string, int> fidx_of;
    for (int i = 0; i < N; i++) fidx_of[field_names[i]] = i;
    std::vector<econ::NodeStandings> st(N);
    collect_nodes_out.clear();
    for (int fn = 0; fn < N; fn++) {
        auto it = byname.find(field_names[fn]);
        if (it == byname.end()) continue;
        for (auto& c : livetrade::read_standings(sim[it->second].obj)) {
            econ::Standing s{};
            s.country = c.tag_index;
            // A COUNTRY'S POWER AT A NODE, exactly as the engine computes it -- read out of the
            // instructions, not inferred from the save:
            //
            //   0xB594DF  movsxd rdx,[rdi+0x4C]   ; max_pow
            //   0xB594E3  movsxd rax,[rdi+0x44]   ; max_demand
            //   0xB594E7  imul   rdx,rax          ; /1000 follows
            //   0xB59503  cmovg  eax,edx          ; cap = max(0, .)
            //   0xB59506  cmp    r10d,eax         ; r10d = val (+0x48)
            //   0xB59509  cmovl  eax,r10d         ; min(val, cap)
            //   0xB5950D  add    eax,ecx          ; + (t_in - t_out)
            //
            // Two things this settles. (1) t_in - t_out is PROPAGATED power that val does NOT
            // contain: the clamp sites at 0xB52114 store the CAP into val, and the propagation
            // writes at 0xB52563/0xB525D2 touch only +0x50/+0x54. An earlier commit dropped the
            // term as "already inside val"; that was refuted at the instruction level and is
            // reverted here. (2) read_standings already divides every fixed-point field by 1000,
            // so max_demand is a fraction and max_pow is in ducats -- the bug that crushed every
            // collector to 0.002-0.07 was a SECOND /1000 on their product, nothing else.
            double capped = std::max(0.0, c.max_pow * c.max_demand);
            s.power = std::min(c.val, capped > 0 ? capped : c.val) + c.t_in - c.t_out;
            if (s.power < 0) s.power = 0;
            // USER DECISION 2026-08-26 (spec 3.14 says collect/steer is vanilla; this diverges):
            // merchants never collect. The only place a country collects is its trade capital,
            // without a merchant, and a merchant cannot be placed there. So collecting is
            // has_capital alone; a merchant record is always a steerer.
            // the ENGINE's collector set, exactly: has_trader ? type==0 : has_capital. The earlier
            // has_capital || (...) counted a TRANSFERRING merchant standing at its own capital as a
            // collector; the engine pays such a record nothing (measured: E1 country#2 predicted 0.57,
            // paid 0, with the renormalisation showing up on its neighbours).
            // DEPARTURE D1 in the division itself: only the trade capital collects. A merchant record
            // that the engine still marks type 0 (an END node, a first tick after a load, a merchant
            // in transit) gets collector share 0 from install_power_shares, so the engine pays it
            // nothing -- the rule holds without the engine having to represent it.
            s.collects = c.has_capital;
            s.is_capital = c.has_capital;
            s.pp = c.province_power;
            s.steer_to = -1;
            // A TABLE-OWNED PLACEMENT IS READ FROM THE TABLE, NOT THE RECORD. syncrec writes a
            // reverse end as +0xA8 = 0, so deriving steer_to from the record here yielded the
            // FORWARD link #0 target -- silently wrong whenever merge did not overwrite it
            // (a name miss, a poll reload, a vacated node). And the +2 merchant-present power
            // that merge granted a country with no other standing vanished the next tick,
            // because the record then existed with val 0 and merge took the found branch.
            // Both are one rule: if the table has this (country, node), the table decides
            // the target and the standing carries at least MERCHANT_MAX_POWER_BONUS.
            auto tab = assign::g_table.find({c.tag_index, field_names[fn]});
            if (tab != assign::g_table.end()) {
                auto tf = fidx_of.find(tab->second);
                if (tf != fidx_of.end()) {
                    s.steer_to = tf->second;
                    // a table entry at the country's OWN capital must not switch home collection off in
                    // the model while the engine keeps collecting there (nocollect keeps type 0 on
                    // capital records; syncrec skips them): collects stays as the engine has it
                    if (!c.has_capital) s.collects = false;
                    s.merchant_floor = true;                    // the +2 lands on the final per-good power
                    if (s.power < 2.0) s.power = 2.0;
                }
            } else if (c.has_trader && c.type == 1 && c.steer_link >= 0 &&
                fn < (int)link_targets.size() &&
                c.steer_link < (int)link_targets[fn].size())
                s.steer_to = link_targets[fn][c.steer_link];
            if (s.collects) collect_nodes_out[s.country].push_back(fn);
            st[fn].entries.push_back(s);
        }
    }
    return st;
}

// Write the per-link realized values into the engine's incoming-link records (spec 2.6's
// "per-link value": net Σ_g realized flow in the installed Phi_w direction). Each record at
// node+0xF0[i] carries the source node's DEFINITION at +0x18; the definition's node index sits at
// def+0xD8, which is the engine node id -- so a record identifies (source_id -> this node).
// `net[(u,v)]` is keyed by FIELD indices, so we translate through name<->id maps.
// Returns the number of link records written.
inline int install_links(const std::vector<livetrade::SimNode>& sim,
                         const std::vector<std::string>& field_names,
                         const std::map<std::pair<int, int>, double>& net_annual,
                         const std::map<int, std::string>& id_to_name) {
    // field index by name, for translating an engine id to a field index
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)field_names.size(); i++) fidx[field_names[i]] = i;
    auto field_of_id = [&](int id) -> int {
        auto n = id_to_name.find(id);
        if (n == id_to_name.end()) return -1;
        auto f = fidx.find(n->second);
        return f == fidx.end() ? -1 : f->second;
    };
    int wrote = 0;
    for (auto& s : sim) {
        int dst_f = field_of_id(s.index);
        if (dst_f < 0) continue;
        for (auto& l : livetrade::read_incoming(s.obj)) {
            uintptr_t src_def = l.words[3];              // +0x18 = source definition
            if (!src_def) continue;
            int src_id = livetrade::ri(src_def + 0xD8);  // def+0xD8 = node index
            int src_f = field_of_id(src_id);
            if (src_f < 0) continue;
            // GROSS directed flow src->dst: the value that actually arrives here. Never negative
            // (spec 1.12: no negative is ever displayed); a link carrying nothing this way is 0.
            auto it = net_annual.find({src_f, dst_f});
            double v = (it != net_annual.end()) ? it->second : 0.0;
            if (v < 0) v = 0;
            livetrade::write_link_value(l.rec, v / 12.0);         // annual -> monthly (spec 2.6)
            wrote++;
        }
    }
    return wrote;
}

// Write each country's share of the collectible pool into the engine's own power_fraction
// (rec+0x2C, permille), so the engine's pass 10 -- rec.total = node.current * power_fraction/1000,
// rec.money, AddDelayedIncome(country, 2 /*trade*/) -- pays out the MODEL's income with no
// second income path of our own (spec 2.6 / 3.10).
//
// spec 3.10's factorisation: whether a country collects is a merchant-or-home property with no
// good dependence, so a good-independent share multiplies a per-good sum and the sum collapses
// to one scalar. The share is therefore over COLLECTORS only: a country that steers takes none
// of the pool (its value was already forwarded).
inline std::map<std::pair<int, std::string>, double> g_written_share;   // (country index, node) -> share written this tick (E1 diagnostics)
inline std::vector<std::map<int, double>> g_share_by_node;   // [field node] country index -> share the MODEL computed this tick (E1 predicts from this)
inline int install_power_shares(const std::vector<livetrade::SimNode>& sim,
                                const std::vector<std::string>& field_names,
                                const std::vector<econ::NodeStandings>& st,
                                const std::vector<econ::GoodFlow>* per_good = nullptr,
                                const std::vector<std::vector<std::vector<double>>>* power_g_all = nullptr) {
    // DEPARTURE D3: the country's share of the node's pool is the flow-weighted per-good collector
    // share, sum_g collected_g * P_c(n,g)/P_collect(n,g) / sum_g collected_g; a non-collector (a
    // merchant the table says steers, at an END node included) gets 0 whatever the engine thinks.
    auto byname = live_by_name(sim);
    int wrote = 0;
    g_share_by_node.assign(field_names.size(), {});
    g_written_share.clear();
    for (int fn = 0; fn < (int)field_names.size() && fn < (int)st.size(); fn++) {
        auto it = byname.find(field_names[fn]);
        if (it == byname.end()) continue;
        const auto& E = st[fn].entries;
        // per-entry share
        std::vector<double> share(E.size(), 0.0);
        double tot_collected = 0;
        if (per_good && power_g_all && per_good->size() == power_g_all->size()) {
            for (size_t g = 0; g < per_good->size(); g++) {
                const econ::GoodFlow& F = (*per_good)[g];
                if (fn >= (int)F.collected.size()) continue;
                double cg = F.collected[fn]; if (cg <= 0) continue;
                const auto& P = (*power_g_all)[g];
                double pcol = 0;
                for (size_t i = 0; i < E.size(); i++) if (E[i].collects && fn < (int)P.size() && i < P[fn].size() && P[fn][i] > 0) pcol += P[fn][i];
                if (pcol <= 0) continue;
                tot_collected += cg;
                for (size_t i = 0; i < E.size(); i++) if (E[i].collects && fn < (int)P.size() && i < P[fn].size() && P[fn][i] > 0) share[i] += cg * P[fn][i] / pcol;
            }
        }
        if (tot_collected > 0) { for (auto& x : share) x /= tot_collected; }
        else {   // nothing collected here this month: fall back to the aggregate collector share
            double collector_power = 0;
            auto base = [&](const econ::Standing& e) { double v = e.has_own ? e.own : e.power; return v > 0 ? v : 0.0; };
            for (auto& e : E) if (e.collects) collector_power += base(e);
            for (size_t i = 0; i < E.size(); i++) share[i] = (collector_power > 0 && E[i].collects) ? base(E[i]) / collector_power : 0.0;
        }
        for (size_t i = 0; i < E.size(); i++) if (share[i] > 0) g_share_by_node[fn][livetrade::country_index_of(E[i].country)] = share[i];
        // write EVERY raw slot: a record read_standings filters out (nothing there) could still carry
        // the engine's -1 (0xB52B93) and yield negative income in pass 10 (reviewed)
        uintptr_t node = sim[it->second].obj;
        if (!node || !livetrade::validate_region(node + 0x18, 16)) continue;
        uintptr_t rb = livetrade::fq(node + 0x18); int rc = livetrade::fi(node + 0x24);
        if (!rb || rc <= 0 || rc > 4096 || !livetrade::validate_region(rb, (size_t)rc * 0xC0)) continue;
        for (int i = 0; i < rc; i++) {
            uintptr_t rec = rb + (uintptr_t)i * 0xC0;
            if ((livetrade::fi(rec + 0x14) & 0xFFFF) != i) continue;
            double sh = 0;
            auto sit = g_share_by_node[fn].find(i);
            if (sit != g_share_by_node[fn].end()) sh = sit->second;
            if (livetrade::write_power_fraction(rec, sh)) { wrote++; if (sh > 0) g_written_share[{i, field_names[fn]}] = sh; }
        }
    }
    return wrote;
}

// Diagnostic: dump the engine's OWN per-country standings at a few named nodes, so the meaning
// of power_fraction (share among all holders vs among collectors) can be READ rather than
// assumed before anything overwrites it.
inline void dump_standings(const std::string& logpath,
                           const std::vector<livetrade::SimNode>& sim,
                           const std::vector<std::string>& want) {
    std::ofstream log(logpath, std::ios::app);
    log << "--- engine per-country standings (rec = node+0x18 + 0xC0*i) ---\n";
    auto byname = live_by_name(sim);
    for (const std::string& nm : want) {
        auto it = byname.find(nm);
        if (it == byname.end()) continue;
        auto recs = livetrade::read_standings(sim[it->second].obj);
        double pf_sum = 0, pf_coll = 0, pow_all = 0, pow_coll = 0;
        for (auto& r : recs) {
            bool collects = r.has_trader ? (r.type == 0) : r.has_capital;
            pf_sum += r.power_fraction;
            pow_all += r.val;
            if (collects) { pf_coll += r.power_fraction; pow_coll += r.val; }
        }
        log << "  " << nm << ": " << recs.size() << " records, Σpower_fraction=" << pf_sum
            << " (collectors only " << pf_coll << "), Σval=" << pow_all
            << " (collectors " << pow_coll << ")\n";
        int shown = 0;
        for (auto& r : recs) {
            if (r.val <= 0 && !r.has_trader) continue;
            bool collects = r.has_trader ? (r.type == 0) : r.has_capital;
            log << "     tag#" << r.tag_index << " val=" << r.val << " pf=" << r.power_fraction
                << " total=" << r.total << " money=" << r.money
                << " trader=" << (int)r.has_trader << " type=" << r.type
                << " capital=" << (int)r.has_capital << " steer_link=" << r.steer_link
                << (collects ? "  [COLLECTS]" : "") << "\n";
            if (++shown >= 8) break;
        }
    }
}

// legacy signature retained for the older call path (writes routed totals to local); superseded
// by install_aggregate. Kept so nothing calling it breaks.
inline int install_economy(const std::vector<livetrade::SimNode>& sim,
                           const std::vector<double>& routed_total) {
    int wrote = 0;
    for (size_t n = 0; n < sim.size() && n < routed_total.size(); n++)
        if (livetrade::write_local_value(sim[n].obj, routed_total[n])) wrote++;
    return wrote;
}

// old read_inject (array-position keyed) kept for the monthly loop's transitional use.
inline std::vector<std::vector<double>> read_inject(const std::vector<livetrade::SimNode>& sim,
                                                    int& goods_count) {
    goods_count = 0;
    for (auto& s : sim) goods_count = std::max<int>(goods_count, (int)s.goods.size());
    std::vector<std::vector<double>> inject(goods_count, std::vector<double>(sim.size(), 0.0));
    for (size_t n = 0; n < sim.size(); n++)
        for (size_t k = 0; k < sim[n].goods.size(); k++)
            inject[k][n] = sim[n].goods[k] / 1000.0;
    return inject;
}

} // namespace install
