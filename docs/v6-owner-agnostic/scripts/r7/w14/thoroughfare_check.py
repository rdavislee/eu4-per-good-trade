import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain
import flowop
from flowop import mincost_flow, ARCS

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
A_PHI = 2.0
def cv(a=A_PHI):
    t = (W / W.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
def bw(a=A_PHI): return np.full(N, 1.0/N) - cv(a)
B = bw()
base = run_drain(B)
directed = base["directed"]
outd = collections.Counter(u for u,v in directed)
ind = collections.Counter(v for u,v in directed)

f, duals, res = mincost_flow(B + 0, np.zeros(N), cost=flowop.TIE_COST)
fout = np.zeros(N)
for ai, (u, v, _ei, _sg) in enumerate(ARCS):
    fout[u] += f[ai]

examples = [(ORDER[i], ind[i], outd[i], round(float(fout[i]),4)) for i in range(N) if ind[i] > outd[i] and fout[i] > 1e-9]
print("nodes with in-degree > out-degree AND positive outflow (genuine thoroughfares):", len(examples))
for e in examples[:10]:
    print(" ", e)
