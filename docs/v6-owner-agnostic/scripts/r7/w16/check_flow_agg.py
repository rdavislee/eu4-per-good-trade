# -*- coding: utf-8 -*-
"""Check: pure min-cost-flow orientation (no sweep, no cycle cancellation) --
   (a) edge-orientation count per good (~79 of 159?)
   (b) value-weighted aggregate of the RAW per-good net flows contains directed cycles?
"""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowop import (run_all, GOODS, LIVE, V, E, EDGES_UND, has_cycle, edges_from_net,
                     ZERO_TOL)

R = run_all()
goods_live = [g for gi, g in enumerate(GOODS) if LIVE[gi]]

oriented_counts = []
for g in goods_live:
    net = R[g]["flow_raw_net"]
    oriented = int((np.abs(net) > ZERO_TOL).sum())
    oriented_counts.append(oriented)

print("goods live:", len(goods_live))
print("oriented-edge counts per good (pre-cancellation, raw min-cost flow):")
print(" min=%d max=%d mean=%.2f" % (min(oriented_counts), max(oriented_counts), sum(oriented_counts)/len(oriented_counts)))
print(" spices value:", oriented_counts[goods_live.index("spices")] if "spices" in goods_live else None)
print(" full list:", dict(zip(goods_live, oriented_counts)))

# how many goods individually have a cycle in the RAW (uncancelled) net?
per_good_cycle = 0
for g in goods_live:
    net = R[g]["flow_raw_net"]
    d = edges_from_net(net)
    if has_cycle(d) is not None:
        per_good_cycle += 1
print("goods whose OWN raw min-cost flow contains a cycle:", per_good_cycle, "of", len(goods_live))

# value-weighted aggregate of RAW per-good net flows
Vgi = {g: V[gi] for gi, g in enumerate(GOODS)}
agg = np.zeros(E)
for g in goods_live:
    agg += Vgi[g] * R[g]["flow_raw_net"]

d_agg = edges_from_net(agg)
cyc = has_cycle(d_agg)
print("value-weighted aggregate of RAW (uncancelled) per-good net flows: cycle found:", cyc)

# also check the aggregate AFTER per-good cancellation (flow_net), for contrast
agg2 = np.zeros(E)
for g in goods_live:
    agg2 += Vgi[g] * R[g]["flow_net"]
d_agg2 = edges_from_net(agg2)
cyc2 = has_cycle(d_agg2)
print("value-weighted aggregate of CANCELLED per-good net flows: cycle found:", cyc2)
