# -*- coding: utf-8 -*-
"""factor.py - the two figures 3.10 still carries under [unverified in v4.0]:
     (1) "agreement to 5.7e-14" for  income_C(n) = powershare_C(n) . collect_pool(n)
     (2) "reproduces per-good truth to 1.4e-14 ... off by 5.96 ducats on a node paying ~250"
         when propagation is per good instead of on the one installed graph.

Every choice is stated, so the construction is reproducible.  Real 1444 data throughout:
per-good node values from the reference solver, the per-good graphs and PHI_w from DRAIN,
and Sevilla's real country list.
"""
import numpy as np, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, sinks_of

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
GI = {g: GOODS.index(g) for g in GL}

# ---------------------------------------------------------------- model quantities
# value_g(n): the node's own annual trade value in good g (1.3's trade_value, summed per good).
value = {g: np.zeros(N) for g in GL}
for r in ROWS:
    if r["good"] in value:
        value[r["good"]][NIDX[r["node"]]] += r["prod_income"]

# provincial trade power, for this test: a province's trade value.  Stated choice - the model
# computes trade value, not EU4's provincial power, and 3.10 is about the model's own algebra.
prov_power = np.zeros(N)
for r in ROWS:
    prov_power[NIDX[r["node"]]] += r["prod_income"]

# per-good graphs and the installed graph
R = {g: run_drain(S[GI[g]] - C[GI[g]]) for g in GL}
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = (wealth / wealth.max()) ** 1.5
num = np.zeros(N); np.add.at(num, pn, t)
PHIW = run_drain(np.full(N, 1.0 / N) - num / num.sum())

NODE = os.environ.get("FNODE","gulf_of_siam"); n = NIDX[NODE]
sinks_here = {g for g in GL if n in sinks_of(R[g]["directed"])[0]}
print("node: %s | goods with nonzero local value: %d | goods that SINK here: %d %s"
      % (NODE, sum(1 for g in GL if value[g][n] > 0), len(sinks_here), sorted(sinks_here)))

# ---------------------------------------------------------------- countries
# Sevilla's real 1444 country list, read from the game this session (province trade power).
COUNTRY_POWER = {"CAS": 129.9, "POR": 88.5, "MOR": 23.4, "GRA": 11.6, "ARA": 0.0, "FRA": 0.0}
HOME = {"CAS": "sevilla"}                       # Castile's home trade node is Sevilla
COLLECTORS = ["CAS", "POR", "GRA"]              # merchant-or-home; stated
TRANSFERRERS = ["MOR", "ARA", "FRA"]            # steer or collect downstream; stated
TRADE_NON_CAPITAL_OFFICE = -0.50                # defines.lua

def collect_power(cty, extra=0.0):
    p = COUNTRY_POWER[cty] + extra
    if HOME.get(cty) != NODE:
        p *= (1.0 + TRADE_NON_CAPITAL_OFFICE)   # 1.8's off-home penalty is on POWER
    return p

# transfer eligibility is per good (1.8): a transferrer counts for g only if it steers g here.
rng = np.random.default_rng(11)
eligible = {g: [c for c in TRANSFERRERS if rng.random() < 0.6] for g in GL}

# ---------------------------------------------------------------- (1) the factoring
def incomes_pergood(prop):
    """prop[cty][g] = propagated power added to cty at this node for good g."""
    out = collections.defaultdict(float)
    for g in GL:
        if value[g][n] <= 0: continue
        Pc = sum(collect_power(c, prop[c][g]) for c in COLLECTORS)
        Pt = sum(COUNTRY_POWER[c] + prop[c][g] for c in eligible[g])
        share = 1.0 if g in sinks_here else (Pc / (Pc + Pt) if (Pc + Pt) > 0 else 0.0)
        for c in COLLECTORS:
            out[c] += value[g][n] * share * (collect_power(c, prop[c][g]) / Pc)
    return out

def incomes_scalar(prop):
    """the node-scalar model: one powershare, one collect_pool."""
    Pc = sum(collect_power(c, prop[c][GL[0]]) for c in COLLECTORS)
    pool = 0.0
    for g in GL:
        if value[g][n] <= 0: continue
        Pt = sum(COUNTRY_POWER[c] + prop[c][g] for c in eligible[g])
        share = 1.0 if g in sinks_here else (Pc / (Pc + Pt) if (Pc + Pt) > 0 else 0.0)
        pool += value[g][n] * share
    return {c: pool * (collect_power(c, prop[c][GL[0]]) / Pc) for c in COLLECTORS}, pool

zero = {c: {g: 0.0 for g in GL} for c in COUNTRY_POWER}
a = incomes_pergood(zero); b, pool = incomes_scalar(zero)
print("\n(1) FACTORING, no propagation")
print("    collect_pool(n) = %.6f" % pool)
worst = 0.0
for c in COLLECTORS:
    d = abs(a[c] - b[c]); rel = d / abs(a[c]) if a[c] else 0.0
    worst = max(worst, rel)
    print("    %-4s per-good %.12f  scalar %.12f  |diff| %.3e  rel %.3e" % (c, a[c], b[c], d, rel))
print("    worst relative disagreement: %.3e" % worst)

# ---------------------------------------------------------------- (2) propagation
def propagated(graph_directed, cty):
    """1.9: share 1/TRADE_PROPAGATE_DIVIDER of provincial power in every node this node is
    upstream of, i.e. over n's outgoing neighbours in the given orientation."""
    down = [v for u, v in graph_directed if u == n]
    frac = COUNTRY_POWER[cty] / max(prov_power[n], 1e-12)   # cty's share of this node's power
    return sum(prov_power[m] * frac for m in down) / 5.0

prop_single = {c: {g: propagated(PHIW["directed"], c) for g in GL} for c in COUNTRY_POWER}
prop_pergood = {c: {g: propagated(R[g]["directed"], c) for g in GL} for c in COUNTRY_POWER}

a1 = incomes_pergood(prop_single); b1, pool1 = incomes_scalar(prop_single)
print("\n(2a) PROPAGATION ON THE ONE INSTALLED GRAPH (PHI_w)")
print("     collect_pool(n) = %.4f ducats" % pool1)
worst1 = max(abs(a1[c] - b1[c]) for c in COLLECTORS)
worstr1 = max(abs(a1[c] - b1[c]) / abs(a1[c]) for c in COLLECTORS if a1[c])
for c in COLLECTORS:
    print("     %-4s per-good %.10f  scalar %.10f  |diff| %.3e" % (c, a1[c], b1[c], abs(a1[c]-b1[c])))
print("     worst |diff| %.3e ducats | worst relative %.3e" % (worst1, worstr1))

a2 = incomes_pergood(prop_pergood); b2, pool2 = incomes_scalar(prop_pergood)
print("\n(2b) PROPAGATION PER GOOD (power varies by good)")
print("     collect_pool(n) = %.4f ducats" % pool2)
worst2 = 0.0
for c in COLLECTORS:
    d = abs(a2[c] - b2[c]); worst2 = max(worst2, d)
    print("     %-4s per-good %.6f  scalar %.6f  |diff| %.4f ducats (%.2f%%)"
          % (c, a2[c], b2[c], d, 100 * d / a2[c] if a2[c] else 0))
print("     worst |diff| %.4f ducats on a node paying %.1f (%.2f%% of node income)"
      % (worst2, sum(a2.values()), 100 * worst2 / sum(a2.values())))
print("     total per-good income %.4f vs scalar %.4f | total error %.4f ducats"
      % (sum(a2.values()), sum(b2.values()), abs(sum(a2.values()) - sum(b2.values()))))
