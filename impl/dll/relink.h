// REORIENT THE DEFINITION GRAPH (spec 1.12 / 2.4; tests B1, B3, C1, D1, F1).
//
// Reversing a route's drawn polyline changed nothing on screen, and the node window's
// incoming/outgoing tabs did not move either. That second symptom is the diagnosis: those tabs
// are built from the DEFINITION graph (each definition's outgoing entry vector), not from render
// geometry. So the drawing was never the thing to change -- the link structure is.
//
// A link A->B is one 0x78-byte entry inside A's outgoing vector (def+0x98/+0xA0/+0xA8), carrying
// the destination definition at +0x30, the destination's name at +0x10, and the drawn polyline at
// +0x58/+0x60. B's incoming vector (def+0x80/+0x88/+0x90) lists A. To reverse the link, the entry
// has to MOVE to B's outgoing vector and point at A, and the incoming lists have to follow.
//
// The engine's own vectors are exactly sized (end == capacity_end), so nothing can be appended in
// place. This module therefore OWNS the arrays: at attach it snapshots every definition and every
// entry, then for any requested orientation it fills its own per-definition outgoing and incoming
// arrays (capacity = that node's incident-link count, so any orientation fits) and repoints the
// definition's three-pointer vectors at them. The engine never grows or frees these, because it
// only reads them after load.
//
// An entry for the reversed direction is built by copying the original 0x78 bytes and fixing
// three fields: the destination definition (+0x30), the destination name (+0x10, an MSVC
// std::string -- SSO when <= 15 chars, otherwise a heap pointer we own), and the polyline, which
// is reversed so the ribbon is drawn from the new source outward.
#pragma once
#include <windows.h>
#include <cstring>
#include <fstream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <deque>
#include "livetrade.h"
#include "arrows.h"

namespace relink {

constexpr int D_NAME      = 0x10;   // inline std::string (size +0x20, cap +0x28)
constexpr int D_IN_BEGIN  = 0x80;   // incoming {begin,end,cap_end}, stride 8 (definition ptrs)
constexpr int D_IN_END    = 0x88;
constexpr int D_IN_CAP    = 0x90;
constexpr int D_OUT_BEGIN = 0x98;   // outgoing {begin,end,cap_end}, stride 0x78 (inline entries)
constexpr int D_OUT_END   = 0xA0;
constexpr int D_OUT_CAP   = 0xA8;
constexpr int D_INDEX     = 0xD8;
constexpr int E_NAME      = 0x10;   // entry: destination name (std::string)
constexpr int E_TARGET    = 0x30;   // entry: destination definition*
constexpr int E_POLY_B    = 0x58;   // entry: polyline {begin,end} of float2
constexpr int E_POLY_E    = 0x60;
constexpr int E_STRIDE    = 0x78;

struct Link {
    int a = -1, b = -1;                    // node indices, as originally declared a -> b
    std::vector<uint8_t> entry;            // the original 0x78 entry bytes (lives in a's list)
    std::vector<uint8_t> poly;             // the original polyline bytes (float2 array)
};

struct DefInfo {
    uintptr_t obj = 0;
    int index = -1;
    std::string name;
    std::vector<int> incident;             // indices into g_links
};

inline std::map<int, DefInfo> g_defs;       // node index -> definition
inline std::vector<Link> g_links;
inline std::map<int, std::vector<uint8_t>> g_out_storage;    // node index -> entry array bytes
inline std::map<int, std::vector<uintptr_t>> g_in_storage;   // node index -> incoming ptr array
// deque, NOT vector: a vector reallocates on growth and would dangle every name pointer
// already handed to the engine -- that crashed the game on the first run.
inline std::deque<std::string> g_name_pool;
inline bool g_ready = false;
inline std::string g_log;

// read an MSVC std::string at `s`
inline std::string read_str(uintptr_t s) {
    if (!livetrade::validate_region(s, 0x20)) return "";
    uint64_t size = (uint64_t)livetrade::fq(s + 0x10);
    uint64_t cap  = (uint64_t)livetrade::fq(s + 0x18);
    if (size > 512) return "";
    if (cap >= 16) {
        uintptr_t p = livetrade::fq(s);
        if (!p || !livetrade::validate_region(p, size)) return "";
        return std::string((const char*)p, (size_t)size);
    }
    char buf[17] = {0};
    memcpy(buf, (const void*)s, 16);
    return std::string(buf, (size_t)(size < 16 ? size : 15));
}

// write an MSVC std::string into the 0x20 bytes at `s`. Short names go in the inline buffer;
// long ones point at a string we keep alive for the process lifetime.
inline void write_str(uintptr_t s, const std::string& v) {
    DWORD old = 0;
    if (!VirtualProtect((void*)s, 0x20, PAGE_READWRITE, &old)) return;
    if (v.size() <= 15) {
        memset((void*)s, 0, 16);
        memcpy((void*)s, v.data(), v.size());
        *(uint64_t*)(s + 0x10) = v.size();
        *(uint64_t*)(s + 0x18) = 15;
    } else {
        g_name_pool.push_back(v);
        const std::string& kept = g_name_pool.back();
        *(uintptr_t*)s = (uintptr_t)kept.c_str();
        *(uint64_t*)(s + 0x10) = kept.size();
        *(uint64_t*)(s + 0x18) = kept.size() + 1;   // >= 16 so the engine reads the pointer
    }
    VirtualProtect((void*)s, 0x20, old, &old);
}

// Snapshot every definition and every declared link. Runs once, on a worker thread.
inline bool capture(std::ofstream& log) {
    if (g_ready) return true;
    auto defs = arrows::definitions();
    if (defs.size() < 40) { log << "  [relink] too few definitions (" << defs.size() << ")\n"; return false; }
    g_defs.clear(); g_links.clear();
    for (uintptr_t d : defs) {
        DefInfo di;
        di.obj = d;
        di.index = livetrade::fi(d + D_INDEX);
        di.name = read_str(d + D_NAME);
        if (di.index < 0) continue;
        g_defs[di.index] = di;
    }
    // every outgoing entry of every definition is one physical link
    for (auto& [idx, di] : g_defs) {
        uintptr_t ob = livetrade::fq(di.obj + D_OUT_BEGIN), oe = livetrade::fq(di.obj + D_OUT_END);
        if (!ob || oe <= ob) continue;
        for (uintptr_t e = ob; e + E_STRIDE <= oe; e += E_STRIDE) {
            uintptr_t tdef = livetrade::fq(e + E_TARGET);
            if (!tdef || !livetrade::validate_region(tdef + D_INDEX, 4)) continue;
            int tidx = livetrade::fi(tdef + D_INDEX);
            if (!g_defs.count(tidx)) continue;
            Link L;
            L.a = idx; L.b = tidx;
            L.entry.resize(E_STRIDE);
            memcpy(L.entry.data(), (const void*)e, E_STRIDE);
            uintptr_t pb = livetrade::fq(e + E_POLY_B), pe = livetrade::fq(e + E_POLY_E);
            if (pb && pe > pb && (pe - pb) <= (1 << 20) && livetrade::validate_region(pb, pe - pb)) {
                L.poly.resize(pe - pb);
                memcpy(L.poly.data(), (const void*)pb, pe - pb);
            }
            g_links.push_back(std::move(L));
        }
    }
    for (size_t i = 0; i < g_links.size(); i++) {
        g_defs[g_links[i].a].incident.push_back((int)i);
        g_defs[g_links[i].b].incident.push_back((int)i);
    }
    // pre-size our arrays so no orientation can ever overflow them
    for (auto& [idx, di] : g_defs) {
        g_out_storage[idx].assign(di.incident.size() * E_STRIDE + E_STRIDE, 0);
        g_in_storage[idx].assign(di.incident.size() + 1, 0);
    }
    g_ready = true;
    log << "  [relink] captured " << g_defs.size() << " definitions, " << g_links.size()
        << " links\n";
    return true;
}

// Point a definition's {begin,end,cap} triple at our own array.
inline void set_vector(uintptr_t def, int off_begin, uintptr_t begin, uintptr_t end, uintptr_t cap) {
    DWORD old = 0;
    if (!VirtualProtect((void*)(def + off_begin), 24, PAGE_READWRITE, &old)) return;
    *(uintptr_t*)(def + off_begin)      = begin;
    *(uintptr_t*)(def + off_begin + 8)  = end;
    *(uintptr_t*)(def + off_begin + 16) = cap;
    VirtualProtect((void*)(def + off_begin), 24, old, &old);
}

// Install `desired` (directed edges over node indices) into the definition graph.
// Returns the number of links drawn/listed in the opposite sense to their file declaration.
inline int apply(const std::set<std::pair<int, int>>& desired_in, std::ofstream& log) {
    if (!g_ready) return -1;
    // IDENTITY MODE: repoint every definition at our own arrays but keep the file's own
    // directions, so nothing reverses. If the game still dies, the fault is the array handoff
    // itself (lifetime, alignment, or a field inside the entry that cannot simply be copied)
    // rather than the reversal -- which is the only way to tell those two apart.
    std::set<std::pair<int, int>> identity;
    if (livetrade::marker_present("RELINK_IDENTITY")) {
        for (auto& L : g_links) identity.insert({L.a, L.b});
        log << "  [relink] IDENTITY MODE: " << identity.size() << " declared directions kept\n";
    }
    // ONE-LINK MODE: keep every declared direction except the FIRST link that wants reversing.
    // If even a single reversal is fatal, the cause is structural (something else is sized to a
    // node's original outgoing count) rather than a matter of how many links moved.
    std::set<std::pair<int, int>> single;
    if (livetrade::marker_present("RELINK_ONE")) {
        bool used = false;
        for (auto& L : g_links) {
            bool wants_rev = !desired_in.count({L.a, L.b}) && desired_in.count({L.b, L.a});
            if (wants_rev && !used) { single.insert({L.b, L.a}); used = true;
                log << "  [relink] ONE-LINK MODE: reversing only " << g_defs[L.a].name
                    << " -> " << g_defs[L.b].name << "\n"; }
            else single.insert({L.a, L.b});
        }
    }
    const std::set<std::pair<int, int>>& desired =
        livetrade::marker_present("RELINK_IDENTITY") ? identity
        : (livetrade::marker_present("RELINK_ONE") ? single : desired_in);
    int reversed_count = 0;
    // build each node's outgoing entry array and incoming pointer array
    std::map<int, std::vector<uint8_t>> outbuf;
    std::map<int, std::vector<uintptr_t>> inbuf;
    for (auto& [idx, di] : g_defs) { outbuf[idx]; inbuf[idx]; }

    for (size_t li = 0; li < g_links.size(); li++) {
        const Link& L = g_links[li];
        bool forward = desired.count({L.a, L.b}) > 0;
        bool backward = !forward && desired.count({L.b, L.a}) > 0;
        int src = forward ? L.a : (backward ? L.b : L.a);   // unknown links keep the declaration
        int dst = forward ? L.b : (backward ? L.a : L.b);
        if (backward) reversed_count++;
        // the entry, adjusted to point from src to dst
        std::vector<uint8_t> e = L.entry;
        std::vector<uint8_t>& buf = outbuf[src];
        size_t at = buf.size();
        buf.insert(buf.end(), e.begin(), e.end());
        // record where the polyline for this entry must live; patched after the buffer is final
        inbuf[dst].push_back((uintptr_t)g_defs[src].obj);
        (void)at;
    }

    // commit: copy into the stable storage, patch per-entry fields, then repoint the vectors
    for (auto& [idx, di] : g_defs) {
        std::vector<uint8_t>& stable = g_out_storage[idx];
        std::vector<uint8_t>& fresh = outbuf[idx];
        if (fresh.size() > stable.size()) continue;             // cannot happen: pre-sized
        if (!fresh.empty()) memcpy(stable.data(), fresh.data(), fresh.size());
        uintptr_t base = (uintptr_t)stable.data();
        // patch every entry's destination pointer + name (the entries were copied verbatim)
        size_t n = fresh.size() / E_STRIDE;
        size_t k = 0;
        for (size_t li = 0; li < g_links.size() && k < n; li++) {
            const Link& L = g_links[li];
            bool forward = desired.count({L.a, L.b}) > 0;
            bool backward = !forward && desired.count({L.b, L.a}) > 0;
            int src = forward ? L.a : (backward ? L.b : L.a);
            int dst = forward ? L.b : (backward ? L.a : L.b);
            if (src != idx) continue;
            uintptr_t e = base + k * E_STRIDE;
            *(uintptr_t*)(e + E_TARGET) = g_defs[dst].obj;
            write_str(e + E_NAME, g_defs[dst].name);
            // the drawn ribbon runs from the entry's owner outward, so the polyline must be in
            // source->destination order. The entry keeps the engine's own polyline buffer; we
            // rewrite its CONTENTS from the captured original, reversed when the link now runs
            // the other way. Each physical link has exactly one live entry, so no sharing.
            if (!L.poly.empty()) {
                uintptr_t pb = livetrade::fq(e + E_POLY_B);
                size_t bytes = L.poly.size();
                if (pb && livetrade::validate_region(pb, bytes)) {
                    DWORD oldp = 0;
                    if (VirtualProtect((void*)pb, bytes, PAGE_READWRITE, &oldp)) {
                        if (!backward) {
                            memcpy((void*)pb, L.poly.data(), bytes);
                        } else {
                            size_t pts = bytes / 8;              // float2
                            const uint64_t* srcp = (const uint64_t*)L.poly.data();
                            uint64_t* dstp = (uint64_t*)pb;
                            for (size_t q = 0; q < pts; q++) dstp[q] = srcp[pts - 1 - q];
                        }
                        VirtualProtect((void*)pb, bytes, oldp, &oldp);
                    }
                }
            }
            k++;
        }
        std::vector<uintptr_t>& instable = g_in_storage[idx];
        std::vector<uintptr_t>& infresh = inbuf[idx];
        if (infresh.size() <= instable.size() && !infresh.empty())
            memcpy(instable.data(), infresh.data(), infresh.size() * 8);
        set_vector(di.obj, D_OUT_BEGIN, base, base + fresh.size(), base + stable.size());
        // The incoming vector's element type is not yet confirmed, so it is only repointed when
        // explicitly enabled; the outgoing vector alone drives the tabs' outgoing side and the
        // arrow layer, and is what this step is proving.
        if (livetrade::marker_present("RELINK_IN")) {
            uintptr_t ibase = (uintptr_t)instable.data();
            set_vector(di.obj, D_IN_BEGIN, ibase, ibase + infresh.size() * 8,
                       ibase + instable.size() * 8);
        }
    }
    return reversed_count;
}

} // namespace relink
