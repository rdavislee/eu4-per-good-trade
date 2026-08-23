# -*- coding: utf-8 -*-
"""Graph/tradenodes facts: sizes, components, 2-core, bridges, inland derivation,
declaration order, vanilla end flags."""
import collections, io, os, re, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import pdx
from solver import N, ORDER, NODES, NIDX, UND, EDGES_UND, COMPS
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
print("nodes                       :", N)
print("undirected edges            :", len(EDGES_UND))
print("directed arcs (2 per edge)  :", 2 * len(EDGES_UND))
print("components                  :", len(COMPS), [len(c) for c in COMPS])
deg = [len(UND[i]) for i in range(N)]
print("degree min/max/mean         :", min(deg), max(deg), round(float(np.mean(deg)), 3))
print("degree-1 nodes              :", [ORDER[i] for i in range(N) if deg[i] == 1])
# bridges
def bridges():
    tin = [-1]*N; low=[0]*N; res=[]; t=[0]
    def dfs(u, p):
        tin[u]=low[u]=t[0]; t[0]+=1
        skipped=False
        for v in UND[u]:
            if v==p and not skipped: skipped=True; continue
            if tin[v]!=-1: low[u]=min(low[u],tin[v])
            else:
                dfs(v,u); low[u]=min(low[u],low[v])
                if low[v]>tin[u]: res.append((u,v))
    sys.setrecursionlimit(10000)
    for i in range(N):
        if tin[i]==-1: dfs(i,-1)
    return res
br = bridges()
print("bridges                     :", len(br), [(ORDER[a],ORDER[b]) for a,b in br][:6])
# multiedges?
cnt = collections.Counter()
for n in ORDER:
    for m in NODES[n]["outgoing"]: cnt[tuple(sorted((n,m)))]+=1
print("duplicate declared links    :", {k:v for k,v in cnt.items() if v>1})
print("declared outgoing links     :", sum(cnt.values()))

# ---- vanilla file: inland flags, end flags, declaration order ----
fp = os.path.join(EU4, "common", "tradenodes", "00_tradenodes.txt")
txt = io.open(fp, encoding="latin-1").read()
tree = pdx.load(fp)
order = []; inland_flag = set(); end_flag = set(); outg = {}
members = {}
for k, v in tree:
    if not isinstance(v, pdx.Node): continue
    order.append(k)
    members[k] = [int(x) for x in pdx.values(v.get("members"))] if v.get("members") is not None else []
    if str(v.get("inland")).lower() == "yes": inland_flag.add(k)
    if str(v.get("end")).lower() == "yes": end_flag.add(k)
    outs = []
    for kk, vv in v:
        if kk == "outgoing" and isinstance(vv, pdx.Node):
            outs.append(str(vv.get("name")).strip('"'))
    outg[k] = outs
print()
print("file nodes                  :", len(order))
print("inland=yes count            :", len(inland_flag))
print("end=yes count               :", len(end_flag), sorted(end_flag))
pos = {n: i for i, n in enumerate(order)}
viol = [(n, m) for n in order for m in outg[n] if pos[m] <= pos[n]]
print("total outgoing declarations :", sum(len(v) for v in outg.values()))
print("links violating 'outgoing declared after':", len(viol), viol[:5])
# coastal members
import json
coastal = set(json.load(open(os.path.join(HERE, "coastal.json")))) if os.path.exists(os.path.join(HERE,"coastal.json")) else None
# derive coastal from map/default + adjacencies: use the mod's coastal.json if it is a list
cj = json.load(open(os.path.join(HERE, "coastal.json")))
print("coastal.json type:", type(cj).__name__, (list(cj)[:3] if isinstance(cj, dict) else cj[:3]))
