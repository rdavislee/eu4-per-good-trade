#pragma once
// STAND IN FOR d3dx9_43.dll WITHOUT SHIPPING A COPY OF IT.
//
// The mod loads because Windows finds our d3dx9_43.dll in the game directory before the System32
// one. That means we must still SERVE the eight d3dx9_43 exports eu4.exe imports, or the
// process dies at load. (Those eight -- D3DXCompileShader, D3DXCreateCubeTexture,
// D3DXCreateLine, D3DXCreateTexture, D3DXLoadSurfaceFromMemory, D3DXLoadSurfaceFromSurface,
// D3DXSaveSurfaceToFileInMemory, D3DXSaveTextureToFileInMemory -- are exactly the names in
// eu4.exe's import table; a proxy that exports any fewer dies at load, extra names are harmless.)
//
// Why this slot and not version.dll/d3d9.dll: those two are the game-directory stand-ins of the
// double-byte (CJK font) patches such as EU4DLL, and a trade patch that also named itself
// version.dll would collide with them -- one of the two would never load. d3dx9_43.dll is free:
// the same engine imports it on every storefront (Steam and Epic alike), no font patch claims
// the slot, and Windows loads the game-directory copy before the system one. This mirrors the
// Epic-store deployment, where the mod already runs as d3dx9_43.dll beside the double-byte
// patch's version.dll/d3d9.dll pair (see the Epic coexistence note in INSTALL.md).
//
// Each export is a two-instruction stub that jumps through a pointer we fill in during DllMain,
// from the real DLL loaded by ABSOLUTE path out of the system directory. No copy, no
// second file, no name that can collide with our own. The stubs carry no signatures on purpose: a
// tail jump preserves every register and the stack frame exactly, so it forwards any calling
// convention. (The system copy exists on every machine that can run the game at all: eu4.exe
// imports d3dx9_43.dll by name, so a box without the DirectX runtime's 64-bit d3dx9_43 in
// System32 cannot even start the game. If it is somehow missing, the stubs fall back to
// pgt_fwd_unavailable instead of faulting.)
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

extern "C" {
#define PGT_DECL_PTR(n) void* pgt_fwd_##n = nullptr;
PGT_D3DX_EXPORTS(PGT_DECL_PTR)
#undef PGT_DECL_PTR
}

// A call that arrives before init() (or for an export this Windows build lacks) must not jump to
// null. Unreached in practice -- DllMain runs before eu4.exe's own code -- but a proxy that faults
// instead of failing is the worst possible failure mode.
extern "C" unsigned long long pgt_fwd_unavailable(void) { return 0; }

#define PGT_STUB(n) \
    asm(".text\n.globl " #n "\n" #n ":\n  jmp *pgt_fwd_" #n "(%rip)\n");
PGT_D3DX_EXPORTS(PGT_STUB)
#undef PGT_STUB

inline int g_resolved = 0;
inline bool g_loaded = false;
inline bool g_self_collision = false;
inline std::string g_private_path;

// Called first thing in DllMain. LoadLibrary under the loader lock is the standard proxy pattern
// and is safe for this target: d3dx9_43.dll's own imports are kernel32/ntdll, already present.
inline void init() {
    char sysdir[MAX_PATH] = {0};
    UINT n = GetSystemDirectoryA(sysdir, MAX_PATH);
    if (!n || n >= MAX_PATH) return;
    std::string sys = std::string(sysdir) + "\\d3dx9_43.dll";

    // WE ARE NAMED d3dx9_43.dll, AND THAT POISONS LoadLibrary. The loader matches an already-
    // loaded module by BASE NAME before it considers the path, so LoadLibraryA("C:\Windows\
    // System32\d3dx9_43.dll") hands back OUR OWN handle. GetProcAddress then returns our stubs,
    // each stub jumps through a pointer to itself, and the first D3DX call the game makes
    // recurses until the process dies. Load the real DLL under a name that cannot collide
    // instead.
    char tmp[MAX_PATH] = {0};
    DWORD tn = GetTempPathA(MAX_PATH, tmp);
    HMODULE h = nullptr;
    if (tn && tn < MAX_PATH) {
        std::string priv = std::string(tmp) + "pgt_d3dx9_orig.dll";
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
    PGT_D3DX_EXPORTS(PGT_RESOLVE)
#undef PGT_RESOLVE
}

} // namespace proxy
