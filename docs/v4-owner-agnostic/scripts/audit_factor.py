# -*- coding: utf-8 -*-
"""Audit of spec v4.0 §3.10's rewritten paragraphs and of factor.py's construction."""
import numpy as np, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, sinks_of

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
GI = {g: GOODS.index(g) for g in GL}
value = {g: np.zeros(N) for g in GL}
for r in ROWS:
    if r["good"] in value:
        value[r["good"]][NIDX[r["node"]]] += r["prod_income"]
prov_power = np.zeros(N)
for r in ROWS:
    prov_power[NIDX[r["node"]]] += r["prod_income"]
R = {g: run_drain(S[GI[g]] - C[GI[g]]) for g in GL}
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = (wealth / wealth.max()) ** 1.5
num = np.zeros(N); np.add.at(num, pn, t)
PHIW = run_drain(np.full(N, 1.0 / N) - num / num.sum())

NODE = "gulf_of_siam"; n = NIDX[NODE]
sinks_here = {g for g in GL if n in sinks_of(R[g]["directed"])[0]}

print("=" * 92)
print("A. §3.10's downstream-set claim for gulf_of_siam")
print("=" * 92)
sets_ = {}
for g in GL:
    down = frozenset(ORDER[v] for u, v in R[g]["directed"] if u == n)
    sets_.setdefault(down, []).append(g)
print("  distinct downstream sets across the %d live goods: %d" % (len(GL), len(sets_)))
for k in sorted(sets_, key=lambda s: -len(sets_[s])):
    print("    %-2d goods -> %s" % (len(sets_[k]), sorted(k) if k else "(none - sink)"))
print("  Phi_w downstream set: %s" % sorted(ORDER[v] for u, v in PHIW["directed"] if u == n))
print("  goods that sink here: %d" % len(sinks_here))

# ---------------------------------------------------------------------------
COUNTRY_POWER = {"CAS": 129.9, "POR": 88.5, "MOR": 23.4, "GRA": 11.6, "ARA": 0.0, "FRA": 0.0}
HOME = {"CAS": "sevilla"}
COLLECTORS = ["CAS", "POR", "GRA"]
TRANSFERRERS = ["MOR", "ARA", "FRA"]
PEN = -0.50


def collect_power(cty, extra, node):
    p = COUNTRY_POWER[cty] + extra
    if HOME.get(cty) != node:
        p *= (1.0 + PEN)
    return p


def propagated(directed, cty, node_i):
    down = [v for u, v in directed if u == node_i]
    frac = COUNTRY_POWER[cty] / max(prov_power[node_i], 1e-12)
    return sum(prov_power[m] * frac for m in down) / 5.0


def run(node_name, seed=11, ref_good=None, pergood_Pc=False, p_elig=0.6):
    ni = NIDX[node_name]
    sh = {g for g in GL if ni in sinks_of(R[g]["directed"])[0]}
    rng = np.random.default_rng(seed)
    elig = {g: [c for c in TRANSFERRERS if rng.random() < p_elig] for g in GL}
    prop = {c: {g: propagated(R[g]["directed"], c, ni) for g in GL} for c in COUNTRY_POWER}
    ref = ref_good or GL[0]

    def pergood():
        out = collections.defaultdict(float)
        for g in GL:
            if value[g][ni] <= 0:
                continue
            Pc = sum(collect_power(c, prop[c][g], node_name) for c in COLLECTORS)
            Pt = sum(COUNTRY_POWER[c] + prop[c][g] for c in elig[g])
            s = 1.0 if g in sh else (Pc / (Pc + Pt) if Pc + Pt > 0 else 0.0)
            for c in COLLECTORS:
                out[c] += value[g][ni] * s * (collect_power(c, prop[c][g], node_name) / Pc)
        return out

    def scalar():
        pool = 0.0
        Pcref = sum(collect_power(c, prop[c][ref], node_name) for c in COLLECTORS)
        for g in GL:
            if value[g][ni] <= 0:
                continue
            Pc = (sum(collect_power(c, prop[c][g], node_name) for c in COLLECTORS)
                  if pergood_Pc else Pcref)
            Pt = sum(COUNTRY_POWER[c] + prop[c][g] for c in elig[g])
            pool += value[g][ni] * (1.0 if g in sh else (Pc / (Pc + Pt) if Pc + Pt > 0 else 0.0))
        return {c: pool * (collect_power(c, prop[c][ref], node_name) / Pcref) for c in COLLECTORS}, pool

    a = pergood(); b, pool = scalar()
    rel = max(abs(a[c] - b[c]) / abs(a[c]) for c in COLLECTORS if a[c])
    return a, b, pool, rel, elig


print()
print("=" * 92)
print("B. the off-home penalty: how many of the three collectors does it hit at each node?")
print("=" * 92)
for nd in ("gulf_of_siam", "sevilla"):
    hit = [c for c in COLLECTORS if HOME.get(c) != nd]
    print("  %-14s penalised collectors: %d of %d %s" % (nd, len(hit), len(COLLECTORS), hit))
print("  -> where all three are penalised the 0.5 is a COMMON factor and cancels out of")
print("     powershare_C entirely; the construction does not exercise the penalty at all.")

print()
print("=" * 92)
print("C. the 0.41%: is it per-good propagation, or the scalar model freezing P_collect at GL[0]?")
print("=" * 92)
a, b, pool, rel, elig = run("gulf_of_siam")
print("  as shipped (ref good = GL[0] = %-10s): worst relative error %.4f%%   pool %.4f"
      % (GL[0], 100 * rel, pool))
a2, b2, pool2, rel2, _ = run("gulf_of_siam", pergood_Pc=True)
print("  same run, pool computed with PER-GOOD P_collect : worst relative error %.3e  pool %.4f"
      % (rel2, pool2))
print("  (§3.10 already concedes collect_pool is 'per good on the inside')")

print()
print("  sensitivity to which good is used as the scalar reference:")
rows = []
for g in GL:
    aa, bb, pp, rr, _ = run("gulf_of_siam", ref_good=g)
    signed = (bb["CAS"] - aa["CAS"]) / aa["CAS"] * 100
    rows.append((signed, g))
rows.sort()
print("    most UNDER-stated : %s" % [(g, "%+.2f%%" % s) for s, g in rows[:4]])
print("    most OVER-stated  : %s" % [(g, "%+.2f%%" % s) for s, g in rows[-4:]])
print("    goods giving a NEGATIVE (understating) error: %d of %d" % (sum(1 for s, _ in rows if s < 0), len(rows)))

print()
print("  sensitivity to the eligibility rng seed (shipped seed = 11):")
for sd in (11, 1, 2, 3, 4, 5, 99):
    aa, bb, pp, rr, el = run("gulf_of_siam", seed=sd)
    print("    seed %-3d worst relative error %.3f%%   pool %.3f  node income %.2f"
          % (sd, 100 * rr, pp, sum(aa.values())))
print()
print("  sensitivity to the eligibility probability (shipped p = 0.6):")
for p in (0.0, 0.3, 0.6, 0.9, 1.0):
    aa, bb, pp, rr, el = run("gulf_of_siam", p_elig=p)
    print("    p = %.1f  worst relative error %.3f%%   node income %.2f" % (p, 100 * rr, sum(aa.values())))

print()
print("=" * 92)
print("D. does powershare_C actually stop factoring out under per-good propagation?")
print("=" * 92)
ni = NIDX["gulf_of_siam"]
prop = {c: {g: propagated(R[g]["directed"], c, ni) for g in GL} for c in COUNTRY_POWER}
for g in GL[:6]:
    Pc = sum(collect_power(c, prop[c][g], "gulf_of_siam") for c in COLLECTORS)
    shares = [collect_power(c, prop[c][g], "gulf_of_siam") / Pc for c in COLLECTORS]
    print("    %-12s powershare_C = %s" % (g, ["%.12f" % s for s in shares]))
print("  -> identical for every good: factor.py's propagated power is proportional to the")
print("     country's own power, so the good-dependent factor cancels in the share.")
