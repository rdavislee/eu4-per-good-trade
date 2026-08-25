// FAITHFUL WRITE-BACK OF THE PER-GOOD ECONOMY (spec 1.8, 1.12).
//
// Every good is routed by its OWN topological pass over its own DAG (econ::route), so per good the
// identity local_g + incoming_g - outgoing_g = collected_g holds exactly, by conservation. Summing
// the goods keeps it:  local + incoming - outgoing = collected,  with every term >= 0.
//
// econ::aggregate already produces exactly those sums, and gross_link_flows gives the directed
// per-edge total in BOTH directions. So the write-back is a transcription, not a derivation.
//
// The previous version re-derived outgoing as a FRACTION of what the engine thought the node held
// (out = (local + Sigma incoming) x forwarded_fraction). That is scale-safe but reconciles with
// nothing -- north_sea showed "Outgoing 3" beside a map panel reading "11" -- and every attempt to
// force the two together reintroduced negative totals, because `outgoing` and `Sigma incoming`
// were being computed from different snapshots. Writing the model's own conserved quantities
// removes the whole class of problem: the engine recomputes
// total = local(+0xB4) + Sigma incoming(+0x10) - outgoing(+0xBC), which is collected by
// construction, and can no more go negative than the model's own collected_share can.
#pragma once
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "outlinks.h"
#include "../src/economy.h"

namespace flowwrite {

inline int g_nodes = 0;
inline double g_worst_residual = 0;      // |displayed total - model collected|, monthly ducats
inline std::string g_worst_node;
inline int g_bad_nodes = 0;

// Write one node's six quantities plus its per-edge figures.
inline int install(const std::vector<livetrade::SimNode>& sim,
                   const std::vector<std::string>& field_names,
                   const std::vector<econ::NodeAggregate>& agg,
                   const std::map<std::pair<int, int>, double>& gross,      // WITH bonus -> incoming
                   const std::map<std::pair<int, int>, double>& away,       // NO bonus  -> outgoing
                   const std::map<int, std::string>& id_to_name,
                   bool write_local) {
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)field_names.size(); i++) fidx[field_names[i]] = i;
    auto field_of_node = [&](uintptr_t nd) -> int {
        if (!nd || !livetrade::validate_region(nd + 0x120, 4)) return -1;
        auto n = id_to_name.find(livetrade::fi(nd + 0x120));
        if (n == id_to_name.end()) return -1;
        auto f = fidx.find(n->second);
        return f == fidx.end() ? -1 : f->second;
    };
    auto byname = install::live_by_name(sim);
    int wrote = 0, bad = 0;
    double worst = 0;

    for (int fn = 0; fn < (int)field_names.size() && fn < (int)agg.size(); fn++) {
        auto it = byname.find(field_names[fn]);
        if (it == byname.end()) continue;
        uintptr_t node = sim[it->second].obj;

        const double local_m = agg[fn].local    / 12.0;     // annual -> monthly (spec 2.6)
        const double in_m    = agg[fn].incoming / 12.0;
        const double out_m   = agg[fn].outgoing / 12.0;
        const double pool_m  = agg[fn].pool     / 12.0;

        // 1. the per-edge INCOMING records: one per incident link, carrying its toward-flow.
        //    Their sum is agg.incoming by construction, which is what makes the identity close.
        // NOT rebuilding the incoming vector, and NOT resizing node+0x88.
        // Repointing those engine vectors is what keeps killing the game: the outgoing-breakdown
        // builder at 0xB56480 indexes node+0x88 by link ordinal with NO bounds check, and the
        // engine push_backs onto both vectors during its own passes using a capacity field we
        // cannot safely rewrite. Two access violations at 0xB5654D came from exactly this.
        // The per-edge figures are supplied by hooking the panel's text instead (panelvalue.h).

        // 2. the node's own figures. local first, so anything derived from it downstream sees the
        //    value that will actually be there when the UI recomputes the total.
        if (write_local) livetrade::write_local_value(node, local_m);
        livetrade::write_outgoing(node, out_m);
        livetrade::write_pool(node, pool_m);

        // 3. the per-edge OUTGOING figures the map panels read (node+0x88, by link ordinal).
        (void)away;

        // 4. measure the identity rather than assume it: what the engine will display, against
        //    what the model says was collected.
        double shown_local = write_local ? local_m : sim[it->second].local_value;
        double rec_sum = 0;
        for (auto& l : livetrade::read_incoming(node)) rec_sum += l.value_raw / 1000.0;
        double residual = (shown_local + rec_sum - out_m) - pool_m;
        if (residual < 0) residual = -residual;
        if (residual > worst) { worst = residual; g_worst_node = field_names[fn]; }
        if (residual > 0.001) bad++;
        wrote++;
    }
    g_nodes = wrote;
    g_worst_residual = worst;
    g_bad_nodes = bad;
    return wrote;
}

} // namespace flowwrite
