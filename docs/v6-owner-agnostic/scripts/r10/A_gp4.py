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
keys = collections.Counter()
recs = {}
for m in re.finditer(r"^-(\d+)=\{", body, re.M):
    st = body.index("{", m.start())
    rec = body[st + 1:mb(body, st)]
    recs[int(m.group(1))] = rec
    for k in re.findall(r"^\t\t([a-z_0-9]+)=", rec, re.M):
        keys[k] += 1
print("distinct top-level province keys:", len(keys))
prod = [k for k in keys if any(t in k for t in ("good", "produc", "trade", "value", "price"))]
print("keys mentioning good/produc/trade/value/price:")
for k in sorted(prod): print("   %-34s %d" % (k, keys[k]))
print()
print("full key list (count>=100):")
print("  " + ", ".join(sorted(k for k in keys if keys[k] >= 100)))
