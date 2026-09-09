#pragma once
// STAND IN FOR d3dx9_43.dll WITHOUT SHIPPING A COPY OF IT.
//
// The mod loads because Windows finds our d3dx9_43.dll in the game directory before the System32
// one. That means we must still SERVE the eight d3dx9_43 exports eu4.exe imports, or the
// process dies at load. (Those eight -- D3DXCompileShader, D3DXCreateCubeTexture,
// D3DXCreateLine, D3DXCreateTexture, D3DXLoadSurfaceFromMemory, D3DXLoadSurfaceFromSurface,
// D3DXSaveSurfaceToFileInMemory, D3DXSaveTextureToFileInMemory -- are exactly the names in
// eu4.exe's import table (llvm-objdump -p on the 1.37.5 build 835bfdf8); a proxy that exports
// any fewer dies at load, extra names are harmless.)
//
// Why this slot: v1.0 and v1.0.1 shipped as version.dll, which is also the game-directory
// stand-in of the double-byte (CJK font) patches such as EU4DLL, and two files called
// version.dll cannot both win the slot. d3dx9_43.dll is free: eu4.exe imports it by name, no
// font patch claims it, it is not a KnownDLL (registry checked), and Windows loads the
// game-directory copy before the System32 one. The switch was contributed in PR #1
// (2026-09-09) and ships as v1.0.2.
//
// Each export is a one-instruction stub (a 6-byte indirect jmp) through a pointer we fill in during
// DllMain, from the real DLL loaded by ABSOLUTE path out of the system directory. No copy, no
// second file, no name that can collide with our own. The stubs carry no signatures on purpose: a
// tail jump preserves every register and the stack frame exactly, so it forwards any calling
// convention.
//
// FAILURE IS LOUD (v1.0.2). All eight return an HRESULT, and the pre-init stub
// pgt_fwd_unavailable returns 0, which is S_OK: a stubbed D3DXCreateTexture would report
// success and hand the engine an unwritten pointer. So DllMain refuses to load (returns FALSE)
// unless complete(): the real DLL loaded and every export resolved. The loader then fails
// eu4.exe with Windows' own "unable to start correctly" message, and the log's first lines say
// why. The stub is reachable only by a call made before init(), which eu4.exe cannot make.
#include <windows.h>
#include <string>

namespace proxy {

// Filled by init(). Named with a pgt_fwd_ prefix so the inline asm below can reference them by a
// stable unmangled symbol (extern "C", and x86-64 Windows adds no leading underscore).
#define PGT_D3DX_EXPORTS(X)      \
    X(D3DXCompileShader)         \
    X(D3DXCreateCubeTexture)     \
    X(D3DXCreateLine)            \
    X(D3DXCreateTexture)         \
    X(D3DXLoadSurfaceFromMemory) \
    X(D3DXLoadSurfaceFromSurface)\
    X(D3DXSaveSurfaceToFileInMemory)\
    X(D3DXSaveTextureToFileInMemory)

// A call that arrives before init() must not jump through a null pointer, so every forwarding
// pointer STARTS at this stub (below) rather than at nullptr. Unreached in practice -- DllMain runs
// before eu4.exe's own code -- and never the steady state: a name init() cannot resolve makes
// DllMain refuse the load (complete() below), so no D3DX import is ever served by this stub.
extern "C" unsigned long long pgt_fwd_unavailable(void) { return 0; }

extern "C" {
#define PGT_DECL_PTR(n) void* pgt_fwd_##n = (void*)&pgt_fwd_unavailable;
PGT_D3DX_EXPORTS(PGT_DECL_PTR)
#undef PGT_DECL_PTR
}

#define PGT_STUB(n) \
    asm(".text\n.globl " #n "\n" #n ":\n  jmp *pgt_fwd_" #n "(%rip)\n");
PGT_D3DX_EXPORTS(PGT_STUB)
#undef PGT_STUB

#define PGT_COUNT_ONE(n) + 1
constexpr int EXPORT_COUNT = 0 PGT_D3DX_EXPORTS(PGT_COUNT_ONE);   // 8, derived from the list above
#undef PGT_COUNT_ONE

inline int g_resolved = 0;
inline bool g_loaded = false;
inline bool g_self_collision = false;
inline std::string g_private_path;    // the file the exports were actually resolved from, for the log
inline std::string g_unresolved;      // the names GetProcAddress did not find, space-separated, for the log

// Called first thing in DllMain. LoadLibrary under the loader lock is the standard proxy pattern.
// The real d3dx9_43.dll imports msvcrt, GDI32, KERNEL32 and ADVAPI32 (llvm-objdump -p on the
// System32 copy); the loader maps whatever is not yet present.
inline void init() {
    char sysdir[MAX_PATH] = {0};
    UINT n = GetSystemDirectoryA(sysdir, MAX_PATH);
    if (!n || n >= MAX_PATH) return;
    std::string sys = std::string(sysdir) + "\\d3dx9_43.dll";

    // A PRIVATE COPY FIRST. On the version.dll slot (2026-08-28) LoadLibraryA of the full System32
    // path handed back OUR OWN module: the stubs then pointed at themselves and the first version
    // API call recursed until the process died silently. So the real DLL is loaded under a name
    // that cannot collide. On the d3dx9_43 slot the collision did NOT reproduce: with the private
    // copy locked and unreadable (measured 2026-09-09) the fallback below loaded the real System32
    // file and resolved 8/8. Both paths stay: the copy is the first choice, the direct load is a
    // real second chance, and a self-collision, should it happen, is still refused.
    char tmp[MAX_PATH] = {0};
    DWORD tn = GetTempPathA(MAX_PATH, tmp);
    HMODULE h = nullptr;
    if (tn && tn < MAX_PATH) {
        std::string priv = std::string(tmp) + "pgt_d3dx9_orig.dll";
        // Overwrite when we can; if a previous run's copy is still mapped the copy fails and the
        // existing file is equally good -- it is the same system DLL.
        CopyFileA(sys.c_str(), priv.c_str(), FALSE);
        h = LoadLibraryA(priv.c_str());
        if (h) g_private_path = priv;
    }
    if (!h) {                                     // last resort; guarded below. When THIS module is
        h = LoadLibraryA(sys.c_str());            // named d3dx9_43.dll the loader hands back our own
        if (h) g_private_path = sys + " (system copy; the private copy could not be loaded)";
    }

    // Never accept our own module, whatever route produced it: that is the recursion above.
    HMODULE self = nullptr;
    GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                       (LPCSTR)&pgt_fwd_unavailable, &self);
    if (h && h == self) { g_self_collision = true; h = nullptr; }
    if (!h) return;
    g_loaded = true;
#define PGT_RESOLVE(nm) \
    pgt_fwd_##nm = (void*)GetProcAddress(h, #nm); \
    if (pgt_fwd_##nm) g_resolved++; else { pgt_fwd_##nm = (void*)&pgt_fwd_unavailable; g_unresolved += " " #nm; }
    PGT_D3DX_EXPORTS(PGT_RESOLVE)
#undef PGT_RESOLVE
}

// The only state in which this proxy may stand in for the system DLL. DllMain refuses otherwise.
inline bool complete() { return g_loaded && !g_self_collision && g_resolved == EXPORT_COUNT; }

} // namespace proxy
