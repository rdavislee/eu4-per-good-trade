# -*- coding: utf-8 -*-
"""Reproduce v6.0's aggregate sink set: unit arc cost (no tie-break), alpha_Phi = 1.5."""
import os, sys, collections
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import drain
from solver import N, ORDER, NIDX, ROWS

drain.TIE_COST = None   # force phase2's mincost_flow(..., cost=TIE_COST) to unit cost

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

def cv(a):
    t = (W / W.max()) ** a
    n = np.zeros(N); np.add.at(n, pn, t)
    return n / n.sum()

def sinks_for(a):
    b = np.full(N, 1.0 / N) - cv(a)
    r = drain.run_drain(b)
    o = collections.Counter(u for u, _ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if o[i] == 0)

for a in (1.5, 2.0):
    print("alpha_Phi=%s  unit-cost sinks: %s" % (a, sinks_for(a)))

# sanity: with TIE_COST restored (shipped), alpha=2.0 should match measure6.out's genua/hangzhou
import importlib
importlib.reload(drain)
print("sanity shipped alpha=2.0:", sinks_for(2.0))
