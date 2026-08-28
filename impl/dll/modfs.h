// MOD-AWARE FILE RESOLUTION (user, 2026-08-27: "test compatibility with anbennar and then
// extended timeline"). The solver's statics -- trade nodes, goods order, prices, static
// modifiers, defines -- were read from the VANILLA install, so under a total conversion the
// model solved a world that was not the one the engine was running: `matched 0/80 live nodes
// to solver nodes by name`, world total 0 (measured, Anbennar 1444). The engine's own rule is
// dlc_load.json -> enabled .mod descriptors -> each mod's files override the install's, later
// mods winning per FILE; directories merge by filename. This module reproduces exactly that for
// the handful of files gamedata reads. Zip-archived mods are logged and skipped (both compat
// targets are unpacked workshop directories; the engine itself prefers unpacked content).
#pragma once
#include <string>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>
#include <filesystem>

namespace savegame { std::string userdir_root(); }   // registry Personal + Paradox path (savegame.h)

namespace modfs {

namespace fs2 = std::filesystem;

inline std::vector<std::string> g_roots;      // [install, mod1, mod2, ...] later wins
inline std::vector<std::string> g_names;      // mod display names, for the log
inline std::vector<std::string> g_replace;    // replace_path prefixes from every enabled mod
// A replace_path'd directory removes the INSTALL's files under it (the engine's rule: mods
// replace the base game, never each other). Without this, a total conversion that renames a
// file would get vanilla content merged in beside its own.
inline bool install_replaced(const std::string& rel) {
    std::string r = rel; for (auto& c : r) if (c == 92) c = '/';
    for (auto& c : r) c = (char)tolower((unsigned char)c);
    for (const std::string& pre : g_replace) {
        if (r.size() >= pre.size() && r.compare(0, pre.size(), pre) == 0 &&
            (r.size() == pre.size() || r[pre.size()] == '/')) return true;
    }
    return false;
}
inline int g_zip_skipped = 0;

inline std::string read_all(const std::string& p) {
    std::ifstream f(p, std::ios::binary);
    if (!f) return std::string();
    std::ostringstream ss; ss << f.rdbuf(); return ss.str();
}

// one string field from a Paradox .mod descriptor: key="value"
inline std::string mod_field(const std::string& text, const std::string& key) {
    size_t at = 0;
    while ((at = text.find(key, at)) != std::string::npos) {
        size_t eq = text.find('=', at + key.size());
        if (eq == std::string::npos) return std::string();
        size_t q1 = text.find('"', eq);
        if (q1 == std::string::npos) return std::string();
        size_t q2 = text.find('"', q1 + 1);
        if (q2 == std::string::npos) return std::string();
        // key must start a token (avoid matching remote_file_id inside another word)
        if (at == 0 || text[at-1] == '\n' || text[at-1] == '\r' || text[at-1] == '\t' || text[at-1] == ' ')
            return text.substr(q1 + 1, q2 - q1 - 1);
        at = q2;
    }
    return std::string();
}

// dlc_load.json's enabled_mods array, in order (tiny fixed-shape JSON; no parser needed)
inline std::vector<std::string> enabled_mods(const std::string& userdir) {
    std::vector<std::string> out;
    std::string j = read_all(userdir + "\\dlc_load.json");
    size_t a = j.find("\"enabled_mods\"");
    if (a == std::string::npos) return out;
    size_t lb = j.find('[', a), rb = j.find(']', a);
    if (lb == std::string::npos || rb == std::string::npos) return out;
    size_t p = lb;
    while (true) {
        size_t q1 = j.find('"', p + 1);
        if (q1 == std::string::npos || q1 > rb) break;
        size_t q2 = j.find('"', q1 + 1);
        if (q2 == std::string::npos || q2 > rb) break;
        out.push_back(j.substr(q1 + 1, q2 - q1 - 1));
        p = q2;
    }
    return out;
}

// build the root list once per campaign load (cheap; called from the setup path)
inline void build(const std::string& install_root, std::ofstream* log) {
    g_roots.clear(); g_names.clear(); g_replace.clear(); g_zip_skipped = 0;
    g_roots.push_back(install_root); g_names.push_back("<install>");
    std::string ud = savegame::userdir_root();
    for (const std::string& rel : enabled_mods(ud)) {
        std::string desc = ud + "\\" + rel;
        for (auto& c : desc) if (c == '/') c = '\\';
        std::string text = read_all(desc);
        if (text.empty()) { if (log) *log << "  [modfs] descriptor unreadable: " << desc << (char)10; continue; }
        {   // every replace_path="..." in the descriptor
            size_t at = 0;
            while ((at = text.find("replace_path", at)) != std::string::npos) {
                size_t q1 = text.find('"', at), q2 = q1 == std::string::npos ? q1 : text.find('"', q1 + 1);
                if (q1 == std::string::npos || q2 == std::string::npos) break;
                std::string rp = text.substr(q1 + 1, q2 - q1 - 1);
                for (auto& c : rp) { if (c == 92) c = '/'; c = (char)tolower((unsigned char)c); }
                if (!rp.empty()) g_replace.push_back(rp);
                at = q2;
            }
        }
        std::string name = mod_field(text, "name");
        std::string path = mod_field(text, "path");
        std::string arch = mod_field(text, "archive");
        if (path.empty() && !arch.empty()) {
            g_zip_skipped++;
            if (log) *log << "  [modfs] SKIPPED zip-archived mod \"" << name << "\" (" << arch
                          << "): statics may be stale for it" << (char)10;
            continue;
        }
        if (path.empty()) continue;
        for (auto& c : path) if (c == '/') c = '\\';
        // relative paths are relative to the user dir (the launcher's convention)
        std::string full = (path.size() > 1 && (path[1] == ':' || path[0] == '\\')) ? path : ud + "\\" + path;
        if (!fs2::exists(full)) { if (log) *log << "  [modfs] mod path missing: " << full << (char)10; continue; }
        g_roots.push_back(full); g_names.push_back(name.empty() ? rel : name);
    }
    if (log) {
        *log << "  [modfs] file roots (later wins):";
        for (auto& n : g_names) *log << " [" << n << "]";
        *log << (char)10;
    }
}

// the winning FILE for a relative path (later roots override), or "" when nowhere
inline std::string resolve(const std::string& rel) {
    std::string r = rel; for (auto& c : r) if (c == '/') c = (char)92;
    for (size_t i = g_roots.size(); i-- > 0; ) {
        if (i == 0 && install_replaced(rel)) break;      // the engine dropped the install's copy
        std::string p = g_roots[i] + (char)92 + r;
        if (fs2::exists(p)) return p;
    }
    return std::string();
}

// merged directory listing: union of *.ext filenames across roots, winner per filename = the
// LAST root shipping it; returned as full paths sorted by FILENAME (the engine's read order)
inline std::vector<std::string> resolve_dir(const std::string& reldir, const std::string& ext) {
    std::string r = reldir; for (auto& c : r) if (c == '/') c = '\\';
    std::map<std::string, std::string> by_name;   // filename -> winning full path
    bool skip_install = install_replaced(reldir);
    for (size_t ri = 0; ri < g_roots.size(); ri++) {   // forward: later roots overwrite
        const std::string& root = g_roots[ri];
        if (ri == 0 && skip_install) continue;         // replace_path: the engine dropped these
        std::error_code ec;
        fs2::path dir = fs2::path(root) / r;
        if (!fs2::is_directory(dir, ec)) continue;
        for (auto& e : fs2::directory_iterator(dir, ec)) {
            if (!e.is_regular_file()) continue;
            std::string fn = e.path().filename().string();
            if (ext.size() && (fn.size() < ext.size() ||
                _stricmp(fn.c_str() + fn.size() - ext.size(), ext.c_str()) != 0)) continue;
            by_name[fn] = e.path().string();
        }
    }
    std::vector<std::string> out;
    for (auto& [fn, full] : by_name) out.push_back(full);
    return out;
}

} // namespace modfs
