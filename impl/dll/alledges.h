// EVERY INCIDENT EDGE, SHOWN AS AN OUTGOING PANEL (spec 1.7, 1.12; tests B3, C1-C5).
//
// Vanilla splits a node's links into two listboxes by the INSTALLED orientation: incoming on the
// left, outgoing on the right. Only the outgoing group carries a usable steer target, because
// `steer_command` writes an INDEX into the node's own outgoing list -- a link drawn INTO the node
// has no index there to name. Under the per-good model that is the wrong split: the per-good
// graphs disagree with Phi_w on ~45% of edge-goods (spec 1.6), so a link drawn INTO a node very
// often still carries goods AWAY from it, and that end must be both visible and assignable.
//
// The node window populate is CTradeNodeView::Populate at 0x13D5560. It:
//   * finds `incoming_nodes_listbox` / `outgoing_nodes_listbox` via [window+0xA0] -> vtable+0xE8,
//   * CLEARS each (vtable+0x278) -- which is what makes appending after it idempotent,
//   * walks the definition's incoming (def+0x80..0x88) and outgoing (def+0x98..0xA0) lists, and
//     for each entry allocates 0x150 bytes, constructs a TradeNodeLink at 0x13CC740(obj, owner,
//     farNode, "TradeNodeLink") and appends it with listbox_vtable+0x260 (child, true).
//
// So we let the engine populate, then append one MORE TradeNodeLink to the OUTGOING listbox for
// every link the engine filed as incoming. The definition graph is untouched -- deliberately:
// putting both u->v and v->u into it would make the engine's calc-order rebuild (a recursive DFS
// at 0xB67D20) walk a cycle and blow the stack, which is the same failure a cyclic
// 00_tradenodes.txt causes. The sim graph stays the acyclic Phi_w; only the VIEW shows both ends.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>
#include "detour.h"
#include "livetrade.h"
#include "console.h"

namespace alledges {

// 0x13D5560 is Populate, but it runs ONCE -- from the window CONSTRUCTOR (0x13CD010 zeroes
// +0xF8 there), with no node attached. The per-open REFRESH is its caller, 0x13CD560, which
// is invoked from three places including 0x831869 -- the node-click path, right beside the
// assignment gate clickgate.h already patches at 0x8317EF.
constexpr uintptr_t REFRESH = 0x13CD560;
inline const uintptr_t REFRESH_CALLS[3] = { 0x80ED1B, 0x831869, 0x13D1D5C };
constexpr uintptr_t LINK_CTOR  = 0x13CC740;   // TradeNodeLink(obj, owner, farNode, &name)
constexpr uintptr_t ENGINE_NEW = 0x1A332D4;   // operator new(size)
constexpr int  LINK_SIZE       = 0x150;
constexpr int  WIN_CONTAINER   = 0xA0;        // window -> GUI container
constexpr int  WIN_NODE        = 0xF8;        // window -> CTradeNode being shown
constexpr int  WIN_OWNER       = 0x280;       // window -> the owner passed to the link ctor
constexpr int  VT_FIND_CHILD   = 0xE8;        // container vtable: FindChild(name) -> widget
constexpr int  VT_ADD_CHILD    = 0x260;       // listbox vtable: AddChild(child, bool)
constexpr int  DEF_IN_BEGIN    = 0x80, DEF_IN_END = 0x88;
constexpr int  ENTRY_TARGET    = 0x30;        // link entry -> target definition
constexpr int  ENTRY_STRIDE    = 0x78;
constexpr int  DEF_PROVINCE    = 0xDC;        // definition -> its province id

inline bool g_active = false;
inline uint64_t g_appended = 0, g_calls = 0;
inline std::string g_log;
inline int g_logged = 0;
inline uintptr_t g_last_window = 0;   // captured so the DLL can drive the window itself

// The console's "window open <name>" stores the window it opened in a global:
//   00E58707  call [rax+0x48]                    ; open by GUI name
//   00E5870A  mov  [rip -> 0x2458F58], rax       ; the opened window
// so the DLL can pick the TradeNodeInterface up from there without any map click.
constexpr uintptr_t LAST_OPENED_WINDOW = 0x2458F58;

using FnRefresh   = void*  (__fastcall*)(uintptr_t);
using FnNew       = void*  (__fastcall*)(size_t);
using FnLinkCtor  = void*  (__fastcall*)(void*, void*, void*, void*);
using FnFindChild = void*  (__fastcall*)(void*, void*);
using FnAddChild  = void*  (__fastcall*)(void*, void*, bool);

// definition -> its CTradeNode, the way 0xB56480 resolves it
inline uintptr_t node_of_def(uintptr_t def) {
    if (!def || !livetrade::validate_region(def + DEF_PROVINCE, 4)) return 0;
    int pid = livetrade::fi(def + DEF_PROVINCE);
    uintptr_t g = livetrade::game_singleton();
    if (!g || pid < 0) return 0;
    uintptr_t provs = livetrade::rq(g + 0x1CA8);
    if (!provs) return 0;
    uintptr_t prov = provs + (uintptr_t)pid * 0x2E10;
    if (!livetrade::validate_region(prov + 0xE8, 8)) return 0;
    return livetrade::fq(prov + 0xE8);
}

// The engine passes a RAW const char* here, not a std::string:
//   013D558C  mov rcx, [rcx+0xA0]                     ; the window's GUI container
//   013D5593  mov rax, [rcx]                          ; its vtable
//   013D5596  lea rdx, [rip -> "incoming_nodes_listbox"]   <-- .rdata char array
//   013D559D  call [rax+0xE8]
// Handing it an MSVC std::string instead is why every lookup came back NOT FOUND.
inline void* find_child(uintptr_t window, const char* name) {
    if (!livetrade::validate_region(window + WIN_CONTAINER, 8)) return nullptr;
    uintptr_t cont = livetrade::fq(window + WIN_CONTAINER);
    if (!cont || !livetrade::validate_region(cont, 8)) return nullptr;
    uintptr_t vt = livetrade::fq(cont);
    if (!vt || !livetrade::validate_region(vt + VT_FIND_CHILD, 8)) return nullptr;
    auto fn = (FnFindChild)livetrade::fq(vt + VT_FIND_CHILD);
    return fn((void*)cont, (void*)name);
}

// Append one TradeNodeLink for `far` to `listbox`, exactly as the engine builds its own.
inline bool append_link(uintptr_t window, void* listbox, uintptr_t far_node) {
    if (!listbox || !far_node) return false;
    auto alloc = (FnNew)(livetrade::module_base() + ENGINE_NEW);
    void* obj = alloc(LINK_SIZE);
    if (!obj) return false;
    console::Str nm; nm.init(); nm.assign("TradeNodeLink");
    auto ctor = (FnLinkCtor)(livetrade::module_base() + LINK_CTOR);
    void* owner = (void*)livetrade::fq(window + WIN_OWNER);
    ctor(obj, owner, (void*)far_node, nm.raw);
    nm.tidy();
    uintptr_t lvt = livetrade::fq((uintptr_t)listbox);
    if (!lvt || !livetrade::validate_region(lvt + VT_ADD_CHILD, 8)) return false;
    auto add = (FnAddChild)livetrade::fq(lvt + VT_ADD_CHILD);
    add(listbox, obj, true);
    g_appended++;
    return true;
}

inline void __fastcall populate_wrapper(uintptr_t window) {
    ((FnRefresh)(livetrade::module_base() + REFRESH))(window);        // let vanilla fill both
    if (!g_active || !window) return;
    g_calls++;
    g_last_window = window;
    {
        uintptr_t nd0 = livetrade::validate_region(window + WIN_NODE, 8)
                            ? livetrade::fq(window + WIN_NODE) : 0;
        if (g_logged < 14 && !g_log.empty()) {
            g_logged++;
            std::ofstream lg(g_log, std::ios::app);
            lg << "  [alledges] call #" << g_calls << " window=0x" << std::hex << window
               << " node=0x" << nd0 << std::dec << "\n";;
        }
    }
    if (!livetrade::validate_region(window + WIN_NODE, 8)) return;
    uintptr_t node = livetrade::fq(window + WIN_NODE);
    if (!node || !livetrade::validate_region(node + 0xA8, 8)) return;
    uintptr_t def = livetrade::fq(node + 0xA8);
    if (!def || !livetrade::validate_region(def + DEF_IN_BEGIN, 16)) return;
    uintptr_t b = livetrade::fq(def + DEF_IN_BEGIN), e = livetrade::fq(def + DEF_IN_END);
    // The INCOMING list is an array of DEFINITION POINTERS (8 bytes each), not 0x78-byte link
    // entries like the outgoing list. The populate divides its span by 8 and indexes [rax+r14*8],
    // then reads element+0xD8 as a node index. Walking it with the outgoing stride made every
    // node report "incoming-defs=0" and append nothing.
    if (!b || e <= b || (e - b) > 8 * 64) return;
    void* out_lb = find_child(window, "outgoing_nodes_listbox");
    int n_in = (int)((e - b) / 8), added = 0;
    if (out_lb) {
        for (uintptr_t p = b; p + 8 <= e; p += 8) {
            if (!livetrade::validate_region(p, 8)) continue;
            uintptr_t src_def = livetrade::fq(p);
            uintptr_t far_node = node_of_def(src_def);
            if (far_node && far_node != node && append_link(window, out_lb, far_node)) added++;
        }
    }
    if (g_logged < 12 && !g_log.empty()) {
        g_logged++;
        std::ofstream lg(g_log, std::ios::app);
        lg << "  [alledges] populate #" << g_calls << ": incoming-defs=" << n_in
           << " outgoing_listbox=" << (out_lb ? "found" : "NOT FOUND")
           << " appended=" << added << "\n";;
    }
}

inline uint8_t* g_thunk = nullptr;
inline bool g_installed = false;


// Open a node's window WITHOUT clicking the map. The console can open the window
// ("window open TradeNodeInterface") but that does not attach a node, so nothing refreshes.
// Setting +0xF8 and calling the refresh ourselves is the same thing the click path does, and it
// makes the node window scriptable -- which is what B3 and the C tests need to be checkable at
// all, since synthetic clicks on a map icon are not reliable.
// The CTradeNodeView is NOT the GUI window the console's "window open" hands back -- it is a C++
// object hanging off the game singleton. The node-click path shows it plainly:
//   0083174A  mov rcx, [rip -> 0233FE78]      ; the game singleton, passed as arg 1
//   00831853  mov rcx, [rdi + 0x1228]         ; -> the CTradeNodeView
//   0083185D  call 0x13D12E0                  ; ShowNode(view, node)  -- sets +0xF8 and refreshes
constexpr int  VIEW_IN_GAME = 0x1228;
constexpr uintptr_t SHOW_NODE = 0x13D12E0;
using FnShowNode = void (__fastcall*)(uintptr_t, uintptr_t);

inline uintptr_t view_ptr() {
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + VIEW_IN_GAME, 8)) return 0;
    uintptr_t v = livetrade::fq(g + VIEW_IN_GAME);
    return (v && livetrade::validate_region(v + WIN_NODE, 8)) ? v : 0;
}

// Show a node in the node window using the engine's OWN entry point, so everything it normally
// does still happens -- and our refresh hook fires, appending the reverse-end panels.
inline bool open_node(uintptr_t node, std::string* err) {
    uintptr_t view = view_ptr();
    if (!view) { if (err) *err = "CTradeNodeView not reachable at G+0x1228"; return false; }
    if (!node) { if (err) *err = "node not found"; return false; }
    ((FnShowNode)(livetrade::module_base() + SHOW_NODE))(view, node);
    return true;
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    int done = 0;
    for (uintptr_t rva : REFRESH_CALLS) {
        uintptr_t site = livetrade::module_base() + rva;
        uint8_t* th = detour::alloc_near(site, 32);
        if (!th) continue;
        uint8_t* p = th;
        *p++ = 0x48; *p++ = 0xB8;                   // mov rax, imm64
        uint64_t fn = (uint64_t)&populate_wrapper;
        memcpy(p, &fn, 8); p += 8;
        *p++ = 0xFF; *p++ = 0xE0;                   // jmp rax
        std::string e1;
        if (detour::repoint_call(site, livetrade::module_base() + REFRESH, th, &e1)) done++;
        else if (err) *err = e1;
    }
    if (!done) { if (err && err->empty()) *err = "no refresh call site could be redirected"; return false; }
    g_installed = true;
    g_active = true;
    return true;
}

} // namespace alledges
