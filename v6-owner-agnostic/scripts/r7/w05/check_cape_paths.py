# -*- coding: utf-8 -*-
"""Reproduce the Cape's three stricter pair-count readings: some-shortest-path (71),
every-shortest-path (60), unique-shortest-path (43), against the loose reading (81)."""
import collections, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
A_PHI = 2.0
_t = (W / W.max()) ** A_PHI
_n = np.zeros(N); np.add.at(_n, PN, _t)
BW = np.full(N, 1.0 / N) - _n / _n.sum()
R = run_drain(BW)
D = R["directed"]
adj = collections.defaultdict(list)
for u, v in D: adj[u].append(v)
cape = NIDX["cape_of_good_hope"]

def bfs_dist_count(src, blocked=None):
    """returns (dist dict, count dict) of shortest-path distances/counts from src,
    optionally with node `blocked` removed from the graph (edges through it excluded)."""
    dist = {src: 0}; count = {src: 1}
    q = collections.deque([src])
    while q:
        x = q.popleft()
        if blocked is not None and x == blocked and x != src:
            continue
        for y in adj[x]:
            if blocked is not None and y == blocked and y != src:
                continue
            if y not in dist:
                dist[y] = dist[x] + 1; count[y] = count[x]
                q.append(y)
            elif dist[y] == dist[x] + 1:
                count[y] += count[x]
    return dist, count

# full-graph distances/counts from every node (needed as source), and separately
# with the cape removed (needed to test "every shortest path uses the cape")
DIST = {}; CNT = {}
DIST_NOCAPE = {}
for a in range(N):
    d, c = bfs_dist_count(a)
    DIST[a] = d; CNT[a] = c
    d2, _ = bfs_dist_count(a, blocked=cape)
    DIST_NOCAPE[a] = d2

# reachability (for the loose/81 baseline, cross-check)
def reach(a):
    seen = {a}; q = collections.deque([a])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in seen: seen.add(y); q.append(y)
    return seen
RCH = {i: reach(i) for i in range(N)}
up = [i for i in range(N) if i != cape and cape in RCH[i]]
down = RCH[cape] - {cape}
loose = sum(1 for a in up for b in down if b != a and b in RCH[a])

some = every = unique = 0
some_pairs = []
for a in range(N):
    if a == cape: continue
    da = DIST[a]
    if cape not in da: continue
    dnc_a = DIST_NOCAPE[a]
    for b in range(N):
        if b == a or b == cape: continue
        if b not in da: continue
        dab = da[b]
        d_a_cape = da[cape]
        d_cape_b = DIST[cape].get(b)
        if d_cape_b is None: continue
        if d_a_cape + d_cape_b == dab:
            some += 1
            # every: removing the cape does not preserve the distance (or makes b unreachable)
            alt = dnc_a.get(b)
            if alt is None or alt > dab:
                every += 1
            # unique: exactly one shortest path total from a to b
            if CNT[a].get(b, 0) == 1:
                unique += 1

print("loose reading (a->cape, cape->b, a->b), cross-check : %d" % loose)
print("some shortest path transits the cape                : %d" % some)
print("every shortest path transits the cape                : %d" % every)
print("unique shortest path (and it transits the cape)      : %d" % unique)
