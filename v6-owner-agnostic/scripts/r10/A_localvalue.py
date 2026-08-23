import zipfile, re, os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import GOODS, PRICES, NIDX, ORDER
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
nodes = []
for m in re.finditer(r"^\tnode=\{", tb, re.M):
    st = tb.index("{", m.start()); nodes.append(tb[st+1:mb(tb, st)])
print("GOODS in solver order:", len(GOODS), GOODS)
rows = []
for nd in nodes:
    name = re.search(r'definitions="([^"]+)"', nd).group(1)
    lv = float(re.search(r"^\t\tlocal_value=(.*)$", nd, re.M).group(1))
    blk = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S).group(1)
    sz = [float(x) for x in blk.split()]
    rows.append((name, lv, sz))
print("slots per node:", len(rows[0][2]))
# try mapping slot i -> GOODS[i]
worst = 0.0; bad = 0
for name, lv, sz in rows:
    est = sum(sz[i] * PRICES[GOODS[i]] for i in range(min(len(sz), len(GOODS))) if GOODS[i] in PRICES)
    d = abs(est - lv)
    if d > 5e-3: bad += 1
    worst = max(worst, d)
    if name in ("sevilla", "genua", "african_great_lakes", "hangzhou"):
        print("  %-22s local_value=%8.3f  sum(size*price)=%8.3f  diff=%.4f" % (name, lv, est, d))
print("nodes off by >0.005:", bad, "of", len(rows), "| worst abs diff %.5f" % worst)
