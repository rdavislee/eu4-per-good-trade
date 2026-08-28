// THE MONEY TESTS (TESTING.md E2 and E4; spec 2.6's two deadlines; probe 3).
//
// E2 -- "the income the treasury actually books equals the displayed trade income from during the
// month". Pass 10 computes each collector's `rec.money` and hands it to
// CCountry::AddDelayedIncome(country, 2 /*trade*/, &money) (0x338A90), which adds it into the
// country's monthly income accumulator at country+0x68 and into the ledger at country+0x760.
// So the check is a before/after on that accumulator: sample it in the tick hook (which runs
// immediately BEFORE pass 10) and again once pass 10 has finished, and compare the delta with
// Sigma rec.money over that country's collecting nodes. Agreement means the figure the engine
// displays during the month is exactly the figure it books -- which is also the observation
// spec 2.7 probe 3 asks for ("whether writing country trade income before month-boundary
// reconciliation makes AI budgeting and AI cash read the same figure").
//
// E4 -- "nothing NaNs, nothing leaks": no negative collected income, no node value exploding or
// draining without cause, no value appearing from or vanishing to nowhere. The solver already
// asserts conservation per tick; this is its visible face, checked on the ENGINE's own fields
// after the mod has written them.
#pragma once
#include <cmath>
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "booklog.h"

namespace money {

// country index -> its income accumulator (country+0x68) sampled before pass 10
inline std::map<int, double> g_accum_before;
// country index -> Sigma rec.money the engine computed this month
inline std::map<int, double> g_money_expected;
inline int g_e2_checked = 0, g_e2_agree = 0;
inline int g_pass10_seen = 0, g_pass10_total = 0;   // declared here: check_e2 reads them
inline long long g_pass10_calls_total = 0;   // every 0xB584F0 call through the wrapper, ever
// Anything that must read the records AFTER pass 10 has paid them registers here and runs from
// the wrapper's last-node branch -- inside the same pass, no thread, no sleep. E1 and E4 used to
// run on a worker thread after a fixed Sleep(400), which raced pass 10: once the booking log's
// thunks lengthened the pass, the read landed on half-paid records and E1 fell to 338/662.
inline void (*g_after_pass10)(const std::vector<livetrade::SimNode>&, std::ofstream&) = nullptr;
inline unsigned long long g_pass10_t0 = 0;   // QueryPerformanceCounter at the first node
inline double g_e2_worst = 0;

// Sample every country's accumulator, and the money pass 10 is about to hand out. Called from the
// tick hook, i.e. after our write and before the collector division.
// The ACCUMULATOR only, for every country holding a record anywhere. rec.money is NOT read
// here: at pass 10's first node no collector has been paid yet, and reading payouts now
// gave paid == 0 for every country, so check_e2 skipped them all (0/0, measured).
inline void sample_before(const std::vector<livetrade::SimNode>& sim) {
    g_accum_before.clear();
    for (auto& s : sim)
        for (auto& rec : livetrade::read_standings(s.obj)) {
            int c = livetrade::country_index_of(rec.tag_index);
            if (!g_accum_before.count(c)) {
                uintptr_t country = livetrade::country_at(c);
                g_accum_before[c] = country ? livetrade::country_income_accum(country) : 0.0;
            }
        }
}

// After pass 10: rec.money now holds what each collector was paid. Compare the accumulator delta
// against the sum of those payments.
// E2, re-based on what the engine BOOKS. country+0x68 was assumed to be the monthly income
// accumulator because AddDelayedIncome does `add [country+0x68], eax` (0x338AFC). Measured with
// every AddDelayedIncome call in pass 10 logged: Ming's records carry money = 4.67+2.87+1.15 =
// 8.69, and pass 10 books 8.689 of category 2 (trade) to Ming -- to the cent -- while +0x68 moved
// 0.253. So +0x68 is not the figure the treasury shows (the per-category ledger at country+0x760,
// 0x338B05..0x338B17, is), and comparing against it manufactured a 40% "shortfall". The test is
// therefore: SUM of category-2 bookings == SUM of rec.money, per country, inside the same pass.
inline void check_e2(const std::vector<livetrade::SimNode>& sim, std::ofstream& lg) {
    if (!booklog::g_installed) { lg << "[E2] not measured this run (pgt.BOOKLOG absent)" << (char)10; return; }
    std::map<int, double> paid;
    for (auto& s : sim)
        for (auto& rec : livetrade::read_standings(s.obj))
            if (rec.money != 0) paid[livetrade::country_index_of(rec.tag_index)] += rec.money;
    int checked = 0, agree = 0; double worst = 0; int worst_c = -1;
    for (auto& [c, m] : paid) {
        if (m <= 0) continue;
        auto it = booklog::g_sums.find(c);
        double booked = 0;
        if (it != booklog::g_sums.end()) { auto c2 = it->second.find(2); if (c2 != it->second.end()) booked = c2->second; }
        checked++;
        double d = booked - m; if (d < 0) d = -d;
        if (d <= 0.002) agree++;
        if (d > worst) { worst = d; worst_c = c; }
    }
    g_e2_checked = checked; g_e2_agree = agree; g_e2_worst = worst;
    lg << "[E2] engine booked (category 2) vs pass-10 rec.money: " << agree << "/" << checked
       << " countries agree to 0.002 ducats; worst |diff| " << worst << " (country #" << worst_c << ")" << (char)10;
    if (worst_c >= 0) booklog::report(worst_c, lg);
}

// E4: the visible face of conservation, checked on the engine's own fields.
inline void check_e4(const std::vector<livetrade::SimNode>& sim, std::ofstream& lg, int tick) {
    int neg_pool = 0, neg_out = 0, neg_link = 0, nan_ct = 0, huge = 0, neg_money = 0;
    // THE NUMBER THE PLAYER ACTUALLY SEES. The engine stores no total: the node window, the map
    // box and the tooltip each recompute local(+0xB4) + Sigma incoming(+0x10) - outgoing(+0xBC).
    // Checking only the stored fields let a negative TOTAL reach the map (baltic_sea, novgorod
    // in a per-good view) while this check still read CLEAN. Spec 1.12: no negative is ever
    // displayed, so the displayed quantity is what has to be measured.
    int neg_total = 0; double worst_total = 0; std::string worst_node;
    double worst_loc = 0, worst_in = 0, worst_out = 0;
    double world_pool = 0, world_local = 0, world_links = 0;
    for (auto& s : sim) {
        double pool = livetrade::fi(s.obj + 0xB0) / 1000.0;
        // LIVE reads. SimNode caches local/outgoing from read_sim_nodes(), which runs at the
        // TOP of the tick -- before install_aggregate writes them. Mixing those stale values
        // with freshly-written incoming records manufactures negatives that are not on screen.
        // E4's contract is the engine's own fields AFTER the mod has written them.
        double outg = livetrade::fi(s.obj + 0xBC) / 1000.0;
        double loc  = livetrade::fi(s.obj + 0xB4) / 1000.0;
        if (!std::isfinite(pool) || !std::isfinite(outg) || !std::isfinite(loc)) nan_ct++;
        if (pool < 0) neg_pool++;
        if (outg < 0) neg_out++;
        if (pool > 1e6 || loc > 1e6) huge++;
        world_pool += pool; world_local += loc;
        for (auto& l : livetrade::read_incoming(s.obj)) {
            double v = l.value_raw / 1000.0;
            if (v < 0) neg_link++;
            world_links += v;
        }
        for (auto& rec : livetrade::read_standings(s.obj))
            if (rec.money < 0) neg_money++;
        double in_sum = 0;
        for (auto& l : livetrade::read_incoming(s.obj)) in_sum += l.value_raw / 1000.0;
        double total = loc + in_sum - outg;
        if (total < -0.0005) {
            neg_total++;
            if (total < worst_total) {
                worst_total = total;
                // name it even when this sim copy was never named (check_e4 runs off pass 10's own
                // read, which does not carry names) -- an unnamed worst node made the 7 violations
                // of the 191-year run undiagnosable
                worst_node = s.name;
                if (worst_node.empty()) {
                    auto it = install::g_id_to_name.find(s.index);
                    worst_node = (it != install::g_id_to_name.end()) ? it->second
                                                                    : ("#" + std::to_string(s.index));
                }
                worst_loc = loc; worst_in = in_sum; worst_out = outg;   // the three terms, to diagnose
            }
        }
    }
    bool ok = !neg_pool && !neg_out && !neg_link && !nan_ct && !huge && !neg_money && !neg_total;
    lg << "[E4] tick " << tick << ": " << (ok ? "CLEAN" : "VIOLATION")
       << " -- negative pool=" << neg_pool << " outgoing=" << neg_out << " link=" << neg_link
       << " money=" << neg_money << " DISPLAYED-TOTAL=" << neg_total
       << (neg_total ? (" (worst " + worst_node + " total=" + std::to_string(worst_total)
                          + " local=" + std::to_string(worst_loc) + " incoming=" + std::to_string(worst_in)
                          + " outgoing=" + std::to_string(worst_out) + ")") : std::string())
       << ", non-finite=" << nan_ct << ", runaway=" << huge
       << " | world local=" << world_local << " pool=" << world_pool
       << " links=" << world_links << "\n";
}


// ---------------------------------------------------------------------------------------
// EXACT-TIMING E2. Sampling the accumulator from a worker thread ~400ms after the tick is not a
// measurement of E2 at all: a month boundary can fall between the two samples and reset what is
// being compared, which shows up as a spurious "shortfall". The comparison has to happen INSIDE
// the same monthly update, so pass 10 itself is wrapped.
//
//   0xB4BF44  call 0xB584F0     ; pass 10, once per node
//
// The wrapper counts calls; on the last node of the pass it samples every accumulator and
// compares the delta against what pass 10 actually paid. Same tick, no boundary in between.
inline uintptr_t g_mgr = 0;
inline std::string g_log_path;
inline bool g_exact = false;

using FnPass10 = void(__fastcall*)(uintptr_t);

inline bool g_suppress_pay = false;   // the attach-time setup run of the driver: no division, no AddDelayedIncome (reviewed)
inline void __fastcall pass10_wrapper(uintptr_t node) {
    if (g_suppress_pay) return;
    // BOTH samples inside pass 10. The 'before' sample used to come from the tick hook, which
    // is earlier in the same monthly update -- but measured, 70 of ~100 countries showed the
    // accumulator growing by LESS than trade paid (worst shortfall 4.0 ducats), which a plain
    // `add [country+0x68], eax` (AddDelayedIncome, 0x338AFC) cannot produce unless something
    // between the two samples reset +0x68. Sampling at pass 10's FIRST node closes every
    // such window: nothing but pass 10 runs between the samples.
    if (g_exact && g_pass10_seen == 0 && g_pass10_total > 0) {
        { LARGE_INTEGER t; QueryPerformanceCounter(&t); g_pass10_t0 = (unsigned long long)t.QuadPart; }
        auto sim0 = livetrade::read_sim_nodes();
        if (!sim0.empty()) sample_before(sim0);
        booklog::reset();
    }
    ((FnPass10)(livetrade::module_base() + 0xB584F0))(node);
    g_pass10_calls_total++;
    if (!g_exact) return;
    if (++g_pass10_seen < g_pass10_total || g_pass10_total <= 0) return;
    g_pass10_seen = 0;
    auto sim = livetrade::read_sim_nodes();
    if (sim.empty()) return;
    std::ofstream lg(g_log_path, std::ios::app);
    { LARGE_INTEGER t, f; QueryPerformanceCounter(&t); QueryPerformanceFrequency(&f);
      lg << "[pass10] " << g_pass10_total << " nodes in " << (1000.0 * (double)((unsigned long long)t.QuadPart - g_pass10_t0) / (double)f.QuadPart) << " ms" << (char)10; }
    check_e2(sim, lg);
    if (g_after_pass10) g_after_pass10(sim, lg);   // E1, E4: same pass, after every record is paid
}

inline bool install_exact(const std::string& logpath, std::string* err) {
    if (g_exact) return true;
    g_log_path = logpath;
    uintptr_t site = livetrade::module_base() + 0xB4BF44;
    if (!livetrade::validate_region(site, 5)) { if (err) *err = "pass-10 call site unreadable"; return false; }
    if (*(uint8_t*)site != 0xE8) { if (err) *err = "pass-10 site is not a rel32 call"; return false; }
    int32_t rel = *(int32_t*)(site + 1);
    if (site + 5 + rel != livetrade::module_base() + 0xB584F0) {
        if (err) *err = "pass-10 call does not reach 0xB584F0"; return false;
    }
    // thunk must be within rel32 range of the site (see OFFSETS.md's rel32 trap)
    uint8_t* thunk = nullptr;
    SYSTEM_INFO si{}; GetSystemInfo(&si);
    const uintptr_t gran = si.dwAllocationGranularity ? si.dwAllocationGranularity : 0x10000;
    for (int64_t d = (int64_t)gran; d < 0x60000000 && !thunk; d += gran)
        for (int dir = 0; dir < 2 && !thunk; dir++) {
            uintptr_t probe = (dir ? (site - (uintptr_t)d) : (site + (uintptr_t)d)) & ~(uintptr_t)(gran - 1);
            if (probe) thunk = (uint8_t*)VirtualAlloc((void*)probe, 32, MEM_COMMIT | MEM_RESERVE,
                                                      PAGE_EXECUTE_READWRITE);
        }
    if (!thunk) { if (err) *err = "pass-10 thunk alloc failed"; return false; }
    int64_t disp = (int64_t)((intptr_t)thunk - (intptr_t)(site + 5));
    if (disp < INT32_MIN || disp > INT32_MAX) { if (err) *err = "pass-10 thunk out of range"; return false; }
    uint8_t* p = thunk;
    *p++ = 0x48; *p++ = 0xB8;                    // mov rax, imm64
    uint64_t fn = (uint64_t)&pass10_wrapper;
    memcpy(p, &fn, 8); p += 8;
    *p++ = 0xFF; *p++ = 0xE0;                    // jmp rax
    DWORD old = 0;
    if (!VirtualProtect((void*)site, 5, PAGE_EXECUTE_READWRITE, &old)) {
        if (err) *err = "VirtualProtect failed"; return false;
    }
    *(int32_t*)(site + 1) = (int32_t)disp;
    VirtualProtect((void*)site, 5, old, &old);
    FlushInstructionCache(GetCurrentProcess(), (void*)site, 5);
    g_exact = true;
    return true;
}

} // namespace money
