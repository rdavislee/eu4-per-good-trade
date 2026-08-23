import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import numpy as np
import flowop, drain
from flowop import ARCS, AEQ, EDGES_UND, TIE_COST, ZERO_TOL, LP_OPTS
from solver import N, GOODS, PRICES, ROWS, build_sc
from scipy.optimize import linprog

A = len(ARCS)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
from solver import NIDX
pn = np.array([NIDX[r["node"]] for r in ROWS])
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

def solve_ident(b_full, opts):
    core, beta, Plog = drain.phase0(b_full)
    bb = np.zeros(N)
    for v in core: bb[v] = beta[v]
    res = linprog(c=TIE_COST, A_eq=AEQ, b_eq=-bb, bounds=(0, None), method="highs", options=opts)
    if not res.success: raise RuntimeError(res.message)
    net = np.zeros(len(EDGES_UND))
    for k, (u, v, ei, sg) in enumerate(ARCS):
        net[ei] += sg * res.x[k]
    d = {}
    for ei, (u, v) in enumerate(EDGES_UND):
        if net[ei] > ZERO_TOL: d[ei] = (u, v)
        elif net[ei] < -ZERO_TOL: d[ei] = (v, u)
    return d, float(res.fun)

mismatches = 0
for name, b in [("aggregate", B_AGG)] + [(g, B_GOOD[g]) for g in GL]:
    d_def, o_def = solve_ident(b, None)
    d_pin, o_pin = solve_ident(b, LP_OPTS)
    if d_def != d_pin or abs(o_def - o_pin) > 1e-9:
        mismatches += 1
        print("MISMATCH", name, "obj", o_def, o_pin, "edges differ:", set(d_def.items()) ^ set(d_pin.items()))
print("checked", 1+len(GL), "b-vectors; mismatches between default-tol IDENT and pinned-tol IDENT:", mismatches)
