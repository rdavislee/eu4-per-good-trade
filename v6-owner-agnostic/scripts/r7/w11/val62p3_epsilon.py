# -*- coding: utf-8 -*-
"""val part3: TIE_EPS / TIE_EPS2 sensitivity, measured through the SHIPPED drain.

The shipped epsilon6.py crashes (its mcf stub rejects drain.phase2's cost= kwarg), so this
rebuilds the measurement by rewriting flowop.TIE_COST / drain.TIE_COST in place.
"""
import collections, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from solver import N, ORDER, NIDX, ROWS, EDGES_UND, GOODS, PRICES, build_sc
from flowop import ARCS, ZERO_TOL

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, PN, W)
WN = (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
_t = (W / W.max()) ** A_PHI
_n = np.zeros(N); np.add.at(_n, PN, _t)
BW = np.full(N, 1.0 / N) - _n / _n.sum()
A1 = np.array([WN[u] for (u, v, e, s) in ARCS])
A2 = np.array([WN[v] for (u, v, e, s) in ARCS])
GEN = np.modf(np.minimum(A1, A2) * np.maximum(A1, A2) * 7919.0)[0]
SHIPPED = flowop.TIE_COST.copy()

def cost(eps, eps2):
    return 1.0 + eps * (A1 + A2) / 2.0 + eps2 * GEN

def with_cost(c, fn):
    o1, o2 = flowop.TIE_COST, drain.TIE_COST
    flowop.TIE_COST = drain.TIE_COST = c
    try:
        return fn()
    finally:
        flowop.TIE_COST, drain.TIE_COST = o1, o2

def sinks():
    r = drain.run_drain(BW)
    od = collections.Counter(u for u, _ in r["directed"])
    return tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0)), set(r["directed"])

assert np.allclose(cost(1e-3, 1e-6), SHIPPED), "cost reconstruction differs from shipped"
S0, D0 = sinks()
print("shipped TIE_EPS=1e-3 TIE_EPS2=1e-6 ->", S0, len(D0), "edges")
print()
print("=== TIE_EPS sweep (TIE_EPS2 held at 1e-6, shipped LP_OPTS) ===")
print("%-10s %-4s %-40s %s" % ("eps", "n", "sinks", "edges moved vs shipped"))
for k in range(-14, 6):
    for m in (1.0, 3.0):
        e = m * 10.0 ** k
        if e > 3e4: continue
        s, d = with_cost(cost(e, 1e-6), sinks)
        print("%-10g %-4d %-40s %d" % (e, len(s), ",".join(s), len(d ^ D0) // 2))

print()
print("=== epsilon6.py's intended configuration: FIRST-ORDER cost only, DEFAULT LP tolerance ===")
_saveopts = flowop.LP_OPTS
flowop.LP_OPTS = None
try:
    for k in range(-14, 6):
        for m in (1.0, 3.0):
            e = m * 10.0 ** k
            if e > 3e4: continue
            s, d = with_cost(cost(e, 0.0), sinks)
            print("%-10g %-4d %-40s %d" % (e, len(s), ",".join(s), len(d ^ D0) // 2))
finally:
    flowop.LP_OPTS = _saveopts
