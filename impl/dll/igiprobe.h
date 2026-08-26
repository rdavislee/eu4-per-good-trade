// IGI SNAPSHOT PROBE (spec 1.12 / test D1: the province-click trigger for the per-good view).
//
// The per-good view is selected today by the pgt.VIEW marker only. The player-facing trigger is a
// province click in trade map mode: the clicked province's trade good becomes the view. The engine
// keeps the selected province somewhere in the in-game interface object (IGI = *(G+0x1E00)) as a
// POINTER (a raw id search across three clicks found nothing; 2,561 bytes of the IGI changed),
// and that offset is UNKNOWN -- this probe finds it empirically: whenever the pgt.IGISNAP marker's
// content (a label) changes, walk every 8-byte field of the IGI (level 1) and of every object it
// points at (level 2), and record each pointee that reads like a CProvince (OFFSETS.md: +0x20 id,
// +0xE8 CTradeNode*). Click Toledo (219), label "a"; Andalucia (224), "b"; Madrid (217), "c"; the
// field that reads 219/224/217 across the three files is the selection.
//
// Runs from the FRAME hook (a paused game never ticks; clicking happens paused). Costs one file
// stat per frame while the marker exists, nothing otherwise; the walk itself is a one-off.
#pragma once
#include <windows.h>
#include <cstdint>
#include <fstream>
#include <string>
#include <vector>
#include "livetrade.h"

namespace igiprobe {

inline std::string g_last_label;
constexpr size_t IGI_BYTES = 0x6000;       // the interface object; generous
constexpr size_t L2_BYTES  = 0x800;        // how far into each level-1 pointee to look

inline bool looks_like_province(uintptr_t p, int* id_out) {
    if (!p || (p & 7) || !livetrade::validate_region(p, 0x100)) return false;
    int id = livetrade::fi(p + 0x20);
    if (id < 1 || id > 5000) return false;
    uintptr_t node = livetrade::fq(p + 0xE8);
    if (node && !livetrade::validate_region(node, 0x130)) return false;   // a province's node pointer must be readable if set
    *id_out = id;
    return true;
}

inline void frame(std::ofstream* lg) {
    if (!livetrade::marker_present("IGISNAP")) return;
    std::string label;
    { std::ifstream f(livetrade::self_dir() + "\\pgt.IGISNAP"); std::getline(f, label); }
    while (!label.empty() && (label.back() == '\r' || label.back() == '\n' || label.back() == ' ')) label.pop_back();
    if (label.empty() || label == g_last_label) return;
    g_last_label = label;
    uintptr_t g = livetrade::game_singleton();
    if (!g) return;
    uintptr_t igi = livetrade::validate_region(g + 0x1E00, 8) ? livetrade::fq(g + 0x1E00) : 0;
    if (!igi) return;
    std::ofstream out(livetrade::self_dir() + "\\igi_" + label + ".txt");
    int l1 = 0, l2 = 0;
    for (size_t off = 0; off + 8 <= IGI_BYTES; off += 8) {
        if (!livetrade::validate_region(igi + off, 8)) break;
        uintptr_t v = livetrade::fq(igi + off);
        int id = 0;
        if (looks_like_province(v, &id)) { out << "L1 " << std::hex << off << std::dec << " id=" << id << (char)10; l1++; }
        // level 2: v as an object holding a province pointer
        if (!v || (v & 7) || v == igi || !livetrade::validate_region(v, L2_BYTES)) continue;
        for (size_t o2 = 0; o2 + 8 <= L2_BYTES; o2 += 8) {
            uintptr_t w = livetrade::fq(v + o2);
            int id2 = 0;
            if (looks_like_province(w, &id2)) { out << "L2 " << std::hex << off << " " << o2 << std::dec << " id=" << id2 << (char)10; l2++; }
        }
    }
    if (lg) *lg << "  [igiprobe] snapshot '" << label << "': IGI=0x" << std::hex << igi << std::dec
                << " province-like pointees: level1=" << l1 << " level2=" << l2 << (char)10;
}

} // namespace igiprobe
