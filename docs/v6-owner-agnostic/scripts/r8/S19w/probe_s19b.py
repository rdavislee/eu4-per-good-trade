# -*- coding: utf-8 -*-
import os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import drain
import flowop
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS,
                    PRICES, ROWS, build_sc)
from drain import (run_drain, sinks_of, phase0, phase1, phase2,
                   sweep_priority, compile_dirs)
from flowop import mincost_flow, ARCS, TIE_EPS, TIE_EPS2

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N)
np.add.at(NODEW, PN, W)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]

def bw(alpha=A_PHI):
    t = (W / W.max()) ** alpha
    n = np.zeros(N)
    np.add.at(n, PN, t)
    return np.full(N, 1.0 / N) - n / n.sum()

B = bw()

# --- reproduce round6.py's 3.9 identity computation exactly ---
f, duals, res = mincost_flow(B + 0, np.zeros(N), cost=flowop.TIE_COST)
fin = np.zeros(N)
fout = np.zeros(N)
for ai, (u, v, _ei, _sg) in enumerate(ARCS):
    fout[u] += f[ai]
    fin[v] += f[ai]
resid = np.abs((fin - fout) - (-B))
dem = [i for i in range(N) if -B[i] > 0]
print("identity holds on %d of %d; max residual %.6e" % (int((resid < 1e-12).sum()), N, resid.max()))
print("net demanders:", len(dem))

directed = run_drain(B)["directed"]
outdeg = collections.Counter(u for u, _v in directed)
outset = collections.defaultdict(list)
for u, v in directed:
    outset[u].append(v)

for name in ("sevilla", "mexico", "gulf_of_siam", "english_channel", "genua"):
    i = NIDX[name]
    print("%-16s  -B(i)=%.6f  fin=%.6f  fout=%.6f  resid=%.3e  outdeg=%d  out-> %s"
          % (name, -B[i], fin[i], fout[i], resid[i], outdeg[i],
             [ORDER[x] for x in outset[i]]))

# how many out-edges are "flow" edges vs "free" edges for mexico / gulf_of_siam
core, beta, Plog = phase0(B)
flow_arc, free, net, cost = phase2(core, beta)
flow_out_arcs = collections.defaultdict(list)
for ei, (u, v) in flow_arc.items():
    flow_out_arcs[u].append((v, net[ei]))
free_adj = collections.defaultdict(list)
for ei in free:
    u, v = EDGES_UND[ei]
    free_adj[u].append(v)
    free_adj[v].append(u)

print()
print("core contains sevilla/mexico/gulf_of_siam?",
      NIDX["sevilla"] in core, NIDX["mexico"] in core, NIDX["gulf_of_siam"] in core)
for name in ("sevilla", "mexico", "gulf_of_siam"):
    i = NIDX[name]
    print(name, "flow_arc out (LP core, phase2):", [(ORDER[v], round(n,5)) for v,n in flow_out_arcs[i]],
          "free-adjacent:", [ORDER[x] for x in free_adj[i]])

# 18-of-80 set: nodes with out-degree>0 (in compiled directed graph) & fout==0 in the 3.9 identity LP
outdeg80 = [i for i in range(N) if outdeg[i] > 0 and fout[i] < 1e-12]
print()
print("count of out-degree>0 & fout==0 nodes:", len(outdeg80))
print("mexico in this set?", NIDX["mexico"] in outdeg80, " gulf_of_siam in this set?", NIDX["gulf_of_siam"] in outdeg80)
print("sevilla in this set (should be false since it has nonzero fout)?", NIDX["sevilla"] in outdeg80)

# which out-arc(s) does mexico/gulf_of_siam have in the compiled `directed` output, and are they "free" (net~0) in the phase2 LP?
for name in ("mexico", "gulf_of_siam"):
    i = NIDX[name]
    outs = outset[i]
    print(name, "compiled out-arcs:", [ORDER[x] for x in outs], "count:", len(outs))
