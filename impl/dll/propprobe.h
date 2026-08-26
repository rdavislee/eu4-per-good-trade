// PROPAGATION PROBE -- measures vanilla's transfer rule on the engine's own records before the
// per-good departure (impl/DEPARTURES.md) reimplements it per good.
//
// Spec 1.9: a country's PROVINCIAL power at node m, if >= TRADE_PROPAGATE_THRESHOLD (2), sends
// 1/TRADE_PROPAGATE_DIVIDER (1/5) of it one hop upstream, no merchant condition, summed at the
// receiver. MEASURED 2026-08-26: rec+0x50/+0x54 are NOT that -- they pair between countries at
// the SAME node (english_channel: #140 t_out 4.39 + #146 t_out 5.43 == #668 t_in 9.82; a subject's
// transfer to its overlord, cf. +0xAF has_subject). The Phi_w propagation is folded into
// val (+0x48), which exceeds province_power (+0x28) by the propagated + bonus amount.
//
// So this probe tests the DECOMPOSITION of val:
//   val(n,c) ?= province_power(n,c) + 2*has_trader + ship_power(+0x1C) + t_in - t_out + prop_in(n,c)
//   prop_in(n,c) = sum over m downstream of n:  pp(m,c) >= 2 ? pp(m,c)/5 : 0        [FULL]
//                                          or:  .../updeg(m)                          [DIVIDED]
// and reports how many records close under each variant (within 1% + 0.005), plus the largest
// residuals, so the departure can rebuild power from parts with a measured error bar.
#pragma once
#include <cstdint>
#include <cmath>
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"

namespace propprobe {

inline void run(const std::vector<livetrade::SimNode>& sim, std::ofstream& lg) {
    std::map<uintptr_t, int> def_to_id; std::map<int, uintptr_t> id_to_obj;
    for (auto& s : sim) { if (!s.obj || !livetrade::validate_region(s.obj + 0xA8, 8)) continue; uintptr_t d = livetrade::fq(s.obj + 0xA8); if (d) { def_to_id[d] = s.index; id_to_obj[s.index] = s.obj; } }
    std::map<int, std::vector<int>> down; std::map<int, int> updeg;
    for (auto& s : sim) {
        if (!s.obj) continue;
        uintptr_t d = livetrade::fq(s.obj + 0xA8);
        if (!d || !livetrade::validate_region(d + 0x80, 0x30)) continue;
        updeg[s.index] = (int)((livetrade::fq(d + 0x88) - livetrade::fq(d + 0x80)) / 8);
        uintptr_t ob = livetrade::fq(d + 0x98), oe = livetrade::fq(d + 0xA0);
        for (uintptr_t e = ob; ob && oe > ob && e + 0x78 <= oe; e += 0x78) {
            if (!livetrade::validate_region(e, 0x78) || livetrade::fq(e + 0x58) == 0) continue;
            uintptr_t t = livetrade::fq(e + 0x30); auto it = def_to_id.find(t);
            if (it != def_to_id.end()) down[s.index].push_back(it->second);
        }
    }
    auto rec_of = [&](uintptr_t node, int cidx) -> uintptr_t {
        if (!node || !livetrade::validate_region(node + 0x18, 16)) return 0;
        uintptr_t rb = livetrade::fq(node + 0x18); int rc = livetrade::fi(node + 0x24);
        if (!rb || cidx < 0 || cidx >= rc) return 0;
        uintptr_t r = rb + (uintptr_t)cidx * 0xC0;
        if (!livetrade::validate_region(r, 0xC0)) return 0;
        if ((livetrade::fi(r + 0x14) & 0xFFFF) != cidx) return 0;
        return r;
    };
    auto f = [](uintptr_t r, int off) { return livetrade::fi(r + off) / 1000.0; };
    int n_tested = 0, close_full = 0, close_div = 0, close_none = 0, close_noprop = 0, samples = 0, clean = 0, clean_full = 0, clean_div = 0, clean_none = 0, clean_samples = 0;
    double worst_full = 0, worst_div = 0; std::string worst_name;
    for (auto& s : sim) {
        uintptr_t node = s.obj; if (!node || !livetrade::validate_region(node + 0x18, 16)) continue;
        int rc = livetrade::fi(node + 0x24);
        for (int c = 0; c < rc && c < 4096; c++) {
            uintptr_t r = rec_of(node, c); if (!r) continue;
            double val = f(r, 0x48), pp = f(r, 0x28), ship = f(r, 0x1C), t_out = f(r, 0x50), t_in = f(r, 0x54);
            int has_trader = livetrade::fb(r + 0xAE);
            if (val <= 0.0005) continue;
            double prop_full = 0, prop_div = 0;
            for (int m : down[s.index]) {
                uintptr_t rm = rec_of(id_to_obj[m], c); if (!rm) continue;
                double ppm = f(rm, 0x28);
                if (ppm >= 2.0) { prop_full += ppm / 5.0; int ud = updeg[m] > 0 ? updeg[m] : 1; prop_div += ppm / 5.0 / ud; }
            }
            double local = pp + 2.0 * has_trader + ship + t_in - t_out;
            double rf = val - (local + prop_full), rd = val - (local + prop_div), rn = val - local;
            double tol = 0.005 + 0.01 * val;
            n_tested++;
            // the CLEAN class: nothing but provincial power and propagation can be in val
            int has_capital = livetrade::fb(r + 0xAD);
            if (!has_trader && !has_capital && ship <= 0.0005 && t_in <= 0.0005 && t_out <= 0.0005 && (prop_full > 0.0005 || val - pp > 0.05)) {
                clean++;
                double rcf = val - pp - prop_full, rcd = val - pp - prop_div, rcn = val - pp;
                if (std::fabs(rcf) <= tol) clean_full++; if (std::fabs(rcd) <= tol) clean_div++; if (std::fabs(rcn) <= tol) clean_none++;
                if (clean_samples < 10) { clean_samples++; lg << "     [prop/clean] " << s.name << " #" << c << ": val=" << val << " pp=" << pp << " val-pp=" << (val - pp) << " prop_full=" << prop_full << " prop_div=" << prop_div << " (down " << down[s.index].size() << ")" << (char)10; }
            }
            bool cf = std::fabs(rf) <= tol, cd = std::fabs(rd) <= tol, cn = std::fabs(rn) <= tol;
            if (cf) close_full++; if (cd) close_div++; if (cn) close_noprop++;
            if (!cf && !cd && !cn) { close_none++; if (samples < 8) { samples++; lg << "     [prop] " << s.name << " #" << c << ": val=" << val << " pp=" << pp << " trader=" << has_trader << " ship=" << ship << " t_in=" << t_in << " t_out=" << t_out << " prop_full=" << prop_full << " prop_div=" << prop_div << " (down " << down[s.index].size() << ")" << (char)10; } }
            if (std::fabs(rf) > worst_full) { worst_full = std::fabs(rf); worst_name = s.name + "#" + std::to_string(c); }
            if (std::fabs(rd) > worst_div) worst_div = std::fabs(rd);
        }
    }
    lg << "  [prop] val decomposition over " << n_tested << " records: closes with FULL fifth=" << close_full << " DIVIDED fifth=" << close_div
       << " with NO propagation=" << close_noprop << " none=" << close_none << " | CLEAN class (no trader/capital/ships/transfers): " << clean << " records, closes FULL=" << clean_full << " DIVIDED=" << clean_div << " no-prop=" << clean_none << " | worst |residual| full=" << worst_full << " (" << worst_name << ") div=" << worst_div << (char)10;
}

} // namespace propprobe
