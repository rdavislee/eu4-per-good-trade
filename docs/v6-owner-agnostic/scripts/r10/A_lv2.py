import zipfile, re, os, sys
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tg = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"), encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tg, re.M)
pr = open(os.path.join(EU4, "common", "prices", "00_prices.txt"), encoding="latin-1").read()
PRICE = {}
for m in re.finditer(r"^([a-z_]+) = \{(.*?)^\}", pr, re.M | re.S):
    b = re.search(r"base_price\s*=\s*([\d.]+)", m.group(2))
    if b: PRICE[m.group(1)] = float(b.group(1))
print("goods in file order:", len(ORDERG), ORDERG)
print("priced:", len(PRICE))
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
i2 = raw.index(chr(10) + "trade={"); j2 = raw.index("{", i2)
tb = raw[j2+1:mb(raw, j2)]
res = []
for m in re.finditer(r"^\tnode=\{", tb, re.M):
    st = tb.index("{", m.start()); nd = tb[st+1:mb(tb, st)]
    name = re.search(r'definitions="([^"]+)"', nd).group(1)
    lvm = re.search(r"^\t\tlocal_value=(.*)$", nd, re.M)
    lv = float(lvm.group(1)) if lvm else 0.0
    blk = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
    sz = [float(x) for x in blk.group(1).split()] if blk else []
    res.append((name, lv, sz, lvm is not None))
print("nodes:", len(res), "| slots:", len(res[0][2]), "| with local_value:", sum(1 for r in res if r[3]))
worst = 0.0; bad = []
for name, lv, sz, has in res:
    est = sum(sz[i] * PRICE.get(ORDERG[i], 0.0) for i in range(min(len(sz), len(ORDERG))))
    d = abs(est - lv)
    if d > 5e-3: bad.append((name, lv, est, d))
    worst = max(worst, d)
for name, lv, sz, has in res:
    if name in ("sevilla", "genua", "african_great_lakes", "hangzhou"):
        est = sum(sz[i] * PRICE.get(ORDERG[i], 0.0) for i in range(min(len(sz), len(ORDERG))))
        print("  %-22s local_value=%8.3f  sum(size*base_price)=%8.3f  diff=%.5f" % (name, lv, est, abs(est-lv)))
print("nodes off by >0.005:", len(bad), "of", len(res), "| worst abs diff %.5f" % worst)
for b in bad[:8]: print("   ", b)
