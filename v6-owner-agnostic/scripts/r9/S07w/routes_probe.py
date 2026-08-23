import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

def cv(a=A_PHI, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a
    n = np.zeros(N)
    np.add.at(n, pn, t)
    return n / n.sum()

cw = cv()
b_w = np.full(N, 1.0 / N) - cw
r = run_drain(b_w)
dset = set(r["directed"])

def check_path(names):
    ok = True
    for a, b in zip(names, names[1:]):
        ia, ib = NIDX[a], NIDX[b]
        present = (ia, ib) in dset
        print("  %-16s -> %-16s : %s" % (a, b, "OK" if present else "MISSING (or reversed=%s)" % ((ib,ia) in dset)))
        ok = ok and present
    return ok

print("Northern route (Volga/steppe):")
north = ["white_sea","novgorod","kazan","siberia","samarkand","lahore","lhasa",
         "ganges_delta","burma","gulf_of_siam","canton","hangzhou"]
print("all edges present:", check_path(north))

print()
print("Iberian route (African coast/Red Sea):")
iberia = ["sevilla","safi","timbuktu","katsina","ethiopia","gulf_of_aden","comorin_cape","ganges_delta"]
print("all edges present:", check_path(iberia))

# find out-edges of ganges_delta to see full continuation (eleven hops claim: sevilla..ganges_delta is 7 hops;
# "eleven hops" total presumably continues to hangzhou)
print()
print("out-edges of ganges_delta:", [ORDER[v] for (u,v) in dset if u==NIDX["ganges_delta"]])
print("in-edges of ganges_delta:", [ORDER[u] for (u,v) in dset if v==NIDX["ganges_delta"]])

# does sevilla reach hangzhou, and by how many hops via shortest path?
import collections as C
adj = C.defaultdict(list)
for (u,v) in dset: adj[u].append(v)
def bfs_path(s,t):
    s=NIDX[s]; t=NIDX[t]
    prev={s:None}; q=C.deque([s])
    while q:
        x=q.popleft()
        if x==t: break
        for y in adj[x]:
            if y not in prev:
                prev[y]=x; q.append(y)
    if t not in prev: return None
    path=[t]
    while path[-1]!=s:
        path.append(prev[path[-1]])
    return [ORDER[i] for i in reversed(path)]

p = bfs_path("sevilla","hangzhou")
print()
print("shortest sevilla->hangzhou path (%d hops):" % (len(p)-1 if p else -1), p)
