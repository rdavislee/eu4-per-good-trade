import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import GOODS, ORDER
import flowop
from flowop import (S0, C0, V, LIVE, EDGES_UND, E, mincost_flow, net_per_edge,
                     edges_from_net, has_cycle, s_targeted, ZERO_TOL)

net_total = np.zeros(E)
for gi, g in enumerate(GOODS):
    if not LIVE[gi]:
        continue
    s = s_targeted(gi)
    c = C0[gi]
    f, duals, res = mincost_flow(s, c, cost=None)  # unit arc costs, per-good FLOW operator
    net_g = net_per_edge(f)
    net_total += V[gi] * net_g

directed = edges_from_net(net_total)
cyc = has_cycle(directed)
print("edges with nonzero net (value-weighted):", int((np.abs(net_total) > ZERO_TOL).sum()), "of", E)
print("has_cycle result:", cyc)
if cyc:
    print("cycle (node names):", [ORDER[i] for i in cyc])
