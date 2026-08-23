import os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "..")
sys.path.insert(0, SCRIPTS); os.chdir(SCRIPTS)
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cv(a, w):
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
def ph(a, w): return run_drain(np.full(N, 1.0 / N) - cv(a, w))

base = ph(A_PHI, W); BD = set(base["directed"])
for s_ in range(6):
    nz = 1 + np.random.default_rng(9000 + s_).uniform(-0.01, 0.01, size=len(W))
    r = ph(A_PHI, W * nz)
    D = set(r["directed"])
    flips = len(BD ^ D) // 2
    o = collections.Counter(u for u,_ in D)
    sinks = sorted(ORDER[i] for i in range(N) if o[i]==0)
    print("seed", s_, "edge flips vs base:", flips, "sinks:", sinks)
