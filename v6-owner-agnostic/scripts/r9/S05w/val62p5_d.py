# -*- coding: utf-8 -*-
"""Y593: v1 sink rule identity on every (good,node) pair, current field; CF1 check; co-sink check."""
import sys, os, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import (N, ORDER, NIDX, UND, GOODS, PRICES, ROWS, build_sc, solve_phi, orient)

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S_UNI, C0, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=1e-6)
ok = tot = 0; bad = []
for gi, g in enumerate(GOODS):
    if not LIVE[gi]: continue
    phi = solve_phi(S_UNI[gi] - C0[gi])
    d = orient(phi)
    od = collections.Counter(u for u,_ in d)
    for n in range(N):
        deg = len(UND[n])
        nb = [phi[m] for m in UND[n]]
        lhs = (C0[gi][n] - S_UNI[gi][n]) / deg
        rhs = np.mean(nb) - min(nb)
        rule = lhs > rhs
        actual = od[n] == 0
        tot += 1
        if rule == actual: ok += 1
        else: bad.append((g, ORDER[n]))
print("sink rule matches actual sinkhood on %d of %d (good,node) pairs; mismatches: %s" % (ok, tot, bad[:5]))

# CF1: uniform demand
gi = GOODS.index("spices")
cu = np.full(N, 1.0/N)
phi = solve_phi(S_UNI[gi] - cu)
od = collections.Counter(u for u,_ in orient(phi))
print("CF1 uniform-demand spices sinks (current field):", sorted(ORDER[i] for i in range(N) if od[i]==0))

# genua co-sink at 1.73
W = np.array([r["tax"]+r["prod_income"] for r in ROWS]); PN = np.array([NIDX[r["node"]] for r in ROWS])
a = ALPHA("spices")
w = np.where(PN == NIDX["genua"], W*1.73, W)
t = w**a; c = np.zeros(N); np.add.at(c, PN, t/t.sum())
od = collections.Counter(u for u,_ in orient(solve_phi(S_UNI[gi] - c)))
print("spices sinks with genua wealth x1.73:", sorted(ORDER[i] for i in range(N) if od[i]==0))
