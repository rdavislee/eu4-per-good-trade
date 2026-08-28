# -*- coding: utf-8 -*-
"""v3measure.py - regenerate EVERY number spec v3.0 quotes, from the install.

Wealth is owner-agnostic and ANNUAL:
    goods_produced(p) = GP_COEFF * base_production(p)      GP_COEFF = 0.2
    trade_value(p)    = goods_produced(p) * price(good(p))
    tax_value(p)      = TAX_COEFF * base_tax(p)            TAX_COEFF = 1.0
    wealth(p)         = tax_value(p) + trade_value(p)
Both coefficients measured in-game 2026-08-20 from Garnatah (pid 223, base_tax 6,
base_production 4, silk, local_autonomy 0): tax tooltip "Base: 0.49 (Yearly 6.00)";
goods tooltip "Base Goods Produced: 0.80 / Base Production: +0.80"; window Trade
Value 3.20 = 0.80 x 4.00. Neither coefficient is a define (searched defines.lua).
"""
import numpy as np, collections, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.stats import spearmanr
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, PROV, PNODE,
                    ROWS, EXCLUDED, build_sc, solve_phi, orient, COMPS, NODES)
import drain
from drain import run_drain, sinks_of, has_cycle, sweep_priority, phase0, phase1, phase2, compile_dirs, flow_def
from flowop import mincost_flow, net_per_edge, ZERO_TOL

TAG = "v4measure.py"
def P(label, value):
    print("%-58s %s   [%s]" % (label, value, TAG))

E = len(EDGES_UND)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

print("=" * 100); print("A. WEALTH MODEL (owner-agnostic, annual ducats)"); print("=" * 100)
P("provinces contributing (owned, is_city)", len(ROWS))
P("live goods", len(GL))
P("world wealth total (annual ducats)", "%.1f" % wealth.sum())
P("richest single province", "pid=%s node=%s w=%.2f" % (
    ROWS[int(np.argmax(wealth))]["pid"], ROWS[int(np.argmax(wealth))]["node"], wealth.max()))
NODEW = np.zeros(N); np.add.at(NODEW, pn, wealth)
P("node wealth range", "%.1f (%s) .. %.1f (%s)" % (
    NODEW.min(), ORDER[int(np.argmin(NODEW))], NODEW.max(), ORDER[int(np.argmax(NODEW))]))

print(); print("=" * 100); print("B. GRAPH / MAP FACTS"); print("=" * 100)
P("nodes", N); P("undirected edges", E); P("arcs presented to the LP", 2 * E)
deg = [len(UND[i]) for i in range(N)]
P("minimum node degree", min(deg))
P("connected components", len(COMPS))
ends = [n for n in ORDER if NODES[n]["end"] == "yes"]
P("vanilla end=yes nodes", "%d %s" % (len(ends), ends))
viol = sum(1 for n in ORDER for m in NODES[n]["outgoing"] if ORDER.index(n) > ORDER.index(m))
P("declaration-order violations in vanilla file", "%d of %d" % (viol, E))

print(); print("=" * 100); print("C. PER-GOOD DRAIN (spec defaults)"); print("=" * 100)
t0 = time.time(); R = {}
for gi, g in GL: R[g] = run_drain(S0m[gi] - C0m[gi])
t1 = time.time()
P("wall time, 29 goods (scipy HiGHS + sweep)", "%.2f s (%.1f ms/good)" % (t1-t0, 1000*(t1-t0)/len(GL)))
acyc = sum(1 for _, g in GL if has_cycle(R[g]["directed"]) is None)
P("acyclic goods", "%d/%d" % (acyc, len(GL)))
sc = [len(sinks_of(R[g]["directed"])[0]) for _, g in GL]
P("sinks per good", "min %d max %d mean %.1f" % (min(sc), max(sc), np.mean(sc)))
P("k values", dict(collections.Counter(R[g]["info"]["k"] for _, g in GL)))
P("fallback promotions (outside the stall lemma)", sum(len(R[g]["fallbacks"]) for _, g in GL))
supp = [len(R[g]["flow_arc"]) for _, g in GL]
P("flow support size", "min %d max %d (N-1 = %d)" % (min(supp), max(supp), N-1))

def reach_share(d, gi, c):
    a = collections.defaultdict(list)
    for u, v in d: a[u].append(v)
    srcs = [i for i in range(N) if GP[gi][i] > 0]
    seen = set(srcs); q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in a[x]:
            if y not in seen: seen.add(y); q.append(y)
    return c[list(seen)].sum() / c.sum(), seen
rok = 0; orph = 0
for gi, g in GL:
    rs, seen = reach_share(R[g]["directed"], gi, C0m[gi])
    if rs >= 1 - 1e-12: rok += 1
    orph += sum(1 for s in sinks_of(R[g]["directed"])[0] if s not in seen and C0m[gi][s] > 0)
P("goods at 100.0% demand reach", "%d/%d" % (rok, len(GL)))
P("orphan sinks", orph)

zero_b = [ORDER[i] for i in range(N) if all((S0m[gi][i]-C0m[gi][i]) == 0.0 for gi, _ in GL)]
P("nodes with b == 0 for every good", zero_b)
cape = NIDX["cape_of_good_hope"]
cond = sum(1 for _, g in GL
           if any(v == cape for u, v in R[g]["directed"]) and any(u == cape for u, v in R[g]["directed"]))
P("cape is a conduit (in>0 and out>0)", "%d/%d goods" % (cond, len(GL)))

# determinism / scan invariance
rng = np.random.default_rng(7); flips = 0; ties = 0
for gi, g in GL:
    b = S0m[gi] - C0m[gi]
    core, beta, Plog = phase0(b); S, info = phase1(core, beta, 0)
    fa, free, net, cost = phase2(core, beta)
    o1, _, _, _ = sweep_priority(core, beta, S, fa, free, net, "defasc_beta")
    d1 = set(compile_dirs(core, o1, fa, free, Plog, beta))
    for _ in range(2):
        pid = {v: int(x) for v, x in zip(range(N), rng.permutation(N))}
        o2, _, _, _ = sweep_priority(core, beta, S, fa, free, net, "defasc_beta", pid=pid)
        flips += len(d1 ^ set(compile_dirs(core, o2, fa, free, Plog, beta))) // 2
    DEF = flow_def(core, beta, fa)
    for ei in free:
        u, v = EDGES_UND[ei]
        if DEF[u] == DEF[v] and beta[u] == beta[v]: ties += 1
P("orientation flips, 2 index permutations x 29 goods", flips)
P("exact (DEF, b) ties on free edges", ties)
base = None; det = True
for _ in range(6):
    k = tuple(sorted(run_drain(S0m[GOODS.index('spices')] - C0m[GOODS.index('spices')])["directed"]))
    if base is None: base = k
    elif k != base: det = False
P("six identical LP solves -> one orientation", det)

print(); print("=" * 100); print("D. Phi_w  (wealth good, alpha_Phi = 1.5)"); print("=" * 100)
def c_w_of(a, w=None):
    w = wealth if w is None else w
    t = (w / w.max()) ** a
    num = np.zeros(N); np.add.at(num, pn, t)
    return num / num.sum()
def phi_w(a=1.5, w=None):
    return run_drain(np.full(N, 1.0/N) - c_w_of(a, w))
rw = phi_w(1.5); dw = rw["directed"]; dws = set(dw)
od = collections.Counter(u for u, _ in dw); idg = collections.Counter(v for _, v in dw)
sinks_w = [ORDER[i] for i in range(N) if od[i] == 0]
srcs_w = [ORDER[i] for i in range(N) if idg[i] == 0]
cr = {ORDER[i]: k+1 for k, i in enumerate(np.argsort(-c_w_of(1.5)))}
wr = {ORDER[i]: k+1 for k, i in enumerate(np.argsort(-NODEW))}
P("Phi_w sinks", "%s (c_w ranks %s | node-wealth ranks %s)" % (
    sinks_w, [cr[s] for s in sinks_w], [wr[s] for s in sinks_w]))
P("Phi_w Phase-1 selection", sorted(ORDER[i] for i in rw["S0"]))
P("Phi_w promotions / fallbacks", "%s / %s" % (
    sorted(ORDER[i] for i in rw["promotions"]), sorted(ORDER[i] for i in rw["fallbacks"])))
P("Phi_w sources (indeg 0)", "%d %s" % (len(srcs_w), srcs_w))
P("Phi_w acyclic / edges oriented", "%s / %d of %d" % (has_cycle(dw) is None, len(dw), E))
o = rw["order"]
P("order-descending violations", sum(1 for u, v in EDGES_UND
    if ((u, v) if o[u] > o[v] else (v, u)) not in dws))
ag = tot = 0; wag = wtot = 0.0
PGd = {g: set(R[g]["directed"]) for _, g in GL}
for gi, g in GL:
    for u, v in EDGES_UND:
        gd = (u, v) if (u, v) in PGd[g] else ((v, u) if (v, u) in PGd[g] else None)
        if gd is None: continue
        tot += 1; wtot += V[gi]
        if ((u, v) if (u, v) in dws else (v, u)) == gd: ag += 1; wag += V[gi]
P("Phi_w agreement with per-good graphs", "%d/%d = %.1f%% (value-weighted %.1f%%)"
  % (ag, tot, 100*ag/tot, 100*wag/wtot))
Pord = np.zeros(N)
for gi, g in GL:
    for i in range(N): Pord[i] += V[gi] * R[g]["order"][i]
oa = ot = 0
for gi, g in GL:
    for u, v in EDGES_UND:
        gd = (u, v) if (u, v) in PGd[g] else ((v, u) if (v, u) in PGd[g] else None)
        if gd is None: continue
        ot += 1
        if ((u, v) if Pord[u] > Pord[v] else (v, u)) == gd: oa += 1
P("Phi_ord agreement (deterministic sweep)", "%d/%d = %.1f%%" % (oa, ot, 100*oa/ot))
ocnt = collections.Counter()
for u, v in EDGES_UND: ocnt[(u if Pord[u] > Pord[v] else v)] += 1
eo = [ORDER[i] for i in range(N) if ocnt[i] == 0]
P("Phi_ord end nodes", len(eo))
nog = [n for n in eo if sum(1 for _, g in GL if not any(u == NIDX[n] for u, _ in PGd[g])) == 0]
P("  Phi_ord ends that terminate NO good", "%d %s" % (len(nog), sorted(nog)))
flips_n = 0; skch = 0
for seed in range(5):
    r2 = np.random.default_rng(1000+seed)
    w2 = wealth * (1 + r2.uniform(-0.01, 0.01, size=len(wealth)))
    rr = phi_w(1.5, w2); d2 = set(rr["directed"])
    flips_n += len(dws ^ d2) // 2
    od2 = collections.Counter(u for u, _ in rr["directed"])
    skch += (frozenset(ORDER[i] for i in range(N) if od2[i] == 0) != frozenset(sinks_w))
P("Phi_w edge flips under +/-1% wealth noise, 5 seeds", flips_n)
P("Phi_w sink-set changes under that noise", "%d/5" % skch)
seq = []
for a in (1, 1.5, 2, 3, 4, 8):
    ra = phi_w(float(a)); oda = collections.Counter(u for u, _ in ra["directed"])
    seq.append(sum(1 for i in range(N) if oda[i] == 0))
P("Phi_w sink count at alpha_Phi in {1,1.5,2,3,4,8}", seq)

print(); print("=" * 100); print("E. CROSS-CHECKS THE SPEC QUOTES"); print("=" * 100)
conn = np.zeros((N, N), dtype=bool)
for gi, g in GL:
    a = collections.defaultdict(list)
    for u, v in R[g]["directed"]: a[u].append(v)
    for s in range(N):
        seen = {s}; q = collections.deque([s])
        while q:
            x = q.popleft()
            for y in a[x]:
                if y not in seen: seen.add(y); q.append(y)
        for t in seen:
            if t != s: conn[s][t] = True
P("ordered node pairs connected by >=1 good", "%d/%d = %.1f%%" % (conn.sum(), N*(N-1), 100*conn.sum()/(N*(N-1))))
gi_s = GOODS.index("spices")
s_u, _, _, _, _, _ = build_sc(ALPHA, eps=1e-6)
P("spices supply contrast (eps-floored max/min)", "%.3g" % (s_u[gi_s].max()/s_u[gi_s].min()))
P("spices demand contrast (max/min over c>0)", "%.1f" % (C0m[gi_s].max()/C0m[gi_s][C0m[gi_s] > 0].min()))
land = {n: sum(1 for p in NODES[n]["members"]) for n in ORDER}
P("cape/girin/nippon/champagne member counts", {k: land[k] for k in
   ("cape_of_good_hope", "girin", "nippon", "champagne")})
print()
print("NOTE: node member counts above are RAW members; land-only counts are in graphchk.py")
