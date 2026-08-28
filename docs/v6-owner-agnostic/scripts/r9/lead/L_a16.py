import os, sys, collections
sys.path.insert(0, os.path.abspath('.')); os.chdir(os.path.abspath('.'))
import numpy as np
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc
from drain import run_drain
A = lambda g: (PRICES[g] / 2.0) ** 2.0          # unclamped alpha^2 calibration
S, C, V, LIVE, GP, W = build_sc(A, eps=0.0)
gi = GOODS.index('cloves')
b = S[gi] - C[gi]
r = run_drain(b)
od = collections.Counter(u for u, _ in r["directed"])
sinks = [ORDER[i] for i in range(N) if od[i] == 0 and (S[gi][i] > 0 or C[gi][i] > 0)]
print("cloves alpha(cloves) =", A('cloves'), " price", PRICES['cloves'])
print("cloves sinks under alpha^2 unclamped:", sorted(sinks))
order = sorted(range(N), key=lambda i: -C[gi][i])
print("top-5 cloves demanders:", [(ORDER[i], round(float(C[gi][i]), 5)) for i in order[:5]])
for s in sinks:
    print("  sink", s, "demand rank", order.index(NIDX[s]) + 1)
