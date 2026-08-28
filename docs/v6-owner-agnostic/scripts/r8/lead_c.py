# -*- coding: utf-8 -*-
"""Lead probe C: Europe->sink pairs and the Cape; +/-1% wealth noise over six seeds; Cape pair counts."""
import os, sys, collections, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain
import json

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])


def field(w):
    t = (w / w.max()) ** A_PHI
    c = np.zeros(N); np.add.at(c, pn, t); c = c / c.sum()
    return np.full(N, 1.0 / N) - c


base = run_drain(field(W))
D0 = set(base["directed"])
out0 = collections.Counter(u for u, _ in D0)
sinks = [i for i in range(N) if out0[i] == 0]
print("sinks:", [ORDER[i] for i in sinks])

adj = collections.defaultdict(list)
for u, v in D0:
    adj[u].append(v)


def reach(src, banned=None):
    seen = {src}; st = [src]
    while st:
        x = st.pop()
        for y in adj[x]:
            if banned is not None and y == banned:
                continue
            if y not in seen:
                seen.add(y); st.append(y)
    return seen


EUR = json.load(open("europe_provinces.json")) if os.path.exists("europe_provinces.json") else None
# European NODES: use europe.py's own definition if available
import europe as EU
eurnodes = None
for attr in ("EUR_NODES", "EU_NODES", "NODES_EU", "EUROPE_NODES"):
    if hasattr(EU, attr):
        eurnodes = getattr(EU, attr); break
print("europe.py node attr:", eurnodes if eurnodes else "(none: deriving from european provinces)")
if eurnodes is None:
    # derive: nodes holding at least one counted European province
    eurprov = set(EU.EURO_PROV) if hasattr(EU, "EURO_PROV") else None
    print("has EURO_PROV:", eurprov is not None)
    if eurprov is None:
        names = [a for a in dir(EU) if not a.startswith("_")]
        print("europe module names:", names)
