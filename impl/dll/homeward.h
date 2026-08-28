// A NEWLY PLACED TRANSFERRING MERCHANT POINTS HOME (user rule, 2026-08-26).
//
// The engine's SetTrader (0xB596E0) picks a transferring merchant's link by scoring the node's
// DEFINITION outgoing entries -- the Phi_w-downstream links -- so the node window's "Transfer Trade
// Power" button parks the merchant on forward link #0 (or, at an END node, on nothing), and the
// player then has to click the reverse panel toward home next month. Under D2 a merchant exists to
// steer goods home, and the homeward direction from a node is geography: the neighbour on the
// shortest link path to the country's trade capital. So whenever a SetTrader call leaves a merchant
// transferring at a node where the assignment table has no entry for that country, the table gets
// (country, node) -> next hop toward home. The table is what the routing, the panels, the tooltips
// and the node window honour; syncrec.h carries it into the record each tick. An AI placement sets
// its own entry right after (envoy.h) and simply overwrites this default.
//
// The per-tick data (names, undirected link graph, each country's home) is published by the tick.
#pragma once
#include <cstdint>
#include <map>
#include <mutex>
#include <string>
#include <vector>
#include "livetrade.h"
#include "assign.h"

namespace homeward {

inline std::vector<std::string> g_names;
inline std::vector<std::vector<int>> g_und;         // undirected link adjacency by field index
inline std::map<int, int> g_home_of;                // country index -> home field index
inline std::map<uintptr_t, int> g_field_of_node;    // CTradeNode* -> field index
inline std::map<std::pair<int, int>, double> g_flow;   // (from, to) -> the model's away-flow, for the tie-break among equal hops
inline uint64_t g_set = 0, g_had = 0, g_nohome = 0, g_nopath = 0, g_athome = 0, g_unknown_node = 0, g_multihome = 0, g_multicollect = 0;
inline bool g_ready = false;
inline bool g_reach_dirty = false;   // a SetTrader call happened: the engine's reachability tables (merchant cones) need a rebuild

inline void publish(const std::vector<std::string>& names, const std::vector<std::vector<int>>& und,
                    const std::map<int, std::vector<int>>& collect_nodes,
                    const std::vector<livetrade::SimNode>& sim,
                    const std::map<std::pair<int, int>, double>* flow = nullptr) {
    g_names = names; g_und = und;
    if (flow) g_flow = *flow; else g_flow.clear();   // one copy per tick (~320 entries)
    g_home_of.clear();
    for (auto& [c, nodes] : collect_nodes) if (!nodes.empty()) {   // D1: a country collects only at its capital -- measured, not assumed
        int ci = livetrade::country_index_of(c);
        auto ex = g_home_of.find(ci);
        if (ex != g_home_of.end() && ex->second != nodes[0]) g_multihome++;
        if (nodes.size() > 1) g_multicollect++;
        g_home_of[ci] = nodes[0];
    }
    g_field_of_node.clear();
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)names.size(); i++) fidx[names[i]] = i;
    for (auto& s : sim) { auto it = fidx.find(s.name); if (it != fidx.end() && s.obj) g_field_of_node[s.obj] = it->second; }
    g_ready = true;
}

// the neighbour of `from` on a shortest undirected path to `home` ("" if none)
inline std::string next_hop(int from, int home) {
    int N = (int)g_und.size();
    if ((int)g_names.size() != N) return std::string();
    if (from < 0 || home < 0 || from >= N || home >= N || from == home) return std::string();
    std::vector<int> dist(N, -1);
    std::vector<int> q; q.push_back(home); dist[home] = 0;
    for (size_t qi = 0; qi < q.size(); qi++) {
        int x = q[qi];
        for (int y : g_und[x]) if (y >= 0 && y < N && dist[y] < 0) { dist[y] = dist[x] + 1; q.push_back(y); }
    }
    if (dist[from] < 0) return std::string();
    // among the hops on a shortest path, the one the goods actually leave `from` along (the model's
    // away-flow): bordeaux has no link to sevilla, and of its two one-step hops (ivory_coast,
    // carribean_trade) the merchant belongs on the one carrying the trade (user, 2026-08-26)
    int best = -1; double bestf = -1.0;
    for (int y : g_und[from]) if (y >= 0 && y < N && dist[y] == dist[from] - 1) {
        auto f = g_flow.find({from, y}); double v = f == g_flow.end() ? 0.0 : f->second;
        if (best < 0 || v > bestf + 1e-12 || (v >= bestf - 1e-12 && g_names[y] < g_names[best])) { best = y; bestf = v; }   // ties by name, never by the engine's link order
    }
    return best >= 0 ? g_names[best] : std::string();
}

// called from the SetTrader hook once the call is known to leave the merchant transferring
inline void auto_target(uintptr_t node, uint64_t handle) {
    if (!g_ready) return;
    int cidx = (int)(int16_t)(handle >> 32);
    if (cidx < 0) return;
    auto f = g_field_of_node.find(node);
    if (f == g_field_of_node.end()) { g_unknown_node++; return; }
    int fn = f->second;
    auto h = g_home_of.find(cidx);
    if (h == g_home_of.end()) { g_nohome++; return; }
    if (h->second == fn) { g_athome++; return; }
    { std::lock_guard<std::mutex> lk(assign::g_mx); if (assign::g_table.count({cidx, g_names[fn]})) { g_had++; return; } }   // the table already decides
    std::string hop = next_hop(fn, h->second);
    if (hop.empty()) { g_nopath++; return; }
    assign::set(cidx, g_names[fn], hop);
    g_set++;
}

} // namespace homeward
