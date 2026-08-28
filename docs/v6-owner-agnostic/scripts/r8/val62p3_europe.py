# -*- coding: utf-8 -*-
"""val part3: the European development sweep on a uniform 0.001 grid, alpha_Phi = 2.0.

Reproduces the sweep the spec's 1.6 attributes to `europe.py`.  NOTE: the shipped europe.py
sweeps x1.00..x1.60 at 0.01 with alpha=1.5, so it is NOT the instrument that produced the
document's figures; this rebuilds the described experiment.
"""
import collections, json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import pdx
from solver import N, ORDER, NIDX, ROWS, NODES
from drain import run_drain

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
EUR = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
PN = np.array([NIDX[r["node"]] for r in ROWS])
BASE = np.array([r["tax"] + r["prod_income"] for r in ROWS])
EURMASK = np.array([r["pid"] in EUR for r in ROWS])
A_PHI = 2.0
print("counted European provinces:", int(EURMASK.sum()))

EU_NODES = {n for n in ORDER if any(p in EUR for p in NODES[n]["members"])}
print("nodes with a European province:", len(EU_NODES))

def sinks(w, a=A_PHI):
    t = (w / w.max()) ** a
    num = np.zeros(N); np.add.at(num, PN, t)
    r = run_drain(np.full(N, 1.0 / N) - num / num.sum())
    od = collections.Counter(u for u, _ in r["directed"])
    return tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0))

t0 = time.time()
_ = sinks(BASE)
print("one run_drain: %.3f s ; 1601 points -> %.0f s" % (time.time()-t0, 1601*(time.time()-t0)))
print("baseline sinks:", _)

grid = [round(1.000 + 0.001*k, 3) for k in range(1601)]
out = []
for i, f in enumerate(grid):
    w = np.where(EURMASK, BASE * f, BASE)
    out.append((f, sinks(w)))
    if i % 200 == 0:
        print("  ... %d/%d (%.0f s)" % (i, len(grid), time.time()-t0), flush=True)
json.dump([[f, list(s)] for f, s in out], open("val62p3_europe_sweep.json", "w"))
print("done in %.0f s" % (time.time()-t0))
