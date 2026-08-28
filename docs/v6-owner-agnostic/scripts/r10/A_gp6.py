import zipfile, re, os
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
print("node blocks:", len(nodes))
n = nodes[0]
k = n.index("\t\ttrade_goods_size=")
print("--- african_great_lakes trade_goods_size ---")
print(n[k:k+320])
# sevilla
for nd in nodes:
    if 'definitions="sevilla"' in nd:
        k = nd.index("\t\ttrade_goods_size=")
        print("--- sevilla trade_goods_size ---")
        print(nd[k:k+320])
        for key in ("local_value", "total", "current"):
            mm = re.search(r"^\t\t%s=(.*)$" % key, nd, re.M)
            print("   sevilla %-14s %s" % (key, mm.group(1).strip()))
        break
