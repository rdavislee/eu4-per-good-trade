# -*- coding: utf-8 -*-
"""S12: minimal wealth multiple making a node a v1-Laplacian spices sink, on the current (v6) field."""
import sys, os, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import (N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc, solve_phi, orient)

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
EPS = 1e-6
gi = GOODS.index("spices"); a = ALPHA("spices")
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
S_UNI, C0, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=EPS)
s = S_UNI[gi]

def sinks_at_mult(node_idx, k):
    w = np.where(PN == node_idx, W * k, W)
    t = w ** a
    c = np.zeros(N); np.add.at(c, PN, t / t.sum())
    phi = solve_phi(s - c)
    d = orient(phi)
    od = collections.Counter(u for u, _ in d)
    return od[node_idx] == 0

def bisect(node_idx, hi=60.0):
    if sinks_at_mult(node_idx, 1.0): return 1.0
    if not sinks_at_mult(node_idx, hi): return None
    lo = 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if sinks_at_mult(node_idx, mid): hi = mid
        else: lo = mid
    return hi

base_d = orient(solve_phi(s - C0[gi]))
base_od = collections.Counter(u for u, _ in base_d)
print("v1 Laplacian spices sinks at baseline (current v6 field):",
      sorted(ORDER[i] for i in range(N) if base_od[i] == 0))
print()
print("named-node wealth multiples to become a spices sink:")
for n in ("genua", "beijing", "hangzhou", "xian", "canton", "girin", "yumen"):
    k = bisect(NIDX[n])
    print("  %-15s %s" % (n, ("%.3fx" % k) if k else ">60x"))

print()
print("sweep over ALL nodes for the cheapest:")
res = []
for i in range(N):
    if not (PN == i).any():
        continue
    k = bisect(i)
    res.append((k if k else 1e9, ORDER[i]))
res.sort()
print("cheapest 15 nodes:")
for k, n in res[:15]:
    print("   %-22s %.3fx" % (n, k))
