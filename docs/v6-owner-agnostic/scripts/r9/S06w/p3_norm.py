# -*- coding: utf-8 -*-
"""Y1037/Y1038: the normalisation of w. Rebuild TIE_COST under four normalisations and
re-run the shipped DRAIN (drain.TIE_COST is what phase2 passes)."""
import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from flowop import ARCS, TIE_EPS, TIE_EPS2, EDGES_UND
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
def tie(norm):
    if norm == "minmax": w = (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
    elif norm == "max":  w = NODEW / NODEW.max()
    elif norm == "mean": w = NODEW / NODEW.mean()
    elif norm == "total":w = NODEW / NODEW.sum()
    a1 = np.array([w[u] for (u, v, ei, sg) in ARCS]); a2 = np.array([w[v] for (u, v, ei, sg) in ARCS])
    gen = np.modf(np.minimum(a1, a2) * np.maximum(a1, a2) * 7919.0)[0]
    return 1.0 + TIE_EPS * (a1 + a2) / 2.0 + TIE_EPS2 * gen
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
t = (W / W.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t)
B_AGG = np.full(N, 1.0 / N) - n / n.sum()
def solve_all(norm):
    drain.TIE_COST = tie(norm)
    out = {}
    r = drain.run_drain(B_AGG)
    od = collections.Counter(u for u, _ in r["directed"])
    out["__AGG__"] = (set(r["directed"]), tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0)))
    for g in GL:
        rr = drain.run_drain(B[g])
        o2 = collections.Counter(u for u, _ in rr["directed"])
        out[g] = (set(rr["directed"]), tuple(sorted(ORDER[i] for i in range(N) if o2[i] == 0)))
    return out
base = solve_all("minmax")
print("shipped (min-max) Phi_w sinks:", base["__AGG__"][1])
for norm in ("max", "mean", "total"):
    r = solve_all(norm)
    agg = len(base["__AGG__"][0] ^ r["__AGG__"][0]) // 2
    diff = [g for g in GL if r[g][0] != base[g][0]]
    print("%-6s vs min-max: aggregate edges differing %d/159, sinks %s | per-good graphs differing %d: %s"
          % (norm, agg, "same" if r["__AGG__"][1] == base["__AGG__"][1] else r["__AGG__"][1],
             len(diff), diff))
# also compare the three against each other (the document says "across the three normalisations")
rs = {nm: solve_all(nm) for nm in ("max", "mean", "total")}
agg_pairs = set()
for a in rs:
    for b in rs:
        if a < b: agg_pairs.add((a, b, len(rs[a]["__AGG__"][0] ^ rs[b]["__AGG__"][0]) // 2))
print("pairwise aggregate differences among max/mean/total:", sorted(agg_pairs))
un = [g for g in GL if len({frozenset(rs[nm][g][0]) for nm in rs}) > 1]
print("per-good graphs differing among the three normalisations alone: %d %s" % (len(un), un))
allf = [g for g in GL if len({frozenset(rs[nm][g][0]) for nm in rs} | {frozenset(base[g][0])}) > 1]
print("per-good graphs differing across all four (incl. min-max): %d %s" % (len(allf), allf))
