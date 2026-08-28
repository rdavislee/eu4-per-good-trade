# -*- coding: utf-8 -*-
import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain, sinks_of, has_cycle
A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = (W / W.max()) ** A_PHI
n = np.zeros(N); np.add.at(n, pn, t); c = n / n.sum()
res = run_drain(np.full(N, 1.0/N) - c)
d = res["directed"]
outdeg = collections.Counter(u for u,_ in d)
indeg = collections.Counter(v for _,v in d)
gi = NIDX['genua']
print("genua out-degree", outdeg[gi], "in-degree", indeg[gi])
print("in-arcs :", sorted(ORDER[u] for u,v in d if v==gi))
print("out-arcs:", sorted(ORDER[v] for u,v in d if u==gi))
print("sinks", sorted(ORDER[i] for i in range(N) if outdeg[i]==0))
