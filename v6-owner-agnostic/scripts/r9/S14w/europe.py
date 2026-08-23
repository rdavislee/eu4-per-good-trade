# -*- coding: utf-8 -*-
"""The European development sweep section 1.6 cites, at the shipped configuration.

Scales every counted European province's wealth by one factor, uniformly on a 0.001 grid from
x1.000 to x2.600, at the shipped alpha_Phi = 2.0, and reports the maximal runs of constant sink
set. Every figure section 1.6 quotes from this experiment is printed by name below so the citation
is checkable against this script's own output.

Repaired under round-7 A5: the previous revision hardcoded alpha = 1.5 (the pre-v6.1 operator), a
0.01 step and x1.00-x1.60, so it could not produce the documented experiment.

Usage: python europe.py            (takes a few minutes: 1,601 aggregate solves)
"""
import collections
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx
from drain import run_drain
from solver import N, ORDER, NIDX, ROWS, NODES

A_PHI = 2.0
LO, HI, STEP = 1000, 2600, 1          # x1.000 to x2.600 on a 0.001 grid

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
EUR = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
PN = np.array([NIDX[r["node"]] for r in ROWS])
BASE = np.array([r["tax"] + r["prod_income"] for r in ROWS])
EURMASK = np.array([r["pid"] in EUR for r in ROWS])
EU_NODES = {n for n in ORDER if any(p in EUR for p in NODES[n]["members"])}
ASIA = {"hangzhou", "beijing", "canton", "xian", "girin", "nippon", "gulf_of_siam", "malacca",
        "doab", "bengal", "ganges_delta", "deccan", "comorin_cape", "gujarat"}

print("counted European provinces scaled: %d ; alpha_Phi = %g ; grid x%.3f-x%.3f step 0.001"
      % (int(EURMASK.sum()), A_PHI, LO / 1000.0, HI / 1000.0))

runs = []                             # [lo, hi, sinkset]
last = None
for k in range(LO, HI + STEP, STEP):
    f = k / 1000.0
    w = np.where(EURMASK, BASE * f, BASE)
    t = (w / w.max()) ** A_PHI
    num = np.zeros(N)
    np.add.at(num, PN, t)
    r = run_drain(np.full(N, 1.0 / N) - num / num.sum())
    od = collections.Counter(u for u, _ in r["directed"])
    s = tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0))
    if s != last:
        runs.append([f, f, s])
        last = s
    else:
        runs[-1][1] = f

print()
print("maximal runs of constant sink set (%d):" % len(runs))
occur = collections.Counter(s for _lo, _hi, s in runs)
for lo, hi, s in runs:
    eu = [x for x in s if x in EU_NODES]
    asia = [x for x in s if x in ASIA and x not in EU_NODES]
    print("  x%.3f-x%.3f  %d sinks  EU:%d Asia:%d  %s%s"
          % (lo, hi, len(s), len(eu), len(asia), list(s),
             "   <== set occurs in this run alone" if occur[s] == 1 and hi - lo < 0.0095 else ""))

print()
three_eu = [(lo, hi, s) for lo, hi, s in runs
            if len([x for x in s if x in EU_NODES]) == 3
            and not [x for x in s if x in ASIA and x not in EU_NODES]]
w = max(three_eu, key=lambda r: r[1] - r[0]) if three_eu else None
print("widest run with three European ends and none in Asia : x%.3f-x%.3f  %s"
      % (w[0], w[1], list(w[2])) if w else "  none")

for node in ("hangzhou", "gulf_of_siam"):
    eps = [(lo, hi) for lo, hi, s in runs if node in s]
    # merge adjacent runs where the node is continuously present
    merged = []
    for lo, hi in eps:
        if merged and abs(lo - merged[-1][1]) <= 0.0015:
            merged[-1][1] = hi
        else:
            merged.append([lo, hi])
    print("%-13s holds an end over: %s" % (node, " and ".join("x%.3f-x%.3f" % (a, b) for a, b in merged)))

narrow = [(lo, hi, s) for lo, hi, s in runs if (hi - lo) < 0.0095]
print("runs narrower than x0.01: %d  (%s)"
      % (len(narrow), "; ".join("x%.3f-x%.3f%s" % (lo, hi, " ONE-OFF" if occur[s] == 1 else "")
                                for lo, hi, s in narrow)))
top = runs[-1]
print("top of range: x%.3f-x%.3f settles at %d sinks %s" % (top[0], top[1], len(top[2]), list(top[2])))
