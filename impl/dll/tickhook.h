// Monthly tick integration (spec 2.6: "recomputed on a fixed monthly tick, aligned to the
// vanilla trade tick"; all writes land at the tick hook).
//
// Two ways to run every month, in increasing order of invasiveness:
//
//  A. POLLING (used by default). A worker thread watches the engine's trade state for the
//     signature of a completed monthly update -- the driver rebuilds every node's
//     trade_goods_size vector each month (pass 4 clears, pass 5 refills), so the vector
//     contents changing across the whole map is the tick's fingerprint. On detection the mod
//     re-reads the inject, re-solves, and re-installs. No code patching, no risk to the engine,
//     and it lands after the engine's own pass -- exactly where spec 2.6 wants the write
//     ("immediately after the value pass").
//
//  B. INLINE HOOK at eu4.exe+0xB4BF00 (the write-back point recovered from the driver, where
//     rbx = the finalized CTradeNode and rsi = the manager). Declared here for completeness;
//     the polling path delivers the same observable behaviour without patching code.
#pragma once
#include <windows.h>
#include <cstdint>
#include <string>
#include <vector>
#include "livetrade.h"

namespace tickhook {

// A cheap fingerprint of the whole trade state: sum of every node's per-good quantities plus
// its local value. The monthly driver rebuilds these, so the fingerprint moves once per month.
inline uint64_t trade_fingerprint(const std::vector<livetrade::SimNode>& sim) {
    uint64_t h = 1469598103934665603ULL;
    auto mix = [&](int64_t v) { h ^= (uint64_t)v; h *= 1099511628211ULL; };
    for (auto& s : sim) {
        mix((int64_t)(s.local_value * 1000));
        mix((int64_t)(s.outgoing_value * 1000));
        for (int32_t q : s.goods) mix(q);
    }
    return h;
}

// Run `on_tick` once per detected monthly update, until `stop` is set.
// poll_ms is the sampling period; the monthly update is far slower than this even at speed 5.
template <class F>
inline void run_monthly_loop(F on_tick, volatile bool* stop, int poll_ms = 400) {
    uint64_t last = 0;
    bool first = true;
    while (!*stop) {
        auto sim = livetrade::read_sim_nodes();
        if (!sim.empty()) {
            uint64_t fp = trade_fingerprint(sim);
            if (fp != last) {
                last = fp;
                if (!first) on_tick(sim);      // skip the initial observation
                first = false;
            }
        }
        Sleep(poll_ms);
    }
}

} // namespace tickhook
