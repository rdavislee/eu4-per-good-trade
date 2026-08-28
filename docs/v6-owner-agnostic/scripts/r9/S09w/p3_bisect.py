# -*- coding: utf-8 -*-
"""Tolerance bisection against copper/paper (spec 2.3, Y1054-Y1057) + per-good margins."""
import os, sys, math
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
exec(open(os.path.join(HERE, "p3_perm.py")).read().split("IDENT = list(range(A))")[0])
IDENT = list(range(A))
def solve_perm(b_full, perm, opts):
    from scipy.sparse import csr_matrix
    core, beta, Plog = drain.phase0(b_full)
    bb = np.zeros(N)
    for v in core: bb[v] = beta[v]
    rows, cols, vals = [], [], []
    cost = np.empty(A)
    for newk, k in enumerate(perm):
        u, v, ei, sg = ARCS[k]
        rows += [v, u]; cols += [newk, newk]; vals += [1.0, -1.0]
        cost[newk] = TIE_COST[k]
    Aeq = csr_matrix((vals, (rows, cols)), shape=(N, A))
    res = linprog(c=cost, A_eq=Aeq, b_eq=-bb, bounds=(0, None), method="highs", options=opts)
    if not res.success: raise RuntimeError(res.message)
    net = np.zeros(len(EDGES_UND))
    for newk, k in enumerate(perm):
        u, v, ei, sg = ARCS[k]
        net[ei] += sg * res.x[newk]
    d = {}
    for ei, (u, v) in enumerate(EDGES_UND):
        if net[ei] > ZERO_TOL: d[ei] = (u, v)
        elif net[ei] < -ZERO_TOL: d[ei] = (v, u)
    return d, float(res.fun)
def flips(d0, d1):
    return sum(1 for ei in set(d0) | set(d1) if d0.get(ei) != d1.get(ei))

# ---------------- per-good margins under the shipped full cost ----------------
def margin(b):
    core, beta, _ = drain.phase0(b)
    bb = np.zeros(N)
    for v in core: bb[v] = beta[v]
    res = linprog(c=TIE_COST, A_eq=AEQ, b_eq=-bb, bounds=(0, None), method="highs", options=LP_OPTS)
    y = np.asarray(res.eqlin.marginals)
    rc = np.array([TIE_COST[k] - y[v] + y[u] for k, (u, v, ei, sg) in enumerate(ARCS)])
    off = res.x <= 1e-11
    pos = rc[off & (rc > 1e-9)]
    nz = int((off & (np.abs(rc) <= 1e-9)).sum())
    return (float(pos.min()) if pos.size else float('nan')), nz
print("=" * 90); print("per-good uniqueness margin under the shipped cost (min positive reduced cost)"); print("=" * 90)
mg = {}
for g in GL:
    m, nz = margin(B_GOOD[g]); mg[g] = m
    print("  %-18s margin %.4g   zero-rc arcs off support: %d" % (g, m, nz))
ma, nza = margin(B_AGG)
print("  %-18s margin %.4g   zero-rc arcs off support: %d" % ("AGGREGATE", ma, nza))
print("  worst per good: %s at %.5g" % (min(mg, key=lambda g: mg[g]), min(mg.values())))
print()

# ---------------- bisection over the tolerance, copper & paper ---------------
print("=" * 90); print("tolerance sweep: flips over 4 and 6 permutations, 3 seeds"); print("=" * 90)
TOLS = [None, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10]
for g in ("copper", "paper"):
    print("  %s (margin %.5g)" % (g, mg[g]))
    for t in TOLS:
        opts = {} if t is None else {"dual_feasibility_tolerance": t,
                                     "primal_feasibility_tolerance": t}
        row = []
        for seed in (20260821, 7, 4242):
            rng = np.random.default_rng(seed)
            d0, o0 = solve_perm(B_GOOD[g], IDENT, opts)
            fl = []
            for _ in range(6):
                p = list(rng.permutation(A))
                d, o = solve_perm(B_GOOD[g], p, opts)
                fl.append(flips(d0, d))
            row.append((sum(fl[:4]), sum(fl)))
        print("    tol %-8s  (sum over 4 perms, sum over 6) by seed: %s"
              % ("unset" if t is None else t, row))
