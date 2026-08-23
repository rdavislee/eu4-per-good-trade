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
r = run_drain(np.full(N, 1.0 / N) - n / n.sum())
D0 = set(r["directed"])
cape = NIDX["cape_of_good_hope"]

adj = collections.defaultdict(list)
radj = collections.defaultdict(list)
for u, v in D0:
    adj[u].append(v); radj[v].append(u)

INF = 10**9
dist = [[INF]*N for _ in range(N)]
for a in range(N):
    dist[a][a] = 0
    q = collections.deque([a])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if dist[a][y] == INF:
                dist[a][y] = dist[a][x] + 1
                q.append(y)

unique_via_cape = 0
for a in range(N):
    if a == cape:
        continue
    tot = [0]*N; via = [0]*N
    tot[a] = 1
    for x in sorted(range(N), key=lambda z: dist[a][z]):
        if x == a or dist[a][x] == INF:
            continue
        for u in radj[x]:
            if dist[a][u] + 1 == dist[a][x]:
                tot[x] += tot[u]
                via[x] += via[u] + (1 if u == cape else 0)
        # normalize via as boolean-ish count isn't quite right; redo below
    # second pass properly: track (count_total, count_through_cape) via DP topologically by dist
    tot2 = [0]*N; thr2 = [0]*N
    tot2[a] = 1; thr2[a] = 0
    for x in sorted(range(N), key=lambda z: dist[a][z]):
        if x == a or dist[a][x] == INF:
            continue
        for u in radj[x]:
            if dist[a][u] + 1 == dist[a][x]:
                tot2[x] += tot2[u]
                thr2[x] += thr2[u] + (tot2[u] if u == cape else 0)
    for b in range(N):
        if b in (a, cape) or dist[a][b] == INF:
            continue
        if tot2[b] == 1 and thr2[b] == 1:
            unique_via_cape += 1

print("pairs where the shortest path is UNIQUE and passes through the cape:", unique_via_cape)
