// SIDECAR PERSISTENCE OF THE ASSIGNMENT TABLE (user, 2026-08-26: "will this save state for opening a
// save that was already running?").
//
// The engine's save keeps the records, and a reverse-end merchant is stored there as "transfer,
// link 0" -- the table (assign.h) that names the real target is memory-only. So it is written next
// to every save and read back on load:
//   SAVE: every save (manual, quick, auto, exit) funnels through eu4savegamehelper's two writers
//         (0x5C6500 / 0x5C7AC0), which write <path>.tmp and then rename it with
//         0x1715BB0(const char* src, const char* dst) -> bool. That function has other callers (the
//         backup rotation renames .eu4 -> bak, unrelated file moves), so the prologue hook acts only
//         when src ends ".tmp" and dst ends ".eu4": it writes <dst>.pgt and remembers the directory.
//   LOAD: the loader assigns G+0x2430 = "<name>.eu4" (0x5D00AA) and then calls InitSaveGame
//         0x7751B0, inside which our loading-path wrapper (earlyload.h, at 0x775EEC) runs the
//         install and the first tick; restore_for_load() is called there, before that tick, so the
//         routing honours the restored targets from the first month. No sidecar -> a save made
//         without the mod: the opening rule (envoy.h startup) runs once instead.
//   NEW GAME: InitNewGame 0x773B20 -> the table is cleared before the first tick.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <map>
#include <mutex>
#include <vector>
#include <fstream>
#include <string>
#include "detour.h"
#include "livetrade.h"
#include "assign.h"

namespace savegame {

constexpr uintptr_t RENAME_FN = 0x1715BB0;      // bool (const char* src, const char* dst)
inline const uintptr_t RENAME_SITES[2] = { 0x5C7888, 0x5C88EF };   // the two save writers' ".tmp -> .eu4" renames (0x5C6500 / 0x5C7AC0)
constexpr int GAME_SAVE_NAME = 0x2430;           // CGame: narrow std::string "<name>.eu4" of the loaded/saved game

inline bool g_installed = false;
inline std::string g_log;
inline std::string g_last_dir;                   // directory of the last save written (sidecars live beside the .eu4)
inline int g_written = 0, g_restored = 0, g_restore_missing = 0, g_cleared = 0, g_renames_seen = 0;

inline void note(const std::string& s) { if (!g_log.empty()) { std::ofstream f(g_log, std::ios::app); f << "[savegame] " << s << (char)10; } }

inline bool ends_with(const std::string& s, const char* suf) {
    size_t n = strlen(suf); if (s.size() < n) return false;
    return _stricmp(s.c_str() + s.size() - n, suf) == 0;
}
inline std::string cstr_at(uintptr_t p) {
    if (!p || !livetrade::validate_region(p, 1)) return std::string();
    std::string out; for (int i = 0; i < 1024; i++) { if (!livetrade::validate_region(p + i, 1)) break; char c = *(const char*)(p + i); if (!c) break; out.push_back(c); }
    return out;
}

inline std::string resolve_save_path(const std::string& p);   // defined below (needs documents_save_dir)

// the wrapper on the two save-writer rename sites: the original runs first; on success the sidecar
// is written beside the .eu4 (the suffix test is belt-and-braces: these sites rename only saves)
using FnRename = uint64_t (__fastcall*)(uintptr_t, uintptr_t);
inline uint64_t __fastcall rename_wrapper(uintptr_t src_p, uintptr_t dst_p) {
    uint64_t ret = ((FnRename)(livetrade::module_base() + RENAME_FN))(src_p, dst_p);
    g_renames_seen++;
    std::string src = cstr_at(src_p), dst = cstr_at(dst_p);
    if ((ret & 0xFF) == 0 || !ends_with(src, ".tmp") || !ends_with(dst, ".eu4")) return ret;
    if (g_written == 0) note("save rename seen on thread " + std::to_string(GetCurrentThreadId()));   // which thread saves (reviewed)
    std::string side = resolve_save_path(dst) + ".pgt";
    if (assign::write_file(side)) {
        g_written++;
        std::string rdst = resolve_save_path(dst);
        size_t sl = rdst.find_last_of("\\/");
        if (sl != std::string::npos) g_last_dir = rdst.substr(0, sl + 1);
        note("wrote " + side + " (" + std::to_string(assign::g_table.size()) + " entries)");
    } else note("could NOT write " + side);
    return ret;
}

// the MSVC std::string at G+0x2430: buf/ptr@0, size@0x10, cap@0x18
inline std::string loaded_save_name() {
    uintptr_t g = livetrade::game_singleton();
    if (!g || !livetrade::validate_region(g + GAME_SAVE_NAME, 0x20)) return std::string();
    uint64_t sz = *(uint64_t*)(g + GAME_SAVE_NAME + 0x10), cap = *(uint64_t*)(g + GAME_SAVE_NAME + 0x18);
    if (sz == 0 || sz > 260 || cap < sz) return std::string();
    const char* p = (const char*)(g + GAME_SAVE_NAME);
    if (cap >= 16) { uintptr_t hp = *(uintptr_t*)(g + GAME_SAVE_NAME); if (!hp || !livetrade::validate_region(hp, sz + 1)) return std::string(); p = (const char*)hp; }
    return std::string(p, (size_t)sz);
}

// the engine passes save paths RELATIVE to its user directory (measured: "save games/autosave.eu4"),
// and the process CWD is the install dir -- resolve relative paths against the user dir (measured live)
inline std::string userdir_root();
inline std::string resolve_save_path(const std::string& p) {
    if (p.size() >= 2 && (p[1] == ':' || (p[0] == '\\' && p[1] == '\\'))) return p;   // absolute already
    std::string root = userdir_root();
    return root.empty() ? p : root + p;
}
inline std::string documents_save_dir() {
    // the Documents folder as Windows resolves it (OneDrive-redirected here): the user shell folder value
    char buf[MAX_PATH * 2] = {0}; DWORD n = sizeof buf;
    if (RegGetValueA(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders", "Personal",
                     RRF_RT_REG_SZ, nullptr, buf, &n) != ERROR_SUCCESS || !buf[0]) return std::string();   // a REG_EXPAND_SZ value is expanded and returned as REG_SZ (RRF_RT_REG_EXPAND_SZ would need RRF_NOEXPAND)
    return std::string(buf) + "\\Paradox Interactive\\Europa Universalis IV\\save games\\";
}
inline std::string userdir_root() {
    std::string d = documents_save_dir();                       // ends in ...(EU4 user dir)(backslash)save games(backslash)
    size_t k = d.rfind("save games");
    return k == std::string::npos ? std::string() : d.substr(0, k);
}

// called from the loading-path wrapper for a SAVEGAME, before the first tick; true if a sidecar was applied
inline bool restore_for_load() {
    std::string name = loaded_save_name();
    if (name.empty()) { note("no save name at G+0x2430: nothing to restore"); g_restore_missing++; { std::lock_guard<std::mutex> lk(assign::g_mx); assign::g_table.clear(); } return false; }
    std::string docs = documents_save_dir();
    std::string cands[2] = { g_last_dir.empty() ? std::string() : g_last_dir + name + ".pgt", docs.empty() ? std::string() : docs + name + ".pgt" };
    for (auto& c : cands) {
        if (c.empty()) continue;
        std::map<std::pair<int, std::string>, std::string> t;
        if (assign::read_file(c, &t)) {
            { std::lock_guard<std::mutex> lk(assign::g_mx); assign::g_table = t; assign::g_dirty = true; }
            g_restored++;
            note("restored " + std::to_string(t.size()) + " entries from " + c);
            return true;
        }
    }
    g_restore_missing++;
    { std::lock_guard<std::mutex> lk(assign::g_mx); assign::g_table.clear(); }   // never carry another world's table into this one (reviewed)
    note("no sidecar for " + name + " (a save made without the mod): the opening rule runs once");
    return false;
}

// called from the loading-path wrapper for a NEW GAME, before the first tick
inline void on_new_game() { { std::lock_guard<std::mutex> lk(assign::g_mx); assign::g_table.clear(); assign::g_dirty = true; } g_cleared++; note("new game: table cleared"); }

inline bool install(const std::string& logpath, std::string* err) {
    g_log = logpath;
    if (g_installed) return true;
    int done = 0;
    for (uintptr_t rva : RENAME_SITES) {
        uintptr_t site = livetrade::module_base() + rva;
        uint8_t* th = detour::alloc_near(site, 32);
        if (!th) { if (err) *err = "no memory within rel32 range of the rename site"; continue; }
        uint8_t* p = th;
        *p++ = 0x48; *p++ = 0xB8; uint64_t f = (uint64_t)&rename_wrapper; memcpy(p, &f, 8); p += 8;
        *p++ = 0xFF; *p++ = 0xE0;
        std::string e;
        if (detour::repoint_call(site, livetrade::module_base() + RENAME_FN, th, &e)) done++; else if (err) *err = e;
    }
    if (done != 2) return false;
    g_installed = true;
    return true;
}

} // namespace savegame
