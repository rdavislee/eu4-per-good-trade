# -*- coding: utf-8 -*-
"""How large is the relabelling effect on 1444, and is it genuine LP degeneracy
(equal optimal cost, different vertex)?"""
import sys, random
import numpy as np
sys.path.insert(0, "C:/Users/rdavi/OneDrive/Documents/Paradox Interactive/Europa Universalis IV/mod/per-good-trade/v5-owner-agnostic/scripts")
from _audit_b_drain import drain
from solver import N, ORDER, GOODS, PRICES, build_sc, EDGES_UND
from drain import NODEW
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
NAMES = list(map(str, range(N))); EDGES = [tuple(e) for e in EDGES_UND]
rng = random.Random(31337)
def relabel(edges, b, w, p):
    e2 = sorted(tuple(sorted((p[u], p[v]))) for u, v in edges)
    b2 = [0.]*N; w2 = [0.]*N
    for i in range(N): b2[p[i]] = b[i]; w2[p[i]] = w[i]
    return e2, b2, w2
rows = []
for gi, g in enumerate(GOODS):
    if not LIVE[gi]: continue
    b = list(S[gi] - C[gi])
    r = drain(NAMES, EDGES, b, wealth=list(NODEW))
    base = set(r["directed"]); cost0 = float(np.abs(r["net"]).sum())
    sk0 = r["sinks"]
    ds = []; costs = []; sinkdiff = []
    for t in range(10):
        p = list(range(N)); rng.shuffle(p)
        e2, b2, w2 = relabel(EDGES, b, list(NODEW), p)
        r2 = drain(NAMES, e2, b2, wealth=w2)
        inv = {p[i]: i for i in range(N)}
        back = set((inv[u], inv[v]) for u, v in r2["directed"])
        flips = sum(1 for (u, v) in base if (v, u) in back)
        ds.append(flips); costs.append(float(np.abs(r2["net"]).sum()))
        sinkdiff.append(len(set(inv[x] for x in r2["sinks"]) ^ sk0))
    rows.append((g, min(ds), max(ds), np.mean(ds), cost0, min(costs), max(costs), max(sinkdiff)))
print("%-15s %5s %5s %7s | %12s %12s | %s" % ("good","min","max","mean","cost base","cost relab range","max sink-set symdiff"))
for g, a, bmax, m, c0, cmin, cmax, sd in rows:
    print("%-15s %5d %5d %7.1f | %12.6f %.6f..%.6f | %d" % (g, a, bmax, m, c0, cmin, cmax, sd))
allmean = np.mean([r[3] for r in rows]); allmax = max(r[2] for r in rows)
print()
print("edge flips out of 159 under a node relabelling: mean %.1f, max %d" % (allmean, allmax))
print("max |cost(relabelled) - cost(base)| over all runs: %.3e"
      % max(abs(r[5]-r[4]) for r in rows) )
print("max sink-set symmetric difference: %d" % max(r[7] for r in rows))
