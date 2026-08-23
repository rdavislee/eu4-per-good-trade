# -*- coding: utf-8 -*-
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pdx
from solver import N, ORDER, NIDX, UND, EDGES_UND, ROWS, NODES
from drain import run_drain

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
EUR = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
EU_NODES = {n for n in ORDER if any(p in EUR for p in NODES[n]["members"])}
print("EU_NODES count:", len(EU_NODES))
print(sorted(EU_NODES))

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
od = collections.Counter(u for u,_ in dset)
sinks = [ORDER[i] for i in range(N) if od[i]==0]
print("sinks:", sinks)

adj = collections.defaultdict(list)
for u,v in dset: adj[u].append(v)
cape = NIDX["cape_of_good_hope"]

def reach_set(a):
    seen={a}; q=collections.deque([a])
    while q:
        x=q.popleft()
        for y in adj[x]:
            if y not in seen: seen.add(y); q.append(y)
    return seen

pairs = 0
cape_transit = 0
for eu in EU_NODES:
    R = reach_set(eu)
    for s in sinks:
        si = NIDX[s]
        if si in R:
            pairs += 1
            # check if cape transiting path exists: eu reaches cape AND cape reaches s
            if cape in R:
                Rcape = reach_set(cape)
                if si in Rcape:
                    cape_transit += 1

print("connected Europe->sink pairs:", pairs)
print("of them, cape-transiting-possible pairs:", cape_transit)
