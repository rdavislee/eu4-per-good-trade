# -*- coding: utf-8 -*-
"""Extend measure6.py's +/-1% wealth-noise sink check to 6 seeds and full edge-orientation diff
(S3.6's 'six-seed run no edge moved at all' claim), using the identical construction."""
import os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain, sinks_of

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])


def cv(a, w):
    t = (w / w.max()) ** a
    n = np.zeros(N)
    np.add.at(n, pn, t)
    return n / n.sum()


def ph(a, w):
    return run_drain(np.full(N, 1.0 / N) - cv(a, w))


base = ph(A_PHI, W)
base_edges = set(base["directed"])
base_sinks = sorted(ORDER[i] for i in sinks_of(base["directed"])[0])
print("base sinks:", base_sinks, " edges:", len(base_edges))

for s_ in range(6):
    nz = 1 + np.random.default_rng(9000 + s_).uniform(-0.01, 0.01, size=len(W))
    r = ph(A_PHI, W * nz)
    edges = set(r["directed"])
    sinks = sorted(ORDER[i] for i in sinks_of(r["directed"])[0])
    diff = len(base_edges ^ edges) // 2
    print("seed %d  sinks=%-30s edges differing from base: %d" % (s_, sinks, diff))
