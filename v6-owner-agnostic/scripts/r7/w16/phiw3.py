# -*- coding: utf-8 -*-
"""v2.1 addendum, part 3: V225 gravity kernel count-follows-seeds + agreement ceiling;
V215 rank readings; V216 cul-de-sac characterisation; V230 latent-good detail."""
import numpy as np, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc, NODES)
from drain import run_drain

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, wealth)

def c_w_of(a, w=None):
    w = wealth if w is None else w
    t = (w / w.max()) ** a
    num = np.zeros(N); np.add.at(num, pn, t)
    return num / num.sum()

c15 = c_w_of(1.5)
D = np.full((N, N), 99)
for s in range(N):
    D[s][s] = 0; q = collections.deque([s])
    while q:
        x = q.popleft()
        for y in UND[x]:
            if D[s][y] == 99: D[s][y] = D[s][x] + 1; q.append(y)
van = set()
for n in ORDER:
    for m in NODES[n]["outgoing"]: van.add((NIDX[n], NIDX[m]))

print("=" * 100); print("V225  does the end count follow the number of masses?"); print("=" * 100)
def topk_unconnected(k):
    out = []
    for i in np.argsort(-c15):
        if all(D[i][j] > 1 for j in out): out.append(int(i))
        if len(out) == k: break
    return out
for k in (1, 2, 3, 4, 5, 6):
    seeds = topk_unconnected(k)
    row = []
    for gam in (0.1, 0.3, 0.5, 0.7, 0.9):
        P = np.array([max(c15[m] * (gam ** D[n][m]) for m in seeds) for n in range(N)])
        oc = collections.Counter()
        for u, v in EDGES_UND: oc[(u if P[u] < P[v] else v)] += 1
        row.append(sum(1 for i in range(N) if oc[i] == 0))
    print("  %d masses (%s) -> ends at gamma .1/.3/.5/.7/.9 = %s"
          % (k, ",".join(ORDER[s] for s in seeds), row))

print()
print("  agreement ceiling, 3 masses, gamma -> 1:")
best = 0
for gam in [0.90, 0.93, 0.95, 0.97, 0.98, 0.99, 0.995, 0.999]:
    seeds = topk_unconnected(3)
    P = np.array([max(c15[m] * (gam ** D[n][m]) for m in seeds) for n in range(N)])
    dd = set(); oc = collections.Counter()
    for u, v in EDGES_UND:
        a, b = (u, v) if P[u] < P[v] else (v, u)
        dd.add((a, b)); oc[a] += 1
    ag = sum(1 for e in dd if e in van)
    best = max(best, ag)
    print("    gamma=%-6s ends=%-3d agreement %d/159 = %.0f%%" % (gam, sum(1 for i in range(N) if oc[i]==0), ag, 100*ag/159))
print("  best agreement found: %d/159 = %.1f%% (claim says 69%% = %d/159)" % (best, 100*best/159, round(0.69*159)))

print()
print("=" * 100); print("V215  rank readings for the two sinks"); print("=" * 100)
wr = {ORDER[i]: k+1 for k, i in enumerate(np.argsort(-NODEW))}
cr = {ORDER[i]: k+1 for k, i in enumerate(np.argsort(-c15))}
for n in ("english_channel", "hangzhou", "genua"):
    print("  %-18s node wealth=%.1f (rank %2d) | c_w(a=1.5)=%.5f (rank %2d)"
          % (n, NODEW[NIDX[n]], wr[n], c15[NIDX[n]], cr[n]))
print("  top-5 by c_w(1.5): %s" % [ORDER[i] for i in np.argsort(-c15)[:5]])

print()
print("=" * 100); print("V216  are the 8 sources cul-de-sacs?"); print("=" * 100)
b = np.full(N, 1.0/N) - c15
r = run_drain(b); d = r["directed"]
idg = collections.Counter(v for _, v in d)
srcs = [i for i in range(N) if idg[i] == 0]
degs = [len(UND[i]) for i in range(N)]
print("  mean degree all nodes: %.2f | mean degree of sources: %.2f"
      % (np.mean(degs), np.mean([len(UND[i]) for i in srcs])))
print("  source c_w ranks: %s" % [(ORDER[i], cr[ORDER[i]]) for i in srcs])
print("  degree-2 (true cul-de-sac-ish) among sources: %d of %d"
      % (sum(1 for i in srcs if len(UND[i]) == 2), len(srcs)))
