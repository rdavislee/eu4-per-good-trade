# -*- coding: utf-8 -*-
"""v5 1.6: the institution demonstration and the 1444 route, on the shipped wealth field."""
import numpy as np, collections, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx
from solver import N, ORDER, NIDX, PROV, ROWS, NODES, PRICES
from drain import run_drain
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
EUR = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
LOW = {90,92,95,96,97,98,99,100,1744}          # the 9 Lowland provinces in english_channel
PN = np.array([NIDX[r["node"]] for r in ROWS])
BASE = np.array([r["tax"] + r["prod_income"] for r in ROWS])

def field(mult):
    """multiplier on development -> both wealth terms scale with it"""
    return np.array([BASE[i] * mult.get(r["pid"], 1.0) for i, r in enumerate(ROWS)])

def sinks(w, a=1.5):
    t = (w / w.max()) ** a
    num = np.zeros(N); np.add.at(num, PN, t)
    r = run_drain(np.full(N, 1.0 / N) - num / num.sum())
    od = collections.Counter(u for u, _ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if od[i] == 0), r

OWNED = {r["pid"] for r in ROWS}
eur = sorted(EUR & OWNED)
eu_nodes = {n for n in ORDER if any(p in EUR for p in NODES[n]["members"])}
print("Europe: %d owned provinces in %d nodes" % (len(eur), len(eu_nodes)))
print("\n=== European development growth, alpha_Phi = 1.5 fixed ===")
last = None
for k in range(0, 61, 1):
    f = 1.0 + 0.01 * k
    s, _ = sinks(field({p: f for p in eur}))
    if tuple(s) != last:
        eu = [x for x in s if x in eu_nodes]
        print("   x%.2f  %d sinks %-56s European: %s" % (f, len(s), s, eu or "none"))
        last = tuple(s)
print("\n=== the Lowlands alone (9 provinces in english_channel) ===")
for f in (1.1, 1.2, 1.25, 1.5, 2.0, 5.0, 10.0):
    s, _ = sinks(field({p: f for p in LOW}))
    print("   x%-5.2f %s" % (f, s))
print("\n=== robust to noise, responsive to regional growth ===")
for seed in range(3):
    nz = 1 + np.random.default_rng(seed).uniform(-0.02, 0.02, size=len(BASE))
    print("   +/-2%% random noise, seed %d -> %s" % (seed, sinks(BASE * nz)[0]))
print("   +2%% systematic to Europe only     -> %s" % sinks(field({p: 1.02 for p in eur}))[0])
print("\n=== the 1444 route ===")
s, r = sinks(BASE)
adj = collections.defaultdict(list)
for u, v in r["directed"]: adj[u].append(v)
def path(a, b):
    s0, d0 = NIDX[a], NIDX[b]; prev = {s0: None}; q = collections.deque([s0])
    while q:
        x = q.popleft()
        if x == d0: break
        for y in adj[x]:
            if y not in prev: prev[y] = x; q.append(y)
    if d0 not in prev: return None
    p = []; x = d0
    while x is not None: p.append(ORDER[x]); x = prev[x]
    return list(reversed(p))
for src in ("genua", "north_sea", "english_channel", "venice"):
    print("   %-16s : %s" % (src, " -> ".join(path(src, s[0]))))
