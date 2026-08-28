# -*- coding: utf-8 -*-
"""Check the four measurable observations from the round-2 claims extraction:
2.8's agreement label, 3.9's node-wealth ranks, what the save's `highest_power` field actually is,
and 3.5's boundary-goods count."""
import os, re, sys, collections, zipfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc)
from drain import run_drain

wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, wealth)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
def cvec(a=1.5):
    t = (wealth / wealth.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()

print("=" * 96); print("1.  the two agreement numbers, unweighted and value-weighted"); print("=" * 96)
R = {g: run_drain(S[gi] - C[gi]) for gi, g in GL}
rw = run_drain(np.full(N, 1.0 / N) - cvec()); dws = set(rw["directed"])
PGd = {g: set(R[g]["directed"]) for _, g in GL}
a = t = 0; wa = wt = 0.0
for gi, g in GL:
    for u, v in EDGES_UND:
        gd = (u, v) if (u, v) in PGd[g] else ((v, u) if (v, u) in PGd[g] else None)
        if gd is None: continue
        t += 1; wt += V[gi]
        if ((u, v) if (u, v) in dws else (v, u)) == gd: a += 1; wa += V[gi]
print("  Phi_w unweighted %.1f%%   value-weighted %.1f%%" % (100.0*a/t, 100.0*wa/wt))

print(); print("=" * 96); print("2.  3.9's node-wealth ranks on the v5.0 field"); print("=" * 96)
wrank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-NW))}
cw = cvec(); crank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-cw))}
for n_ in ("genua", "gulf_of_siam", "sevilla", "venice", "english_channel", "hangzhou"):
    print("  %-16s node wealth %7.1f  rank %2d   |  c_w rank %2d"
          % (n_, NW[NIDX[n_]], wrank[n_], crank[n_]))

print(); print("=" * 96); print("3.  what the save's `highest_power` field actually holds"); print("=" * 96)
SAVE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
z = zipfile.ZipFile(SAVE); txt = z.read("gamestate").decode("latin-1"); z.close()
i = txt.find("\ntrade={"); j = i + len("\ntrade="); d = 0; k = j
while k < len(txt):
    if txt[k] == "{": d += 1
    elif txt[k] == "}":
        d -= 1
        if d == 0: break
    k += 1
tr = txt[j:k + 1]
rows = []
for m in re.finditer(r"\n\tnode=\{", tr):
    s = m.end() - 1; dd = 0; e = s
    while e < len(tr):
        if tr[e] == "{": dd += 1
        elif tr[e] == "}":
            dd -= 1
            if dd == 0: break
        e += 1
    b = tr[s:e + 1]; nm = re.search(r'definitions="([^"]+)"', b).group(1)
    hp = re.search(r"\n\t\thighest_power=([\d.]+)", b)
    pw = {mm.group(1): float(mm.group(2))
          for mm in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{[^{}]*?\n\t\t\tval=([\d.]+)', b)}
    prov = re.search(r"\n\t\tprovincial_trade_power=([\d.]+)", b)
    tot = re.search(r"\n\t\ttotal=([\d.]+)", b)
    cur = re.search(r"\n\t\tcurrent=([\d.]+)", b)
    if hp and pw:
        rows.append((nm, float(hp.group(1)), max(pw.values()), sum(pw.values()),
                     float(prov.group(1)) if prov else None,
                     float(tot.group(1)) if tot else None,
                     float(cur.group(1)) if cur else None, sorted(pw.values())[-3:]))
print("  %-16s %9s %9s %9s %9s %9s %9s" % ("node", "highest", "max(val)", "sum(val)", "provincial", "total", "current"))
for r_ in rows[:10]:
    print("  %-16s %9.2f %9.2f %9.2f %9s %9s %9s"
          % (r_[0], r_[1], r_[2], r_[3],
             "-" if r_[4] is None else "%.2f" % r_[4],
             "-" if r_[5] is None else "%.2f" % r_[5],
             "-" if r_[6] is None else "%.2f" % r_[6]))
hp = np.array([r_[1] for r_ in rows]); mx = np.array([r_[2] for r_ in rows])
sm = np.array([r_[3] for r_ in rows])
print("  n=%d   highest_power range %.2f..%.2f" % (len(rows), hp.min(), hp.max()))
for lab, arr in (("max(country val)", mx), ("sum(country val)", sm)):
    print("     vs %-18s equal on %d/%d | max |diff| %.3f" % (lab, int((np.abs(hp-arr) < 1e-6).sum()), len(rows), np.abs(hp-arr).max()))
prov = np.array([r_[4] if r_[4] is not None else np.nan for r_ in rows])
if not np.all(np.isnan(prov)):
    ok = ~np.isnan(prov)
    print("     vs provincial_trade_power  equal on %d/%d | max |diff| %.3f"
          % (int((np.abs(hp[ok]-prov[ok]) < 1e-6).sum()), int(ok.sum()), np.abs(hp[ok]-prov[ok]).max()))
# is it a share?
print("     highest_power / sum(val): %.4f..%.4f" % ((hp/sm).min(), (hp/sm).max()))
print("     the five largest highest_power values:",
      [(r_[0], r_[1]) for r_ in sorted(rows, key=lambda x: -x[1])[:5]])

print(); print("=" * 96); print("4.  3.5's boundary goods (floor lands exactly on 2.0)"); print("=" * 96)
import pdx
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
hits = []
def walk(node, src):
    for kk, vv in node:
        if isinstance(vv, pdx.Node):
            if kk == "change_price":
                tg, val = vv.get("trade_goods"), vv.get("value")
                if tg is not None and val is not None: hits.append((tg, float(val)))
            walk(vv, src)
for tree in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, tree)):
        for fn in fs:
            if fn.endswith(".txt"):
                try: walk(pdx.load(os.path.join(dp, fn)), tree)
                except Exception: pass
neg = collections.defaultdict(list)
for tg, v_ in hits:
    if v_ < 0: neg[tg].append(v_)
below, exact, above, none_ = [], [], [], []
for g in sorted(PRICES):
    if PRICES[g] <= 0: continue
    if g not in neg: none_.append(g); continue
    fl = PRICES[g] * (1 + min(neg[g]))
    (below if fl < 2.0 - 1e-9 else exact if abs(fl - 2.0) < 1e-9 else above).append((g, round(fl, 3)))
print("  floor exactly 2.0 :", exact)
print("  floor below  2.0 :", len(below), "| above:", len(above), "| no negative event:", len(none_))
