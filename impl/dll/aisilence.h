// VANILLA'S MERCHANT AI IS SILENCED; OURS IS THE ONLY ONE (spec 3.14; tests G1, G2).
//
// Measured with both running: of 347 nodes we placed a merchant at, 150 still held one a cadence
// later and 197 did not -- vanilla's merchant AI (1,020 moves per tick) recalled what we placed
// on its own schedule, and we re-dispatched ~180 per tick to put them back. A tug-of-war, not a
// placement model.
//
// Vanilla's merchant AI is 0x1BC1E0 -- the function holding the x1.5 hysteresis at 0x1BD206 and
// the merchant enumeration at 0x1BC2ED. It has exactly ONE caller, `call 0x1BC1E0` at 0x1B831D,
// whose result is discarded (the caller goes straight on to `call 0x1BA150` and returns; the
// function's own tail is `add rsp,0x20; pop rdi; ret`, no value). So the whole of vanilla's
// merchant decision-making is removed by turning that one call into five NOPs. Nothing else
// changes: envoy travel, recall, the record setters and the trade pass are all untouched.
//
// Pinned to the exact bytes; any other build is refused (spec 2.5).
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "livetrade.h"
#include "detour.h"

namespace aisilence {

constexpr uintptr_t CALL_SITE = 0x1B831D;   // call 0x1BC1E0, inside the per-country AI tick

inline bool g_installed = false;

inline bool install(std::string* err) {
    if (g_installed) return true;
    uintptr_t at = livetrade::module_base() + CALL_SITE;
    std::vector<uint8_t> expect = {0xE8, 0xBE, 0x3E, 0x00, 0x00};     // call +0x3EBE -> 0x1BC1E0
    std::vector<uint8_t> nops   = {0x90, 0x90, 0x90, 0x90, 0x90};
    if (!livetrade::validate_region(at, 5)) { if (err) *err = "call site unreadable"; return false; }
    if (!detour::patch_bytes(at, expect, nops, err)) return false;
    g_installed = true;
    return true;
}

} // namespace aisilence
