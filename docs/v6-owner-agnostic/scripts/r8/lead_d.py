# -*- coding: utf-8 -*-
"""Lead probe D: 23 European nodes, 27 Europe->sink pairs, 0 Cape-transiting; six-seed +/-1% noise;
Cape ordered-pair counts under the three readings."""
import os, sys, collections, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS, NODES
from drain import run_drain
import europe as EU

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])


def field(w):
    t = (w / w.max()) ** A_PHI
    c = np.zeros(N); np.add.at(c, pn, t); c = c / c.sum()
    return np.full(N, 1.0 / N) - c


res = run_drain(field(W))
D = set(res["directed"])
out = collections.Counter(u for u, _ in D)
sinks = [i for i in range(N) if out[i] == 0]
print("sinks:", [ORDER[i] for i in sinks])

adj = collections.defaultdict(list)
for u, v in D:
    adj[u].append(v)


def reach_from(s, avoid=None):
    seen = {s}; st = [s]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y == avoid:
                continue
            if y not in seen:
                seen.add(y); st.append(y)
    return seen


EUN = sorted(EU.EU_NODES)
print("European nodes:", len(EUN))
CAPE = NIDX["cape_of_good_hope"]
R = {i: reach_from(i) for i in range(N)}
Rno = {}
pairs = 0
via = 0
for nm in EUN:
    i = NIDX[nm]
    for s in sinks:
        if s == i:
            continue
        if s in R[i]:
            pairs += 1
            # is there a Cape-transiting path i -> ... -> CAPE -> ... -> s ?
            if CAPE in R[i] and s in R[CAPE]:
                via += 1
print("connected Europe->sink pairs:", pairs, "| with a Cape-transiting path:", via)

# Cape ordered-pair counts, three readings
allreach = R
cnt_a = sum(1 for a in range(N) for b in range(N)
            if a != b and b != CAPE and a != CAPE
            and CAPE in allreach[a] and b in allreach[CAPE] and b in allreach[a])
print("Cape ordered pairs (a reaches Cape, Cape reaches b, a reaches b):", cnt_a)

# six-seed +/-1% wealth noise on the aggregate
print()
base_dirs = D
for seed in range(6):
    rng = np.random.default_rng(seed)
    w2 = W * (1.0 + rng.uniform(-0.01, 0.01, size=W.shape))
    r2 = run_drain(field(w2))
    d2 = set(r2["directed"])
    o2 = collections.Counter(u for u, _ in d2)
    sk2 = sorted(ORDER[i] for i in range(N) if o2[i] == 0)
    moved = len(base_dirs ^ d2) // 2
    print("  seed %d  sinks=%s  edges moved=%d" % (seed, sk2, moved))
