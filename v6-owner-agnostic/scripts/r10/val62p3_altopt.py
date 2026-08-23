# -*- coding: utf-8 -*-
"""val part3: goods admitting an alternative Phase-2 optimum, as a function of the tie-break cost."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import flowop
from flowop import mincost_flow, ARCS
from solver import N, ORDER, NIDX, ROWS, EDGES_UND, GOODS, PRICES, build_sc

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, PN, W)
WN = (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
A1 = np.array([WN[u] for (u, v, e, s) in ARCS])
A2 = np.array([WN[v] for (u, v, e, s) in ARCS])
GEN = np.modf(np.minimum(A1, A2) * np.maximum(A1, A2) * 7919.0)[0]
_t = (W / W.max()) ** 2.0
_n = np.zeros(N); np.add.at(_n, PN, _t)
BW = np.full(N, 1.0 / N) - _n / _n.sum()

def cost(eps, eps2):
    return 1.0 + eps * (A1 + A2) / 2.0 + eps2 * GEN

def alt(b, c):
    """zero reduced-cost arcs off the optimal support -> an alternative optimum exists."""
    fl, du, _r = mincost_flow(b + 0, np.zeros(N), cost=c)
    rc = np.array([c[ai] - (du[ARCS[ai][1]] - du[ARCS[ai][0]]) for ai in range(len(ARCS))])
    off = rc[fl <= 1e-12]
    return int((np.abs(off) <= 1e-14).sum())

for eps, eps2, tag in [(1e-3, 0.0, "first-order only"),
                       (1e-3, 1e-7, "TIE_EPS2 = 1e-7"),
                       (1e-3, 1e-6, "TIE_EPS2 = 1e-6 (shipped)"),
                       (1e-3, 1e-5, "TIE_EPS2 = 1e-5"),
                       (0.0, 0.0, "unit cost")]:
    c = cost(eps, eps2)
    bad = [g for gi, g in GL if alt(S[gi] - C[gi], c) > 0]
    print("%-28s aggregate zero-rc off support: %-4d ; goods with alternative optimum %2d of %d  %s"
          % (tag, alt(BW, c), len(bad), len(GL), bad))
