# -*- coding: utf-8 -*-
"""Re-derive spec 2.1/2.3's LP-degeneracy figures from the shipped solver.

Instrument validation (mandatory before any figure is trusted): for every b this script
solves, the support it extracts from its own LP call must equal drain.phase2's flow_arc
on the same b, computed by the shipped code.  The script aborts otherwise.
"""
import collections, os, sys, math
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from flowop import ARCS, AEQ, EDGES_UND, TIE_COST, TIE_EPS, TIE_EPS2, ZERO_TOL, LP_OPTS
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from scipy.optimize import linprog

A = len(ARCS)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)

def wn(mode="minmax"):
    if mode == "minmax":
        return (NODEW - NODEW.min()) / ((NODEW.max() - NODEW.min()) or 1.0)
    if mode == "max":  return NODEW / NODEW.max()
    if mode == "mean": return NODEW / NODEW.mean()
    if mode == "total":return NODEW / NODEW.sum()
    raise ValueError(mode)

def cost_vec(kind, norm="minmax"):
    w = wn(norm)
    a1 = np.array([w[u] for (u, v, ei, sg) in ARCS])
    a2 = np.array([w[v] for (u, v, ei, sg) in ARCS])
    if kind == "unit":  return np.ones(A)
    if kind == "first": return 1.0 + TIE_EPS * (a1 + a2) / 2.0
    if kind == "full":
        gen = np.modf(np.minimum(a1, a2) * np.maximum(a1, a2) * 7919.0)[0]
        return 1.0 + TIE_EPS * (a1 + a2) / 2.0 + TIE_EPS2 * gen
    if kind == "absdiff":
        return 1.0 + TIE_EPS * (a1 + a2) / 2.0 + (TIE_EPS ** 2) * np.abs(a1 - a2)
    raise ValueError(kind)

# --------------------------------------------------------------- b vectors ---
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

# ------------------------------------------------- the LP that phase2 runs ---
def phase2_lp(b_full, cost, opts=LP_OPTS):
    """Exactly drain.phase2's LP: peel, then s=beta on the core, c=0."""
    core, beta, Plog = drain.phase0(b_full)
    bb = np.zeros(N)
    for v in core: bb[v] = beta[v]
    res = linprog(c=cost, A_eq=AEQ, b_eq=-bb, bounds=(0, None), method="highs",
                  options=opts)
    if not res.success: raise RuntimeError(res.message)
    y = np.asarray(res.eqlin.marginals)
    # reduced cost of arc a (col = e_v - e_u):  c_a - y_v + y_u
    rc = np.array([cost[k] - y[v] + y[u] for k, (u, v, ei, sg) in enumerate(ARCS)])
    supp = res.x > 1e-11
    return core, beta, res, rc, supp, Plog

def support_edges(res):
    net = flowop.net_per_edge(res.x)
    out = {}
    for ei, (u, v) in enumerate(EDGES_UND):
        if net[ei] > ZERO_TOL: out[ei] = (u, v)
        elif net[ei] < -ZERO_TOL: out[ei] = (v, u)
    return out

# ------------------------------------------------------------- VALIDATION ----
print("=" * 90); print("INSTRUMENT VALIDATION against drain.phase2 (shipped)"); print("=" * 90)
bad = 0
for name, b in [("aggregate", B_AGG)] + [(g, B_GOOD[g]) for g in GL]:
    core, beta, Plog = drain.phase0(b)
    fa_ship, free_ship, net_ship, cost_ship = drain.phase2(core, beta)
    core2, beta2, res, rc, supp, _ = phase2_lp(b, TIE_COST)
    fa_mine = {ei: e for ei, e in support_edges(res).items()
               if ei in fa_ship or ei in free_ship}
    same = (fa_mine == fa_ship) and abs(res.fun - cost_ship) < 1e-12
    if not same:
        bad += 1
        print("  MISMATCH %-12s ship=%d mine=%d obj %.15g vs %.15g"
              % (name, len(fa_ship), len(fa_mine), cost_ship, res.fun))
print("  %d of %d b-vectors reproduce drain.phase2's support and objective exactly"
      % (1 + len(GL) - bad, 1 + len(GL)))
if bad:
    sys.exit("INSTRUMENT FAILED VALIDATION - no figure below is usable")

# ------------------------------------------- zero-reduced-cost arc counts ----
def zrc(b, kind, thresh=1e-9, norm="minmax"):
    c = cost_vec(kind, norm)
    core, beta, res, rc, supp, _ = phase2_lp(b, c)
    off = ~supp
    n0 = int(((np.abs(rc) <= thresh) & off).sum())
    pos = rc[off & (np.abs(rc) > thresh)]
    return n0, (float(pos.min()) if pos.size else float("nan")), float(res.fun)

print()
print("=" * 90); print("ZERO-REDUCED-COST ARCS OUTSIDE THE SUPPORT (threshold 1e-9)"); print("=" * 90)
for kind in ("unit", "first", "full", "absdiff"):
    n_ag, m_ag, _ = zrc(B_AGG, kind)
    per = {g: zrc(B_GOOD[g], kind) for g in GL}
    tot = sum(v[0] for v in per.values())
    ngoods = sum(1 for v in per.values() if v[0] > 0)
    margins = [v[1] for v in per.values() if not math.isnan(v[1])]
    print("%-9s aggregate %3d (margin %.4g) | per-good total %3d on %2d of %d goods"
          " | worst per-good margin %.4g"
          % (kind, n_ag, m_ag, tot, ngoods, len(GL), min(margins)))
    if kind in ("full", "absdiff"):
        print("           goods still carrying one: %s"
              % {g: v[0] for g, v in per.items() if v[0] > 0})

print()
print("=" * 90); print("DISTINCTNESS OF ARC COSTS (per undirected edge, 159)"); print("=" * 90)
for kind in ("unit", "first", "full", "absdiff"):
    c = cost_vec(kind)
    per_edge = {}
    for k, (u, v, ei, sg) in enumerate(ARCS):
        per_edge[ei] = c[k]
    vals = sorted(per_edge.values())
    nd = len(set(vals))
    dup = len(vals) - nd
    print("%-9s %d distinct of %d edge costs; %d duplicate slots" % (kind, nd, len(vals), dup))
