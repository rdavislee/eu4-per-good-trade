// Manual DLL injector: loads per-good-trade.dll into the already-running eu4.exe via
// CreateRemoteThread(LoadLibraryA). In-process, the DLL reads/writes the live trade structures
// directly and hooks the monthly tick -- solving the pooled-memory problem that defeats external
// fixed-address breakpoints (the tick's computed values reallocate each month). No game restart.
//
// Build: g++ -O2 -std=c++17 -o injector.exe injector.cpp
#include <windows.h>
#include <tlhelp32.h>
#include <cstdio>
#include <string>

static DWORD find_pid(const char* name) {
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 pe{}; pe.dwSize = sizeof(pe);
    DWORD pid = 0;
    if (Process32First(snap, &pe)) do {
        if (_stricmp(pe.szExeFile, name) == 0) { pid = pe.th32ProcessID; break; }
    } while (Process32Next(snap, &pe));
    CloseHandle(snap);
    return pid;
}

int main(int argc, char** argv) {
    if (argc < 2) { printf("usage: injector <full\\path\\to\\dll>\n"); return 2; }
    std::string dll = argv[1];
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!h) { printf("OpenProcess failed %lu\n", GetLastError()); return 1; }
    size_t n = dll.size() + 1;
    void* remote = VirtualAllocEx(h, nullptr, n, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!remote) { printf("VirtualAllocEx failed\n"); return 1; }
    if (!WriteProcessMemory(h, remote, dll.c_str(), n, nullptr)) { printf("WPM failed\n"); return 1; }
    HMODULE k32 = GetModuleHandleA("kernel32.dll");
    auto loadlib = (LPTHREAD_START_ROUTINE)GetProcAddress(k32, "LoadLibraryA");
    HANDLE th = CreateRemoteThread(h, nullptr, 0, loadlib, remote, 0, nullptr);
    if (!th) { printf("CreateRemoteThread failed %lu\n", GetLastError()); return 1; }
    WaitForSingleObject(th, 10000);
    DWORD exitcode = 0; GetExitCodeThread(th, &exitcode);
    printf("injected %s into pid %lu; LoadLibrary returned module 0x%lx\n", dll.c_str(), pid, exitcode);
    VirtualFreeEx(h, remote, 0, MEM_RELEASE);
    CloseHandle(th); CloseHandle(h);
    return exitcode ? 0 : 1;
}
