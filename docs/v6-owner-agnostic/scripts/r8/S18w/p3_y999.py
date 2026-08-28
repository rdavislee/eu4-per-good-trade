# -*- coding: utf-8 -*-
"""Y999 (absdiff variant) and Y143's 84/290 baseline, measured several ways so the
denominator the document quotes can be identified."""
import collections, io, os, sys, types
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from solver import N, ORDER, NIDX, EDGES_UND, ROWS, GOODS, PRICES, build_sc
import drain as DR
from flowop import TIE_EPS, TIE_EPS2, LP_OPTS, ARCS, AEQ, ZERO_TOL
A = len(ARCS)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
wn = (NODEW - NODEW.min()) / ((NODEW.max() - NODEW.min()) or 1.0)
a1 = np.array([wn[u] for (u, v, ei, sg) in ARCS]); a2 = np.array([wn[v] for (u, v, ei, sg) in ARCS])
COSTS = {
 "unit":    np.ones(A),
 "first":   1.0 + TIE_EPS * (a1 + a2) / 2.0,
 "full":    1.0 + TIE_EPS * (a1 + a2) / 2.0 + TIE_EPS2 * np.modf(np.minimum(a1,a2)*np.maximum(a1,a2)*7919.0)[0],
 "absdiff": 1.0 + TIE_EPS * (a1 + a2) / 2.0 + (TIE_EPS**2) * np.abs(a1 - a2),
}
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
B = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    B[g] = val[g] / val[g].sum() - n / n.sum()

def support_colperm(b_full, cost, perm, opts):
    core, beta, _ = DR.phase0(b_full)
    bb = np.zeros(N)
    for v in core: bb[v] = beta[v]
    rows, cols, vals = [], [], []
    c = np.empty(A)
    for newk, k in enumerate(perm):
        u, v, ei, sg = ARCS[k]
        rows += [v, u]; cols += [newk, newk]; vals += [1.0, -1.0]; c[newk] = cost[k]
    Aeq = csr_matrix((vals, (rows, cols)), shape=(N, A))
    res = linprog(c=c, A_eq=Aeq, b_eq=-bb, bounds=(0, None), method="highs", options=opts)
    net = np.zeros(len(EDGES_UND))
    for newk, k in enumerate(perm):
        u, v, ei, sg = ARCS[k]
        net[ei] += sg * res.x[newk]
    return frozenset((ei, 1 if net[ei] > ZERO_TOL else -1) for ei in range(len(EDGES_UND))
                     if abs(net[ei]) > ZERO_TOL)

IDENT = list(range(A))
print("SUPPORT under LP COLUMN permutation, 8 per good (232 runs), 3 seeds")
for kind in ("first", "full", "absdiff"):
    for opts, tag in ((dict(), "default"), (LP_OPTS, "1e-10")):
        line = []
        for seed in (20260821, 7, 4242):
            rng = np.random.default_rng(seed); moved = 0; gm = set()
            for g in GL:
                base = support_colperm(B[g], COSTS[kind], IDENT, opts)
                for _ in range(8):
                    s = support_colperm(B[g], COSTS[kind], list(rng.permutation(A)), opts)
                    if s != base: moved += 1; gm.add(g)
            line.append((moved, len(gm)))
        print("  %-8s tol=%-8s moved/232 (goods) by seed: %s" % (kind, tag, line))
