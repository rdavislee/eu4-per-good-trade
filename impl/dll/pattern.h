// In-memory byte-pattern scanner over the main module, modelled on EU4dll's BytePattern
// (matanki-saito/EU4dll, itself from ThirteenAG/Hooking.Patterns) -- the attach scaffolding
// spec 2.5 says to follow. Supports "??" wildcards. Used to (a) verify the build by finding the
// version string in the loaded image and (b) locate the trade structures / tick hook once their
// signatures are found in the debugger session.
#pragma once
#include <windows.h>
#include <cstdint>
#include <string>
#include <vector>

namespace pat {

struct Module {
    uintptr_t base = 0;
    size_t size = 0;
};

inline Module main_module() {
    Module m;
    HMODULE h = GetModuleHandleW(nullptr);
    m.base = reinterpret_cast<uintptr_t>(h);
    auto dos = reinterpret_cast<IMAGE_DOS_HEADER*>(m.base);
    auto nt = reinterpret_cast<IMAGE_NT_HEADERS*>(m.base + dos->e_lfanew);
    m.size = nt->OptionalHeader.SizeOfImage;
    return m;
}

// parse "48 8B ?? 89" into bytes + mask (0 = wildcard)
inline void parse(const std::string& sig, std::vector<uint8_t>& bytes, std::vector<uint8_t>& mask) {
    size_t i = 0;
    while (i < sig.size()) {
        if (sig[i] == ' ') { i++; continue; }
        if (sig[i] == '?') {
            bytes.push_back(0); mask.push_back(0);
            i++; if (i < sig.size() && sig[i] == '?') i++;
        } else {
            auto hex = [](char c) -> int {
                if (c >= '0' && c <= '9') return c - '0';
                if (c >= 'a' && c <= 'f') return c - 'a' + 10;
                if (c >= 'A' && c <= 'F') return c - 'A' + 10;
                return -1;
            };
            int hi = hex(sig[i]), lo = hex(sig[i + 1]);
            bytes.push_back(uint8_t((hi << 4) | lo)); mask.push_back(1);
            i += 2;
        }
    }
}

// first match address, or 0. Scans the whole image; fine for one-time attach-scan use.
inline uintptr_t find(const Module& m, const std::string& sig) {
    std::vector<uint8_t> b, mask;
    parse(sig, b, mask);
    if (b.empty()) return 0;
    auto* p = reinterpret_cast<const uint8_t*>(m.base);
    size_t n = b.size();
    for (size_t i = 0; i + n <= m.size; i++) {
        bool ok = true;
        for (size_t j = 0; j < n; j++)
            if (mask[j] && p[i + j] != b[j]) { ok = false; break; }
        if (ok) return m.base + i;
    }
    return 0;
}

// literal ASCII search (for version strings like "release_1.37.5")
inline uintptr_t find_string(const Module& m, const std::string& lit) {
    auto* p = reinterpret_cast<const char*>(m.base);
    size_t n = lit.size();
    for (size_t i = 0; i + n <= m.size; i++) {
        if (memcmp(p + i, lit.data(), n) == 0) return m.base + i;
    }
    return 0;
}

} // namespace pat
