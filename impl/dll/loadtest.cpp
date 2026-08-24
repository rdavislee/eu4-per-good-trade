// Load-test host for per-good-trade.dll. LoadLibrary's the mod DLL, which runs its DllMain
// attach logic against THIS process's main module. Because this host is not eu4.exe, the build
// gate must REFUSE (no "release_1.37.5" in the image) -- proving the gate fails closed on a
// wrong target (spec 2.5 / TESTING A4's second half) in a real in-process attach, and that the
// solver headers link and load inside a DLL. Injecting into the real eu4.exe is the live step.
#include <windows.h>
#include <cstdio>

int main(int argc, char** argv) {
    const char* dll = argc > 1 ? argv[1] : "per-good-trade.dll";
    printf("loading %s into a non-EU4 host (build gate must refuse)...\n", dll);
    HMODULE h = LoadLibraryA(dll);
    if (!h) {
        printf("LoadLibrary failed: %lu\n", GetLastError());
        return 1;
    }
    printf("loaded and DllMain ran. See per-good-trade.log for the attach verdict.\n");
    FreeLibrary(h);
    return 0;
}
