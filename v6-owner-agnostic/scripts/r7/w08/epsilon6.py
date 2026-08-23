# -*- coding: utf-8 -*-
"""Sink sets over the Phase-2 tie-break strength TIE_EPS, on the shipped operator.

The swept cost is the SHIPPED cost shape -- first-order term at the swept eps plus the shipped
second-order generic term:

    c(u,v) = 1 + eps * (WN[u] + WN[v]) / 2 + TIE_EPS2 * frac(min(WN)*max(WN)*7919)

so at eps = TIE_EPS = 1e-3 the swept cost equals flowop.TIE_COST bit for bit, and that point is the
validation gate: the run aborts unless it reproduces the shipped map 159/159. An eps = 0 gate would
be unsatisfiable by construction -- the shipped map carries TIE_EPS = 1e-3, and eps = 0 agrees with
it on 143 of 159 edges (the sweep's own low-end drift), which this script reports as data.

Repaired under round-7 B5. The previous revision (a) pinned alpha_Phi = 1.5, the pre-v6.1 operator;
(b) swept a 34-point grid over 1e-12..1e+4 that could not produce the documented 1e-13..1e+12
result; (c) omitted TIE_EPS2, so it swept a cost shape the model does not ship; and (d) "validated"
by restoring the shipped solver at eps = 0, which validates nothing. Its mcf(s, c) signature also
predated drain.phase2 passing cost= and raised TypeError on every call.

Usage: python epsilon6.py [alpha_Phi]        (default 2.0, the shipped value)
"""
import collections
import sys

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, ".")
import drain
import flowop
from flowop import TIE_EPS, TIE_EPS2
from solver import N, ORDER, NIDX, ROWS

ALPHA = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N)
np.add.at(NODEW, pn, W)
WN = (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
_t = (W / W.max()) ** ALPHA
_num = np.zeros(N)
np.add.at(_num, pn, _t)
BW = np.full(N, 1.0 / N) - _num / _num.sum()

_A1 = np.array([WN[u] for (u, v, ei, sg) in flowop.ARCS])
_A2 = np.array([WN[v] for (u, v, ei, sg) in flowop.ARCS])
_GEN = np.modf(np.minimum(_A1, _A2) * np.maximum(_A1, _A2) * 7919.0)[0]


def cost_at(eps):
    """The shipped cost shape with the first-order strength swept."""
    return 1.0 + eps * (_A1 + _A2) / 2.0 + TIE_EPS2 * _GEN


def solve(eps):
    cost = cost_at(eps)

    def mcf(s, c, cost_ignored=None, **kw):
        r = linprog(c=cost, A_eq=flowop.AEQ, b_eq=c - s, bounds=(0, None),
                    method="highs", options=flowop.LP_OPTS)
        if not r.success:
            raise RuntimeError(r.message)
        du = np.asarray(r.eqlin.marginals) if getattr(r, "eqlin", None) is not None else None
        return r.x, du, r

    old = drain.mincost_flow
    drain.mincost_flow = mcf
    try:
        r = drain.run_drain(BW)
    finally:
        drain.mincost_flow = old
    d = set(r["directed"])
    od = collections.Counter(u for u, _ in d)
    sinks = tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0))
    return sinks, d, len(r.get("promotions") or []), len(r.get("fallbacks") or []), bool(drain.has_cycle(d))


# ---- the shipped map, and the two structural checks ----------------------------------------------
_ship = drain.run_drain(BW)
D_SHIP = set(_ship["directed"])
_od = collections.Counter(u for u, _ in D_SHIP)
S_SHIP = tuple(sorted(ORDER[i] for i in range(N) if _od[i] == 0))

assert np.array_equal(cost_at(TIE_EPS), flowop.TIE_COST), \
    "swept cost at eps = TIE_EPS is not the shipped TIE_COST -- the sweep is off the shipped path"

s_gate, d_gate, _, _, _ = solve(TIE_EPS)
if not (s_gate == S_SHIP and d_gate == D_SHIP):
    sys.exit("eps = TIE_EPS does not reproduce the shipped map -- no figure from this run is usable")
print("alpha_Phi = %g   validation: eps = TIE_EPS = %g reproduces the shipped map %d/%d, sinks %s"
      % (ALPHA, TIE_EPS, len(D_SHIP & d_gate), len(D_SHIP), ", ".join(S_SHIP)))
print()

# ---- the 24-point grid the document quotes -------------------------------------------------------
GRID = [1e-13, 1e-12, 1e-11, 3e-11, 1e-10, 3e-10, 1e-9, 3e-9, 1e-8, 1e-7, 1e-6,
        1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 3.0, 10.0, 1e2, 1e3, 1e6, 1e9, 1e12]
print("%-8s %-3s %-28s %-14s %-4s %s" % ("eps", "n", "sinks", "edges-vs-ship", "cyc", "promo/fb"))
sink_sets = set()
max_below, max_above = 0, 0
for e in GRID:
    s, d, pr, fb, cy = solve(e)
    moved = len(D_SHIP) - len(D_SHIP & d)
    sink_sets.add(s)
    if e < 1e-4:
        max_below = max(max_below, moved)
    if e > 3:
        max_above = max(max_above, moved)
    print("%-8g %-3d %-28s %-14d %-4s %d/%d" % (e, len(s), ",".join(s), moved, cy, pr, fb))
print()
print("distinct sink sets over the %d grid points: %d  %s"
      % (len(GRID), len(sink_sets), sorted(sink_sets)))
print("max edges moved below 1e-4: %d ; above 3: %d" % (max_below, max_above))
# eps = 0, reported as data (not a gate): the first-order term off entirely
s0, d0, _, _, _ = solve(0.0)
print("eps = 0 (first-order term off): agrees with shipped map on %d/%d edges, sinks %s"
      % (len(D_SHIP & d0), len(D_SHIP), ",".join(s0)))
