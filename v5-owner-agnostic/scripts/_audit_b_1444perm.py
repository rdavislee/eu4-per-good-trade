# -*- coding: utf-8 -*-
"""End-to-end node-relabelling test on the real 1444 map (all 29 goods + Phi_w).
Unlike v5measure.py's `pid` permutation -- which only re-keys sweep_priority -- this
permutes the node indexing through EVERY phase, so it also exercises Phase 1's
within-cluster (beta, index) tiebreak and the stall promotion's (beta, index) tiebreak."""
import sys, random, collections, itertools
import numpy as np
sys.path.insert(0, "C:/Users/rdavi/OneDrive/Documents/Paradox Interactive/Europa Universalis IV/mod/per-good-trade/v5-owner-agnostic/scripts")
from _audit_b_drain import drain
from solver import N, ORDER, GOODS, PRICES, build_sc, EDGES_UND, NIDX
from drain import run_drain, NODEW

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
NAMES = list(map(str, range(N)))
EDGES = [tuple(e) for e in EDGES_UND]

# ---- 0. sanity: does the independent implementation match drain.py on 1444?
mism = 0
for gi, g in enumerate(GOODS):
    if not LIVE[gi]: continue
    b = S[gi] - C[gi]
    a = set(run_drain(b)["directed"])
    c = set(drain(NAMES, EDGES, list(b), wealth=list(NODEW))["directed"])
    if a != c: mism += 1
print("sanity: goods where the independent impl disagrees with drain.py:", mism, "/29")

def relabel(edges, b, w, p):
    e2 = sorted(tuple(sorted((p[u], p[v]))) for u, v in edges)
    b2 = [0.]*N; w2 = [0.]*N
    for i in range(N): b2[p[i]] = b[i]; w2[p[i]] = w[i]
    return e2, b2, w2

def phase1_tie_report(b):
    """count exact within-cluster beta ties at the argmin, and tied cluster masses"""
    from solver import UND
    beta = np.asarray(b, float)
    D = [v for v in range(N) if beta[v] < 0]
    ds = set(D); comps = []; seen = set()
    for v in D:
        if v in seen: continue
        comp = {v}; st = [v]; seen.add(v)
        while st:
            x = st.pop()
            for y in UND[x]:
                if y in ds and y not in comp: comp.add(y); seen.add(y); st.append(y)
        comps.append(sorted(comp))
    M = [sum(-beta[v] for v in c) for c in comps]
    tot = sum(M); HHI = sum((m/tot)**2 for m in M)
    k = int(min(max(round(1.0/HHI), 1), len(comps)))
    top = sorted(range(len(comps)), key=lambda j: -M[j])[:k]
    argmin_ties = 0
    for j in top:
        mn = min(beta[v] for v in comps[j])
        if sum(1 for v in comps[j] if beta[v] == mn) > 1: argmin_ties += 1
    mass_tie = (len(set(M)) != len(M))
    return argmin_ties, mass_tie, k, len(comps)

PERMS = 20
rng = random.Random(4242)
tot_changed = tot_same_sup = tot_diff_sup = 0
p1_tie_goods = []; mass_tie_goods = []
for gi, g in enumerate(GOODS):
    if not LIVE[gi]: continue
    b = list(S[gi] - C[gi])
    at, mt, k, nc = phase1_tie_report(b)
    if at: p1_tie_goods.append((g, at))
    if mt: mass_tie_goods.append((g, k, nc))
    r = drain(NAMES, EDGES, b, wealth=list(NODEW))
    base = set(r["directed"]); basesup = set(r["flow_arc"].values())
    for t in range(PERMS):
        p = list(range(N)); rng.shuffle(p)
        e2, b2, w2 = relabel(EDGES, b, list(NODEW), p)
        r2 = drain(NAMES, e2, b2, wealth=w2)
        inv = {p[i]: i for i in range(N)}
        back = set((inv[u], inv[v]) for u, v in r2["directed"])
        sup2 = set((inv[u], inv[v]) for u, v in r2["flow_arc"].values())
        if back != base:
            tot_changed += 1
            if sup2 == basesup: tot_same_sup += 1
            else: tot_diff_sup += 1
print()
print("1444, 29 goods x %d full node relabellings = %d runs" % (PERMS, 29*PERMS))
print("  orientation changed            :", tot_changed)
print("     ...with the SAME LP support :", tot_same_sup, " (the sweep's index tiebreaks)")
print("     ...with a DIFFERENT support :", tot_diff_sup, " (LP vertex choice)")
print("  goods with an exact within-cluster beta tie at a Phase-1 argmin:", p1_tie_goods)
print("  goods with tied cluster masses at the top-k cut:", mass_tie_goods)

# Phi_w as well
pn = np.array([NIDX[r_["node"]] for r_ in __import__("solver").ROWS])
wealth = np.array([r_["tax"] + r_["prod_income"] for r_ in __import__("solver").ROWS])
t = (wealth/wealth.max())**1.5; num = np.zeros(N); np.add.at(num, pn, t)
bw = list(np.full(N, 1.0/N) - num/num.sum())
at, mt, k, nc = phase1_tie_report(bw)
r = drain(NAMES, EDGES, bw, wealth=list(NODEW)); base = set(r["directed"]); basesup = set(r["flow_arc"].values())
ch = same = 0
for t_ in range(PERMS):
    p = list(range(N)); rng.shuffle(p)
    e2, b2, w2 = relabel(EDGES, bw, list(NODEW), p)
    r2 = drain(NAMES, e2, b2, wealth=w2)
    inv = {p[i]: i for i in range(N)}
    if set((inv[u], inv[v]) for u, v in r2["directed"]) != base:
        ch += 1
        if set((inv[u], inv[v]) for u, v in r2["flow_arc"].values()) == basesup: same += 1
print("  Phi_w: %d/%d relabellings changed the orientation (same-support: %d); phase1 argmin ties=%d mass tie=%s"
      % (ch, PERMS, same, at, mt))
