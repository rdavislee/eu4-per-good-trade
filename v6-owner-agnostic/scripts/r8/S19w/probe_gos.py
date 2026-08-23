import os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import drain
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
print("num live goods:", len(GL))

gos = NIDX["gulf_of_siam"]
sets = set()
detail = {}
for gi, g in GL:
    b = S[gi] - C[gi]
    res = run_drain(b)
    d = res["directed"]
    outs = sorted(ORDER[v] for u, v in d if u == gos)
    key = tuple(outs)
    sets.add(key)
    detail.setdefault(key, []).append(g)

print("distinct downstream sets for gulf_of_siam across", len(GL), "goods:", len(sets))
for k, gs in sorted(detail.items(), key=lambda kv: -len(kv[1])):
    print(" ", k, "<-", gs)
