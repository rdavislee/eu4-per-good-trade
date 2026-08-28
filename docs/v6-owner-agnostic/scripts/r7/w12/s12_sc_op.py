# -*- coding: utf-8 -*-
"""S12: reproduce the 's-c' local-comparison operator's stranded-demand figures,
mirroring val62p5_f.py's direct b=S-C edge orientation (endpoint comparison),
extended with value weighting."""
import collections, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc)

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
print("live goods:", len(GL))

def reach_share(directed, s, c):
    adj = collections.defaultdict(list)
    for u, v in directed: adj[u].append(v)
    srcs = [i for i in range(N) if s[i] > 0]
    seen = set(srcs); st = list(srcs)
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    tot = c.sum()
    return (sum(c[i] for i in seen) / tot if tot else 1.0), seen

tot_r = []; orphans = 0; per_good = {}
for gi, g in GL:
    b = S[gi] - C[gi]
    d = []
    for (u, v) in EDGES_UND:
        if b[u] > b[v]: d.append((u, v))
        elif b[v] > b[u]: d.append((v, u))
    r, seen = reach_share(d, S[gi], C[gi]); tot_r.append(r); per_good[g] = r
    od = collections.Counter(u for u, _ in d)
    orphans += sum(1 for i in range(N) if od[i] == 0 and i not in seen)

unweighted_mean_unreach = 100*(1-np.mean(tot_r))
Vg = {g: V[gi] for gi, g in GL}
totV = sum(Vg.values())
vw_unreach = 100*(1 - sum(per_good[g]*Vg[g] for gi,g in GL)/totV)

print("  s-c operator: mean reach %.2f%% -> unreachable %.2f%% ; orphan sinks %d"
      % (100*np.mean(tot_r), unweighted_mean_unreach, orphans))
print("  s-c operator value-weighted unreachable: %.2f%%" % vw_unreach)

# cloves / genua check
gi = GOODS.index("cloves"); b = S[gi]-C[gi]
d = []
for (u, v) in EDGES_UND:
    if b[u] > b[v]: d.append((u, v))
    elif b[v] > b[u]: d.append((v, u))
od = collections.Counter(u for u, _ in d)
r, seen = reach_share(d, S[gi], C[gi])
gn = NIDX["genua"]
print("  cloves: genua is a sink: %s ; genua reachable from cloves supply: %s"
      % (od[gn] == 0, gn in seen))
print("  cloves per-good unreachable: %.2f%%" % (100*(1-per_good['cloves'])))
