// ONE VALUE PER PHYSICAL LINK, WRITTEN AT BOTH ENDS (spec 1.12; the B3 reconciliation).
//
// Every trade node owns a per-incident-link vector at node+0xF0 (0x20-byte entries; entry+0x18 is
// the OTHER end's definition, entry+0x10 the int32 value x1000). Both the node window's link rows
// and the on-map trade_route_branch panel read it -- the panel for the arrow n->m looks up node n's
// vector for the entry whose +0x18 is m's definition (0x13379E9..0x1337B94).
//
// The old install_links filled each node's vector with the flow INTO that node, which makes the two
// ends of one link disagree: english_channel's entry for north_sea held north_sea->english_channel,
// while north_sea's entry for english_channel held the REVERSE flow -- and the view labels that one
// as outgoing. So the same link read 11 at one end and 3 at the other.
//
// A physical link has ONE drawn direction (Phi_w) and therefore one number. Compute it once, from
// the definition's own outgoing list, and write it into BOTH endpoints' vectors.
#pragma once
#include <map>
#include <string>
#include <fstream>
#include <vector>
#include "livetrade.h"
#include "outlinks.h"

namespace linkvalue {

inline int g_written = 0, g_mismatched = 0;

inline int install(const std::vector<livetrade::SimNode>& sim,
                   const std::vector<std::string>& field_names,
                   const std::map<std::pair<int, int>, double>& flow,   // annual, directed
                   const std::map<int, std::string>& id_to_name) {
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)field_names.size(); i++) fidx[field_names[i]] = i;
    auto field_of_node = [&](uintptr_t nd) -> int {
        if (!nd || !livetrade::validate_region(nd + 0x120, 4)) return -1;
        auto n = id_to_name.find(livetrade::fi(nd + 0x120));
        if (n == id_to_name.end()) return -1;
        auto f = fidx.find(n->second);
        return f == fidx.end() ? -1 : f->second;
    };
    auto field_of_def = [&](uintptr_t def) -> int {
        return field_of_node(outlinks::node_of_def_pub(def));
    };
    // does `node` declare an outgoing entry to `other_def`?  (i.e. is the link DRAWN this way)
    auto drawn_from = [&](uintptr_t node, uintptr_t other_def) -> bool {
        int n = outlinks::def_out_count(node);
        for (int i = 0; i < n; i++) {
            uintptr_t def = livetrade::fq(node + 0xA8);
            if (!def) return false;
            uintptr_t b = livetrade::fq(def + 0x98);
            if (!b) return false;
            uintptr_t e = b + (uintptr_t)i * 0x78;
            if (!livetrade::validate_region(e + 0x30, 8)) continue;
            if (livetrade::fq(e + 0x30) == other_def) return true;
        }
        return false;
    };

    int wrote = 0;
    for (auto& s : sim) {
        int self_f = field_of_node(s.obj);
        if (self_f < 0) continue;
        for (auto& l : livetrade::read_incoming(s.obj)) {
            uintptr_t other_def = l.words[3];
            if (!other_def) continue;
            int other_f = field_of_def(other_def);
            if (other_f < 0) continue;
            // node+0xF0 is the INCOMING list: every record here is a link drawn INTO this node,
            // and the engine sums them all as inflow. So the value is always the TOWARD flow.
            // (The away flow for out-drawn links lives in node+0x88 -- see outlinks::write_slots.)
            auto it = flow.find(std::make_pair(other_f, self_f));
            double v = (it != flow.end() && it->second > 0) ? it->second / 12.0 : 0.0;
            livetrade::write_link_value(l.rec, v);
            wrote++;
        }
    }
    g_written = wrote;
    return wrote;
}


// ASSERT the model's own rule, which is a CROSS-match, not a symmetry.
//
// A physical edge {A,B} carries TWO disjoint figures: F(A->B), the goods oriented A->B, and
// F(B->A), the rest. Both belong at both ends:
//     A.incoming[B] == B.outgoing[A] == F(B->A)
//     A.outgoing[B] == B.incoming[A] == F(A->B)
// So the check is not "both ends hold the same number" -- that was wrong, and asserting it drove
// away-flows into the incoming totals. The check is that each node's stored inbound figure for a
// neighbour equals the model's flow FROM that neighbour.
inline int g_missing_logged = 0;
inline bool g_dumped_map = false;
inline bool g_dumped_atlantic = false;

inline void assert_flows(const std::vector<livetrade::SimNode>& sim,
                         const std::vector<std::string>& field_names,
                         const std::map<std::pair<int, int>, double>& flow,
                         const std::map<int, std::string>& id_to_name,
                         std::ofstream& lg) {
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)field_names.size(); i++) fidx[field_names[i]] = i;
    auto field_of_node = [&](uintptr_t nd) -> int {
        if (!nd || !livetrade::validate_region(nd + 0x120, 4)) return -1;
        auto n = id_to_name.find(livetrade::fi(nd + 0x120));
        if (n == id_to_name.end()) return -1;
        auto f = fidx.find(n->second);
        return f == fidx.end() ? -1 : f->second;
    };
    // ONE-OFF: the engine index -> model field mapping, and each node's record count. A record
    // that resolves to field -1 is a NAME mapping failure, not a bad pointer, and a node with
    // fewer records than incident links means the rebuild did not cover it (or was overwritten).
    if (!g_dumped_map) {
        g_dumped_map = true;
        lg << "    [map] sim nodes = " << sim.size() << ", model fields = "
           << field_names.size() << (char)10;
        for (auto& s2 : sim) {
            int idx = livetrade::validate_region(s2.obj + 0x120, 4)
                        ? livetrade::fi(s2.obj + 0x120) : -1;
            auto n = id_to_name.find(idx);
            std::string nm = (n == id_to_name.end()) ? std::string("<no name>") : n->second;
            int f = -1;
            auto fit = fidx.find(nm);
            if (fit != fidx.end()) f = fit->second;
            size_t nrec = livetrade::read_incoming(s2.obj).size();
            if (f < 0 || nrec == 0)
                lg << "    [map] idx=" << idx << " name=" << nm << " field=" << f
                   << " records=" << nrec << "   <-- UNMAPPED" << (char)10;
        }
    }
    // ONE-OFF: every directed model flow touching a New World / Atlantic node. Before
    // colonisation these links should carry essentially nothing, so any substantial number here
    // is either a real model output or a wiring error, and the two must be told apart.
    if (!g_dumped_atlantic) {
        g_dumped_atlantic = true;
        static const char* watch[] = {"st_lawrence", "north_sea", "carribean_trade",
                                      "chesapeake_bay", "ohio", "james_bay", "mississippi_river",
                                      "bordeaux", "english_channel", "sevilla", "ivory_coast"};
        for (auto& [k, v] : flow) {
            if (v <= 0) continue;
            if (k.first < 0 || k.first >= (int)field_names.size()) continue;
            if (k.second < 0 || k.second >= (int)field_names.size()) continue;
            const std::string& a = field_names[k.first];
            const std::string& b = field_names[k.second];
            bool hit = false;
            for (auto* w : watch) if (a == w || b == w) { hit = true; break; }
            if (!hit) continue;
            lg << "    [flow] " << a << " -> " << b << "  " << (v / 12.0)
               << " ducats/month" << (char)10;
        }
    }
    int checked = 0, bad = 0, missing = 0;
    double worst = 0; std::string worst_at, worst_from;
    for (auto& s : sim) {
        int self_f = field_of_node(s.obj);
        if (self_f < 0) continue;
        // every neighbour the model sends value to this node from must have a record here
        std::map<int, double> have;
        for (auto& l : livetrade::read_incoming(s.obj)) {
            int of = field_of_node(outlinks::node_of_def_pub(l.words[3]));
            if (of >= 0) have[of] = l.value_raw / 1000.0;
        }
        for (auto& [k, v] : flow) {
            if (k.second != self_f || v <= 0) continue;
            checked++;
            double want = v / 12.0;
            auto it = have.find(k.first);
            if (it == have.end()) {
                missing++; bad++;
                // NAME them. A count cannot be acted on: these are exactly the directed inflows
                // whose panel has no record to read, so they are the panels that show nothing.
                if (g_missing_logged < 40) {
                    g_missing_logged++;
                    lg << "    [flowassert/missing] " << field_names[self_f] << " <- "
                       << field_names[k.first] << "  want " << want << (char)10;
                }
                continue;
            }
            double d = it->second - want; if (d < 0) d = -d;
            if (d > 0.0005) {
                bad++;
                if (d > worst) { worst = d; worst_at = field_names[self_f];
                                 worst_from = field_names[k.first]; }
            }
        }
    }
    lg << "  [flowassert] " << bad << " of " << checked
       << " directed inflows wrong (" << missing << " have no record at the destination)";
    if (worst > 0) lg << "; worst at " << worst_at << " from " << worst_from
                      << " off by " << worst;
    lg << "\n";;
}

} // namespace linkvalue
