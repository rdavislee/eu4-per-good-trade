import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc
from drain import run_drain

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
print("live goods:", len(GL))

upstream_any = np.zeros(N, dtype=bool)  # out-degree>0 in at least one good's directed graph
for gi, g in GL:
    r = run_drain(S[gi] - C[gi])
    outd = collections.Counter(u for u, v in r["directed"])
    for i in range(N):
        if outd[i] > 0:
            upstream_any[i] = True

n_up = int(upstream_any.sum())
print("nodes upstream (out-degree>0) for >=1 good:", n_up, "of", N)
if n_up < N:
    print("nodes NEVER upstream for any good:", [ORDER[i] for i in range(N) if not upstream_any[i]])
