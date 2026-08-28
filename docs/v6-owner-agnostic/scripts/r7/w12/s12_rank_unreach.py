# -*- coding: utf-8 -*-
"""S12 reproduction: RANK (s-c) operator unreachable-demand figures."""
import numpy as np, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc
from rankop import run as rank_run, GOODS_LIVE, GIDX

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S0m, C0m, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)


def reach(directed, srcs):
    adj = collections.defaultdict(list)
    for u, v in directed:
        adj[u].append(v)
    seen = set(srcs)
    stack = list(srcs)
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); stack.append(v)
    return seen


R = rank_run()
per_good_unreach = {}
for g in GOODS_LIVE:
    gi = GIDX[g]
    d = R[g]["rank_dir"]
    srcs = [i for i in range(N) if GP[gi][i] > 0]
    rs = reach(d, srcs)
    reachable_demand = C0m[gi][list(rs)].sum()
    total_demand = C0m[gi].sum()
    unreach_frac = 1.0 - reachable_demand / total_demand
    per_good_unreach[g] = unreach_frac

unweighted_mean = np.mean(list(per_good_unreach.values()))
Vlive = {g: V[GIDX[g]] for g in GOODS_LIVE}
totV = sum(Vlive.values())
value_weighted = sum(per_good_unreach[g] * Vlive[g] for g in GOODS_LIVE) / totV

print("per-good unreachable fraction (RANK / s-c operator):")
for g in sorted(per_good_unreach, key=lambda x: -per_good_unreach[x]):
    print("  %-15s %.4f%%" % (g, per_good_unreach[g]*100))

print()
print("unweighted per-good mean unreachable: %.4f%%" % (unweighted_mean*100))
print("value-weighted unreachable:           %.4f%%" % (value_weighted*100))

# Genoa crowned a cloves sink cloves cannot reach?
gi_cloves = GIDX["cloves"]
d = R["cloves"]["rank_dir"]
srcs = [i for i in range(N) if GP[gi_cloves][i] > 0]
sinks = [i for i in range(N) if all(u != i for u, v in d)]
od = collections.Counter(u for u, v in d)
sink_nodes = [i for i in range(N) if od[i] == 0]
rs = reach(d, srcs)
print()
print("cloves sources:", [ORDER[i] for i in srcs])
print("cloves RANK sinks:", [ORDER[i] for i in sink_nodes])
print("genua index reachable from cloves sources:", NIDX["genua"] in rs, " genua is a sink:", NIDX["genua"] in sink_nodes)
