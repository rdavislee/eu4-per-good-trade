// WHAT PASS 10 ACTUALLY BOOKS (test E2's premise, measured rather than assumed).
//
// E2 compares each country's accumulator delta (country+0x68) against the sum of its records'
// rec.money. Measured: Ming's three records carry money = 5.36 + 2.98 + 1.31 = 9.65 and its
// accumulator moved 0.25. The disassembly of pass 10 (0xB584F0) shows why that comparison may be
// the wrong premise, not a booking bug:
//
//   0xB58526  mov r13,[rcx+0x18]        ; r13 = the node's FIRST record, loaded once
//   0xB586DD  mov [r13+0x34],edx        ; rec.money written per record inside the loop
//   0xB587E6  call 0x338A90             ; category 0xC, amount = money x share / 1000, PER RECORD
//   0xB5895E  call 0x338A90             ; category 2 (trade), amount = [r13+0x34] -- record[0] ONLY
//
// So category 2 is booked once per node for record[0], and every other collector's money is
// booked (if at all) through the category-0xC path. Which path carries a collector's real trade
// income, and whether +0x68 is the right aggregate, is settled here by logging every call.
//
// Both call sites are 5-byte rel32 calls redirected to a thunk that forwards to a wrapper with the
// category and amount; the wrapper calls the original and records (country index, category,
// amount) into per-month sums. The thunk lives within rel32 range of the site (OFFSETS.md's rel32
// trap). Nothing about the engine's bookkeeping is changed; this only observes it.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <map>
#include <string>
#include "livetrade.h"

namespace booklog {

constexpr uintptr_t ADD_DELAYED_INCOME = 0x338A90;
constexpr uintptr_t SITE_CAT_C  = 0xB587E6;    // per-record, category 0xC
constexpr uintptr_t SITE_CAT_2  = 0xB5895E;    // per-node record[0], category 2

using FnAdd = void (__fastcall*)(uintptr_t country, int category, int32_t* amount);

// per month: country index -> category -> sum (ducats)
inline std::map<int, std::map<int, double>> g_sums;
inline std::map<int, int> g_calls;
inline bool g_installed = false;

inline void __fastcall wrapper(uintptr_t country, int category, int32_t* amount) {
    int32_t v = amount ? *amount : 0;
    ((FnAdd)(livetrade::module_base() + ADD_DELAYED_INCOME))(country, category, amount);
    // country index from the handle at country+0x20 (bytes 4..5), the engine's own idiom
    if (country && livetrade::validate_region(country + 0x20, 8)) {
        int idx = (int)(int16_t)(livetrade::fq(country + 0x20) >> 32);
        g_sums[idx][category] += v / 1000.0;
        g_calls[category]++;
    }
}

inline void reset() { g_sums.clear(); g_calls.clear(); }

// dump one country's bookings this month, and the category call counts
inline void report(int country_idx, std::ofstream& lg) {
    lg << "[booklog] calls by category:";
    for (auto& [cat, n] : g_calls) lg << " cat" << cat << "=" << n;
    lg << (char)10;
    auto it = g_sums.find(country_idx);
    if (it == g_sums.end()) { lg << "[booklog] country#" << country_idx << ": no bookings" << (char)10; return; }
    lg << "[booklog] country#" << country_idx << " booked this month:";
    double tot = 0;
    for (auto& [cat, v] : it->second) { lg << " cat" << cat << "=" << v; tot += v; }
    lg << "  total=" << tot << (char)10;
}

inline bool redirect(uintptr_t site_rva, std::string* err) {
    uintptr_t site = livetrade::module_base() + site_rva;
    if (!livetrade::validate_region(site, 5) || *(uint8_t*)site != 0xE8) { if (err) *err = "site is not a rel32 call"; return false; }
    int32_t rel = *(int32_t*)(site + 1);
    if (site + 5 + rel != livetrade::module_base() + ADD_DELAYED_INCOME) { if (err) *err = "site does not call 0x338A90"; return false; }
    uint8_t* thunk = nullptr;
    SYSTEM_INFO si{}; GetSystemInfo(&si);
    const uintptr_t gran = si.dwAllocationGranularity ? si.dwAllocationGranularity : 0x10000;
    for (int64_t d = (int64_t)gran; d < 0x60000000 && !thunk; d += gran)
        for (int dir = 0; dir < 2 && !thunk; dir++) {
            uintptr_t probe = (dir ? (site - (uintptr_t)d) : (site + (uintptr_t)d)) & ~(uintptr_t)(gran - 1);
            if (probe) thunk = (uint8_t*)VirtualAlloc((void*)probe, 32, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
        }
    if (!thunk) { if (err) *err = "thunk alloc failed"; return false; }
    int64_t disp = (int64_t)((intptr_t)thunk - (intptr_t)(site + 5));
    if (disp < INT32_MIN || disp > INT32_MAX) { if (err) *err = "thunk out of rel32 range"; return false; }
    uint8_t* p = thunk;
    *p++ = 0x48; *p++ = 0xB8; uint64_t fn = (uint64_t)&wrapper; memcpy(p, &fn, 8); p += 8;   // mov rax, wrapper
    *p++ = 0xFF; *p++ = 0xE0;                                                                   // jmp rax
    DWORD old = 0;
    if (!VirtualProtect((void*)site, 5, PAGE_EXECUTE_READWRITE, &old)) { if (err) *err = "VirtualProtect failed"; return false; }
    *(int32_t*)(site + 1) = (int32_t)disp;
    VirtualProtect((void*)site, 5, old, &old);
    FlushInstructionCache(GetCurrentProcess(), (void*)site, 5);
    return true;
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    if (!redirect(SITE_CAT_C, err)) return false;
    if (!redirect(SITE_CAT_2, err)) return false;
    g_installed = true;
    return true;
}

} // namespace booklog
