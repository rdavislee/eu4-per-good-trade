# -*- coding: utf-8 -*-
"""Reproduce v6.0's sink set: unit-cost Phase-2 solver (no tie-break), alpha_Phi = 1.5."""
import sys, os, collections, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import flowop
# Monkeypatch: force Phase 2 to use unit arc costs (cost=None) regardless of TIE_COST,
# to reproduce the pre-v6.1 "unit-cost solver".
import drain as drain_mod
orig_mincost_flow = flowop.mincost_flow
def unit_cost_mincost_flow(s, c, cost=None):
    return orig_mincost_flow(s, c, cost=None)   # force unit cost, ignore TIE_COST arg
drain_mod.mincost_flow = unit_cost_mincost_flow

from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

def cv(a, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a
    n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()

def sk(r):
    o = collections.Counter(u for u, _ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if o[i] == 0)

for a in (1.5, 2.0):
    c = cv(a)
    res = run_drain(np.full(N, 1.0 / N) - c)
    print("alpha=%s  unit-cost sinks = %s" % (a, sk(res)))
