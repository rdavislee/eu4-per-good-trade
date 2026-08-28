# -*- coding: utf-8 -*-
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, UND, EDGES_UND, ROWS
from drain import run_drain

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cv(a=A_PHI):
    w = W
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()

cw = cv()
b_w = np.full(N, 1.0/N) - cw
r = run_drain(b_w)
o = r["order"]
dset = set(r["directed"])
violations = 0
for u, v in EDGES_UND:
    want = (u, v) if o[u] > o[v] else (v, u)
    if want not in dset:
        violations += 1
print("edges checked:", len(EDGES_UND))
print("violations:", violations)
print("sinks:", sorted(ORDER[i] for i in range(N) if collections.Counter(uu for uu,_ in r['directed'])[i]==0))
