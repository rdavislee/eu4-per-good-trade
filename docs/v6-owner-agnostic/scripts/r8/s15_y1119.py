# -*- coding: utf-8 -*-
import numpy as np, sys, os
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop
from flowop import mincost_flow, net_per_edge, TIE_COST, EDGES_UND
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
wmax = W.max()
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]

def build_c2(g, k_exp=2, clamp=False):
    a = (PRICES[g]/2.0)**k_exp
    if clamp: a = min(max(a, 0.2), 3.0)
    t = (W/wmax)**a
    num = np.zeros(N); np.add.at(num, pn, t)
    return num/num.sum()

ndiff = 0
for g in GL:
    c2 = build_c2(g)
    b = val[g]/val[g].sum() - c2   # s=b -> matches final.py: mincost_flow(b+0, zeros, cost=...) with s=b,c=0
    f_unit, _, _ = mincost_flow(b + 0, np.zeros(N), cost=None)
    f_tie, _, _  = mincost_flow(b + 0, np.zeros(N), cost=TIE_COST)
    net_unit = net_per_edge(f_unit)
    net_tie  = net_per_edge(f_tie)
    diff = np.abs(net_unit - net_tie).max()
    same_support = np.allclose(net_unit, net_tie, atol=1e-6)
    if not same_support:
        ndiff += 1
    print("%-16s maxdiff=%.6f  same_vertex=%s" % (g, diff, same_support))
print()
print("goods differing (unit vs TIE_COST) vertex: %d of %d" % (ndiff, len(GL)))
