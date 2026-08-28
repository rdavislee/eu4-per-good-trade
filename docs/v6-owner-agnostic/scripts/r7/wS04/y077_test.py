# -*- coding: utf-8 -*-
"""Isolated province-4237-only counterfactual for Y077: hold every OTHER input fixed
at the baseline (installed) field, and only reprice province 4237 to coal while
also dropping its devastation multiplier. Report wealth delta and edge-flip count
against the baseline directed edge set, computed exactly as measure6.py does."""
import io, os, re, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, GOODS_PRODUCED_FACTOR, TAX_COEFF,
                     ON_STARTUP_DEVASTATION, PROV, PRICES, ROWS)
from drain import run_drain

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

def cv(a, w):
    t = (w / w.max()) ** a
    n = np.zeros(N)
    np.add.at(n, pn, t)
    return n / n.sum()

def ph(a, w):
    return run_drain(np.full(N, 1.0 / N) - cv(a, w))

base = ph(A_PHI, W)
BD = set(base["directed"])

# confirm 4237 is in ROWS, latent-coal, and devastated
idx4237 = [i for i, r in enumerate(ROWS) if r["pid"] == 4237]
print("province 4237 rows found:", idx4237, [ROWS[i] for i in idx4237])
print("4237 in ON_STARTUP_DEVASTATION:", 4237 in ON_STARTUP_DEVASTATION,
      ON_STARTUP_DEVASTATION.get(4237))

# locate latent-coal set the same way measure6.py does
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
_h = os.path.join(EU4, "history", "provinces")
_coal = set()
for _fn in os.listdir(_h):
    _m = re.match(r"^\s*(\d+)", _fn)
    if not _m:
        continue
    _tx = io.open(os.path.join(_h, _fn), encoding="latin-1", errors="replace").read()
    if re.search(r"latent_trade_goods[^=]*=[^{]*\{[^}]*coal", _tx):
        _coal.add(int(_m.group(1)))
print("4237 in latent-coal set:", 4237 in _coal)

# Isolated counterfactual: ONLY province 4237 changes -- reprice to coal AND drop devastation.
W3 = W.copy()
for i, r in enumerate(ROWS):
    if r["pid"] == 4237:
        gp = GOODS_PRODUCED_FACTOR * PROV[r["pid"]]["base_production"]   # devastation dropped
        W3[i] = TAX_COEFF * PROV[r["pid"]]["base_tax"] + max(0.0, gp) * PRICES["coal"]
        print("row before:", r["tax"] + r["prod_income"], "row after:", W3[i],
              "delta:", W3[i] - (r["tax"] + r["prod_income"]))

wealth_delta = round(float(W3.sum() - W.sum()), 2)
print("isolated 4237 wealth delta:", wealth_delta)

new = ph(A_PHI, W3)
ND = set(new["directed"])
flips = len(BD ^ ND) // 2
print("isolated 4237 edge flips vs baseline:", flips)
print("sym-diff raw count:", len(BD ^ ND))

# also compare against the 45-province coal-reprice field (as in measure6.py) to see whether
# adding the devastation-drop on top of THAT field moves any additional edge
_coal_owned = set(r["pid"] for r in ROWS if r["pid"] in _coal)
W2 = W.copy()   # all 45 latent-coal owned provinces repriced to coal, devastation multiplier retained
for i, r in enumerate(ROWS):
    if r["pid"] in _coal:
        gp = GOODS_PRODUCED_FACTOR * PROV[r["pid"]]["base_production"]
        if r["pid"] in ON_STARTUP_DEVASTATION:
            gp *= 1.0 + (-2.0 * ON_STARTUP_DEVASTATION[r["pid"]] / 100.0)
        W2[i] = TAX_COEFF * PROV[r["pid"]]["base_tax"] + max(0.0, gp) * PRICES["coal"]
new2 = ph(A_PHI, W2)
ND2 = set(new2["directed"])
flips2 = len(BD ^ ND2) // 2
print("45-province coal reprice (devastation retained) wealth delta:",
      round(float(W2.sum() - W.sum()), 2), "edge flips:", flips2)

# Now: 45-province reprice PLUS drop 4237's devastation on top of it (mixed counterfactual
# matching the doc's wording "a reprice that drops its devastation" -- i.e. the 45-reprice with
# 4237 ALSO healed)
W4 = W2.copy()
for i, r in enumerate(ROWS):
    if r["pid"] == 4237:
        gp = GOODS_PRODUCED_FACTOR * PROV[r["pid"]]["base_production"]   # devastation dropped, coal priced
        W4[i] = TAX_COEFF * PROV[r["pid"]]["base_tax"] + max(0.0, gp) * PRICES["coal"]
new4 = ph(A_PHI, W4)
ND4 = set(new4["directed"])
flips4 = len(BD ^ ND4) // 2
print("45-province reprice WITH 4237 healed, wealth delta vs baseline:",
      round(float(W4.sum() - W.sum()), 2), "edge flips vs baseline:", flips4)
print("edge flips: 45-with-heal vs 45-without-heal (additional edges from healing 4237):",
      len(ND ^ ND4) // 2 if False else len(ND2 ^ ND4) // 2)
