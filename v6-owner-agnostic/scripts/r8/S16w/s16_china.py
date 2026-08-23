import sys, os, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc, solve_phi, orient)

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
EPS = 1e-6
gi = GOODS.index("spices"); a = ALPHA("spices")
W = np.array([r["tax"]+r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
S_UNI, C0, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=EPS)
s = S_UNI[gi]

def sinks_at(node_idx, k):
    w = np.where(PN == node_idx, W * k, W)
    t = w ** a
    c = np.zeros(N); np.add.at(c, PN, t / t.sum())
    phi = solve_phi(s - c)
    d = orient(phi)
    od = collections.Counter(u for u,_ in d)
    return od[node_idx] == 0

def bisect(node):
    i = NIDX[node]
    lo, hi = 1.0, 30.0
    if sinks_at(i, 1.0): return 1.0
    if not sinks_at(i, hi): return None
    for _ in range(40):
        mid = (lo+hi)/2
        if sinks_at(i, mid): hi = mid
        else: lo = mid
    return hi

# print all node names to find china-ish nodes
names = list(ORDER)
print(len(names), "nodes")
china_candidates = [n for n in names if n in ("beijing","hangzhou","xian","canton","girin","yumen","shanghai","nanjing","guangzhou","yangtze","huguang","shansi","yunnan","sichuan")]
print("candidates present:", china_candidates)
