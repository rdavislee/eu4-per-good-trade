import numpy as np
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc
from drain import run_drain

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
print("num live goods:", len(GL))

gos = NIDX["gulf_of_siam"]
sets = {}
for gi, g in GL:
    b = S[gi] - C[gi]
    r = run_drain(b)
    d = r["directed"]
    downstream = tuple(sorted(ORDER[v] for u,v in d if u == gos))
    sets.setdefault(downstream, []).append(g)

print("distinct downstream sets:", len(sets))
for k,v in sorted(sets.items(), key=lambda kv: -len(kv[1])):
    print(f"  {k} : {len(v)} goods -> {v}")
