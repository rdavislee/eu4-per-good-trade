# -*- coding: utf-8 -*-
"""B3: unit-cost vs tie-break sink sets across alpha_Phi"""
import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import drain, flowop
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain, sinks_of

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cv(a):
    t = (W/W.max())**a; n = np.zeros(N); np.add.at(n, pn, t); return n/n.sum()
def sset(a):
    r = run_drain(np.full(N,1.0/N) - cv(a)); sk,_ = sinks_of(r["directed"])
    return sorted(ORDER[i] for i in sk)

orig = flowop.TIE_COST
for label, cost in (("tie-break (shipped)", orig), ("unit cost (v6.0)", None)):
    drain.TIE_COST = cost
    print("--", label)
    for a in (1.0, 1.5, 2.0, 3.0):
        print("   alpha_Phi=%-4s -> %s" % (a, sset(a)))
drain.TIE_COST = orig
