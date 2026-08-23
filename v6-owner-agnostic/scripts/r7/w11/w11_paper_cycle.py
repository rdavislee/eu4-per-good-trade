import sys, os, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc, EDGES_UND
from flowop import ARCS, AEQ, A, TIE_COST, LP_OPTS, mincost_flow

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
gi = GOODS.index("paper")
s = S0m[gi]; c = C0m[gi]
fl, du, res = mincost_flow(s, c, cost=TIE_COST)
rc = np.array([TIE_COST[ai] - (du[ARCS[ai][1]] - du[ARCS[ai][0]]) for ai in range(A)])

# net per undirected edge and its carrying direction (the "support" edges)
net = {}
for ai,(u,v,ei,sg) in enumerate(ARCS):
    net.setdefault(ei, 0.0)
    net[ei] += sg*fl[ai]
support_edges = []  # (u,v) meaning flow direction u->v with amount
for ei,(a,b) in enumerate(EDGES_UND):
    n = net[ei]
    if abs(n) > 1e-9:
        if n > 0: support_edges.append((a,b,n))
        else: support_edges.append((b,a,-n))

print("support edge count:", len(support_edges), "N-1=", N-1)

# build undirected tree adjacency from support edges (assume it's a tree, since N-1 edges & connected)
adj = collections.defaultdict(list)
for (u,v,f) in support_edges:
    adj[u].append((v, f, +1))  # traverse u->v costs "forward" i.e can reduce f if we push cycle backward through here
    adj[v].append((u, f, -1))

off_ai = None
for ai in np.where(fl <= 1e-12)[0]:
    if abs(rc[ai]) <= 1e-14:
        off_ai = ai; break
u0, v0, ei0, sg0 = ARCS[off_ai]
print("off-support zero-rc arc:", ORDER[u0], "->", ORDER[v0])

# BFS/DFS path from u0 to v0 in the tree
parent = {u0: None}
q = collections.deque([u0])
edge_used = {}
while q:
    x = q.popleft()
    if x == v0: break
    for (y, f, direction) in adj[x]:
        if y not in parent:
            parent[y] = x
            edge_used[y] = (x, y, f, direction)
            q.append(y)

# reconstruct path u0 -> v0
path = []
cur = v0
while cur != u0:
    x, y, f, direction = edge_used[cur]
    path.append((x, y, f, direction))
    cur = x
path.reverse()
print("tree path length:", len(path))
# For the cycle: off-support arc adds v0<-... wait off arc is u0->v0 with rc 0 meaning entering variable x(u0->v0).
# entering this raises flow u0->v0 by theta; to maintain conservation we adjust the tree path from u0 to v0:
# if tree edge is oriented same direction as path traversal (x->y, direction==+1, i.e. edge carries x->y and path goes x to y) it must DECREASE by theta (since we already push flow via new arc)
# if oriented opposite, must INCREASE by theta.
bottleneck = None
for (x,y,f,direction) in path:
    if direction == +1:
        # edge carries x->y with flow f; new arc's flow theta effectively reduces need along this direction => this edge flow decreases by theta, bounded below by 0
        limit = f
    else:
        # edge in tree is actually v->u meaning original support edge orientation is y->x (since we stored u->v with f); direction==-1 means we traversed edge backward
        limit = None  # increasing, no upper bound from this edge alone (other than overall solution)
    if limit is not None:
        if bottleneck is None or limit < bottleneck:
            bottleneck = limit
print("bottleneck theta (max flow pushable through off-support arc while staying optimal):", bottleneck)
