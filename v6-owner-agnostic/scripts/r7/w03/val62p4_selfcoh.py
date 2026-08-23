# Y1035: self-coherence with the per-good graphs under first-order-only cost vs shipped (full) cost.
import collections, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from flowop import ARCS, AEQ, EDGES_UND, TIE_EPS, TIE_EPS2, ZERO_TOL, LP_OPTS
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc
from scipy.optimize import linprog

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
wn = (NODEW - NODEW.min()) / ((NODEW.max() - NODEW.min()) or 1.0)
a1 = np.array([wn[u] for (u, v, ei, sg) in ARCS])
a2 = np.array([wn[v] for (u, v, ei, sg) in ARCS])
FIRST = 1.0 + TIE_EPS * (a1 + a2) / 2.0

def phase2_lp(b_full, cost, opts=LP_OPTS):
    core, beta, Plog = drain.phase0(b_full)
    bb = np.zeros(N)
    for v in core: bb[v] = beta[v]
    res = linprog(c=cost, A_eq=AEQ, b_eq=-bb, bounds=(0, None), method="highs", options=opts)
    if not res.success: raise RuntimeError(res.message)
    return res

def support_dirs(res, core, Plog, beta):
    net = flowop.net_per_edge(res.x)
    fa = {}
    for ei, (u, v) in enumerate(EDGES_UND):
        if net[ei] > ZERO_TOL: fa[ei] = (u, v)
        elif net[ei] < -ZERO_TOL: fa[ei] = (v, u)
    return fa

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
VAL = {g: np.zeros(N) for _, g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in VAL: VAL[r["good"]][pn[i]] += r["prod_income"]

def full_directed(b, cost):
    r = drain.run_drain(b) if cost is flowop.TIE_COST else None
    if r is not None:
        return set(r["directed"])
    # rebuild via drain.py but override the LP cost by monkeypatching flowop.TIE_COST
    old = flowop.TIE_COST
    flowop.TIE_COST = cost
    try:
        r = drain.run_drain(b)
    finally:
        flowop.TIE_COST = old
    return set(r["directed"])

BW = np.full(N, 1.0 / N) - (lambda: (lambda t: (lambda n: n / n.sum())(
    (lambda n: (np.add.at(n, pn, t), n)[1])(np.zeros(N))))((W / W.max()) ** 2.0))()

for label, cost in (("shipped (full)", flowop.TIE_COST), ("first-order only", FIRST)):
    BD = full_directed(BW, cost)
    PG = {}
    for gi, g in GL:
        b = S[gi] - C[gi]
        PG[g] = full_directed(b, cost)
    ag = tot = 0; wag = wtot = 0.0
    for gi, g in GL:
        for u, v in EDGES_UND:
            gd = (u, v) if (u, v) in PG[g] else ((v, u) if (v, u) in PG[g] else None)
            if gd is None: continue
            tot += 1; wtot += VAL[g][NIDX[ORDER[0]]] if False else 0  # placeholder unused
    # weight by good total value like measure6.py: VAL[g] good's total production value
    goodval = {g: float(VAL[g].sum()) for _, g in GL}
    ag = tot = 0; wag = wtot = 0.0
    for gi, g in GL:
        for u, v in EDGES_UND:
            gd = (u, v) if (u, v) in PG[g] else ((v, u) if (v, u) in PG[g] else None)
            if gd is None: continue
            tot += 1; wtot += goodval[g]
            if ((u, v) if (u, v) in BD else (v, u)) == gd:
                ag += 1; wag += goodval[g]
    print("%-18s self-coherence edge-goods %.1f%%  value-weighted %.1f%%" %
          (label, 100.0*ag/tot, 100.0*wag/wtot))
