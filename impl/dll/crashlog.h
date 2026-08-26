// LAST-WORDS CRASH LOG. The engine's own crash handler writes a minidump for access violations but
// nothing at all for a stack overflow (it needs stack to run), and twice on 2026-08-26 the process
// simply vanished: no dump, no error.log line. A vectored exception handler runs FIRST, on the
// faulting thread, before the engine's filter -- so it can still record the faulting address and
// a few return addresses with the little stack that is left. Rules for surviving there:
//   - the output file is opened at install, never at fault time (no CRT, no allocation)
//   - fixed static buffers, WriteFile only, hand-rolled hex
//   - RtlCaptureStackBackTrace for the frames (it walks with unwind tables, no allocation)
//   - EXCEPTION_CONTINUE_SEARCH always: the engine's handler still gets its turn
// Only fatal-looking codes are logged (AV, stack overflow, illegal instruction, int3, guard page),
// and at most 8 events per process, so a benign first-chance exception storm cannot fill a disk.
#pragma once
#include <windows.h>
#include <cstdint>
#include <string>

namespace crashlog {

constexpr DWORD SELFTEST_CODE = 0xE0DDF00D;
inline HANDLE g_file = INVALID_HANDLE_VALUE;
inline volatile LONG g_events = 0;
inline uintptr_t g_module_base = 0;
inline PVOID g_handler = nullptr;

inline void put(const char* s, size_t n) { DWORD w = 0; WriteFile(g_file, s, (DWORD)n, &w, nullptr); }
inline void puts_(const char* s) { size_t n = 0; while (s[n]) n++; put(s, n); }
inline void puthex(uint64_t v) {
    char b[19]; b[0] = '0'; b[1] = 'x'; int p = 2;
    bool started = false;
    for (int i = 60; i >= 0; i -= 4) { int d = (int)((v >> i) & 0xF); if (d || started || i == 0) { b[p++] = (char)(d < 10 ? '0' + d : 'a' + d - 10); started = true; } }
    b[p] = 0; put(b, (size_t)p);
}
inline void putmod(uint64_t va) {          // "eu4.exe+0x..." when inside the main module, else raw
    if (g_module_base && va >= g_module_base && va < g_module_base + 0x4000000) { puts_("eu4.exe+"); puthex(va - g_module_base); }
    else puthex(va);
}

inline LONG WINAPI handler(EXCEPTION_POINTERS* ep) {
    if (!ep || !ep->ExceptionRecord) return EXCEPTION_CONTINUE_SEARCH;
    DWORD code = ep->ExceptionRecord->ExceptionCode;
    if (code == SELFTEST_CODE) {   // the logger's own red test: log it and resume
        if (g_file != INVALID_HANDLE_VALUE) { puts_("[crashlog] SELFTEST exception seen at "); putmod((uint64_t)ep->ExceptionRecord->ExceptionAddress); puts_(" -- the handler fires"); puts_("\n"); FlushFileBuffers(g_file); }
        return EXCEPTION_CONTINUE_EXECUTION;
    }
    if (code != EXCEPTION_ACCESS_VIOLATION && code != EXCEPTION_STACK_OVERFLOW && code != EXCEPTION_ILLEGAL_INSTRUCTION &&
        code != EXCEPTION_BREAKPOINT && code != EXCEPTION_GUARD_PAGE && code != EXCEPTION_INT_DIVIDE_BY_ZERO && code != 0xC0000409)
        return EXCEPTION_CONTINUE_SEARCH;
    if (g_file == INVALID_HANDLE_VALUE) return EXCEPTION_CONTINUE_SEARCH;
    if (InterlockedIncrement(&g_events) > 8) return EXCEPTION_CONTINUE_SEARCH;
    puts_("[crashlog] exception "); puthex(code);
    puts_(" at "); putmod((uint64_t)ep->ExceptionRecord->ExceptionAddress);
    if (code == EXCEPTION_ACCESS_VIOLATION && ep->ExceptionRecord->NumberParameters >= 2) {
        puts_(ep->ExceptionRecord->ExceptionInformation[0] ? " writing " : " reading "); puthex(ep->ExceptionRecord->ExceptionInformation[1]);
    }
    if (ep->ContextRecord) { puts_(" rsp="); puthex(ep->ContextRecord->Rsp); puts_(" tid="); puthex(GetCurrentThreadId()); }
    puts_("\n");
    // the stack, if there is any left to walk it with
    void* frames[24];
    USHORT n = 0;
    if (code != EXCEPTION_STACK_OVERFLOW) n = RtlCaptureStackBackTrace(0, 24, frames, nullptr);
    else {
        // on overflow, read return addresses straight off the faulting stack: cheap, allocation-free,
        // and good enough to name the recursion
        uint64_t* sp = (uint64_t*)ep->ContextRecord->Rsp;
        for (int i = 0; i < 24 && n < 24; i++) {
            uint64_t v = sp[i];
            if (g_module_base && v >= g_module_base + 0x1000 && v < g_module_base + 0x4000000) frames[n++] = (void*)v;
        }
    }
    for (USHORT i = 0; i < n; i++) { puts_("    frame "); puthex(i); puts_(": "); putmod((uint64_t)frames[i]); puts_("\n"); }
    FlushFileBuffers(g_file);
    return EXCEPTION_CONTINUE_SEARCH;
}

inline void selftest() { RaiseException(SELFTEST_CODE, 0, 0, nullptr); }

inline bool install(const std::string& path, uintptr_t module_base, std::string* err) {
    g_module_base = module_base;
    g_file = CreateFileA(path.c_str(), FILE_APPEND_DATA, FILE_SHARE_READ, nullptr, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
    if (g_file == INVALID_HANDLE_VALUE) { if (err) *err = "cannot open the crash log file"; return false; }
    g_handler = AddVectoredExceptionHandler(1, handler);
    if (!g_handler) { if (err) *err = "AddVectoredExceptionHandler failed"; return false; }
    // a little headroom for the handler itself on THIS thread; the engine's threads keep the default
    ULONG guarantee = 32 * 1024; SetThreadStackGuarantee(&guarantee);
    return true;
}

} // namespace crashlog
