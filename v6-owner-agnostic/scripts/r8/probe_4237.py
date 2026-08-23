# -*- coding: utf-8 -*-
import io, os, re, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, PROV,
                    GOODS_PRODUCED_FACTOR, TAX_COEFF, ON_STARTUP_DEVASTATION)
from drain import run_drain

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cv(a, w):
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
def ph(a, w): return run_drain(np.full(N, 1.0 / N) - cv(a, w))

base = ph(A_PHI, W); BD = set(base["directed"])

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
_h = os.path.join(EU4, "history", "provinces"); _coal = set()
for _fn in os.listdir(_h):
    _m = re.match(r"^\s*(\d+)", _fn)
    if not _m: continue
    _tx = io.open(os.path.join(_h, _fn), encoding="latin-1", errors="replace").read()
    if re.search(r"latent_trade_goods[^=]*=[^{]*\{[^}]*coal", _tx): _coal.add(int(_m.group(1)))

print("4237 in latent-coal set:", 4237 in _coal)
print("4237 in ON_STARTUP_DEVASTATION:", 4237 in ON_STARTUP_DEVASTATION, ON_STARTUP_DEVASTATION.get(4237))
print("4237 counted (in ROWS):", any(r["pid"] == 4237 for r in ROWS))

# W2: coal activation only (devastation multiplier RETAINED for all, matching measure6.py's actual computed figure -- 16 flips)
W2 = W.copy()
for i, r in enumerate(ROWS):
    if r["pid"] in _coal:
        gp = GOODS_PRODUCED_FACTOR * PROV[r["pid"]]["base_production"]
        if r["pid"] in ON_STARTUP_DEVASTATION:
            gp *= 1.0 + (-2.0 * ON_STARTUP_DEVASTATION[r["pid"]] / 100.0)
        W2[i] = TAX_COEFF * PROV[r["pid"]]["base_tax"] + max(0.0, gp) * PRICES["coal"]
d2 = ph(A_PHI, W2)
flips_coal_only = len(BD ^ set(d2["directed"])) // 2
print("coal-only wealth delta:", round(float(W2.sum() - W.sum()), 2))
print("coal-only edge flips (vs baseline):", flips_coal_only)

# W3: coal activation for all 45, but for province 4237 ALSO drop devastation (heals) --
# the mixed counterfactual the spec's parenthetical describes.
W3 = W.copy()
for i, r in enumerate(ROWS):
    if r["pid"] in _coal:
        gp = GOODS_PRODUCED_FACTOR * PROV[r["pid"]]["base_production"]
        if r["pid"] in ON_STARTUP_DEVASTATION and r["pid"] != 4237:
            gp *= 1.0 + (-2.0 * ON_STARTUP_DEVASTATION[r["pid"]] / 100.0)
        # for pid 4237: devastation dropped entirely (healed), so no multiplier applied
        W3[i] = TAX_COEFF * PROV[r["pid"]]["base_tax"] + max(0.0, gp) * PRICES["coal"]
d3 = ph(A_PHI, W3)
flips_mixed_vs_baseline = len(BD ^ set(d3["directed"])) // 2
flips_mixed_vs_coalonly = len(set(d2["directed"]) ^ set(d3["directed"])) // 2
print("mixed (coal+heal) wealth delta vs baseline:", round(float(W3.sum() - W.sum()), 2))
print("mixed wealth delta vs coal-only (i.e. healing's own contribution):", round(float(W3.sum() - W2.sum()), 2))
print("mixed edge flips vs baseline:", flips_mixed_vs_baseline)
print("mixed edge flips vs coal-only (the 'additional' edges the healing contributes):", flips_mixed_vs_coalonly)
