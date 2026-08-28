// OPEN THE NODE-WINDOW CLICK GATE (spec 1.7, 1.10; test C1).
//
// Spec 1.7: an incoming link entry "must accept a merchant assignment rather than merely
// navigate". Probe 14 established that today it only navigates. The RE then found that the click
// ALREADY reaches the merchant-assignment dispatcher -- so this is a gate to open, not a
// mechanism to build:
//
//   0x13CCE80  link entry clicked (same handler for both lists)
//   0x831790   dispatcher; if a merchant is in placement mode:
//     0x8317E7    edi = node index
//     0x8317EF    call 0x1418E70      ; CanAssignHere(nodeIdx) -> al
//     0x8317F4    test al, al
//     0x8317F6    je 0x8318BA         ; refused -> falls through to plain navigation
//     0x831814    jmp 0x1419470       ; AssignHere(nodeIdx)
//
// The gate's only graph-shaped test is 0xB69FC0, which is the upstream/downstream predicate --
// and spec 1.10 is explicit that "any mechanism gated on one nation being upstream or downstream
// of another evaluates TRUE", and that this is done "at the call site rather than by forcing any
// shared predicate". So the patch is exactly that: at this one call site, produce true.
//
//   0x8317EF  e8 7c 76 be 00   call 0x1418E70
//        ->   b0 01 90 90 90   mov al,1 ; nop ; nop ; nop
//
// `test al,al` is deliberately left in place so it sets the flags the following `je` reads --
// replacing the test as well would leave `je` reading stale flags.
#pragma once
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"

namespace clickgate {

constexpr uintptr_t GATE_CALL = 0x8317EF;

inline bool g_open = false;

inline bool open_gate(std::string* err) {
    if (g_open) return true;   // a second campaign re-runs the install (reviewed)
    uintptr_t at = livetrade::module_base() + GATE_CALL;
    std::vector<uint8_t> expected{0xE8, 0x7C, 0x76, 0xBE, 0x00};       // call 0x1418E70
    std::vector<uint8_t> patched {0xB0, 0x01, 0x90, 0x90, 0x90};       // mov al,1 ; nop*3
    if (!detour::patch_bytes(at, expected, patched, err)) return false;
    g_open = true;
    return true;
}

inline bool close_gate(std::string* err) {
    uintptr_t at = livetrade::module_base() + GATE_CALL;
    std::vector<uint8_t> patched {0xB0, 0x01, 0x90, 0x90, 0x90};
    std::vector<uint8_t> original{0xE8, 0x7C, 0x76, 0xBE, 0x00};
    if (!detour::patch_bytes(at, patched, original, err)) return false;
    g_open = false;
    return true;
}

} // namespace clickgate
