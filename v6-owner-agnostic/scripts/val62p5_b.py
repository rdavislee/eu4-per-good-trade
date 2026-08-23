# -*- coding: utf-8 -*-
import collections, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import drain, flowop
from solver import N, ORDER, NIDX, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, sinks_of
from flowop import mincost_flow, ARCS, TIE_COST
from scipy.optimize import linprog
from scipy.sparse import vstack, csr_matrix

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)

print("== graph SOURCES (in-degree 0) for spices/cloves (Y537 reading) ==")
for g in ("spices","cloves"):
    gi = GOODS.index(g)
    r = run_drain(S[gi]-C[gi])
    ind = collections.Counter(v for _,v in r["directed"])
    src = sorted(ORDER[i] for i in range(N) if ind[i]==0)
    print(g, "graph sources:", src)

print("\n== paper genuine tie, inequality form ==")
gi = GOODS.index("paper")
b = S[gi]-C[gi]
f, du, res = mincost_flow(b+0, np.zeros(N), cost=TIE_COST)
rc = np.array([TIE_COST[ai] - (du[ARCS[ai][1]] - du[ARCS[ai][0]]) for ai in range(len(ARCS))])
opt = res.fun
zero_off = [ai for ai in range(len(ARCS)) if f[ai] <= 1e-12 and abs(rc[ai]) <= 1e-14]
for ai in zero_off:
    u,v,ei,sg = ARCS[ai]
    cobj = np.zeros(len(ARCS)); cobj[ai] = -1.0
    for slack in (1e-12, 1e-10):
        r3 = linprog(c=cobj, A_eq=flowop.AEQ, b_eq=np.zeros(N)-b,
                     A_ub=csr_matrix(TIE_COST.reshape(1,-1)), b_ub=[opt+slack],
                     bounds=(0,None), method="highs")
        print("  arc %s->%s slack %g: max flow at optimality = %.6g (success=%s)"
              % (ORDER[u],ORDER[v], slack, -r3.fun if r3.success else float('nan'), r3.success))
