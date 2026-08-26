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
inline int g_merge_applied = 0, g_merge_kept_collector = 0, g_merge_added = 0, g_merge_noname = 0;
inline std::string g_merge_noname_example;

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
        if (nf == fidx.end() || tf == fidx.end()) {
            g_merge_noname++;
            if (g_merge_noname_example.empty()) g_merge_noname_example = key.second + " -> " + target;
            continue;
        }
        econ::NodeStandings& ns = st[nf->second];
        bool found = false;
        for (auto& e : ns.entries)
            if (e.country == key.first) {
                // THE TABLE IS THE DECISION. An earlier guard here refused to convert a merchant
                // the engine marked as collecting -- and vetoed every placement the AI made: 96
                // table entries, merge applied=0, kept_collector=107, measured. The AI has ALREADY
                // weighed collecting against steering (score_collect vs score_steer with the x1.5
                // margin, aiwire.h), so a table entry for a collecting merchant is the outcome of
                // that comparison, not a mistake to be corrected. Protecting home-node collectors
                // from being pushed onto links is the AI's job, and it does it upstream.
                // A steering merchant is NOT a collector. econ::route takes the collect branch
                // FIRST (`if (s.collects) { pc += power; continue; }`) and never reads
                // steer_to for a collecting standing -- so setting steer_to while leaving
                // collects=true wrote a placement the router silently ignored. That is the
                // exact state measured after the guard above was removed: 101 placements,
                // merge applied=0, no reverse target ever reaching a standing.
                e.steer_to = tf->second;      // steer, not collect (spec 1.7)
                e.collects = false;
                found = true;
                applied++; g_merge_applied++;
                break;
            }
        // The found branch above is now redundant with read_standings_field, which reads a
        // table-owned placement directly; it stays as the fallback for a standing built
        // elsewhere. The not-found branch below is the only path that still adds anything.
        if (!found) {
            // the country holds no power here yet; a merchant present is still +2 power
            // (MERCHANT_MAX_POWER_BONUS) and steers, so it belongs in the standings.
            econ::Standing s{};
            s.country = key.first;
            s.power = 2.0;
            s.collects = false;
            s.steer_to = tf->second;
            ns.entries.push_back(s);
            applied++; g_merge_added++;
        }
    }
    return applied;
}

} // namespace assign
