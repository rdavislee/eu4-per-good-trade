# -*- coding: utf-8 -*-
"""V145/V146 price-event scan; V115/V189 rank genua-cloves; V191 basin best reach."""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx
import numpy as np

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"

# ---------------- V145/V146: change_price effects across events/ (and everywhere) ----
prices = {}
for k, v in pdx.load(os.path.join(EU4, "common", "prices", "00_prices.txt")):
    if isinstance(v, pdx.Node):
        prices[k] = float(v.get("base_price", 0.0))
goods = [g for g in prices if g not in ("gold",)]   # 31 incl unknown; count both ways

def walk(node, hits, src):
    for k, v in node:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                tg = v.get("trade_goods"); val = v.get("value")
                if tg is not None and val is not None:
                    hits.append((tg, float(val), src))
            walk(v, hits, src)

hits = []
scopes = {"events": os.path.join(EU4, "events"),
          "decisions": os.path.join(EU4, "decisions"),
          "missions": os.path.join(EU4, "missions"),
          "common": os.path.join(EU4, "common")}
for tag, root in scopes.items():
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            if fn.endswith(".txt"):
                p = os.path.join(dirpath, fn)
                try:
                    walk(pdx.load(p), hits, tag + "/" + fn)
                except Exception as e:
                    print("PARSEFAIL", fn, e)

print("change_price effects found in events/: %d" % len(hits))
neg = collections.defaultdict(list)
for tg, val, src in hits:
    if val < 0: neg[tg].append(val)
below = []
nonneg = []
for g in sorted(prices):
    if g == "gold": continue
    base = prices[g]
    if base == 0.0: continue   # unknown
    worst = min(neg[g]) if g in neg else None
    if worst is None:
        nonneg.append(g)
    else:
        floor1 = base * (1 + worst)
        if floor1 < 2.0: below.append((g, base, worst, round(floor1, 4)))
print("goods total (base_price>0):", sum(1 for g in prices if g != 'gold' and prices[g] > 0))
print("V145 goods pushable below 2.0 by a single event: %d" % len(below))
for g, b, w, f in sorted(below, key=lambda x: x[3]): print("   %-14s base=%.1f worst=%.2f -> %.4g" % (g, b, w, f))
print("V146 goods with NO negative price event: %d %s" % (len(nonneg), nonneg))

# ---------------- V115/V189: RANK operator, genua cloves sink unreachable --------
print()
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, build_sc, orient
from rankop import rank_score, GIDX
ALPHA = lambda g: max(0.2, min(3.0, (prices[g] / 2.0) ** 1.0))
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
gi = GOODS.index("cloves")
sc, emp, regions, wp = rank_score(GIDX["cloves"])
d = orient(sc)
od = collections.Counter(u for u, _ in d)
sinks = [ORDER[i] for i in range(N) if od[i] == 0]
srcs = [i for i in range(N) if GP[gi][i] > 0]
a = collections.defaultdict(list)
for u, v in d: a[u].append(v)
seen = set(srcs); q = collections.deque(srcs)
while q:
    x = q.popleft()
    for y in a[x]:
        if y not in seen: seen.add(y); q.append(y)
print("V115/V189 RANK cloves: genua a sink: %s | genua reachable from cloves sources: %s"
      % ("genua" in sinks, NIDX["genua"] in seen))
print("          cloves sources: %s | sinks: %s" % ([ORDER[i] for i in srcs], sinks[:8]))

# ---------------- V191: BASIN best tuning (gamma=1000) mean demand reach ---------
print()
from basin import phase0 as b_p0, phase1 as b_p1, phase2 as b_p2, phase3 as b_p3, phase4 as b_p4, P as BP
from solver import solve_phi
S_UNI, _, _, _, _, _ = build_sc(ALPHA, eps=1e-6)
GL = [g for gg, g in enumerate(GOODS) if LIVE[gg]]
GI = {g: GOODS.index(g) for g in GL}
lapS = {}
for g in GL:
    dd = orient(solve_phi(S_UNI[GI[g]] - C0m[GI[g]]))
    odc = collections.Counter(u for u, _ in dd)
    lapS[g] = sum(1 for i in range(N) if odc[i] == 0)

def basin_best_dir(b, S, K, sign, gamma):
    core, btil, pend, drains, pe = b_p0(b, UND)
    T, _ = b_p1(core, btil, UND, max(S, 1), BP["lam"], BP["R"])
    mu = {t: 1.0 for t in T}; scale = sum(max(0.0, -btil[v]) for v in core) or 1.0
    best = None; bestd = None
    for it in range(K):
        phi, basin, bal, tier, parent, SEED = b_p2(core, btil, UND, T, drains, mu, gamma,
                                                   BP["kplus"], BP["kminus"], BP["gmin"], BP["gmax"])
        d2, key = b_p3(core, phi, tier, pe, UND)
        un, st = b_p4(core, btil, d2, key)
        if best is None or un < best - 1e-15: best, bestd = un, d2
        for t in mu: mu[t] = mu[t] * np.exp(sign * BP["eta"] * bal[t] / scale)
    return bestd

reaches = []
for g in GL:
    gg = GI[g]
    d3 = basin_best_dir(S0m[gg] - C0m[gg], lapS[g], 8, +1.0, 1000.0)
    a = collections.defaultdict(list)
    for u, v in d3: a[u].append(v)
    srcs = [i for i in range(N) if GP[gg][i] > 0]
    seen = set(srcs); q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in a[x]:
            if y not in seen: seen.add(y); q.append(y)
    c = C0m[gg]
    reaches.append(c[list(seen)].sum() / c.sum())
print("V191 BASIN gamma=1000 mean demand reach: %.1f%% | goods at 100%%: %d/29"
      % (100 * np.mean(reaches), sum(1 for r in reaches if r >= 1.0 - 1e-12)))
