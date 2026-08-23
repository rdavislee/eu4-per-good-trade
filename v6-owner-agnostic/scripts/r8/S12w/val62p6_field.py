# -*- coding: utf-8 -*-
"""Node wealth ranks, Phi_w orientation, net-flow-aggregate cycles, gulf_of_siam downstream sets."""
import os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import drain, flowop
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, sinks_of
from flowop import mincost_flow, ARCS

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, PN, W)
rank = sorted(range(N), key=lambda i: -NODEW[i])
print("=== node wealth ranks (top 10) ===")
for k, i in enumerate(rank[:10]):
    print("  %2d  %-22s %.1f" % (k+1, ORDER[i], NODEW[i]))
for nm in ("english_channel", "genua", "mexico", "gulf_of_siam", "sevilla", "hangzhou"):
    i = NIDX[nm]; print("  %-22s wealth %.1f  rank %d" % (nm, NODEW[i], rank.index(i)+1))

def bw(alpha=A_PHI):
    t = (W / W.max()) ** alpha
    n = np.zeros(N); np.add.at(n, PN, t)
    return np.full(N, 1.0/N) - n/n.sum()

B = bw()
R = run_drain(B)
print("\n=== Phi_w sinks / orientation ===")
print("  sinks:", [ORDER[i] for i in sinks_of(R["directed"])[0]])
dirs = R["directed"]
succ = collections.defaultdict(list)
for u, v in dirs: succ[u].append(v)
print("  english_channel -> ", [ORDER[v] for v in succ[NIDX["english_channel"]]])
print("  genua out-degree", len(succ[NIDX["genua"]]))
print("  net demanders (-b_w>0):", sum(1 for i in range(N) if -B[i] > 0))

# net-flow aggregate: sum_g V_g * net_g -- does it contain directed cycles?
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
netagg = np.zeros(len(EDGES_UND))
for gi, g in GL:
    r = run_drain(S[gi] - C[gi])
    f = r["flow"] if "flow" in r else None
    net = r.get("net")
    if net is None:
        raise SystemExit("run_drain gives keys: %s" % list(r.keys()))
    netagg += V[gi] * np.asarray(net)
print("\n=== value-weighted net flow aggregate ===")
E = list(EDGES_UND)
darcs = []
for ei, (u, v) in enumerate(E):
    if netagg[ei] > 1e-12: darcs.append((u, v))
    elif netagg[ei] < -1e-12: darcs.append((v, u))
print("  oriented edges: %d of %d" % (len(darcs), len(E)))
adj = collections.defaultdict(list)
for u, v in darcs: adj[u].append(v)
colour = [0]*N; cyc = []
def dfs(u, stack):
    colour[u] = 1; stack.append(u)
    for v in adj[u]:
        if colour[v] == 1:
            cyc.append([ORDER[x] for x in stack[stack.index(v):]] + [ORDER[v]])
        elif colour[v] == 0:
            dfs(v, stack)
    stack.pop(); colour[u] = 2
sys.setrecursionlimit(10000)
for i in range(N):
    if colour[i] == 0: dfs(i, [])
print("  directed cycles found: %d" % len(cyc))
for c in cyc[:4]: print("    ", " -> ".join(c))

# gulf_of_siam: distinct downstream sets across goods
print("\n=== gulf_of_siam downstream sets per good ===")
gsi = NIDX["gulf_of_siam"]
sets = {}
for gi, g in GL:
    r = run_drain(S[gi] - C[gi])
    d = frozenset(ORDER[v] for u, v in r["directed"] if u == gsi)
    sets.setdefault(d, []).append(g)
print("  live goods: %d ; distinct downstream sets: %d" % (len(GL), len(sets)))
for d, gs in sorted(sets.items(), key=lambda kv: -len(kv[1])):
    print("    %-45s  %d goods: %s" % (sorted(d), len(gs), ",".join(gs[:6])))
