// NODE-WINDOW MERCHANT BUTTONS UNDER D1 (user rules, 2026-08-26): never "Collect from Trade" on any
// node, "Transfer Trade Power" at END nodes too, and NO button at the player's home node.
//
// The two buttons are not .gui elements: CTradeNodeView::RebuildEnvoyItems (0x13D6120) creates
// them as `envoy_item` rows of the `envoy_list` listbox (item ctor 0x13CA530, type 0 collect /
// 1 transfer / 2 recall), on window open (0x13CD642), after any send_merchant Execute (0x2743B4)
// and when the cached merchant state changes (0x13D0A15). Two paths:
//   A (no merchant of ours here):  collect item unconditionally (0x13D634D); transfer item unless
//                                  this is our home node (+0xAD, 0x13D6390) or def->end (0x13D63A0).
//   B (our merchant is here):      transfer item unless home or def->end (0x13D6273);
//                                  collect item (0x13D62A4..); recall item always (0x13D6317).
// `def+0xE5` is the definition's `end = yes` flag (the save writer emits it under token 0x1A0 "end"
// at 0xB695F3); it is read NOWHERE else in the image -- a pure UI gate. Nothing in the click path
// (0x13CB560 -> 0x13D6570 -> Execute 0x274180 -> SetTrader 0xB596E0) refuses a transfer at an END
// node; SetTrader's own zero-link case writes +0xA8 = 0, which nocollect.h/syncrec.h already carry.
//
// Four two-byte patches, verified byte-exact against 835bfdf8:
//   0x13D627A  75 28 -> 90 90   path B: ignore def->end
//   0x13D63A7  75 31 -> 90 90   path A: ignore def->end
//   0x13D62A4  48 8D -> EB 71   path B: skip the collect item, land on the recall item (0x13D6317)
//   0x13D634D  48 8B -> EB 2C   path A: skip the collect item, land on the transfer gate (0x13D637B)
// Result: no merchant -> Transfer only (home: nothing, the +0xAD gate stands); our merchant here ->
// Recall (plus Transfer while it is still collecting: 0xB58E00 true routes through the transfer item
// first). Both patch addresses are branch targets themselves; neither second byte is one. Callers of
// 0x13D6120: 0x13CD642, 0x13D0A15, 0x2743B4, 0x2749CD.
#pragma once
#include <windows.h>
#include <cstdint>
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"

namespace envoybuttons {

struct Patch { uintptr_t rva; std::vector<uint8_t> expect, write; const char* what; };
// ORDER: the two jumps (no collect item) land first, the two NOPs (transfer at END nodes) second, so
// every intermediate state the render thread could see is a strict subset of the final one -- never
// a collect item at an END node (reviewed)
inline const Patch PATCHES[4] = {
    { 0x13D62A4, {0x48, 0x8D}, {0xEB, 0x71}, "path B: no collect item (jump to the recall item)" },
    { 0x13D634D, {0x48, 0x8B}, {0xEB, 0x2C}, "path A: no collect item (jump to the transfer gate)" },
    { 0x13D627A, {0x75, 0x28}, {0x90, 0x90}, "path B: transfer item ignores def->end" },
    { 0x13D63A7, {0x75, 0x31}, {0x90, 0x90}, "path A: transfer item ignores def->end" },
};
inline int g_rollback_failed = 0;
inline bool g_installed = false;

// all four or none: a half-applied set would build a list the engine never builds
inline bool install(std::string* err) {
    if (g_installed) return true;
    for (auto& p : PATCHES) {
        uintptr_t at = livetrade::module_base() + p.rva;
        if (!livetrade::validate_region(at, 4) || memcmp((void*)at, p.expect.data(), p.expect.size()) != 0) {
            if (err) *err = std::string("unexpected bytes at ") + p.what; return false;
        }
    }
    int done = 0;
    for (auto& p : PATCHES) {
        std::string e;
        if (detour::patch_bytes(livetrade::module_base() + p.rva, p.expect, p.write, &e)) done++;
        else { if (err) *err = std::string(p.what) + ": " + e; break; }
    }
    if (done != 4) {   // roll back whatever landed (expected = what is there now, replacement = the original)
        for (int i = 0; i < done; i++) {
            bool ok = false;
            for (int attempt = 0; attempt < 5 && !ok; attempt++)
                ok = detour::patch_bytes(livetrade::module_base() + PATCHES[i].rva, PATCHES[i].write, PATCHES[i].expect, nullptr);
            if (!ok) { g_rollback_failed++; if (err) *err += std::string(" | ROLLBACK FAILED: ") + PATCHES[i].what; }
        }
        return false;
    }
    g_installed = true;
    return true;
}

} // namespace envoybuttons
