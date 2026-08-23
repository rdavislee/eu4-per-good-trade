import collections
import numpy as np
import drain
import flowop
from solver import N, ORDER, NIDX, ROWS, UND, EDGES_UND
from drain import run_drain, phase0, phase1, phase2, sweep_priority, compile_dirs, ZERO_TOL
from flowop import mincost_flow, ARCS

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N)
np.add.at(NODEW, PN, W)

def bw(alpha=A_PHI):
    t = (W / W.max()) ** alpha
    n = np.zeros(N)
    np.add.at(n, PN, t)
    return np.full(N, 1.0 / N) - n / n.sum()

B = bw()
core, beta, Plog = phase0(B)
print("mexico in core?", NIDX["mexico"] in core, "gulf_of_siam in core?", NIDX["gulf_of_siam"] in core, "sevilla in core?", NIDX["sevilla"] in core)
flow_arc, free, net, cost = phase2(core, beta)

for name in ["mexico","gulf_of_siam","sevilla"]:
    i = NIDX[name]
    print("\n==", name, "UND neighbors:", [ORDER[j] for j in UND[i]])
    for ei,(u,v) in enumerate(EDGES_UND):
        if u==i or v==i:
            kind = "flow_arc" if ei in flow_arc else ("free" if ei in free else "NOT-CORE-EDGE")
            fa_dir = flow_arc.get(ei)
            print(f"   edge {ei}: EDGES_UND=({ORDER[u]},{ORDER[v]}) net={net[ei]:.6g} kind={kind} flow_arc_dir={fa_dir if fa_dir is None else (ORDER[fa_dir[0]],ORDER[fa_dir[1]])}")
