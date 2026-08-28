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
#include <mutex>
#include <atomic>
#include "livetrade.h"
#include "../src/economy.h"

namespace assign {

// (COUNTRY INDEX, node name) -> target node name.
//
// THE KEY IS THE BARE COUNTRY INDEX (low 16 bits of the record's tag dword at rec+0x14). The AI
// writers pass the raw dword (0x010000b9 for Castile) and the player's click passes the index
// (0xb9); until 2026-08-26 both were stored verbatim, so a click entry never matched the
// record's standing in install.h and merge() ADDED a second standing keyed 0x000000b9 with power
// 2 and no received power -- written to the same record slot AFTER the real one (measured at
// valencia: 4.72 model, 2.00 on screen). set()/clear() normalise; every exact lookup does too.
inline std::map<std::pair<int, std::string>, std::string> g_table;
inline bool g_dirty = false;
inline std::mutex g_mx;                          // writers and the sidecar serialiser (the save writer may be off the game thread; reviewed)
inline std::atomic<bool> g_in_loading{false};    // set by the loading-path wrapper for its whole duration (earlyload.h)
inline bool g_skip_startup_once = false;         // a restored sidecar: the opening re-placement must not override the saved targets
inline int g_merge_applied = 0, g_merge_kept_collector = 0, g_merge_added = 0, g_merge_noname = 0, g_merge_bareidx = 0;
inline std::string g_merge_noname_example;

inline void set(int country, const std::string& node, const std::string& target) {
    std::lock_guard<std::mutex> lk(g_mx);
    g_table[{country & 0xFFFF, node}] = target;
    g_dirty = true;
}
inline void clear(int country, const std::string& node) {
    std::lock_guard<std::mutex> lk(g_mx);
    g_table.erase({country & 0xFFFF, node});
    g_dirty = true;
}

// SIDECAR PERSISTENCE (user, 2026-08-26): the table is what a save cannot carry (a reverse-end
// merchant is stored by the engine as 'transfer, link 0'), so it is written next to every save as
// <save>.pgt in the marker-file format and read back on load. Lines: '<countryIdx> <node> <target>'.
inline int g_sidecar_written = 0, g_sidecar_loaded = 0;
inline bool write_file(const std::string& path) {
    std::ofstream f(path, std::ios::trunc);
    if (!f) return false;
    f << "# per-good-trade assignment table: countryIdx node target" << (char)10;
    { std::lock_guard<std::mutex> lk(g_mx);
      for (auto& [k, v] : g_table) f << k.first << ' ' << k.second << ' ' << v << (char)10; }
    g_sidecar_written++;
    return (bool)f;
}
inline bool read_file(const std::string& path, std::map<std::pair<int, std::string>, std::string>* out) {
    std::ifstream f(path);
    if (!f) return false;
    std::string line;
    while (std::getline(f, line)) {
        while (!line.empty() && (line.back() == (char)13 || line.back() == (char)10)) line.pop_back();
        if (line.empty() || line[0] == '#') continue;
        int c = 0; char node[128] = {0}, tgt[128] = {0};
        if (sscanf(line.c_str(), "%d %127s %127s", &c, node, tgt) == 3) (*out)[{c & 0xFFFF, std::string(node)}] = std::string(tgt);
    }
    if (out->empty()) return false;   // an empty or placeholder file is not a restore (reviewed)
    g_sidecar_loaded++;
    return true;
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
            next[{c & 0xFFFF, std::string(node)}] = std::string(tgt);   // the same convention as set()
    }
    std::lock_guard<std::mutex> lk(g_mx);
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
    std::lock_guard<std::mutex> lk(g_mx);          // the save thread may serialise the table meanwhile (reviewed)
    std::map<int, int> dword_of;   // country index -> its raw tag dword (any standing anywhere carries it)
    for (auto& ns0 : st) for (auto& e0 : ns0.entries) dword_of.emplace(e0.country & 0xFFFF, e0.country);
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
            if ((e.country & 0xFFFF) == key.first) {
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
            // carry the country's RAW tag dword (any standing of it anywhere has one), so the split
            // propagation's receipts -- keyed by the dword -- land on this standing, not on a twin
            { auto d = dword_of.find(key.first); s.country = d != dword_of.end() ? d->second : key.first; if (d == dword_of.end()) g_merge_bareidx++; }
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
