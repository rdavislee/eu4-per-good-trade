# -*- coding: utf-8 -*-
"""spec 2.8 numeric rows: spices/cloves, the barbell, razed China, node wealth ranks,
and the alpha-calibration variant re-run under the SHIPPED tie-break cost."""
import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from drain import run_drain, sinks_of, phase0, phase1, phase2, sweep_priority, compile_dirs, has_cycle
from flowop import EDGES_UND, TIE_COST, mincost_flow, net_per_edge
from solver import N, ORDER, NIDX, UND, PROV, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
C = {}; S = {}; B = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    C[g] = n / n.sum(); S[g] = val[g] / val[g].sum(); B[g] = S[g] - C[g]
R = {g: run_drain(B[g]) for g in GL}
SK = {g: sorted(ORDER[i] for i in sinks_of(R[g]["directed"])[0]) for g in GL}
print("A. spices / cloves")
for g in ("spices", "cloves"):
    src = sorted(ORDER[i] for i in range(N) if S[g][i] > 0)
    rank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-C[g]))}
    print("  %-7s sources %-32s sinks %-40s demand ranks %s"
          % (g, src, SK[g], [(s, rank[s]) for s in SK[g]]))
print("  Australia/Venice/Deccan among either sink set:",
      [x for x in ("australia", "venice", "deccan") if x in SK["spices"] + SK["cloves"]])
print("  node names containing austral/venice/deccan:",
      [n for n in ORDER if any(k in n for k in ("austral", "venice", "deccan", "brazil", "kongo", "genua"))])
print()
print("B. barbell (2.8 'Most goods, 1444')")
top = bot = 0; ntop = nbot = 0
for g in GL:
    order = list(np.argsort(-C[g]))
    t8, b8 = order[:8], order[-8:]
    sk = {NIDX[s] for s in SK[g]}
    top += sum(1 for i in t8 if i in sk); ntop += 8
    bot += sum(1 for i in b8 if i in sk); nbot += 8
print("  top-8 demanders that are sinks   : %d of %d = %.1f%%" % (top, ntop, 100.0 * top / ntop))
print("  bottom-8 demanders that are sinks: %d of %d = %.1f%%" % (bot, nbot, 100.0 * bot / nbot))
scnt = [len(SK[g]) for g in GL]
print("  sinks per good min/max/mean      : %d / %d / %.2f" % (min(scnt), max(scnt), float(np.mean(scnt))))
print()
print("C. node wealth and razed China")
def bagg(w=None):
    w = W if w is None else w
    t = (w / w.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t)
    return np.full(N, 1.0 / N) - n / n.sum()
base = run_drain(bagg()); BD = set(base["directed"])
print("  baseline Phi_w sinks:", sorted(ORDER[i] for i in sinks_of(base["directed"])[0]))
holders = sorted({NIDX[r["node"]] for r in ROWS})
print("  nodes holding counted provinces:", len(holders))
rk = {ORDER[i]: k + 1 for k, i in enumerate(sorted(holders, key=lambda i: -NODEW[i]))}
for nm in ("hangzhou", "beijing"):
    print("  %-9s node wealth %.1f  rank %d of %d" % (nm, NODEW[NIDX[nm]], rk[nm], len(holders)))
ri = int(np.argmax(W))
print("  richest single province: pid %d node %s wealth %.2f" % (ROWS[ri]["pid"], ROWS[ri]["node"], W[ri]))
for nm in ("hangzhou", "beijing"):
    w2 = W.copy()
    for i, r in enumerate(ROWS):
        if r["node"] == nm: w2[i] = 0.0
    r2 = run_drain(bagg(w2)); d2 = set(r2["directed"])
    print("  zeroing %-9s -> sinks %-34s flips %d of %d"
          % (nm, sorted(ORDER[i] for i in sinks_of(r2["directed"])[0]), len(d2 ^ BD) // 2, len(EDGES_UND)))
print()
print("D. alpha-calibration (k_exp=2 unclamped, rho=0.5, tol=3e-4) under BOTH costs")
def phase1_q(core, beta, rho):
    dem = sorted([v for v in core if beta[v] < 0], key=lambda v: beta[v])
    D = sum(-beta[v] for v in dem)
    if not dem or D <= 0: return set()
    keep, acc = [], 0.0
    for v in dem:
        keep.append(v); acc += -beta[v]
        if acc >= rho * D: break
    ks = set(keep); comps = []; seen = set()
    for v in keep:
        if v in seen: continue
        comp = {v}; st = [v]; seen.add(v)
        while st:
            x = st.pop()
            for y in UND[x]:
                if y in ks and y not in comp: comp.add(y); seen.add(y); st.append(y)
        comps.append(sorted(comp))
    M = [sum(-beta[v] for v in c_) for c_ in comps]
    HHI = sum((m / sum(M)) ** 2 for m in M)
    k = int(min(max(round(1.0 / HHI), 1), len(comps)))
    out = set()
    for j in sorted(range(len(comps)), key=lambda j: -M[j])[:k]:
        out.add(min(comps[j], key=lambda v: (beta[v], v)))
    return out
TOL = 3e-4
for usetie in (False, True):
    res = {}
    for g in ("spices", "cloves"):
        a = (PRICES[g] / 2.0) ** 2
        t = (W / W.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t)
        c2 = n / n.sum(); b = S[g] - c2
        core, beta, Plog = phase0(b)
        Sset = phase1_q(core, beta, 0.5)
        f, du, r0 = mincost_flow(b, np.zeros(N), cost=(TIE_COST if usetie else None))
        net = net_per_edge(f)
        flow_arc = {}; free = []
        for ei, (u, v) in enumerate(EDGES_UND):
            if abs(net[ei]) > TOL: flow_arc[ei] = (u, v) if net[ei] > 0 else (v, u)
            else: free.append(ei)
        old = drain.ZERO_TOL; drain.ZERO_TOL = TOL
        o, S2, promo, fb = sweep_priority(core, beta, Sset, flow_arc, free, net, "defasc_beta")
        drain.ZERO_TOL = old
        d = compile_dirs(core, o, flow_arc, free, Plog, beta)
        sk, od = sinks_of(d)
        rank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-c2))}
        res[g] = (a, sorted(ORDER[i] for i in sk), [(ORDER[i], rank[ORDER[i]]) for i in sk])
    print("  cost=%-9s spices alpha=%.0f sinks %s | cloves alpha=%.0f sinks %s (ranks %s)"
          % ("TIE_COST" if usetie else "unit", res["spices"][0], res["spices"][1],
             res["cloves"][0], res["cloves"][1], res["cloves"][2]))
