# -*- coding: utf-8 -*-
"""F4 replacement, attacked: real per-node, per-country provincial trade power from
VANILLA_start.eu4, so a country's share genuinely differs between downstream nodes.

Stated choices (the thing factor.py did not state):
  collectors   = the three largest holders of provincial power in the node
  transferrers = the next six, eligibility per good by a seeded draw
  the scalar model's single powershare is taken from the INSTALLED graph (Phi_w)
  collect_pool is built PER GOOD (3.10 already concedes it is per good on the inside)
"""
import os, re, sys, zipfile, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, sinks_of

SG = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"
z = zipfile.ZipFile(os.path.join(SG, "VANILLA_start.eu4"))
t = z.read("gamestate").decode("latin-1"); z.close()
i = t.find("\ntrade={"); j = i + len("\ntrade="); d = 0; k = j
while k < len(t):
    if t[k] == "{": d += 1
    elif t[k] == "}":
        d -= 1
        if d == 0: break
    k += 1
tr = t[j:k + 1]
PP = {}                      # node -> {country: provincial trade power}
for m2 in re.finditer(r"\n\tnode=\{", tr):
    s0 = m2.end() - 1; d2 = 0; e = s0
    while e < len(tr):
        if tr[e] == "{": d2 += 1
        elif tr[e] == "}":
            d2 -= 1
            if d2 == 0: break
        e += 1
    b = tr[s0:e + 1]
    nm = re.search(r'definitions="([^"]+)"', b).group(1)
    cs = {}
    for cm in re.finditer(r"\n\t\t([A-Z0-9]{3})=\{", b):
        s1 = cm.end() - 1; d3 = 0; e1 = s1
        while e1 < len(b):
            if b[e1] == "{": d3 += 1
            elif b[e1] == "}":
                d3 -= 1
                if d3 == 0: break
            e1 += 1
        blk = b[s1:e1 + 1]
        pw = re.search(r"province_power=([\d.eE+-]+)", blk)
        if pw: cs[cm.group(1)] = float(pw.group(1))
    PP[nm] = cs

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
GI = {g: GOODS.index(g) for g in GL}
value = {g: np.zeros(N) for g in GL}
for r in ROWS:
    if r["good"] in value: value[r["good"]][NIDX[r["node"]]] += r["prod_income"]
R = {g: run_drain(S[GI[g]] - C[GI[g]]) for g in GL}
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
tt = (wealth / wealth.max()) ** 1.5
num = np.zeros(N); np.add.at(num, pn, tt)
PHIW = run_drain(np.full(N, 1.0 / N) - num / num.sum())
PEN = -0.50

def analyse(node, seed=11):
    ni = NIDX[node]
    holders = sorted(PP.get(node, {}).items(), key=lambda kv: -kv[1])
    if len(holders) < 4: return None
    COLL = [c for c, _ in holders[:3]]
    TRAN = [c for c, _ in holders[3:9]]
    HOMEC = COLL[0]                                     # largest holder is home here
    sh = {g for g in GL if ni in sinks_of(R[g]["directed"])[0]}
    rng = np.random.default_rng(seed)
    elig = {g: [c for c in TRAN if rng.random() < 0.6] for g in GL}
    def prop(directed, c):
        return sum(PP.get(ORDER[m], {}).get(c, 0.0) for u, m in directed if u == ni) / 5.0
    pg = {c: {g: prop(R[g]["directed"], c) for g in GL} for c in COLL + TRAN}
    ps = {c: prop(PHIW["directed"], c) for c in COLL + TRAN}
    base = {c: PP[node].get(c, 0.0) for c in COLL + TRAN}
    def cpow(c, extra): return (base[c] + extra) * (1.0 + PEN if c != HOMEC else 1.0)
    # per-good truth
    truth = collections.defaultdict(float)
    vecs = set()
    for g in GL:
        if value[g][ni] <= 0: continue
        Pc = sum(cpow(c, pg[c][g]) for c in COLL)
        Pt = sum(base[c] + pg[c][g] for c in elig[g])
        s = 1.0 if g in sh else (Pc / (Pc + Pt) if Pc + Pt > 0 else 0.0)
        vecs.add(tuple(round(cpow(c, pg[c][g]) / Pc, 12) for c in COLL))
        for c in COLL: truth[c] += value[g][ni] * s * (cpow(c, pg[c][g]) / Pc)
    # node-scalar, powershare from the installed graph, pool per good
    def scalar(propmap, permap):
        Pc0 = sum(cpow(c, propmap[c]) for c in COLL)
        pool = 0.0
        for g in GL:
            if value[g][ni] <= 0: continue
            Pc = sum(cpow(c, permap[c][g]) for c in COLL)
            Pt = sum(base[c] + permap[c][g] for c in elig[g])
            pool += value[g][ni] * (1.0 if g in sh else (Pc / (Pc + Pt) if Pc + Pt > 0 else 0.0))
        return {c: pool * cpow(c, propmap[c]) / Pc0 for c in COLL}, pool
    sc, pool = scalar(ps, pg)
    # control: single installed graph everywhere (propagation good-independent)
    truth1 = collections.defaultdict(float)
    for g in GL:
        if value[g][ni] <= 0: continue
        Pc = sum(cpow(c, ps[c]) for c in COLL)
        Pt = sum(base[c] + ps[c] for c in elig[g])
        s = 1.0 if g in sh else (Pc / (Pc + Pt) if Pc + Pt > 0 else 0.0)
        for c in COLL: truth1[c] += value[g][ni] * s * (cpow(c, ps[c]) / Pc)
    sc1, _ = scalar(ps, {c: {g: ps[c] for g in GL} for c in COLL + TRAN})
    ctl = max(abs(truth1[c] - sc1[c]) / abs(truth1[c]) for c in COLL if truth1[c])
    errs = [100 * (sc[c] - truth[c]) / truth[c] if truth[c] else 0.0 for c in COLL]
    return node, COLL, len(vecs), ctl, errs, sum(truth.values())

print("%-16s %-16s %-6s %-12s %-34s %s" % ("node","collectors","vecs","single-graph","per-good propagation (% by collector)","income"))
for nd in ("gulf_of_siam","malacca","genua","champagne","sevilla","english_channel","hangzhou","canton"):
    r = analyse(nd)
    if r is None: continue
    node, coll, nv, ctl, errs, inc = r
    print("%-16s %-16s %-6d %-12.1e %-34s %.1f" % (node, ",".join(coll), nv, ctl,
          " ".join("%+.3f" % e for e in errs), inc))
print()
print("seed sensitivity of the per-good column, sevilla:")
for sd in (11,1,2,3,4,5,99):
    r = analyse("sevilla", seed=sd)
    print("   seed %-3d vecs=%d  errors %s" % (sd, r[2], " ".join("%+.3f%%" % e for e in r[4])))
