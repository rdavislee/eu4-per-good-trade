# -*- coding: utf-8 -*-
"""Y1038, settled. Rebuild TIE_COST under every candidate normalisation of node wealth and
re-run the SHIPPED drain.run_drain (all phases), at the pinned tolerance and at HiGHS's default.

Guards against each construction error that could produce a wrong answer:
  * frac() is applied AFTER rescaling (rescale w, then frac(lo*hi*7919)) -- the only order that
    corresponds to "normalising w";
  * the full two-term cost is rebuilt from the rescaled w, not patched term-by-term;
  * drain.run_drain is called, so Phases 0/1/3/4 see the new field, not just the LP support;
  * LP_OPTS is exercised explicitly as a variable, because at HiGHS's 1e-7 default copper and
    paper return unequal-quality answers and would inflate any per-good difference count;
  * /total and /total*N are BOTH measured, because they are not the same thing.

Validation: tie("minmax") must be bit-identical to flowop.TIE_COST, and the minmax run must
reproduce the shipped map, or the script aborts.
"""
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

def wn_of(norm):
    if norm == "minmax":  return (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
    if norm == "max":     return NODEW / NODEW.max()
    if norm == "mean":    return NODEW / NODEW.mean()
    if norm == "total":   return NODEW / NODEW.sum()
    if norm == "totalxN": return N * NODEW / NODEW.sum()
    raise ValueError(norm)

def tie(norm):
    w = wn_of(norm)
    a1 = np.array([w[u] for (u, v, ei, sg) in ARCS])
    a2 = np.array([w[v] for (u, v, ei, sg) in ARCS])
    gen = np.modf(np.minimum(a1, a2) * np.maximum(a1, a2) * 7919.0)[0]   # frac AFTER rescaling
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

def solve_all(norm, opts):
    drain.TIE_COST = tie(norm)
    def mcf(s, c, cost=None):
        res = linprog(c=(np.ones(len(ARCS)) if cost is None else cost), A_eq=AEQ, b_eq=c - s,
                      bounds=(0, None), method="highs", options=opts)
        if not res.success: raise RuntimeError(res.message)
        du = np.asarray(res.eqlin.marginals) if getattr(res, "eqlin", None) is not None else None
        return res.x, du, res
    old = drain.mincost_flow; drain.mincost_flow = mcf
    out = {}
    for k, b in [("__AGG__", B_AGG)] + [(g, B[g]) for g in GL]:
        r = drain.run_drain(b)
        od = collections.Counter(u for u, _ in r["directed"])
        out[k] = (frozenset(r["directed"]),
                  tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0)))
    drain.mincost_flow = old
    return out

# ------------------------------------------------------------------ VALIDATION
print("=" * 96); print("VALIDATION"); print("=" * 96)
same = bool(np.array_equal(tie("minmax"), flowop.TIE_COST))
print("  tie('minmax') is bit-identical to flowop.TIE_COST : %s" % same)
if not same: sys.exit("ABORT: the cost rebuild does not reproduce the shipped cost")
drain.TIE_COST = flowop.TIE_COST
ship = drain.run_drain(B_AGG); SHIP_E = frozenset(ship["directed"])
_od = collections.Counter(u for u, _ in ship["directed"])
SHIP_S = tuple(sorted(ORDER[i] for i in range(N) if _od[i] == 0))
base = solve_all("minmax", LP_OPTS)
ok = base["__AGG__"] == (SHIP_E, SHIP_S)
print("  minmax @ LP_OPTS reproduces the shipped map        : %s  %s" % (ok, SHIP_S))
if not ok: sys.exit("ABORT")
print("  /mean and /totalxN are the same vector             : %s"
      % bool(np.allclose(wn_of("mean"), wn_of("totalxN"), rtol=0, atol=0)))
print("  wn magnitudes: %s"
      % {k: "[%.4g, %.4g]" % (wn_of(k).min(), wn_of(k).max())
         for k in ("minmax", "max", "mean", "total", "totalxN")})

# ---------------------------------------------------------------------- TABLE
for tag, opts in (("LP_OPTS 1e-10 (shipped)", LP_OPTS), ("HiGHS default", {})):
    print()
    print("=" * 96); print("against min-max, %s" % tag); print("=" * 96)
    b0 = solve_all("minmax", opts)
    print("  %-9s %-14s %-16s %s" % ("norm", "agg edges dif", "per-good graphs", "per-good sink sets"))
    res = {}
    for norm in ("max", "mean", "total", "totalxN"):
        r = solve_all(norm, opts); res[norm] = r
        agg = len(r["__AGG__"][0] ^ b0["__AGG__"][0]) // 2
        gd = [g for g in GL if r[g][0] != b0[g][0]]
        sd = [g for g in GL if r[g][1] != b0[g][1]]
        print("  %-9s %-14s %-16s %s" % (norm, "%d / 159" % agg,
                                         "%d / 29" % len(gd), "%d / 29" % len(sd)))
        if gd: print("            graphs: %s" % gd)
    un = sorted({g for norm in res for g in GL if res[norm][g][0] != b0[g][0]})
    print("  union over max/mean/total/totalxN, vs min-max : %d of 29 %s" % (len(un), un))
    un3 = sorted({g for norm in ("max", "mean", "totalxN") for g in GL
                  if res[norm][g][0] != b0[g][0]})
    print("  union over max/mean/totalxN only              : %d of 29 %s" % (len(un3), un3))
    aggs = sorted({len(res[a]["__AGG__"][0] ^ res[b]["__AGG__"][0]) // 2
                   for a in res for b in res if a < b})
    print("  pairwise aggregate differences among the four : %s" % aggs)
