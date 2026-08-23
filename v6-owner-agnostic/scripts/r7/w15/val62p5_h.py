# -*- coding: utf-8 -*-
"""Y162: is any node cheaper than the four named? Sweep the minimal wealth multiple
that makes a node a v1-Laplacian spices sink, over every node."""
import sys, os, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc, solve_phi, orient
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
gi = GOODS.index("spices"); a = ALPHA("spices")
W = np.array([r["tax"]+r["prod_income"] for r in ROWS]); PN = np.array([NIDX[r["node"]] for r in ROWS])
S_UNI, C0, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=1e-6)
s = S_UNI[gi]
def is_sink(i, k):
    w = np.where(PN == i, W*k, W); t = w**a
    c = np.zeros(N); np.add.at(c, PN, t/t.sum())
    od = collections.Counter(u for u,_ in orient(solve_phi(s - c)))
    return od[i] == 0
def bisect(i, hi=60.0):
    if is_sink(i, 1.0): return 1.0
    if not is_sink(i, hi): return None
    lo = 1.0
    for _ in range(34):
        mid = (lo+hi)/2
        if is_sink(i, mid): hi = mid
        else: lo = mid
    return hi
res = []
for i in range(N):
    if not (PN == i).any(): continue
    k = bisect(i)
    res.append((k if k else 1e9, ORDER[i]))
res.sort()
NAMED = {"beijing","hangzhou","xian","canton"}
print("cheapest 15 nodes by minimal wealth multiple to become a v1 spices sink:")
for k, n in res[:15]:
    print("   %-22s %s%s" % (n, ("%.3f" % k) if k < 1e8 else ">60", "   <== one of the four named" if n in NAMED else ""))
print()
print("minimum over ALL nodes: %s at %.3f" % (res[0][1], res[0][0]))
print("minimum over the four named: %s" % min((k,n) for k,n in res if n in NAMED)[1])
for n in ("girin","yumen"):
    print("  %s = %.3f" % (n, dict((b,a2) for a2,b in res)[n]))
