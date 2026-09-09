#pragma once
// UPGRADE GUARD (v1.0.2). v1.0 and v1.0.1 shipped as version.dll; v1.0.2 ships as d3dx9_43.dll.
// A player who drops the new file next to the old one runs BOTH: eu4.exe's import table binds
// VERSION.dll before d3dx9_43.dll, so the old build's DllMain runs first, repoints the setup call
// sites, and owns the process; this copy sees the sites taken (dllmain.cpp's one-instance test)
// and stays inert. Nothing crashes, and the player silently plays the old build.
//
// The stale file is recognised by its PE export-directory name, NEVER by the file name: EU4DLL's
// own version.dll lives at the same path and must not trip this. `LIBRARY per-good-trade` in the
// .def (since v1.0) makes lld record the name as "per-good-trade.dll" (measured on the v1.0.1
// release and on this build; the System32 files read "VERSION.dll" and "d3dx9_43.dll"), so both
// spellings are accepted, case-insensitively. Pure file parsing, no LoadLibrary (loading the file
// would run its DllMain).
#include <windows.h>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <string>

namespace stalecheck {

// The export-directory name of the PE image at `path`; "" when the file is missing, is not a PE
// image, has no export table, or is malformed. Every read is bounds-checked against the file size.
inline std::string export_name(const std::string& path) {
    std::ifstream f(path, std::ios::binary);
    if (!f) return "";
    std::string s((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
    const size_t n = s.size();
    auto rd16 = [&](size_t o) -> uint32_t {
        return o + 2 <= n ? (uint32_t)(uint8_t)s[o] | ((uint32_t)(uint8_t)s[o + 1] << 8) : 0;
    };
    auto rd32 = [&](size_t o) -> uint32_t {
        return o + 4 <= n ? (uint32_t)(uint8_t)s[o] | ((uint32_t)(uint8_t)s[o + 1] << 8) |
                            ((uint32_t)(uint8_t)s[o + 2] << 16) | ((uint32_t)(uint8_t)s[o + 3] << 24) : 0;
    };
    if (n < 0x40 || s[0] != 'M' || s[1] != 'Z') return "";
    uint32_t pe = rd32(0x3C);                                   // IMAGE_DOS_HEADER.e_lfanew
    if (pe == 0 || (size_t)pe + 24 > n || rd32(pe) != 0x00004550) return "";   // "PE\0\0"
    uint32_t nsec = rd16(pe + 6);                               // FileHeader.NumberOfSections
    uint32_t optsz = rd16(pe + 20);                             // FileHeader.SizeOfOptionalHeader
    size_t opt = (size_t)pe + 24;
    uint32_t magic = rd16(opt);
    size_t dd = magic == 0x20B ? opt + 112 : magic == 0x10B ? opt + 96 : 0;   // DataDirectory[0]: exports
    if (!dd || opt + optsz > n) return "";
    uint32_t exp_rva = rd32(dd), exp_size = rd32(dd + 4);
    if (!exp_rva || exp_size < 40) return "";
    size_t sec = opt + optsz;                                   // the section table follows the optional header
    auto rva2off = [&](uint32_t rva) -> size_t {
        for (uint32_t i = 0; i < nsec && i < 96; i++) {
            size_t h = sec + (size_t)i * 40;
            if (h + 40 > n) return 0;
            uint32_t vsz = rd32(h + 8), va = rd32(h + 12), rsz = rd32(h + 16), raw = rd32(h + 20);
            uint32_t span = vsz > rsz ? vsz : rsz;
            if (rva >= va && rva < va + span) { size_t off = (size_t)raw + (rva - va); return off < n ? off : 0; }
        }
        return 0;
    };
    size_t ed = rva2off(exp_rva);
    if (!ed || ed + 40 > n) return "";
    size_t nm = rva2off(rd32(ed + 12));                         // IMAGE_EXPORT_DIRECTORY.Name
    if (!nm) return "";
    std::string out;
    for (size_t i = nm; i < n && s[i] != '\0' && out.size() < 256; i++) out += s[i];
    return out;
}

// True when the file at `path` is a build of THIS mod, of any version.
inline bool is_per_good_trade(const std::string& path) {
    std::string n = export_name(path);
    for (char& c : n) c = (char)tolower((unsigned char)c);
    return n == "per-good-trade" || n == "per-good-trade.dll";
}

// Tell the player from a thread of our own, so nothing runs under the loader lock. Once per launch
// while the stale file exists; the log carries the same text.
inline DWORD WINAPI warn_thread(LPVOID p) {
    std::string* msg = (std::string*)p;
    Sleep(2500);
    MessageBoxA(nullptr, msg->c_str(), "Mare Liberum: an old version.dll is still installed",
                MB_OK | MB_ICONWARNING | MB_TOPMOST | MB_SETFOREGROUND);
    delete msg;
    return 0;
}
inline void warn_later(const std::string& text) {
    HANDLE t = CreateThread(nullptr, 0, warn_thread, new std::string(text), 0, nullptr);
    if (t) CloseHandle(t);
}

} // namespace stalecheck
