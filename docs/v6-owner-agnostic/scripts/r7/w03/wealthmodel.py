# -*- coding: utf-8 -*-
"""The v5 (Option 1) corrected wealth field, as one importable model.
16 provinces carry local modifiers beyond gems/incense; see the audit trail."""
import numpy as np, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, UND, EDGES_UND, PROV, PNODE, PRICES, ROWS, NODES
from drain import run_drain

FLAT  = {8:3.0, 684:0.5, 1821:0.5, 1822:0.5, 2145:0.5,
         6:2.0, 362:2.0, 363:2.0, 370:1.0, 371:1.0, 387:3.0, 542:4.0, 2151:2.5, 2316:2.0, 4316:2.0}
GPMOD = {262:0.10}
TVMOD = {684:0.1, 1821:0.1, 1822:0.1, 2145:0.1}
PN = np.array([NIDX[r["node"]] for r in ROWS])

def wealth(dev_mult=None):
    """dev_mult: dict pid->factor applied to base_tax AND base_production (development growth)."""
    dev_mult = dev_mult or {}
    w = []
    for r in ROWS:
        pid = r["pid"]; g = r["good"]; f = dev_mult.get(pid, 1.0)
        bt = PROV[pid]["base_tax"] * f
        bp = PROV[pid]["base_production"] * f
        gp = (0.2 * bp + FLAT.get(pid, 0.0)) * (1.0 + GPMOD.get(pid, 0.0))
        tv = (0.10 if g == "incense" else 0.0) + TVMOD.get(pid, 0.0)
        w.append(bt * (1.0 + (0.15 if g == "gems" else 0.0)) + gp * PRICES.get(g, 0.0) * (1.0 + tv))
    return np.array(w)

def phi_w(w, alpha=1.5):
    t = (w / w.max()) ** alpha
    num = np.zeros(N); np.add.at(num, PN, t)
    return run_drain(np.full(N, 1.0 / N) - num / num.sum()), num / num.sum()

def sinks(r):
    od = collections.Counter(u for u, _ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if od[i] == 0)

def node_wealth(w):
    nw = np.zeros(N); np.add.at(nw, PN, w); return nw

def route(r, src, dst):
    """the directed path the wealth map actually draws from src to dst"""
    adj = collections.defaultdict(list)
    for u, v in r["directed"]: adj[u].append(v)
    s, d = NIDX[src], NIDX[dst]
    prev = {s: None}; q = collections.deque([s])
    while q:
        x = q.popleft()
        if x == d: break
        for y in adj[x]:
            if y not in prev: prev[y] = x; q.append(y)
    if d not in prev: return None
    p = []; x = d
    while x is not None: p.append(ORDER[x]); x = prev[x]
    return list(reversed(p))
