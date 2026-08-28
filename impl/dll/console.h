// THE CONSOLE, DRIVEN FROM INSIDE THE PROCESS (spec 2.2 item 8; tests F2-F6, and the F1 re-run).
//
// Why not synthetic keystrokes: EU4 reads the keyboard through raw input, so only SendInput with
// KEYEVENTF_SCANCODE reaches it at all -- virtual-key injection is silently ignored, which is why
// every earlier attempt appeared to succeed and did nothing. Scancodes DO get text into the
// console field, but the path stays fragile: it needs the window foregrounded for every call, a
// focus change jogs the map camera, and a cursor parked near a screen edge scrolls the map out
// from under the test. None of that belongs in an acceptance suite.
//
// We are already inside the process, so we can call the console the way the game calls it. The
// engine's own path, at 0x758E1B:
//
//   00758E1B  call 0x6E74C0            ; the CConsoleCommandManager singleton  -> rax
//   00758E20  lea  r8, [rsp+0x30]      ; args: {begin,end,cap} of vector<std::string>
//   00758E25  lea  rdx, [rsp+0x48]     ; out: {bool ok; std::string message;}
//   00758E2A  mov  rcx, rax
//   00758E2D  call 0x1721320           ; Execute(mgr, &out, &args)
//
// argv[0] is the command name, argv[1..] its parameters -- the line is pre-split, so we tokenise
// on spaces ourselves rather than handing over a raw string.
//
// The strings must be MSVC std::string (this DLL is built with MinGW, whose layout differs):
//   +0x00 union { char sso[16]; char* ptr; }   +0x10 size   +0x18 capacity     (SSO while cap<16)
// Rather than open-code the SSO/heap split we initialise the header and let the engine's own
// assign do the work, so growth uses the engine's allocator:
//   0x95110  std::string::assign(this, const char* s, size_t n)
//   0x95660  std::string::~basic_string / _Tidy
//
// Commands MUST run on the game thread -- the dispatcher touches the same state the simulation
// does. drain() is therefore called from the monthly tick hook, never from the resolver thread.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>
#include "livetrade.h"

namespace console {

constexpr uintptr_t GET_MANAGER = 0x6E74C0;
constexpr uintptr_t EXECUTE     = 0x1721320;
constexpr uintptr_t STR_ASSIGN  = 0x95110;
constexpr uintptr_t STR_TIDY    = 0x95660;

using FnManager = uintptr_t (*)();
using FnExecute = void*     (*)(uintptr_t mgr, void* out, void* args);
using FnAssign  = void*     (*)(void* str, const char* s, size_t n);
using FnTidy    = void      (*)(void* str);

inline uint64_t g_ran = 0, g_failed = 0;

// one MSVC std::string, freshly constructed empty (SSO, capacity 15)
struct Str {
    alignas(8) uint8_t raw[0x20];
    void init() {
        memset(raw, 0, sizeof(raw));
        *(uint64_t*)(raw + 0x18) = 15;          // capacity -> SSO, size stays 0
    }
    void assign(const std::string& s) {
        ((FnAssign)(livetrade::module_base() + STR_ASSIGN))(raw, s.c_str(), s.size());
    }
    void tidy() { ((FnTidy)(livetrade::module_base() + STR_TIDY))(raw); }
    std::string read() const {
        uint64_t size = *(const uint64_t*)(raw + 0x10);
        uint64_t cap  = *(const uint64_t*)(raw + 0x18);
        const char* p = (cap < 16) ? (const char*)raw : *(const char* const*)raw;
        if (!p || size > (1u << 20)) return std::string();
        return std::string(p, (size_t)size);
    }
};

inline std::vector<std::string> split(const std::string& line) {
    std::vector<std::string> out;
    std::string cur;
    for (char c : line) {
        if (c == ' ' || c == '\t') { if (!cur.empty()) { out.push_back(cur); cur.clear(); } }
        else cur.push_back(c);
    }
    if (!cur.empty()) out.push_back(cur);
    return out;
}

// Run one console command line. Returns false only when the call could not be made at all;
// a command the engine rejects still returns true, with the engine's message in `reply`.
inline bool exec(const std::string& line, std::string* reply) {
    auto toks = split(line);
    if (toks.empty()) return false;
    uintptr_t base = livetrade::module_base();
    uintptr_t mgr = ((FnManager)(base + GET_MANAGER))();
    if (!mgr) return false;

    std::vector<Str> argv(toks.size());
    for (size_t i = 0; i < toks.size(); i++) { argv[i].init(); argv[i].assign(toks[i]); }

    // the engine takes {begin, end, capacity_end} by pointer, exactly as a vector lays out
    void* vec[3] = { argv.data(), argv.data() + argv.size(), argv.data() + argv.size() };

    alignas(8) uint8_t out[0x30];
    memset(out, 0, sizeof(out));                 // Execute overwrites out+8 wholesale

    ((FnExecute)(base + EXECUTE))(mgr, out, vec);

    bool ok = out[0] != 0;
    if (reply) *reply = ((Str*)(out + 8))->read();
    ((Str*)(out + 8))->tidy();
    for (auto& s : argv) s.tidy();
    g_ran++;
    if (!ok) g_failed++;
    return true;
}

// Drain `pgt.CMD`: every non-blank, non-# line is one console command. The file is DELETED once
// executed so a command fires exactly once, and the marker can simply be rewritten to fire again.
inline bool g_hold = false;   // set at attach: commands wait until the first tick has run (earlyload.h / ticklive.h)
inline unsigned long long g_hold_since = 0;
inline void set_hold(bool on) { g_hold = on; g_hold_since = on ? GetTickCount64() : 0; }
constexpr unsigned long long HOLD_DEADLINE_MS = 180000;  // covers the late path's world wait + install + solve; a hold nobody released is a bug, not a lock (reviewed)
inline void drain(const std::string& logpath) {
    if (g_hold && GetTickCount64() - g_hold_since < HOLD_DEADLINE_MS) return;   // the run's `speed` command must not move the world before the setup
    if (!livetrade::marker_present("CMD")) return;
    std::string path = livetrade::self_dir() + "\\pgt.CMD";
    std::vector<std::string> lines;
    {
        std::ifstream f(path);
        std::string l;
        while (std::getline(f, l)) {
            while (!l.empty() && (l.back() == '\n' || l.back() == '\r' || l.back() == ' ')) l.pop_back();
            if (!l.empty() && l[0] != '#') lines.push_back(l);
        }
    }
    DeleteFileA(path.c_str());                   // exactly once, even if a command throws
    if (lines.empty()) return;
    std::ofstream lg(logpath, std::ios::app);
    for (auto& l : lines) {
        std::string reply;
        bool called = exec(l, &reply);
        lg << "  [cmd] " << l << "  ->  " << (called ? (reply.empty() ? "(ok)" : reply)
                                                     : "CALL FAILED (no manager)") << "\n";
    }
    lg.flush();
}

} // namespace console
