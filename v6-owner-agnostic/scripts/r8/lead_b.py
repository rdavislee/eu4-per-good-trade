# -*- coding: utf-8 -*-
"""Lead probe B: §3.9 flow_in/flow_out per node, free out-edges, out-degree>0 & zero out-flow."""
import os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, W)
t = (W / W.max()) ** A_PHI
cw = np.zeros(N); np.add.at(cw, pn, t); cw = cw / cw.sum()
bw = np.full(N, 1.0 / N) - cw
res = run_drain(bw)
net = res["net"]; free = res["free"]; directed = res["directed"]; flow_arc = res["flow_arc"]

fin = np.zeros(N); fout = np.zeros(N)
for e, (u, v) in enumerate(EDGES_UND):
    f = net[e]
    if f > 0:
        fout[u] += f; fin[v] += f
    elif f < 0:
        fout[v] += -f; fin[u] += -f

resid = fin - fout + bw
print("identity max |flow_in - flow_out + b_w| :", "%.3g" % np.max(np.abs(resid)))
print("net demanders (-b_w > 0):", int(np.sum(-bw > 0)))
print("identity holds on all 80:", bool(np.max(np.abs(resid)) < 1e-12))

out = collections.Counter(u for u, _ in directed)
zero_out_flow = [ORDER[i] for i in range(N) if out[i] > 0 and fout[i] <= 1e-15]
print("nodes with out-degree>0 and ZERO outgoing flow:", len(zero_out_flow))
print("   ", sorted(zero_out_flow))

# free edges as a set of undirected pairs
freeset = set()
for item in free:
    freeset.add(tuple(sorted(item[:2])) if not isinstance(item, int) else item)
print("free repr sample:", free[:3], "len", len(free))
print("flow_arc sample:", list(flow_arc.items())[:3])

for n in ("sevilla", "mexico", "gulf_of_siam"):
    i = NIDX[n]
    print("%-14s flow_in %.6f flow_out %.6f  b_w %.6f  outdeg %d" % (n, fin[i], fout[i], bw[i], out[i]))
    # out-arcs of this node, classified free vs flow
    outs = [(u, v) for (u, v) in directed if u == i]
    for (u, v) in outs:
        # find edge index
        for e, (a, b) in enumerate(EDGES_UND):
            if {a, b} == {u, v}:
                kind = "FLOW" if abs(net[e]) > 1e-15 else "free"
                print("     -> %-18s %s net=%.3g" % (ORDER[v], kind, net[e]))
                break
