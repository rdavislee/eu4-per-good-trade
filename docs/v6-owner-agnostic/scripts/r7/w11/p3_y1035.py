# -*- coding: utf-8 -*-
"""Y1035: what the second-order term costs. Compare first-order-only against the shipped
full cost on every quantity the sentence names."""
import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from flowop import ARCS, TIE_EPS, TIE_EPS2, EDGES_UND
from solver import N, ORDER, NIDX, UND, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
wn = (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
a1 = np.array([wn[u] for (u, v, ei, sg) in ARCS]); a2 = np.array([wn[v] for (u, v, ei, sg) in ARCS])
FIRST = 1.0 + TIE_EPS * (a1 + a2) / 2.0
FULL = FIRST + TIE_EPS2 * np.modf(np.minimum(a1, a2) * np.maximum(a1, a2) * 7919.0)[0]
assert np.array_equal(FULL, flowop.TIE_COST), "FULL must equal the shipped TIE_COST"
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
VAL = {g: float(val[g].sum()) for g in GL}
def bagg(w=None):
    w = W if w is None else w
    t = (w / w.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t)
    return np.full(N, 1.0 / N) - n / n.sum()
def report(cost, tag):
    drain.TIE_COST = cost
    base = drain.run_drain(bagg()); BD = set(base["directed"])
    od = collections.Counter(u for u, _ in BD)
    sinks = sorted(ORDER[i] for i in range(N) if od[i] == 0)
    PG = {}; scnt = []
    acyc = 0
    for g in GL:
        r = drain.run_drain(B[g]); PG[g] = set(r["directed"])
        o = collections.Counter(u for u, _ in r["directed"])
        scnt.append(sum(1 for i in range(N) if o[i] == 0))
        acyc += (drain.has_cycle(r["directed"]) is None)
    ag = tot = 0; wag = wtot = 0.0
    for g in GL:
        for u, v in EDGES_UND:
            gd = (u, v) if (u, v) in PG[g] else ((v, u) if (v, u) in PG[g] else None)
            if gd is None: continue
            tot += 1; wtot += VAL[g]
            if ((u, v) if (u, v) in BD else (v, u)) == gd: ag += 1; wag += VAL[g]
    noise = []
    for s in range(6):
        nz = 1 + np.random.default_rng(9000 + s).uniform(-0.01, 0.01, size=len(W))
        d = set(drain.run_drain(bagg(W * nz))["directed"])
        noise.append(len(d ^ BD) // 2)
    print("%-12s Phi_w sinks %-24s sinks/good %d-%d mean %.2f  acyclic %d/29"
          % (tag, ",".join(sinks), min(scnt), max(scnt), float(np.mean(scnt)), acyc))
    print("%-12s self-coherence edge-goods %.1f%%  value-weighted %.1f%%   +/-1%% noise edges moved (6 seeds) %s"
          % ("", 100.0 * ag / tot, 100.0 * wag / wtot, noise))
    return 100.0 * ag / tot, 100.0 * wag / wtot
a = report(FIRST, "first-order")
b = report(FULL, "shipped full")
print("self-coherence delta (full - first): edge-goods %+.2f  value-weighted %+.2f"
      % (b[0] - a[0], b[1] - a[1]))
