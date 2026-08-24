// Runtime-attach build gate (spec 2.5): the DLL must verify the target binary at attach and
// REFUSE any other. "A patch is a new binary" -- every found offset is invalidated by a patch,
// so the gate fails closed with a clear message rather than reading offsets against the wrong
// image (spec 2.3's re-measure-on-patch rule, applied to offsets).
//
// Two independent identity checks, both cheap:
//   1. eu4_rev.txt next to the module carries the build revision 835bfdf8... verbatim.
//   2. the eu4.exe image SHA-256 is pinned (measured on the frozen 1.37.5 build).
// Either mismatch -> refuse. This header is host-portable (no Windows headers) so the solver
// harness can unit-test the gate; the DLL supplies the real module-path/lookup around it.
#pragma once
#include <cstdint>
#include <fstream>
#include <string>
#include "sha256.h"

namespace attach {

// the frozen target (spec: build 835bfdf8, release_1.37.5, stamped 2024-10-03)
constexpr const char* TARGET_REV = "835bfdf8ca24c291a1b3f1b5bc72d47e7df1ae18";
constexpr const char* TARGET_BRANCH = "release_1.37.5";
constexpr const char* TARGET_EXE_SHA256 =
    "9ad3efe1af169f40ee577f9dae5debbc87af6fb8b5450fb345ebf110dc4d771a";
constexpr size_t TARGET_EXE_SIZE = 38462504;

struct Verdict {
    bool ok = false;
    std::string message;
};

inline std::string read_all(const std::string& path) {
    std::ifstream f(path, std::ios::binary);
    if (!f) return "";
    return std::string((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
}

inline std::string trim(std::string s) {
    while (!s.empty() && (s.back() == '\n' || s.back() == '\r' || s.back() == ' ' || s.back() == '\t'))
        s.pop_back();
    size_t b = 0;
    while (b < s.size() && (s[b] == ' ' || s[b] == '\t')) b++;
    return s.substr(b);
}

// eu4_root is the install directory holding eu4.exe, eu4_rev.txt, eu4_branch.txt.
// full=true also hashes the 38 MB image (slower; do it once at attach).
inline Verdict verify_install(const std::string& eu4_root, bool full = true) {
    Verdict v;
    std::string rev = trim(read_all(eu4_root + "/eu4_rev.txt"));
    if (rev.empty()) { v.message = "eu4_rev.txt not found or empty at " + eu4_root; return v; }
    if (rev != TARGET_REV) {
        v.message = "build mismatch: this DLL targets " + std::string(TARGET_REV) +
                    " (" + TARGET_BRANCH + "), found " + rev +
                    ". A patch is a new binary -- refusing to attach (spec 2.5).";
        return v;
    }
    std::string branch = trim(read_all(eu4_root + "/eu4_branch.txt"));
    if (!branch.empty() && branch != TARGET_BRANCH) {
        v.message = "branch mismatch: expected " + std::string(TARGET_BRANCH) + ", found " + branch;
        return v;
    }
    if (full) {
        std::string exe = read_all(eu4_root + "/eu4.exe");
        if (exe.size() != TARGET_EXE_SIZE) {
            v.message = "eu4.exe size mismatch: expected " + std::to_string(TARGET_EXE_SIZE) +
                        ", found " + std::to_string(exe.size()) + " -- refusing to attach";
            return v;
        }
        std::string got = sha256::hex(exe);
        if (got != TARGET_EXE_SHA256) {
            v.message = "eu4.exe SHA-256 mismatch: expected " + std::string(TARGET_EXE_SHA256) +
                        ", found " + got + " -- refusing to attach (offsets are invalid)";
            return v;
        }
    }
    v.ok = true;
    v.message = "verified build " + rev + " (" + TARGET_BRANCH + "): offsets valid";
    return v;
}

} // namespace attach
