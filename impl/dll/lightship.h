// LIGHT SHIPS GO WHERE THE MODEL SAYS STEERING PAYS (user, 2026-08-26: "if they can make money at a
// downstream Phi_w node by putting trade ships there and steering against Phi_w, they should").
//
// Vanilla's protect-trade AI (CAITrade::EvaluateTradeFleets 0x1BA150, on the same 10-24 day cadence
// as the silenced merchant AI) scores every eligible node inline -- (1 - share) x node value, halved
// when collecting, crowding, a reach penalty from matrix C, personality multipliers, rival ships --
// and then hands the allocation to 0x1B8340(this, &deficit, &budget, shipsPerNode, SCORE, power,
// share, shipPower, &totalScore, privateerNode, privateerBudget), which splits the light-ship budget
// across nodes in proportion to SCORE (nodes below 1000 = 1 ducat get nothing), recalls surplus
// fleets, picks the fleet with 0xDB950 and posts the trade_mission command (token 0x2DBB). The
// allocation depends on exactly two inputs: SCORE (arg 5, [rsp+0x28] at entry) and *totalScore
// (arg 9, [rsp+0x48]); power/share/shipPower feed only the debug log (static RE 2026-08-26).
//
// So the model owns the SCORE: a prologue detour on 0x1B8340 overwrites the array with the value the
// tick published for this country -- per node, the gain of the country's steering placement standing
// there (frontier::added_value, the same figure that ranks its merchants) plus, at its home node, the
// pool it does not yet own -- and the total. Everything downstream stays the engine's: fleet choice,
// the surplus recall, the command, the validity check, the log. A ship's contribution is what the
// engine credits: unit trade_power into rec+0x1C, rolled into max_pow (+0x4C) monthly.
#pragma once
#include <windows.h>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <map>
#include <mutex>
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"

namespace lightship {

constexpr uintptr_t ALLOCATE = 0x1B8340;
constexpr int ARG_SCORE = 0x28, ARG_TOTAL = 0x48;   // stack slots of args 5 and 9 at entry (rsp unchanged)
constexpr int AI_COUNTRY_HANDLE = 0x28;             // the AI-trade object's owning country handle
constexpr int GAME_NODE_COUNT = 0x21BC;             // G + 0x21BC = trade node count (tm+0x24)

inline detour::Hook g_hook;
inline std::string g_log;
inline std::mutex g_mx;
inline std::map<int, std::map<int, int32_t>> g_scores;   // country index -> engine node index -> score x1000
inline uint64_t g_calls = 0, g_rewritten = 0, g_nocountry = 0, g_badargs = 0, g_logged = 0;
// THE SCALE. Vanilla's score is a gross quantity ((1 - share) x the node's whole value, 1e5..1e6 in
// x1000 units); the model's is marginal (the gain of one placement, often under 1000 = 1 ducat), and
// the allocator drops any node below 1000 and RECALLS ships standing at a node it assigned nothing.
// Only the ratios matter to the proportional split, so the best node is put at vanilla's magnitude and
// the rest scaled with it: the ranking is the model's, the floor then means "under 0.1% of the best".
constexpr double SCORE_TOP = 1.0e6;
constexpr int32_t FLOOR = 1000;

inline void publish(int cidx, std::map<int, int32_t>&& scores) {
    std::lock_guard<std::mutex> lk(g_mx);
    if (scores.empty()) g_scores.erase(cidx); else g_scores[cidx] = std::move(scores);
}
inline void clear_all() { std::lock_guard<std::mutex> lk(g_mx); g_scores.clear(); g_logged = 0; }

inline void on_allocate(detour::Regs* r) {
    g_calls++;
    static const bool s_off = livetrade::marker_present("NOSHIPS");   // read once: this runs on the AI tick
    if (s_off) return;                                                 // vanilla's own scores
    uintptr_t self = r->rcx;
    if (!self || !livetrade::validate_region(self + AI_COUNTRY_HANDLE, 8)) { g_badargs++; return; }
    int cidx = (int)(int16_t)(livetrade::fq(self + AI_COUNTRY_HANDLE) >> 32);
    uintptr_t rsp = r->rsp();
    if (!livetrade::validate_region(rsp + ARG_SCORE, ARG_TOTAL - ARG_SCORE + 8)) { g_badargs++; return; }
    int32_t* score = *(int32_t**)(rsp + ARG_SCORE);
    int32_t* total = *(int32_t**)(rsp + ARG_TOTAL);
    uintptr_t g = livetrade::game_singleton();
    int N = (g && livetrade::validate_region(g + GAME_NODE_COUNT, 4)) ? livetrade::fi(g + GAME_NODE_COUNT) : 0;
    if (!score || !total || N <= 0 || N > 512 || !livetrade::validate_region((uintptr_t)score, (size_t)N * 4) ||
        !livetrade::validate_region((uintptr_t)total, 4)) { g_badargs++; return; }
    std::map<int, int32_t> mine;
    { std::lock_guard<std::mutex> lk(g_mx); auto it = g_scores.find(cidx); if (it == g_scores.end()) { g_nocountry++; return; } mine = it->second; }
    double mx = 0; for (auto& [k, v] : mine) if (v > mx) mx = v;
    double scale = mx > 0 ? SCORE_TOP / mx : 0.0;
    int64_t sum = 0, vanilla_sum = 0; int nz = 0, eligible = 0;
    for (int i = 0; i < N; i++) {
        vanilla_sum += score[i];
        if (i == 0) { score[0] = 0; continue; }                      // index 0 is the allocator's "invalid node" singleton (0xB60B80)
        auto s = mine.find(i);
        double raw = (s == mine.end() || s->second < 0) ? 0.0 : (double)s->second;
        int32_t v = (int32_t)std::min(raw * scale, (double)INT32_MAX);
        score[i] = v;
        if (v > 0) nz++;
        if (v >= FLOOR) { sum += v; eligible++; }                     // the split spends only these: the divisor must match
    }
    *total = (int32_t)std::min<int64_t>(sum, INT32_MAX);
    g_rewritten++;
    if (!g_log.empty() && g_logged < 12) {
        g_logged++;
        std::ofstream f(g_log, std::ios::app);
        f << "  [ships] country#" << cidx << ": model scores on " << nz << " of " << N << " nodes (" << eligible << " at or above the floor), best " << (long long)mx
          << " ducats x1000 scaled to " << (long long)SCORE_TOP << ", total " << sum << " (vanilla's total was " << vanilla_sum << "), light-ship budget "
          << (livetrade::validate_region(r->r8, 4) ? livetrade::fi(r->r8) : -1) << (char)10;
    }
}

inline bool install(const std::string& logpath, std::string* err) {
    g_log = logpath;
    if (g_hook.active) return true;
    // 48 8B C4 | 4C 89 40 18 | 48 89 50 10 | 48 89 48 08  -- 15 relocatable bytes ending on `push rbp`
    std::vector<uint8_t> expected = { 0x48, 0x8B, 0xC4, 0x4C, 0x89, 0x40, 0x18, 0x48, 0x89, 0x50, 0x10, 0x48, 0x89, 0x48, 0x08 };
    if (!detour::install(g_hook, livetrade::module_base() + ALLOCATE, expected, &on_allocate, "light-ship allocation")) {
        if (err) *err = g_hook.error; return false;
    }
    return true;
}

} // namespace lightship
