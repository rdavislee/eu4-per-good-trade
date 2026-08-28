# -*- coding: utf-8 -*-
"""Re-measure the four figures the v5 claims-delta extraction flagged as stale or contradictory:
the razed-China row (2.8), the inland-node basis (1.10 / 2.2), the spices supply/demand contrast
(3.2 / 3.15), and the caravan share on both bases."""
import os, re, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx
from solver import N, ORDER, NIDX, UND, GOODS, PRICES, ROWS, build_sc, NODES
from drain import run_drain

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cvec(a=1.5, w=None):
    w = wealth if w is None else w
    t = (w / w.max()) ** a; num = np.zeros(N); np.add.at(num, pn, t); return num / num.sum()
def phiw(a=1.5, w=None):
    return run_drain(np.full(N, 1.0 / N) - cvec(a, w))
def sinks(r):
    o = collections.Counter(u for u, _ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if o[i] == 0)

print("=" * 96); print("1.  2.8's Razed-China row, on the v5.0 wealth field"); print("=" * 96)
base = phiw()
print("  baseline sinks                      ", sinks(base))
cw = cvec(); crank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-cw))}
NW = np.zeros(N); np.add.at(NW, pn, wealth)
wrank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-NW))}
for node in ("hangzhou", "beijing"):
    w2 = wealth.copy()
    w2[[i for i, r in enumerate(ROWS) if r["node"] == node]] = 0.0
    print("  zeroing %-9s -> sinks        " % node, sinks(phiw(1.5, w2)))
    print("     %-9s c_w rank %d, node-wealth rank %d, node wealth %.1f"
          % (node, crank[node], wrank[node], NW[NIDX[node]]))
rich = ROWS[int(np.argmax(wealth))]
print("  richest single province             ", rich["pid"], rich["node"], round(float(wealth.max()), 2))

print(); print("=" * 96); print("2.  inland nodes: the flag against the derivation"); print("=" * 96)
tn = pdx.load(os.path.join(EU4, "common", "tradenodes", "00_tradenodes.txt"))
COAST = set()
for dp, _, fs in os.walk(os.path.join(EU4, "map")):
    for fn in fs:
        if fn == "positions.txt": pass
raw = open(os.path.join(EU4, "map", "default.map"), encoding="latin-1").read()
sea = set()
for key in ("sea_starts", "lakes"):
    m = re.search(key + r"\s*=\s*\{([^}]*)\}", raw)
    if m: sea |= set(int(x) for x in re.findall(r"\d+", m.group(1)))
adj = collections.defaultdict(set)
for line in open(os.path.join(EU4, "map", "adjacencies.csv"), encoding="latin-1").read().split("\n")[1:]:
    p = line.split(";")
    if len(p) > 2 and p[0].isdigit() and p[1].isdigit():
        adj[int(p[0])].add(int(p[1])); adj[int(p[1])].add(int(p[0]))
flag_inland, derived_inland, members = [], [], {}
for k, v in tn:
    if not isinstance(v, pdx.Node): continue
    mem = [int(x) for x in pdx.values(v.get("members") or [])]
    members[k] = mem
    if str(v.get("inland")).lower() in ("yes", "true"): flag_inland.append(k)
# a node is derived-inland when no member province touches a sea/lake province
import json
try:
    ADJP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "coastal.json")))
    coastal = set(int(x) for x in (ADJP if isinstance(ADJP, list) else ADJP.get("coastal", [])))
except Exception:
    coastal = set()
print("  coastal.json provinces               ", len(coastal))
for k, mem in members.items():
    if not any(p in coastal for p in mem): derived_inland.append(k)
print("  flag inland nodes                    ", len(flag_inland))
print("  derived inland nodes                 ", len(derived_inland))
print("  flag-only                            ", sorted(set(flag_inland) - set(derived_inland)))
print("  derived-only                         ", sorted(set(derived_inland) - set(flag_inland)))

print(); print("=" * 96); print("3.  spices supply / demand contrast, no regularizer"); print("=" * 96)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
gi = GOODS.index("spices")
sp = S[gi][S[gi] > 0]; dm = C[gi][C[gi] > 0]
print("  spices supply  max/min over producing nodes  %.1f  (%d nodes)" % (sp.max() / sp.min(), len(sp)))
print("  spices demand  max/min over demanding nodes  %.1f  (%d nodes)" % (dm.max() / dm.min(), len(dm)))
alls, alld = [], []
for g_i, g in enumerate(GOODS):
    if not LIVE[g_i]: continue
    a = S[g_i][S[g_i] > 0]; b = C[g_i][C[g_i] > 0]
    if len(a) > 1: alls.append(a.max() / a.min())
    if len(b) > 1: alld.append(b.max() / b.min())
print("  over all 29 goods: supply contrast %.0f..%.3g | demand contrast %.0f..%.3g"
      % (min(alls), max(alls), min(alld), max(alld)))

print(); print("=" * 96); print("4.  the caravan cap on both inland bases"); print("=" * 96)
import zipfile
SAVE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
z = zipfile.ZipFile(SAVE); t = z.read("gamestate").decode("latin-1"); z.close()
i = t.find("\ntrade={"); j = i + len("\ntrade="); d = 0; k = j
while k < len(t):
    if t[k] == "{": d += 1
    elif t[k] == "}":
        d -= 1
        if d == 0: break
    k += 1
tr = t[j:k + 1]
TOT, TOP = {}, {}
for m in re.finditer(r"\n\tnode=\{", tr):
    s = m.end() - 1; dd = 0; e = s
    while e < len(tr):
        if tr[e] == "{": dd += 1
        elif tr[e] == "}":
            dd -= 1
            if dd == 0: break
        e += 1
    b = tr[s:e + 1]; nm = re.search(r'definitions="([^"]+)"', b).group(1)
    pw = {mm.group(1): float(mm.group(2))
          for mm in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{[^{}]*?\n\t\t\tval=([\d.]+)', b)}
    if pw: TOT[nm] = sum(pw.values()); TOP[nm] = max(pw.values())
for label, nodes in (("flag (26)", flag_inland), ("derived (25)", derived_inland)):
    sh = sorted(50.0 / TOT[n] * 100 for n in nodes if n in TOT)
    tops = sorted(TOP[n] for n in nodes if n in TOT)
    beats = sum(1 for n in nodes if n in TOT and 50.0 > TOP[n])
    print("  %-13s n=%d | cap share %.1f%%..%.1f%% median %.1f%% | totals %.1f..%.1f | largest holder %.1f..%.1f | cap beats it in %d of %d"
          % (label, len([n for n in nodes if n in TOT]), min(sh), max(sh), sh[len(sh) // 2],
             min(TOT[n] for n in nodes if n in TOT), max(TOT[n] for n in nodes if n in TOT),
             min(tops), max(tops), beats, len([n for n in nodes if n in TOT])))
