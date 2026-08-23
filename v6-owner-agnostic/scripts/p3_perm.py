# -*- coding: utf-8 -*-
"""LP column-permutation experiments for spec 2.1's table and 2.3's tolerance paragraph.

Validation: with the identity permutation and LP_OPTS the support must equal drain.phase2's.
"""
import collections, os, sys, math, json
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from flowop import ARCS, AEQ, EDGES_UND, TIE_COST, TIE_EPS, TIE_EPS2, ZERO_TOL, LP_OPTS
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

A = len(ARCS)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
_wn = (NODEW - NODEW.min()) / ((NODEW.max() - NODEW.min()) or 1.0)

A_PHI = 2.0
def cv(a=A_PHI, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
B_AGG = np.full(N, 1.0 / N) - cv()
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
B_GOOD = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    B_GOOD[g] = (val[g] / val[g].sum()) - n / n.sum()

def solve_perm(b_full, perm, opts):
    """Phase 2's LP with its arc columns in order `perm`. Returns (edge->dir map, objective)."""
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
    return d, float(res.fun), net

IDENT = list(range(A))

# --------------------------------------------------------- validation --------
print("=" * 92); print("VALIDATION: identity column order reproduces drain.phase2"); print("=" * 92)
bad = 0
for name, b in [("aggregate", B_AGG)] + [(g, B_GOOD[g]) for g in GL]:
    core, beta, _ = drain.phase0(b)
    fa, free, net, obj = drain.phase2(core, beta)
    d, o, _ = solve_perm(b, IDENT, LP_OPTS)
    if d != fa or abs(o - obj) > 1e-12:
        bad += 1; print("  MISMATCH", name, len(d), len(fa), o, obj)
print("  %d of %d reproduce exactly" % (1 + len(GL) - bad, 1 + len(GL)))
if bad: sys.exit("INSTRUMENT FAILED VALIDATION")

def flips(d0, d1):
    return sum(1 for ei in set(d0) | set(d1) if d0.get(ei) != d1.get(ei))

def run(name, b, nperm, opts, seed=20260821):
    rng = np.random.default_rng(seed)
    d0, o0, _ = solve_perm(b, IDENT, opts)
    fl = []; objs = [o0]
    for _ in range(nperm):
        p = list(rng.permutation(A))
        d, o, _ = solve_perm(b, p, opts)
        fl.append(flips(d0, d))
        objs.append(o)
    spread = (max(objs) - min(objs)) / max(1e-300, abs(o0))
    return fl, spread

print()
print("=" * 92); print("A. spec 2.1 table: orientation under LP column permutation, LP_OPTS=1e-10"); print("=" * 92)
NP = 6
tot_moved = 0
fl, sp = run("aggregate", B_AGG, NP, LP_OPTS)
print("  aggregate : flips %s   objective rel spread %.3g" % (fl, sp))
tot_moved += sum(1 for x in fl if x)
allsp = [sp]
for g in GL:
    fl, sp = run(g, B_GOOD[g], NP, LP_OPTS)
    allsp.append(sp)
    if any(fl): print("  %-16s flips %s  spread %.3g" % (g, fl, sp)); tot_moved += 1
print("  goods/aggregate with any flip over %d permutations: %d of %d" % (NP, tot_moved, 1 + len(GL)))
print("  max objective relative spread over all 30 solves: %.3g" % max(allsp))

print()
print("=" * 92); print("B. spec 2.3: same at HiGHS default tolerance (options omitted)"); print("=" * 92)
DEFAULT = {}
res_default = {}
fl, sp = run("aggregate", B_AGG, NP, DEFAULT)
print("  aggregate : flips %s  spread %.3g" % (fl, sp))
for g in GL:
    fl, sp = run(g, B_GOOD[g], NP, DEFAULT)
    res_default[g] = (fl, sp)
    if any(fl): print("  %-16s flips %s  max spread %.3g" % (g, fl, sp))
print("  goods with any flip: %s" % [g for g in GL if any(res_default[g][0])])
