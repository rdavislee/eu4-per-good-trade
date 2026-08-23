# -*- coding: utf-8 -*-
"""Y1034 (nothing moved when the tolerance was pinned) and Y996's algebra, numerically."""
import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from flowop import ARCS, AEQ, EDGES_UND, TIE_COST, TIE_EPS, ZERO_TOL, LP_OPTS
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc
from scipy.optimize import linprog
A = len(ARCS)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
wn = (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
B = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t); B[g] = val[g]/val[g].sum() - n/n.sum()
t = (W / W.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t); B["__AGG__"] = np.full(N, 1.0/N) - n/n.sum()

# ---- Y1034: shipped column order, default tolerance vs LP_OPTS ---------------
def graph(b, opts):
    orig = flowop.LP_OPTS
    def mcf(s, c, cost=None):
        res = linprog(c=(np.ones(A) if cost is None else cost), A_eq=AEQ, b_eq=c - s,
                      bounds=(0, None), method="highs", options=opts)
        if not res.success: raise RuntimeError(res.message)
        du = np.asarray(res.eqlin.marginals) if getattr(res, "eqlin", None) is not None else None
        return res.x, du, res
    old = drain.mincost_flow; drain.mincost_flow = mcf
    r = drain.run_drain(b)
    drain.mincost_flow = old
    od = collections.Counter(u for u, _ in r["directed"])
    return set(r["directed"]), tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0))
diff = []
for k, b in B.items():
    d1, s1 = graph(b, LP_OPTS); d2, s2 = graph(b, {})
    if d1 != d2 or s1 != s2: diff.append((k, len(d1 ^ d2)//2))
print("Y1034: b-vectors whose graph differs between LP_OPTS(1e-10) and HiGHS default,"
      " shipped column order: %d of %d %s" % (len(diff), len(B), diff))

# ---- Y996: an antisymmetric term's total is constant over feasible routings ---
print()
core, beta, _ = drain.phase0(B["__AGG__"])
bb = np.zeros(N)
for v in core: bb[v] = beta[v]
dirc = np.array([-(wn[v] - wn[u]) for (u, v, ei, sg) in ARCS])       # the -(w[v]-w[u]) part
tot = []
rng = np.random.default_rng(3)
for trial in range(8):
    c = 1.0 + rng.uniform(-1e-3, 1e-3, size=A)     # arbitrary cost -> different routings
    res = linprog(c=c, A_eq=AEQ, b_eq=-bb, bounds=(0, None), method="highs", options=LP_OPTS)
    tot.append(float(dirc @ res.x))
print("Y996: total of the antisymmetric term over 8 different feasible optima:")
print("   values %s" % ["%.12f" % x for x in tot])
print("   spread %.3e   |   sum_n w[n]*b_eq[n] = %.12f"
      % (max(tot) - min(tot), float(wn @ (-(-bb)))))
print("   (predicted constant = -sum_n w[n]*b_eq[n] = %.12f)" % float(-(wn @ (-bb))))
