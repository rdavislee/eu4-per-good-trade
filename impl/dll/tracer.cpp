// Hardware-breakpoint tracer for the RE session (spec 2.9 memory track). Attaches to eu4.exe as
// a debugger, sets a HW breakpoint (debug registers DR0-3) on a target address, and logs every
// instruction that reads/writes it -- RIP as module+offset, plus the general registers, so the
// trade struct base register and the trade-tick code are found empirically instead of guessed.
//
//   tracer <hexaddr> <r|w|rw> <seconds> [<hexaddr2> ...]   up to 4 addresses (DR0-3)
//
// Detaches cleanly (DebugActiveProcessStop) so the game keeps running.
// Build: g++ -O2 -std=c++17 -o tracer.exe tracer.cpp
#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <map>
#include <set>
#include <string>
#include <vector>

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

static void enable_debug_priv() {
    HANDLE tok;
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &tok)) return;
    TOKEN_PRIVILEGES tp{}; tp.PrivilegeCount = 1;
    LookupPrivilegeValue(nullptr, SE_DEBUG_NAME, &tp.Privileges[0].Luid);
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    AdjustTokenPrivileges(tok, FALSE, &tp, sizeof(tp), nullptr, nullptr);
    CloseHandle(tok);
}

static uintptr_t g_base = 0; static size_t g_size = 0;
static void module_range(DWORD pid) {
    HANDLE h = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
    if (!h) return;
    HMODULE mods[1024]; DWORD need;
    if (EnumProcessModules(h, mods, sizeof(mods), &need)) {
        MODULEINFO mi{};
        if (GetModuleInformation(h, mods[0], &mi, sizeof(mi))) {
            g_base = (uintptr_t)mi.lpBaseOfDll; g_size = mi.SizeOfImage;
        }
    }
    CloseHandle(h);
}
static std::string modoff(uintptr_t rip) {
    if (rip >= g_base && rip < g_base + g_size)
        return "eu4.exe+0x" + [&]{ char b[32]; sprintf(b, "%llx", (unsigned long long)(rip - g_base)); return std::string(b); }();
    char b[32]; sprintf(b, "0x%llx", (unsigned long long)rip); return std::string(b);
}

struct Target { uintptr_t addr; int rw; int len; };  // rw: 1=write,3=readwrite ; len bits

static int g_verified = 0;
static void set_drs(HANDLE thread, const std::vector<Target>& tg) {
    // Debug registers must be set with the thread suspended, or the write is unreliable.
    DWORD susp = SuspendThread(thread);
    (void)susp;
    CONTEXT ctx{}; ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    if (!GetThreadContext(thread, &ctx)) { ResumeThread(thread); return; }
    DWORD64* dr[4] = {&ctx.Dr0, &ctx.Dr1, &ctx.Dr2, &ctx.Dr3};
    DWORD64 dr7 = 0;
    for (size_t i = 0; i < tg.size() && i < 4; i++) {
        *dr[i] = tg[i].addr;
        dr7 |= (DWORD64(1) << (i * 2));                       // Li enable (local)
        dr7 |= (DWORD64(1) << 8);                             // LE (local exact) recommended
        dr7 |= (DWORD64(tg[i].rw) << (16 + i * 4));           // R/Wi
        dr7 |= (DWORD64(tg[i].len) << (18 + i * 4));          // LENi
    }
    for (size_t i = tg.size(); i < 4; i++) *dr[i] = 0;
    ctx.Dr7 = dr7; ctx.Dr6 = 0;
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    SetThreadContext(thread, &ctx);
    // verify it took
    CONTEXT chk{}; chk.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    if (GetThreadContext(thread, &chk) && !tg.empty() && chk.Dr0 == tg[0].addr && (chk.Dr7 & 1))
        g_verified++;
    ResumeThread(thread);
}

static std::vector<DWORD> thread_ids(DWORD pid) {
    std::vector<DWORD> out;
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    THREADENTRY32 te{}; te.dwSize = sizeof(te);
    if (Thread32First(snap, &te)) do {
        if (te.th32OwnerProcessID == pid) out.push_back(te.th32ThreadID);
    } while (Thread32Next(snap, &te));
    CloseHandle(snap);
    return out;
}

int main(int argc, char** argv) {
    if (argc < 4) { printf("usage: tracer <hexaddr> <r|w|rw> <seconds> [addr2 ...]\n"); return 2; }
    // mode: w=write(01,len4), rw=readwrite(11,len4), x=execute(00,len0)
    bool exec = !strcmp(argv[2], "x");
    int rwmode = exec ? 0 : (!strcmp(argv[2], "w") ? 1 : 3);
    int lenbits = exec ? 0 : 3;                    // exec BP must use LEN=00
    int secs = atoi(argv[3]);
    std::vector<Target> targets;
    targets.push_back({(uintptr_t)strtoull(argv[1], nullptr, 0), rwmode, lenbits});
    for (int i = 4; i < argc && targets.size() < 4; i++)
        targets.push_back({(uintptr_t)strtoull(argv[i], nullptr, 0), rwmode, lenbits});

    enable_debug_priv();
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    module_range(pid);
    printf("attaching to pid %lu, base 0x%llx; %zu breakpoint(s), %ds\n",
           pid, (unsigned long long)g_base, targets.size(), secs);
    for (auto& t : targets) printf("  BP @ 0x%llx %s\n", (unsigned long long)t.addr,
                                   rwmode == 1 ? "write" : "read/write");

    if (!DebugActiveProcess(pid)) { printf("DebugActiveProcess failed %lu\n", GetLastError()); return 1; }
    DebugSetProcessKillOnExit(FALSE);

    struct Hit { uint64_t rax, rbx, rcx, rdx, rsi, rdi, rbp, r8, r9, r10, r11, r12, r13, r14, r15, rsp; int which; };
    std::map<std::string, int> hitcount;
    std::map<std::string, Hit> sample;
    std::set<uint64_t> distinct_r14, distinct_rbx, distinct_rcx;
    ULONGLONG deadline = GetTickCount64() + (ULONGLONG)secs * 1000;
    bool armed = false;
    DEBUG_EVENT ev{};
    int total_hits = 0;

    while (GetTickCount64() < deadline) {
        if (!WaitForDebugEvent(&ev, 200)) continue;
        DWORD cont = DBG_CONTINUE;
        if (ev.dwDebugEventCode == EXCEPTION_DEBUG_EVENT) {
            DWORD code = ev.u.Exception.ExceptionRecord.ExceptionCode;
            if (code == EXCEPTION_BREAKPOINT && !armed) {
                // initial breakpoint: arm DRs on all threads now (process is stopped)
                int nthreads = 0;
                for (DWORD tid : thread_ids(pid)) {
                    HANDLE th = OpenThread(THREAD_GET_CONTEXT | THREAD_SET_CONTEXT | THREAD_SUSPEND_RESUME, FALSE, tid);
                    if (th) { set_drs(th, targets); CloseHandle(th); nthreads++; }
                }
                armed = true;
                printf("armed on %d threads, %d verified DR0/DR7 set\n", nthreads, g_verified);
            } else if (code == EXCEPTION_SINGLE_STEP) {
                // our HW breakpoint fired
                HANDLE th = OpenThread(THREAD_GET_CONTEXT | THREAD_SET_CONTEXT, FALSE, ev.dwThreadId);
                if (th) {
                    CONTEXT c{}; c.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS;
                    GetThreadContext(th, &c);
                    int which = -1;
                    for (int i = 0; i < 4; i++) if (c.Dr6 & (1u << i)) which = i;
                    std::string key = modoff(c.Rip);
                    if (hitcount.find(key) == hitcount.end())
                        sample[key] = {c.Rax,c.Rbx,c.Rcx,c.Rdx,c.Rsi,c.Rdi,c.Rbp,c.R8,c.R9,c.R10,c.R11,c.R12,c.R13,c.R14,c.R15,c.Rsp,which};
                    distinct_r14.insert(c.R14); distinct_rbx.insert(c.Rbx); distinct_rcx.insert(c.Rcx);
                    hitcount[key]++;
                    total_hits++;
                    // RF (resume flag): for EXEC breakpoints, lets this instruction run once
                    // without immediately re-faulting. Harmless for data breakpoints.
                    c.EFlags |= 0x10000;
                    c.Dr6 = 0; c.ContextFlags = CONTEXT_DEBUG_REGISTERS | CONTEXT_CONTROL;
                    SetThreadContext(th, &c);
                    CloseHandle(th);
                }
            } else {
                cont = DBG_EXCEPTION_NOT_HANDLED;   // pass real exceptions to the app
            }
        } else if (ev.dwDebugEventCode == CREATE_THREAD_DEBUG_EVENT) {
            if (armed) set_drs(ev.u.CreateThread.hThread, targets);
        } else if (ev.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT) {
            break;
        }
        ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, cont);
    }
    // disarm
    for (DWORD tid : thread_ids(pid)) {
        HANDLE th = OpenThread(THREAD_GET_CONTEXT | THREAD_SET_CONTEXT, FALSE, tid);
        if (th) { std::vector<Target> none; set_drs(th, none); CloseHandle(th); }
    }
    DebugActiveProcessStop(pid);

    printf("\n=== %d hits at %zu distinct RIPs ===\n", total_hits, hitcount.size());
    printf("distinct r14=%zu rbx=%zu rcx=%zu\n", distinct_r14.size(), distinct_rbx.size(), distinct_rcx.size());
    if (distinct_r14.size() >= 40 && distinct_r14.size() <= 120) {
        FILE* f = fopen("r14_nodes.txt", "w");
        for (uint64_t v : distinct_r14) fprintf(f, "%llx\n", (unsigned long long)v);
        fclose(f);
        printf("wrote %zu distinct r14 values to r14_nodes.txt\n", distinct_r14.size());
    }
    std::vector<std::pair<std::string,int>> rows(hitcount.begin(), hitcount.end());
    std::sort(rows.begin(), rows.end(), [](auto&a, auto&b){ return a.second > b.second; });
    for (auto& [rip, n] : rows) {
        const Hit& h = sample[rip];
        printf("%6d x  %-22s DR%d  rax=%llx rbx=%llx rcx=%llx rdx=%llx rsi=%llx rdi=%llx rbp=%llx r8=%llx r12=%llx r13=%llx r14=%llx r15=%llx\n",
               n, rip.c_str(), h.which,
               (unsigned long long)h.rax,(unsigned long long)h.rbx,(unsigned long long)h.rcx,(unsigned long long)h.rdx,
               (unsigned long long)h.rsi,(unsigned long long)h.rdi,(unsigned long long)h.rbp,(unsigned long long)h.r8,
               (unsigned long long)h.r12,(unsigned long long)h.r13,(unsigned long long)h.r14,(unsigned long long)h.r15);
    }
    return 0;
}
