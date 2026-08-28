import zipfile, re, os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
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
print("province records:", len(recs))

def field(rec, key):
    g = re.search(r"^\t\t%s=\"?([A-Za-z0-9_.\-]+)" % key, rec, re.M)
    return g.group(1) if g else None

# 1. province 1 base_tax
print("prov 1 base_tax:", field(recs[1], "base_tax"))
# 2. devastation on the 11
DEV = {266:50.0,2968:50.0,2970:50.0,4724:50.0,4725:50.0,265:20.0,267:20.0,1771:20.0,2967:20.0,4237:20.0,4726:20.0}
devs = {}
for pid in sorted(DEV):
    devs[pid] = field(recs[pid], "devastation")
print("devastation of the 11:", devs)
# any other province with devastation?
other = [p for p, r in recs.items() if field(r, "devastation") and p not in DEV]
print("other provinces with devastation:", other[:20], "count", len(other))
# 3. coal producers in save
coal = [p for p, r in recs.items() if field(r, "trade_goods") == "coal"]
print("coal producers in save:", coal)
# 4. history-vs-save comparison on counted provinces
PROV = {int(k): v for k, v in json.load(open(os.path.join(HERE, "prov1444.json"))).items()}
ND = json.load(open(os.path.join(HERE, "nodes.json")))
PNODE = {}
for n in ND["order"]:
    for p in ND["nodes"][n]["members"]:
        PNODE[p] = n
counted = [p for p, s in PROV.items() if s.get("owner") and p in PNODE]
print("counted provinces (history parse):", len(counted))
mismatch = {"base_tax": [], "base_production": [], "owner": [], "trade_goods": []}
unknown_hist = []
for p in counted:
    s = PROV[p]; r = recs.get(p)
    if r is None:
        print("MISSING in save:", p); continue
    bt = float(field(r, "base_tax") or 0); bp = float(field(r, "base_production") or 0)
    ow = field(r, "owner"); tg = field(r, "trade_goods")
    if abs(bt - s["base_tax"]) > 1e-9: mismatch["base_tax"].append((p, s["base_tax"], bt))
    if abs(bp - s["base_production"]) > 1e-9: mismatch["base_production"].append((p, s["base_production"], bp))
    if ow != s["owner"]: mismatch["owner"].append((p, s["owner"], ow))
    hg = s.get("trade_goods")
    if hg in (None, "unknown"):
        unknown_hist.append((p, tg))
    elif hg != tg:
        mismatch["trade_goods"].append((p, hg, tg))
for k, v in mismatch.items():
    print("mismatch", k, ":", len(v), v[:5])
print("history-unknown counted provinces:", len(unknown_hist))
tally = collections.Counter(g for _, g in unknown_hist)
print("rolled tally:", dict(tally))
