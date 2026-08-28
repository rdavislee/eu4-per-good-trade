// Inline hooks for eu4.exe (spec 2.5: runtime patching, following the EU4dll precedent).
//
// A hook site is chosen OFFLINE with capstone (impl/tools/disasm.py) so that its first `stolen`
// bytes are whole instructions with no RIP-relative operand and no relative branch. At install
// the site's bytes are compared against the expected signature (a patch is a new binary --
// spec 2.5 -- so a mismatch refuses, never guesses), a trampoline is built from the stolen bytes
// plus an absolute jump back, and the site is overwritten with `jmp [rip+0]; dq stub` (14
// bytes) while every other thread is suspended and verified to be outside the patched range.
//
// The generated stub saves the full GPR set + flags + the volatile XMM registers, aligns the
// stack, and calls a C++ handler with a pointer to the saved register block (`Regs`). Anything
// the handler writes into that block is restored into the live registers before control returns
// to the trampoline, so a handler can read rbx=node/rsi=mgr at the site or alter a result.
#pragma once
#include <windows.h>
#include <tlhelp32.h>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

namespace detour {

struct Regs {
    uint64_t r15, r14, r13, r12, r11, r10, r9, r8, rdi, rsi, rbp, rbx, rdx, rcx, rax, rflags;
    uint64_t rsp() const { return (uint64_t)(this + 1); }   // the original rsp at the site
};
using Handler = void (*)(Regs*);

struct Hook {
    std::string name;
    uintptr_t target = 0;           // absolute address of the site
    size_t stolen = 0;
    std::vector<uint8_t> original;
    uint8_t* stub = nullptr;        // register-saving stub (executable)
    uint8_t* trampoline = nullptr;  // stolen bytes + jmp back
    bool active = false;
    std::string error;
};

inline uint8_t* alloc_exec(size_t n) {
    return (uint8_t*)VirtualAlloc(nullptr, n, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
}

// Allocate executable memory WITHIN rel32 range of `site`. A plain VirtualAlloc(nullptr, ...) can
// land anywhere in the 64-bit address space; when a 5-byte rel32 call is then repointed at it, the
// displacement truncates and execution jumps into garbage. That is not hypothetical -- it killed
// EU4 with an access violation at its own image base (see OFFSETS.md's rel32 trap). Every
// call-site redirect in this DLL allocates its thunk through here.
inline uint8_t* alloc_near(uintptr_t site, size_t n) {
    SYSTEM_INFO si{};
    GetSystemInfo(&si);
    const uintptr_t gran = si.dwAllocationGranularity ? si.dwAllocationGranularity : 0x10000;
    for (int64_t d = (int64_t)gran; d < 0x60000000; d += (int64_t)gran) {
        for (int dir = 0; dir < 2; dir++) {
            uintptr_t probe = (dir ? (site - (uintptr_t)d) : (site + (uintptr_t)d)) & ~(uintptr_t)(gran - 1);
            if (!probe) continue;
            uint8_t* p = (uint8_t*)VirtualAlloc((void*)probe, n, MEM_COMMIT | MEM_RESERVE,
                                                PAGE_EXECUTE_READWRITE);
            if (!p) continue;
            int64_t disp = (int64_t)((intptr_t)p - (intptr_t)(site + 5));
            if (disp >= INT32_MIN && disp <= INT32_MAX) return p;
            VirtualFree(p, 0, MEM_RELEASE);        // in range for allocation, not for rel32
        }
    }
    return nullptr;
}

// Repoint an existing `e8 <rel32>` call at `site` to `thunk`, after proving the original really
// reaches `expect` (spec 2.5: a patched binary is a different binary and must be refused).
inline bool repoint_call(uintptr_t site, uintptr_t expect, uint8_t* thunk, std::string* err) {
    if (IsBadReadPtr((void*)site, 5)) { if (err) *err = "call site unreadable"; return false; }
    if (*(uint8_t*)site != 0xE8) { if (err) *err = "site is not a rel32 call"; return false; }
    int32_t rel = *(int32_t*)(site + 1);
    if (site + 5 + rel != expect) { if (err) *err = "call does not reach the expected target"; return false; }
    int64_t disp = (int64_t)((intptr_t)thunk - (intptr_t)(site + 5));
    if (disp < INT32_MIN || disp > INT32_MAX) { if (err) *err = "thunk out of rel32 range"; return false; }
    DWORD old = 0;
    if (!VirtualProtect((void*)site, 5, PAGE_EXECUTE_READWRITE, &old)) {
        if (err) *err = "VirtualProtect failed"; return false;
    }
    *(int32_t*)(site + 1) = (int32_t)disp;
    VirtualProtect((void*)site, 5, old, &old);
    FlushInstructionCache(GetCurrentProcess(), (void*)site, 5);
    return true;
}

inline void emit(std::vector<uint8_t>& b, std::initializer_list<uint8_t> bytes) {
    b.insert(b.end(), bytes.begin(), bytes.end());
}
inline void emit_u64(std::vector<uint8_t>& b, uint64_t v) {
    for (int i = 0; i < 8; i++) b.push_back((uint8_t)(v >> (8 * i)));
}
inline void emit_jmp_abs(std::vector<uint8_t>& b, uint64_t to) {
    emit(b, {0xFF, 0x25, 0x00, 0x00, 0x00, 0x00});     // jmp [rip+0]
    emit_u64(b, to);
}

// Build the stub: pushfq; push rax..r15; mov rbp,rsp; and rsp,-16; sub rsp,0xA0;
// save xmm0-5; mov rcx,rbp; mov rax,handler; call rax; restore xmm; mov rsp,rbp; pops; popfq;
// jmp trampoline.
inline std::vector<uint8_t> build_stub(uint64_t handler, uint64_t trampoline) {
    std::vector<uint8_t> b;
    emit(b, {0x9C});                                              // pushfq
    emit(b, {0x50, 0x51, 0x52, 0x53, 0x55, 0x56, 0x57});          // push rax,rcx,rdx,rbx,rbp,rsi,rdi
    emit(b, {0x41, 0x50, 0x41, 0x51, 0x41, 0x52, 0x41, 0x53,      // push r8..r11
             0x41, 0x54, 0x41, 0x55, 0x41, 0x56, 0x41, 0x57});    // push r12..r15
    emit(b, {0x48, 0x89, 0xE5});                                  // mov rbp, rsp
    emit(b, {0x48, 0x83, 0xE4, 0xF0});                            // and rsp, -16
    emit(b, {0x48, 0x81, 0xEC, 0xA0, 0x00, 0x00, 0x00});          // sub rsp, 0xA0
    for (uint8_t i = 0; i < 6; i++)                               // movdqu [rsp+0x20+16i], xmm_i
        emit(b, {0xF3, 0x0F, 0x7F, (uint8_t)(0x44 | (i << 3)), 0x24, (uint8_t)(0x20 + 16 * i)});
    emit(b, {0x48, 0x89, 0xE9});                                  // mov rcx, rbp
    emit(b, {0x48, 0xB8}); emit_u64(b, handler);                  // mov rax, handler
    emit(b, {0xFF, 0xD0});                                        // call rax
    for (uint8_t i = 0; i < 6; i++)                               // movdqu xmm_i, [rsp+0x20+16i]
        emit(b, {0xF3, 0x0F, 0x6F, (uint8_t)(0x44 | (i << 3)), 0x24, (uint8_t)(0x20 + 16 * i)});
    emit(b, {0x48, 0x89, 0xEC});                                  // mov rsp, rbp
    emit(b, {0x41, 0x5F, 0x41, 0x5E, 0x41, 0x5D, 0x41, 0x5C,      // pop r15..r12
             0x41, 0x5B, 0x41, 0x5A, 0x41, 0x59, 0x41, 0x58});    // pop r11..r8
    emit(b, {0x5F, 0x5E, 0x5D, 0x5B, 0x5A, 0x59, 0x58});          // pop rdi,rsi,rbp,rbx,rdx,rcx,rax
    emit(b, {0x9D});                                              // popfq
    emit_jmp_abs(b, trampoline);
    return b;
}

// Suspend every other thread; fail if any has RIP inside [lo, hi). Returns handles to resume.
struct Freeze {
    std::vector<HANDLE> threads;
    bool ok = true;
    std::string why;
    Freeze(uintptr_t lo, uintptr_t hi) {
        DWORD me = GetCurrentThreadId(), pid = GetCurrentProcessId();
        HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
        if (snap == INVALID_HANDLE_VALUE) { ok = false; why = "snapshot failed"; return; }
        THREADENTRY32 te{}; te.dwSize = sizeof(te);
        // TWO PASSES: open every handle (allocating freely) BEFORE suspending anything -- a thread
        // suspended while holding the heap lock would deadlock the push_back (reviewed)
        std::vector<HANDLE> opened; opened.reserve(64);
        for (BOOL more = Thread32First(snap, &te); more; more = Thread32Next(snap, &te)) {
            if (te.th32OwnerProcessID != pid || te.th32ThreadID == me) continue;
            HANDLE h = OpenThread(THREAD_SUSPEND_RESUME | THREAD_GET_CONTEXT, FALSE, te.th32ThreadID);
            if (h) opened.push_back(h);
        }
        CloseHandle(snap);
        // NOTHING ALLOCATES OR FREES PAST THIS LINE until every thread is resumed: `opened`'s buffer
        // is handed to `threads` (so no destructor free either), suspended-but-failed handles are
        // closed without vector surgery, and push_back never reallocates (capacity == size). A free
        // while another thread holds the CRT heap lock deadlocks the process (reviewed).
        threads.swap(opened);                            // threads now owns the buffer; opened is empty
        size_t keep = 0;
        for (size_t i = 0; i < threads.size(); i++) {
            HANDLE h = threads[i];
            if (SuspendThread(h) == (DWORD)-1) { CloseHandle(h); continue; }
            threads[keep++] = h;
            CONTEXT c{}; c.ContextFlags = CONTEXT_CONTROL;
            if (GetThreadContext(h, &c) && c.Rip >= lo && c.Rip < hi) {
                ok = false; why = "a thread is executing inside the hook site";
            }
        }
        threads.resize(keep);                            // shrink only: no reallocation
    }
    ~Freeze() { for (HANDLE h : threads) { ResumeThread(h); CloseHandle(h); } }
};

// Install a hook. `expected` are the bytes that must be at the site (>= 14 bytes, whole
// instructions, relocatable). Retries the freeze a few times if a thread sits in the range.
inline bool install(Hook& h, uintptr_t target, const std::vector<uint8_t>& expected,
                    Handler handler, const char* name) {
    h.name = name; h.target = target; h.stolen = expected.size(); h.error.clear();
    if (h.stolen < 14) { h.error = "site must cover >= 14 bytes"; return false; }
    if (memcmp((void*)target, expected.data(), expected.size()) != 0) {
        h.error = "site bytes differ from the expected signature (patched binary?)";
        return false;
    }
    h.original.assign((uint8_t*)target, (uint8_t*)target + h.stolen);
    // trampoline: stolen bytes + jmp back
    std::vector<uint8_t> tr(h.original.begin(), h.original.end());
    emit_jmp_abs(tr, target + h.stolen);
    h.trampoline = alloc_exec(tr.size());
    if (!h.trampoline) { h.error = "trampoline alloc failed"; return false; }
    memcpy(h.trampoline, tr.data(), tr.size());
    std::vector<uint8_t> st = build_stub((uint64_t)handler, (uint64_t)h.trampoline);
    h.stub = alloc_exec(st.size());
    if (!h.stub) { h.error = "stub alloc failed"; return false; }
    memcpy(h.stub, st.data(), st.size());
    // the patch: jmp [rip+0]; dq stub; then int3-pad the rest of the stolen range
    std::vector<uint8_t> patch;
    emit_jmp_abs(patch, (uint64_t)h.stub);
    while (patch.size() < h.stolen) patch.push_back(0xCC);
    for (int attempt = 0; attempt < 20; attempt++) {
        Freeze fz(target, target + h.stolen);
        if (!fz.ok) { Sleep(5); continue; }
        DWORD old = 0;
        if (!VirtualProtect((void*)target, h.stolen, PAGE_EXECUTE_READWRITE, &old)) {
            h.error = "VirtualProtect failed"; return false;
        }
        memcpy((void*)target, patch.data(), patch.size());
        VirtualProtect((void*)target, h.stolen, old, &old);
        FlushInstructionCache(GetCurrentProcess(), (void*)target, h.stolen);
        h.active = true;
        return true;
    }
    h.error = "could not freeze threads outside the site";
    return false;
}

inline bool remove(Hook& h) {
    if (!h.active) return true;
    for (int attempt = 0; attempt < 20; attempt++) {
        Freeze fz(h.target, h.target + h.stolen);
        if (!fz.ok) { Sleep(5); continue; }
        DWORD old = 0;
        VirtualProtect((void*)h.target, h.stolen, PAGE_EXECUTE_READWRITE, &old);
        memcpy((void*)h.target, h.original.data(), h.stolen);
        VirtualProtect((void*)h.target, h.stolen, old, &old);
        FlushInstructionCache(GetCurrentProcess(), (void*)h.target, h.stolen);
        h.active = false;
        return true;
    }
    return false;
}

// Simple byte patch (for the spec 1.10 gates: force a predicate result at the call site).
inline bool patch_bytes(uintptr_t at, const std::vector<uint8_t>& expected,
                        const std::vector<uint8_t>& replacement, std::string* err = nullptr) {
    if (expected.size() != replacement.size()) { if (err) *err = "size mismatch"; return false; }
    if (memcmp((void*)at, expected.data(), expected.size()) != 0) {
        if (err) *err = "bytes differ from expected"; return false;
    }
    for (int attempt = 0; attempt < 20; attempt++) {
        Freeze fz(at, at + expected.size());
        if (!fz.ok) { Sleep(5); continue; }
        DWORD old = 0;
        if (!VirtualProtect((void*)at, expected.size(), PAGE_EXECUTE_READWRITE, &old)) {
            if (err) *err = "VirtualProtect failed"; return false;
        }
        memcpy((void*)at, replacement.data(), replacement.size());
        VirtualProtect((void*)at, expected.size(), old, &old);
        FlushInstructionCache(GetCurrentProcess(), (void*)at, expected.size());
        return true;
    }
    if (err) *err = "freeze failed";
    return false;
}

} // namespace detour
