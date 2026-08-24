// Proves detour.h outside the game: hooks a known 14-byte relocatable prologue, checks that the
// handler sees the live registers, that a register written by the handler reaches the
// trampolined original code, that flags/xmm survive, and that unhook restores the bytes.
#include <cstdio>
#include <cstdint>
#include <thread>
#include <atomic>
#include "detour.h"

// target: rax = rcx + rdx + r8, with 5 nops so the first 14 bytes are whole relocatable insns
extern "C" uint64_t testfn(uint64_t, uint64_t, uint64_t);
asm(R"(
.text
.globl testfn
testfn:
    mov %rcx, %rax
    add %rdx, %rax
    add %r8, %rax
    nop
    nop
    nop
    nop
    nop
    ret
)");

static std::atomic<int> g_calls{0};
static uint64_t g_seen_rcx = 0, g_seen_rdx = 0;
static void handler(detour::Regs* r) {
    g_calls++;
    if (r->rcx == 10) { g_seen_rcx = r->rcx; g_seen_rdx = r->rdx; }   // the test call, not the busy threads
    r->rcx += 100;                      // must reach the original code via the trampoline
}

int main() {
    int fails = 0;
    auto check = [&](bool ok, const char* what) { printf("  [%s] %s\n", ok ? "OK  " : "FAIL", what); if (!ok) fails++; };
    uint64_t base = testfn(1, 2, 3);
    check(base == 6, "unhooked: 1+2+3 == 6");
    // busy threads so the freeze path is exercised
    std::atomic<bool> stop{false};
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; i++) ts.emplace_back([&] { volatile uint64_t x = 0; while (!stop) x += testfn(1, 1, 1); });
    detour::Hook h;
    std::vector<uint8_t> expected{0x48, 0x89, 0xC8, 0x48, 0x01, 0xD0, 0x4C, 0x01, 0xC0,
                                  0x90, 0x90, 0x90, 0x90, 0x90};
    bool inst = detour::install(h, (uintptr_t)&testfn, expected, handler, "testfn");
    check(inst, inst ? "install" : h.error.c_str());
    double f = 1.5;                 // xmm survives the hook?
    uint64_t v = testfn(10, 20, 30);
    f *= 2.0;
    check(v == 160, "hooked: handler's rcx+=100 reached the original (10+100+20+30 == 160)");
    check(g_seen_rcx == 10 && g_seen_rdx == 20, "handler saw rcx=10, rdx=20");
    check(f == 3.0, "xmm state intact across the hook");
    check(g_calls.load() > 0, "handler called");
    stop = true; for (auto& t : ts) t.join();
    int before = g_calls.load();
    check(detour::remove(h), "unhook");
    testfn(1, 2, 3);
    check(g_calls.load() == before, "after unhook the handler no longer runs");
    check(testfn(1, 2, 3) == 6, "bytes restored: 1+2+3 == 6");
    // byte patch: replace the three adds' first byte sequence? use patch_bytes on the nops
    std::string err;
    check(detour::patch_bytes((uintptr_t)&testfn + 9, {0x90, 0x90, 0x90, 0x90, 0x90},
                              {0x48, 0xFF, 0xC0, 0x90, 0x90}, &err), "patch_bytes: inc rax over the nops");
    check(testfn(1, 2, 3) == 7, "patched code runs (== 7)");
    check(!detour::patch_bytes((uintptr_t)&testfn + 9, {0x90, 0x90, 0x90, 0x90, 0x90}, {0, 0, 0, 0, 0}, &err),
          "patch_bytes refuses when bytes differ from expected");
    printf("RESULT: %d failed\n", fails);
    return fails ? 1 : 0;
}
