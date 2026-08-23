import sys, os
sys.path.insert(0, ".")
import numpy as np
import flowop, drain
from flowop import ARCS, TIE_EPS, TIE_EPS2, EDGES_UND, LP_OPTS
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
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
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    B[g] = val[g] / val[g].sum() - n / n.sum()

# absdiff cost
a1 = np.array([wn[u] for (u, v, ei, sg) in ARCS]); a2 = np.array([wn[v] for (u, v, ei, sg) in ARCS])
ABSDIFF = 1.0 + TIE_EPS * (a1 + a2) / 2.0 + (TIE_EPS**2) * np.abs(a1 - a2)

# find, for 'copper', the tree/support and check for an off-support arc with tiny reduced cost, then check path monotonicity
import scipy.sparse as sp
from scipy.optimize import linprog
AEQ = flowop.AEQ
g = "copper"
core, beta, Plog = drain.phase0(B[g])
bb = np.zeros(N)
for v in core: bb[v] = beta[v]
res = linprog(c=ABSDIFF, A_eq=AEQ, b_eq=-bb, bounds=(0,None), method="highs", options=LP_OPTS)
y = np.asarray(res.eqlin.marginals)
rc = np.array([ABSDIFF[k] - y[v] + y[u] for k,(u,v,ei,sg) in enumerate(ARCS)])
supp = res.x > 1e-11
off = ~supp
idx = np.argsort(np.where(off, np.abs(rc), np.inf))[:5]
for k in idx:
    u,v,ei,sg = ARCS[k]
    print(g, "arc", ORDER[u], "->", ORDER[v], "rc=", rc[k], "own cost", ABSDIFF[k], "wn[u]=%.4f wn[v]=%.4f"%(wn[u],wn[v]))
