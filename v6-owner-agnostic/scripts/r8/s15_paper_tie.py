# -*- coding: utf-8 -*-
import numpy as np, sys, os
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from flowop import mincost_flow, net_per_edge, TIE_COST, EDGES_UND, ZERO_TOL, ARCS, LP_OPTS
from solver import build_sc
from scipy.optimize import linprog
import flowop
S0, C0, V, LIVE, GP, WORLD = flowop.S0, flowop.C0, flowop.V, flowop.LIVE, flowop.GP, flowop.WORLD
from solver import GOODS
gi = GOODS.index("paper")
s = flowop.s_targeted(gi); c = C0[gi]
f, duals, res = mincost_flow(s, c, cost=TIE_COST)
net = net_per_edge(f)
# reduced costs for off-support arcs (edges with ~0 net flow)
# recompute reduced cost = cost - (dual[v]-dual[u]) using AEQ orientation as in flowop
import scipy.sparse as sp
n = len(duals)
rows=[]
for ei,(u,v) in enumerate(EDGES_UND):
    if abs(net[ei]) <= ZERO_TOL:
        # reduced cost on arc u->v
        rc = TIE_COST[2*ei] - (duals[v]-duals[u])
        rc2 = TIE_COST[2*ei+1] - (duals[u]-duals[v])
        rows.append((ei,u,v,rc,rc2,min(abs(rc),abs(rc2))))
rows.sort(key=lambda r:r[5])
print("paper: off-support arcs sorted by |reduced cost| (smallest first), top 5:")
for ei,u,v,rc,rc2,m in rows[:5]:
    print("  edge %d (%d,%d) rc(u->v)=%.3e rc(v->u)=%.3e" % (ei,u,v,rc,rc2))
print("smallest |reduced cost| among off-support arcs: %.3e" % rows[0][5])
