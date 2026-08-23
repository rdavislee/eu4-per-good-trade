import os, sys, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from solver import (ROWS, PROV, PRICES, ROLLED, GOODS, N, ORDER, NIDX, build_sc, EXCLUDED)

# Y033/Y034 breakdown
MON = {8,684,1821,1822,2145,262}
PERM = {6,362,363,370,371,387,542,2151,2316,4316}
MP = MON | PERM
gems = [r["pid"] for r in ROWS if r["good"] == "gems"]
inc = [r["pid"] for r in ROWS if r["good"] == "incense"]
mp = [r["pid"] for r in ROWS if r["pid"] in MP]
both = (set(gems) | set(inc)) & set(mp)
print("gems counted:", len(gems), "incense counted:", len(inc), "mon/perm counted:", len(mp))
print("overlap:", both)
print("union:", len(set(gems) | set(inc) | set(mp)))
print("4856 rolled:", ROLLED.get(4856), "| 4856 in history unknown:", PROV[4856].get("trade_goods"))

# is_city filter: which counted provinces lack is_city = yes in history parse?
# prov1444.json may carry is_city; check keys
sample = next(iter(PROV.values()))
print("prov1444 keys:", sorted(sample.keys()))
if "is_city" in sample:
    nocity = [r["pid"] for r in ROWS if not PROV[r["pid"]].get("is_city")]
    print("counted without is_city:", len(nocity), "265 among them:", 265 in nocity)
    # apparatus count under is_city filter
    u = [p for p in (set(gems)|set(inc)|set(mp)) if PROV[p].get("is_city")]
    print("apparatus provinces under is_city filter:", len(u))

# Y070: cost of pricing the 20 rolled provinces at zero = their trade value
tv20 = sum(r["prod_income"] for r in ROWS if PROV[r["pid"]].get("trade_goods") in (None, "unknown"))
print("trade value of the 20 rolled provinces: %.2f" % tv20)

# Y074: max base_tax among counted; and total dev of 1821
mx = max(ROWS, key=lambda r: PROV[r["pid"]]["base_tax"])
print("max base_tax counted:", PROV[mx["pid"]]["base_tax"], "at", mx["pid"])
s = PROV[1821]
print("1821 dev:", s["base_tax"], s["base_production"], s.get("base_manpower"), "total:",
      s["base_tax"] + s["base_production"] + (s.get("base_manpower") or 0))

# Y276: nodes with b == 0 exactly, per good and for wealth field
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, live, gp, world = build_sc(ALPHA, eps=0.0)
zero_nodes = set()
for gi, g in enumerate(GOODS):
    if not live[gi]: continue
    b = S[gi] - C[gi]
    for i in range(N):
        if b[i] == 0.0:
            zero_nodes.add((g, ORDER[i]))
from collections import Counter
cnt = Counter(n for _, n in zero_nodes)
print("nodes with b==0 exactly (any good):", dict(cnt))
# wealth field b_w
wealth = np.zeros(N)
for r in ROWS:
    wealth[NIDX[r["node"]]] += r["tax"] + r["prod_income"]
c_w = wealth**1.0  # placeholder; the wealth-field b is s_w - c_w per drain usage
# check which nodes have no counted provinces
empty = [ORDER[i] for i in range(N) if wealth[i] == 0.0]
print("nodes with zero counted wealth:", empty)
