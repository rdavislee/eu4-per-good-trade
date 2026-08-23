# -*- coding: utf-8 -*-
"""Lead probe: copper flip count over four column permutations, seeds 0-30, HiGHS default tolerance.
Same counting rule as p3_bisect.py: sum of distinct per-permutation flips against the identity order."""
import os, sys, collections
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE)
os.chdir(HERE)
exec(open(os.path.join(HERE, "p3_perm.py")).read().split("IDENT = list(range(A))")[0])
IDENT = list(range(A))
from scipy.sparse import csr_matrix


def solve_perm(b_full, perm, opts):
    core, beta, Plog = drain.phase0(b_full)
    bb = np.zeros(N)
    for v in core:
        bb[v] = beta[v]
    rows, cols, vals = [], [], []
    cost = np.empty(A)
    for newk, k in enumerate(perm):
        u, v, ei, sg = ARCS[k]
        rows += [v, u]; cols += [newk, newk]; vals += [1.0, -1.0]
        cost[newk] = TIE_COST[k]
    Aeq = csr_matrix((vals, (rows, cols)), shape=(N, A))
    res = linprog(c=cost, A_eq=Aeq, b_eq=-bb, bounds=(0, None), method="highs", options=opts)
    if not res.success:
        raise RuntimeError(res.message)
    net = np.zeros(len(EDGES_UND))
    for newk, k in enumerate(perm):
        u, v, ei, sg = ARCS[k]
        net[ei] += sg * res.x[newk]
    d = {}
    for ei, (u, v) in enumerate(EDGES_UND):
        if net[ei] > ZERO_TOL:
            d[ei] = (u, v)
        elif net[ei] < -ZERO_TOL:
            d[ei] = (v, u)
    return d


def flips(d0, d1):
    return sum(1 for ei in set(d0) | set(d1) if d0.get(ei) != d1.get(ei))


g = "copper"
b = B_GOOD[g]
counts = {}
for opts, label in (({}, "unset(default)"),):
    d0 = solve_perm(b, IDENT, opts)
    for seed in range(31):
        rng = np.random.default_rng(seed)
        tot = 0
        for _ in range(4):
            p = list(rng.permutation(A))
            tot += flips(d0, solve_perm(b, p, opts))
        counts[seed] = tot
        print("  seed %-3d  flips over 4 perms = %d" % (seed, tot))
vals = list(counts.values())
c = collections.Counter(vals)
print()
print("seeds 0-30: min %d max %d" % (min(vals), max(vals)))
print("distribution:", dict(sorted(c.items())))
print("most common:", c.most_common(3))
# named seeds
d0 = solve_perm(b, IDENT, {})
for seed in (20260821, 7, 4242):
    rng = np.random.default_rng(seed)
    tot = sum(flips(d0, solve_perm(b, list(rng.permutation(A)), {})) for _ in range(4))
    print("named seed %-10d flips over 4 perms = %d" % (seed, tot))
