# -*- coding: utf-8 -*-
"""Classify every good's off-support arcs by the three-branch rule spec 2.8's 'Solver optimality
tolerance' row describes: halt if min positive reduced cost <= tol; report if a zero-reduced-cost
off-support arc carries no flow in ANY optimum (genuine tie); halt if a zero-reduced-cost off-support
arc CAN carry flow (alternative optimum reachable)."""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import flowop
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from flowop import mincost_flow, ARCS, TIE_COST
from scipy.optimize import linprog
from scipy.sparse import vstack, csr_matrix

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
TOL = 1e-10

for gi, g in enumerate(GOODS):
    if not LIVE[gi]: continue
    b = S[gi]-C[gi]
    f, du, res = mincost_flow(b+0, np.zeros(N), cost=TIE_COST)
    rc = np.array([TIE_COST[ai] - (du[ARCS[ai][1]] - du[ARCS[ai][0]]) for ai in range(len(ARCS))])
    opt = res.fun
    pos_rc = rc[(f <= 1e-12) & (rc > 1e-14)]
    min_pos = pos_rc.min() if len(pos_rc) else None
    zero_off = [ai for ai in range(len(ARCS)) if f[ai] <= 1e-12 and abs(rc[ai]) <= 1e-14]
    branch = "clean"
    detail = ""
    if min_pos is not None and min_pos <= TOL:
        branch = "HALT(margin)"
        detail = "min positive rc=%.3g" % min_pos
    if zero_off:
        for ai in zero_off:
            u, v, ei, sg = ARCS[ai]
            cobj = np.zeros(len(ARCS)); cobj[ai] = -1.0
            r3 = linprog(c=cobj, A_eq=flowop.AEQ, b_eq=np.zeros(N)-b,
                         A_ub=csr_matrix(TIE_COST.reshape(1, -1)), b_ub=[opt + 1e-9],
                         bounds=(0, None), method="highs")
            maxflow = -r3.fun if r3.success else float('nan')
            can_flow = r3.success and maxflow > 1e-6
            tag = "HALT(alt-optimum)" if can_flow else "REPORT(genuine-tie)"
            print("%-14s arc %s->%s  rc=%.3g maxflow=%.3g -> %s" %
                  (g, ORDER[u], ORDER[v], rc[ai], maxflow, tag))
    if branch != "clean":
        print("%-14s %s %s" % (g, branch, detail))
print("done")
