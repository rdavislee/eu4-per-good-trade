# -*- coding: utf-8 -*-
"""Check the two named long routes against the actual directed edge set D."""
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
D = set(R["directed"])
adj = collections.defaultdict(list)
for u, v in R["directed"]: adj[u].append(v)

def check_path(names):
    ok = True
    for i in range(len(names) - 1):
        u, v = NIDX[names[i]], NIDX[names[i+1]]
        present = (u, v) in D
        if not present:
            ok = False
        print("  %-14s -> %-14s : %s" % (names[i], names[i+1], "edge present" if present else "EDGE ABSENT/WRONG-DIR"))
    print("  path fully present and directed as stated:", ok, " hops:", len(names)-1)
    return ok

print("=== doc's northern route ===")
northern = ["white_sea","novgorod","kazan","siberia","samarkand","lahore","lhasa",
            "ganges_delta","burma","gulf_of_siam","canton","hangzhou"]
check_path(northern)

print()
print("=== doc's Iberian route (11 hops incl. final unlabelled leg to Asian end) ===")
iberian = ["sevilla","safi","timbuktu","katsina","ethiopia","gulf_of_aden","comorin_cape","ganges_delta"]
check_path(iberian)

# BFS shortest-path length white_sea -> hangzhou, and count of distinct shortest paths
def bfs_dist_count(src):
    dist = {src: 0}; count = {src: 1}
    q = collections.deque([src])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + 1; count[y] = count[x]; q.append(y)
            elif dist[y] == dist[x] + 1:
                count[y] += count[x]
    return dist, count

d, c = bfs_dist_count(NIDX["white_sea"])
print()
print("white_sea -> hangzhou shortest length:", d.get(NIDX["hangzhou"]), " # distinct shortest paths:", c.get(NIDX["hangzhou"]))

d2, c2 = bfs_dist_count(NIDX["sevilla"])
print("sevilla -> ganges_delta shortest length:", d2.get(NIDX["ganges_delta"]), " # distinct shortest paths:", c2.get(NIDX["ganges_delta"]))
print("sevilla -> hangzhou shortest length:", d2.get(NIDX["hangzhou"]), " # distinct shortest paths:", c2.get(NIDX["hangzhou"]))

# enumerate all shortest paths white_sea->hangzhou (small enough?) to see if doc's route is AMONG them
def all_shortest_paths(src, dst, dist):
    # DFS following only edges that decrease remaining distance by 1
    target_len = dist.get(dst)
    if target_len is None: return []
    paths = []
    stack = [(src, [src])]
    # limit explosion
    count_found = 0
    def dfs(u, path):
        nonlocal count_found
        if count_found > 200000: return
        if u == dst:
            paths.append(list(path)); count_found += 1
            return
        for v in adj[u]:
            if dist.get(v) == dist[u] + 1 and dist[v] + (target_len - dist[v]) == target_len:
                if len(path) - 1 + (target_len - dist[v]) <= target_len:
                    path.append(v); dfs(v, path); path.pop()
    dfs(src, [src])
    return paths

paths = all_shortest_paths(NIDX["white_sea"], NIDX["hangzhou"], d)
print("total shortest paths white_sea->hangzhou enumerated:", len(paths))
doc_path_idx = [NIDX[x] for x in northern]
match = any(p == doc_path_idx for p in paths)
print("doc's exact northern route is among the shortest paths:", match)
if not match and paths:
    print("example shortest path found:", [ORDER[i] for i in paths[0]])
