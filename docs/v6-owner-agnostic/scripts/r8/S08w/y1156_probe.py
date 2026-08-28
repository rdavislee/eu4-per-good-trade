# -*- coding: utf-8 -*-
import collections, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
A_PHI = 2.0
t = (W / W.max()) ** A_PHI
n = np.zeros(N); np.add.at(n, PN, t)
BASE = run_drain(np.full(N, 1.0/N) - n/n.sum())
D0 = set(BASE["directed"])
cape = NIDX["cape_of_good_hope"]

adj = collections.defaultdict(list)
radj = collections.defaultdict(list)
for u, v in D0: adj[u].append(v); radj[v].append(u)
INF = 10**9
dist = [[INF]*N for _ in range(N)]
for a in range(N):
    dist[a][a] = 0; q = collections.deque([a])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if dist[a][y] == INF: dist[a][y] = dist[a][x] + 1; q.append(y)

unique_via_cape = 0
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
        if tot[b] == 1 and av[b] == 0:
            unique_via_cape += 1
print("pairs where the UNIQUE shortest path goes through the cape:", unique_via_cape)
