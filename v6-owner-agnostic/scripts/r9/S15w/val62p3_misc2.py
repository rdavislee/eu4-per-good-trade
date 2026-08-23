# -*- coding: utf-8 -*-
"""val part3: node scalings, Cape reversal, dev-stacking, shortest-path Cape count, noise seeds."""
import collections, os, sys, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import pdx, drain, flowop
from solver import N, ORDER, NIDX, ROWS, NODES, UND, GOODS, PRICES, build_sc, PROV
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
A_PHI = 2.0
def phi(w, a=A_PHI):
    t = (w / w.max()) ** a
    n = np.zeros(N); np.add.at(n, PN, t)
    return run_drain(np.full(N, 1.0 / N) - n / n.sum())
def sk(r):
    od = collections.Counter(u for u, _ in r["directed"])
    return tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0))
BASE = phi(W); D0 = set(BASE["directed"])

W18 = ["english_channel","north_sea","baltic_sea","white_sea","novgorod","lubeck","rheinland",
       "saxony","wien","krakow","pest","venice","ragusa","genua","champagne","bordeaux",
       "valencia","sevilla"]
E4 = ["constantinople","crimea","kiev","kazan"]
def scale_nodes(names, k):
    idx = {NIDX[x] for x in names}
    return np.array([W[i] * (k if PN[i] in idx else 1.0) for i in range(len(ROWS))])

print("=== 18 western/central NODES scaled ===")
last=None; first_sole=None; broke=None
for j in range(100, 2601):
    k = j / 100.0
    s = sk(phi(scale_nodes(W18, k)))
    if s != last:
        print("  x%.2f  %s" % (k, ",".join(s))); last = s
    if s == ("genua",):
        if first_sole is None: first_sole = k
    elif first_sole is not None and broke is None:
        broke = k
print("  first x with genua the SOLE sink: %s ; first x after that where it is not: %s ; top of range x26.00" % (first_sole, broke))

print("\n=== all 22 NODES scaled ===")
last=None; sole=[]
for j in range(100, 2601):
    k = j / 100.0
    s = sk(phi(scale_nodes(W18 + E4, k)))
    if s != last:
        print("  x%.2f  %s" % (k, ",".join(s))); last = s
    if len(s) == 1: sole.append(k)
print("  multiples (x1.00..x26.00 step .01) with a SOLE sink:", sole[:10] or "none")

print("\n=== the Cape under the 22-node scaling ===")
cape = NIDX["cape_of_good_hope"]
prev=None
for j in range(100, 301):
    k = j / 100.0
    d = phi(scale_nodes(W18 + E4, k))["directed"]
    ins = tuple(sorted(ORDER[u] for u, v in d if v == cape))
    outs = tuple(sorted(ORDER[v] for u, v in d if u == cape))
    if (ins, outs) != prev:
        print("  x%.2f  in=%-42s out=%s" % (k, ",".join(ins), ",".join(outs)))
        prev = (ins, outs)

print("\n=== dev-stacking a single node's top province ===")
for node in ("english_channel", "genua", "hangzhou"):
    idx = [i for i in range(len(ROWS)) if PN[i] == NIDX[node]]
    top = max(idx, key=lambda i: W[i])
    seq = []
    for k in (2, 5, 10, 25, 50, 100, 250, 1000):
        w = W.copy(); w[top] *= k
        seq.append((k, sk(phi(w))))
    print("  %-16s top province pid %d  " % (node, ROWS[top]["pid"]))
    for k, s in seq: print("      x%-6d %s" % (k, ",".join(s)))

print("\n=== +/-1%% wealth noise, six seeds ===")
for s_ in range(6):
    nz = 1 + np.random.default_rng(9000 + s_).uniform(-0.01, 0.01, size=len(W))
    r = phi(W * nz)
    print("  seed %d sinks %-28s edges moved %d" % (9000+s_, ",".join(sk(r)), len(set(r["directed"]) ^ D0)//2))

print("\n=== Cape ordered pairs: strict shortest-path readings ===")
adj = collections.defaultdict(list)
for u, v in D0: adj[u].append(v)
INF = 10**9
dist = [[INF]*N for _ in range(N)]
for a in range(N):
    dist[a][a] = 0; q = collections.deque([a])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if dist[a][y] == INF: dist[a][y] = dist[a][x] + 1; q.append(y)
some = sum(1 for a in range(N) for b in range(N)
           if a != b and a != cape and b != cape and dist[a][b] < INF
           and dist[a][cape] + dist[cape][b] == dist[a][b])
print("  pairs with SOME shortest path through the cape:", some)
# every shortest path through the cape: count shortest paths total vs those avoiding cape
def npaths(a):
    """number of shortest paths a->b, and number avoiding the cape"""
    order_ = sorted(range(N), key=lambda x: dist[a][x])
    tot = [0]*N; av = [0]*N
    tot[a] = 1; av[a] = 0 if a == cape else 1
    for x in order_:
        if dist[a][x] == INF or x == a: continue
        for y in range(N):
            pass
    return tot, av
radj = collections.defaultdict(list)
for u, v in D0: radj[v].append(u)
every = 0
for a in range(N):
    if a == cape: continue
    tot = [0]*N; av = [0]*N
    tot[a] = 1; av[a] = 1
    for x in sorted(range(N), key=lambda z: dist[a][z]):
        if x == a or dist[a][x] == INF: continue
        for u in radj[x]:
            if dist[a][u] + 1 == dist[a][x]:
                tot[x] += tot[u]
                if u != cape: av[x] += av[u]
    for b in range(N):
        if b in (a, cape) or dist[a][b] == INF: continue
        if tot[b] > 0 and av[b] == 0: every += 1
print("  pairs where EVERY shortest path goes through the cape:", every)
