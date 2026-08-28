# -*- coding: utf-8 -*-
"""Lead probe: Y1331/Y1332/Y1277 -- reconstruct node local_value from the save's
trade_goods_size arrays x current price, and compare to the engine's own field."""
import os, re, zipfile, collections
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SG  = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                   "Europa Universalis IV", "save games", "VANILLA_start.eu4")
tgt = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"), encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tgt, re.M)
print("goods in 00_tradegoods.txt:", len(ORDERG))
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
def mb(txt, i):
    d = 0; k = i; inq = False
    while k < len(txt):
        c = txt[k]
        if c == '"': inq = not inq
        elif not inq:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(txt) - 1
cur = {}
m0 = re.search(r"^change_price=\{", raw, re.M)
st = raw.index("{", m0.start()); pb = raw[st+1:mb(raw, st)]
for mm in re.finditer(r"^\t([a-z_]+)=\{", pb, re.M):
    s2 = pb.index("{", mm.start()); blk = pb[s2+1:mb(pb, s2)]
    cp = re.search(r"current_price=([\d.]+)", blk)
    if cp: cur[mm.group(1)] = float(cp.group(1))
print("prices parsed:", len(cur))
i2 = raw.index(chr(10) + "trade={"); j2 = raw.index("{", i2); tb = raw[j2+1:mb(tb0:=raw, j2)]
nodes = []
slotcount = collections.Counter()
allzero = None
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2 = tb.index("{", mm.start()); nd = tb[s2+1:mb(tb, s2)]
    name = re.search(r'definitions="([a-z_]+)"', nd)
    blk = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
    sz = [float(x) for x in blk.group(1).split()] if blk else []
    slotcount[len(sz)] += 1
    nz = set(k for k, v in enumerate(sz) if v)
    allzero = nz if allzero is None else (allzero | nz)
    lv = re.search(r"^\t\tlocal_value=([\d.eE+-]+)", nd, re.M)
    recon = sum(sz[k] * cur.get(ORDERG[k-1], 0.0) for k in range(1, min(len(sz), len(ORDERG)+1)) if sz[k])
    nodes.append((name.group(1) if name else "?", recon, float(lv.group(1)) if lv else None, sz))
print("node blocks:", len(nodes))
print("trade_goods_size slot-count distribution:", dict(slotcount))
NS = max(slotcount)
print("slots never nonzero on any node:", sorted(set(range(NS)) - allzero))
exact = 0; tot_r = 0.0; tot_e = 0.0; ratios = []; short = []
for name, recon, lv, sz in nodes:
    if lv is None: continue
    r12 = recon / 12.0
    tot_r += r12; tot_e += lv
    if abs(r12 - lv) < 0.005: exact += 1
    if lv > 0: ratios.append((round(recon / lv, 2), name))
    short.append((lv - r12, name, round(r12,2), round(lv,2)))
print("nodes reproducing local_value exactly (|d|<0.005) : %d of %d" % (exact, len(nodes)))
print("aggregate recon/12 = %.2f  engine local_value = %.2f  shortfall = %.2f%%"
      % (tot_r, tot_e, 100.0*(tot_r-tot_e)/tot_e))
rc = collections.Counter(r for r, n in ratios)
print("ratio (Sum size*price)/local_value histogram:", rc.most_common(8))
print("nodes at exactly 12.00x:", sum(1 for r, n in ratios if r == 12.00))
short.sort(reverse=True)
print("largest shortfalls (engine - recon/12):")
for d, n, a, b in short[:10]: print("   %-22s recon/12 %8.2f  engine %8.2f  short %8.2f" % (n, a, b, d))

print()
print("=== tolerance sensitivity for the 'reproduces exactly' count ===")
import math
vals = [(n, recon/12.0, lv) for n, recon, lv, sz in nodes if lv is not None]
print("nodes with local_value == 0 :", sum(1 for n,a,b in vals if b == 0))
print("nodes with recon == 0       :", sum(1 for n,a,b in vals if a == 0))
for tol in (1e-9, 1e-6, 1e-4, 1e-3, 5e-3, 1e-2):
    print("  abs tol %-8g -> %d of 80" % (tol, sum(1 for n,a,b in vals if abs(a-b) <= tol)))
for rt in (1e-9, 1e-6, 1e-4, 1e-3, 1e-2):
    print("  rel tol %-8g -> %d of 80" % (rt, sum(1 for n,a,b in vals if b>0 and abs(a-b)/b <= rt)))
print("save local_value decimals seen:", sorted({len(str(b).split('.')[-1]) for n,a,b in vals})[:6])
print()
print("nodes NOT exact at abs tol 5e-3:")
for n,a,b in vals:
    if abs(a-b) > 5e-3: print("   %-22s recon/12 %10.5f  engine %10.5f" % (n,a,b))
