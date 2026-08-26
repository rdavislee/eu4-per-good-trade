// SENDING A MERCHANT TO THE NODE THE PLAN CHOSE (spec 3.14; the frontier model's last link).
//
// frontier::plan says where a country's k merchants should stand. aiwire can only write a
// placement where a merchant already IS; a planned node with no merchant there was counted as
// g_wants_move and nothing happened -- 1,005 of them on tick 7, against 8 placed. This is the
// mechanic that closes the gap.
//
// THE SEAM, from the send-merchant trace: the engine has a direct placement function, used by its
// own trade-company code (0x3BAB22, 0x3BB173) and by 0x774E05 (which picks a free envoy and calls
// it with mode=0, link=-1, force=0):
//
//   0x3BAD90  PlaceMerchantAtNode(CCountry* country /*rcx*/, CEnvoy* envoy /*rdx*/,
//                                 uint8 mode /*r8b: 0 collect, 1 transfer*/, CTradeNode* node /*r9*/,
//                                 int32 steerLinkIndex /*[rsp+0x20]; -1 = engine's choice*/,
//                                 uint8 force /*[rsp+0x28]; 1 skips the eligibility check*/)
//
// Body: operator new(0xA0) -> CMerchantConstruction ctor 0x25AAF0 -> mc+0x40 = country+0x20 (the
// handle) -> location province of the node -> SetEnvoy(mc, prov, envoy, force*2+1) -> envoy+0x18
// = 2 (posted) -> if steerLinkIndex >= 0, GetTraderRecord(node, handle) and rec+0xA8 = it
// (0x3BAE33). The force*2+1 is load-bearing: SetEnvoy's tail takes r9d in {1,3} as "instant"
// (progress 0x3E8, dates collapsed, 0x25C9C4..0x25C9DC) and tail-jumps into Update, where
// `cmp ecx,3; je` at 0x25B920 skips CanSendMerchantTo entirely and lands on SetTrader at
// 0x25B9A3. So one call places, registers the trade record, and sets the steer index -- with the
// +0xA8 write landing AFTER SetTrader's own link scoring (0xB599AE), so our override wins. No
// command queue, no gate, no travel delay.
//
// Caveat from the trace: SetTrader on that path is guarded by rec+0xAE == 0 (0x25B98E), so at a
// node where the country ALREADY has a trader the envoy is placed but the record's mode is not
// rewritten. We never call it in that state: a planned node with a merchant standing there is
// handled by aiwire (table + syncrec), and dispatch only targets nodes with none.
//
// Merchants never collect (user decision 2026-08-26): mode is always 1. steerLinkIndex is passed
// as -1 and the real target is written by syncrec from the table on the next tick, because a
// reverse end has no link index to pass.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include "livetrade.h"
#include "assign.h"
#include "aiwire.h"
#include "../src/frontier.h"

namespace envoy {

constexpr uintptr_t PLACE_MERCHANT = 0x3BAD90;
constexpr int ENVOY_ACTION = 0x18;      // 0 free / 1 travelling / 2 posted
constexpr int ENVOY_ID     = 0x44;

using FnPlace = void (__fastcall*)(uintptr_t country, uintptr_t envoy, uint8_t mode, uintptr_t node,
                                   int32_t steerLinkIndex, uint8_t force);

inline uint64_t g_sent = 0, g_no_free = 0, g_no_node = 0, g_stale_record = 0;
inline std::map<std::pair<int, int>, int> g_sent_tick;   // (country, node) -> tick, dwell
inline std::map<int, int> g_nothing_tick;                  // country -> tick it last placed nothing
inline std::string g_log;
inline bool g_installed = false;

// the engine node object for a field index, by name
inline uintptr_t node_obj(const std::vector<livetrade::SimNode>& sim, const std::string& name) {
    for (auto& s : sim) if (s.name == name) return s.obj;
    return 0;
}

// a free envoy (action 0) of this country, or 0
inline uintptr_t free_envoy(int country_idx) {
    uintptr_t c = aiwire::country_by_index(country_idx);
    if (!c || !livetrade::validate_region(c + 0x1480, 8)) return 0;
    uintptr_t vec = livetrade::fq(c + 0x1480);
    if (!vec || !livetrade::validate_region(vec + 8, 8)) return 0;
    uintptr_t cont = livetrade::fq(vec + 8);
    if (!cont || !livetrade::validate_region(cont + 0x20, 16)) return 0;
    uintptr_t first = livetrade::fq(cont + 0x20), last = livetrade::fq(cont + 0x28);
    if (!first || last <= first || (last - first) > 8 * 256) return 0;
    if (!livetrade::validate_region(first, last - first)) return 0;          // C-2: the whole span
    for (uintptr_t p = first; p + 8 <= last; p += 8) {
        uintptr_t e = livetrade::fq(p);
        if (e && livetrade::validate_region(e, 0x48) && livetrade::fb(e + ENVOY_ACTION) == 0) return e;   // C-1: a byte
    }
    return 0;
}

// Place a free merchant of `country_idx` at `node` transferring. Returns false, touching nothing,
// if there is no free merchant or the node is unresolved.
inline bool send(int country_idx, uintptr_t node, std::ofstream* lg, const std::string& node_name) {
    uintptr_t c = aiwire::country_by_index(country_idx);
    if (!c || !node) { g_no_node++; return false; }
    uintptr_t e = free_envoy(country_idx);
    if (!e) { g_no_free++; return false; }
    auto place = (FnPlace)(livetrade::module_base() + PLACE_MERCHANT);
    place(c, e, 1, node, -1, 1);
    g_sent++;
    if (lg) *lg << "  [envoy] country#" << country_idx << " merchant#" << livetrade::fi(e + ENVOY_ID)
                << " placed at " << node_name << " (transfer; target set by the table next tick)" << (char)10;
    return true;
}

// One pass per AI tick, after aiwire::step: for each country, for each planned node with no
// merchant standing there, send a free one. Dwell-floored so a merchant is not bounced.
inline int dispatch(const std::vector<livetrade::SimNode>& sim,
                    const std::vector<std::string>& names,
                    const std::vector<econ::NodeStandings>& st,
                    const std::vector<std::vector<int>>& undirected_adj,
                    const std::vector<econ::GoodFlow>& per_good,
                    int tick, std::ofstream* lg) {
    if (!g_installed) return 0;
    // DO OUR PLACEMENTS STICK? Every (country,node) we sent to is in g_sent_tick; count how
    // many still have one of that country's merchants standing there this tick.
    { int still = 0, gone = 0;
      std::map<int, std::set<int>> where;   // country -> field nodes with a posted merchant
      std::map<int, int> e2f;
      for (int fn = 0; fn < (int)names.size(); fn++) for (auto& s : sim) if (s.name == names[fn]) { e2f[s.index] = fn; break; }
      for (auto& [key, t0] : g_sent_tick) {
          int c = key.first; if (!where.count(c)) { for (auto& m : aiwire::merchants_of(livetrade::country_index_of(c))) if (m.action == 2) { auto f = e2f.find(m.node_index); if (f != e2f.end()) where[c].insert(f->second); } }
          if (where[c].count(key.second)) still++; else gone++;
      }
      if (lg && (still || gone)) *lg << "  [envoy] of " << (still + gone) << " nodes we ever sent a merchant to, " << still << " still hold one, " << gone << " do not" << (char)10;
    }
    int sent = 0;
    std::set<int> countries;
    for (auto& ns : st) for (auto& e : ns.entries) if (e.power > 0) countries.insert(e.country);
    // hoisted: the same for every country, was rebuilt per country (80 x sim.size() string compares)
    std::map<int, int> eng_to_field;
    for (int fn = 0; fn < (int)names.size(); fn++)
        for (auto& s : sim) if (s.name == names[fn]) { eng_to_field[s.index] = fn; break; }
    for (int c : countries) {
        int cidx = livetrade::country_index_of(c);
        if (aiwire::g_shard >= 0 && (cidx % 3) != aiwire::g_shard) continue;   // same shard as step
        int home = -1;
        for (int fn = 0; fn < (int)st.size() && home < 0; fn++)
            for (auto& e : st[fn].entries) if (e.country == c && e.is_capital) { home = fn; break; }
        if (home < 0) continue;
        auto ms = aiwire::merchants_of(cidx);
        if (ms.empty()) continue;
        int k = (int)ms.size();
        // nothing to dispatch if no merchant is free: every plan() call for such a country is
        // wasted (measured: dispatch 190 ms of a 375 ms AI tick, most countries saturated)
        { bool any_free = false; for (auto& m : ms) if (m.action == 0) { any_free = true; break; }
          if (!any_free) { g_no_free++; continue; } }
        // a country whose free merchant could not be placed last pass will not place now either
        // (the plan is the same until the standings move); skip it for the dwell floor
        { auto ns = g_nothing_tick.find(c); if (ns != g_nothing_tick.end() && tick - ns->second < (int)ai::DWELL_FLOOR_MONTHS) continue; }
        std::set<int> standing;
        for (auto& m : ms) if (m.action == 2) { auto f = eng_to_field.find(m.node_index); if (f != eng_to_field.end()) standing.insert(f->second); }
        const auto& plan = aiwire::cached_plan((int)names.size(), home, k, undirected_adj, st, c);
        int sent_here = 0;
        for (auto& pl : plan) {
            if (standing.count(pl.node)) continue;               // aiwire handles the ones already there
            if (pl.node == home) continue;                        // never at the capital
            // D-1 (review): the engine's record can say has_trader=1 with no envoy there -- 0x775C14
            // frees an envoy without ClearTrader, and Update then bails forever on +0x58. Placing
            // another merchant on such a record is not caught by the envoy list; read the record.
            {
                uintptr_t nd0 = node_obj(sim, names[pl.node]);
                uintptr_t rb = nd0 ? livetrade::rq(nd0 + 0x18) : 0; int rc = nd0 ? livetrade::ri(nd0 + 0x24) : 0;
                if (rb && cidx >= 0 && cidx < rc && livetrade::validate_region(rb + (uintptr_t)cidx * 0xC0 + 0xAE, 1)
                    && livetrade::fb(rb + (uintptr_t)cidx * 0xC0 + 0xAE) != 0) { g_stale_record++; continue; }
            }
            auto key = std::make_pair(c, pl.node);
            auto it = g_sent_tick.find(key);
            if (it != g_sent_tick.end() && tick - it->second < (int)ai::DWELL_FLOOR_MONTHS) continue;
            uintptr_t nd = node_obj(sim, names[pl.node]);
            if (!send(cidx, nd, lg, names[pl.node])) break;      // no free merchant: stop for this country
            // the table entry is what routing and syncrec read; write it now
            assign::set(c, names[pl.node], names[pl.target]);
            g_sent_tick[key] = tick;
            // G1: is this end one the engine can index (declared outgoing) or a reverse end?
            {
                bool outgoing = false;
                uintptr_t def = nd ? livetrade::fq(nd + 0xA8) : 0;
                if (def && livetrade::validate_region(def + 0x98, 16)) {
                    uintptr_t b2 = livetrade::fq(def + 0x98), e2 = livetrade::fq(def + 0xA0);
                    for (uintptr_t p2 = b2; b2 && e2 > b2 && p2 + 0x78 <= e2; p2 += 0x78) {
                        uintptr_t t = livetrade::validate_region(p2 + 0x30, 8) ? livetrade::fq(p2 + 0x30) : 0;
                        if (t && livetrade::def_key(t) == names[pl.target]) { outgoing = true; break; }
                    }
                }
                if (outgoing) aiwire::g_phi_out++; else aiwire::g_phi_in++;
            }
            standing.insert(pl.node);
            sent++; sent_here++;
        }
        if (sent_here == 0) g_nothing_tick[c] = tick;
    }
    if (lg && sent) *lg << "  [envoy] dispatched " << sent << " merchants to planned nodes this tick ("
                        << g_sent << " total; " << g_no_free << " refused: no free merchant; " << g_stale_record << " skipped: record already has_trader)" << (char)10;
    return sent;
}

inline bool install(const std::string& logpath, std::string* err) {
    g_log = logpath;
    uintptr_t fn = livetrade::module_base() + PLACE_MERCHANT;
    if (!livetrade::validate_region(fn, 16)) { if (err) *err = "0x3BAD90 unreadable"; return false; }
    // the traced prologue, byte-exact; any other build is refused (spec 2.5)
    static const uint8_t expect[20] = {0x48,0x89,0x5C,0x24,0x10, 0x48,0x89,0x6C,0x24,0x18,
                                       0x48,0x89,0x74,0x24,0x20, 0x57, 0x48,0x83,0xEC,0x20};
    if (memcmp((const void*)fn, expect, 20) != 0) { if (err) *err = "0x3BAD90 prologue differs (patched binary?)"; return false; }
    g_installed = true;
    return true;
}

} // namespace envoy
