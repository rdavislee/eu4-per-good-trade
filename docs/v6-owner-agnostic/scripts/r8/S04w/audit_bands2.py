# -*- coding: utf-8 -*-
"""Stress-test the two quantitative claims v5.0 introduced in 1.6 that a reviewer would attack:
(a) the alpha_Phi band edges at finer resolution than the 0.01 the table was measured on, and
(b) "under +/-1% wealth noise the narrow window moves or disappears while the wide bands move by
    <= 0.03"."""
import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cvec(a, w):
    t = (w / w.max()) ** a; num = np.zeros(N); np.add.at(num, pn, t); return num / num.sum()
def sinkset(a, w):
    r = run_drain(np.full(N, 1.0 / N) - cvec(a, w))
    o = collections.Counter(u for u, _ in r["directed"])
    return tuple(sorted(ORDER[i] for i in range(N) if o[i] == 0))

print("=" * 96)
print("(a) band edges at 0.001 resolution around each 0.01-grid boundary")
print("=" * 96)
GRID = {}
for k in range(100, 301):
    a = round(k / 100, 2); GRID[a] = sinkset(a, wealth)
bands = []
cur, lo = GRID[1.00], 1.00
for k in range(101, 301):
    a = round(k / 100, 2)
    if GRID[a] != cur:
        bands.append((cur, lo, round(a - 0.01, 2))); cur, lo = GRID[a], a
bands.append((cur, lo, 3.00))
named = [b for b in bands if b[0] in (("hangzhou",), ("genua", "hangzhou"),
                                      ("doab", "genua", "hangzhou"), ("english_channel", "hangzhou"))]
for s, lo, hi in named:
    # refine each edge downward/upward at 0.001
    e_lo = lo
    for k in range(1, 11):
        a = round(lo - k / 1000, 3)
        if a < 1.0 or sinkset(a, wealth) != s: break
        e_lo = a
    e_hi = hi
    for k in range(1, 11):
        a = round(hi + k / 1000, 3)
        if a > 3.0 or sinkset(a, wealth) != s: break
        e_hi = a
    print("  %-42s 0.01 grid [%.2f, %.2f] w=%.2f | refined [%.3f, %.3f] w=%.3f"
          % ("+".join(s), lo, hi, hi - lo, e_lo, e_hi, e_hi - e_lo))

print()
print("=" * 96)
print("(b) the same bands under +/-1% per-province wealth noise, 8 seeds")
print("=" * 96)
TARGETS = [("hangzhou",), ("genua", "hangzhou"), ("doab", "genua", "hangzhou"),
           ("english_channel", "hangzhou")]
base = {t: None for t in TARGETS}
for s, lo, hi in named: base[s] = (lo, hi)
rows = {t: [] for t in TARGETS}
for seed in range(8):
    w = wealth * (1 + np.random.default_rng(4000 + seed).uniform(-0.01, 0.01, size=len(wealth)))
    g = {}
    for k in range(100, 301):
        a = round(k / 100, 2); g[a] = sinkset(a, w)
    for t in TARGETS:
        hit = sorted(a for a in g if g[a] == t)
        rows[t].append((min(hit), max(hit), len(hit)) if hit else None)
for t in TARGETS:
    b = base[t]
    print("  %-42s baseline [%.2f, %.2f]" % ("+".join(t), b[0], b[1]))
    gone = sum(1 for r in rows[t] if r is None)
    if gone: print("       DISAPPEARS on %d of 8 seeds" % gone)
    got = [r for r in rows[t] if r]
    if got:
        dlo = max(abs(r[0] - b[0]) for r in got); dhi = max(abs(r[1] - b[1]) for r in got)
        w_ = [round(r[1] - r[0], 2) for r in got]
        print("       edges move at most %.2f (lo) / %.2f (hi) | widths %s"
              % (dlo, dhi, sorted(set(w_))))
