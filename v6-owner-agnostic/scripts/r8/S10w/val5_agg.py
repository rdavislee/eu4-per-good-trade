# -*- coding: utf-8 -*-
"""Aggregate-field helper for the round-5 audit. Same construction measure6.py uses
(c_w from (w/w.max())**a summed per node, b_w = 1/N - c_w, DRAIN via drain.run_drain),
kept in one place so every variant below is computed the same way. Validated against
measure6.out's baseline before use."""
import collections, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS, EDGES_UND, PROV, PRICES, GOODS_PRODUCED_FACTOR, TAX_COEFF, ON_STARTUP_DEVASTATION
from drain import run_drain, has_cycle

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])

def cw(a, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a
    n = np.zeros(N); np.add.at(n, PN, t)
    return n / n.sum()

def agg(a=2.0, w=None):
    return run_drain(np.full(N, 1.0 / N) - cw(a, w))

def sinks(r):
    o = collections.Counter(u for u, _ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if o[i] == 0)

def flips(r1, r2):
    return len(set(r1["directed"]) ^ set(r2["directed"])) // 2

if __name__ == "__main__":
    b = agg(2.0)
    print("baseline a=2.0 sinks:", sinks(b), "edges", len(b["directed"]),
          "acyclic", has_cycle(b["directed"]) is None,
          "promotions", len(b["promotions"]), "fallbacks", len(b["fallbacks"]))
    print("world wealth %.2f  counted %d  N=%d  edges=%d" % (W.sum(), len(ROWS), N, len(EDGES_UND)))
