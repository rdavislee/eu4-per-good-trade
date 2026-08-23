# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import numpy as np
import flowop, drain
from flowop import ARCS, AEQ, EDGES_UND, TIE_COST, TIE_EPS, TIE_EPS2, ZERO_TOL, LP_OPTS
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

A = len(ARCS)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

A_PHI = 2.0
def cv(a=A_PHI, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
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

def run(name, b, nperm, opts, seed=20260821):
    rng = np.random.default_rng(seed)
    d0, o0, _ = solve_perm(b, IDENT, opts)
    fl = []; objs = [o0]; changed_edges = set(); flip_events = 0
    for _ in range(nperm):
        p = list(rng.permutation(A))
        d, o, _ = solve_perm(b, p, opts)
        moved = set(ei for ei in set(d0) | set(d) if d0.get(ei) != d.get(ei))
        fl.append(len(moved))
        changed_edges |= moved
        flip_events += len(moved)
        objs.append(o)
    spread = (max(objs) - min(objs)) / max(1e-300, abs(o0))
    return fl, spread, changed_edges, flip_events

DEFAULT = {}
for g in ("copper", "paper"):
    fl, sp, edges, events = run(g, B_GOOD[g], 6, DEFAULT)
    print(g, "flips per perm:", fl, "sum:", sum(fl), "distinct edge-slots:", len(edges), "edges:", edges, "obj rel spread:", sp)
