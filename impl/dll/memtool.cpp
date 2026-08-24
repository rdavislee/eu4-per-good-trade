// Live memory tool for the reverse-engineering session (spec 2.7 / 2.9 memory track). Attaches
// to eu4.exe from outside and reads/scans its address space, so the trade structures can be
// located by VALUE SCANNING: the readable save gives the exact node values the live fields hold
// at a known state (e.g. african_great_lakes total=121.051), and searching committed memory for
// those doubles/floats finds the structure without any symbols.
//
//   memtool proc                         find eu4.exe (pid, module base, image size)
//   memtool scan-double <v> [tol] [max]  addresses holding double ~= v (default tol 1e-4)
//   memtool scan-float  <v> [tol] [max]  addresses holding float  ~= v
//   memtool scan-doubles v1,v2,v3 [span] addresses where those doubles appear within `span` bytes
//                                        of each other (a struct signature -- far fewer hits)
//   memtool read  <addr> <n>             hex+float dump of n bytes at addr
//   memtool rdump <addr> <n> f64|f32|u32 typed dump
//   memtool pattern "<AA BB ?? CC>"      byte-pattern scan of the module image
//   memtool str "<literal>"              ASCII-string scan of the module image
//   memtool write-double <addr> <v>      poke a double (use with care; RE only)
//
// Build: g++ -O2 -std=c++17 -o memtool.exe memtool.cpp -lpsapi
#include <windows.h>
#include <psapi.h>
#include <tlhelp32.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <string>
#include <vector>

static DWORD find_pid(const char* name) {
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 pe{}; pe.dwSize = sizeof(pe);
    DWORD pid = 0;
    if (Process32First(snap, &pe)) {
        do {
            if (_stricmp(pe.szExeFile, name) == 0) { pid = pe.th32ProcessID; break; }
        } while (Process32Next(snap, &pe));
    }
    CloseHandle(snap);
    return pid;
}

static bool module_info(DWORD pid, uintptr_t& base, size_t& size) {
    HANDLE h = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
    if (!h) return false;
    HMODULE mods[1024]; DWORD needed;
    bool ok = false;
    if (EnumProcessModules(h, mods, sizeof(mods), &needed)) {
        MODULEINFO mi{};
        if (GetModuleInformation(h, mods[0], &mi, sizeof(mi))) {
            base = reinterpret_cast<uintptr_t>(mi.lpBaseOfDll);
            size = mi.SizeOfImage;
            ok = true;
        }
    }
    CloseHandle(h);
    return ok;
}

static HANDLE open_rw(DWORD pid) {
    return OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ | PROCESS_VM_WRITE |
                       PROCESS_VM_OPERATION, FALSE, pid);
}

// walk committed, readable regions and hand each buffer to `fn`
template <class F>
static void walk_regions(HANDLE h, F fn) {
    MEMORY_BASIC_INFORMATION mbi{};
    uintptr_t addr = 0;
    std::vector<uint8_t> buf;
    while (VirtualQueryEx(h, reinterpret_cast<void*>(addr), &mbi, sizeof(mbi)) == sizeof(mbi)) {
        uintptr_t region = reinterpret_cast<uintptr_t>(mbi.BaseAddress);
        size_t rsize = mbi.RegionSize;
        bool readable = (mbi.State == MEM_COMMIT) &&
                        (mbi.Protect & (PAGE_READONLY | PAGE_READWRITE | PAGE_WRITECOPY |
                                        PAGE_EXECUTE_READ | PAGE_EXECUTE_READWRITE)) &&
                        !(mbi.Protect & PAGE_GUARD);
        if (readable && rsize > 0) {
            buf.resize(rsize);
            SIZE_T got = 0;
            if (ReadProcessMemory(h, mbi.BaseAddress, buf.data(), rsize, &got) && got > 0)
                fn(region, buf.data(), got);
        }
        addr = region + rsize;
        if (addr <= region) break;   // overflow guard
    }
}

static int cmd_proc() {
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe NOT running\n"); return 1; }
    uintptr_t base = 0; size_t size = 0;
    if (!module_info(pid, base, size)) { printf("pid %lu but module info failed (elevation?)\n", pid); return 1; }
    printf("eu4.exe pid=%lu base=0x%llx size=%zu (0x%zx)\n", pid, (unsigned long long)base, size, size);
    return 0;
}

static int scan_val(int argc, char** argv, bool is_float) {
    if (argc < 3) { printf("need value\n"); return 2; }
    double target = atof(argv[2]);
    double tol = argc > 3 ? atof(argv[3]) : 1e-4;
    int maxhits = argc > 4 ? atoi(argv[4]) : 40;
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed %lu\n", GetLastError()); return 1; }
    int hits = 0;
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t n) {
        if (hits >= maxhits) return;
        if (is_float) {
            for (size_t i = 0; i + 4 <= n; i += 4) {
                float f; memcpy(&f, data + i, 4);
                if (std::isfinite(f) && std::fabs(double(f) - target) <= tol) {
                    printf("0x%llx  f32 %.6f\n", (unsigned long long)(region + i), f);
                    if (++hits >= maxhits) return;
                }
            }
        } else {
            for (size_t i = 0; i + 8 <= n; i += 4) {   // 4-byte stride catches unaligned doubles
                double d; memcpy(&d, data + i, 8);
                if (std::isfinite(d) && std::fabs(d - target) <= tol) {
                    printf("0x%llx  f64 %.6f\n", (unsigned long long)(region + i), d);
                    if (++hits >= maxhits) return;
                }
            }
        }
    });
    printf("(%d hits%s)\n", hits, hits >= maxhits ? ", capped" : "");
    CloseHandle(h);
    return 0;
}

// several doubles appearing within `span` bytes of each other -> a struct fingerprint
static int scan_doubles(int argc, char** argv) {
    if (argc < 3) { printf("need comma-separated values\n"); return 2; }
    std::vector<double> vals;
    { char* s = argv[2]; char* tok = strtok(s, ","); while (tok) { vals.push_back(atof(tok)); tok = strtok(nullptr, ","); } }
    size_t span = argc > 3 ? size_t(atoll(argv[3])) : 256;
    double tol = argc > 4 ? atof(argv[4]) : 1e-3;
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed\n"); return 1; }
    int hits = 0;
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t n) {
        if (hits >= 40) return;
        // find every offset of the first value, then check the others are within span
        for (size_t i = 0; i + 8 <= n; i += 4) {
            double d; memcpy(&d, data + i, 8);
            if (!(std::isfinite(d) && std::fabs(d - vals[0]) <= tol)) continue;
            size_t lo = i > span ? i - span : 0;
            size_t hi = i + span + 8 < n ? i + span + 8 : n;
            bool all = true;
            for (size_t k = 1; k < vals.size(); k++) {
                bool found = false;
                for (size_t j = lo; j + 8 <= hi; j += 4) {
                    double e; memcpy(&e, data + j, 8);
                    if (std::isfinite(e) && std::fabs(e - vals[k]) <= tol) { found = true; break; }
                }
                if (!found) { all = false; break; }
            }
            if (all) {
                printf("0x%llx  anchor %.6f + %zu more within %zu bytes\n",
                       (unsigned long long)(region + i), d, vals.size() - 1, span);
                if (++hits >= 40) return;
            }
        }
    });
    printf("(%d struct-fingerprint hits)\n", hits);
    CloseHandle(h);
    return 0;
}

// several FLOATS appearing within `span` bytes of each other -> a float-struct fingerprint
static int scan_floats(int argc, char** argv) {
    if (argc < 3) { printf("need comma-separated values\n"); return 2; }
    std::vector<double> vals;
    { char* s = argv[2]; char* tok = strtok(s, ","); while (tok) { vals.push_back(atof(tok)); tok = strtok(nullptr, ","); } }
    size_t span = argc > 3 ? size_t(atoll(argv[3])) : 256;
    double tol = argc > 4 ? atof(argv[4]) : 0.02;
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed\n"); return 1; }
    int hits = 0;
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t n) {
        if (hits >= 40) return;
        for (size_t i = 0; i + 4 <= n; i += 4) {
            float f; memcpy(&f, data + i, 4);
            if (!(std::isfinite(f) && std::fabs(double(f) - vals[0]) <= tol)) continue;
            size_t lo = i > span ? i - span : 0;
            size_t hi = i + span + 4 < n ? i + span + 4 : n;
            bool all = true;
            for (size_t k = 1; k < vals.size(); k++) {
                bool found = false;
                for (size_t j = lo; j + 4 <= hi; j += 4) {
                    float e; memcpy(&e, data + j, 4);
                    if (std::isfinite(e) && std::fabs(double(e) - vals[k]) <= tol) { found = true; break; }
                }
                if (!found) { all = false; break; }
            }
            if (all) {
                printf("0x%llx  anchor %.4f + %zu more within %zu bytes\n",
                       (unsigned long long)(region + i), double(f), vals.size() - 1, span);
                if (++hits >= 40) return;
            }
        }
    });
    printf("(%d f32-fingerprint hits)\n", hits);
    CloseHandle(h);
    return 0;
}

// scanlist <val> <tol> <outfile> [f64]: uncapped scan, write every matching address (+ value)
static int cmd_scanlist(int argc, char** argv) {
    if (argc < 5) { printf("need val tol outfile\n"); return 2; }
    double val = atof(argv[2]); double tol = atof(argv[3]);
    bool f64 = argc > 5 && !strcmp(argv[5], "f64");
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed\n"); return 1; }
    FILE* out = fopen(argv[4], "w");
    long n = 0;
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t sz) {
        size_t step = 4;
        for (size_t i = 0; i + (f64 ? 8 : 4) <= sz; i += step) {
            double v;
            if (f64) { double d; memcpy(&d, data + i, 8); v = d; }
            else { float f; memcpy(&f, data + i, 4); v = f; }
            if (std::isfinite(v) && std::fabs(v - val) <= tol) {
                fprintf(out, "%llx\n", (unsigned long long)(region + i)); n++;
            }
        }
    });
    fclose(out); CloseHandle(h);
    printf("scanlist: %ld addresses -> %s\n", n, argv[4]);
    return 0;
}

// refine <infile> <val> <tol> <outfile> [f64]: keep addresses whose CURRENT value ~= val
static int cmd_refine(int argc, char** argv) {
    if (argc < 6) { printf("need infile val tol outfile\n"); return 2; }
    double val = atof(argv[3]); double tol = atof(argv[4]);
    bool f64 = argc > 6 && !strcmp(argv[6], "f64");
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed\n"); return 1; }
    FILE* in = fopen(argv[2], "r"); if (!in) { printf("cannot open %s\n", argv[2]); return 1; }
    FILE* out = fopen(argv[5], "w");
    char line[64]; long kept = 0, total = 0;
    while (fgets(line, sizeof(line), in)) {
        uintptr_t addr = strtoull(line, nullptr, 16); if (!addr) continue;
        total++;
        uint8_t buf[8]; SIZE_T got = 0;
        if (!ReadProcessMemory(h, (void*)addr, buf, f64 ? 8 : 4, &got) || got < (f64 ? 8u : 4u)) continue;
        double v; if (f64) { double d; memcpy(&d, buf, 8); v = d; } else { float f; memcpy(&f, buf, 4); v = f; }
        if (std::isfinite(v) && std::fabs(v - val) <= tol) { fprintf(out, "%llx\n", (unsigned long long)addr); kept++; }
    }
    fclose(in); fclose(out); CloseHandle(h);
    printf("refine: kept %ld of %ld -> %s\n", kept, total, argv[5]);
    return 0;
}

// dumplist <infile> [f64]: print current value at each address (for eyeballing survivors)
static int cmd_dumplist(int argc, char** argv) {
    if (argc < 3) { printf("need infile\n"); return 2; }
    bool f64 = argc > 3 && !strcmp(argv[3], "f64");
    DWORD pid = find_pid("eu4.exe"); if (!pid) { printf("not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    FILE* in = fopen(argv[2], "r"); if (!in) return 1;
    char line[64];
    while (fgets(line, sizeof(line), in)) {
        uintptr_t addr = strtoull(line, nullptr, 16); if (!addr) continue;
        uint8_t buf[8]; SIZE_T got = 0;
        if (ReadProcessMemory(h, (void*)addr, buf, f64 ? 8 : 4, &got)) {
            double v; if (f64) { double d; memcpy(&d, buf, 8); v = d; } else { float f; memcpy(&f, buf, 4); v = f; }
            printf("0x%llx = %.5f\n", (unsigned long long)addr, v);
        }
    }
    fclose(in); CloseHandle(h);
    return 0;
}

// snap <infile> <snapfile> [f64]: record current value at each candidate address
static int cmd_snap(int argc, char** argv) {
    if (argc < 4) { printf("need infile snapfile\n"); return 2; }
    bool f64 = argc > 4 && !strcmp(argv[4], "f64");
    DWORD pid = find_pid("eu4.exe"); if (!pid) { printf("not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    FILE* in = fopen(argv[2], "r"); if (!in) return 1;
    FILE* out = fopen(argv[3], "w");
    char line[64]; long n = 0;
    while (fgets(line, sizeof(line), in)) {
        uintptr_t addr = strtoull(line, nullptr, 16); if (!addr) continue;
        uint8_t buf[8]; SIZE_T got = 0;
        if (!ReadProcessMemory(h, (void*)addr, buf, f64 ? 8 : 4, &got)) continue;
        double v; if (f64) { double d; memcpy(&d, buf, 8); v = d; } else { float f; memcpy(&f, buf, 4); v = f; }
        fprintf(out, "%llx %.9g\n", (unsigned long long)addr, v); n++;
    }
    fclose(in); fclose(out); CloseHandle(h);
    printf("snap: %ld addresses -> %s\n", n, argv[3]);
    return 0;
}

// keepchanged/keepsame <snapfile> <tol> <outfile> [f64]: filter by whether current value moved
static int cmd_keep(int argc, char** argv, bool want_changed) {
    if (argc < 5) { printf("need snapfile tol outfile\n"); return 2; }
    double tol = atof(argv[3]);
    bool f64 = argc > 5 && !strcmp(argv[5], "f64");
    DWORD pid = find_pid("eu4.exe"); if (!pid) { printf("not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    FILE* in = fopen(argv[2], "r"); if (!in) return 1;
    FILE* out = fopen(argv[4], "w");
    char line[128]; long kept = 0, total = 0;
    while (fgets(line, sizeof(line), in)) {
        uintptr_t addr; double snapval;
        if (sscanf(line, "%llx %lf", (unsigned long long*)&addr, &snapval) != 2) continue;
        total++;
        uint8_t buf[8]; SIZE_T got = 0;
        if (!ReadProcessMemory(h, (void*)addr, buf, f64 ? 8 : 4, &got)) continue;
        double v; if (f64) { double d; memcpy(&d, buf, 8); v = d; } else { float f; memcpy(&f, buf, 4); v = f; }
        if (!std::isfinite(v)) continue;
        bool changed = std::fabs(v - snapval) > tol;
        if (changed == want_changed) { fprintf(out, "%llx %.9g\n", (unsigned long long)addr, v); kept++; }
    }
    fclose(in); fclose(out); CloseHandle(h);
    printf("%s: kept %ld of %ld -> %s\n", want_changed ? "keepchanged" : "keepsame", kept, total, argv[4]);
    return 0;
}

static int cmd_read(int argc, char** argv, const char* type) {
    if (argc < 4) { printf("need addr and len\n"); return 2; }
    uintptr_t addr = strtoull(argv[2], nullptr, 0);
    size_t n = strtoull(argv[3], nullptr, 0);
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed\n"); return 1; }
    std::vector<uint8_t> buf(n);
    SIZE_T got = 0;
    if (!ReadProcessMemory(h, reinterpret_cast<void*>(addr), buf.data(), n, &got)) {
        printf("read failed %lu\n", GetLastError()); CloseHandle(h); return 1;
    }
    if (type && strcmp(type, "f64") == 0) {
        for (size_t i = 0; i + 8 <= got; i += 8) {
            double d; memcpy(&d, buf.data() + i, 8);
            printf("0x%llx +%03zu  f64 %.6f\n", (unsigned long long)(addr + i), i, d);
        }
    } else if (type && strcmp(type, "f32") == 0) {
        for (size_t i = 0; i + 4 <= got; i += 4) {
            float f; memcpy(&f, buf.data() + i, 4);
            printf("0x%llx +%03zu  f32 %.6f\n", (unsigned long long)(addr + i), i, f);
        }
    } else if (type && strcmp(type, "u32") == 0) {
        for (size_t i = 0; i + 4 <= got; i += 4) {
            uint32_t u; memcpy(&u, buf.data() + i, 4);
            printf("0x%llx +%03zu  u32 %u  0x%08x\n", (unsigned long long)(addr + i), i, u, u);
        }
    } else {
        for (size_t i = 0; i < got; i += 16) {
            printf("0x%llx  ", (unsigned long long)(addr + i));
            for (size_t j = 0; j < 16 && i + j < got; j++) printf("%02x ", buf[i + j]);
            printf(" ");
            for (size_t j = 0; j < 16 && i + j < got; j++) {
                uint8_t c = buf[i + j];
                printf("%c", (c >= 32 && c < 127) ? c : '.');
            }
            printf("\n");
        }
    }
    CloseHandle(h);
    return 0;
}

// find a base where val[k] ~= f32 at base + k*stride for all k -> locates a float array in
// node order. Tries the given stride, or a set of common strides if stride==0.
static int cmd_fseq(int argc, char** argv) {
    if (argc < 3) { printf("need v1,v2,...\n"); return 2; }
    std::vector<double> vals;
    { char* s = argv[2]; char* tok = strtok(s, ","); while (tok) { vals.push_back(atof(tok)); tok = strtok(nullptr, ","); } }
    std::vector<int> strides;
    if (argc > 3 && atoi(argv[3]) > 0) strides = {atoi(argv[3])};
    else strides = {4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 64, 80, 96, 128, 160, 192, 256};
    double tol = argc > 4 ? atof(argv[4]) : 0.01;
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed\n"); return 1; }
    int hits = 0;
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t n) {
        if (hits >= 20) return;
        for (size_t i = 0; i + 4 <= n; i += 4) {
            float f; memcpy(&f, data + i, 4);
            if (!(std::isfinite(f) && std::fabs(double(f) - vals[0]) <= tol)) continue;
            for (int st : strides) {
                if (i + size_t(st) * (vals.size() - 1) + 4 > n) continue;
                bool all = true;
                for (size_t k = 1; k < vals.size(); k++) {
                    float e; memcpy(&e, data + i + size_t(st) * k, 4);
                    if (!(std::isfinite(e) && std::fabs(double(e) - vals[k]) <= tol)) { all = false; break; }
                }
                if (all) {
                    printf("0x%llx  stride=%d  (%zu values)\n",
                           (unsigned long long)(region + i), st, vals.size());
                    if (++hits >= 20) return;
                    break;
                }
            }
        }
    });
    printf("(%d sequence hits)\n", hits);
    CloseHandle(h);
    return 0;
}

// find every offset within +/-radius of addr holding a float ~= val -> reveals array stride
static int cmd_near(int argc, char** argv) {
    if (argc < 4) { printf("need addr val [radius] [tol]\n"); return 2; }
    uintptr_t addr = strtoull(argv[2], nullptr, 0);
    double val = atof(argv[3]);
    long radius = argc > 4 ? atol(argv[4]) : 4096;
    double tol = argc > 5 ? atof(argv[5]) : 0.02;
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed\n"); return 1; }
    size_t n = 2 * radius;
    std::vector<uint8_t> buf(n);
    SIZE_T got = 0;
    ReadProcessMemory(h, reinterpret_cast<void*>(addr - radius), buf.data(), n, &got);
    for (size_t i = 0; i + 4 <= got; i += 4) {
        float f; memcpy(&f, buf.data() + i, 4);
        if (std::isfinite(f) && std::fabs(double(f) - val) <= tol) {
            long off = long(i) - radius;
            printf("  %+ld  (0x%llx)  f32 %.4f\n", off, (unsigned long long)(addr + off), f);
        }
    }
    CloseHandle(h);
    return 0;
}

static int cmd_write_double(int argc, char** argv) {
    if (argc < 4) { printf("need addr and value\n"); return 2; }
    uintptr_t addr = strtoull(argv[2], nullptr, 0);
    double v = atof(argv[3]);
    DWORD pid = find_pid("eu4.exe");
    if (!pid) { printf("eu4.exe not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    if (!h) { printf("OpenProcess failed\n"); return 1; }
    SIZE_T wrote = 0;
    bool ok = WriteProcessMemory(h, reinterpret_cast<void*>(addr), &v, 8, &wrote);
    printf("%s wrote %.6f to 0x%llx\n", ok ? "OK" : "FAIL", v, (unsigned long long)addr);
    CloseHandle(h);
    return ok ? 0 : 1;
}

// scanstr <string> [max]: find an ASCII byte string in committed memory (node names etc.)
static int cmd_scanstr(int argc, char** argv) {
    if (argc < 3) { printf("need string\n"); return 2; }
    std::string needle = argv[2];
    int maxhits = argc > 3 ? atoi(argv[3]) : 40;
    DWORD pid = find_pid("eu4.exe"); if (!pid) { printf("not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    int hits = 0;
    size_t n = needle.size();
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t sz) {
        if (hits >= maxhits) return;
        for (size_t i = 0; i + n <= sz; i++) {
            if (memcmp(data + i, needle.data(), n) == 0) {
                // print a bit of context (is it null-terminated / inline?)
                char after = (i + n < sz) ? char(data[i + n]) : '?';
                printf("0x%llx  after=0x%02x('%c')\n", (unsigned long long)(region + i),
                       (unsigned char)after, (after >= 32 && after < 127) ? after : '.');
                if (++hits >= maxhits) return;
            }
        }
    });
    printf("(%d hits)\n", hits);
    CloseHandle(h);
    return 0;
}

// scanptr <hexval> [max]: find 8-byte little-endian pointers equal to hexval (e.g. a vtable VA)
static int cmd_scanptr(int argc, char** argv) {
    if (argc < 3) { printf("need hexval\n"); return 2; }
    uint64_t want = strtoull(argv[2], nullptr, 0);
    int maxhits = argc > 3 ? atoi(argv[3]) : 200;
    DWORD pid = find_pid("eu4.exe"); if (!pid) { printf("not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    int hits = 0;
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t sz) {
        if (hits >= maxhits) return;
        for (size_t i = 0; i + 8 <= sz; i += 8) {   // 8-aligned (objects are pointer-aligned)
            uint64_t v; memcpy(&v, data + i, 8);
            if (v == want) {
                printf("0x%llx\n", (unsigned long long)(region + i));
                if (++hits >= maxhits) return;
            }
        }
    });
    printf("(%d objects with that vtable)\n", hits);
    CloseHandle(h);
    return 0;
}

// findnode: scan heap for the runtime CTradeNode signature from the serializer --
//   [O+0xF8] = heap ptr P;  [O+0xA0] = heap ptr;  [P+0xB4] = int in [0, 2e6] (local_value*1000)
// Reports O and the decoded local_value. There should be ~80 (the trade nodes).
static int cmd_findnode(int argc, char** argv) {
    DWORD pid = find_pid("eu4.exe"); if (!pid) { printf("not running\n"); return 1; }
    uintptr_t mbase = 0; size_t msize = 0; module_info(pid, mbase, msize);
    HANDLE h = open_rw(pid);
    const uint64_t HMIN = 0x2c000000000ULL, HMAX = 0x2c200000000ULL;
    uint64_t MBASE = mbase, MEND = mbase + msize;
    int found = 0;
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t sz) {
        if (found >= 3000) return;
        for (size_t i = 0; i + 0x170 <= sz; i += 8) {
            uint64_t vt, f8, a0;
            memcpy(&vt, data + i + 0x00, 8);
            if (!(vt >= MBASE && vt < MEND)) continue;         // vtable in eu4.exe
            memcpy(&f8, data + i + 0xF8, 8);
            memcpy(&a0, data + i + 0xA0, 8);
            if (!(f8 >= HMIN && f8 < HMAX && a0 >= HMIN && a0 < HMAX)) continue;
            int32_t lv; SIZE_T got = 0;
            if (!ReadProcessMemory(h, (void*)(f8 + 0xB4), &lv, 4, &got) || got < 4) continue;
            if (lv < 100 || lv > 500000) continue;   // 0.1 .. 500 ducats: real node local_value
            printf("0x%llx  vt=eu4+0x%llx  sub=0x%llx  local_value=%.3f\n",
                   (unsigned long long)(region + i), (unsigned long long)(vt - MBASE),
                   (unsigned long long)f8, lv / 1000.0);
            if (++found >= 3000) return;
        }
    });
    printf("(%d runtime-node candidates)\n", found);
    CloseHandle(h);
    return 0;
}

// nodes: enumerate the live trade nodes via the CTradeNodeDefinition vtable (eu4.exe+0x1C439D0)
// and read each object's inline-std::string name at +0x10. Demonstrates the DLL's live read path
// against the running game (build 835bfdf8). RESOLVED seam, not a scan for unknown values.
static int cmd_nodes(int argc, char** argv) {
    DWORD pid = find_pid("eu4.exe"); if (!pid) { printf("not running\n"); return 1; }
    uintptr_t mbase = 0; size_t msize = 0; module_info(pid, mbase, msize);
    uint64_t defvt = mbase + 0x1C439D0;
    HANDLE h = open_rw(pid);
    std::vector<std::string> names;
    walk_regions(h, [&](uintptr_t region, const uint8_t* data, size_t sz) {
        for (size_t i = 0; i + 0x30 <= sz; i += 8) {
            uint64_t v; memcpy(&v, data + i, 8);
            if (v != defvt) continue;
            char nm[17] = {0}; memcpy(nm, data + i + 0x10, 16);
            std::string s(nm, strnlen(nm, 16));
            if (!s.empty() && s.find_first_not_of("abcdefghijklmnopqrstuvwxyz_") == std::string::npos)
                names.push_back(s);
        }
    });
    // distinct, sorted
    std::sort(names.begin(), names.end());
    std::vector<std::string> uniq;
    for (auto& n : names) if (uniq.empty() || uniq.back() != n) uniq.push_back(n);
    printf("live trade nodes via CTradeNodeDefinition vtable (eu4.exe+0x1C439D0):\n");
    int col = 0;
    for (auto& n : uniq) { printf("%-22s", n.c_str()); if (++col % 4 == 0) printf("\n"); }
    printf("\n(%zu distinct node names, %zu objects)\n", uniq.size(), names.size());
    CloseHandle(h);
    return 0;
}

static int cmd_write_float(int argc, char** argv) {
    if (argc < 4) { printf("need addr and value\n"); return 2; }
    uintptr_t addr = strtoull(argv[2], nullptr, 0);
    float v = (float)atof(argv[3]);
    DWORD pid = find_pid("eu4.exe"); if (!pid) { printf("not running\n"); return 1; }
    HANDLE h = open_rw(pid);
    SIZE_T wrote = 0;
    bool ok = WriteProcessMemory(h, (void*)addr, &v, 4, &wrote);
    printf("%s wrote %.4f to 0x%llx\n", ok ? "OK" : "FAIL", v, (unsigned long long)addr);
    CloseHandle(h);
    return ok ? 0 : 1;
}

int main(int argc, char** argv) {
    if (argc < 2) { printf("usage: memtool proc|scan-double|scan-float|scan-doubles|read|rdump|write-double ...\n"); return 2; }
    std::string c = argv[1];
    if (c == "proc") return cmd_proc();
    if (c == "scan-double") return scan_val(argc, argv, false);
    if (c == "scan-float") return scan_val(argc, argv, true);
    if (c == "scan-doubles") return scan_doubles(argc, argv);
    if (c == "scan-floats") return scan_floats(argc, argv);
    if (c == "read") return cmd_read(argc, argv, "hex");
    if (c == "rdump") return cmd_read(argc, argv, argc > 4 ? argv[4] : "f64");
    if (c == "scanlist") return cmd_scanlist(argc, argv);
    if (c == "refine") return cmd_refine(argc, argv);
    if (c == "dumplist") return cmd_dumplist(argc, argv);
    if (c == "snap") return cmd_snap(argc, argv);
    if (c == "keepchanged") return cmd_keep(argc, argv, true);
    if (c == "keepsame") return cmd_keep(argc, argv, false);
    if (c == "fseq") return cmd_fseq(argc, argv);
    if (c == "near") return cmd_near(argc, argv);
    if (c == "write-double") return cmd_write_double(argc, argv);
    if (c == "write-float") return cmd_write_float(argc, argv);
    if (c == "scanstr") return cmd_scanstr(argc, argv);
    if (c == "scanptr") return cmd_scanptr(argc, argv);
    if (c == "findnode") return cmd_findnode(argc, argv);
    if (c == "nodes") return cmd_nodes(argc, argv);
    printf("unknown command %s\n", c.c_str());
    return 2;
}
