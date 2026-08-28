import zipfile, re, os
SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                    "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
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
recs = {}
for m in re.finditer(r"^-(\d+)=\{", body, re.M):
    st = body.index("{", m.start())
    recs[int(m.group(1))] = body[st + 1:mb(body, st)]

def field(rec, key):
    g = re.search(r"^\t\t%s=\"?([A-Za-z0-9_.\-]+)" % key, rec, re.M)
    return g.group(1) if g else None

for pid in (223, 1747):
    r = recs[pid]
    print(pid, "local_autonomy:", field(r,"local_autonomy"), "base_tax:", field(r,"base_tax"),
          "base_production:", field(r,"base_production"), "trade_goods:", field(r,"trade_goods"))

# find GRA country record and its monarch personality
i2 = raw.index(chr(10)+"countries={")
j2 = raw.index("{", i2)
cbody = raw[j2+1:mb(raw,j2)]
m = re.search(r"\n\tGRA=\{", cbody)
st = cbody.index("{", m.start())
gra = cbody[st+1: mb(cbody, st)]
# find monarch block (first one, the ruler at game start)
mm = re.search(r"\tmonarch=\{", gra)
if mm:
    mst = gra.index("{", mm.start())
    monblk = gra[mst+1: mb(gra, mst)]
    print("--- GRA monarch block (first 1500 chars) ---")
    print(monblk[:1500])
