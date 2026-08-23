# -*- coding: utf-8 -*-
"""val part3: Cape, routes, marking order, Europe-node definitions, on the shipped 1444 field."""
import collections, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import pdx, drain
from solver import N, ORDER, NIDX, ROWS, NODES, UND, GOODS, PRICES, build_sc
from drain import run_drain, sinks_of

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
EURP = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
A_PHI = 2.0
_t = (W / W.max()) ** A_PHI
_n = np.zeros(N); np.add.at(_n, PN, _t)
BW = np.full(N, 1.0 / N) - _n / _n.sum()
R = run_drain(BW)
D = R["directed"]
adj = collections.defaultdict(list)
radj = collections.defaultdict(list)
for u, v in D: adj[u].append(v); radj[v].append(u)
od = collections.Counter(u for u, _ in D); idg = collections.Counter(v for _, v in D)
SINKS = [i for i in range(N) if od[i] == 0]
print("sinks:", [ORDER[i] for i in SINKS])
cape = NIDX["cape_of_good_hope"]

def reach(a, g=adj):
    seen = {a}; q = collections.deque([a])
    while q:
        x = q.popleft()
        for y in g[x]:
            if y not in seen: seen.add(y); q.append(y)
    return seen
RCH = {i: reach(i) for i in range(N)}

print("\n=== Europe node-set definitions ===")
byname = {n: NODES[n] for n in ORDER}
defs = {}
defs["any member province in continent europe (all members)"] = \
    sorted(n for n in ORDER if any(p in EURP for p in NODES[n]["members"]))
counted = collections.defaultdict(set)
for r in ROWS: counted[r["node"]].add(r["pid"])
defs["any COUNTED province in continent europe"] = \
    sorted(n for n in ORDER if any(p in EURP for p in counted[n]))
defs["majority of members in continent europe"] = \
    sorted(n for n in ORDER if NODES[n]["members"] and
           sum(1 for p in NODES[n]["members"] if p in EURP) * 2 > len(NODES[n]["members"]))
DOC22 = ["english_channel","north_sea","baltic_sea","white_sea","novgorod","lubeck","rheinland",
         "saxony","wien","krakow","pest","venice","ragusa","genua","champagne","bordeaux",
         "valencia","sevilla","constantinople","crimea","kiev","kazan"]
defs["the document's 22"] = sorted(DOC22)
for k, v in defs.items():
    print("  %-46s %2d  %s" % (k, len(v), ",".join(v)))

print("\n=== Europe -> sink pairs and Cape transit, per definition ===")
def capetransit(a, b):
    """does SOME directed a->b path pass through the cape?"""
    return (cape in RCH[a]) and (b in RCH[cape]) and a != cape
for k, v in defs.items():
    idx = [NIDX[x] for x in v]
    pairs = [(a, s) for a in idx for s in SINKS if s != a and s in RCH[a]]
    trans = [(a, s) for a, s in pairs if capetransit(a, s)]
    print("  %-46s nodes=%2d  connected Europe->sink pairs=%2d  cape-transiting=%d"
          % (k, len(idx), len(pairs), len(trans)))

print("\n=== the Cape ===")
print("  in-degree %d out-degree %d" % (idg[cape], od[cape]))
print("  in from :", sorted(ORDER[u] for u in radj[cape]))
print("  out to  :", sorted(ORDER[v] for v in adj[cape]))
up = [i for i in range(N) if i != cape and cape in RCH[i]]
down = RCH[cape] - {cape}
loose = sum(1 for a in up for b in down if b != a and b in RCH[a])
print("  loose ordered pairs (a->cape, cape->b, a->b):", loose)
# strict reading: pairs whose SHORTEST path uses the cape
def bfs_path(a, b):
    prev = {a: None}; q = collections.deque([a])
    while q:
        x = q.popleft()
        if x == b: break
        for y in adj[x]:
            if y not in prev: prev[y] = x; q.append(y)
    if b not in prev: return None
    p = []; x = b
    while x is not None: p.append(x); x = prev[x]
    return p[::-1]
strict = 0
for a in range(N):
    for b in range(N):
        if a == b: continue
        p = bfs_path(a, b)
        if p and cape in p and cape not in (a, b): strict += 1
print("  strict reading (BFS shortest path uses the cape):", strict)

print("\n=== routes ===")
def rt(a, b):
    p = bfs_path(NIDX[a], NIDX[b])
    return " -> ".join(ORDER[x] for x in p) if p else "NO ROUTE"
print("  white_sea -> hangzhou :", rt("white_sea", "hangzhou"))
print("  sevilla   -> hangzhou :", rt("sevilla", "hangzhou"))
print("  sevilla   -> ganges_delta :", rt("sevilla", "ganges_delta"))
print("  english_channel -> genua :", rt("english_channel", "genua"))
print("  english_channel -> hangzhou :", rt("english_channel", "hangzhou"))
print("  genua out-degree %d in-degree %d ; in from %s"
      % (od[NIDX["genua"]], idg[NIDX["genua"]], sorted(ORDER[u] for u in radj[NIDX["genua"]])))

print("\n=== marking order as a potential ===")
order = R["order"]
viol = sum(1 for (u, v) in D if not (order.get(u, -1) > order.get(v, -1)))
print("  order defined on %d of %d nodes" % (len(order), N))
print("  edges (u,v) with NOT order[u] > order[v]: %d of %d" % (viol, len(D)))
# peeled nodes have no order entry
peeled = [i for i in range(N) if i not in order]
print("  nodes with no marking order (Phase-0 peeled): %d %s" % (len(peeled), [ORDER[i] for i in peeled]))

print("\n=== sources ===")
src = [i for i in range(N) if idg[i] == 0]
CW = _n / _n.sum()
rank = {i: r for r, i in enumerate(sorted(range(N), key=lambda j: -CW[j]), 1)}
print("  count %d ; names %s" % (len(src), sorted(ORDER[i] for i in src)))
print("  c_w rank range (%d, %d) ; mean degree %.2f ; map mean degree %.2f"
      % (min(rank[i] for i in src), max(rank[i] for i in src),
         float(np.mean([len(UND[i]) for i in src])), float(np.mean([len(UND[i]) for i in range(N)]))))
print("  all in bottom half of wealth field (rank > %d): %s" % (N // 2, all(rank[i] > N // 2 for i in src)))

print("\n=== every node drains to a sink ===")
SS = set(SINKS)
print("  nodes reaching a sink: %d of %d" % (sum(1 for i in range(N) if RCH[i] & SS), N))
print("  acyclic:", drain.has_cycle(D) is None, " edges oriented: %d" % len(D))

print("\n=== per-good: does the Cape carry spices toward Europe? ===")
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
gi = GOODS.index("spices")
rs = run_drain(S[gi] - C[gi])
a2 = collections.defaultdict(list)
for u, v in rs["directed"]: a2[u].append(v)
print("  spices: cape out ->", sorted(ORDER[v] for v in a2[cape]))
sp = reach(cape, a2)
EUIDX = {NIDX[x] for x in DOC22}
print("  spices: cape reaches European nodes:", sorted(ORDER[i] for i in sp & EUIDX))
