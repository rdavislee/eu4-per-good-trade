// THE REVERSE PANEL MUST NOT WEAR SOMEONE ELSE'S MERCHANTS (spec 1.7, 1.12).
//
// Observed in game: at north_sea, the reverse panels toward st_lawrence and white_sea both showed
// Norway's shield -- the same merchant the north_sea -> lubeck panel shows. The engine was
// claiming Norway steers to three places at once.
//
// The mechanism, read out of the flag builder 0x13FD7B0. It derives the link's ordinal by walking
// the SOURCE node's definition outgoing vector (def+0x98, stride 0x78) and comparing each
// entry+0x30 against [LinkView+0x80]->+0x30 (0x13FD83C..0x13FD899). The result register is
// zero-initialised at 0x13FD835 (`xor r12d,r12d`) and written ONLY on a match; the no-match path
// at 0x13FD894 jumps straight out, so a failed search yields ordinal 0 rather than "not found".
// The row then admits every record whose +0xA8 equals that ordinal (0x13FD9C1), i.e. everyone
// steering along the node's link #0.
//
// A reverse view fails that search by construction: it asks the target node's outgoing list for a
// link back to the source, and the graph is a DAG. So every reverse panel at a node collapses onto
// that node's link #0 and inherits its merchants. Worse, when the node has 0 or 1 outgoing links
// the ordinal test is skipped entirely (0x13FD9BC `cmp ecx,1; jle`) and EVERY steering country
// there is drawn.
//
// Vanilla panels never reach the default -- their entry really is in the outgoing list -- so this
// is purely an artefact of the injected views, and the correct behaviour for them is to show no
// engine-derived merchants at all. The engine cannot express a merchant steering along a link it
// has no index for; that is the whole reason assign::g_table exists (see assign.h).
//
// Interception: the panel's vtable is 0x1D823C0 and its per-frame Update is slot +0x10
// (0x13FCD80). Swapping that slot lets the original run -- so the value, the button state and the
// forward panels are all untouched -- and then clears the flag row on our panels only. Clearing
// after Update covers BOTH ways the row gets populated: the full rebuild at 0x13FD7B0 and the
// incremental diff inside Update (0x13FD238..0x13FD57E), which reuses shields and never calls the
// rebuild.
//
// The clear itself is the engine's own, copied from 0x13FD7D2..0x13FD7FF:
//     child = window->vtbl[0xE8](window, "director_flags")   // the name is a raw const char*
//     child->vtbl[0x278](child)                              // clear the container
#pragma once
#include <windows.h>
#include <cstdint>
#include <string>
#include "livetrade.h"
#include "revpanel.h"

namespace flagfix {

constexpr uintptr_t PANEL_VTABLE   = 0x1D823C0;
constexpr int       VT_UPDATE      = 0x10;      // per-frame Update
constexpr uintptr_t PANEL_UPDATE   = 0x13FCD80;
constexpr int       PANEL_WINDOW   = 0x08;      // GUI window, written by the ctor at 0x13FB8A5
constexpr int       PANEL_LINKVIEW = 0x38;      // zeroed by the ctor at 0x13FB97B
constexpr int       WIN_FIND_CHILD = 0xE8;      // window vtbl slot: (win, const char* name)
constexpr int       ELEM_CLEAR     = 0x278;     // element vtbl slot: (elem)

using FnUpdate = void (__fastcall*)(uintptr_t);
using FnFind   = uintptr_t (__fastcall*)(uintptr_t, const char*);
using FnClear  = void (__fastcall*)(uintptr_t);

inline FnUpdate g_orig = nullptr;
inline bool g_installed = false;
inline uint64_t g_cleared = 0;

inline void __fastcall update_hook(uintptr_t panel) {
    if (g_orig) g_orig(panel);                  // let the engine do everything it normally does
    if (!panel || !livetrade::validate_region(panel + PANEL_LINKVIEW, 8)) return;
    uintptr_t lv = livetrade::fq(panel + PANEL_LINKVIEW);
    if (!lv || !revpanel::is_reverse(lv)) return;       // forward panels are correct already
    uintptr_t win = livetrade::fq(panel + PANEL_WINDOW);
    if (!win || !livetrade::validate_region(win, 8)) return;
    uintptr_t wvt = livetrade::fq(win);
    if (!wvt || !livetrade::validate_region(wvt + WIN_FIND_CHILD, 8)) return;
    auto find = (FnFind)livetrade::fq(wvt + WIN_FIND_CHILD);
    if (!find) return;
    uintptr_t child = find(win, "director_flags");
    if (!child || !livetrade::validate_region(child, 8)) return;
    uintptr_t cvt = livetrade::fq(child);
    if (!cvt || !livetrade::validate_region(cvt + ELEM_CLEAR, 8)) return;
    auto clear = (FnClear)livetrade::fq(cvt + ELEM_CLEAR);
    if (!clear) return;
    clear(child);
    g_cleared++;
}

// Swap the vtable slot. Verified against the expected original first: on any other build the slot
// holds something else and we refuse rather than corrupt a vtable (spec 2.5).
inline bool install(std::string* err) {
    if (g_installed) return true;
    uintptr_t slot = livetrade::module_base() + PANEL_VTABLE + VT_UPDATE;
    if (!livetrade::validate_region(slot, 8)) { if (err) *err = "panel vtable unreadable"; return false; }
    uintptr_t cur = livetrade::fq(slot);
    if (cur != livetrade::module_base() + PANEL_UPDATE) {
        if (err) *err = "panel vtable slot +0x10 is not 0x13FCD80 (patched binary?)";
        return false;
    }
    g_orig = (FnUpdate)cur;
    DWORD old = 0;
    if (!VirtualProtect((void*)slot, 8, PAGE_READWRITE, &old)) {
        if (err) *err = "VirtualProtect on the panel vtable failed"; return false;
    }
    *(uintptr_t*)slot = (uintptr_t)&update_hook;
    VirtualProtect((void*)slot, 8, old, &old);
    FlushInstructionCache(GetCurrentProcess(), (void*)slot, 8);
    g_installed = true;
    return true;
}

} // namespace flagfix
