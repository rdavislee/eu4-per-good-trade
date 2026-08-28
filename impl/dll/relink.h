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

// merchants forced from steer to collect because their node has no outgoing link
// under the installed orientation (a sink). Counted separately from index clamps.
inline uint64_t g_demoted = 0;
inline uint64_t g_reclaimed = 0;   // engine replaced one of our installed vectors; we re-allocated

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

// EVERYTHING INSTALLED INTO ENGINE OBJECTS COMES FROM THE ENGINE'S ALLOCATOR (2026-08-27).
// The entry arrays and any >SSO name buffer live inside engine-owned structures; if the engine
// grows, assigns or destroys one, it frees the memory with ITS allocator. DLL-heap (mingw)
// buffers there are a cross-heap free waiting to happen -- vanilla never triggered it (every
// vanilla node key fits SSO; the engine never grew our vectors), Anbennar did: deterministic
// 0xC0000374 two ticks in, invisible to HeapValidate (the engine pool checks itself).
constexpr uintptr_t ENGINE_NEW_R = 0x1A332D4;   // the engine's operator new (outlinks' pattern)
inline uintptr_t engine_alloc(size_t bytes) {
    using FnNew = void* (__fastcall*)(size_t);
    auto alloc = (FnNew)(livetrade::module_base() + ENGINE_NEW_R);
    void* p = alloc(bytes);
    if (p) memset(p, 0, bytes);
    return (uintptr_t)p;
}
struct EngBuf {                                  // engine-heap block, never freed by the DLL
    uintptr_t p = 0; size_t n = 0;
    uint8_t* data() { return (uint8_t*)p; }
    size_t size() const { return n; }
    void engine_assign(size_t bytes) { p = engine_alloc(bytes); n = p ? bytes : 0; }
};

inline std::map<int, DefInfo> g_defs;       // node index -> definition
inline std::vector<Link> g_links;
inline std::map<int, EngBuf> g_out_storage;    // node index -> entry array (ENGINE heap)
inline std::map<int, EngBuf> g_in_storage;     // (vestigial; kept for reset symmetry)
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
        // ENGINE-heap name buffer (deduped): the string lives inside an engine structure, and an
        // engine-side assign/destroy frees it with the ENGINE's allocator. A DLL-heap c_str here
        // was a cross-heap free on any node key longer than SSO -- vanilla has none, mods do.
        static std::map<std::string, uintptr_t> pool;
        uintptr_t& buf = pool[v];
        if (!buf) {
            buf = engine_alloc(v.size() + 1);
            if (buf) memcpy((void*)buf, v.c_str(), v.size() + 1);
        }
        if (!buf) return;
        *(uintptr_t*)s = buf;
        *(uint64_t*)(s + 0x10) = v.size();
        *(uint64_t*)(s + 0x18) = v.size() + 1;   // >= 16 so the engine reads the pointer
    }
    VirtualProtect((void*)s, 0x20, old, &old);
}

// Snapshot every definition and every declared link. Runs once, on a worker thread.
// An in-process world reload frees every definition this module captured; writing through them
// afterwards corrupts the new world's heap. reset() forces a fresh capture() on the new objects.
inline void reset() { g_ready = false; g_defs.clear(); g_links.clear(); g_out_storage.clear(); g_in_storage.clear(); }

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
        g_out_storage[idx].engine_assign(di.incident.size() * E_STRIDE + E_STRIDE);
        g_in_storage[idx].engine_assign((di.incident.size() + 1) * 8);
    }
    g_ready = true;
    log << "  [relink] captured " << g_defs.size() << " definitions, " << g_links.size()
        << " links\n";
    return true;
}


// ---------------------------------------------------------------------------------------
// THE ENGINE'S OWN FIXUP ROUTINES. EU4 mutates this graph itself (the Random New World path
// at 0x8BD6D0), and its epilogue is the recipe to copy. Reusing the engine's routines beats
// replicating them: 0xB69710 re-derives each entry's destination pointer FROM THE NAME and
// re-pushes the definition into every destination's incoming vector, which is exactly the
// consistency the load-time validator checks.
//
// Hard constraint: 0xB67D20 -> 0xB6A840 is an unbounded recursive DFS over outgoing links, so
// the mutated graph MUST stay a DAG. Phi_w is acyclic by construction (spec 1.1), so that holds.
// DO NOT call 0xB4C620: it destructs every CTradeNode, losing all per-country records and
// merchant flags -- that is a reload, not a fixup.
using FnDef  = void(__fastcall*)(uintptr_t);
using FnDB   = void(__fastcall*)(uintptr_t);
using FnMgr  = void(__fastcall*)(uintptr_t);

inline uintptr_t defs_db() { return livetrade::rq(livetrade::module_base() + 0x242BE48); }

// Re-resolve one definition's outgoing destinations from their names and re-push it into every
// destination's incoming vector.
inline void engine_relink_def(uintptr_t def) {
    ((FnDef)(livetrade::module_base() + 0xB69710))(def);
}
// Recompute def+0xE0, the calc-order sort key. REQUIRED after any topology change; DAG only.
inline void engine_recompute_order_keys() {
    uintptr_t db = defs_db();
    if (db) ((FnDB)(livetrade::module_base() + 0xB67D20))(db);
}
// Rebuild and re-sort the manager's calc order WITHOUT destroying any CTradeNode. REQUIRED.
inline void engine_rebuild_calc_order() {
    uintptr_t g = livetrade::game_singleton();
    if (g) ((FnMgr)(livetrade::module_base() + 0xB4C490))(g + 0x2198);
}

// The node window indexes outgoing[rec+0xA8] UNGUARDED (0x13D04A4), so a steer index left over
// from a larger outgoing list is an out-of-bounds read the moment the window opens. Clamp every
// country record on every node whenever link counts change.
inline int clamp_steer_indices(const std::vector<livetrade::SimNode>& sim) {
    int clamped = 0;
    for (auto& s : sim) {
        uintptr_t def = livetrade::fq(s.obj + 0xA8);
        if (!def || !livetrade::validate_region(def + D_OUT_BEGIN, 16)) continue;
        uintptr_t ob = livetrade::fq(def + D_OUT_BEGIN), oe = livetrade::fq(def + D_OUT_END);
        int n = (ob && oe > ob) ? (int)((oe - ob) / E_STRIDE) : 0;
        uintptr_t base = livetrade::rq(s.obj + 0x18);
        int cnt = livetrade::ri(s.obj + 0x24);
        if (!base || cnt <= 0 || cnt > 4096) continue;
        if (!livetrade::validate_region(base, (size_t)cnt * 0xC0)) continue;
        for (int i = 0; i < cnt; i++) {
            uintptr_t rec = base + (uintptr_t)i * 0xC0;
            int32_t idx = livetrade::fi(rec + 0xA8);
            // A node with NO outgoing link under the active graph is a sink for it. Clamping the
            // steer index to 0 there is still out of range -- an empty list has no element 0 --
            // and the trade pass indexes it unguarded, which is an access violation at 0xB5654D
            // (observed the first time a per-good view made `lubeck` a sink). Nobody can steer
            // from a sink, so the record is demoted to COLLECT (+0xAC, 0 = collect / 1 = steer),
            // which is also what spec 1.8 says a sink does: it forwards nothing.
            if (n == 0) {
                // END NODE: the ordinal is clamped to 0 but the record is NOT demoted to collect any
                // more. The two reads that made type 1 here look fatal are covered: 0xB5654D /
                // 0x13FC24D read a slack-padded buffer (outlinks::resize gives end nodes a real
                // zero-filled array) and 0xB53C77 is a SIGNED compare (0 > N-1 = -1 exits). A merchant
                // steering a reverse end at genua stays a steerer -- no -50% collecting penalty (user).
                DWORD old = 0;
                if (idx != 0 && VirtualProtect((void*)(rec + 0xA8), 8, PAGE_READWRITE, &old)) {
                    *(int32_t*)(rec + 0xA8) = 0;
                    VirtualProtect((void*)(rec + 0xA8), 8, old, &old);
                }
                if (*(uint8_t*)(rec + 0xAC) != 0) g_demoted++;   // counted, no longer changed
                continue;
            }
            if (idx >= n || idx < 0) {
                DWORD old = 0;
                if (VirtualProtect((void*)(rec + 0xA8), 4, PAGE_READWRITE, &old)) {
                    *(int32_t*)(rec + 0xA8) = 0;
                    VirtualProtect((void*)(rec + 0xA8), 4, old, &old);
                    clamped++;
                }
            }
        }
    }
    return clamped;
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


// Log a node's CURRENT outgoing and incoming lists, by name, straight from the definition graph.
// The node window's listboxes are built from exactly this (UI RE: 0x13D5560 reads the definition
// graph, never the runtime link records), so what this prints is what those tabs must show.
inline void dump_lists(const std::string& logpath, const std::vector<std::string>& want) {
    std::ofstream log(logpath, std::ios::app);
    log << "--- definition graph: outgoing / incoming by name ---\n";
    for (auto& [idx, di] : g_defs) {
        bool wanted = want.empty();
        for (auto& w : want) if (w == di.name) wanted = true;
        if (!wanted) continue;
        std::string outs, ins;
        uintptr_t ob = livetrade::fq(di.obj + D_OUT_BEGIN), oe = livetrade::fq(di.obj + D_OUT_END);
        for (uintptr_t e = ob; ob && oe > ob && e + E_STRIDE <= oe; e += E_STRIDE) {
            uintptr_t t = livetrade::fq(e + E_TARGET);
            if (t && livetrade::validate_region(t + D_INDEX, 4)) {
                int ti = livetrade::fi(t + D_INDEX);
                outs += (g_defs.count(ti) ? g_defs[ti].name : std::string("?")) + " ";
            }
        }
        uintptr_t ib = livetrade::fq(di.obj + D_IN_BEGIN), ie = livetrade::fq(di.obj + D_IN_END);
        for (uintptr_t p = ib; ib && ie > ib && p + 8 <= ie; p += 8) {
            uintptr_t t = livetrade::fq(p);
            if (t && livetrade::validate_region(t + D_INDEX, 4)) {
                int ti = livetrade::fi(t + D_INDEX);
                ins += (g_defs.count(ti) ? g_defs[ti].name : std::string("?")) + " ";
            }
        }
        log << "  " << di.name << ":  OUTGOING [ " << outs << "]   INCOMING [ " << ins << "]\n";
    }
}

// Install `desired` (directed edges over node indices) into the definition graph, following the
// engine's own Random-New-World fixup order (see relink.md 5.2). Returns links reversed, or -1.
inline int apply(const std::set<std::pair<std::string, std::string>>& desired_in,
                 std::ofstream& log, const std::vector<livetrade::SimNode>& sim) {
    if (!g_ready) return -1;
    // Everything below is keyed by NODE NAME. The engine has two distinct index spaces --
    // definition indices (def+0xD8, where 0 is a null sentinel) and sim node indices
    // (node+0x120) -- and conflating them silently left links "unmatched". An unmatched link
    // keeps its file direction, and mixing those with solver-oriented links closed a CYCLE,
    // which is the stack overflow. Names remove the whole hazard.
    using NamePair = std::pair<std::string, std::string>;
    auto NA = [&](int i) { return g_defs[i].name; };

    std::set<NamePair> identity;
    if (livetrade::marker_present("RELINK_IDENTITY"))
        for (auto& L : g_links) identity.insert({NA(L.a), NA(L.b)});
    std::set<NamePair> single;
    if (livetrade::marker_present("RELINK_ONE")) {
        bool used = false;
        for (auto& L : g_links) {
            bool rev = !desired_in.count({NA(L.a), NA(L.b)}) && desired_in.count({NA(L.b), NA(L.a)});
            if (rev && !used) { single.insert({NA(L.b), NA(L.a)}); used = true;
                log << "  [relink] ONE-LINK: " << NA(L.a) << " -> " << NA(L.b) << "\n"; }
            else single.insert({NA(L.a), NA(L.b)});
        }
    }
    const std::set<NamePair>& desired =
        livetrade::marker_present("RELINK_IDENTITY") ? identity
        : (livetrade::marker_present("RELINK_ONE") ? single : desired_in);

    // ---- 2. decide each link's direction ----
    int reversed_count = 0, unmatched = 0;
    std::map<int, std::vector<int>> per_node;      // node index -> link ids, in slot order
    std::vector<std::pair<int, int>> final_edges;  // the graph we are about to install
    for (size_t li = 0; li < g_links.size(); li++) {
        const Link& L = g_links[li];
        bool fwd = desired.count({NA(L.a), NA(L.b)}) > 0;
        bool bwd = !fwd && desired.count({NA(L.b), NA(L.a)}) > 0;
        if (bwd) reversed_count++;
        if (!fwd && !bwd) {
            unmatched++;                            // no opinion: keep the file's declaration
            if (unmatched <= 6)
                log << "  [relink] unmatched link " << g_defs[L.a].name << " -> "
                    << g_defs[L.b].name << " (keeping declared direction)\n";
        }
        int src = bwd ? L.b : L.a, dst = bwd ? L.a : L.b;
        per_node[src].push_back((int)li);
        final_edges.push_back({src, dst});
    }

    // ---- 2a. THE GRAPH MUST BE A DAG ----
    // 0xB67D20 -> 0xB6A840 is an unbounded recursive DFS over outgoing links with only a
    // "monotone deepen" memo: a directed cycle recurses until the stack dies, with no crash dump.
    // Mixing solver-oriented links with unmatched links that keep their file direction can close
    // a cycle, so verify before touching anything and refuse rather than kill the game.
    {
        std::map<int, std::vector<int>> adj;
        std::map<int, int> indeg;
        std::set<int> nodes;
        for (auto& [u, v] : final_edges) { adj[u].push_back(v); indeg[v]++; nodes.insert(u); nodes.insert(v); }
        std::vector<int> q;
        for (int n : nodes) if (!indeg.count(n) || indeg[n] == 0) q.push_back(n);
        size_t seen = 0;
        while (!q.empty()) {
            int x = q.back(); q.pop_back(); seen++;
            for (int y : adj[x]) if (--indeg[y] == 0) q.push_back(y);
        }
        if (seen != nodes.size()) {
            log << "  [relink] REFUSED: the requested graph has a CYCLE (" << (nodes.size() - seen)
                << " of " << nodes.size() << " nodes in it) -- installing it would stack-overflow "
                   "the engine's DFS at 0xB67D20. " << unmatched
                << " links had no orientation from the solve and kept their declared direction.\n";
            return -2;
        }
    }
    for (auto& [idx, di] : g_defs) {
        if (idx == 0) continue;                     // definition 0 is the null sentinel
        EngBuf& stable = g_out_storage[idx];
        const std::vector<int>& mine = per_node[idx];
        size_t need = mine.size() * E_STRIDE;
        if (need > stable.size()) { log << "  [relink] overflow at node " << idx << (char)10; return -1; }
        {   // the ENGINE may have grown/replaced this vector since the last install (its realloc
            // freed our engine-heap block cleanly); writing through the old pointer would be a
            // use-after-free -- take a fresh block instead and count it
            uintptr_t cur = livetrade::fq(di.obj + D_OUT_BEGIN);
            if (cur != (uintptr_t)stable.data() && stable.p) { stable.engine_assign(stable.n); g_reclaimed++; }
        }
        uintptr_t base = (uintptr_t)stable.data();
        for (size_t k = 0; k < mine.size(); k++) {
            const Link& L = g_links[mine[k]];
            bool bwd = (L.b == idx) && !(desired.count({NA(L.a), NA(L.b)}) > 0);
            int dst = bwd ? L.a : L.b;
            uintptr_t e = base + k * E_STRIDE;
            memcpy((void*)e, L.entry.data(), E_STRIDE);
            *(uintptr_t*)(e + E_TARGET) = g_defs[dst].obj;      // destination definition
            write_str(e + E_NAME, g_defs[dst].name);            // destination NAME (0xB69710 reads it)
            *(int32_t*)(e + 0x38) = (int32_t)k;                 // the entry's own index -- REQUIRED
            if (!L.poly.empty()) {                              // ribbon runs source -> destination
                uintptr_t pb = livetrade::fq(e + E_POLY_B);
                size_t bytes = L.poly.size();
                if (pb && livetrade::validate_region(pb, bytes)) {
                    DWORD op = 0;
                    if (VirtualProtect((void*)pb, bytes, PAGE_READWRITE, &op)) {
                        const uint64_t* sp = (const uint64_t*)L.poly.data();
                        uint64_t* dp = (uint64_t*)pb;
                        size_t pts = bytes / 8;
                        for (size_t q = 0; q < pts; q++) dp[q] = bwd ? sp[pts - 1 - q] : sp[q];
                        VirtualProtect((void*)pb, bytes, op, &op);
                    }
                }
            }
        }
        set_vector(di.obj, D_OUT_BEGIN, base, base + need, base + need);
    }

    // ---- 3. let the ENGINE rebuild incoming: empty each, then re-push from the names ----
    for (auto& [idx, di] : g_defs) {
        uintptr_t b = livetrade::fq(di.obj + D_IN_BEGIN);
        set_vector(di.obj, D_IN_BEGIN, b, b, livetrade::fq(di.obj + D_IN_CAP));
    }
    for (auto& [idx, di] : g_defs) if (idx != 0) engine_relink_def(di.obj);

    // ---- 4. clamp steer indices (the node window indexes these unguarded) ----
    int clamped = clamp_steer_indices(sim);

    // ---- 5 + 7. the two REQUIRED fixups: order keys, then the manager's calc order ----
    engine_recompute_order_keys();
    engine_rebuild_calc_order();

    // ---- 6. EVERY INCIDENT LINK ALSO APPEARS IN THE OUTGOING LIST (spec 1.7, 1.12) -----------
    // The node window fills its listboxes from the DEFINITION lists, and `steer_command` names a
    // link by its index in the node's own OUTGOING list. So a link drawn INTO a node is neither
    // shown as an outgoing panel nor nameable as a steer target -- exactly the end the per-good
    // model needs assignable, since the per-good graphs disagree with Phi_w on ~45% of edge-goods
    // and a link drawn n<-m routinely still carries goods n->m.
    //
    // Appending the missing links here -- AFTER the two fixups above -- gives every incident link
    // an outgoing panel and a steer index, through vanilla's own widgets and command path. The
    // ORDERING is the whole trick: 0xB67D20's DFS is an unbounded recursion over outgoing links,
    // so it must see only the acyclic Phi_w graph. It already has -- it ran at step 5. The
    // incoming lists were rebuilt at step 3, before the append, so nothing duplicates there.
    int extra = 0;
    if (livetrade::marker_present("ALLOUT")) {
        for (auto& [idx, di] : g_defs) {
            if (idx == 0) continue;
            EngBuf& stable = g_out_storage[idx];
            const std::vector<int>& mine = per_node[idx];
            std::set<int> have(mine.begin(), mine.end());
            uintptr_t base = (uintptr_t)stable.data();
            size_t k = mine.size();
            for (int li : di.incident) {
                if (have.count(li)) continue;
                if ((k + 1) * E_STRIDE > stable.size()) break;
                const Link& L = g_links[li];
                int other = (L.a == idx) ? L.b : L.a;
                auto fd = g_defs.find(other);
                if (fd == g_defs.end() || !fd->second.obj) continue;
                uintptr_t e = base + k * E_STRIDE;
                memcpy((void*)e, L.entry.data(), E_STRIDE);
                *(uintptr_t*)(e + E_TARGET) = fd->second.obj;
                write_str(e + E_NAME, fd->second.name);
                *(int32_t*)(e + 0x38) = (int32_t)k;     // its own index -- steer_command uses it
                // NO RIBBON on an appended entry: the arrow layer (0x10AFC05) and the panel builder
                // skip entries whose polyline is empty, so the drawn map stays exactly Phi_w and the
                // reverse panels stay revpanel's. What the entry adds is a STEER ORDINAL for this
                // reverse end (syncrec can write it, the record can hold it, the node window lists
                // it with a button) -- which is what an end node like genua never had.
                *(uintptr_t*)(e + E_POLY_B) = 0;
                *(uintptr_t*)(e + E_POLY_E) = 0;
                k++; extra++;
            }
            if (k > mine.size())
                set_vector(di.obj, D_OUT_BEGIN, base, base + k * E_STRIDE, base + k * E_STRIDE);
        }
    }

    // ---- B1 (TESTING.md): the ENGINE's outgoing lists must equal the installed graph ----
    // Read back what the definitions now hold, by name, and compare with `desired` -- the
    // test's own statement ("the arrows are the installed Phi_w") checked on the engine's data,
    // not on ours. Named spot-checks are the ones the test quotes.
    {
        std::set<NamePair> engine; int appended = 0;
        std::map<std::string, std::string> outs, ins;
        for (auto& [idx, di] : g_defs) {
            if (idx == 0) continue;
            uintptr_t ob = livetrade::fq(di.obj + D_OUT_BEGIN), oe = livetrade::fq(di.obj + D_OUT_END);
            for (uintptr_t e = ob; ob && oe > ob && e + E_STRIDE <= oe; e += E_STRIDE) {
                uintptr_t t = livetrade::fq(e + E_TARGET);
                if (!t || !livetrade::validate_region(t + D_INDEX, 4)) continue;
                if (livetrade::fq(e + E_POLY_B) == 0) { appended++; continue; }   // an ALLOUT reverse-end entry (no ribbon) is not a drawn edge
                int ti = livetrade::fi(t + D_INDEX);
                if (!g_defs.count(ti)) continue;
                engine.insert({di.name, g_defs[ti].name});
                outs[di.name] += g_defs[ti].name + " ";
                ins[g_defs[ti].name] += di.name + " ";
            }
        }
        int missing = 0, extra_e = 0;   // appended counted above
        for (auto& d : desired) if (!engine.count(d)) missing++;
        for (auto& e : engine) if (!desired.count(e)) extra_e++;
        log << "[B1] engine outgoing edges=" << engine.size() << " installed graph edges=" << desired.size()
            << " missing=" << missing << " extra=" << extra_e
            << " appended reverse-end entries=" << appended << (missing == 0 && extra_e == 0 ? "  EQUAL" : "  MISMATCH") << (char)10;
        log << "[B1] genua: OUT [ " << outs["genua"] << "] IN [ " << ins["genua"] << "]  hangzhou: OUT [ "
            << outs["hangzhou"] << "]  english_channel: OUT [ " << outs["english_channel"] << "]  champagne: OUT [ "
            << outs["champagne"] << "]" << (char)10;
    }
    log << "  [relink] applied: " << reversed_count << " links reversed, "
        << clamped << " steer clamped, " << g_demoted << " demoted, "
        << extra << " reverse ends added as outgoing panels\n";;
    return reversed_count;
}

} // namespace relink
