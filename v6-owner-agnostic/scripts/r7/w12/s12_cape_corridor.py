# -*- coding: utf-8 -*-
"""S12: reproduce the Cape-corridor hop counts and the 24% spice-flow figure
on DRAIN's own certificate flow (Phase 2 b-flow under TIE_COST)."""
import collections, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from drain import run_drain

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]

# ---------- hop counts ----------
def bfs(a, z):
    prev = {a: None}; q = collections.deque([a])
    while q:
        x = q.popleft()
        if x == z:
            p = []
            while x is not None: p.append(x); x = prev[x]
            return p[::-1]
        for y in UND[x]:
            if y not in prev: prev[y] = x; q.append(y)
    return None

def hops_via(a, z, via):
    return (len(bfs(a, via)) - 1) + (len(bfs(via, z)) - 1)

m = NIDX["malacca"]; ch = NIDX["english_channel"]
cape = NIDX["cape_of_good_hope"]; alex = NIDX["alexandria"]
print("malacca -> channel via cape     :", hops_via(m, ch, cape), "hops")
print("malacca -> channel via alexandria:", hops_via(m, ch, alex), "hops")
print("malacca -> channel direct shortest:", len(bfs(m, ch)) - 1, "hops")

# ---------- spice flow through the Cape (DRAIN certificate flow, TIE_COST) ----------
gi_sp = GOODS.index("spices")
r = run_drain(S[gi_sp] - C[gi_sp])
net = r["net"]
ei_mc = next(ei for ei, (u, v) in enumerate(EDGES_UND) if {u, v} == {m, cape})
print()
print("spices flow on malacca<->cape edge (fraction of world spice supply): %.6f (%.1f%%)"
      % (abs(net[ei_mc]), 100*abs(net[ei_mc])))

# total flow into/out of the cape for spices, and total world spice supply share represented
flow_arc = r["flow_arc"]
into_cape = sum(abs(net[ei]) for ei, (u, v) in flow_arc.items() if v == cape)
outof_cape = sum(abs(net[ei]) for ei, (u, v) in flow_arc.items() if u == cape)
print("total spice flow INTO the cape (sum over incoming flow-edges):  %.6f (%.1f%%)" % (into_cape, 100*into_cape))
print("total spice flow OUT of the cape (sum over outgoing flow-edges): %.6f (%.1f%%)" % (outof_cape, 100*outof_cape))
print("world spice supply share sum (should be 1.0):", S[gi_sp].sum())

# cross-check against flowop.py's unit-cost s_targeted FLOW operator (verify.py's method)
print()
print("cross-check via flowop.py's unit-cost s_targeted FLOW operator (verify.py method):")
import flowop
from flowop import mincost_flow, net_per_edge, s_targeted
f, pi, res = mincost_flow(s_targeted(gi_sp), C[gi_sp])
FLsp = net_per_edge(f)
print("  spices flow on malacca<->cape edge: %.6f (%.1f%%)" % (abs(FLsp[ei_mc]), 100*abs(FLsp[ei_mc])))
