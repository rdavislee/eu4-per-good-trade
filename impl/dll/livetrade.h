// In-process live trade access (spec 1.8, 2.6). Runs INSIDE eu4.exe after injection, so it
// dereferences the live trade structures directly -- no ReadProcessMemory, no fixed-address
// breakpoints, and it can act synchronously with the game. Uses the confirmed offsets
// (hooks.h tradeoff::) for build 835bfdf8.
//
// Enumerates the CTradeNodeDefinition objects by their vtable (base+0x1C439D0), reads each node's
// inline-std::string name (obj+0x10), reads the TradeNodeDatabase singleton (base+0x242B8C8), and
// walks to the runtime CTradeNode values. Everything is logged so the injection can be verified
// from outside.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <string>
#include <unordered_map>
#include <vector>

namespace livetrade {

inline uintptr_t module_base() { return (uintptr_t)GetModuleHandleW(nullptr); }

// Environment variables are NOT inherited by an already-running injected process, so optional
// behaviour is switched by a marker file sitting next to this DLL (e.g. "pgt.WRITETEST").
inline std::string self_dir() {
    char self[MAX_PATH] = {0};
    HMODULE h = nullptr;
    GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                       GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                       (LPCSTR)&module_base, &h);
    DWORD n = GetModuleFileNameA(h, self, MAX_PATH);
    std::string p(self, n ? n : 0);
    size_t slash = p.find_last_of("\\/");
    return slash == std::string::npos ? std::string(".") : p.substr(0, slash);
}
inline bool marker_present(const char* name) {
    std::string path = self_dir() + "\\pgt." + name;
    return GetFileAttributesA(path.c_str()) != INVALID_FILE_ATTRIBUTES;
}

// safe read of `n` bytes at `p` in our own address space. MinGW has no __try/__except, so the
// pointer is validated with VirtualQuery before dereferencing (committed, readable, not guard).
inline bool safe_read(uintptr_t p, void* out, size_t n) {
    if (p < 0x10000 || n == 0) return false;
    MEMORY_BASIC_INFORMATION mbi{};
    if (VirtualQuery((void*)p, &mbi, sizeof(mbi)) != sizeof(mbi)) return false;
    if (mbi.State != MEM_COMMIT) return false;
    if (mbi.Protect & PAGE_GUARD) return false;
    if (!(mbi.Protect & (PAGE_READONLY | PAGE_READWRITE | PAGE_WRITECOPY |
                         PAGE_EXECUTE_READ | PAGE_EXECUTE_READWRITE))) return false;
    uintptr_t region_end = (uintptr_t)mbi.BaseAddress + mbi.RegionSize;
    if (p + n > region_end) return false;          // would straddle into an unknown region
    memcpy(out, (void*)p, n);
    return true;
}
inline uintptr_t rq(uintptr_t p) { uintptr_t v = 0; safe_read(p, &v, 8); return v; }
inline int32_t ri(uintptr_t p) { int32_t v = 0; safe_read(p, &v, 4); return v; }

// ---------------------------------------------------------------------------------------
// FAST PATH (spec H3: the tick hook's added cost must be imperceptible).
// safe_read() issues a VirtualQuery per field, which is the right thing for exploratory scans
// but far too slow inside the monthly update: naming + standings + links touch on the order of
// 10^5 fields, and a syscall each turns a millisecond of arithmetic into seconds of stall (a
// hitch measured in the running game). validate_region() checks a whole contiguous structure
// once; after that the fields inside it are read directly.
inline bool validate_region(uintptr_t p, size_t n) {
    MEMORY_BASIC_INFORMATION mbi{};
    uintptr_t end = p + n;
    while (p < end) {
        if (!VirtualQuery((void*)p, &mbi, sizeof(mbi))) return false;
        if (mbi.State != MEM_COMMIT) return false;
        DWORD prot = mbi.Protect & 0xFF;
        if (prot == PAGE_NOACCESS || (mbi.Protect & PAGE_GUARD)) return false;
        p = (uintptr_t)mbi.BaseAddress + mbi.RegionSize;
    }
    return true;
}
inline int32_t fi(uintptr_t p) { return *(const int32_t*)p; }       // validated region only
inline uintptr_t fq(uintptr_t p) { return *(const uintptr_t*)p; }   // validated region only
inline uint8_t fb(uintptr_t p) { return *(const uint8_t*)p; }       // validated region only

// Walk our own committed PRIVATE regions and hand each to fn(base, size).
// Bounded: only MEM_PRIVATE read/write data (the heap -- where game objects live), skipping
// images/mapped files and huge reserved spans, and stopping at the 128 GB user-space mark.
// Unbounded walks of a 39 GB address space stall the worker for minutes.
template <class F>
inline void walk_self(F fn) {
    MEMORY_BASIC_INFORMATION mbi{};
    uintptr_t addr = 0;
    const uintptr_t LIMIT = 0x2000000000000ULL;
    while (addr < LIMIT && VirtualQuery((void*)addr, &mbi, sizeof(mbi)) == sizeof(mbi)) {
        bool usable = mbi.State == MEM_COMMIT &&
                      mbi.Type == MEM_PRIVATE &&
                      (mbi.Protect & (PAGE_READWRITE | PAGE_WRITECOPY)) &&
                      !(mbi.Protect & PAGE_GUARD) &&
                      mbi.RegionSize <= (256ull << 20);   // skip pathological spans
        if (usable) fn((uintptr_t)mbi.BaseAddress, mbi.RegionSize);
        uintptr_t next = (uintptr_t)mbi.BaseAddress + mbi.RegionSize;
        if (next <= addr) break;
        addr = next;
    }
}

struct Node { uintptr_t obj; std::string name; };

// Enumerate the trade node definition objects by their vtable. The region handed in by
// walk_self is already validated committed+readable, so the scan reads it directly (a
// VirtualQuery per 8-byte probe would make this take minutes).
inline std::vector<Node> enumerate_nodes() {
    uintptr_t base = module_base();
    uintptr_t defvt = base + 0x1C439D0;   // tradeoff::TRADENODE_DEF_VTABLE
    std::vector<Node> nodes;
    walk_self([&](uintptr_t region, size_t sz) {
        const uint8_t* p = (const uint8_t*)region;
        for (size_t i = 0; i + 0x30 <= sz; i += 8) {
            uintptr_t vt;
            memcpy(&vt, p + i, 8);
            if (vt != defvt) continue;
            char nm[17] = {0};
            memcpy(nm, p + i + 0x10, 16);
            size_t len = strnlen(nm, 16);
            std::string s(nm, len);
            bool ok = !s.empty();
            for (char c : s) if (!(c >= 'a' && c <= 'z') && c != '_') ok = false;
            if (ok) nodes.push_back({region + i, s});
        }
    });
    return nodes;
}

// Find the RUNTIME node objects that pair with each definition. A runtime CTradeNode holds a
// pointer to its definition; so for each def object, scan the heap for a qword equal to that
// def address and report the containing object (its vtable + the offset the pointer sits at).
// One consistent (vtable, offset) pair across many nodes identifies the runtime class -- the
// object that carries local_value/total/trade_goods_size (spec 1.8).
struct RuntimeHit { uintptr_t obj; uintptr_t vt; int off; std::string defname; };

inline std::vector<RuntimeHit> find_runtime_nodes(const std::vector<Node>& defs, size_t max_defs) {
    std::vector<RuntimeHit> hits;
    uintptr_t mbase = module_base();
    // build a lookup of def address -> name for the first N defs
    std::vector<std::pair<uintptr_t, std::string>> want;
    for (size_t i = 0; i < defs.size() && want.size() < max_defs; i++) want.push_back({defs[i].obj, defs[i].name});
    // O(1) membership instead of a linear probe per qword -- the linear form is far too slow
    // over a multi-GB heap.
    std::unordered_map<uintptr_t, const std::string*> wantmap;
    for (auto& w : want) wantmap[w.first] = &w.second;
    walk_self([&](uintptr_t region, size_t sz) {
        const uint8_t* p = (const uint8_t*)region;
        for (size_t i = 0; i + 8 <= sz; i += 8) {
            uintptr_t v;
            memcpy(&v, p + i, 8);
            if (v < 0x2c000000000ULL || v >= 0x2c200000000ULL) continue;
            auto it = wantmap.find(v);
            if (it == wantmap.end()) continue;
            {
                std::pair<uintptr_t, std::string> w{v, *it->second};
                // candidate: the pointer sits inside some object. Probe plausible object starts
                // by looking back for a vtable (a pointer into eu4.exe) at 8-byte steps.
                for (int back = 0; back <= 0x200; back += 8) {
                    if ((size_t)back > i) break;
                    uintptr_t maybe_vt;
                    memcpy(&maybe_vt, p + i - back, 8);
                    if (maybe_vt >= mbase && maybe_vt < mbase + 0x2600000) {
                        hits.push_back({region + i - back, maybe_vt, back, w.second});
                        break;    // nearest preceding vtable = the object start
                    }
                }
            }
        }
    });
    return hits;
}

// ---------------------------------------------------------------------------------------
// THE LIVE ECONOMY READ (spec 1.8). A CTradeNode carries the six node-window values as int32
// fixed-point x1000 at +0x160..+0x170, and a sub-object pointer at +0xF8 whose +0xB4/+0xBC are
// the local/outgoing sources. That combination is a strong signature: scan the heap for objects
// where the cached fields agree with the sub-object's source values.
struct LiveNode {
    uintptr_t obj;
    double incoming, outgoing, local, total, our_from_this;
    std::string name;
};

// defs: the CTradeNodeDefinition objects (from enumerate_nodes). A real CTradeNode holds a
// pointer to its definition somewhere in its first 0x200 bytes -- requiring that link is what
// separates the true nodes from coincidental field matches.
inline std::vector<LiveNode> read_live_nodes(const std::vector<Node>& defs) {
    std::vector<LiveNode> out;
    std::unordered_map<uintptr_t, const std::string*> defmap;
    for (auto& d : defs) defmap[d.obj] = &d.name;
    // Collect the usable regions once so a candidate's sub-object pointer can be validated by an
    // interval lookup instead of a VirtualQuery syscall per probe (which makes the scan crawl).
    std::vector<std::pair<uintptr_t, uintptr_t>> regions;
    walk_self([&](uintptr_t r, size_t s) { regions.push_back({r, r + s}); });
    auto readable = [&](uintptr_t a, size_t need) {
        for (auto& r : regions) if (a >= r.first && a + need <= r.second) return true;
        return false;
    };
    walk_self([&](uintptr_t region, size_t sz) {
        const uint8_t* p = (const uint8_t*)region;
        for (size_t i = 0; i + 0x190 <= sz; i += 8) {
            // cheap pre-filter first: a real node's cached local_value is a small positive int
            int32_t loc_pre;
            memcpy(&loc_pre, p + i + 0x168, 4);
            if (loc_pre <= 0 || loc_pre > 2000000) continue;
            uintptr_t sub;
            memcpy(&sub, p + i + 0xF8, 8);
            if (sub < 0x2c000000000ULL || sub >= 0x2c200000000ULL) continue;
            if (!readable(sub, 0xC0)) continue;
            int32_t src_local, src_out;
            memcpy(&src_local, (const uint8_t*)sub + 0xB4, 4);
            memcpy(&src_out,   (const uint8_t*)sub + 0xBC, 4);
            int32_t inc, outg, loc, tot, ours;
            memcpy(&inc,  p + i + 0x160, 4);
            memcpy(&outg, p + i + 0x164, 4);
            memcpy(&loc,  p + i + 0x168, 4);
            memcpy(&tot,  p + i + 0x16C, 4);
            memcpy(&ours, p + i + 0x170, 4);
            // the serializer keeps these caches equal to their sources -- that is the signature
            if (loc != src_local || outg != src_out) continue;
            if (loc <= 0 || loc > 2000000) continue;         // a real node has local value
            if (inc < 0 || inc > 5000000) continue;
            if (tot < 0 || tot > 20000000) continue;
            // Prove nodehood by the DEFINITION link. The node may hold either a raw pointer to
            // its definition object or (as the def objects themselves show, e.g. +0xF8 == 0x165)
            // a small definition INDEX. Accept either: a pointer into defmap, or an int in the
            // trade-node id range that also appears in a def object.
            const std::string* nm = nullptr;
            for (int off = 0; off < 0x200 && !nm; off += 8) {
                uintptr_t q;
                memcpy(&q, p + i + off, 8);
                if (q >= 0x2c000000000ULL && q < 0x2c200000000ULL) {
                    auto it = defmap.find(q);
                    if (it != defmap.end()) { nm = it->second; break; }
                    // one hop: the node may point at a wrapper that points at the definition
                    if (readable(q, 8)) {
                        uintptr_t q2;
                        memcpy(&q2, (const uint8_t*)q, 8);
                        auto it2 = defmap.find(q2);
                        if (it2 != defmap.end()) { nm = it2->second; break; }
                    }
                }
            }
            static const std::string kUnnamed = "(node)";
            out.push_back({region + i, inc / 1000.0, outg / 1000.0, loc / 1000.0,
                           tot / 1000.0, ours / 1000.0, nm ? *nm : kUnnamed});
        }
    });
    return out;
}

// =========================================================================================
// THE REAL TRADE MODEL ACCESS (spec 1.8 / 2.6). Walks the game singleton -> CTradeManager ->
// the CTradeNode array directly, using the offsets recovered from the monthly-update driver.
// No scanning, no heuristics: this is the engine's own data path.
struct SimNode {
    uintptr_t obj;
    int index;
    double local_value, outgoing_value, retention, gross_local;
    std::vector<int32_t> goods;     // trade_goods_size, indexed by trade-good id
    std::string name;               // authoritative: read from the node's definition in memory
};

// The AUTHORITATIVE name of a sim node: a CTradeNode holds a pointer to its CTradeNodeDefinition
// (whose inline std::string name sits at +0x10). Scan the node's own 0x138 bytes for a qword
// that points to an object whose first qword is the definition vtable, then read that name.
// This is what makes the engine node-array index -> node-name mapping ground truth, independent
// of any file's declaration order (which a mod reorders -- the source of an index-mismatch bug).
inline std::string def_name_of(uintptr_t node) {
    uintptr_t defvt = module_base() + 0x1C439D0;   // TRADENODE_DEF_VTABLE
    for (int off = 0; off < 0x138; off += 8) {
        uintptr_t p = rq(node + off);
        if (!p || (p & 7)) continue;
        uintptr_t vt = rq(p);
        if (vt != defvt) continue;
        char nm[17] = {0};
        if (!safe_read(p + 0x10, nm, 16)) continue;   // inline std::string (SSO)
        size_t len = strnlen(nm, 16);
        std::string s(nm, len);
        bool ok = !s.empty();
        for (char c : s) if (!((c >= 'a' && c <= 'z') || c == '_' || (c >= '0' && c <= '9'))) ok = false;
        if (ok) return s;
        // long std::string: the buffer is a pointer at +0x10, size at +0x18
        uintptr_t buf = rq(p + 0x10);
        int32_t sz = ri(p + 0x18);
        if (buf && sz > 0 && sz < 64) {
            char big[65] = {0};
            if (safe_read(buf, big, sz)) {
                std::string b(big, sz);
                bool ok2 = true;
                for (char c : b) if (!((c >= 'a' && c <= 'z') || c == '_' || (c >= '0' && c <= '9'))) ok2 = false;
                if (ok2) return b;
            }
        }
    }
    return "";
}

inline uintptr_t trade_manager() {
    uintptr_t base = module_base();
    uintptr_t g = 0;
    if (!safe_read(base + 0x233FE78, &g, 8) || !g) return 0;   // GAME_SINGLETON
    return g + 0x2198;                                          // TRADE_MANAGER_OFF
}

inline std::vector<SimNode> read_sim_nodes(int max_nodes = 100) {
    std::vector<SimNode> out;
    uintptr_t mgr = trade_manager();
    if (!mgr) return out;
    uintptr_t nodes_base = 0;
    int32_t count = 0;
    if (!safe_read(mgr + 0x18, &nodes_base, 8)) return out;     // MGR_NODES_PTR
    if (!safe_read(mgr + 0x24, &count, 4)) return out;          // MGR_NODES_COUNT
    if (!nodes_base || count <= 0 || count > 4096) return out;
    // validate the whole node array once; then read fields directly (spec H3 -- a VirtualQuery
    // per field made the tick hook stall the game for seconds).
    int take = (count < max_nodes) ? count : max_nodes;
    if (!validate_region(nodes_base, (size_t)take * 0x138)) return out;
    out.reserve(take);
    for (int i = 0; i < take; i++) {
        uintptr_t n = nodes_base + (uintptr_t)i * 0x138;        // NODE_STRIDE
        SimNode s{};
        s.obj = n;
        s.index          = fi(n + 0x120);                       // SIM_NODE_ID
        s.local_value    = fi(n + 0xB4) / 1000.0;               // SIM_LOCAL_VALUE
        s.outgoing_value = fi(n + 0xBC) / 1000.0;               // SIM_OUTGOING_VALUE
        s.retention      = fi(n + 0xB8) / 1000.0;               // permille
        s.gross_local    = fi(n + 0xB0) / 1000.0;               // `current` = the pool
        // per-good produced quantities: vector<int32> at +0x108 / +0x110
        uintptr_t gb = fq(n + 0x108), ge = fq(n + 0x110);
        if (gb && ge > gb && (ge - gb) <= 4096 && validate_region(gb, ge - gb)) {
            size_t ng = (ge - gb) / 4;
            s.goods.resize(ng);
            memcpy(s.goods.data(), (const void*)gb, ng * 4);
        }
        out.push_back(std::move(s));
    }
    return out;
}

// =========================================================================================
// WRITE PATH (spec 2.6). Writing a node's local_value proves the DLL owns the engine's own
// numbers -- the game recomputes displays from these fields, so a write shows up in the node
// window. This is the same store the mod uses to install the per-good economy.
// write an int32 fixed-point (ducats x1000) at node+off, guarded by VirtualProtect.
inline bool write_fixed(uintptr_t node, int off, double ducats) {
    int32_t v = (int32_t)(ducats * 1000.0 + (ducats >= 0 ? 0.5 : -0.5));
    DWORD old = 0;
    if (!VirtualProtect((void*)(node + off), 4, PAGE_READWRITE, &old)) return false;
    *(int32_t*)(node + off) = v;
    VirtualProtect((void*)(node + off), 4, old, &old);
    return true;
}
inline bool write_local_value(uintptr_t node, double ducats) { return write_fixed(node, 0xB4, ducats); }
// spec 2.6's writes, on the CONFIRMED field map (flow-pass RE):
//   +0xB0 `current` = the node's COLLECTIBLE POOL -- what pass 10 divides among collectors
//                     (rec.total = current * power_fraction/1000), i.e. spec 2.6's "collectible pool"
//   +0xBC outgoing_value
//   local (+0xB4) is deliberately NOT written: spec test B4 requires it to stay the engine's own.
// (NOTE: +0xCC is p_pow, NOT a total -- writing it corrupts trade power. Never write it here.)
inline bool write_pool(uintptr_t node, double ducats)     { return write_fixed(node, 0xB0, ducats); }
inline bool write_outgoing(uintptr_t node, double ducats) { return write_fixed(node, 0xBC, ducats); }
// retention is PERMILLE (1000 - pull*1000/(pull+retain)), not a ducat value
inline bool write_retention_permille(uintptr_t node, double frac_retained) {
    int32_t v = (int32_t)(frac_retained * 1000.0 + 0.5);
    if (v < 0) v = 0; if (v > 1000) v = 1000;
    DWORD old = 0;
    if (!VirtualProtect((void*)(node + 0xB8), 4, PAGE_READWRITE, &old)) return false;
    *(int32_t*)(node + 0xB8) = v;
    VirtualProtect((void*)(node + 0xB8), 4, old, &old);
    return true;
}
// one incoming-link record's value (+0x10) and steering add (+0x14), both signed int32 x1000
inline bool write_link_value(uintptr_t rec, double ducats) { return write_fixed(rec, 0x10, ducats); }
inline bool write_link_add(uintptr_t rec, double ducats)   { return write_fixed(rec, 0x14, ducats); }
// UI caches on the same object (display side), int32 x1000
inline bool write_ui_incoming(uintptr_t node, double d) { return write_fixed(node, 0x160, d); }
inline bool write_ui_outgoing(uintptr_t node, double d) { return write_fixed(node, 0x164, d); }
inline bool write_ui_total(uintptr_t node, double d)    { return write_fixed(node, 0x16C, d); }

// ---------------------------------------------------------------------------------------
// PER-NODE PER-COUNTRY RECORDS (spec 1.8's powershare, 1.9's propagation, 3.14's AI inputs).
// Array at node+0x18, count at node+0x24, stride 0xC0, indexed by country tag index.
// Offsets proved by the engine's own Entry::Save at 0xB5E320 (see OFFSETS.md).
struct CountryStanding {
    uintptr_t rec;
    int tag_index;
    double province_power, ship_power, val, max_pow, max_demand;
    double power_fraction;      // permille share among power holders (+0x2C)
    double total, money;        // what pass 10 writes back (+0x38, +0x34)
    double t_in, t_out;         // propagated in/out
    bool has_trader, has_capital;
    int type;                   // 0 = collect, 1 = steer
    int steer_link;             // outgoing-link index this country steers toward (+0xA8)
};

inline int country_record_count(uintptr_t node) {
    int32_t n = ri(node + 0x24);
    return (n > 0 && n < 4096) ? n : 0;
}

inline std::vector<CountryStanding> read_standings(uintptr_t node) {
    std::vector<CountryStanding> out;
    uintptr_t base = rq(node + 0x18);
    int n = country_record_count(node);
    if (!base || !n) return out;
    // validate the WHOLE record array once, then read its fields directly (spec H3)
    if (!validate_region(base, (size_t)n * 0xC0)) return out;
    out.reserve(n);
    for (int i = 0; i < n; i++) {
        uintptr_t r = base + (uintptr_t)i * 0xC0;
        CountryStanding c{};
        c.rec = r;
        c.tag_index = fi(r + 0x14);
        c.province_power = fi(r + 0x28) / 1000.0;
        c.ship_power     = fi(r + 0x1C) / 1000.0;
        c.power_fraction = fi(r + 0x2C) / 1000.0;
        c.money          = fi(r + 0x34) / 1000.0;
        c.total          = fi(r + 0x38) / 1000.0;
        c.max_demand     = fi(r + 0x44) / 1000.0;
        c.val            = fi(r + 0x48) / 1000.0;
        c.max_pow        = fi(r + 0x4C) / 1000.0;
        c.t_out          = fi(r + 0x50) / 1000.0;
        c.t_in           = fi(r + 0x54) / 1000.0;
        c.steer_link     = fi(r + 0xA8);
        c.type = fb(r + 0xAC);
        c.has_capital = fb(r + 0xAD) != 0;
        c.has_trader  = fb(r + 0xAE) != 0;
        if (c.val <= 0 && c.province_power <= 0 && !c.has_trader && !c.has_capital) continue;
        out.push_back(c);
    }
    return out;
}

// Write a country's share of the collectible pool (permille). Pass 10 computes
// rec.total = node.current * power_fraction/1000, then money from it -- so this is the lever
// that makes the engine's OWN collector division pay out the model's per-country income.
inline bool write_power_fraction(uintptr_t rec, double frac) {
    int32_t v = (int32_t)(frac * 1000.0 + 0.5);
    if (v < 0) v = 0; if (v > 1000) v = 1000;
    DWORD old = 0;
    if (!VirtualProtect((void*)(rec + 0x2C), 4, PAGE_READWRITE, &old)) return false;
    *(int32_t*)(rec + 0x2C) = v;
    VirtualProtect((void*)(rec + 0x2C), 4, old, &old);
    return true;
}

// ---------------------------------------------------------------------------------------
// COUNTRIES (spec 2.6's "country trade income", test E1/E2).
// vector<CCountry*> at G+0x1d08 (count int32 at G+0x1d14). A per-node record's country index is
// the low 16 bits of the tag dword at rec+0x14. Income: CCountry::AddDelayedIncome(country, 2)
// adds to the monthly accumulator at country+0x68 and to the ledger object at country+0x760
// (category 2 = trade) -- 0x338A90, named by its own assert string "AddDelayedIncome, %s, %d, %d".
inline int country_index_of(int tag_dword) { return tag_dword & 0xFFFF; }

inline uintptr_t game_singleton() {
    uintptr_t g = 0;
    safe_read(module_base() + 0x233FE78, &g, 8);
    return g;
}

inline uintptr_t country_at(int index) {
    uintptr_t g = game_singleton();
    if (!g) return 0;
    uintptr_t vec = rq(g + 0x1d08);
    int32_t n = ri(g + 0x1d14);
    if (!vec || index < 0 || index >= n || n > 8192) return 0;
    if (!validate_region(vec + (uintptr_t)index * 8, 8)) return 0;
    return fq(vec + (uintptr_t)index * 8);
}

// the country's accumulating monthly income (all categories), int32 x1000
inline double country_income_accum(uintptr_t country) {
    if (!country || !validate_region(country + 0x68, 4)) return 0;
    return fi(country + 0x68) / 1000.0;
}

// One incoming-link record (node+0xF0 vector, stride 0x20). value at +0x10 (signed int32 x1000).
// The source-node reference offset is what we resolve here by dumping.
struct InLink { uintptr_t rec; int32_t value_raw; uintptr_t words[4]; };

inline std::vector<InLink> read_incoming(uintptr_t node) {
    std::vector<InLink> out;
    uintptr_t begin = rq(node + 0xF0), end = rq(node + 0xF8);
    if (!begin || end <= begin || (end - begin) > 0x20 * 512) return out;
    if (!validate_region(begin, end - begin)) return out;   // validate once (spec H3)
    for (uintptr_t p = begin; p + 0x20 <= end; p += 0x20) {
        InLink l{};
        l.rec = p;
        l.value_raw = fi(p + 0x10);
        for (int w = 0; w < 4; w++) l.words[w] = fq(p + w * 8);
        out.push_back(l);
    }
    return out;
}

// Dump the incoming-link records of the first few sim nodes so the record layout (which word is
// the source node) can be identified against the known graph. Behind the LINKDUMP marker.
inline void dump_incoming(const std::string& logpath, const std::vector<SimNode>& sim) {
    std::ofstream log(logpath, std::ios::app);
    log << "--- incoming-link records (node+0xF0 vector, stride 0x20) ---\n";
    uintptr_t base = module_base();
    int shown = 0;
    for (auto& s : sim) {
        auto links = read_incoming(s.obj);
        if (links.empty()) continue;
        log << "  node[" << s.index << "] " << (s.name.empty() ? "?" : s.name)
            << " has " << links.size() << " incoming records:\n";
        for (auto& l : links) {
            log << "     rec@0x" << std::hex << l.rec << " val=" << std::dec
                << (l.value_raw / 1000.0);
            for (int w = 0; w < 4; w++) {
                log << "  [+0x" << std::hex << (w * 8) << "]=0x" << l.words[w];
                // annotate if the word looks like a sim-node pointer (in the node array range)
            }
            log << std::dec << "\n";
        }
        if (++shown >= 4) break;
    }
}

// log a snapshot of live trade state to a file next to eu4.exe
inline void log_snapshot(const std::string& logpath) {
    std::ofstream log(logpath, std::ios::app);
    uintptr_t base = module_base();
    log << "=== livetrade in-process snapshot ===\n";
    log << "module base 0x" << std::hex << base << std::dec << "\n";
    uintptr_t singleton = rq(base + 0x242B8C8);
    log << "TradeNodeDatabase singleton [base+0x242B8C8] = 0x" << std::hex << singleton << std::dec << "\n";
    auto nodes = enumerate_nodes();
    // distinct names
    std::vector<std::string> seen;
    int distinct = 0;
    for (auto& n : nodes) {
        bool dup = false;
        for (auto& s : seen) if (s == n.name) { dup = true; break; }
        if (!dup) { seen.push_back(n.name); distinct++; }
    }
    log << "enumerated " << nodes.size() << " def objects, " << distinct << " distinct node names\n";
    // print a few with their sub-object local_value if reachable
    int shown = 0;
    for (auto& n : nodes) {
        if (shown++ >= 12) break;
        uintptr_t sub = rq(n.obj + 0xF8);       // may be an id for def objects
        std::string lv = "-";
        if (sub > 0x10000 && sub < 0x00007ff000000000ULL) {
            int32_t v = ri(sub + 0xB4);
            if (v >= 0 && v < 2000000) lv = std::to_string(v / 1000.0);
        }
        log << "  node " << n.name << "  obj=0x" << std::hex << n.obj << std::dec
            << "  +0xF8=0x" << std::hex << sub << std::dec << "  local_value=" << lv << "\n";
    }
    // --- THE LIVE ECONOMY READ (spec 1.8): six node-window values per node ---
    {
        // ===== THE REAL READ: singleton -> CTradeManager -> CTradeNode array (spec 1.8) =====
        {
            uintptr_t mgr = trade_manager();
            log << "--- SIM trade model ---\n";
            log << "  game singleton [base+0x233FE78] -> CTradeManager = 0x"
                << std::hex << mgr << std::dec << "\n";
            auto sim = read_sim_nodes();
            log << "  CTradeNode array: " << sim.size() << " nodes read (stride 0x138)\n";
            int shown = 0;
            double world_local = 0;
            int with_goods = 0;
            for (auto& s : sim) {
                world_local += s.local_value;
                if (!s.goods.empty()) with_goods++;
                if (shown++ < 12) {
                    log << "   node[" << s.index << "] @0x" << std::hex << s.obj << std::dec
                        << " local=" << s.local_value
                        << " outgoing=" << s.outgoing_value
                        << " retention=" << s.retention
                        << " goods=" << s.goods.size();
                    // show the non-zero per-good quantities (the inject vector, spec 1.8)
                    int nz = 0;
                    for (size_t k = 0; k < s.goods.size(); k++) {
                        if (s.goods[k] != 0 && nz < 8) {
                            log << " [g" << k << "]=" << s.goods[k] / 1000.0;
                            nz++;
                        }
                    }
                    log << "\n";
                }
            }
            log << "  world local value = " << world_local
                << " ; nodes carrying a per-good array = " << with_goods << "\n";

            // ===== WRITE PROOF (spec 2.6): mark one node so the change is visible in-game =====
            // Writing local_value on the highest-value node and reading it back proves the DLL
            // owns the engine's own trade numbers -- the precondition for installing the
            // per-good economy. Guarded so it only runs when explicitly requested.
            if (marker_present("WRITETEST") && !sim.empty()) {
                const SimNode* target = &sim[0];
                for (auto& s : sim) if (s.local_value > target->local_value) target = &s;
                double before = target->local_value;
                bool ok = write_local_value(target->obj, 123.456);
                int32_t after = 0;
                safe_read(target->obj + 0xB4, &after, 4);
                log << "  WRITE TEST node[" << target->index << "]: local " << before
                    << " -> wrote 123.456 -> reads " << (after / 1000.0)
                    << (ok ? "  [OK]" : "  [FAILED]") << "\n";
            }

            // ---- name the nodes AUTHORITATIVELY: each sim node carries a pointer to its
            // CTradeNodeDefinition, whose name we read from memory (def_name_of). This is ground
            // truth for the engine node-array index -> node-name mapping, independent of any
            // file's declaration order (a mod reorders it, which silently mis-indexes routing).
            {
                std::ofstream dump(logpath + ".nodes.tsv", std::ios::trunc);
                dump << "index\tname\tid\tlocal_value\toutgoing\tretention";
                for (int k = 0; k < 33; k++) dump << "\tg" << k;
                dump << "\n";
                int named = 0;
                for (size_t i = 0; i < sim.size(); i++) {
                    const SimNode& s = sim[i];
                    if (!s.name.empty()) named++;
                    dump << i << "\t"
                         << (s.name.empty() ? std::string("?") : s.name) << "\t"
                         << s.index << "\t"
                         << s.local_value << "\t" << s.outgoing_value << "\t" << s.retention;
                    for (int k = 0; k < 33; k++)
                        dump << "\t" << (k < (int)s.goods.size() ? s.goods[k] / 1000.0 : 0.0);
                    dump << "\n";
                }
                log << "  wrote node dump: " << logpath << ".nodes.tsv ("
                    << named << "/" << sim.size() << " named from memory)\n";
            }
        }

        // DIRECT VALUE SEARCH (superseded by the SIM read above; kept behind PGT_DEEPSCAN).
        if (marker_present("DEEPSCAN")) {
            log << "--- direct search for the game's own Sevilla trio (7000/-1200/5800) ---\n";
            int found_trio = 0;
            walk_self([&](uintptr_t region, size_t sz) {
                if (found_trio >= 12) return;
                const uint8_t* q = (const uint8_t*)region;
                for (size_t i = 0; i + 0x40 <= sz; i += 4) {
                    int32_t a; memcpy(&a, q + i, 4);
                    if (a < 6900 || a > 7100) continue;           // local_value ~ 7.0
                    bool has_out = false, has_tot = false;
                    for (int j = -0x30; j <= 0x30; j += 4) {
                        if ((long)i + j < 0 || i + j + 4 > sz) continue;
                        int32_t b; memcpy(&b, q + i + j, 4);
                        if (b > -1300 && b < -1100) has_out = true;
                        if (b > 5700 && b < 5900) has_tot = true;
                    }
                    if (!has_out || !has_tot) continue;
                    log << "  TRIO @0x" << std::hex << (region + i) << std::dec << " :";
                    for (int j = -0x20; j <= 0x20; j += 4) {
                        if ((long)i + j < 0 || i + j + 4 > sz) continue;
                        int32_t b; memcpy(&b, q + i + j, 4);
                        log << " " << std::showpos << j << std::noshowpos << "=" << b;
                    }
                    log << "\n";
                    if (++found_trio >= 12) return;
                }
            });
            log << "  (" << found_trio << " trio matches)\n";
        }

        auto live = marker_present("DEEPSCAN") ? read_live_nodes(nodes) : std::vector<LiveNode>();
        log << "--- heuristic economy scan (diagnostic): " << live.size() << " candidates ---\n";
        // GROUND TRUTH CHECK: the game's own Sevilla window read local 7.00 / outgoing -1.20 /
        // total 5.80 at this save point. Any candidate matching those values IS the real node.
        for (auto& v : live) {
            if (v.local > 6.5 && v.local < 7.6) {
                log << "  *** GROUND-TRUTH MATCH (local~7.0): @0x" << std::hex << v.obj << std::dec
                    << " incoming=" << v.incoming << " local=" << v.local
                    << " outgoing=" << v.outgoing << " total=" << v.total << "\n";
            }
        }
        int n = 0;
        for (auto& v : live) {
            if (n++ >= 30) break;
            log << "  " << v.name << " @0x" << std::hex << v.obj << std::dec
                << "  incoming=" << v.incoming << " local=" << v.local
                << " outgoing=" << v.outgoing << " total=" << v.total
                << " our_from_this=" << v.our_from_this << "\n";
        }
    }

    // --- runtime node discovery (diagnostic; the economy read above is the product) ---
    std::vector<RuntimeHit> hits;
    if (marker_present("DEEPSCAN")) {
        log << "--- runtime objects referencing the node definitions ---\n";
        hits = find_runtime_nodes(nodes, 6);
    }
    // tally (vtable, offset) pairs: the real runtime class is the one recurring across nodes
    struct Tally { uintptr_t vt; int off; int count; };
    std::vector<Tally> tally;
    for (auto& h : hits) {
        bool found = false;
        for (auto& t : tally) if (t.vt == h.vt && t.off == h.off) { t.count++; found = true; break; }
        if (!found) tally.push_back({h.vt, h.off, 1});
    }
    for (auto& t : tally) {
        if (t.count < 2) continue;
        log << "  vtable eu4.exe+0x" << std::hex << (t.vt - base) << std::dec
            << "  def-ptr at +0x" << std::hex << t.off << std::dec
            << "  seen on " << t.count << " nodes\n";
    }
    int shown2 = 0;
    for (auto& h : hits) {
        if (shown2++ >= 14) break;
        log << "  " << h.defname << ": obj=0x" << std::hex << h.obj
            << " vt=eu4+0x" << (h.vt - base) << " defptr@+0x" << h.off << std::dec << "\n";
    }
    // --- dump the runtime node class layout (vtable eu4+0x1D82450, def ptr at +0x80) ---
    // Report every plausible field so the trade values can be labelled against the node window:
    // int32s (EU4 stores trade values as fixed-point x1000), floats, and heap pointers.
    log << "--- runtime node layout (vt eu4+0x1D82450, defptr@+0x80) ---\n";
    for (auto& h : hits) {
        if ((h.vt - base) != 0x1D82450 || h.off != 0x80) continue;
        log << "runtime node '" << h.defname << "' @ 0x" << std::hex << h.obj << std::dec << "\n";
        const uint8_t* o = (const uint8_t*)h.obj;
        for (int i = 0; i < 0x200; i += 4) {
            int32_t iv; memcpy(&iv, o + i, 4);
            float fv; memcpy(&fv, o + i, 4);
            uintptr_t pv = 0;
            if (i % 8 == 0) memcpy(&pv, o + i, 8);
            bool isptr = (i % 8 == 0) && ((pv >= 0x2c000000000ULL && pv < 0x2c200000000ULL) ||
                                          (pv >= base && pv < base + 0x2600000));
            if (isptr) {
                log << "   +0x" << std::hex << i << " PTR 0x" << pv << std::dec << "\n";
            } else if (iv > 0 && iv < 2000000) {
                log << "   +0x" << std::hex << i << std::dec << " i32=" << iv
                    << " (/1000=" << (iv / 1000.0) << ")";
                if (fv > 0.0001f && fv < 1e6f) log << "  f32=" << fv;
                log << "\n";
            } else if (fv > 0.0001f && fv < 1e6f) {
                log << "   +0x" << std::hex << i << std::dec << " f32=" << fv << "\n";
            }
        }
        break;   // one full layout is enough
    }

    // --- follow the render node's economy pointers one level down ---
    // The trade-map render code reads a node value as [[node+0x68]+0x100]; walk each pointer
    // field of the render node and report any sub-object carrying trade-shaped numbers, so the
    // economy object (local/total/power, and the per-good array) can be identified.
    log << "--- render-node sub-objects (economy candidates) ---\n";
    for (auto& h : hits) {
        if ((h.vt - base) != 0x1D82450 || h.off != 0x80) continue;
        const uint8_t* o = (const uint8_t*)h.obj;
        for (int off : {0x08, 0x60, 0x68, 0x78, 0x88, 0xa0, 0xa8, 0xb0}) {
            uintptr_t sub; memcpy(&sub, o + off, 8);
            if (sub < 0x2c000000000ULL || sub >= 0x2c200000000ULL) continue;
            MEMORY_BASIC_INFORMATION mbi{};
            if (VirtualQuery((void*)sub, &mbi, sizeof(mbi)) != sizeof(mbi) ||
                mbi.State != MEM_COMMIT) continue;
            const uint8_t* s = (const uint8_t*)sub;
            // count trade-shaped int32s (fixed-point x1000 in a plausible ducat range)
            int shaped = 0;
            for (int i = 0; i < 0x140; i += 4) {
                int32_t iv; memcpy(&iv, s + i, 4);
                if (iv > 100 && iv < 500000) shaped++;
            }
            log << "  " << h.defname << " +0x" << std::hex << off << " -> 0x" << sub << std::dec
                << "  trade-shaped i32s: " << shaped << "\n";
            if (shaped >= 6) {
                for (int i = 0; i < 0xC0; i += 4) {
                    int32_t iv; memcpy(&iv, s + i, 4);
                    float fv; memcpy(&fv, s + i, 4);
                    if (iv > 100 && iv < 500000)
                        log << "      +0x" << std::hex << i << std::dec << " i32=" << iv
                            << " (/1000=" << (iv / 1000.0) << ")\n";
                    else if (fv > 0.001f && fv < 1e5f)
                        log << "      +0x" << std::hex << i << std::dec << " f32=" << fv << "\n";
                }
            }
        }
        break;
    }
    log << "=== end snapshot ===\n";
    log.flush();
}

} // namespace livetrade
