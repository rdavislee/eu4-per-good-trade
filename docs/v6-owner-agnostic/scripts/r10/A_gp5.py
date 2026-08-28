import zipfile, re, os, collections
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
i = raw.index(chr(10) + "provinces={"); j = raw.index("{", i)
body = raw[j + 1:mb(raw, j)]
m = re.search(r"^-223=\{", body, re.M)
st = body.index("{", m.start()); rec = body[st+1:mb(body, st)]
k = rec.index("\t\ttrade=")
print("--- province 223 'trade=' value ---")
print(rec[k:k+120])
print()
# top-level trade block: node schema
i2 = raw.index(chr(10) + "trade={"); j2 = raw.index("{", i2)
tb = raw[j2+1:mb(raw, j2)]
m2 = re.search(r"^\tnode=\{", tb, re.M)
st2 = tb.index("{", m2.start()); node = tb[st2+1:mb(tb, st2)]
print("--- first node block, keys at depth 2 ---")
ks = re.findall(r"^\t\t([a-z_0-9]+)=", node, re.M)
print(sorted(set(ks)))
for key in ("definitions", "current", "local_value", "outgoing", "value_added_outgoing", "total", "provincial_trade_power", "max"):
    mm = re.search(r"^\t\t%s=(.*)$" % key, node, re.M)
    print("   %-24s %s" % (key, mm.group(1).strip() if mm else "ABSENT"))
