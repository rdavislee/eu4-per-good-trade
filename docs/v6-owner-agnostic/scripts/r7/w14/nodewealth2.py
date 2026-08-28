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
def cv(a=A_PHI, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
def bw(a=A_PHI):
    return np.full(N, 1.0/N) - cv(a)

B = bw()
base = run_drain(B)
directed = base["directed"]

names = ["english_channel", "genua", "mexico", "gulf_of_siam", "sevilla"]
for name in names:
    i = NIDX[name]
    print(name, "b_w=%.6f  -b_w>0(net demander)=%s" % (B[i], (-B[i])>0))

print()
print("english_channel outgoing directed edges:")
i = NIDX["english_channel"]
for u,v in directed:
    if u==i:
        print("  ->", ORDER[v])
    if v==i:
        print("  <-", ORDER[u])

print()
print("genua outgoing directed edges (should be none = sink):")
i = NIDX["genua"]
for u,v in directed:
    if u==i:
        print("  ->", ORDER[v])

# flow computation
f, duals, res = mincost_flow(B + 0, np.zeros(N), cost=flowop.TIE_COST)
fin = np.zeros(N); fout = np.zeros(N)
for ai, (u, v, _ei, _sg) in enumerate(ARCS):
    fout[u] += f[ai]; fin[v] += f[ai]

print()
for name in names:
    i = NIDX[name]
    print(name, "flow_in=%.4f flow_out=%.4f" % (fin[i], fout[i]))

print()
print("precise flow_out for the 5 named nodes:")
for name in names:
    i = NIDX[name]
    print(name, "flow_in=%.10f flow_out=%.10f" % (fin[i], fout[i]))

print()
print("outdeg>0 & flow_out<1e-12 nodes (the 18):")
outdeg = collections.Counter(u for u,v in directed)
lst = [ORDER[i] for i in range(N) if outdeg[i]>0 and fout[i] < 1e-12]
print(len(lst), lst)
