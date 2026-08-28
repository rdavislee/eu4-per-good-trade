# -*- coding: utf-8 -*-
"""Lead probe F: do the promotion and fallback counts hold constant across the 180 relabellings?
relabel6.py compares edges and sink sets only; this compares promotions/fallbacks as well, using the
shipped drain.py on relabelled inputs (identity permutation validated against the shipped solve)."""
import os, sys, collections
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import drain
from drain import run_drain
from solver import N, ORDER, NIDX, EDGES_UND, ROWS

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, W)
t = (W / W.max()) ** 2.0
num = np.zeros(N); np.add.at(num, pn, t)
BW = np.full(N, 1.0 / N) - num / num.sum()

ship = run_drain(BW)
SHIP_E = set(ship["directed"])
_od = collections.Counter(u for u, _ in SHIP_E)
SHIP_S = tuple(sorted(ORDER[i] for i in range(N) if _od[i] == 0))
SHIP_P, SHIP_F = len(ship["promotions"]), len(ship["fallbacks"])
print("shipped: sinks=%s promotions=%d fallbacks=%d" % (SHIP_S, SHIP_P, SHIP_F))

_ORDER = list(ORDER); _EDGES = list(EDGES_UND); _NW = NW.copy()


def relabelled(perm):
    """Run the shipped operator with node i renamed to perm[i]; map results back."""
    inv = {perm[i]: i for i in range(N)}
    names = [None] * N
    for i in range(N):
        names[perm[i]] = _ORDER[i]
    edges = sorted(tuple(sorted((perm[u], perm[v]))) for u, v in _EDGES)
    b2 = np.zeros(N); w2 = np.zeros(N)
    for i in range(N):
        b2[perm[i]] = BW[i]; w2[perm[i]] = _NW[i]
    # patch the module-level tables the shipped operator reads
    import solver, flowop
    old = (solver.ORDER, solver.EDGES_UND, drain.ORDER, drain.EDGES_UND)
    try:
        drain.ORDER = names
        drain.EDGES_UND = edges
        drain.UND = [[] for _ in range(N)]
        for a, b in edges:
            drain.UND[a].append(b); drain.UND[b].append(a)
        r = drain.run_drain(b2, wealth=w2) if 'wealth' in drain.run_drain.__code__.co_varnames \
            else drain.run_drain(b2)
    finally:
        drain.ORDER, drain.EDGES_UND = old[2], old[3]
        drain.UND = [[] for _ in range(N)]
        for a, b in _EDGES:
            drain.UND[a].append(b); drain.UND[b].append(a)
    back = {(inv[u], inv[v]) for (u, v) in r["directed"]}
    o = collections.Counter(u for u, _ in back)
    return back, tuple(sorted(_ORDER[i] for i in range(N) if o[i] == 0)), len(r["promotions"]), len(r["fallbacks"])


e0, s0, p0, f0 = relabelled(list(range(N)))
print("identity: edges agree %d/%d  sinks %s  promo %d  fb %d"
      % (len(e0 & SHIP_E), len(SHIP_E), s0 == SHIP_S, p0, f0))
if not (len(e0 & SHIP_E) == len(SHIP_E) and s0 == SHIP_S):
    sys.exit("INSTRUMENT FAILED VALIDATION")

pc = collections.Counter(); fc = collections.Counter(); moved = 0; sinkok = 0; n = 0
for sd in (4242, 7, 999):
    rng = np.random.default_rng(sd)
    for _ in range(60):
        e, s, p, f = relabelled(list(rng.permutation(N)))
        n += 1
        moved += len(e ^ SHIP_E) // 2
        sinkok += (s == SHIP_S)
        pc[p] += 1; fc[f] += 1
print("over %d relabellings: total edges moved %d ; baseline sink set %d/%d" % (n, moved, sinkok, n))
print("promotion-count distribution:", dict(pc))
print("fallback-count distribution:", dict(fc))
