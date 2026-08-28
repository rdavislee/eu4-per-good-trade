# -*- coding: utf-8 -*-
"""Probe: does the UNPATCHED v5 reimplementation (unit-cost Phase 2, as relabel6.py's instrument
stood before it was patched to carry the tie-break cost) disagree with the shipped drain.py
(which now minimises the tie-break cost) on the identity permutation, and by how many of 159 edges?"""
import io, os, sys, types, collections
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain

V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
_p5 = os.path.join(V5, "_audit_b_drain.py")
_src = io.open(_p5, encoding="utf-8").read()
ab = types.ModuleType("abd_unpatched"); ab.__dict__["__name__"] = "abd_unpatched"
exec(compile(_src, "_audit_b_drain[UNPATCHED unit-cost]", "exec"), ab.__dict__)

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = (W / W.max()) ** 2.0
num = np.zeros(N); np.add.at(num, pn, t)
BW = np.full(N, 1.0 / N) - num / num.sum()

shipped = run_drain(BW)
SHIP_E = set(shipped["directed"])

names = list(ORDER)
edges = sorted(EDGES_UND)
r = ab.drain(names, edges, BW, None)
d = r["directed"] if isinstance(r, dict) else r
UNPATCHED_E = set(d)

agree = UNPATCHED_E & SHIP_E
disagree_count = len(UNPATCHED_E ^ SHIP_E) // 2  # symmetric diff, each differing edge counted twice (once per side, reversed or missing)
print("shipped edges:", len(SHIP_E), "unpatched-instrument edges:", len(UNPATCHED_E))
print("edges agreeing:", len(agree), "of", len(SHIP_E))
print("edges NOT agreeing (present in one, absent/reversed in other):", len(SHIP_E) - len(agree))
