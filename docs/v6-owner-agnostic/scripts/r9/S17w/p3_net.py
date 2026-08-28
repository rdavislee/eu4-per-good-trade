# -*- coding: utf-8 -*-
"""spec 2.1 free-versus-flow margin (Y1015) and the LP_OPTS objective spread (Y1014/Y1033)."""
import os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from flowop import ARCS, AEQ, EDGES_UND, TIE_COST, ZERO_TOL, LP_OPTS
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
A = len(ARCS)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
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
def cvag(a=2.0):
    t = (W / W.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
B_AGG = np.full(N, 1.0 / N) - cvag()

# ---- Y1015: per-good |net| distribution over the 29 goods x 159 edges --------
allnet = []
for g in GL:
    core, beta, _ = drain.phase0(B_GOOD[g])
    fa, free, net, obj = drain.phase2(core, beta)      # SHIPPED phase2
    allnet.append(np.abs(net))
allnet = np.concatenate(allnet)
print("edge-goods total                :", allnet.size, "(29 x %d)" % len(EDGES_UND))
print("exactly 0.0                     :", int((allnet == 0.0).sum()))
print("in (0, 1e-11]                   :", int(((allnet > 0) & (allnet <= 1e-11)).sum()))
print("in (1e-11, 1e-6]                :", int(((allnet > 1e-11) & (allnet <= 1e-6)).sum()))
print("above 1e-6                      :", int((allnet > 1e-6).sum()))
nz = allnet[allnet > 0]
print("smallest strictly positive |net|:", nz.min())
print("largest zero-side value         :", allnet[allnet == 0.0].size and 0.0)

# ---- objective spread under LP column permutation, 30 permutations ----------
def solve_perm(b_full, perm, opts):
    core, beta, _ = drain.phase0(b_full)
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
    return float(res.fun)
print()
rng = np.random.default_rng(11)
worst = 0.0; where = None
for name, b in [("aggregate", B_AGG)] + [(g, B_GOOD[g]) for g in GL]:
    o0 = solve_perm(b, list(range(A)), LP_OPTS)
    os_ = [o0] + [solve_perm(b, list(rng.permutation(A)), LP_OPTS) for _ in range(20)]
    sp = (max(os_) - min(os_)) / abs(o0)
    if sp > worst: worst, where = sp, name
print("max objective relative spread, 21 column orders x 30 solves: %.4g  (at %s)" % (worst, where))
