// WHAT STORES A NODE'S ORIGINAL LINK COUNT? (the relink blocker)
//
// Repointing every definition at our own outgoing arrays is stable as long as the DIRECTIONS are
// unchanged; reversing even one link crashes. So some other structure is sized by, or indexed
// against, each node's original outgoing count or link order. The engine can only compare against
// an "original" if that original is stored somewhere -- so find every such store, and the
// disagreement disappears.
//
// This scans each runtime CTradeNode for {begin,end} pairs whose element count equals that node's
// definition outgoing or incoming count, and reports the offsets that match consistently across
// many nodes. Those offsets are the per-link parallel arrays that must be rebuilt whenever a
// node's link set changes. Measurement, not assumption.
#pragma once
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "arrows.h"

namespace countscan {

struct Hit { int off = 0; int elem = 0; int matched_out = 0; int matched_in = 0; int seen = 0; };

inline void scan(const std::string& logpath, const std::vector<livetrade::SimNode>& sim) {
    std::ofstream log(logpath, std::ios::app);
    log << "--- COUNT SCAN: runtime arrays sized by a node's link counts ---\n";

    // definition (by node index) -> its outgoing / incoming counts
    std::map<int, std::pair<int, int>> counts;
    for (uintptr_t d : arrows::definitions()) {
        int idx = livetrade::fi(d + 0xD8);
        uintptr_t ob = livetrade::fq(d + 0x98), oe = livetrade::fq(d + 0xA0);
        uintptr_t ib = livetrade::fq(d + 0x80), ie = livetrade::fq(d + 0x88);
        int nout = (ob && oe > ob) ? (int)((oe - ob) / 0x78) : 0;
        int nin  = (ib && ie > ib) ? (int)((ie - ib) / 8) : 0;
        counts[idx] = {nout, nin};
    }

    // for every 8-byte slot in the node, treat it as {begin,end} and see whether the implied
    // element count tracks that node's outgoing or incoming count
    std::map<int, std::map<int, Hit>> stats;   // offset -> element size -> stats
    int nodes_used = 0;
    for (auto& s : sim) {
        auto c = counts.find(s.index);
        if (c == counts.end()) continue;
        int nout = c->second.first, nin = c->second.second;
        if (nout == 0 && nin == 0) continue;
        nodes_used++;
        for (int off = 0x08; off <= 0x130; off += 8) {
            uintptr_t b = livetrade::fq(s.obj + off);
            uintptr_t e = livetrade::fq(s.obj + off + 8);
            if (!b || e <= b) continue;
            size_t span = e - b;
            if (span > 64 * 1024) continue;
            for (int esz : {4, 8, 0x10, 0x18, 0x20, 0x28, 0x30}) {
                if (span % esz) continue;
                int n = (int)(span / esz);
                if (n <= 0 || n > 64) continue;
                Hit& h = stats[off][esz];
                h.off = off; h.elem = esz; h.seen++;
                if (n == nout) h.matched_out++;
                if (n == nin) h.matched_in++;
            }
        }
    }
    log << "  scanned " << nodes_used << " nodes\n";
    for (auto& [off, bysz] : stats)
        for (auto& [esz, h] : bysz) {
            if (h.seen < nodes_used / 2) continue;
            bool out_hit = h.matched_out >= nodes_used - 2;
            bool in_hit  = h.matched_in  >= nodes_used - 2;
            if (!out_hit && !in_hit) continue;
            log << "  node+0x" << std::hex << off << std::dec << " {begin,end} elem=0x"
                << std::hex << esz << std::dec
                << "  matches " << (out_hit ? "OUTGOING" : "") << (in_hit ? "INCOMING" : "")
                << " count on " << (out_hit ? h.matched_out : h.matched_in)
                << "/" << nodes_used << " nodes  <== per-link array, must be rebuilt\n";
        }

    // plain int32 fields that equal the node's outgoing count
    std::map<int, int> intmatch;
    for (auto& s : sim) {
        auto c = counts.find(s.index);
        if (c == counts.end()) continue;
        for (int off = 0x08; off <= 0x134; off += 4)
            if (livetrade::fi(s.obj + off) == c->second.first) intmatch[off]++;
    }
    for (auto& [off, n] : intmatch)
        if (n >= nodes_used - 2)
            log << "  node+0x" << std::hex << off << std::dec
                << " is an int32 equal to the OUTGOING count on " << n << "/" << nodes_used
                << " nodes  <== a stored 'original' count\n";
}

} // namespace countscan
