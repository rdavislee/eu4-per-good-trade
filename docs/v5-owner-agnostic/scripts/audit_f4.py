# -*- coding: utf-8 -*-
"""F4 done properly: real per-country trade power PER NODE from the vanilla save, so a country's
share genuinely differs between downstream nodes.  Does per-good propagation then break the
income factoring, and by how much?  collect_pool is built per good throughout (3.10 says it is)."""
import numpy as np, collections, re, sys, os, zipfile, json
sys.path.insert(0, os.getcwd())
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, sinks_of

SAVE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
z = zipfile.ZipFile(SAVE); t = z.read("gamestate").decode("latin-1"); z.close()
i = t.find("\ntrade={"); j = i + len("\ntrade="); d = 0; k = j
while k < len(t):
    if t[k] == "{": d += 1
    elif t[k] == "}":
        d -= 1
        if d == 0: break
    k += 1
tr = t[j:k+1]
POW = {}                                   # node -> {tag: power}
for m in re.finditer(r"\n\tnode=\{", tr):
    s = m.end()-1; dd = 0; e = s
    while e < len(tr):
        if tr[e] == "{": dd += 1
        elif tr[e] == "}":
            dd -= 1
            if dd == 0: break
        e += 1
    b = tr[s:e+1]; nm = re.search(r'definitions="([^"]+)"', b).group(1)
    POW[nm] = {mm.group(1): float(mm.group(2))
               for mm in re.finditer(r"\n\t\t([A-Z][A-Z0-9]{2})=\{[^}]*?\n\t\t\tval=([\d.eE+-]+)", b, re.S)}
print("nodes with a country power table:", sum(1 for v in POW.values() if v))

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]; GI = {g: GOODS.index(g) for g in GL}
val = {g: np.zeros(N) for g in GL}
for r in ROWS:
    if r["good"] in val: val[r["good"]][NIDX[r["node"]]] += r["prod_income"]
R = {g: run_drain(S[GI[g]]-C[GI[g]]) for g in GL}
wealth = np.array([r["tax"]+r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
tt = (wealth/wealth.max())**1.5; num = np.zeros(N); np.add.at(num, pn, tt)
PHIW = run_drain(np.full(N, 1.0/N) - num/num.sum())

def analyse(node):
    n = NIDX[node]; sink = {g for g in GL if n in sinks_of(R[g]["directed"])[0]}
    here = POW.get(node, {})
    if not here: return None
    tags = sorted(here, key=lambda c: -here[c])[:6]
    COL, TR = tags[:3], tags[3:]
    rng = np.random.default_rng(11)
    elig = {g: [c for c in TR if rng.random() < 0.6] for g in GL}
    def prop(directed, c):
        return sum(POW.get(ORDER[m], {}).get(c, 0.0) for u, m in directed if u == n) / 5.0
    PS = {c: {g: prop(PHIW["directed"], c) for g in GL} for c in tags}
    PGp = {c: {g: prop(R[g]["directed"], c) for g in GL} for c in tags}
    def pergood(P):
        o = collections.defaultdict(float)
        for g in GL:
            if val[g][n] <= 0: continue
            Pc = sum(here[c]+P[c][g] for c in COL); Pt = sum(here[c]+P[c][g] for c in elig[g])
            sh = 1.0 if g in sink else (Pc/(Pc+Pt) if Pc+Pt > 0 else 0.0)
            for c in COL: o[c] += val[g][n]*sh*((here[c]+P[c][g])/Pc)
        return o
    def scalar(P):
        ref = GL[0]
        Pc_ref = sum(here[c]+P[c][ref] for c in COL); pool = 0.0
        for g in GL:
            if val[g][n] <= 0: continue
            Pc = sum(here[c]+P[c][g] for c in COL)          # collect_pool IS per good on the inside
            Pt = sum(here[c]+P[c][g] for c in elig[g])
            sh = 1.0 if g in sink else (Pc/(Pc+Pt) if Pc+Pt > 0 else 0.0)
            pool += val[g][n]*sh
        return {c: pool*((here[c]+P[c][ref])/Pc_ref) for c in COL}, pool
    out = {}
    for label, P in (("single graph", PS), ("per good", PGp)):
        a = pergood(P); b, pool = scalar(P)
        errs = [(b[c]-a[c])/a[c] for c in COL if a[c]]
        out[label] = (max(abs(e) for e in errs), pool, sum(a.values()),
                      [round(100*e, 3) for e in errs])
    shares = {g: tuple(round((here[c]+PGp[c][g])/sum(here[x]+PGp[x][g] for x in COL), 9) for c in COL) for g in GL}
    out["distinct powershares across goods"] = len(set(shares.values()))
    return out, COL

for node in ("gulf_of_siam", "sevilla", "champagne", "genua", "malacca"):
    r = analyse(node)
    if not r: print("%-14s (no country table)" % node); continue
    o, COL = r
    print("\n%s  collectors=%s" % (node, COL))
    print("   distinct powershare vectors across the 29 goods: %d" % o["distinct powershares across goods"])
    for label in ("single graph", "per good"):
        w, pool, tot, errs = o[label]
        print("   %-12s worst relative error %.4e  (per collector %% %s)  node collects %.1f" % (label, w, errs, tot))
