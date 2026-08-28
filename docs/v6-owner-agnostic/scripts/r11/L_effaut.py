# -*- coding: utf-8 -*-
"""Lead probe (Y1275, Y1341): does vanilla's node trade_goods_size carry local autonomy
or production efficiency?  Singleton (node,good) cells only, so the engine's node sum is
attributable to one province."""
import os, re, zipfile, collections, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + os.sep + "..")
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import ROWS, GOODS_PRODUCED_FACTOR
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tg = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"), encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tg, re.M)
SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
def mb(s, i):
    d = 0; k = i; q = False
    while k < len(s):
        c = s[k]
        if c == '"': q = not q
        elif not q:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1
# --- per-province local_autonomy and owner from the save
i1 = raw.index(chr(10) + "provinces={"); j1 = raw.index("{", i1); pb = raw[j1+1:mb(raw, j1)]
AUT = {}; OWN = {}
for mm in re.finditer(r"^-(\d+)=\{", pb, re.M):
    pid = int(mm.group(1)); s2 = pb.index("{", mm.start()); blk = pb[s2+1:mb(pb, s2)]
    a = re.search(r"^\t\tlocal_autonomy=([\d.]+)", blk, re.M)
    o = re.search(r'^\t\towner="([A-Z]{3})"', blk, re.M)
    AUT[pid] = float(a.group(1)) if a else 0.0
    if o: OWN[pid] = o.group(1)
# --- per-country adm_tech (production efficiency's main 1444 source)
i3 = raw.index(chr(10) + "countries={"); j3 = raw.index("{", i3); cb = raw[j3+1:mb(raw, j3)]
TECH = {}
for mm in re.finditer(r'^\t([A-Z]{3})=\{', cb, re.M):
    s2 = cb.index("{", mm.start()); blk = cb[s2+1:mb(cb, s2)]
    t = re.search(r"adm_tech=(\d+)", blk)
    if t: TECH[mm.group(1)] = int(t.group(1))
# --- engine node x good quantity
i2 = raw.index(chr(10) + "trade={"); j2 = raw.index("{", i2); tb = raw[j2+1:mb(raw, j2)]
ENG = {}
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2 = tb.index("{", mm.start()); nd = tb[s2+1:mb(tb, s2)]
    nm = re.search(r'definitions="([a-z_]+)"', nd).group(1)
    b = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
    sz = [float(x) for x in b.group(1).split()] if b else []
    for k in range(1, min(len(sz), len(ORDERG)+1)):
        if sz[k]: ENG[(nm, ORDERG[k-1])] = sz[k]
# --- model rows grouped into (node,good) cells
cells = collections.defaultdict(list)
for r in ROWS: cells[(r["node"], r["good"])].append(r)
sing = {k: v[0] for k, v in cells.items() if len(v) == 1 and k in ENG}
print("singleton (node,good) cells with an engine quantity: %d" % len(sing))
rows = []
for k, r in sing.items():
    pred = GOODS_PRODUCED_FACTOR * r["gp"] / GOODS_PRODUCED_FACTOR  # r["gp"] already = 0.2*bp*(1+mod)
    pred = r["gp"]
    ratio = ENG[k] / pred if pred > 0 else None
    if ratio is None: continue
    rows.append((k[0], k[1], r["pid"], AUT.get(r["pid"], 0.0),
                 TECH.get(OWN.get(r["pid"], ""), None), pred, ENG[k], ratio))
def pear(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    sx = math.sqrt(sum((x-mx)**2 for x in xs)); sy = math.sqrt(sum((y-my)**2 for y in ys))
    if sx == 0 or sy == 0: return float("nan")
    return sum((x-mx)*(y-my) for x, y in zip(xs, ys))/(sx*sy)
aut = [r[3] for r in rows]; rat = [r[7] for r in rows]
print("cells with ratio engine/model == 1.000 exactly : %d of %d"
      % (sum(1 for r in rows if abs(r[7]-1.0) < 1e-9), len(rows)))
print()
print("--- WAY 1 (save): local autonomy ---")
print("  provinces with local_autonomy > 0 : %d" % sum(1 for a in aut if a > 0))
print("  max local_autonomy in the sample  : %.1f%%" % max(aut))
print("  Pearson r(local_autonomy, engine/model ratio) = %+.4f" % pear(aut, rat))
hi = [r for r in rows if r[3] >= 50.0]
print("  cells with autonomy >= 50%%        : %d ; of those ratio==1.000 : %d"
      % (len(hi), sum(1 for r in hi if abs(r[7]-1.0) < 1e-9)))
for r in sorted(hi, key=lambda z: -z[3])[:5]:
    print("     %-20s %-12s pid %-5d autonomy %5.1f%%  model %.3f engine %.3f ratio %.4f"
          % (r[0], r[1], r[2], r[3], r[5], r[6], r[7]))
print()
print("--- WAY 2 (save): production efficiency, via owner adm_tech ---")
tr = [(r[4], r[7]) for r in rows if r[4] is not None]
print("  cells with a known owner adm_tech : %d ; tech range %d..%d"
      % (len(tr), min(t for t, _ in tr), max(t for t, _ in tr)))
print("  Pearson r(owner adm_tech, engine/model ratio) = %+.4f"
      % pear([t for t, _ in tr], [x for _, x in tr]))
byt = collections.defaultdict(list)
for t, x in tr: byt[t].append(x)
for t in sorted(byt): print("     adm_tech %-3d n=%-4d mean ratio %.4f" % (t, len(byt[t]), sum(byt[t])/len(byt[t])))
