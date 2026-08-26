// MERCHANT ASSIGNMENT ON ANY LINK END (spec 1.7, 1.12; tests C1-C5).
//
// Spec 1.7: "the node window lists every link incident to the node ... what changes is what an
// INCOMING entry does -- it must accept a merchant assignment rather than merely navigate. A
// merchant assigned to link {n,m} steers every good oriented n->m, is inert for every good
// oriented m->n, and keeps its assignment when a link flips; only its active good set changes."
//
// Why this cannot simply be handed to the engine: `steer_command` (token 0x2DB9) writes an INDEX
// into the node's own outgoing list (rec+0xA8). The engine's outgoing list is the installed Phi_w
// orientation, so a link drawn INTO n has no index at n to name -- there is nothing to write. But
// the per-good graphs disagree with Phi_w on 45% of edge-goods (spec 1.6), so "the goods oriented
// n->m" is very often non-empty on a link that Phi_w draws m->n. That is exactly the case the
// spec wants assignable, and exactly the case the engine cannot express.
//
// So the assignment lives here, keyed by (country, node) -> target node, and is merged into the
// routing model's per-node standings. The engine's own assignments are still read and honoured;
// this table only adds the ends the engine has no index for, and takes precedence where both
// exist. Because it is keyed by link END rather than by link index, it survives a flip untouched
// -- only the good set the merchant is active on changes, which is precisely spec 1.7's rule.
#pragma once
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include <cstdio>
#include "livetrade.h"
#include "../src/economy.h"

namespace assign {

// (country tag index, node name) -> target node name
inline std::map<std::pair<int, std::string>, std::string> g_table;
inline bool g_dirty = false;

inline void set(int country, const std::string& node, const std::string& target) {
    g_table[{country, node}] = target;
    g_dirty = true;
}
inline void clear(int country, const std::string& node) {
    g_table.erase({country, node});
    g_dirty = true;
}

// Read assignments from a marker file, one per line: "<countryIdx> <node> <target>".
// This is the test harness for C2/C3 (the player-facing trigger is the node-window click, which
// the engine already routes to the assignment dispatcher -- only its gate refuses).
inline void poll(const std::string& logpath) {
    if (!livetrade::marker_present("ASSIGN")) return;
    std::ifstream f(livetrade::self_dir() + "\\pgt.ASSIGN");
    std::string line;
    std::map<std::pair<int, std::string>, std::string> next;
    while (std::getline(f, line)) {
        while (!line.empty() && (line.back() == '\r' || line.back() == '\n')) line.pop_back();
        if (line.empty() || line[0] == '#') continue;
        int c = 0; char node[128] = {0}, tgt[128] = {0};
        if (sscanf(line.c_str(), "%d %127s %127s", &c, node, tgt) == 3)
            next[{c, std::string(node)}] = std::string(tgt);
    }
    if (next != g_table) {
        g_table = next;
        std::ofstream log(logpath, std::ios::app);
        log << "  [assign] " << g_table.size() << " DLL-owned merchant assignments loaded\n";
        for (auto& [k, v] : g_table)
            log << "     country#" << k.first << " at " << k.second << " steers toward " << v << "\n";
    }
}

// Merge the table into the routing standings. `names` is field index -> node name.
// Returns how many standings were overridden or added.
inline int merge(std::vector<econ::NodeStandings>& st, const std::vector<std::string>& names) {
    if (g_table.empty()) return 0;
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)names.size(); i++) fidx[names[i]] = i;
    int applied = 0;
    for (auto& [key, target] : g_table) {
        auto nf = fidx.find(key.second);
        auto tf = fidx.find(target);
        if (nf == fidx.end() || tf == fidx.end()) continue;
        econ::NodeStandings& ns = st[nf->second];
        bool found = false;
        for (auto& e : ns.entries)
            if (e.country == key.first) {
                // A merchant the engine says is COLLECTING here stays a collector. This
                // table only adds steering on ends the engine has no index for; it must
                // never convert a collector, because that is the country's income at
                // this node and the engine is the authority on what its merchant is
                // doing. Unconditionally clearing `collects` was how Venice -- over half
                // the power in venice, collecting -- saw almost all of it forwarded.
                if (e.collects) { found = true; break; }
                e.steer_to = tf->second;      // steer, not collect (spec 1.7)
                found = true;
                applied++;
                break;
            }
        if (!found) {
            // the country holds no power here yet; a merchant present is still +2 power
            // (MERCHANT_MAX_POWER_BONUS) and steers, so it belongs in the standings.
            econ::Standing s{};
            s.country = key.first;
            s.power = 2.0;
            s.collects = false;
            s.steer_to = tf->second;
            ns.entries.push_back(s);
            applied++;
        }
    }
    return applied;
}

} // namespace assign
