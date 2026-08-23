# coordinator recheck of Y992: Phi_w sink set as TIE_EPS varies, shipped code path,
# alpha_Phi = 2.0, TIE_EPS2 and LP_OPTS as shipped. drain.TIE_COST patched per value.
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = np.zeros(N); np.add.at(t, pn, (W / W.max()) ** 2.0)
b = np.full(N, 1.0 / N) - t / t.sum()

def sinks(directed):
    out = {u for (u, v) in directed}
    inn = {v for (u, v) in directed}
    return sorted(ORDER[i] for i in (inn - out))

# sanity: shipped TIE_COST must reproduce the baseline
r0 = run_drain(b)
print("shipped eps=%g sinks=%s edges=%d" % (flowop.TIE_EPS, sinks(r0["directed"]), len(r0["directed"])))

grid = [1e-13, 1e-12, 1e-11, 3e-11, 1e-10, 3e-10, 1e-9, 3e-9, 1e-8, 1e-7, 1e-6,
        1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 3.0, 10.0, 1e2, 1e3, 1e6, 1e9, 1e12]
base = None
for eps in grid:
    drain.TIE_COST = 1.0 + eps * (flowop._a1 + flowop._a2) / 2.0 + flowop.TIE_EPS2 * flowop._gen
    r = run_drain(b)
    s = sinks(r["directed"])
    same = "SAME" if s == sinks(r0["directed"]) else "DIFF"
    print("eps=%-8g sinks=%s  edges_vs_shipped=%d differ  [%s]" %
          (eps, s, len(set(r["directed"]) ^ set(r0["directed"])) // 2, same))
