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
    std::vector<econ::NodeStandings> st(N);
    collect_nodes_out.clear();
    for (int fn = 0; fn < N; fn++) {
        auto it = byname.find(field_names[fn]);
        if (it == byname.end()) continue;
        for (auto& c : livetrade::read_standings(sim[it->second].obj)) {
            econ::Standing s{};
            s.country = c.tag_index;
            // A COUNTRY'S POWER AT A NODE IS `val`, full stop.
            //
            // This used to be min(val, max_pow * max_demand) + t_in - t_out, which is an
            // invention: no define, string or spec line names it, and it has two failure modes.
            // The cap silently demotes a country whose max_demand has been adjusted below 1,
            // and the t_in - t_out term adds a component that is ALREADY inside val. Aragon
            // holds the largest standing in valencia by a wide margin and collects there, and
            // was earning almost nothing, because its payout share is power / SUM(collector
            // power) and the cap had cut its power down.
            //
            // The engine settles what val means: the field map verifies node+0xC8 `total` --
            // the node's total trade power, the figure the node window shows -- equals the SUM
            // of the per-country `val` on 77 of 80 nodes. So val is exactly the per-country
            // modified power in the node's own accounting, and CalcPower has already folded the
            // merchant bonus, the off-home penalty, propagation and the caravan grant into it.
            //
            // (The earlier bug here was narrower and is fixed too: read_standings divides every
            // fixed-point field by 1000, so max_demand was already a fraction and the cap was
            // dividing by 1000 a second time, making every capped power 1000x too small.)
            s.power = c.val > 0 ? c.val : 0.0;
            if (s.power < 0) s.power = 0;
            s.collects = c.has_trader ? (c.type == 0) : c.has_capital;
            s.steer_to = -1;
            if (c.has_trader && c.type == 1 && c.steer_link >= 0 &&
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
inline int install_power_shares(const std::vector<livetrade::SimNode>& sim,
                                const std::vector<std::string>& field_names,
                                const std::vector<econ::NodeStandings>& st) {
    auto byname = live_by_name(sim);
    int wrote = 0;
    for (int fn = 0; fn < (int)field_names.size() && fn < (int)st.size(); fn++) {
        auto it = byname.find(field_names[fn]);
        if (it == byname.end()) continue;
        double collector_power = 0;
        for (auto& e : st[fn].entries) if (e.collects && e.power > 0) collector_power += e.power;
        auto recs = livetrade::read_standings(sim[it->second].obj);
        for (auto& r : recs) {
            // find this country's modelled standing
            double share = 0;
            if (collector_power > 0)
                for (auto& e : st[fn].entries)
                    if (e.country == r.tag_index && e.collects && e.power > 0) {
                        share = e.power / collector_power;
                        break;
                    }
            if (livetrade::write_power_fraction(r.rec, share)) wrote++;
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
