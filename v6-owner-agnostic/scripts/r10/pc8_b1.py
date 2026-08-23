# -*- coding: utf-8 -*-
"""B1 + C8: copper flip counts under column permutation, two constructions, many seeds."""
import os, sys, io, contextlib
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import flowop, drain
from flowop import ARCS, AEQ, TIE_COST, ZERO_TOL
from solver import N, GOODS, PRICES, EDGES_UND, build_sc

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
gi = GOODS.index("copper"); B = S[gi] - C[gi]

def orient_r6(tol, perm, b):
    opts = None if tol is None else {"dual_feasibility_tolerance": tol,
                                     "primal_feasibility_tolerance": tol}
    cost = TIE_COST[perm]; aeq = AEQ[:, perm]
    with contextlib.redirect_stderr(io.StringIO()):
        r = linprog(c=cost, A_eq=aeq, b_eq=np.zeros(N) - b, bounds=(0, None),
                    method="highs", options=opts)
    x = np.zeros(len(ARCS)); x[perm] = r.x
    net = np.zeros(len(EDGES_UND))
    for ai, (_u, _v, ei, sg) in enumerate(ARCS):
        net[ei] += sg * x[ai]
    return tuple(np.sign(np.where(np.abs(net) > 1e-11, net, 0.0)).astype(int))

def flipset(tol, seed, nperm=4, b=B):
    rng = np.random.default_rng(seed)
    perms = [np.arange(len(ARCS))] + [rng.permutation(len(ARCS)) for _ in range(nperm)]
    ref = orient_r6(tol, perms[0], b)
    fset = set()
    for pi, p in enumerate(perms[1:], 1):
        got = orient_r6(tol, p, b)
        for slot, (a, bb) in enumerate(zip(ref, got)):
            if a != bb: fset.add((pi, slot))
    return fset

print("== round6.py mechanism, seed 4 (shipped), by tolerance ==")
sets = {}
for tol in (None, 1e-7, 1e-8, 1e-10, 1e-11):
    s = flipset(tol, 4); sets[tol] = s
    print("   tol %-8s count=%d" % ("unset" if tol is None else tol, len(s)))
print("   set identity unset==1e-7 :", sets[None] == sets[1e-7])
print("   1e-8 empty:", sets[1e-8] == set(), "  1e-10 empty:", sets[1e-10] == set())
print("   rejected 1e-11 == unset:", sets[1e-11] == sets[None])

print()
print("== B1: round6.py mechanism swept over seeds 0-30, tolerance unset ==")
vals = {}
for seed in range(31):
    n = len(flipset(None, seed)); vals[seed] = n
print("   per-seed:", vals)
import collections
print("   distinct values:", sorted(set(vals.values())))
print("   histogram:", dict(sorted(collections.Counter(vals.values()).items())))
print("   min=%d max=%d ; 2 occurs? %s" % (min(vals.values()), max(vals.values()), 2 in vals.values()))

print()
print("== B1: p3_bisect.py's three seeds (20260821, 7, 4242), 6 perms drawn, first 4 summed ==")
def p3_count(tol, seed):
    rng = np.random.default_rng(seed)
    perms = [rng.permutation(len(ARCS)) for _ in range(6)]
    ref = orient_r6(tol, np.arange(len(ARCS)), B)
    fl = []
    for p in perms:
        got = orient_r6(tol, p, B)
        fl.append(sum(1 for a, b in zip(ref, got) if a != b))
    return sum(fl[:4]), sum(fl)
for tol in (None, 1e-7, 1e-8):
    for seed in (20260821, 7, 4242):
        print("   tol %-8s seed %-10s -> (4perm, 6perm) = %s" % ("unset" if tol is None else tol, seed, p3_count(tol, seed)))
