// PASS-path test host for per-good-trade.dll. Unlike loadtest.cpp this host EMBEDS the target
// version string, so the in-memory build-gate scan finds it, and it sets PGT_ROOT to the real
// EU4 install so the file identity checks and the embedded solver self-test run against real
// data -- all INSIDE this process, proving the DLL's pass path and the in-process solver without
// injecting into the live game. (Live injection into eu4.exe is the remaining step.)
#include <windows.h>
#include <cstdio>

// volatile + referenced so the linker keeps it and the scanner finds it in this image
volatile const char kBuildTag[] = "release_1.37.5";

int main(int argc, char** argv) {
    const char* dll = argc > 1 ? argv[1] : "per-good-trade.dll";
    printf("PASS-path host: build tag '%s' embedded at %p\n", (const char*)kBuildTag,
           (void*)kBuildTag);
    // touch it so it is not optimised away
    if (kBuildTag[0] == 0) return 99;
    HMODULE h = LoadLibraryA(dll);
    if (!h) { printf("LoadLibrary failed: %lu\n", GetLastError()); return 1; }
    printf("DllMain ran; see per-good-trade.log.\n");
    FreeLibrary(h);
    return 0;
}
