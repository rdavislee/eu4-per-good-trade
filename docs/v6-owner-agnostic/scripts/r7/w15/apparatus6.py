# -*- coding: utf-8 -*-
"""The one figure §0, §1.3 and §3.13 quote that no shipped script computed: the ducat value of
the modifier apparatus v6.0 deleted.

Round-5 part-4 validation found 105.30 present only as a literal in the edit script `r24.py` --
absent from `measure6.out`, unchecked by `verify6.py`. This regenerates it.

It does NOT resurrect v5.0's two-test classifier, and it runs no whole-install sweep. The
apparatus is a FROZEN TABLE of twenty-two constants, copied verbatim from
`../../v5-owner-agnostic/scripts/solver.py:59-75`, applied to the v6.0 province table. That is
why instrumenting the figure costs nothing in input surface: nothing here classifies anything,
so there is no rule to be wrong about, and both audits' refutations (W041, X035) were of the
classifier, not of these values.

Reproduces `preconfirm-round2.md` note N03 exactly: 10,607.40 / 10,712.70 / 105.30 / 89.

Usage: python apparatus6.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import (ROWS, PROV, PRICES, GOODS_PRODUCED_FACTOR, TAX_COEFF,
                    STATE_GOODS_MOD, ON_STARTUP_DEVASTATION)

# ---- v5.0's apparatus, verbatim from v5-owner-agnostic/scripts/solver.py:59-75 -------------
LOCAL_TAX_MOD = {"gems": 0.15}            # trade good: local_tax_modifier   -> tax_value
LOCAL_TV_MOD  = {"incense": 0.10}         # trade good: trade_value_modifier -> trade_value
MON_FLAT  = {8: 3.0, 684: 0.5, 1821: 0.5, 1822: 0.5, 2145: 0.5}   # falun, grand_canal_1..4
MON_GPMOD = {262: 0.10}                                           # krakow_cloth_hall
MON_TVMOD = {684: 0.1, 1821: 0.1, 1822: 0.1, 2145: 0.1}           # grand_canal_1..4
PERM_FLAT = {6: 2.0, 362: 2.0, 363: 2.0, 370: 1.0, 371: 1.0,      # add_permanent_province_modifier
             387: 3.0, 542: 4.0, 2151: 2.5, 2316: 2.0, 4316: 2.0}
FLAT_GOODS = dict(MON_FLAT); FLAT_GOODS.update(PERM_FLAT)

off = on = 0.0
touched = set()
for r in ROWS:
    pid, g = r["pid"], r["good"]
    price = PRICES.get(g, 0.0)
    s = PROV[pid]
    gmod = STATE_GOODS_MOD["devastation"] * (ON_STARTUP_DEVASTATION.get(pid, 0.0) / 100.0)
    tax0 = TAX_COEFF * s["base_tax"]
    gp0 = max(0.0, GOODS_PRODUCED_FACTOR * s["base_production"] * (1.0 + gmod))
    off += tax0 + gp0 * price
    gp = max(0.0, GOODS_PRODUCED_FACTOR * s["base_production"]
             * (1.0 + gmod + MON_GPMOD.get(pid, 0.0)) + FLAT_GOODS.get(pid, 0.0))
    on += (tax0 * (1.0 + LOCAL_TAX_MOD.get(g, 0.0))
           + gp * price * (1.0 + LOCAL_TV_MOD.get(g, 0.0) + MON_TVMOD.get(pid, 0.0)))
    if (g in LOCAL_TAX_MOD or g in LOCAL_TV_MOD or pid in FLAT_GOODS
            or pid in MON_GPMOD or pid in MON_TVMOD):
        touched.add(pid)

# C1: exposed as a dict so measure6.py can import these rather than inline the frozen table. The
# constants below are dead v5 data; keeping them in a separate file stops a future editor wiring
# them back into the live wealth path, which is the input surface v6.0 deleted.
#
# No EXPECT block: once verify6.py checks the computed figure against the document, a hard-coded
# expectation here is just a second typed copy of 105.30, and not typing 105.30 is the whole point.
FIGURES = {
    "apparatus world wealth off": round(off, 2),
    "apparatus world wealth on": round(on, 2),
    "deleted apparatus in ducats": round(on - off, 2),
    "apparatus pct of on-total": round(100.0 * (on - off) / on, 2),
    "apparatus pct of v6 field": round(100.0 * (on - off) / off, 2),
    "apparatus provinces touched": len(touched),
}

if __name__ == "__main__":
    for _k, _v in FIGURES.items():
        print("%-40s %s" % (_k, _v))
