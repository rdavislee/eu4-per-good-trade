# -*- coding: utf-8 -*-
import numpy as np, collections, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rankop import *

from rankop import (run, sinks_of, has_cycle, reach_path, rank_score, empty_set,
                    ALPHA, EPS, S0, C0, V, LIVE, GP, S_UNI, GOODS_LIVE, GIDX, DEG, E)
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc, solve_phi, orient, EXCLUDED
from scipy.stats import spearmanr

R = run()
OPS = ["LAP", "RANK"]
def dirs(g, op): return R[g]["lap_dir"] if op == "LAP" else R[g]["rank_dir"]

# vanilla out-degree, from the shipped file
VAN = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodes.json")))
van_out = np.array([len(VAN["nodes"][ORDER[i]]["outgoing"]) for i in range(N)])

# =============================================================== ITEM 1 ======
print("=" * 104); print("ITEM 1 - sink sets and demand correlation  [HEADLINE]"); print("=" * 104)
print("  Two sign conventions, both reported to avoid ambiguity:")
print("    rho_rank = spearman(demand RANK, sink indicator)   NEGATIVE = sinks are high-demand (good)")
print("    rho_val  = spearman(demand c,    sink indicator)   POSITIVE = sinks are high-demand (good)")
print()
print("  %-8s %8s %10s %12s %12s %11s %11s" %
      ("operator", "sinks/g", "mean rank", "P(sink|top10)", "P(sink|bot10)", "rho_rank", "rho_val"))
stash = {}
for op in OPS:
    ar, ai, av, per = [], [], [], []
    t10 = b10 = t10n = b10n = 0
    for g in GOODS_LIVE:
        gi = GIDX[g]; c = C0[gi]
        rank = np.empty(N, dtype=int); rank[np.argsort(-c)] = np.arange(1, N + 1)
        sk, od = sinks_of(dirs(g, op)); ss = set(sk); per.append(len(sk))
        for i in range(N):
            ar.append(rank[i]); av.append(c[i]); ai.append(1 if i in ss else 0)
            if rank[i] <= 10: t10n += 1; t10 += (i in ss)
            if rank[i] > N - 10: b10n += 1; b10 += (i in ss)
    ar = np.array(ar); ai = np.array(ai); av = np.array(av)
    rr = spearmanr(ar, ai).statistic; rv = spearmanr(av, ai).statistic
    stash[op] = (np.mean(per), ar[ai == 1].mean(), 100*t10/t10n, 100*b10/b10n, rr, rv)
    print("  %-8s %8.1f %10.1f %11.1f%% %11.1f%% %11.3f %11.3f"
          % (op, *stash[op][:4], rr, rv))
print("  (all-node mean rank is 40.5)")
print()
print("  For reference, from flow-orientation.md: FLOW rho_rank = +0.132 (anti-correlated),")
print("  TREE rho_rank = +0.040 / -0.048 / -0.085.")
print()

# =============================================================== ITEM 7 ======
print("=" * 104); print("ITEM 7 - sinks per good; goods keeping more than one"); print("=" * 104)
print("  %-8s %6s %6s %16s %8s" % ("operator", "min", "max", "goods with >1", "mean"))
for op in OPS:
    cnt = [len(sinks_of(dirs(g, op))[0]) for g in GOODS_LIVE]
    print("  %-8s %6d %6d %15d/%d %8.1f" % (op, min(cnt), max(cnt), sum(1 for x in cnt if x > 1), len(cnt), np.mean(cnt)))
print()
for op in OPS:
    fr = collections.Counter()
    for g in GOODS_LIVE:
        for i in sinks_of(dirs(g, op))[0]: fr[ORDER[i]] += 1
    print("  %-5s most frequent sinks: %s" % (op, fr.most_common(10)))
print()

# =============================================================== ITEM 2 ======
print("=" * 104); print("ITEM 2 - cloves and spices at the named nodes, with demand rank"); print("=" * 104)
for g in ("spices", "cloves"):
    gi = GIDX[g]; c = C0[gi]
    rank = np.empty(N, dtype=int); rank[np.argsort(-c)] = np.arange(1, N + 1)
    print("  --- %s (alpha=%.2f) ---" % (g, ALPHA(g)))
    print("    %-10s %10s %6s %6s %12s | %-8s %-8s" % ("node","c","rank","s>0","score","LAP","RANK"))
    for nm in ("genua","venice","beijing","canton","saxony","safi","english_channel","hangzhou"):
        i = NIDX[nm]
        cells = ["SINK" if i in set(sinks_of(dirs(g,op))[0]) else "-" for op in OPS]
        print("    %-10s %10.5f %6d %6s %12.6f | %-8s %-8s"
              % (nm, c[i], rank[i], "yes" if S0[gi][i]>0 else "no", R[g]["score"][i], cells[0], cells[1]))
print()

# =============================================================== ITEM 8 ======
print("=" * 104); print("ITEM 8 - out-degree against demand rank (aggregated over goods)"); print("=" * 104)
print("  Nodes binned by demand rank (using the value-weighted mean demand across goods).")
cbar = np.zeros(N)
for g in GOODS_LIVE: cbar += V[GIDX[g]] * C0[GIDX[g]]
cbar /= sum(V[GIDX[g]] for g in GOODS_LIVE)
order_by_c = np.argsort(-cbar)
bins = [(0,8),(8,16),(16,24),(24,40),(40,56),(56,72),(72,80)]
print("  %-14s %8s | %10s %10s %10s" % ("demand-rank bin","nodes","VANILLA","LAP","RANK"))
for a,b in bins:
    sel = order_by_c[a:b]
    vo = van_out[sel].mean()
    lo = np.mean([np.mean([collections.Counter(u for u,_ in dirs(g,"LAP"))[i] for g in GOODS_LIVE]) for i in sel])
    ro = np.mean([np.mean([collections.Counter(u for u,_ in dirs(g,"RANK"))[i] for g in GOODS_LIVE]) for i in sel])
    print("  %-14s %8d | %10.2f %10.2f %10.2f" % ("%d-%d"%(a+1,b), len(sel), vo, lo, ro))
print()
for nm,arr in (("VANILLA",van_out),):
    print("  spearman(demand rank, %s out-degree) = %.3f" % (nm, spearmanr(np.argsort(np.argsort(-cbar)), arr).statistic))
for op in OPS:
    od = np.array([np.mean([collections.Counter(u for u,_ in dirs(g,op))[i] for g in GOODS_LIVE]) for i in range(N)])
    print("  spearman(demand rank, %-4s out-degree) = %.3f  (positive = rich nodes have FEW outgoing)"
          % (op, spearmanr(np.argsort(np.argsort(-cbar)), od).statistic))
print()

# =============================================================== ITEM 5 ======
print("=" * 104); print("ITEM 5 - acyclicity"); print("=" * 104)
for op in OPS:
    bad = [g for g in GOODS_LIVE if has_cycle(dirs(g, op)) is not None]
    print("  %-6s non-acyclic goods: %d/%d %s" % (op, len(bad), len(GOODS_LIVE), bad[:4]))
Phi_r = np.zeros(N); Phi_l = np.zeros(N)
for g in GOODS_LIVE:
    Phi_r += V[GIDX[g]] * R[g]["score"]; Phi_l += V[GIDX[g]] * R[g]["lap_phi"]
print("  Phi(LAP)  acyclic: %s" % (has_cycle(orient(Phi_l)) is None))
print("  Phi(RANK) acyclic: %s" % (has_cycle(orient(Phi_r)) is None))
print("  (RANK orientation is by a per-node scalar, so acyclicity is guaranteed by the same")
print("   argument as for phi: score strictly decreases along any directed path.)")
print()
tie = 0
for g in GOODS_LIVE:
    sc = R[g]["score"]
    for (u,v) in EDGES_UND:
        if sc[u] == sc[v]: tie += 1
print("  exact score ties over %d edge-good pairs: %d (unoriented edges)" % (len(GOODS_LIVE)*E, tie))
print()

# =============================================================== ITEM 6 ======
print("=" * 104); print("ITEM 6 - Phi = phi0 residual at alpha = 1"); print("=" * 104)
S1, C1, V1, L1, gp1, w1 = build_sc(lambda g: 1.0, eps=0.0)
tv = np.zeros(N)
for r in ROWS:
    if r["good"] in EXCLUDED or r["good"] not in PRICES: continue
    tv[NIDX[r["node"]]] += r["gp"] * PRICES[r["good"]]
s0 = tv / tv.sum()
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
c0 = np.zeros(N); np.add.at(c0, pn, wealth / wealth.sum())
phi0_lap = solve_phi(s0 - c0)
score0 = s0 - c0
PhiR1 = np.zeros(N)
for g in GOODS_LIVE:
    gi = GIDX[g]
    sc, _, _, _ = rank_score(gi)          # structure only; recompute at alpha=1 below
for g in GOODS_LIVE:
    pass
# rebuild RANK scores at alpha = 1
PhiR1 = np.zeros(N); tot = 0.0
for g in GOODS_LIVE:
    gi = GIDX[g]
    sc = S1[gi] - C1[gi]
    emp = [i for i in range(N) if S1[gi][i] == 0 and C1[gi][i] == 0]
    for i in emp:                          # single-node harmonic extension
        sc[i] = np.mean([sc[j] for j in UND[i]])
    PhiR1 += V1[gi] * sc; tot += V1[gi]
for nm, target in (("spec phi0 (Laplacian solve of s0-c0)", phi0_lap),
                   ("ranked analogue score0 = s0 - c0", score0)):
    mask = np.abs(target) > 1e-14
    k = (PhiR1[mask] / target[mask]).mean()
    res = np.abs(PhiR1 - k * target).max() / max(np.abs(PhiR1).max(), 1e-300)
    ag = len(set(orient(PhiR1)) & set(orient(target)))
    print("  Phi(RANK,a=1) vs %-38s k=%12.4f rel.residual=%.3e orient agree %d/%d"
          % (nm, k, res, ag, E))
print("  sum_g V_g = %.6f ; world trade value = %.6f" % (tot, tv.sum()))
print()
