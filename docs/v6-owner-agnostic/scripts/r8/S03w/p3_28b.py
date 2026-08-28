import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from drain import run_drain, sinks_of
from flowop import EDGES_UND, TIE_COST
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
C = {}; S = {}; B = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    C[g] = n / n.sum(); S[g] = val[g] / val[g].sum(); B[g] = S[g] - C[g]
R = {g: run_drain(B[g]) for g in GL}
SK = {g: sorted(ORDER[i] for i in sinks_of(R[g]["directed"])[0]) for g in GL}
print("graph SOURCES (in-degree 0):")
for g in ("spices", "cloves"):
    ind = collections.Counter(v for _, v in R[g]["directed"])
    print("  %-7s %s" % (g, sorted(ORDER[i] for i in range(N) if ind[i] == 0)))
print()
zero_c = [ORDER[i] for i in range(N) if C[GL[0]][i] == 0]
print("nodes with zero demand share:", zero_c)
print()
print("barbell variants (46/232 and 16/232 claimed):")
for label, restrict in (("all 80 nodes", False), ("only nodes with c>0", True)):
    top = bot = 0
    for g in GL:
        idx = [i for i in range(N) if (not restrict or C[g][i] > 0)]
        order = sorted(idx, key=lambda i: -C[g][i])
        sk = {NIDX[s] for s in SK[g]}
        top += sum(1 for i in order[:8] if i in sk)
        bot += sum(1 for i in order[-8:] if i in sk)
    print("  %-22s top8 %3d/232 = %.1f%%   bottom8 %3d/232 = %.1f%%"
          % (label, top, 100.0*top/232, bot, 100.0*bot/232))
print()
print("razed-China flip count under both costs:")
def bagg(w):
    t = (w / w.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t)
    return np.full(N, 1.0 / N) - n / n.sum()
import numpy as _np
for tag, cost in (("TIE_COST (shipped)", TIE_COST), ("unit (pre-tie-break)", _np.ones(len(TIE_COST)))):
    drain.TIE_COST = cost
    BD = set(run_drain(bagg(W))["directed"])
    for nm in ("hangzhou", "beijing"):
        w2 = W.copy()
        for i, r in enumerate(ROWS):
            if r["node"] == nm: w2[i] = 0.0
        r2 = run_drain(bagg(w2)); d2 = set(r2["directed"])
        print("  %-22s zero %-9s sinks %-32s flips %d"
              % (tag, nm, sorted(ORDER[i] for i in sinks_of(r2["directed"])[0]), len(d2 ^ BD)//2))
