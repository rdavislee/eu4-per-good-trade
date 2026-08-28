// TREASURE-FLEET ROUTING (spec 1.11 + the 1.10 ladder).
//
// What the engine already does for us, verified by disassembly of CCountry::SendTreasureFleet
// (0x3E1EC0..0x3E3939, one caller at 0x2F3E33 inside the monthly country update):
//
//   * The fleet walks the TRADE GRAPH hop by hop in a single call. Loop head 0x3E2083: check the
//     visited list, push the current node, stamp it, let every privateering country skim a share
//     of the amount proportional to its power AT THAT NODE, then test for arrival.
//   * Hop selection at 0x3E2358..0x3E2403: scan the current definition's OUTGOING links and take
//     the first whose target still satisfies matrix A -- "is upstream of the overlord's trade
//     capital" (A's BFS at 0xB4D0D0 expands over the INCOMING vectors, so A[c][n] == 1 means n
//     drains into c's capital node; the engine's own string agrees: CANT_REACH says "our Trade
//     capital is not downstream from their Trade capital").
//   * Because the mod rewrites the definitions, that walk is already a Phi_w path -- rung 1 of the
//     1.10 ladder comes for free, and with the gate predicate 0x3E1D30 forced true the overlord
//     always receives (spec 1.11's first sentence, spec 3.12).
//
// What is missing, and why this file exists. When Phi_w does NOT connect the colonial node to the
// overlord's capital, the link scan exhausts on the first pass and 0x3E2418 sets the current node
// straight to the destination -- the fleet TELEPORTS. It still arrives (nothing is lost), but it
// skims at two nodes instead of the four or five a real route would pass, which is exactly the
// en-route privateer share spec 1.11 describes. Measured on the 1444 field at alpha_phi = 2.0:
// 55 of 144 (colonial node, European capital node) pairs do not connect, and the two dominant gold
// nodes -- mexico (11 gold provinces) and lima (2, including Potosi) -- reach NO European capital,
// so the canonical Spanish silver fleet is precisely the case that teleports.
//
// The fix is the ladder itself: rung 1 Phi_w, rung 2 the shortest path inside a single good's
// graph, rung 3 the undirected shortest path. A hook at the top of the hop-selection block supplies
// the next hop; everything else -- the skim loop, the payouts, inflation, the messages -- is the
// engine's own and is untouched.
//
// SAFETY, by construction:
//   * All graph work is PRECOMPUTED once per tick into a flat int16 table (rebuild()), so the hook
//     itself is table lookups plus livetrade::validate_region's VirtualQuery guards -- no allocation,
//     no locking, no throwing, nothing that can re-enter the engine inside its money path. (The
//     region cache that would allocate is only armed inside the model's own tick, never here.)
//   * The hook returns 0 -- "engine, you decide" -- for anything it is not certain about: unknown
//     node, no path, a hop already in the visited list. Worst case is exactly today's behaviour.
//   * Never returning a visited node is what keeps the walk away from 0x3E248C ("Stuck processing
//     trade nodes"), the one branch that pays the privateers and then drops the overlord's gold.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <map>
#include <queue>
#include "detour.h"
#include "livetrade.h"

namespace treasure {

constexpr uintptr_t HOP_SITE = 0x3E2358;   // top of hop selection: mov r8,[r13+0xA8]; mov rax,[r8+0x98]
constexpr uintptr_t LOOP_TOP = 0x3E2083;   // the walk's head: visited check, skim, arrival test
constexpr int STOLEN = 14;                 // the two whole instructions at HOP_SITE

// frame offsets inside SendTreasureFleet, read off the disassembly
constexpr int FR_DEST    = -0x60;          // [rbp-0x60]  destination CTradeNode*
constexpr int FR_VIS_PTR = 0x168;          // [rbp+0x168] visited array (CTradeNode*[])
constexpr int FR_VIS_CNT = 0x174;          // [rbp+0x174] the visited COUNT. NOT 0x3C0: that is a
                                           // parameter home slot the function reuses -- it holds the
                                           // count only between 0x3E20B5 and 0x3E218E, and by the time
                                           // the hook runs 0x3E21D7 has overwritten it with a POINTER,
                                           // which silently disabled this guard entirely (reviewed).
constexpr int NODE_ID    = 0x120;          // CTradeNode -> its index

inline bool  g_installed = false;
inline uint8_t* g_stub = nullptr;
inline uintptr_t g_next_hop = 0;           // the stub reads this after every call
inline uint64_t g_calls = 0, g_supplied = 0, g_declined = 0, g_norow = 0;

// ---- the precomputed ladder -------------------------------------------------------------------
// g_next[from * N + to] = the field index of the first hop, or -1. Built from the mod's own graphs.
inline std::vector<int16_t> g_next;
inline int g_n = 0;
inline std::vector<int> g_field_of_engine_id;   // engine node id -> field index (-1 when unknown)
inline std::vector<int> g_engine_id_of_field;   // field index -> engine node id (-1 when unknown)

// Drop the ladder when the world changes. pick_hop's fail-closed check compares the hop node's id
// against the engine id it expects, but node N's id IS N in any world, so a stale ladder from the
// previous campaign would pass that check and hand the engine hops from the old topology until the
// next tick rebuilt it (reviewed). Called from ticklive::reset_world_state; inert without the marker.
inline void reset() {
    g_next.clear(); g_n = 0;
    g_field_of_engine_id.clear(); g_engine_id_of_field.clear();
}

// one BFS layer helper: fills `first_hop` for every reachable target from `src` over `adj`
inline void bfs_from(int src, const std::vector<std::vector<int>>& adj, std::vector<int16_t>& row) {
    const int N = (int)adj.size();
    std::vector<int> prev(N, -1);
    std::vector<char> seen(N, 0);
    std::queue<int> q; q.push(src); seen[src] = 1;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (v < 0 || v >= N || seen[v]) continue;
            seen[v] = 1; prev[v] = u; q.push(v);
        }
    }
    for (int t = 0; t < N; t++) {
        if (t == src || !seen[t] || row[t] >= 0) continue;   // rung 1 wins over rung 2 wins over rung 3
        int cur = t;                                          // walk back to the hop out of src
        while (prev[cur] != src && prev[cur] != -1) cur = prev[cur];
        if (prev[cur] == src) row[t] = (int16_t)cur;
    }
}

// Rebuild the table from the current plan. Called once per tick from the model's own tick, never
// from the engine's money path.
inline void rebuild(int N,
                    const std::vector<std::pair<int,int>>& phi_w,
                    const std::vector<std::vector<std::pair<int,int>>>& good_graphs,
                    const std::vector<std::vector<int>>& link_targets,
                    const std::map<int, std::string>& id_to_name,
                    const std::vector<std::string>& names) {
    if (N <= 0 || N > 4096) return;
    std::vector<std::vector<int>> phi(N), und(N);
    for (auto& [u, v] : phi_w)
        if (u >= 0 && u < N && v >= 0 && v < N) { phi[u].push_back(v); und[u].push_back(v); und[v].push_back(u); }
    for (int u = 0; u < N && u < (int)link_targets.size(); u++)
        for (int v : link_targets[u])
            if (v >= 0 && v < N) { und[u].push_back(v); und[v].push_back(u); }

    std::vector<int16_t> next((size_t)N * N, -1);
    for (int s = 0; s < N; s++) {
        std::vector<int16_t> row(N, -1);
        bfs_from(s, phi, row);                                  // rung 1: the Phi_w path
        bool complete = true;
        for (int t = 0; t < N; t++) if (t != s && row[t] < 0) { complete = false; break; }
        if (!complete) {                                        // rung 2: one good's graph
            for (auto& g : good_graphs) {
                std::vector<std::vector<int>> ga(N);
                for (auto& [u, v] : g) if (u >= 0 && u < N && v >= 0 && v < N) ga[u].push_back(v);
                bfs_from(s, ga, row);
            }
            bfs_from(s, und, row);                              // rung 3: undirected
        }
        std::memcpy(&next[(size_t)s * N], row.data(), sizeof(int16_t) * N);
    }

    // engine node id <-> field index, so the hook can translate without touching a std::map
    int maxid = 0;
    for (auto& [id, nm] : id_to_name) if (id > maxid) maxid = id;
    std::vector<int> f_of(maxid + 1, -1), e_of(N, -1);
    std::map<std::string, int> field_of_name;
    for (int i = 0; i < N && i < (int)names.size(); i++) field_of_name[names[i]] = i;
    for (auto& [id, nm] : id_to_name) {
        auto it = field_of_name.find(nm);
        if (it == field_of_name.end() || id < 0 || id > maxid) continue;
        f_of[id] = it->second;
        if (it->second >= 0 && it->second < N) e_of[it->second] = id;
    }
    g_next.swap(next); g_field_of_engine_id.swap(f_of); g_engine_id_of_field.swap(e_of); g_n = N;
}

// ---- the hook's C++ side: integer lookups only -------------------------------------------------
inline int field_of_node(uintptr_t node) {
    if (!node || !livetrade::validate_region(node + NODE_ID, 4)) return -1;
    int id = livetrade::fi(node + NODE_ID);
    if (id < 0 || id >= (int)g_field_of_engine_id.size()) return -1;
    return g_field_of_engine_id[id];
}

extern "C" void __fastcall pick_hop(uintptr_t cur, uintptr_t rbp) {
    g_next_hop = 0;
    g_calls++;
    if (g_n <= 0 || g_next.empty()) { g_norow++; return; }
    uintptr_t mgr = livetrade::trade_manager();
    if (!mgr || !livetrade::validate_region(mgr + 0x18, 16)) { g_norow++; return; }
    uintptr_t base = livetrade::fq(mgr + 0x18);
    int cnt = livetrade::fi(mgr + 0x24);
    if (!base || cnt <= 0 || cnt > 4096) { g_norow++; return; }
    if (!rbp || !livetrade::validate_region(rbp + FR_VIS_PTR, 8)) { g_norow++; return; }

    uintptr_t dest = livetrade::fq(rbp + FR_DEST);
    int cf = field_of_node(cur), df = field_of_node(dest);
    if (cf < 0 || df < 0 || cf == df) { g_declined++; return; }

    if (cf >= g_n || df >= g_n || (size_t)cf * g_n + df >= g_next.size()) { g_declined++; return; }
    int16_t hop = g_next[(size_t)cf * g_n + df];
    if (hop < 0 || hop >= g_n) { g_declined++; return; }            // no ladder answer: engine decides
    int eid = g_engine_id_of_field[hop];
    if (eid < 0 || eid >= cnt) { g_declined++; return; }
    uintptr_t hop_node = base + (uintptr_t)eid * 0x138;
    if (!livetrade::validate_region(hop_node + NODE_ID, 4)) { g_declined++; return; }
    if (livetrade::fi(hop_node + NODE_ID) != eid) { g_declined++; return; }   // fail closed if the
                                                    // manager's base/stride is ever not what we think

    // never hand back a node the walk has already stamped: that is the 0x3E248C abort, the one
    // branch that pays privateers and then drops the overlord's gold
    uintptr_t vis = livetrade::fq(rbp + FR_VIS_PTR);
    int vn = livetrade::validate_region(rbp + FR_VIS_CNT, 4) ? livetrade::fi(rbp + FR_VIS_CNT) : 0;
    if (vis && vn > 0 && vn < 4096 && livetrade::validate_region(vis, (size_t)vn * 8)) {
        for (int i = 0; i < vn; i++)
            if (*(uintptr_t*)(vis + (uintptr_t)i * 8) == hop_node) { g_declined++; return; }
    }
    g_next_hop = hop_node;
    g_supplied++;
}

// ---- the stub ---------------------------------------------------------------------------------
// Saves every volatile register (xmm included -- this is the middle of a live function), calls
// pick_hop, and then either redirects the walk to our hop or runs the stolen bytes and falls back
// into the engine's own link scan.
inline bool install(std::string* err) {
    if (g_installed) return true;
    uintptr_t base = livetrade::module_base();
    uintptr_t site = base + HOP_SITE;
    const uint8_t expect[STOLEN] = {
        0x4D, 0x8B, 0x85, 0xA8, 0x00, 0x00, 0x00,      // mov r8, [r13+0xA8]
        0x49, 0x8B, 0x80, 0x98, 0x00, 0x00, 0x00 };    // mov rax, [r8+0x98]
    if (!livetrade::validate_region(site, STOLEN) || memcmp((void*)site, expect, STOLEN) != 0) {
        if (err) *err = "hop-selection site bytes differ (patched binary?)";
        return false;
    }
    uint8_t* s = detour::alloc_near(site, 256);
    if (!s) { if (err) *err = "no memory within rel32 of the hop site"; return false; }
    g_stub = s;
    uint8_t* p = s;
    auto emit = [&](std::initializer_list<uint8_t> b) { for (uint8_t x : b) *p++ = x; };
    auto imm64 = [&](uint64_t v) { memcpy(p, &v, 8); p += 8; };

    emit({0x50, 0x51, 0x52, 0x41, 0x50, 0x41, 0x51, 0x41, 0x52, 0x41, 0x53, 0x53}); // push rax,rcx,rdx,r8,r9,r10,r11,rbx (8 -> stays 16-aligned)
    emit({0x48, 0x81, 0xEC, 0x80, 0x00, 0x00, 0x00});                               // sub rsp, 0x80
    for (int i = 0; i < 6; i++) {                                                   // movdqu [rsp+16i], xmm0..5
        emit({0xF3, 0x0F, 0x7F}); *p++ = (uint8_t)(0x44 | (i << 3)); emit({0x24, (uint8_t)(i * 16)});
    }
    emit({0x4C, 0x89, 0xE9});                                                       // mov rcx, r13   (current node)
    emit({0x48, 0x89, 0xEA});                                                       // mov rdx, rbp
    emit({0x48, 0x83, 0xEC, 0x20});                                                 // sub rsp, 0x20  (shadow)
    emit({0x48, 0xB8}); imm64((uint64_t)&pick_hop);                                 // mov rax, &pick_hop
    emit({0xFF, 0xD0});                                                             // call rax
    emit({0x48, 0x83, 0xC4, 0x20});                                                 // add rsp, 0x20
    for (int i = 0; i < 6; i++) {                                                   // movdqu xmm0..5, [rsp+16i]
        emit({0xF3, 0x0F, 0x6F}); *p++ = (uint8_t)(0x44 | (i << 3)); emit({0x24, (uint8_t)(i * 16)});
    }
    emit({0x48, 0x81, 0xC4, 0x80, 0x00, 0x00, 0x00});                               // add rsp, 0x80
    emit({0x5B, 0x41, 0x5B, 0x41, 0x5A, 0x41, 0x59, 0x41, 0x58, 0x5A, 0x59});       // pop rbx,r11,r10,r9,r8,rdx,rcx
    // rax is still on the stack; use it as scratch for the decision
    emit({0x48, 0xB8}); imm64((uint64_t)&g_next_hop);                               // mov rax, &g_next_hop
    emit({0x48, 0x8B, 0x00});                                                       // mov rax, [rax]
    emit({0x48, 0x85, 0xC0});                                                       // test rax, rax
    uint8_t* jz_at = p; emit({0x74, 0x00});                                         // jz -> fallback (back-patched)
    // REDIRECT. 0x3E2083 has a loop-carried live-in: EDX is the visited count, and all three of the
    // engine's own backedges load it from [rbp+0x174] immediately before jumping. Jumping without it
    // would send a stale value into the visited scan and the append -- an out-of-bounds write of r13
    // at [visited + edx*8], or a silently corrupted count that lets the walk revisit nodes and pay
    // privateers twice (reviewed).
    emit({0x8B, 0x95, 0x74, 0x01, 0x00, 0x00});                                     // mov edx, [rbp+0x174]
    emit({0x49, 0x89, 0xC5});                                                       // mov r13, rax   (our hop)
    emit({0x58});                                                                   // pop rax        (restore)
    emit({0xFF, 0x25}); { uint32_t z = 0; memcpy(p, &z, 4); p += 4; } imm64(base + LOOP_TOP);  // jmp [rip+0] -> loop top
    // fallback: restore rax, run the stolen bytes, continue into the engine's own scan
    *(jz_at + 1) = (uint8_t)((p - (jz_at + 2)) & 0xFF);                             // the real displacement
    emit({0x58});                                                                   // pop rax
    memcpy(p, expect, STOLEN); p += STOLEN;
    emit({0xFF, 0x25}); { uint32_t z = 0; memcpy(p, &z, 4); p += 4; } imm64(site + STOLEN);

    detour::Freeze freeze(site, site + STOLEN);        // the project's own discipline: no thread may
    if (!freeze.ok) { if (err) *err = freeze.why; return false; }   // sit in the range we overwrite
    DWORD old = 0;
    if (!VirtualProtect((void*)site, STOLEN, PAGE_EXECUTE_READWRITE, &old)) {
        if (err) *err = "VirtualProtect failed at the hop site"; return false;
    }
    uint8_t patch[STOLEN];
    memset(patch, 0xCC, STOLEN);                        // trap, not nop: nothing may fall through here
    int32_t rel = (int32_t)((intptr_t)s - (intptr_t)(site + 5));
    patch[0] = 0xE9; memcpy(patch + 1, &rel, 4);
    memcpy((void*)site, patch, STOLEN);
    VirtualProtect((void*)site, STOLEN, old, &old);
    FlushInstructionCache(GetCurrentProcess(), (void*)site, STOLEN);
    g_installed = true;
    return true;
}

} // namespace treasure
