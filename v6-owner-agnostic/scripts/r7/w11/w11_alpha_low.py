import sys, os, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

def cv(a):
    t = (W / W.max()) ** a
    n = np.zeros(N); np.add.at(n, pn, t)
    return n / n.sum()

def sset(a):
    r = run_drain(np.full(N, 1.0/N) - cv(a))
    o = collections.Counter(u for u,_ in r["directed"])
    return tuple(sorted(ORDER[i] for i in range(N) if o[i] == 0))

for a in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0]:
    s = sset(a)
    print("alpha=%.2f  sinks=%d  %s" % (a, len(s), s))
