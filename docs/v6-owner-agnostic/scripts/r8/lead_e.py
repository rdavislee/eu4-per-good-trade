# -*- coding: utf-8 -*-
"""Lead probe E: zero-reduced-cost arcs off support under unit / first-order / full cost.
Reproduces section 2.3's 40 -> 0 aggregate, 41 arcs on 18 of 29 goods, and 1 arc on 1 good."""
import os, sys, collections
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from scipy.optimize import linprog
import flowop
from flowop import ARCS, AEQ, TIE_COST, TIE_EPS, TIE_EPS2, LP_OPTS, ZERO_TOL
from solver import N, ORDER, NIDX, EDGES_UND, GOODS, ROWS, build_sc, PRICES
import drain

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, world = build_sc(ALPHA, eps=0.0)
GL = [(i, g) for i, g in enumerate(GOODS) if LIVE[i]]

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, W)
w = NW.copy()
w = (w - w.min()) / (w.max() - w.min())          # min-max, the shipped normalisation

unit = np.ones(len(ARCS))
first = np.array([1.0 + TIE_EPS * (w[u] + w[v]) / 2.0 for (u, v, ei, sg) in ARCS])
full = TIE_COST.copy()


def zero_rc(b, cost):
    core, beta, _ = drain.phase0(b)
    bb = np.zeros(N)
    for v in core:
        bb[v] = beta[v]
    res = linprog(c=cost, A_eq=AEQ, b_eq=-bb, bounds=(0, None), method="highs", options=LP_OPTS)
    y = np.asarray(res.eqlin.marginals)
    rc = np.array([cost[k] - y[v] + y[u] for k, (u, v, ei, sg) in enumerate(ARCS)])
    off = res.x <= 1e-11
    return int((off & (np.abs(rc) <= 1e-9)).sum())


A_PHI = 2.0
t = (W / W.max()) ** A_PHI
cw = np.zeros(N); np.add.at(cw, pn, t); cw = cw / cw.sum()
B_AGG = np.full(N, 1.0 / N) - cw

for label, cost in (("unit", unit), ("first-order only", first), ("full (shipped)", full)):
    agg = zero_rc(B_AGG, cost)
    tot = 0; goods = []
    for gi, g in GL:
        n = zero_rc(S[gi] - C[gi], cost)
        if n:
            goods.append((g, n)); tot += n
    print("%-18s aggregate zero-rc off-support arcs: %-4d | per-good total %-4d on %d of %d goods"
          % (label, agg, tot, len(goods), len(GL)))
    print("                   goods:", goods)
