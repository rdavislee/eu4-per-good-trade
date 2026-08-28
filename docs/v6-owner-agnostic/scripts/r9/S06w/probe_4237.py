import io, os, re, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "..")
sys.path.insert(0, SCRIPTS); os.chdir(SCRIPTS)
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
print("4237 in ROWS:", any(r["pid"] == 4237 for r in ROWS))
print("4237 in devastated:", 4237 in ON_STARTUP_DEVASTATION, ON_STARTUP_DEVASTATION.get(4237))

_h = os.path.join(EU4 if False else r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV", "history", "provinces")
_coal = set()
for _fn in os.listdir(_h):
    _m = re.match(r"^\s*(\d+)", _fn)
    if not _m: continue
    _tx = io.open(os.path.join(_h, _fn), encoding="latin-1", errors="replace").read()
    if re.search(r"latent_trade_goods[^=]*=[^{]*\{[^}]*coal", _tx): _coal.add(int(_m.group(1)))
print("4237 in latent-coal set:", 4237 in _coal)

# Variant 1: coal activation, devastation RETAINED (matches measure6.py's P("coal activation..."))
W1 = W.copy()
for i, r in enumerate(ROWS):
    if r["pid"] in _coal:
        gp = GOODS_PRODUCED_FACTOR * PROV[r["pid"]]["base_production"]
        if r["pid"] in ON_STARTUP_DEVASTATION:
            gp *= 1.0 + (-2.0 * ON_STARTUP_DEVASTATION[r["pid"]] / 100.0)
        W1[i] = TAX_COEFF * PROV[r["pid"]]["base_tax"] + max(0.0, gp) * PRICES["coal"]
d1 = ph(A_PHI, W1)
flips1 = len(BD ^ set(d1["directed"])) // 2
print("variant 1 (devastation retained) wealth delta:", round(float(W1.sum()-W.sum()),2), "edge flips:", flips1)

# Variant 2: coal activation, devastation DROPPED for every latent-coal province that was devastated (mixed counterfactual)
W2 = W.copy()
for i, r in enumerate(ROWS):
    if r["pid"] in _coal:
        gp = GOODS_PRODUCED_FACTOR * PROV[r["pid"]]["base_production"]   # no devastation multiplier applied
        W2[i] = TAX_COEFF * PROV[r["pid"]]["base_tax"] + max(0.0, gp) * PRICES["coal"]
d2 = ph(A_PHI, W2)
flips2 = len(BD ^ set(d2["directed"])) // 2
print("variant 2 (devastation dropped for coal-activated provinces) wealth delta:", round(float(W2.sum()-W.sum()),2), "edge flips:", flips2)

print("difference in wealth delta (variant2 - variant1):", round(float(W2.sum()-W1.sum()),2))
print("difference in edge flips (variant2 - variant1):", flips2-flips1)

# also just province 4237 alone: value under each variant
i4237 = [i for i,r in enumerate(ROWS) if r["pid"]==4237][0]
print("province 4237 W  base:", W[i4237], "variant1:", W1[i4237], "variant2:", W2[i4237])
print("province 4237 base_production:", PROV[4237]["base_production"], "base_tax:", PROV[4237]["base_tax"])
print("expected formula 0.2*3*10*(1-0.6):", 0.2*PROV[4237]["base_production"]*10*(1-0.6) if False else None)
