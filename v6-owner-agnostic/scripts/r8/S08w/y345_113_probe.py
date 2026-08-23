# -*- coding: utf-8 -*-
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, UND, EDGES_UND, ROWS
from drain import run_drain

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cv(a=A_PHI):
    w = W
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()

cw = cv()
b_w = np.full(N, 1.0/N) - cw
r = run_drain(b_w)
dset = set(r["directed"])

def check_route(route):
    ok = True
    for a,b in zip(route, route[1:]):
        ia, ib = NIDX[a], NIDX[b]
        edge_ok = (ia, ib) in dset
        print(f"  {a} -> {b}: {'OK' if edge_ok else 'MISSING/REVERSED'}")
        if not edge_ok: ok = False
    return ok

print("=== northern route ===")
north = ["white_sea","novgorod","kazan","siberia","samarkand","lahore","lhasa","ganges_delta","burma","gulf_of_siam","canton","hangzhou"]
print("all hops OK:", check_route(north))

print("=== iberian route ===")
iberia = ["sevilla","safi","timbuktu","katsina","ethiopia","gulf_of_aden","comorin_cape","ganges_delta"]
print("all hops OK:", check_route(iberia))
print("iberia route hop count:", len(iberia)-1)

# genua out-degree / in-degree
gi = NIDX["genua"]
outdeg = sum(1 for u,v in dset if u==gi)
indeg = sum(1 for u,v in dset if v==gi)
print("genua out-degree:", outdeg, "in-degree:", indeg)

# english_channel
eci = NIDX["english_channel"]
outdeg_ec = sum(1 for u,v in dset if u==eci)
print("english_channel out-degree:", outdeg_ec)
print("english_channel -> champagne -> genua:")
champ = NIDX["champagne"]
print("  ec->champagne:", (eci,champ) in dset)
print("  champagne->genua:", (champ,gi) in dset)

# reach: is there any path from english_channel to hangzhou?
import collections
adj = collections.defaultdict(list)
for u,v in dset: adj[u].append(v)
def reaches(a,b):
    seen={a}; q=collections.deque([a])
    while q:
        x=q.popleft()
        if x==b: return True
        for y in adj[x]:
            if y not in seen: seen.add(y); q.append(y)
    return b in seen
hz = NIDX["hangzhou"]
print("english_channel reaches hangzhou:", reaches(eci, hz))
