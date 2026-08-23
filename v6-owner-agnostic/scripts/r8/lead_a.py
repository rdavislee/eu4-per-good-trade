# -*- coding: utf-8 -*-
"""Lead validator probe A: §3.9 end/flow figures, §3.7 per-node out-arc coverage, §3.3 ratios."""
import os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from drain import run_drain
import drain as D

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, W)
t = (W / W.max()) ** A_PHI
cw = np.zeros(N); np.add.at(cw, pn, t); cw = cw / cw.sum()
bw = np.full(N, 1.0 / N) - cw
res = run_drain(bw)
print("keys:", sorted(res.keys()))

directed = res["directed"]
flow = res.get("flow")
print("flow type:", type(flow))

out = collections.Counter(u for u, _ in directed)
inn = collections.Counter(v for _, v in directed)
sinks = sorted(ORDER[i] for i in range(N) if out[i] == 0)
print("sinks:", sinks)

# node wealth ranks
nwrank = {ORDER[i]: r + 1 for r, i in enumerate(sorted(range(N), key=lambda i: -NW[i]))}
for n in ("english_channel", "mexico", "gulf_of_siam", "genua", "sevilla", "hangzhou", "beijing"):
    i = NIDX[n]
    print("  %-16s wealth %8.1f  rank %d  outdeg %d indeg %d" % (n, NW[i], nwrank[n], out[i], inn[i]))

# flow arcs: reconstruct from res
print()
print("res['flow_arcs'] present?", 'flow_arcs' in res)
for k in res:
    v = res[k]
    print("  %-14s %s" % (k, (type(v).__name__ + " len=" + str(len(v))) if hasattr(v, '__len__') else v))
