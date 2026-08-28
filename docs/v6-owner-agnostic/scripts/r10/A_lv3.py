import zipfile, re, os
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tg = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"), encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tg, re.M)
SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
def mb(s, i):
    d = 0; k = i; inq = False
    while k < len(s):
        c = s[k]
        if c == '"': inq = not inq
        elif not inq:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1
# ---- current prices from the save
m = re.search(r"^change_price=\{", raw, re.M)
st = raw.index("{", m.start()); pb = raw[st+1:mb(raw, st)]
CUR = {}
for mm in re.finditer(r"^\t([a-z_]+)=\{", pb, re.M):
    s2 = pb.index("{", mm.start()); blk = pb[s2+1:mb(pb, s2)]
    cp = re.search(r"current_price=([\d.]+)", blk)
    if cp: CUR[mm.group(1)] = float(cp.group(1))
print("current prices parsed:", len(CUR))
print("  sample:", {k: CUR[k] for k in list(ORDERG)[:6] if k in CUR})
# ---- nodes
i2 = raw.index(chr(10) + "trade={"); j2 = raw.index("{", i2)
tb = raw[j2+1:mb(raw, j2)]
res = []
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2 = tb.index("{", mm.start()); nd = tb[s2+1:mb(tb, s2)]
    name = re.search(r'definitions="([^"]+)"', nd).group(1)
    lvm = re.search(r"^\t\tlocal_value=(.*)$", nd, re.M)
    blk = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
    sz = [float(x) for x in blk.group(1).split()] if blk else []
    res.append((name, float(lvm.group(1)) if lvm else 0.0, sz))
worst = 0.0; bad = []
for name, lv, sz in res:
    est = sum(sz[i] * CUR.get(ORDERG[i-1], 0.0) for i in range(1, min(len(sz), len(ORDERG)+1))) / 12.0
    d = abs(est - lv)
    if d > 1e-3: bad.append((name, lv, round(est, 4), round(d, 4)))
    worst = max(worst, d)
    if name in ("sevilla", "genua", "african_great_lakes", "hangzhou"):
        print("  %-22s local_value=%8.3f  sum(size*current_price)/12=%8.4f  diff=%.5f" % (name, lv, est, d))
print("nodes off by >0.001:", len(bad), "of", len(res), "| worst %.5f" % worst)
for b in bad[:10]: print("   ", b)

tl = sum(r[1] for r in res)
te = sum(sum(r[2][i] * CUR.get(ORDERG[i-1], 0.0) for i in range(1, min(len(r[2]), len(ORDERG)+1))) / 12.0 for r in res)
print()
print("world sum local_value        = %.3f /month" % tl)
print("world sum size*price/12      = %.3f /month" % te)
print("gap                          = %+.3f  (%.2f%% of local_value)" % (te - tl, 100.0*(te-tl)/tl))
print("nodes exact to 1e-3          = %d of %d" % (sum(1 for r in res if abs(sum(r[2][i]*CUR.get(ORDERG[i-1],0.0) for i in range(1,min(len(r[2]),len(ORDERG)+1)))/12.0 - r[1]) <= 1e-3), len(res)))
