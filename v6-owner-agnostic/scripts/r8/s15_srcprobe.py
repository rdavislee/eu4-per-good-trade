# -*- coding: utf-8 -*-
import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from drain import run_drain, sinks_of
from flowop import EDGES_UND
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
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
for g in ("spices", "cloves"):
    edges = R[g]["directed"]
    indeg = collections.Counter(); outdeg = collections.Counter()
    nodes_in_graph = set()
    for (u, v) in edges:
        outdeg[u]+=1; indeg[v]+=1
        nodes_in_graph.add(u); nodes_in_graph.add(v)
    graph_sources = sorted(ORDER[i] for i in nodes_in_graph if indeg[i]==0)
    sinks_ids, _ = sinks_of(edges)
    graph_sinks = sorted(ORDER[i] for i in sinks_ids)
    print(g, "graph-sources(indeg0):", graph_sources)
    print(g, "sinks:", graph_sinks)
