# coordinator recheck of Y1035: self-coherence, first-order-only cost vs shipped full cost.
# Reproduces measure6.py's exact coherence construction in both worlds.
import os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc, EDGES_UND
from drain import run_drain, has_cycle

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = np.zeros(N); np.add.at(t, pn, (W / W.max()) ** 2.0)
b_agg = np.full(N, 1.0 / N) - t / t.sum()

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for _, g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]

def world(cost):
    drain.TIE_COST = cost
    base = run_drain(b_agg); BD = set(base["directed"])
    PG = {}; V = {}
    sc = []
    acyc = 0
    for gi, g in GL:
        tt = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, tt)
        S = val[g] / val[g].sum() if val[g].sum() > 0 else np.zeros(N)
        r = run_drain(S - n / n.sum())
        PG[g] = set(r["directed"]); V[g] = float(val[g].sum())
        outn = {u for (u, v) in PG[g]}; inn = {v for (u, v) in PG[g]}
        sc.append(len(inn - outn))
        if has_cycle(r["directed"]) is None: acyc += 1
    ag = tot = 0; wag = wtot = 0.0
    for _, g in GL:
        for u, v in EDGES_UND:
            gd = (u, v) if (u, v) in PG[g] else ((v, u) if (v, u) in PG[g] else None)
            if gd is None: continue
            tot += 1; wtot += V[g]
            if ((u, v) if (u, v) in BD else (v, u)) == gd: ag += 1; wag += V[g]
    outb = {u for (u, v) in BD}; innb = {v for (u, v) in BD}
    return dict(coh_edge=100.0 * ag / tot, coh_val=100.0 * wag / wtot,
                sinks=sorted(ORDER[i] for i in (innb - outb)),
                spg=(min(sc), max(sc), round(float(np.mean(sc)), 2)), acyclic=acyc)

full = 1.0 + flowop.TIE_EPS * (flowop._a1 + flowop._a2) / 2.0 + flowop.TIE_EPS2 * flowop._gen
first = 1.0 + flowop.TIE_EPS * (flowop._a1 + flowop._a2) / 2.0
wf = world(full)
w1 = world(first)
print("full  : coh_edge=%.3f coh_val=%.3f sinks=%s spg=%s acyc=%d" % (wf["coh_edge"], wf["coh_val"], wf["sinks"], wf["spg"], wf["acyclic"]))
print("first : coh_edge=%.3f coh_val=%.3f sinks=%s spg=%s acyc=%d" % (w1["coh_edge"], w1["coh_val"], w1["sinks"], w1["spg"], w1["acyclic"]))
print("delta : edge=%.3f val=%.3f  (claim: falls 0.1-0.2 points going first->full)" %
      (w1["coh_edge"] - wf["coh_edge"], w1["coh_val"] - wf["coh_val"]))
