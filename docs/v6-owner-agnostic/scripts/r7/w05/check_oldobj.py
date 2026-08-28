# -*- coding: utf-8 -*-
"""Reproduce the 26-of-159 disagreement: run the v5 reimplementation's identity-permutation
trial WITHOUT patching Phase 2's objective (i.e. the old unit-cost objective), and count how many
edges disagree with the shipped drain.py output."""
import collections, io, os, sys, types
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(HERE, "..", "..", "..", "..", "v5-owner-agnostic", "scripts")
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain

_p5 = os.path.join(V5, "_audit_b_drain.py")
if not os.path.exists(_p5):
    sys.exit("the five-phase reimplementation is missing; cannot run this experiment safely")
_src = io.open(_p5, encoding="utf-8").read()
ab = types.ModuleType("abd_old"); ab.__dict__["__name__"] = "abd_old"
exec(compile(_src, "_audit_b_drain[OLD unpatched objective]", "exec"), ab.__dict__)

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
t = (W / W.max()) ** 2.0
num = np.zeros(N); np.add.at(num, pn, t)
BW = np.full(N, 1.0 / N) - num / num.sum()

shipped = run_drain(BW)
SHIP_E = set(shipped["directed"])

# identity permutation trial with the OLD (unpatched) Phase 2 objective
perm = list(range(N))
inv = {perm[i]: i for i in range(N)}
names = [None] * N
for i in range(N): names[perm[i]] = ORDER[i]
edges = sorted(tuple(sorted((perm[u], perm[v]))) for u, v in EDGES_UND)
b2 = np.zeros(N); w2 = np.zeros(N)
for i in range(N):
    b2[perm[i]] = BW[i]; w2[perm[i]] = NODEW[i]
r = ab.drain(names, edges, b2, w2)
d = r["directed"] if isinstance(r, dict) else r
back = {(inv[u], inv[v]) for (u, v) in d}

agree = len(back & SHIP_E)
disagree = len(SHIP_E) - agree
print("edges agreeing with shipped drain.py (OLD unpatched objective) : %d of %d" % (agree, len(SHIP_E)))
print("edges DISAGREEING                                              : %d of %d" % (disagree, len(SHIP_E)))
_od = collections.Counter(u for u, _ in back)
old_sinks = tuple(sorted(ORDER[i] for i in range(N) if _od[i] == 0))
_od2 = collections.Counter(u for u, _ in SHIP_E)
ship_sinks = tuple(sorted(ORDER[i] for i in range(N) if _od2[i] == 0))
print("sink set (old objective) : %s" % (old_sinks,))
print("sink set (shipped)       : %s" % (ship_sinks,))
