import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, UND, EDGES_UND, ROWS
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = (W / W.max()) ** 2.0
n = np.zeros(N); np.add.at(n, pn, t)
r = run_drain(np.full(N, 1.0/N) - n/n.sum())
dset = set(r["directed"])
gi = NIDX["genua"]
ins = [ORDER[u] for u,v in dset if v==gi]
print("genua in-edges (directed):", sorted(ins))
# confirm undirected adjacency (is genua-alexandria even a link in the raw graph)
ai = NIDX["alexandria"]
print("genua-alexandria is an undirected edge (raw graph):", ai in UND[gi])
print("genua's full undirected neighbor set:", sorted(ORDER[x] for x in UND[gi]))
