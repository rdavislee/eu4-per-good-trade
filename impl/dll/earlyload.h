// THE MOD SETS UP INSIDE THE LOADING SCREEN (user rule, 2026-08-26): "the game needs to stop
// starting before the mod has warmed up".
//
// The engine's game-setup paths each make one trade call while the loading screen is still up:
//   0x773B20 "Initializing new game"   -> 0x774C3B  call 0xB4BA90  (the monthly trade driver)
//   0x7751B0 "Initializing savegame"   -> 0x775EEC  call 0xB4DB00  (the reachability rebuild)
// Both sites are repointed. The wrapper lets the engine's own call run (a new game has no trade
// values before its driver runs, and run_install waits for a world that carries value), then does
// the mod's whole install on the loading thread, solves the orientation synchronously, and runs
// the driver once more with income suppressed -- our tick hook inside it is tick 1: the graph is
// re-oriented, the opening re-placement happens, every write lands. Only then does the call return
// and the loading finish, so the map appears already set up. The DLL must be in the process before
// the campaign loads (the version.dll proxy, or the runner injecting at the main menu); injected
// after the load, the sites have passed and the frame-poll first tick (ticklive.h) is the fallback.
//
// The attach worker and this wrapper share one claim: whichever sees the world first installs; the
// other waits for it. The frame poll's own first tick is disarmed here, since this path does it.
#pragma once
#include <windows.h>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <string>
#include "detour.h"
#include "livetrade.h"
#include "resolver.h"
#include "money.h"
#include "console.h"
#include "ticklive.h"
#include "savegame.h"
#include "envoy.h"
#include "gates.h"

namespace earlyload {

constexpr uintptr_t DRIVER = 0xB4BA90;
constexpr uintptr_t REACH  = 0xB4DB00;
constexpr uintptr_t SITE_NEWGAME  = 0x774C3B;   // call 0xB4BA90 inside 0x773B20
constexpr uintptr_t SITE_SAVEGAME = 0x775EEC;   // call 0xB4DB00 inside 0x7751B0
constexpr uintptr_t INIT_NEWGAME  = 0x773B20, SITE_INIT_NEWGAME  = 0x81AC47;   // the single caller of InitNewGame
constexpr uintptr_t INIT_SAVEGAME = 0x7751B0, SITE_INIT_SAVEGAME = 0x5D00BC;   // the single caller of InitSaveGame

inline std::string g_log;
inline bool (*g_run_install)() = nullptr;        // dllmain's run_install, bound at attach; true when the plan is ready
inline uintptr_t g_node_base = 0;                 // the node array the install was built on (mgr+0x18): a new campaign reallocates it
constexpr uintptr_t SITE_OPENING_PLACE = 0x774E05; // call 0x3BAD90 inside 0x773B20: vanilla parks one merchant per country at its capital
constexpr uintptr_t SITE_OPENING_AUTO  = 0x774DB1; // call 0x3BAE50 inside the SAME loop: vanilla auto-places ALL idle merchants at trade
constexpr uintptr_t AUTO_PLACER = 0x3BAE50;        // nodes (measured: it re-placed the player's setup merchants as collectors at
                                                   // bordeaux/valencia through the arrival path -- the 16-frame chain named 0x774DB6)
constexpr uintptr_t PLACE_MERCHANT = 0x3BAD90;
inline std::atomic<int> g_opening_placements_skipped{0};
inline std::atomic<bool> g_claimed{false};       // the install has an owner (worker or wrapper)
inline std::atomic<bool> g_install_done{false};
inline std::atomic<int>  g_hits{0};
inline bool g_installed = false;

inline void note(const std::string& s) { std::ofstream f(g_log, std::ios::app); f << "[earlyload] " << s << (char)10; }
inline bool claim() { bool e = false; return g_claimed.compare_exchange_strong(e, true); }

inline bool g_resetup_no_driver = false;   // set while a resetup runs INSIDE the engine's driver: no nested driver runs
inline void finish_setup(uintptr_t mgr, const char* which) try {
    note(std::string(which) + ": the engine's setup call was reached with the world loading");
    uintptr_t node_base = livetrade::validate_region(mgr + 0x18, 8) ? livetrade::fq(mgr + 0x18) : 0;
    // a second hit of a setup site IS a second world (each setup function runs once per campaign load);
    // the node-array pointer is logged, not trusted -- the allocator can hand the same block back (reviewed)
    bool second_world = g_install_done.load();
    if (second_world) {
        note(std::string("a SECOND WORLD in this process (node array ") + (node_base == g_node_base ? "at the same address" : "moved") + "): resetting and re-installing");
        ticklive::reset_world_state();
        g_claimed = true;                            // this path owns the re-install; g_install_done stays TRUE (a third campaign is again a second world; reviewed)
    }
    ticklive::g_first_tick_done = true;              // this path does the first tick; the frame poll must not race it
    bool owner = second_world || claim();
    if (owner) {
        bool ok = g_run_install ? g_run_install() : false;
        if (!ok) { note("the install did not produce a ready plan: claim released; nothing acts until the next campaign load"); g_claimed = false; ticklive::g_first_tick_done = false; console::set_hold(false); return; }
        g_install_done = true;                       // success only: this is also the "second world" indicator (reviewed)
        ticklive::arm_world_identity(mgr);         // the world (node-array identity) this plan is armed for (reload detection)
        g_node_base = node_base;
    } else {
        note("the attach worker already owns the install; waiting for it");
        for (int i = 0; i < 6000 && !g_install_done.load(); i++) Sleep(20);   // up to two minutes
    }
    if (!ticklive::g_plan.ready) { note("plan not ready after the install: no first tick this campaign"); ticklive::g_first_tick_done = false; console::set_hold(false); return; }
    if (!money::g_exact) { note("pass-10 wrapper not installed: the setup driver run would pay a month -- skipped"); console::set_hold(false); return; }
    // the table before the first tick: a new game starts empty; a loaded save restores its sidecar,
    // and a save made without the mod (no sidecar) gets the opening rule once (savegame.h)
    if (std::string(which) == "new game") savegame::on_new_game();
    else if (savegame::restore_for_load()) assign::g_skip_startup_once = true;   // keep the saved targets: no opening re-placement
    resolver::Orientation o; std::string why;
    LARGE_INTEGER f{}, t0{}, t1{}; QueryPerformanceFrequency(&f); QueryPerformanceCounter(&t0);
    bool ok = resolver::solve_once(o, &why);
    QueryPerformanceCounter(&t1);
    if (!ok) { note("solve FAILED: " + why + " -- no first tick"); console::set_hold(false); return; }
    resolver::publish(o);
    note("orientation gen " + std::to_string(o.generation) + " solved in " + std::to_string((int)((t1.QuadPart - t0.QuadPart) * 1000 / (f.QuadPart ? f.QuadPart : 1))) + " ms; running the driver as tick 1 (income suppressed: the engine's own call just paid)");
    if (!g_resetup_no_driver) {                  // never nest the driver (a resetup from the tick hook)
        money::g_suppress_pay = true;
        ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + DRIVER))(mgr);
        money::g_suppress_pay = false;
    }
    console::set_hold(false);
    note("done: tick counter now " + std::to_string(ticklive::g_ticks.load()) + "; the loading may finish");
} catch (...) {
    note("C++ exception inside the loading-path setup: the engine continues without the first tick (faults are the crash logger's)");
    console::set_hold(false);
}

// both wrappers: the loading flag for the whole setup, the console hold re-armed for this campaign,
// and campaign 1's plan disarmed BEFORE the engine's own pre-wrapper driver runs (0x774C2F -> 0x75D690
// calls the driver unconditionally; a live tick hook would apply the old plan to the new world)
// The brackets sit on the INIT FUNCTIONS' own single call sites (0x81AC47 -> InitNewGame 0x773B20,
// 0x5D00BC -> InitSaveGame 0x7751B0), so they cover the engine's monthly updates BEFORE our site
// (0x774C2F) and AFTER it (0x774D33): the plan is disarmed before any pre-site driver run could apply
// campaign 1's plan to campaign 2's nodes, and the loading flag holds through the post-site tick
// (no capital recall, no player UI notify, while the UI may not exist) (reviewed).
inline void enter_setup() {
    ticklive::g_plan.ready = false;
    ticklive::g_world_cnt = 0;      // disarm the tick hook's campaign-change guard for the whole
    ticklive::g_world_nb = 0;       // load: the engine runs a monthly driver mid-build and our hook
    ticklive::g_world_fp = 0;       // sits inside it (reviewed). finish_setup re-arms on success.                  // first, unconditionally: a frame between these lines must not release the hold
    assign::g_in_loading = true;
    console::set_hold(true);
}
inline void leave_setup() { assign::g_in_loading = false; }
inline void __fastcall newgame_outer(uintptr_t game) {
    enter_setup();
    ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + INIT_NEWGAME))(game);
    leave_setup();
}
inline void __fastcall savegame_setup_after_init(uintptr_t mgr);   // defined below
inline void __fastcall savegame_outer(uintptr_t game) {
    enter_setup();
    ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + INIT_SAVEGAME))(game);
    savegame_setup_after_init(game + 0x2198);        // the world is complete only now (reviewed live)
    leave_setup();
}

inline void __fastcall newgame_wrapper(uintptr_t mgr) {
    g_hits++;
    ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + DRIVER))(mgr);   // the engine's own setup run: values exist after it
    finish_setup(mgr, "new game");
}
// The INNER savegame site (0x775EEC) fires TOO EARLY: it sits before the deserializer has restored
// the provinces and node values, so a setup run there sees an empty world and aborts (measured:
// "live trade state still empty after waiting" on a Continue Game load). It now only counts the
// hit; the setup runs from the OUTER wrapper, after InitSaveGame returns, world complete, loading
// screen still up.
inline void __fastcall savegame_wrapper(uintptr_t mgr) {
    g_hits++;
    ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + REACH))(mgr);    // the engine's own call at this site
    // AND REFILL. This site is one of the six calls to 0xB4DB00; because earlyload hooks it first,
    // gates::install cannot repoint it (it reports "5/6 ... MISSED 0x775EEC"), so the refill has to
    // happen here or the load path leaves matrix B holding the engine's own BFS. The old comment
    // here claimed "fill_b runs from the wrapper on the monthly path" -- true, but only from the
    // NEXT month, which is exactly the window spec 1.10 must not have.
    gates::fill_b(mgr, gates::FILL_REBUILD);
}
// RESETUP FROM INSIDE THE MONTHLY UPDATE (2026-08-27). The frame poll rides the map update and
// stops entirely at the menu -- and in a second campaign it never resumed, so a tick guard that
// merely "held ticks until the frame poll re-setups" deadlocked and the mod stayed silent (the ET
// 1241 -> 1776 bug). The tick hook can do the resetup itself, but it is ALREADY INSIDE the engine's
// driver (0xB4BF09), so both driver runs must be skipped: the values this tick just computed are
// exactly what run_install needs.
inline void __fastcall savegame_setup_after_init(uintptr_t mgr) {
    // a loaded save has not run the driver in this session: one suppressed run gives run_install a
    // world that carries value without waiting on the deserializer (reviewed)
    if (money::g_exact && !g_resetup_no_driver) { money::g_suppress_pay = true; ((void (__fastcall*)(uintptr_t))(livetrade::module_base() + DRIVER))(mgr); money::g_suppress_pay = false; }
    finish_setup(mgr, "savegame");
}

// An in-game load (exit to menu -> load, or load from the pause menu) reaches neither the
// 0x5D00BC outer site nor the inner 0x775EEC site -- a different loader builds the world. The
// frame poll detects the manager swap (ticklive::g_world_mgr) and calls this: the same setup the
// outer wrapper would have run, on the completed world.
inline void __fastcall resetup_inline(uintptr_t mgr) {
    enter_setup();
    savegame_setup_after_init(mgr);
    leave_setup();
}

// the same resetup, safe to call from INSIDE the engine's monthly driver (no nested driver runs)
inline void __fastcall resetup_in_tick(uintptr_t mgr) {
    g_resetup_no_driver = true;
    enter_setup();
    savegame_setup_after_init(mgr);
    leave_setup();
    g_resetup_no_driver = false;
}

// VANILLA'S OPENING PLACEMENT IS SKIPPED. After the setup driver calls, 0x773B20 loops the countries
// and parks one idle merchant per country at its trade capital (0x774DD0..0x774E05, PlaceMerchantAtNode
// with type 0) -- the source of the ~570 capital-parked collectors at 1444, and it runs AFTER the
// mod's loading-time tick, undoing D1 (reviewed). The call is repointed to this stub; the merchants
// stay in their pools until the model places them.
inline uint64_t __fastcall opening_place_stub(uintptr_t, uintptr_t, uint64_t, uintptr_t) { g_opening_placements_skipped++; return 0; }

inline uint8_t* thunk_to(uintptr_t site, void* fn) {
    uint8_t* th = detour::alloc_near(site, 32);
    if (!th) return nullptr;
    uint8_t* p = th;
    *p++ = 0x48; *p++ = 0xB8; uint64_t f = (uint64_t)fn; memcpy(p, &f, 8); p += 8;
    *p++ = 0xFF; *p++ = 0xE0;
    return th;
}

inline bool install(std::string* err) {
    if (g_installed) return true;
    ticklive::g_resetup_inline = &resetup_inline;    // the frame poll's in-session reload path
    ticklive::g_resetup_in_tick = &resetup_in_tick;  // the tick hook's own path (frame poll may never run)
    int done = 0; std::string e;
    { uintptr_t site = livetrade::module_base() + SITE_NEWGAME;  uint8_t* th = thunk_to(site, (void*)&newgame_wrapper);
      if (th && detour::repoint_call(site, livetrade::module_base() + DRIVER, th, &e)) done++; else if (err) *err = "new game: " + e; }
    { uintptr_t site = livetrade::module_base() + SITE_SAVEGAME; uint8_t* th = thunk_to(site, (void*)&savegame_wrapper);
      if (th && detour::repoint_call(site, livetrade::module_base() + REACH, th, &e)) done++; else if (err) *err = "savegame: " + e; }
    { uintptr_t site = livetrade::module_base() + SITE_OPENING_PLACE; uint8_t* th = thunk_to(site, (void*)&opening_place_stub);
      if (th && detour::repoint_call(site, livetrade::module_base() + PLACE_MERCHANT, th, &e)) done++; else if (err) *err = "opening placement: " + e; }
    { uintptr_t site = livetrade::module_base() + SITE_OPENING_AUTO; uint8_t* th = thunk_to(site, (void*)&opening_place_stub);
      if (th && detour::repoint_call(site, livetrade::module_base() + AUTO_PLACER, th, &e)) done++; else if (err) *err = "opening auto-placement: " + e; }
    { uintptr_t site = livetrade::module_base() + SITE_INIT_NEWGAME; uint8_t* th = thunk_to(site, (void*)&newgame_outer);
      if (th && detour::repoint_call(site, livetrade::module_base() + INIT_NEWGAME, th, &e)) done++; else if (err) *err = "InitNewGame site: " + e; }
    { uintptr_t site = livetrade::module_base() + SITE_INIT_SAVEGAME; uint8_t* th = thunk_to(site, (void*)&savegame_outer);
      if (th && detour::repoint_call(site, livetrade::module_base() + INIT_SAVEGAME, th, &e)) done++; else if (err) *err = "InitSaveGame site: " + e; }
    if (done != 6) {
        // a partial set must not stand: the outer brackets alone would disarm the plan on every load
        // with no finish_setup to re-arm it (reviewed). Revert what landed by restoring each call.
        struct Site { uintptr_t site, target; } all[6] = {
            { SITE_NEWGAME, DRIVER }, { SITE_SAVEGAME, REACH }, { SITE_OPENING_PLACE, PLACE_MERCHANT },
            { SITE_OPENING_AUTO, AUTO_PLACER },
            { SITE_INIT_NEWGAME, INIT_NEWGAME }, { SITE_INIT_SAVEGAME, INIT_SAVEGAME } };
        for (auto& x : all) {
            uintptr_t site = livetrade::module_base() + x.site;
            if (!livetrade::validate_region(site, 5) || *(uint8_t*)site != 0xE8) continue;
            int32_t rel = *(int32_t*)(site + 1);
            uintptr_t cur = site + 5 + rel;
            if (cur == livetrade::module_base() + x.target) continue;      // still the original
            int64_t disp = (int64_t)((intptr_t)(livetrade::module_base() + x.target) - (intptr_t)(site + 5));
            DWORD old = 0;
            if (VirtualProtect((void*)site, 5, PAGE_EXECUTE_READWRITE, &old)) {
                *(int32_t*)(site + 1) = (int32_t)disp;
                VirtualProtect((void*)site, 5, old, &old);
                FlushInstructionCache(GetCurrentProcess(), (void*)site, 5);
            }
        }
        if (err) *err += " (partial install REVERTED)";
        return false;
    }
    g_installed = true;
    return true;
}

} // namespace earlyload
