# -*- coding: utf-8 -*-
"""val part3: Cape strict count under BFS tie-breaks, spices direction, unit-cost disagreement,
the doc's northern route as an edge check, and the third sweep key."""
import collections, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import drain, flowop
from solver import N, ORDER, NIDX, ROWS, EDGES_UND, GOODS, PRICES, build_sc, UND
from drain import run_drain, phase0, phase1, phase2, sweep_priority, compile_dirs

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
_t = (W / W.max()) ** 2.0
_n = np.zeros(N); np.add.at(_n, PN, _t)
BW = np.full(N, 1.0 / N) - _n / _n.sum()
R = run_drain(BW); D = set(R["directed"]); cape = NIDX["cape_of_good_hope"]

print("=== Cape strict count under different BFS successor orders ===")
base = collections.defaultdict(list)
for u, v in R["directed"]: base[u].append(v)
def count(adj):
    tot = 0
    for a in range(N):
        prev = {a: None}; q = collections.deque([a])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y not in prev: prev[y] = x; q.append(y)
        for b in range(N):
            if b in (a, cape) or b not in prev or a == cape: continue
            p = []; x = b
            while x is not None: p.append(x); x = prev[x]
            if cape in p: tot += 1
    return tot
for tag, f in (("insertion order", lambda l: l),
               ("ascending index", sorted),
               ("descending index", lambda l: sorted(l, reverse=True))):
    adj = {u: f(list(base.get(u, []))) for u in range(N)}
    print("  %-18s -> %d" % (tag, count(adj)))

print("\n=== per-good spices: is there an Asia -> cape -> Europe path? ===")
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
gi = GOODS.index("spices")
rs = run_drain(S[gi] - C[gi])
a2 = collections.defaultdict(list); r2 = collections.defaultdict(list)
for u, v in rs["directed"]: a2[u].append(v); r2[v].append(u)
def rch(a, g):
    seen = {a}; q = collections.deque([a])
    while q:
        x = q.popleft()
        for y in g[x]: 
            if y not in seen: seen.add(y); q.append(y)
    return seen
print("  spices cape in-edges  :", sorted(ORDER[u] for u in r2[cape]))
print("  spices cape out-edges :", sorted(ORDER[v] for v in a2[cape]))
ASIA = {"malacca","gulf_of_siam","canton","hangzhou","comorin_cape","ganges_delta","burma",
        "doab","lahore","gujarat","beijing","xian","girin","nippon","yumen","lhasa","samarkand"}
into = rch(cape, r2)   # nodes that reach cape
EUR22 = {"english_channel","north_sea","baltic_sea","white_sea","novgorod","lubeck","rheinland",
         "saxony","wien","krakow","pest","venice","ragusa","genua","champagne","bordeaux",
         "valencia","sevilla","constantinople","crimea","kiev","kazan"}
frm = rch(cape, a2)
print("  Asian nodes reaching the cape in the spices graph:",
      sorted(ORDER[i] for i in into if ORDER[i] in ASIA))
print("  European nodes the cape reaches in the spices graph:",
      sorted(ORDER[i] for i in frm if ORDER[i] in EUR22))
# spices producers
val = np.zeros(N)
for i, r in enumerate(ROWS):
    if r["good"] == "spices": val[PN[i]] += r["prod_income"]
print("  top spice producers:", [ORDER[i] for i in np.argsort(-val)[:6]])

print("\n=== the unit-cost objective against the shipped tie-break objective ===")
o = flowop.TIE_COST.copy()
try:
    flowop.TIE_COST = drain.TIE_COST = np.ones(len(flowop.ARCS))
    ru = run_drain(BW)
    du = set(ru["directed"])
finally:
    flowop.TIE_COST = drain.TIE_COST = o
print("  edges differing between unit-cost DRAIN and shipped DRAIN: %d of %d" % (len(du ^ D)//2, len(EDGES_UND)))
odu = collections.Counter(u for u,_ in du)
print("  unit-cost sinks:", sorted(ORDER[i] for i in range(N) if odu[i]==0))

print("\n=== the document's northern route, edge by edge ===")
doc = ["white_sea","novgorod","kazan","siberia","samarkand","lahore","lhasa","ganges_delta",
       "burma","gulf_of_siam","canton","hangzhou"]
und = {tuple(sorted(e)) for e in EDGES_UND}
for a, b in zip(doc, doc[1:]):
    ia, ib = NIDX[a], NIDX[b]
    print("  %-16s -> %-16s directed:%-5s reverse:%-5s undirected edge exists:%s"
          % (a, b, (ia, ib) in D, (ib, ia) in D, tuple(sorted((ia, ib))) in und))
doci = ["sevilla","safi","timbuktu","katsina","ethiopia","gulf_of_aden","comorin_cape","ganges_delta"]
print("  Iberian prefix:")
for a, b in zip(doci, doci[1:]):
    ia, ib = NIDX[a], NIDX[b]
    print("    %-16s -> %-16s directed:%s" % (a, b, (ia, ib) in D))

print("\n=== the third sweep key ('def_absb') against the shipped one ===")
def facts(key):
    core, beta, Plog = phase0(BW)
    Sset, _ = phase1(core, beta)
    fa, free, net, _c = phase2(core, beta)
    o_, _S2, promo, fb = sweep_priority(core, beta, Sset, fa, free, net, key)
    d = compile_dirs(core, o_, fa, free, Plog, beta)
    od_ = collections.Counter(u for u, _ in d)
    return sorted(ORDER[i] for i in range(N) if od_[i] == 0), len(promo), len(fb), set(d)
for key in ("defasc_beta", "def_beta", "def_absb"):
    s, p, f, d = facts(key)
    print("  %-12s sinks=%-30s promo=%d fb=%d edges differing from shipped=%d"
          % (key, ",".join(s), p, f, len(d ^ D)//2))
