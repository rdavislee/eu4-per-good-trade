import sys, os, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc
from drain import run_drain, sinks_of

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)

for good in ("spices", "cloves"):
    gi = GOODS.index(good)
    b = S0m[gi] - C0m[gi]
    r = run_drain(b)
    d = r["directed"]
    sk, od = sinks_of(d)
    sinks = sorted(ORDER[i] for i in sk)
    c = C0m[gi]
    demand_rank = {ORDER[i]: k+1 for k,i in enumerate(np.argsort(-c))}
    print(good, "baseline sinks:", sinks, "demand ranks:", {n: demand_rank[n] for n in sinks})
    # graph sources: nodes with in-degree 0 in directed graph, restricted to those with s>0 (supply)
    ind = collections.Counter(v for _,v in d)
    outd = collections.Counter(u for u,_ in d)
    s = S0m[gi]
    all_nodes_in_graph = set(u for u,v in d) | set(v for u,v in d)
    srcs = sorted(ORDER[i] for i in range(N) if i in all_nodes_in_graph and ind[i]==0)
    print(good, "graph sources (in-degree 0, in graph):", srcs)
    print(good, "supply at those sources:", {n: s[NIDX[n]] for n in srcs})
