import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from drain import run_drain, sinks_of
from flowop import EDGES_UND, TIE_COST
from solver import N, ORDER, NIDX, PROV, ROWS, GOODS, PRICES, build_sc, GOODS_PRODUCED_FACTOR, TAX_COEFF
W = np.array([r["tax"] + r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
def bagg(w):
    t = (w / w.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t)
    return np.full(N, 1.0 / N) - n / n.sum()
BD = set(run_drain(bagg(W))["directed"])
print("razed-hangzhou flip-count variants, shipped TIE_COST:")
# variant 1: zero wealth of hangzhou provinces (done: 32)
w2 = W.copy()
for i, r in enumerate(ROWS):
    if r["node"] == "hangzhou": w2[i] = 0.0
print("  zero wealth        :", len(set(run_drain(bagg(w2))["directed"]) ^ BD)//2)
# variant 2: drop the provinces from the table entirely
keep = [i for i, r in enumerate(ROWS) if r["node"] != "hangzhou"]
w3 = W[keep]; pn3 = pn[keep]
def bagg3(w, p):
    t = (w / w.max()) ** 2.0; n = np.zeros(N); np.add.at(n, p, t)
    return np.full(N, 1.0 / N) - n / n.sum()
print("  drop provinces     :", len(set(run_drain(bagg3(w3, pn3))["directed"]) ^ BD)//2)
# variant 3: zero base_production only
w4 = np.array([(TAX_COEFF*PROV[r["pid"]]["base_tax"] if r["node"] != "hangzhou" else TAX_COEFF*PROV[r["pid"]]["base_tax"])
               if False else (r["tax"] + (0.0 if r["node"]=="hangzhou" else r["prod_income"])) for r in ROWS])
print("  zero prod income   :", len(set(run_drain(bagg(w4))["directed"]) ^ BD)//2)
# variant 4: zero base_tax only
w5 = np.array([((0.0 if r["node"]=="hangzhou" else r["tax"]) + r["prod_income"]) for r in ROWS])
print("  zero tax           :", len(set(run_drain(bagg(w5))["directed"]) ^ BD)//2)
print()
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
print("barbell under each Phase-2 cost:")
for tag, cost in (("TIE_COST", TIE_COST), ("unit", np.ones(len(TIE_COST)))):
    drain.TIE_COST = cost
    top = bot = 0
    for g in GL:
        t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
        c = n / n.sum(); s = val[g] / val[g].sum()
        r = run_drain(s - c)
        sk = set(sinks_of(r["directed"])[0])
        order = sorted(range(N), key=lambda i: -c[i])
        top += sum(1 for i in order[:8] if i in sk)
        bot += sum(1 for i in order[-8:] if i in sk)
    print("  %-9s top8 %3d/232 = %.1f%%   bottom8 %3d/232 = %.1f%%"
          % (tag, top, 100.0*top/232, bot, 100.0*bot/232))
