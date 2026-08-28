import numpy as np, collections
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc, UND, EDGES_UND
from drain import run_drain

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
gidx = {g: gi for gi, g in GL}

gi = gidx["spices"]
b = S[gi] - C[gi]
r = run_drain(b)
directed = r["directed"]
adj = collections.defaultdict(list)
for u, v in directed: adj[u].append(v)

def reach(u):
    seen = {u}; q = collections.deque([u])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in seen: seen.add(y); q.append(y)
    return seen

cape = NIDX["cape_of_good_hope"]
malacca = NIDX["malacca"]
print("malacca out:", [ORDER[v] for v in adj[malacca]])
print("cape out:", [ORDER[v] for v in adj[cape]])
print("cape in:", [ORDER[u] for u,vs in adj.items() for v in vs if v==cape])
print("does malacca reach cape?", cape in reach(malacca))
print("does cape reach genua?", NIDX["genua"] in reach(cape))
print("does malacca reach genua (any path)?", NIDX["genua"] in reach(malacca))
print("does malacca reach genua VIA cape specifically?")
rc = reach(cape)
rm_direct = set(adj[malacca])
print("  cape's reach set includes genua:", NIDX["genua"] in rc)
print("does genua reach malacca (reverse direction)?", malacca in reach(NIDX["genua"]))
