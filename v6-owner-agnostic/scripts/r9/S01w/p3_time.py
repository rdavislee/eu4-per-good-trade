# -*- coding: utf-8 -*-
"""Y132/Y133/Y134: DRAIN timing on the reference implementation. 3 replicates x 12 runs
of all 29 goods, timing the shipped run_drain (LP + sweep) only."""
import os, sys, time
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from drain import run_drain
from solver import N, NIDX, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
B = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    B[g] = val[g] / val[g].sum() - n / n.sum()
for g in GL: run_drain(B[g])          # warm up
for rep in range(3):
    totals = []; peravg = []
    for run in range(12):
        t0 = time.perf_counter()
        for g in GL: run_drain(B[g])
        t1 = time.perf_counter()
        totals.append(t1 - t0); peravg.append((t1 - t0) * 1000.0 / len(GL))
    inside = sum(1 for x in totals if 0.17 <= x <= 0.21)
    print("replicate %d: all-29 total  min %.3f s  median %.3f s  max %.3f s"
          % (rep, min(totals), float(np.median(totals)), max(totals)))
    print("             per-good avg  %.1f - %.1f ms   |  runs inside v5.0's [0.17, 0.21] s : %d of 12"
          % (min(peravg), max(peravg), inside))
