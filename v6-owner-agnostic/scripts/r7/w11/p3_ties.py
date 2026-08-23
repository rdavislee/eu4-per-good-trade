# -*- coding: utf-8 -*-
"""Y148 tie census, Y464/Y566 sink-set equality, Y442/Y560/Y561 conservation."""
import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import drain
from drain import phase0, phase1, phase2, flow_def, run_drain, sinks_of
from flowop import EDGES_UND, ZERO_TOL
from solver import N, ORDER, NIDX, UND, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
B = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    B[g] = val[g] / val[g].sum() - n / n.sum()
t = (W / W.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t)
B["__AGG__"] = np.full(N, 1.0 / N) - n / n.sum()

tot_free_ties = tot_clu_ties = tot_mass_ties = 0
eq_ok = 0; contain_ok = 0; fb_total = 0; sumb = []
peeled = 0
for k in list(B):
    b = B[k]
    sumb.append(abs(float(b.sum())))
    core, beta, Plog = phase0(b)
    peeled += len(Plog)
    S, info = phase1(core, beta)
    flow_arc, free, net, cost = phase2(core, beta)
    DEF = flow_def(core, beta, flow_arc)
    # free-edge sweep key is (DEF asc, beta asc, index) -- count exact (DEF,beta) ties
    # among nodes that ever compete, i.e. endpoints of free edges
    ends = set()
    for ei in free:
        u, v = EDGES_UND[ei]; ends.add(u); ends.add(v)
    keys = collections.Counter((round(DEF[x], 17), round(beta[x], 17)) for x in ends)
    ft = sum(c - 1 for c in keys.values() if c > 1)
    tot_free_ties += ft
    # Phase 1 within-cluster argmin ties: min by (beta, v) inside each demander component
    coreset = set(core); Dset = [v for v in core if beta[v] < 0]; ds = set(Dset)
    comps = []; seen = set()
    for v in Dset:
        if v in seen: continue
        comp = {v}; st = [v]; seen.add(v)
        while st:
            x = st.pop()
            for y in UND[x]:
                if y in ds and y not in comp: comp.add(y); seen.add(y); st.append(y)
        comps.append(sorted(comp))
    ct = 0
    for c in comps:
        mn = min(beta[x] for x in c)
        ct += sum(1 for x in c if beta[x] == mn) - 1
    tot_clu_ties += ct
    M = [sum(-beta[v] for v in c) for c in comps]
    mt = len(M) - len(set(M))
    tot_mass_ties += mt
    # sink-set equality
    r = run_drain(b)
    sk, od = sinks_of(r["directed"])
    inflow = collections.defaultdict(float)
    for ei, (u, v) in flow_arc.items(): inflow[v] += abs(net[ei])
    outs = collections.defaultdict(list)
    for ei, (u, v) in flow_arc.items(): outs[u].append(v)
    flowterm = {v for v in core if len(outs[v]) == 0 and inflow[v] > ZERO_TOL}
    eq = (set(S) & flowterm) | set(r["promotions"])
    contain = set(r["S"]) | set(r["promotions"]) | set(r["fallbacks"])
    eq_ok += (set(sk) == eq)
    contain_ok += set(sk) <= contain
    fb_total += len(r["fallbacks"])
    if set(sk) != eq:
        print("  equality miss on %-10s sinks=%s eq=%s" % (k, sorted(ORDER[i] for i in sk),
                                                          sorted(ORDER[i] for i in eq)))
print("b-vectors tested (29 goods + aggregate) :", len(B))
print("max |sum b|                             : %.3e" % max(sumb))
print("Phase-0 peels across all b-vectors      :", peeled)
print("exact (DEF, beta) ties on free-edge ends:", tot_free_ties)
print("Phase-1 within-cluster beta ties        :", tot_clu_ties)
print("tied cluster masses                     :", tot_mass_ties)
print("sink-set EQUALITY holds                 : %d of %d" % (eq_ok, len(B)))
print("sink-set CONTAINMENT holds              : %d of %d" % (contain_ok, len(B)))
print("fallbacks fired                         :", fb_total)
