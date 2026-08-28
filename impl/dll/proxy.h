#pragma once
// STAND IN FOR version.dll WITHOUT SHIPPING A COPY OF IT.
//
// The mod loads because Windows finds our version.dll in the game directory before the System32
// one. That means we must still SERVE the fifteen version.dll exports eu4.exe imports, or the
// process dies at load.
//
// This used to be done with .def forwarders (`GetFileVersionInfoA = pgt_version_orig.…`), which
// required the user to hand-copy System32's version.dll into the game directory under a private
// name. That was the single most error-prone step in installing this mod, and getting it wrong
// kills the process before any window or log appears -- the forwarder target CANNOT be named
// "version", because the loader resolves it by the normal search order and finds US, and a
// self-referential forwarder is a load-time failure.
//
// Instead each export is a two-instruction stub that jumps through a pointer we fill in during
// DllMain, from the real DLL loaded by ABSOLUTE path out of the system directory. No copy, no
// second file, no name that can collide with our own. The stubs carry no signatures on purpose: a
// tail jump preserves every register and the stack frame exactly, so it forwards any calling
// convention -- including GetFileVersionInfoByHandle, which is undocumented and whose prototype we
// would otherwise have to guess.
#include <windows.h>
#include <string>

namespace proxy {

// Filled by init(). Named with a pgt_fwd_ prefix so the inline asm below can reference them by a
// stable unmangled symbol (extern "C", and x86-64 Windows adds no leading underscore).
#define PGT_VERSION_EXPORTS(X)      \
    X(GetFileVersionInfoA)          \
    X(GetFileVersionInfoByHandle)   \
    X(GetFileVersionInfoExW)        \
    X(GetFileVersionInfoExA)        \
    X(GetFileVersionInfoSizeA)      \
    X(GetFileVersionInfoSizeExW)    \
    X(GetFileVersionInfoSizeExA)    \
    X(GetFileVersionInfoSizeW)      \
    X(GetFileVersionInfoW)          \
    X(VerFindFileA)                 \
    X(VerFindFileW)                 \
    X(VerInstallFileA)              \
    X(VerInstallFileW)              \
    X(VerLanguageNameA)             \
    X(VerLanguageNameW)             \
    X(VerQueryValueA)               \
    X(VerQueryValueW)

extern "C" {
#define PGT_DECL_PTR(n) void* pgt_fwd_##n = nullptr;
PGT_VERSION_EXPORTS(PGT_DECL_PTR)
#undef PGT_DECL_PTR
}

// A call that arrives before init() (or for an export this Windows build lacks) must not jump to
// null. Unreached in practice -- DllMain runs before eu4.exe's own code -- but a proxy that faults
// instead of failing is the worst possible failure mode.
extern "C" unsigned long long pgt_fwd_unavailable(void) { return 0; }

#define PGT_STUB(n) \
    asm(".text\n.globl " #n "\n" #n ":\n  jmp *pgt_fwd_" #n "(%rip)\n");
PGT_VERSION_EXPORTS(PGT_STUB)
#undef PGT_STUB

inline int g_resolved = 0;
inline bool g_loaded = false;
inline bool g_self_collision = false;
inline std::string g_private_path;

// Called first thing in DllMain. LoadLibrary under the loader lock is the standard proxy pattern
// and is safe for this target: version.dll's own imports are kernel32/ntdll, already present.
inline void init() {
    char sysdir[MAX_PATH] = {0};
    UINT n = GetSystemDirectoryA(sysdir, MAX_PATH);
    if (!n || n >= MAX_PATH) return;
    std::string sys = std::string(sysdir) + "\\version.dll";

    // WE ARE NAMED version.dll, AND THAT POISONS LoadLibrary. The loader matches an already-loaded
    // module by BASE NAME before it considers the path, so LoadLibraryA("C:\Windows\System32\
    // version.dll") hands back OUR OWN handle. GetProcAddress then returns our stubs, each stub
    // jumps through a pointer to itself, and the first version API call the game makes recurses
    // until the process dies -- measured: a clean attach, then silent death before any campaign,
    // no crash dump. Load the real DLL under a name that cannot collide instead.
    char tmp[MAX_PATH] = {0};
    DWORD tn = GetTempPathA(MAX_PATH, tmp);
    HMODULE h = nullptr;
    if (tn && tn < MAX_PATH) {
        std::string priv = std::string(tmp) + "pgt_version_orig.dll";
        // Overwrite when we can; if a previous run's copy is still mapped the copy fails and the
        // existing file is equally good -- it is the same system DLL.
        CopyFileA(sys.c_str(), priv.c_str(), FALSE);
        h = LoadLibraryA(priv.c_str());
        g_private_path = priv;
    }
    if (!h) h = LoadLibraryA(sys.c_str());        // last resort; guarded below

    // Never accept our own module, whatever route produced it: that is the recursion above.
    HMODULE self = nullptr;
    GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                       (LPCSTR)&pgt_fwd_unavailable, &self);
    if (h && h == self) { g_self_collision = true; h = nullptr; }
    if (!h) return;
    g_loaded = true;
#define PGT_RESOLVE(nm) \
    pgt_fwd_##nm = (void*)GetProcAddress(h, #nm); \
    if (pgt_fwd_##nm) g_resolved++; else pgt_fwd_##nm = (void*)&pgt_fwd_unavailable;
    PGT_VERSION_EXPORTS(PGT_RESOLVE)
#undef PGT_RESOLVE
}

} // namespace proxy
