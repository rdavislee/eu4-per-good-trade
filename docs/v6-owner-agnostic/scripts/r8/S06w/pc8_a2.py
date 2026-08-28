import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain, sinks_of
W = np.array([r["tax"] + r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
t = (W/W.max())**2.0; nn = np.zeros(N); np.add.at(nn, pn, t)
b = np.full(N,1.0/N) - nn/nn.sum()
r = run_drain(b)
free = set(r["free"]); flow_arc = r["flow_arc"]
out = collections.defaultdict(list)
for (u,v) in r["directed"]: out[u].append(v)
eidx = {tuple(sorted(e)): i for i, e in enumerate(EDGES_UND)}
for nm in ("mexico","gulf_of_siam","sevilla","english_channel"):
    i = NIDX[nm]
    rows=[]
    for v in out[i]:
        ei = eidx[tuple(sorted((i,v)))]
        rows.append((ORDER[v], "FREE" if ei in free else "flow", round(float(r["net"][ei]),8)))
    print("%-16s out-arcs: %s" % (nm, rows))
sk,_ = sinks_of(r["directed"])
print("sinks:", sorted(ORDER[i] for i in sk))
