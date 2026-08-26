// IGI SNAPSHOT PROBE, two-phase (spec 1.12 / test D1: the province-click trigger for the per-good view).
//
// The per-good view is selected today by the pgt.VIEW marker only. The player-facing trigger is a
// province click in trade map mode: the clicked province's trade good becomes the view. The engine
// keeps the selected province somewhere in the in-game interface object (IGI = *(G+0x1E00)) as a
// POINTER (a raw id search across three clicks found nothing; 2,561 bytes of the IGI changed).
//
// Phase 1 (pgt.IGISNAP = label): dump the raw IGI bytes to igi_<label>.bin. Safe: it ran three
// times on 2026-08-26. Diff the dumps offline for 8-byte fields that changed between clicks and
// look like heap pointers -- those are the candidates.
// Phase 2 (pgt.IGIDEREF = label + hex offsets): for each candidate offset, dump 0x800 bytes of the
// object it points at, to igi_<label>_<off>.bin. Diff those for an int32 reading 219/224/217
// (CProvince+0x20 is the id, OFFSETS.md).
//
// The single-phase version walked EVERY pointer-like field of the IGI and 0x800 bytes of each
// pointee (~800k VirtualQuery calls on the render thread, in one frame) and the process died
// without a crash dump. Phase 2 reads a few dozen objects instead.
//
// Runs from the FRAME hook (a paused game never ticks; clicking happens paused). Costs one file
// stat per frame while a marker exists, nothing otherwise.
#pragma once
#include <windows.h>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "livetrade.h"

namespace igiprobe {

inline std::string g_last_snap, g_last_deref;
constexpr size_t IGI_BYTES = 0x6000;
constexpr size_t OBJ_BYTES = 0x800;

inline void dump(const std::string& path, uintptr_t base, size_t n) {
    std::vector<uint8_t> buf;
    for (size_t off = 0; off < n; off += 0x1000) {
        size_t chunk = (n - off < 0x1000) ? (n - off) : 0x1000;
        if (livetrade::validate_region(base + off, chunk)) buf.insert(buf.end(), (const uint8_t*)(base + off), (const uint8_t*)(base + off) + chunk);
        else buf.insert(buf.end(), chunk, 0xEE);
    }
    std::ofstream f(path, std::ios::binary);
    f.write((const char*)buf.data(), (std::streamsize)buf.size());
}

inline std::string marker_text(const char* name) {
    std::string t;
    std::ifstream f(livetrade::self_dir() + "\\pgt." + name);
    std::getline(f, t);
    while (!t.empty() && (t.back() == '\r' || t.back() == '\n' || t.back() == ' ')) t.pop_back();
    return t;
}

inline void frame(std::ofstream* lg) {
    uintptr_t g = livetrade::game_singleton();
    if (!g) return;
    uintptr_t igi = livetrade::validate_region(g + 0x1E00, 8) ? livetrade::fq(g + 0x1E00) : 0;
    if (!igi) return;
    std::string dir = livetrade::self_dir() + "\\";
    if (livetrade::marker_present("IGISNAP")) {
        std::string label = marker_text("IGISNAP");
        if (!label.empty() && label != g_last_snap) {
            g_last_snap = label;
            dump(dir + "igi_" + label + ".bin", igi, IGI_BYTES);
            if (lg) *lg << "  [igiprobe] phase 1 '" << label << "': IGI=0x" << std::hex << igi << std::dec << " " << IGI_BYTES << " bytes" << (char)10;
        }
    }
    if (livetrade::marker_present("IGIDEREF")) {
        std::string spec = marker_text("IGIDEREF");       // "<label> <hexoff> <hexoff> ..."
        if (!spec.empty() && spec != g_last_deref) {
            g_last_deref = spec;
            std::istringstream ss(spec);
            std::string label; ss >> label;
            std::string tok; int done = 0;
            while (ss >> tok) {
                size_t off = (size_t)strtoull(tok.c_str(), nullptr, 16);
                if (off + 8 > IGI_BYTES || !livetrade::validate_region(igi + off, 8)) continue;
                uintptr_t v = livetrade::fq(igi + off);
                if (!v || (v & 7)) continue;
                dump(dir + "igi_" + label + "_" + tok + ".bin", v, OBJ_BYTES);
                done++;
            }
            if (lg) *lg << "  [igiprobe] phase 2 '" << label << "': " << done << " pointees dumped" << (char)10;
        }
    }
}

} // namespace igiprobe
